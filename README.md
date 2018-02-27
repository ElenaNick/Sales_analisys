Sales_analisys
Analysis of sales record using time sliding window

The program opens TRD.csv file that contains list of trades description in the format:
trade time, share price, number of shares, exchange character

The program reads the information from the file line by line and finds the 1 second window during which the largest
amount of trades was made. It also finds such the 1 second window for each exchange.

The algorithm:
Trades are read line by line. The trade read is added to the end of a list of trades in current time window. 
The current window start time is the time of first trade in the list, stop time is (start time + 1).

While trades time read is less than stop time, the counter for all trades and for particular exchange trades are incremented.

Once the time read is greater or equal to the current stop time, it's time to move the sliding window. First the counters
are compared to current maximum trades counts for all exchanges and each exchange separately. If current count is greater 
than saved max, the max and window times of the max are updated. Than the window is moved by removing trades from 
the front of the trades list, while decrementing counters for all trades and the removed trade. The new first trade's
time is used as new start time, and new stop time is calculated. This is repeated till the new stop time is greater than
time of the last read trade, or till only one element left in the list(which is the last trade read). I.e. the window is moved
till the last trade can fit inside new time window.

The process is repeated till all trade are read from the file.
Then the results are printed out to a console.


Time complexity:
O(n), where n is number of trades in the file: with each line read the trade is either added to the list, or trades 
are removed from the list with counters updated. Thus for each line in the file, a trade will be added to the list, and 
than removed from the list (except last time window trades) resulting in O(2n +C) operations -> O(n) time complexity.

Space complexity:
O(m), where m is the largest number of trades made in 1 second window: the counter and max trades lists take fixed space
(27 elements). The list of trades in the current window theoretically can go as long as n for small ns.


P.S.: the program was written for a particular TRD.csv file, for which I had to fight with encoding, hence cutting out
"\ufeff" out of time string on line 22 and checking trades char length on line 23