# Plots
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import re
import random


def plot_several_countries(df, ylabel, title, country_list="", save=False, num="", xticks_hourly=False, kind='bar', linestyle='-', color='mbygcr', marker='o', linewidth=4.0, fontsize=16, legend=True):
    """
    This function plots a dataframe with several countries
    @param df: data frame
    @param ylabel: label for y axis
    @param title: graphic title
    @param kind: graphic type ex: bar or line
    @param linestyle: lines style
    @param color: color to use
    @param marker: shape of point on a line
    @param linewidth: line width
    @param fontsize: font size
    @return: n/a
    """

    # Plotting
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}

    matplotlib.rc('font', **font)

    if xticks_hourly:
        xticks_hourly = range(0,24)
    else:
        xticks_hourly = None

    ### PLOT FINAL
    if kind == 'line':
        graphic = df.plot(title=title, kind=kind, fontsize=fontsize, linestyle=linestyle, color=color,
                          linewidth=linewidth, marker=marker, xticks=xticks_hourly, figsize=(18,9))
    else:
        graphic = df.plot(title=title, kind=kind, fontsize=fontsize, color=color,
                          xticks=xticks_hourly, figsize=(18,9))
    if legend == False:
        graphic.legend_.remove()
    graphic.set_ylabel(ylabel)
    graphic.legend(prop={'size': 12})


    if save==True and country_list!="":
        namefile= re.sub("[\'\",\[\]]", "", str(country_list))
        namefile= re.sub("[\s+]", "-", namefile)
        if num=="":
            num = random.randrange(1,100)
        plt.savefig(namefile+str(num))
    else:
        plt.show()


def plot_yearly_consumption(df, country, kind='bar', linestyle='-', color='blue', marker='o', linewidth=4.0,fontsize=16):

    """
    This function plots the yearly data from a monthlypowerconsumptions data frame
    @param df: monthlypowerconsumptions data frame
    @param df: country name to add on the title of the plot
    @return: n/a
    """

    # Plotting
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}

    matplotlib.rc('font', **font)

    ### PLOT FINAL
    if kind == 'line':
        graphic = df.plot(x='year', y='Sum', title='Evolution of electricity consumption in '+ country, kind=kind, fontsize=fontsize, linestyle=linestyle, color=color , marker=marker)
    else:
        graphic = df.plot(x='year', y='Sum', title='Evolution of electricity consumption in '+ country, kind=kind, fontsize=fontsize, color=color)
    graphic.set_ylabel('GWh')
    plt.show()

def plot_monthly_average_consumption(mpc, country_list, ylabel='normalized', title='', kind='bar', linestyle='-', color='mbygcr', marker='o', linewidth=4.0, fontsize=16, legend=True):
    """
    This function plots the yearly data from a monthlypowerconsumptions object
    @param df: monthlypowerconsumptions object
    @param country_list: country names to add on the title of the plot
    @param ylabel: label for y axis
    @param title: graphic title
    @param kind: graphic type ex: bar or line
    @param linestyle: lines style
    @param color: color to use
    @param marker: shape of point on a line
    @param linewidth: line width
    @param fontsize: font size
    @return: n/a
    """

    # Plotting
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}

    matplotlib.rc('font', **font)

    df = mpc.data_normalization(year=False)
    df = df.groupby('country').mean()
    del df['year']
    del df['Sum']
    df = df.T
    plot_several_countries(df[country_list], ylabel, title, kind=kind, linestyle=linestyle, color=color, marker=marker, linewidth=linewidth, fontsize=fontsize, legend=legend)


def plot_average_week(df, ylabel='Normalized', title="Normalized average weekday consumption",kind='bar', color='rbbbbgg', rotation=50, legend=True):
    # Plotting
    """

    @param df: Data frame with the values to plot
    @param ylabel: Label for the y axis
    @param title: Title for the graphic
    @param kind: Type of graphic: bar, line,...
    @param color: color values
    @param rotation: degrees for the ylabel rotation
    @param legend: True or False legend on or off
    """
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 12}

    matplotlib.rc('font', **font)

    #create a dictionary for the week days
    dayDict={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thrusday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
    df = df[['Country', 'weekday', 'daily']]
    df = df.pivot(index='weekday', columns='Country')
    df = df.rename(index=dayDict)
    df.columns = df.columns.droplevel()
    # normalized
    df = df/df.mean()


    graphic = df.plot(title=title, kind=kind, color=color, legend=legend)
    graphic.set_ylabel(ylabel)
    graphic.legend(prop={'size': 12})
    plt.xticks(rotation=rotation)
    plt.show()



# #### PLOT FINAL
# # Plot the infaltion with the spanish consumption
# ES_info_year = ES_info[['year','Sum','inflation']]
# ES_info_year.set_index('year')
# plt.figure()
# ax = ES_info_year.plot(x='year', title='Consumption and Inflation in Spain', y='Sum', kind='bar',fontsize=16)
# ax.set_ylabel('Consumption - GWh')
# ax2 = ax.twinx()
# ax2.plot(ES_info_year['inflation'].values, linestyle='-', color='red', marker='o', linewidth=4.0)
# ax2.set_ylabel('Inflation - Annual Change [%]')
# plt.show()