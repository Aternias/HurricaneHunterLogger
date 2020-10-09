import numpy as np
import matplotlib.pyplot as plt
from selenium import webdriver
import module.file_parser as file_parser
import datetime

global driver
driver = webdriver.Chrome()


# Get Latest Recon Data. Compare last recon with current recon.
# If time from last data is current data, do nothing. If no data
# recieved within the last 30 minutes, set mission to Finished.
def getRecon(driver):
    driver.delete_all_cookies()
    driver.get('https://www.nhc.noaa.gov/text')
    # URNT15-USAF.shtml <-- AF309 Aircraft 1
    # URNT15-NOAA.shtml <-- NOAA9 Aircraft 1
    # MIAREPNT1.shtml <-- RECCO OBSERVATIONS
    # MIAREPNT2.shtml <-- CENTER CIRCULATION DATA
    # MIAREPNT3.shtml <-- DROPSONDE DATA

    pathDate = '/html/body/table/tbody/tr[{}]/td[{}]'

    # Checking For File With Valid Name And Soonest Last Modified Date. (ONLY GETS 1 ELEMENT AS OF NOW)
    row_count = driver.execute_script("return document.getElementsByTagName('tr').length") - 4
    validAircraft = ['URNT15-USAF.shtml'] # [usaf_aircraft_1, noaa_aircraft_1]
    logElementPosition = []
    logElementTime = []
    logElementName = []
    global getLogTime
    xtest = 4
    while xtest <= row_count:
        for item in validAircraft:
            if item.find(driver.find_element_by_xpath('/html/body/table/tbody/tr[{}]/td[2]/a'.format(xtest)).text) > -1:
                getLogTime = driver.find_element_by_xpath('/html/body/table/tbody/tr[{}]/td[{}]'.format(xtest, 3)).text
                # Remove All Unwanted Characters
                for i in [' ', '-', ':']:
                    getLogTime = getLogTime.replace(i, '')
                getLogTime = int(getLogTime)
                logElementPosition.append(xtest)
                logElementTime.append(getLogTime)
                logElementName.append(driver.find_element_by_xpath('/html/body/table/tbody/tr[{}]/td[2]/a'.format(xtest)).text)
        xtest = xtest + 1
    print(logElementPosition)
    print(logElementTime)
    dataPage = 'https://www.nhc.noaa.gov/text/{}'.format(logElementName[0])
    driver.get(dataPage)

    getFlightLog = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/pre').text

    f = open("dataBuffer.txt", "w")  # a appends instead of overwriting
    f.write(getFlightLog)
    f.close()


global time_past
time_past = []
global sfc_pressure
sfc_pressure = []
global sfc_pressure_range
sfc_pressure_range = []
global sfc_pressure_intervals
sfc_pressure_intervals = []
global fl_wind
fl_wind = []
global lineLex
global buffer
buffer = []


def main():
    global driver
    global lineLex
    global buffer
    global sfc_pressure_range
    global sfc_pressure_intervals
    global fl_wind
    # driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    #driver.minimize_window()
    getRecon(driver)
    # driver.quit()

    f = open("dataBuffer.txt", "r")
    buffer = f.readlines()
    f.close()

    file_parser.appendLogs(False)
    file_parser.loadLogs()
    # sfc_pressure_range = sfc_pressure_intervals
    # sfc_pressure_intervals = max(sfc_pressure_intervals) - min(sfc_pressure_intervals)

    # y_1 == Wind Data
    # x_1 == Time Data
    # x_2 == Pressure Data

    # Evenly spaced horizontal time intervals.
    # obs_time_rg = (max(time_past) - min(time_past)) / 48.5
    # x_1_bounds = np.linspace(min(time_past), max(time_past), dtype=int)
    # print(x_1)
    # Evenly spaced vertical intervals from minimum surface pressure to maximum surface pressure
    # sfcp_bounds = np.linspace(min(sfc_pressure_range), max(sfc_pressure_range), num=int(sfc_pressure_intervals) + 2, dtype=int)
    # fl_wind_rg = np.amax(fl_wind) - np.amin(fl_wind) + 1
    # flw_bounds = np.linspace(min(fl_wind), max(fl_wind), num=fl_wind_rg, dtype=int)
    # print(fl_wind)

    plt.plot(time_past, fl_wind)
    plt.axis([min(time_past), max(time_past), min(fl_wind), max(fl_wind)])
    plt.ylabel('Flight Lvl-wind 10s')
    newXtick = []
    for idx, val in enumerate(time_past):
        if idx % 5 == 0:
            newXtick.append(val)
    plt.xticks(newXtick)
    plt.xlabel('Time')
    plt.show()

    # cmap = ListedColormap(['#0095ff', '#00ff2f', '#f6ff00', 'orange', '#ff3636', '#fa70e5'])
    # norm = BoundaryNorm([0, 38, 73, 95, 130, 155, 200], cmap.N)
    # fig.colorbar(line, ax=axs[0])


if __name__ == "__main__":
    main()
