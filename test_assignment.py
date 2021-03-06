import csv
from datetime import datetime, timedelta
import codecs

with codecs.open('TRD.csv', 'rU', 'utf_16') as csvfile:
    readCSV = csv.reader(csvfile)
    init_time = datetime.strptime("0:0:0.0", "%H:%M:%S.%f")
    # format of list: start time, stop time, trades count
    # exchanges[0] = all exchanges, then A, B, C ... Z
    exchanges = [[init_time, init_time, 0] for x in range(27)]

    # initialize data containers
    # counts of trades for exchanges for current sliding window
    current_window_count = [0 for x in range(27)]
    # list of trades in the current window, the first trade in the list has the current window start time
    current_window_trades = []
    # current stop time - just outside of the sliding window
    current_stop_time = datetime.strptime("0:0:0.0", "%H:%M:%S.%f")

    # read each row in the file and process
    for row in readCSV:
        time_read = datetime.strptime(row[0].replace("\ufeff", ""), "%H:%M:%S.%f")
        if len(row[3]) == 1:
            trade_char = row[3]
        else:
            for c in row[3]:
                if c.isalpha():
                    trade_char = c

        # add new trade to the trades list
        current_window_trades.append([time_read, trade_char])
        # if we are still in the current window - add the trade to list of current window trades
        # and increment corresponding counters
        if time_read < current_stop_time:
            current_window_count[0] += 1
            current_window_count[ord(trade_char)-64] += 1
        else:
            # time to move the sliding time window
            # first check if current counts are greater than saved max counts
            for i in range(27):
                if exchanges[i][2] < current_window_count[i]:
                    exchanges[i][0] = current_window_trades[0][0]
                    exchanges[i][1] = current_stop_time - timedelta(seconds=0.001)
                    exchanges[i][2] = current_window_count[i]

            # than decrease counts for the exchanges in the current_window_trades list till we find new time window so
            # that newly read time could fit in or till the list has just 1 element (just added)
            while time_read >= current_stop_time and len(current_window_trades) > 1:
                current_window_count[0] -= 1
                current_window_count[ord(current_window_trades[0][1]) - 64] -= 1
                current_window_trades.pop(0)
                current_stop_time = current_window_trades[0][0] + timedelta(seconds=1)
            # if just added trade was more than 1s away from other trades in the list, it's the only one left in
            # the list now
            if time_read >= current_stop_time:
                current_stop_time = current_window_trades[0][0] + timedelta(seconds=1)

            # increase count for total and for newly added trade
            current_window_count[0] += 1
            current_window_count[ord(trade_char) - 64] += 1

    # check if current counts are greater than saved max counts - after the file was read to the end
    for i in range(27):
        if exchanges[i][2] < current_window_count[i]:
            exchanges[i][0] = current_window_trades[0][0]
            exchanges[i][1] = current_stop_time - timedelta(seconds=0.001)
            exchanges[i][2] = current_window_count[i]

    # print out results
    print("Max trades in 1 second time interval for all exchanges is from {} to {}. During this interval {} trades "
          "took place".format(exchanges[0][0].strftime("%H:%M:%S.%f"), exchanges[0][1].strftime("%H:%M:%S.%f"),
                              exchanges[0][2]))
    print("Results by exchange:")
    for i in range (1, 27):
        if exchanges[i][2] > 0:
            print("{}: from {} to {}, {} trades".format(chr(i+64), exchanges[i][0].strftime("%H:%M:%S.%f"),
                                                        exchanges[i][1].strftime("%H:%M:%S.%f"), exchanges[i][2]))
