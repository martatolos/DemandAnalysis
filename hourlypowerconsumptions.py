"""
This module provides functions to parse data from https://www.entsoe.eu/
to a Pandas DataFrame
"""
__author__ = 'mtolos'
__version__ = "1.0"
__email__ = "mtolos@tid.es"

# import packages for analysis and modeling
# data frame operations
import pandas as pd
# pathname pattern expansion
import glob
# dates treatment
import datetime
import os
# regular expressions
import re


class HourlyPowerConsumptions(object):
    """
        This class contains all the structures and functions to handle
        hourly power consumptions data
    """
    DEFAULT_ENCODING = 'UTF-8'

    # constructor
    def __init__(self, dir_path, pattern, sheet='Statistics', skiprows=9,
                 maxcolumns=26, hourchange='3B:00:00'):
        """
        Constructor
        @param dir_path: The path where to search for the files
        @param pattern: The pattern of the xlsx files to be read
        @param sheet: The sheet to be read
        @param skiprows: rows to skip from the excel file
        @param maxcolumns: max number of columns that should appear on the
        excel file (except for months with hour change)
        @param hourchange: label showing the hour change that makes a new
        column on the worksheet and should be treated
        @return: A Pandas DataFrame object with the hourly consumption
        """

        # check if there is a saved data frame with the values
        if os.path.isfile(os.path.join(dir_path, 'hconsum')):
            self.df = pd.read_pickle(os.path.join(dir_path, 'hconsum'))
        else:
            self.load_dataframe(dir_path, pattern, sheet, skiprows,
                                maxcolumns, hourchange)

    # load data frame from files
    def load_dataframe(self, dir_path, pattern, sheet='Statistics', skiprows=9,
                       maxcolumns=26, hourchange='3B:00:00'):
        """
        This function parses hourly (1:24) consumption data from
        all countries and returns a Pandas DataFrame with the
        following schema:
        (Country, Day, H01, H02,...,H24, date, weekday,month, year)
        @param dir_path: The path where to search for the files
        @param pattern: The pattern of the xlsx files to be read
        @param sheet: The sheet to be read
        @param skiprows: rows to skip from the excel file
        @param maxcolumns: max number of columns that should appear on the
        excel file (except for months with hour change)
        @param hourchange: label showing the hour change that makes a new
        column on the worksheet and should be treated
        @return: A Pandas DataFrame object with the hourly consumption
        for all countries and all dates
        """

        print('_' * 80)

        # create a DataFrame
        self.df = pd.DataFrame()

        # search for the files to load
        for file_name in glob.glob(dir_path + pattern):

            print file_name

            # read excel file
            wb = pd.read_excel(file_name, sheet, skiprows=skiprows,
                               na_values=[u'n.a.'], keep_default_na=False)

            # check if there are more than maxcolumns since
            # it means a change of hour
            if len(wb.columns) != maxcolumns:
                # take out the change of hour
                del wb[hourchange]
                # change columns name for 3A:00 to 3:00
                wb = wb.rename(columns=lambda x:
                re.sub(r'^(\d{1})A:.+', 'H0\\1', x))

            # change columns names if they are hours for H01, H02,...
            wb = wb.rename(columns=lambda x: re.sub(r'^(\d{2}):.+', 'H\\1', x))

            # remove rows if they have too many NaN (at least the 23 non NaN)
            wb = wb.dropna(thresh=23)

            # fill missing values from the change of hour in march at 3:00
            wb = wb.fillna(method='pad', axis='columns')

            # create new column as a date object
            wb['date'] = pd.to_datetime(wb['Day'])


            # Add new columns with info about weekday, month and year
            wb['weekday'] = wb.date.apply(lambda x: x.weekday())
            wb['month'] = wb.date.apply(lambda x: x.month)
            wb['year'] = wb.date.apply(lambda x: x.year)

            # Append to the self.df data frame
            self.df = self.df.append(wb)

        # change hourly consumptions data type to float
        # self.df.iloc[:, 2:26] = self.df.iloc[:, 2:26].astype(float)

        # save the data frame for latter use, to avoid reading all files again
        self.df.to_pickle(os.path.join(dir_path, 'hconsum'))


    def historical_daily_aggregates(self, country, year, num_years=3):
        """
        Obtain a new data frame with historical daily aggregate consumption
        for a specific country
        @rtype : data frame
        @param country: Country to select. Ex: "ES" for Spain
        @param year: reference year to compute the historical data
        @param num_years: Number of previous years to get the historical
        @return data frame with the daily aggregated consumption
        """

        df = self.df.copy(deep=True)

        # Select the years to consider
        df = df[df.year.isin(range(year - num_years, year + 1))]

        # Select the country to work with
        df = df[df.Country == country]

        # Set index to make operations easier
        df = df.set_index(['Country', 'year', "month",
                           "weekday", "date", "Day"])

        # Compute daily consumption
        df["Consumption"] = df.sum(axis='columns')

        # reset index to give a plain data frame
        df = df.reset_index()

        # return only the selected columns
        return df[['date', 'weekday', 'month', 'year', 'Consumption']]

    def normalized_hourly_country_data(self, country):

        """
        This function selects only the data from a country and normalizes based
        on the daily consumption, thus, the hourly consumptions per day are
        shown as values between [0,1]
        @param country: Country to select
        @return: data frame with the country normalized hourly consumptions
        """
        df = self.df.copy(deep=True)

        # Select values only for this country
        df = df[df.Country == country]

        # Set index to make computations easier
        df = df.set_index(['Country', 'year', "month",
                           "weekday", "date", "Day"])

        # Do normalization based on the daily consumption
        daily_consumption = df.sum(axis=1)
        df = df.div(daily_consumption, axis='index')

        # return the dataframe
        return df
