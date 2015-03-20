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


class Population(object):
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
        @return: A Pandas DataFrame object with population data
        """

        # check if there is a saved data frame with the values
        if os.path.isfile(os.path.join(dir_path, 'popu')):
            self.df = pd.read_pickle(os.path.join(dir_path, 'popu'))
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
        self.df = pd.read_csv(dir_path+filename, sep='\t')

        # arrange country name
        self.df.iloc[:,0] = self.df.iloc[:,0].apply(lambda x: x.split(',')[1])

        # rename the columns (it only changes the fist one)
        self.df = self.df.rename(columns=lambda x: re.sub(r'^\D+', 'country', x))

        # prepare dataframe
        # take out non float values
        self.df.replace("\s*[bep]\s*", "" ,inplace=True, regex=True)
        self.df.replace("\s*:\s*", "NaN" ,inplace=True, regex=True)

        # prepare dataframe
        # transpose
        self.df = self.df.T
        self.df.columns = self.df.loc['country']
        self.df = self.df.drop('country')
        self.df = self.df.reset_index()
        self.df = self.df.rename(columns = {u'index':'year'})
        self.df.columns.names = ['']

        self.df = self.df.set_index('year')
        # save the data frame for latter use, to avoid reading all files again
        if save == 1:
            self.df.to_pickle(os.path.join(dir_path, 'population'))

        # return dataframe
        return self.df



    def select_countries_data(self, country_list):
        """
        This function selects the monthly data from several countries
        @param country_list: A list of countries for example ['ES','PT']
        @return: data frame with the countries data
        """
        df = self.df.copy(deep=True)

        # Select values only for this country
        df[country_list] = df[country_list].astype(float)
        df = df[country_list]

        # return the dataframe
        return df
