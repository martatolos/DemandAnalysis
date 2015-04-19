import visualizations as visual
from inflation import Inflation
from monthlypowerconsumptions import MonthlyPowerConsumptions
from hourlypowerconsumptions import HourlyPowerConsumptions
from gdp import GDP
from population import Population
from unemployment import Unemployment

# Plots
import matplotlib.pyplot as plt
import matplotlib


dir_path = "/Users/marta/Box Sync/ProjecteFinal/all-country-data"
patternM = "/Monthly_*.xls"

dir_path_inflation = '/Users/marta/Box Sync/ProjecteFinal/eurostats/Inflation/'
inflation_file = 'inflation_tec00118.xlsx'


dir_gdp = "/Users/marta/Box Sync/ProjecteFinal/eurostats/_GDP/"
#filegdp = "tec00114"
filegdp = "tec00115"

filepop = "tps00001"
dir_pop = "/Users/marta/Box Sync/ProjecteFinal/eurostats/_Population/"

fileun = "tsdec450"
dir_un = "/Users/marta/Box Sync/ProjecteFinal/eurostats/_Unemployment/"



dir_path = "/Users/marta/Box Sync/ProjecteFinal/all-country-data"
patternM = "/Monthly_*.xls"
patternH = "/Hourly_*.xls"

dir_path_inflation = '/Users/marta/Box Sync/ProjecteFinal/eurostats/Inflation/'
inflation_file = 'inflation_tec00118.xlsx'


# Monthly consumption
mpc = MonthlyPowerConsumptions(dir_path, patternM, skiprows=7)

# Read inflation, gdp, pop, un
inflation = Inflation(dir_path_inflation, inflation_file)
gdp = GDP(dir_gdp, filegdp)
pop = Population(dir_pop, filepop)
un = Unemployment(dir_un, fileun)

# Hourly consumption
hpc = HourlyPowerConsumptions(dir_path, patternH, save=True)



# Console
# execfile('Cargar.py')