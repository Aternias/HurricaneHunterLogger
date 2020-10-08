import __main__
import numpy


def parse():
    count = 0
    for line in __main__.lineLex:
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
            __main__.time_past.append(int(obs_time))
            print('(Time): ' + obs_time_ref_est)

            # Aircraft Height (Feet)
            obs_height = line_data[4]
            int(obs_height)
            print('(Aircraft Height): ' + obs_height + ' ft')

            # Extrapolated Sea Pressure (mB)
            obs_expressure = line_data[5]
            if '/' in obs_expressure:
                obs_expressure_print = '///'
                __main__.sfc_pressure.append(float(0))
            else:
                obs_expressure_print = (obs_expressure[:3] + '.' + obs_expressure[3:])
                if obs_expressure_print[0:1] == '0':
                    obs_expressure_print = ('1' + obs_expressure[:3] + '.' + obs_expressure[3:])
                __main__.sfc_pressure.append(float(obs_expressure_print))
                __main__.sfc_pressure_intervals.append(float(obs_expressure_print))
            print('(Extrapolation Sea Pressure): ' + obs_expressure_print + ' mB')

            # Flight Level Wind 10s-average (mph)
            __main__.obs_fl_wind = line_data[9]
            __main__.fl_wind = __main__.np.append(__main__.fl_wind, int(__main__.obs_fl_wind))
            __main__.fl_wind = __main__.fl_wind.astype(int)
            print('(Flight Level Wind): ' + __main__.obs_fl_wind + ' Mph')

            print('')

        count = count + 1
