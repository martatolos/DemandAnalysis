"""
This module provides functions to parse data from https://www.entsoe.eu/
to a Pandas DataFrame
"""
__author__ = 'mtolos'
__version__ = "1.1"
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
# import datetime for dealing with time expressions
import datetime

class MonthlyPowerConsumptions(object):
    """
        This class contains all the structures and functions to handle
        hourly power consumptions data
    """
    DEFAULT_ENCODING = 'UTF-8'

    #_monthDict={'1':'Jan', '2':'Feb', '3':'Mar', '4':'Apr', '5':'May', '6':'Jun', '7':'Jul', '8':'Aug', '9':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}


    # constructor
    def __init__(self, dir_path, pattern, sheet='Statistics', skiprows=7,save=1):
        """
        Constructor
        @param dir_path: The path where to search for the files
        @param pattern: The pattern of the xlsx files to be read
        @param sheet: The sheet to be read
        @param skiprows: rows to skip from the excel file
        @return: A Pandas DataFrame object with the hourly consumption
        """

        # check if there is a saved data frame with the values
        if os.path.isfile(os.path.join(dir_path, 'mconsum')):
            self.df = pd.read_pickle(os.path.join(dir_path, 'mconsum'))
        else:
            self.load_dataframe(dir_path, pattern, sheet, skiprows, save=save)

    # load data frame from files
    def load_dataframe(self, dir_path, pattern, sheet='Statistics',
                       skiprows=7, save=1):
        """
        This function parses monthly (1:12) consumption data from
        all countries and returns a Pandas DataFrame with the
        following schema:
        (Country, Sum, M1, M2,...,M24)
        @param dir_path: The path where to search for the files
        @param pattern: The pattern of the xlsx files to be read
        @param sheet: The sheet to be read
        @param save: Save a pickle of the dataframe to not read xls again
        @return: A Pandas DataFrame object with the monthly consumption
        for all countries and all dates
        """

        global year
        print('_' * 80)

        # create a DataFrame
        self.df = pd.DataFrame()

        # search for the files to load
        for file_name in glob.glob(dir_path + pattern):

            print file_name

            # read excel file first only to get the year
            wb = pd.read_excel(file_name, sheet)
            # get year
            if wb.iloc[1, 0] == "Year:":
                year = wb.iloc[1, 1]

            # read excel file this time to get the right format skipping rows
            wb = pd.read_excel(file_name, sheet, skiprows=skiprows,
                               na_values=[u'n.a.'], keep_default_na=False)


            # add year to data frame
            wb['year'] = year

            # Append to the self.df data frame
            self.df = self.df.append(wb)

        # change monthly consumptions data type to float
        self.df.iloc[:, 1:14] = self.df.iloc[:, 1:14].astype(float)

        #monthDict={'1':'Jan', '2':'Feb', '3':'Mar', '4':'Apr', '5':'May', '6':'Jun', '7':'Jul', '8':'Aug', '9':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
        ## change columns names if they are months for a meanfull name
        #self.df = self.df.rename(columns=monthDict)
        # rename Country to country
        self.df = self.df.rename(columns=lambda x: re.sub('Country', 'country', str(x)))

        # save the data frame for latter use, to avoid reading all files again
        if save == 1:
            self.df.to_pickle(os.path.join(dir_path, 'mconsum'))

    def arrange_months_names(self):
        """
        This function changes the columns names to month names instead of numbers
        @param n/a
        @return: data frame with the df with the new columns names
        """
        df = self.df.copy(deep=True)

        monthDict={'1':'Jan', '2':'Feb', '3':'Mar', '4':'Apr', '5':'May', '6':'Jun', '7':'Jul', '8':'Aug', '9':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
        df = df.rename(columns=monthDict)

        return df

    def normalized_monthly_country_data(self, country):

        """
        This function selects only the data from a country and normalizes based
        on the yearly consumption, thus, the monthly consumptions per year are
        shown as values between [0,1]
        @param country: Country to select
        @return: data frame with the country normalized monthly consumptions
        """
        df = self.arrange_months_names()

        # Select values only for this country
        df = df[df.country == country]

        # Set index to make computations easier
        df = df.set_index(['country', 'year'])

        # Do normalization based on the yearly consumption
        yearly_consumption = df.sum(axis=1)
        df = df.div(yearly_consumption, axis='index')

        # return the dataframe
        return df

    def get_yearly_consumption_countries(self, country_list, normalized=False, year=""):
        """
        This function gets the yearly consumption from the list of countries given
        @param countries: list of countries example ['ES','PT']
        @param normalized: True if normalized data
        @para year: default "" all years, if year set, then from this year on
        @return: data frame with the countries yearly consumption. Ex: [year, ES, PT]
        """

        if normalized==True:
            df = self.data_normalization(year=True, country_list=country_list)
            df = pd.DataFrame(df.unstack(), columns=['Sum']).reset_index()
            df = df.pivot(index='year', columns='country', values='Sum')

        else:
            df = self.select_countries_data(country_list)
            df = df.pivot(index='year', columns='country', values='Sum')

        # select the years
        df = df[df.index>= year]

        return df

    def select_country_data(self, country):

        """
        This function selects the monthly data from a country
        @param country: Country to select
        @return: data frame with the country data
        """
        df = self.arrange_months_names()

        # Select values only for this country
        df = df[df.country == country]

        # return the dataframe
        return df

    def select_countries_data(self, country_list):
        """
        This function selects the monthly data from several countries
        @param country_list: A list of countries for example ['ES','PT']
        @return: data frame with the countries data
        """
        df = self.arrange_months_names()

        if country_list != '':
            # Select values only for this country
            df = df[df.country.isin(country_list)]

        # return the dataframe
        return df

    def transform_monthly_data(self):
        """
        This function arranges the monthly data for processing
        @param none:
        @return: data frame with the arrange monthly data
        """

        df = self.arrange_months_names()

        # Take out the sum of the year
        del df['Sum']
        df = df.set_index(['year', 'country'])
        df = df.T
        df = df.unstack()
        df.index.names = ['year', 'country', 'month']

        # return the dataframe
        return df

    def data_normalization(self, year=True, how='mean', country_list=''):
        """
        This function normalized the data based on the "how" given
        @param how: mean, max, value (another information given by country in a dictionary)
        @param year: True or False (year or not, then month data, default year data)
        @param country_list: List of countries to select if different from ''
        @return: data frame with normalized data
        """
        df = self.select_countries_data(country_list=country_list)

        if how == 'mean':

            if year==True:

                # Normalize year data base on mean value for all the years for each country
                df_year = df.pivot(index='country', columns='year', values='Sum')
                df_year_means = df_year.mean(axis=1)
                df_year = df_year.div(df_year_means, axis='index')
                df = df_year

            else:
                # Normalize monthly data base on the yearly sum
                df_month = df.copy()
                df_month.loc[:,"Jan":"Dec"] = df_month.loc[:,"Jan":"Dec"].div(df_month['Sum'], axis=0)
                df = df_month

        else:
            print "WARNING: Don't know how to do this normalization... returning the dataframe as it is...\n"

        # return the dataframe
        return df

def data_normalization(self, year=True, how='mean', country_list=''):
        """
        This function normalized the data based on the "how" given
        @param how: mean, max, value (another information given by country in a dictionary)
        @param year: True or False (year or not, then month data, default year data)
        @param country_list: List of countries to select if different from ''
        @return: data frame with normalized data
        """
        df = self.select_countries_data(country_list=country_list)

        if how == 'mean':

            if year==True:

                # Normalize year data base on mean value for all the years for each country
                df_year = df.pivot(index='country', columns='year', values='Sum')
                df_year_means = df_year.mean(axis=1)
                df_year = df_year.div(df_year_means, axis='index')
                df = df_year

            else:
                # Normalize monthly data base on the yearly sum
                df_month = df.copy()
                df_month.loc[:,"Jan":"Dec"] = df_month.loc[:,"Jan":"Dec"].div(df_month['Sum'], axis=0)
                df = df_month

        else:
            print "WARNING: Don't know how to do this normalization... returning the dataframe as it is...\n"

        # return the dataframe
        return df

def get_monthly_consumption_countries(self, country_list, normalized=False):

        if normalized==False:
            df = self.select_countries_data(country_list=country_list)
            df = df.loc[:,"Jan":"Dec"]

        else:
            df = self.data_normalization(year=False, how='mean', country_list=country_list)

        return df


