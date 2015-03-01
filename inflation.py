"""
This module provides functions to parse inflation data from eurostats
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


class Inflation(object):
    """
        This class contains all the structures and functions to handle
        inflation data from several countries
    """
    DEFAULT_ENCODING = 'UTF-8'

    # constructor
    def __init__(self, dir_path, filename):
        """
        Constructor
        @param dir_path: The path where to search for the files
        @param filename: The file to be read
        @return: A Pandas DataFrame object with inflation data
        """

        # check if there is a saved data frame with the values
        if os.path.isfile(os.path.join(dir_path, 'inflation')):
            self.df = pd.read_pickle(os.path.join(dir_path, 'inflation'))
        else:
            self.load_dataframe(dir_path, filename)

    # load data frame from file
    def load_dataframe(self, dir_path, filename, save=0):
        """
        This function parses inflation data from
        all countries and returns a Pandas DataFrame with the
        following schema:
        (Country, year1, year2,....)
        @param dir_path: The path where to search for the files
        @param filename: The file to be read
        @param save: Save a pickle of the dataframe to not read xls again
        @return: A Pandas DataFrame object with the inflation data
        for all countries and years available
        """

        # create a DataFrame
        self.df = pd.DataFrame()

        # read excel file
        self.df = pd.read_excel(dir_path+filename)

        # rename columns
        self.df = self.df.rename(columns = {u'geo\\time':'country'})

        # prepare dataframe
        # transpose
        self.df = self.df.T
        self.df.columns = self.df.loc['country']
        self.df = self.df.drop('country')
        self.df = self.df.reset_index()
        self.df = self.df.rename(columns = {u'index':'year'})
        self.df.columns.names = ['']

        # save the data frame for latter use, to avoid reading all files again
        if save == 1:
            self.df.to_pickle(os.path.join(dir_path, 'inflation'))

        # return dataframe
        return self.df



    def select_country_data(self, country):

        """
        This function selects the monthly data from a country
        @param country: Country to select
        @return: data frame with the country data
        """
        df = self.df.copy(deep=True)

        # Select the country inflation data
        df = df[['year', country]]
        df = df.rename(columns = {'ES':'inflation'})
        df['inflation'] = df['inflation'].astype(float)
        df = df.set_index('year')

        # return the dataframe
        return df

    def select_countries_data(self, country_list):
        """
        This function selects the monthly data from several countries
        @param country_list: A list of countries for example ['ES','PT']
        @return: data frame with the countries data
        """
        df = self.df.copy(deep=True)

        # Select values only for this country
        df[country_list] = df[country_list].astype(float)
        country_list.append('year')
        df = df[country_list]
        df = df.set_index('year')

        # return the dataframe
        return df
