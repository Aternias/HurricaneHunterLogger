import time
from selenium import webdriver
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.pyplot as plt
import matplotlib.colors as colors


# Get Latest Recon Data. Compare last recon with current recon.
# If time from last data is current data, do nothing. If no data
# recieved within the last 30 minutes, set mission to Finished.
def getRecon(driver):
    # driver.delete_all_cookies()
    # driver.get('https://www.nhc.noaa.gov/text/URNT15-NOAA.shtml')
    # getFlightLog = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/pre').text

    # f = open("dataBuffer.txt", "w") # a appends instead of overwriting
    # f.write(getFlightLog)
    # f.close()

    # open and read the file after the appending:
    f = open("dataBuffer.txt", "r")
    print(f.readline(1))


def formatRecon():
    None


# driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
# driver.minimize_window()
# getRecon(driver)
# driver.quit()

time_past = []
sfc_pressure = []
sfc_pressure_intervals = []
sfc_pressure_range = []
fl_wind = np.array([])

f = open("dataBuffer.txt", "r")
print(f.readline(0))
lineLex = f.readlines()

count = 0
# Strips the newline character
for line in lineLex:
    sep2 = ' '

    # GetFlightInfo
    if count == 2:
        sep1 = '  '
        mission = line.split(sep1, 1)[0]
        callsign = mission.split(sep2)[0]
        flight_id = mission.split(sep2)[1]
        storm_name = mission.split(sep2)[2]

        print("(Callsign): " + callsign)
        print("(Flight ID): " + flight_id)
        print("(Storm): " + storm_name)

        HDOB = line.split(sep1, 1)[1]
        REFORMATTED_HDOB = HDOB.split(sep1)[6]
        obs_num = REFORMATTED_HDOB.split(sep2)[1]
        date = REFORMATTED_HDOB.split(sep2)[2]

        print("(Observation #): " + obs_num)
        print("(Date): " + "{}-{}-{}".format(date[4:6], date[6:8], date[0:4]))
        print("")

    elif count != 0 and count != 1:

        # Time
        line_data = line.split(sep2)
        obs_time = line_data[0]
        obs_time_ref = "{}:{}:{}".format(obs_time[0:2], obs_time[2:4], obs_time[4:6])
        hour_1 = obs_time_ref[0:1]
        hour_2 = obs_time_ref[1:2]
        hour_1_new = (int(hour_1) / 2).__trunc__()
        hour_2_new = int(hour_2) - 2
        obs_time_ref_est = "{}{}:{}:{}".format(hour_1_new, hour_2_new, obs_time[2:4], obs_time[4:6])
        time_past.append(int(obs_time))
        #print('(Time): ' + obs_time_ref_est)

        # Aircraft Height (Feet)
        obs_height = line_data[4]
        int(obs_height)
        #print('(Aircraft Height): ' + obs_height + ' ft')

        # Extrapolated Sea Pressure (mB)
        obs_expressure = line_data[5]
        if '/' in obs_expressure:
            obs_expressure_print = '///'
            sfc_pressure.append(float(0))
        else:
            obs_expressure_print = (obs_expressure[:3] + '.' + obs_expressure[3:])
            if obs_expressure_print[0:1] == '0':
                obs_expressure_print = ('1' + obs_expressure[:3] + '.' + obs_expressure[3:])
            sfc_pressure.append(float(obs_expressure_print))
            sfc_pressure_intervals.append(float(obs_expressure_print))
        #print('(Extrapolation Sea Pressure): ' + obs_expressure_print + ' mB')

        # Flight Level Wind 10s-average (mph)
        obs_fl_wind = line_data[9]
        fl_wind = np.append(fl_wind, int(obs_fl_wind))
        fl_wind = fl_wind.astype(int)
        #print('(Flight Level Wind): ' + obs_fl_wind + ' Mph')

        #print('')

    count = count + 1





sfc_pressure_range = sfc_pressure_intervals
sfc_pressure_intervals = max(sfc_pressure_intervals) - min(sfc_pressure_intervals)

#print(sfc_pressure)

# y_1 == Wind Data
# x_1 == Time Data
# x_2 == Pressure Data

# Evenly spaced horizontal time intervals.
obs_time_rg = (max(time_past) - min(time_past))/48.5
x_1_bounds = np.linspace(min(time_past), max(time_past), dtype=int)
#print(x_1)
# Evenly spaced vertical intervals from minimum surface pressure to maximum surface pressure
sfcp_bounds = np.linspace(min(sfc_pressure_range), max(sfc_pressure_range), num=int(sfc_pressure_intervals)+2, dtype=int)
fl_wind_rg = np.amax(fl_wind) - np.amin(fl_wind) + 1
flw_bounds = np.linspace(min(fl_wind), max(fl_wind), num=fl_wind_rg, dtype=int)
print(fl_wind)


plt.plot(time_past, fl_wind)
plt.axis([min(time_past), max(time_past), min(fl_wind), max(fl_wind)])
plt.ylabel('Flight Lvl-wind 10s')
plt.xlabel('Time')
plt.show()

#cmap = ListedColormap(['#0095ff', '#00ff2f', '#f6ff00', 'orange', '#ff3636', '#fa70e5'])
#norm = BoundaryNorm([0, 38, 73, 95, 130, 155, 200], cmap.N)
#fig.colorbar(line, ax=axs[0])