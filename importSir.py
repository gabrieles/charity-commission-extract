#!/usr/bin/env python
from __future__ import print_function
import bcp_tsv
import zipfile
import sys
import csv

cc_files = {
    "sir_data": [
      "regno",
      "name",
      "sircode",
      "questionId",
	  "question",
	  "responseType",
	  "response",
    ]
}

def to_file(bcpdata, csvfilename="", col_headers=None):
    if csvfilename=="":
        csvfilename = 'converted.csv'

    # have to check system version annoyingly
    if sys.version_info >= (3,0):

        # python3 csv writer needs strings
        with open(csvfilename, 'w', encoding='utf-8') as csvfile:
            if(col_headers):
                for c in col_headers:
                    c = c
                writer = csv.writer(csvfile, lineterminator='\n')
                writer.writerow(col_headers)
            csvfile.write(bcpdata)

    else:

        # python2 csv writer needs bytes
        with open(csvfilename, 'wb') as csvfile:
            if(col_headers):
                for c in col_headers:
                    c = c.encode('utf-8')
                writer = csv.writer(csvfile)
                writer.writerow(col_headers)
            csvfile.write(bcpdata.encode('utf-8'))

    return csvfilename

def import_zip_stream(zip_file):
    zf = zipfile.ZipFile(zip_file, 'r')
    print('Opened zip file: %s' % zip_file)
    for filename in cc_files:
        try:
            bcp_filename = filename + '.bcp'
            csv_filename = filename + '.csv'
            col_headers=cc_files[filename]

            # have to check system version annoyingly
            # for python 3 >
            if sys.version_info >= (3,0):

                with zf.open(bcp_filename, 'r') as bcpfile:
                    with open(csv_filename, 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(col_headers)
                        for bcpfields in bcp_tsv.stream(bcpfile):
                            writer.writerow(bcpfields)

            # for python 2
            else:

                with zf.open(bcp_filename, 'r') as bcpfile:
                    with open(csv_filename, 'wb') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(col_headers)
                        for bcpfields in bcp_tsv.stream(bcpfile):
                            writer.writerow(bcpfields)

            print('Converted: %s' % bcp_filename)
        except KeyError:
            print('ERROR: Did not find %s in zip file' % bcp_filename)

def import_zip(zip_file):
    zf = zipfile.ZipFile(zip_file, 'r')
    print('Opened zip file: %s' % zip_file)
    for filename in cc_files:
        try:
            check_filename = filename + '.bcp'
            csv_filename = filename + '.csv'

            # check whether there is a file in the
            for i in zf.namelist():
                if i[-len(check_filename):]==check_filename:
                    bcp_filename = i

            bcpdata = zf.read(bcp_filename)
            bcpdata = bcpdata.decode('utf-8', errors="replace")
            bcpdata = bcp_tsv.convert(bcpdata)
            to_file(bcpdata, csvfilename=csv_filename, col_headers=cc_files[filename])
            print('Converted: %s' % bcp_filename)
        except KeyError:
            print('ERROR: Did not find %s in zip file' % bcp_filename)

def main():
    zip_file = sys.argv[1]
    import_zip(zip_file)

if __name__ == '__main__':
    main()
