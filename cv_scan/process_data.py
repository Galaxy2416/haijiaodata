#!/usr/bin/env python3

import argparse
import glob
import re
import csv
import math
import os

def main():
    parser = argparse.ArgumentParser(description='parameters')
    parser.add_argument('--ph', type=float, help='The ph value [0-14]', required=True)
    parser.add_argument('--line', type=int, help='The line start to process', required=True)
    parser.add_argument('--data', type=str, help='The folder of the data with *.csv', required=True)
    parser.add_argument('--output', type=str, help='the output file', required=True)
    args = parser.parse_args()

    path = os.path.join(args.data, '*.csv')
    print(path)

    if not os.path.isdir(args.data):
        print('The {} is not valid dir'.format(args.data))

    os.chdir(args.data)

    files = glob.glob(r'*.csv')
    print(files)
    rpms = {}

    n = 0
    pattern = re.compile(r'scans-([0-9]+)')
    for f in files:
        print('Processing the file "{}"'.format(f))
        title = int(pattern.search(f).group(1))
        with open(f) as fd:
            reader = csv.reader(fd)
            rows = [row for idx, row in enumerate(reader) if idx >= args.line-1]
            rpms[title] = rows
            if n == 0:
                n = len(rows)
            assert(n == len(rows))

    rpms = dict(sorted(rpms.items()))
    print('The total number of the data point is {}'.format(n))

    head = ['RHE(ph)={}'.format(args.ph)]
    for title in rpms.keys():
        head.append(str(title)+'rpm')
    head.append(' ')
    head.append('Ag/Agcl, ph={}'.format(args.ph))
    for title in rpms.keys():
        head.append(str(title)+'rpm')

    out = []
    out.append(head)

    datas = list(rpms.values())
    titles = list(rpms.keys())

    for i in range(len(datas[0])):
        do = []
        v = float(datas[0][i][0].strip())
        pv = v + 0.059*args.ph + 0.1976
        do.append(pv)

        for count, d in enumerate(datas):
            vi = float(d[i][0].strip())
            # assert v == vi, 'The voltage {} of the file {} is different from others {}'.format(vi, titles[count], v)
            if v != vi:
                print('Warning: The voltage {} of the file {} is different from others {}'.format(vi, titles[count], v))
            rpm = float(d[i][1].strip())
            do.append(rpm*1000*16/math.pi)

        do.append(' ')

        do.append(v)
        out.append(do)
        for count, d in enumerate(datas):
            rpm = float(d[i][1].strip())
            do.append(rpm)

    print(out)
    print('writing data to file {}'.format(args.output))
    with open(args.output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(out)
            
if __name__ == '__main__':
    main()
