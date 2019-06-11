#!/usr/bin/python

import sys, getopt
import cbpro
import datetime, time

public_client = cbpro.PublicClient()

def history_data(pair, start=None, end=None, granularity=3600):
    data = []
    if start is not None and end is not None:
        diff = (end - start) / granularity
        if diff > 300:
            data += history_data(pair, start, end - 300 * granularity, granularity)
    hist = public_client.get_product_historic_rates(pair.upper(), start=start, end=end, granularity=granularity)
    for i in range(len(hist)):
        date = datetime.datetime.utcfromtimestamp(hist[i][0]).strftime('%Y-%m-%d %I-%p')
        data.append([date, pair.upper().replace('-', ''), hist[i][3], hist[i][2], hist[i][1], hist[i][4], round(hist[i][5], 2), round(hist[i][5] * (hist[i][3] + hist[i][4]) / 2, 2)])
    return data


def history(pair, start=None, end=datetime.datetime.now(), granularity=3600):
    if start is not None:
        start = time.mktime(time.strptime(start, '%Y/%m/%d %H:%M'))
    if end is not None:
        end = time.mktime(time.strptime(end, '%Y/%m/%d %H:%M'))
    print('start', start)
    print('end', end)
    hist = history_data(pair, start, end, granularity)
    print(*['Date','Symbol','Open','High','Low','Close','Volume BTC','Volume USD'], sep=',')
    for i in range(len(hist)):
        print(*hist[i], sep=',')

def main(argv):
    pair = ''
    op = ''
    start = None
    end = datetime.datetime.now().strftime('%Y/%m/%d %H:%M')
    granularity = 3600
    try:
        opts, args = getopt.getopt(argv, "hp:cs:e:g:")
    except getopt.GetoptError:
        print('cb-utils.py -p pair -start "yyyy/mm/dd hh:mm" -end "yyyy/mm/dd hh:mm" -granularity 3600 -c')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            op = 'usage'
        elif opt in ("-p", "--pair"):
            pair = arg
        elif opt in ("-c", "--history"):
            op = 'hist'
        elif opt in ("-s", "--start"):
            start = arg
        elif opt in ("-e", "--end"):
            end = arg
        elif opt in ("-g", "--granularity"):
            granularity = arg
    if op == 'usage':
        print('cb-utils.py -p pair -start "yyyy/mm/dd hh:mm" -end "yyyy/mm/dd hh:mm" -granularity 3600 -c')
        sys.exit()
    elif op == 'hist':
        history(pair, start, end, granularity)
    else:
        print('pair is', pair.upper())


if __name__ == "__main__":
    main(sys.argv[1:])
