import __main__
import numpy
import math

global log

# def parse():
#     global date_month
#     global date_day
#     global date_year_last2
#     count = 0
#     for line in __main__.lineLex:
#         date = ''
#         sep2 = ' '
#         # GetFlightInfo
#         if count == 2:
#             sep1 = '  '
#             mission = line.split(sep1, 1)[0]
#             callsign = mission.split(sep2)[0]
#             flight_id = mission.split(sep2)[1]
#             storm_name = mission.split(sep2)[2]
#
#             print("(Callsign): " + callsign)
#             print("(Flight ID): " + flight_id)
#             print("(Storm): " + storm_name)
#
#             HDOB = line.split(sep1, 1)[1]
#             REFORMATTED_HDOB = HDOB.split(sep1)[6]
#             obs_num = REFORMATTED_HDOB.split(sep2)[1]
#             date = REFORMATTED_HDOB.split(sep2)[2]
#
#             date_month = date[4:6]
#             date_day = date[6:8]
#             date_year_last2 = date[2:4]
#
#             print("(Observation #): " + obs_num)
#             print("(Date): " + "{}-{}-{}".format(date[4:6], date[6:8], date[0:4]))
#             print("")
#
#         elif count != 0 and count != 1 and "$" not in line and ";" not in line:
#
#             # Time
#             line_data = line.split(sep2)
#             obs_time = line_data[0]
#             obs_time_ref = "{}:{}:{}".format(obs_time[0:2], obs_time[2:4], obs_time[4:6])
#             hour_1 = obs_time_ref[0:1]
#             hour_2 = obs_time_ref[1:2]
#             hour_1_new = (int(hour_1) / 2).__trunc__()
#             hour_2_new = int(hour_2) - 2
#             obs_time_ref_est = "{}{}:{}:{}".format(hour_1_new, hour_2_new, obs_time[2:4], obs_time[4:6])
#             __main__.time_past.append(int(obs_time))
#             print('(Time): ' + obs_time_ref_est + ' EST')
#
#             # Aircraft Height (Feet)
#             # obs_height = line_data[4]
#             # int(obs_height)
#             # print('(Aircraft Height): ' + obs_height + ' ft')
#
#             # Extrapolated Sea Pressure (mB)
#             obs_expressure = line_data[5]
#             if '/' in obs_expressure:
#                 obs_expressure_print = '///'
#                 __main__.sfc_pressure.append(float(0))
#             else:
#                 obs_expressure_print = (obs_expressure[:3] + '.' + obs_expressure[3:])
#                 if obs_expressure_print[0:1] == '0':
#                     obs_expressure_print = ('1' + obs_expressure[:3] + '.' + obs_expressure[3:])
#                 __main__.sfc_pressure.append(float(obs_expressure_print))
#                 __main__.sfc_pressure_intervals.append(float(obs_expressure_print))
#             # print('(Extrapolation Sea Pressure): ' + obs_expressure_print + ' mB')
#
#             # Flight Level Wind 10s-average (mph)
#             __main__.obs_fl_wind = line_data[9]
#             __main__.obs_fl_wind = float(__main__.obs_fl_wind)
#             __main__.obs_fl_wind = math.trunc(__main__.obs_fl_wind * 1.15078)
#             __main__.fl_wind = __main__.np.append(__main__.fl_wind, int(__main__.obs_fl_wind)).astype(int)
#             print('(Flight Level Wind): ' + str(int(__main__.obs_fl_wind)) + ' Mph')
#
#             print('')
#
#         count = count + 1


def appendLogs(doAppend):
    count = 0
    global log
    global date_month
    global date_day
    global date_year_last2
    for idx, val in enumerate(__main__.buffer):
        date = ''
        sep2 = ' '
        # GetFlightInfo
        if count == 2:
            sep1 = '  '
            mission = val.split(sep1, 1)[0]
            callsign = mission.split(sep2)[0]
            flight_id = mission.split(sep2)[1]
            storm_name = mission.split(sep2)[2]
            HDOB = val.split(sep1, 1)[1]
            REFORMATTED_HDOB = HDOB.split(sep1)[6]
            obs_num = REFORMATTED_HDOB.split(sep2)[1]
            date = REFORMATTED_HDOB.split(sep2)[2]
            date_month = date[4:6]
            date_day = date[6:8]
            date_year_last2 = date[2:4]

        elif count != 0 and count != 1 and "$" not in val and ";" not in val and doAppend == True:
            # Append Buffer To Logs
            log = open('data_logs/logs-{month}-{day}-{year}.dat'.format(month=date_month, day=date_day, year=date_year_last2),'a+')
            log.write(val)
            print(val)
            log.close()
        count = count + 1
    __main__.buffer.clear()


def loadLogs():
    global date_month
    global date_day
    global date_year_last2
    global log
    count = 0
    log = open('data_logs/logs-{month}-{day}-{year}.dat'.format(month=date_month, day=date_day, year=date_year_last2),'r')
    __main__.lineLex = log.readlines()
    for line in __main__.lineLex:
        date = ''
        sep2 = ' '
        # GetFlightInfo
        # Time
        line_data = line.split(sep2)
        obs_time = line_data[0]
        obs_time_ref = "{}:{}:{}".format(obs_time[0:2], obs_time[2:4], obs_time[4:6])
        hour_1 = obs_time_ref[0:1]
        hour_2 = obs_time_ref[1:2]
        hour_1_new = (int(hour_1) / 2).__trunc__()
        hour_2_new = int(hour_2) - 2
        obs_time_ref_est = "{}{}:{}:{}".format(hour_1_new, hour_2_new, obs_time[2:4], obs_time[4:6])
        __main__.time_past.append(str(obs_time))

        # Flight Level Wind 10s-average (mph)
        __main__.obs_fl_wind = line_data[9]
        __main__.obs_fl_wind = float(__main__.obs_fl_wind)
        __main__.obs_fl_wind = __main__.obs_fl_wind * 1.15078
        __main__.fl_wind.append(round(__main__.obs_fl_wind, 1))

        count = count + 1
    print(__main__.fl_wind)
