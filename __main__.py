import numpy as np
import matplotlib.pyplot as plt
from module.file_parser import parse


# Get Latest Recon Data. Compare last recon with current recon.
# If time from last data is current data, do nothing. If no data
# recieved within the last 30 minutes, set mission to Finished.
# def getRecon(driver):
#     driver.delete_all_cookies()
#     driver.get('https://www.nhc.noaa.gov/text/URNT15-NOAA.shtml')
#     getFlightLog = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/pre').text
#
#     f = open("dataBuffer.txt", "w")  # a appends instead of overwriting
#     f.write(getFlightLog)
#     f.close()
#
#     # open and read the file after the appending:
#     f = open("dataBuffer.txt", "r")
#     print(f.readline(1))

global time_past
time_past = []
global sfc_pressure
sfc_pressure = []
global sfc_pressure_range
sfc_pressure_range = []
global sfc_pressure_intervals
sfc_pressure_intervals = []
global fl_wind
fl_wind = np.array([])
global lineLex
lineLex = ''

def main():
    global lineLex
    global sfc_pressure_range
    global sfc_pressure_intervals
    # driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    # driver.minimize_window()
    # getRecon(driver)
    # driver.quit()

    f = open("dataBuffer.txt", "r")
    print(f.readline(0))
    lineLex = f.readlines()

    count = 0

    parse()

    sfc_pressure_range = sfc_pressure_intervals
    sfc_pressure_intervals = max(sfc_pressure_intervals) - min(sfc_pressure_intervals)

    # print(sfc_pressure)

    # y_1 == Wind Data
    # x_1 == Time Data
    # x_2 == Pressure Data

    # Evenly spaced horizontal time intervals.
    obs_time_rg = (max(time_past) - min(time_past)) / 48.5
    x_1_bounds = np.linspace(min(time_past), max(time_past), dtype=int)
    # print(x_1)
    # Evenly spaced vertical intervals from minimum surface pressure to maximum surface pressure
    sfcp_bounds = np.linspace(min(sfc_pressure_range), max(sfc_pressure_range), num=int(sfc_pressure_intervals) + 2,
                              dtype=int)
    fl_wind_rg = np.amax(fl_wind) - np.amin(fl_wind) + 1
    flw_bounds = np.linspace(min(fl_wind), max(fl_wind), num=fl_wind_rg, dtype=int)
    print(fl_wind)

    plt.plot(time_past, fl_wind)
    plt.axis([min(time_past), max(time_past), min(fl_wind), max(fl_wind)])
    plt.ylabel('Flight Lvl-wind 10s')
    plt.xlabel('Time')
    plt.show()

    # cmap = ListedColormap(['#0095ff', '#00ff2f', '#f6ff00', 'orange', '#ff3636', '#fa70e5'])
    # norm = BoundaryNorm([0, 38, 73, 95, 130, 155, 200], cmap.N)
    # fig.colorbar(line, ax=axs[0])


if __name__ == "__main__":
    main()
