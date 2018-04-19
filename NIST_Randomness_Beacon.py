#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import xml.dom.minidom
import argparse
import requests
import os
import collections



class Bgcolors:
    def __init__(self):
        self.get = {
            'HEADER': '\033[95m',
            'OKBLUE': '\033[94m',
            'OKGREEN': '\033[92m',
            'WARNING': '\033[93m',
            'FAIL': '\033[91m',
            'ENDC': '\033[0m',
            'BOLD': '\033[1m',
            'UNDERLINE': '\033[4m'
        }


def timestamp_epoch(t_epoch):
    array_with_timestamp = []

    t = time.strptime(t_epoch, "%m/%d/%Y %H:%M")
    timestamp = int(time.mktime(t))
    array_with_timestamp.append(timestamp)

    return array_with_timestamp


def time_epoch(from_epoch, to_epoch):
    array_with_timestamp = []

    if (from_epoch is not None) and (to_epoch is not None):
        from_time_epoch = time.strptime(from_epoch, "%m/%d/%Y %H:%M")
        from_timestamp_epoch = int(time.mktime(from_time_epoch))
        to_time_epoch = time.strptime(to_epoch, "%m/%d/%Y %H:%M")
        to_timestamp_epoch = int(time.mktime(to_time_epoch))
        if (int(from_timestamp_epoch) == 1378395540) or (int(to_timestamp_epoch) == 1378395540):
            print ('Sorry, but the timestamp for this date is can not be used...')
            print('Please change --from or --to date!')
            exit(0)
        else:
            interval = int(from_timestamp_epoch)
            while True:
                array_with_timestamp.append(interval)
                interval += 60
                if interval == to_timestamp_epoch:
                    break

    return array_with_timestamp


def beacon_outputValue(t_epoch, from_epoch, to_epoch):
    array_with_beacon_outputValue = []
    if (from_epoch is not None) and (to_epoch is not None):
        timestamps = time_epoch(from_epoch, to_epoch)
    else:
        timestamps = timestamp_epoch(t_epoch)

    dir_path = "./timestamps/"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(dir_path, 'has been created')

    beacon_url = "https://beacon.nist.gov/rest/record/"
    for stamp in timestamps:
        print(stamp)
        r = requests.get(str(beacon_url) + str(stamp))
        dom = xml.dom.minidom.parseString(r.text)

        f = open(dir_path + str(stamp) + '.html', 'wb')
        f.write(dom.toprettyxml().encode('utf-8'))
        f.close()
        # can be read from a file
        # doc = xml.dom.minidom.parse('./timestamps/'+ str(stamp) + '.html')
        # doc.getElementsByTagName returns NodeList
        # name = doc.getElementsByTagName("outputValue")[0]
        # print(name.firstChild.data)

        doc = xml.dom.minidom.parseString(dom.toprettyxml().encode('utf-8'))
        output_value = doc.getElementsByTagName("outputValue")[0]
        # print(output_value.firstChild.data)
        array_with_beacon_outputValue.append(output_value.firstChild.data)

    return array_with_beacon_outputValue


def work_with_beacon_outputValue(t_epoch, from_epoch, to_epoch):
    array_with_beacon_outputValue = beacon_outputValue(t_epoch, from_epoch, to_epoch)

    joinedList = ""
    for array in array_with_beacon_outputValue:
        joinedList += (str(array))
    print (joinedList)

    # results = collections.Counter(joinedList)
    # print(results)

    dd = {}
    for c in joinedList:
        try:
            dd[c] += 1
        except:
            dd[c] = 1

    for k in dd.keys():
        print ("%s, %d" % (k, dd[k]))


    for array_with_beacon in array_with_beacon_outputValue:
        print (array_with_beacon)

        #results = collections.Counter(str(array_with_beacon))
        #print(results)

        d = {}
        for string_array in str(array_with_beacon):
            try:
                d[string_array] += 1
            except:
                d[string_array] = 1

        for k in d.keys():
            print ("%s, %d" % (k, d[k]))


    return work_with_beacon_outputValue


def main():

    start__time = time.time()

    parser = argparse.ArgumentParser(prog='python3 script_name.py -h',
                                     usage='python3 script_name.py {ARGS}',
                                     add_help=True,
                                     prefix_chars='--/',
                                     epilog='''created by Vitalii Natarov''')
    parser.add_argument('--version', action='version', version='v1.0.0')
    parser.add_argument('--time', '--t', nargs='+', dest='time', help='Enter time epoch. Ex: 09/30/2013 00:15',
                        default='09/30/2013 00:15')
    parser.add_argument('--from', dest='from_epoch', help='Enter time epoch (from)', default=None)
    parser.add_argument('--to', dest='to_epoch', help='Enter time epoch (to)', default=None)

    results = parser.parse_args()
    t_epoch = results.time
    from_epoch = results.from_epoch
    to_epoch = results.to_epoch

    if (from_epoch is not None) and (to_epoch is not None):
        # print(time_epoch(from_epoch, to_epoch))
        work_with_beacon_outputValue(t_epoch, from_epoch, to_epoch)
    else:
        # print(timestamp_epoch(t_epoch))
        work_with_beacon_outputValue(t_epoch, from_epoch, to_epoch)

    end__time = round(time.time() - start__time, 2)
    print("--- %s seconds ---" % end__time)

    print(
        Bgcolors().get['OKGREEN'], "============================================================",
        Bgcolors().get['ENDC'])
    print(
        Bgcolors().get['OKGREEN'], "==========================FINISHED==========================",
        Bgcolors().get['ENDC'])
    print(
        Bgcolors().get['OKGREEN'], "============================================================",
        Bgcolors().get['ENDC'])


if __name__ == '__main__':
    main()
