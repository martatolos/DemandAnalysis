# Plots
import matplotlib.pyplot as plt
import matplotlib


def plot_several_countries(df, ylabel, title, kind='bar', linestyle='-', color='mbygcr', marker='o', linewidth=4.0, fontsize=16, legend=True):
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

    ### PLOT FINAL
    if kind == 'line':
        graphic = df.plot(title=title, kind=kind, fontsize=fontsize, linestyle=linestyle, color=color , marker=marker)
    else:
        graphic = df.plot(title=title, kind=kind, fontsize=fontsize, color=color)
    if legend == False:
        graphic.legend_.remove()
    graphic.set_ylabel(ylabel)
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
    df = mpc.data_normalization(year=False)
    df = df.groupby('country').mean()
    del df['year']
    del df['Sum']
    df = df.T
    plot_several_countries(df[country_list], ylabel, title, kind=kind, linestyle=linestyle, color=color, marker=marker, linewidth=linewidth, fontsize=fontsize, legend=legend)
