#!/usr/bin/env python

from argparse import ArgumentParser
import csv
import re
import sys

from vsc.atools.utils import InvalidLogEntryError


def parse_log_line(line):
    '''Retrieve array ID from log line'''
    match = re.match(r'(\d+)\s+', line)
    if match:
        return int(match.group(1))
    else:
        raise InvalidLogEntryError(line.rstrip())


def compute_ranges(todo):
    '''Compute the ranges of arrays IDs that are still to do'''
    todo_list = sorted(todo)
    ranges = []
    if todo_list:
        range_min = todo_list.pop(0)
        previous = range_min
        while todo_list:
            item = todo_list.pop(0)
            if previous + 1 != item:
                if range_min != previous:
                    ranges.append('{0:d}-{1:d}'.format(range_min, previous))
                else:
                    ranges.append('{0:d}'.format(range_min))
                range_min = item
            previous = item
        if range_min != previous:
            ranges.append('{0:d}-{1:d}'.format(range_min, previous))
        else:
            ranges.append('{0:d}'.format(range_min))
    return ','.join(ranges)

    
if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Compute the array ID range')
    arg_parser.add_argument('--data', required=True, nargs='+',
                            help='CSV files to use')
    arg_parser.add_argument('--log', nargs='*',
                            help='log file to compute completed items from')
    arg_parser.add_argument('--redo', action='store_true',
                            help='redo failed items')
    arg_parser.add_argument('--sniff', type=int, default=1024,
                            help='number of bytes to sniff for CSV dialect')
    options = arg_parser.parse_args()
    nr_work_items = sys.maxsize
    try:
        for filename in options.data:
            with open(filename, 'r') as csv_file:
                dialect = csv.Sniffer().sniff(csv_file.read(options.sniff))
                csv_file.seek(0)
                csv_reader = csv.DictReader(csv_file, fieldnames=None,
                                            restkey='rest', restval=None,
                                            dialect=dialect)
                row_nr = 0
                for row in csv_reader:
                    row_nr += 1
                if row_nr < nr_work_items:
                    nr_work_items = row_nr
    except IOError as error:
        msg = '### IOError: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    if options.log:
        todo = set((i for i in xrange(1, nr_work_items + 1)))
        completed = set()
        failed = set()
        try:
            for filename in options.log:
                with open(filename, 'r') as log_file:
                    for line in log_file:
                        if 'completed' in line:
                            todo.discard(parse_log_line(line))
                            completed.add(parse_log_line(line))
                        elif 'failed' in line:
                            failed.add(parse_log_line(line))
            if not options.redo:
                failed -= completed
                todo -= failed
            print(compute_ranges(todo))
        except IOError as error:
            msg = '### IOError: {0}'.format(str(error))
            sys.stderr.write(msg)
            sys.exit(error.errno)
        except InvalidLogEntryError as error:
            msg = '### IOError: {0}'.format(str(error))
            sys.stderr.write(msg)
            sys.exit(error.errno)
    else:
        print('1-{0:d}'.format(nr_work_items))
