#!/usr/bin/python

import os
import sys
import getopt
import csv
import locale
import re


def usage(pname):
    print("Usage:")
    print("\t<FILE> \t\t\t Input file")
    sys.exit("")


def ReadPportCsv(fname):
    datap = {}
    print "Read %s" % fname
    with open(fname, 'rb') as f:
        reader = csv.reader(f)
        entries = list(reader)
        for entry in entries:
            for item in reversed(entry):
                print item
    return datap


def ReadPport(fname, fstart='Total'):
    datap = []
    print "Read %s" % fname
    hand = open(fname)
    n = 0
    for line in hand:
        n += 1
        if n == 1:
            if line[0:len(fstart)] != fstart:
                print "Not a %s document" % fstart
                return datap
        line = line.rstrip()
        #if re.search('From:', line) :
            #print line
        datap.append(line)
    return datap


def ReadBank(fname, fstart='Date', lstart='ACB KREDIET'):
    datab = {}
    print "Read %s" % fname
    with open(fname, 'rb') as f:
        reader = csv.reader(f)
        entries = list(reader)
        if entries[0][0][0:len(fstart)] != fstart:
            print "Not a bank statement:",
            print entries[0][0]
            return datab
        for entry in entries:
            if entry[1][0:len(lstart)] != lstart:
                continue
            #for item in entry:
                #print item
            words = entry[1].split(' ')
            for word in reversed(words):
                try:
                    bnum = int(word)
                    #print "%d" % bnum
                    datab[bnum] = entry
                    break
                except ValueError:
                    pass
            #try:
                #amountr = float(entry[2].replace("R", "").replace(",", ""))
                #amountc = int(entry[2].replace("R", "").replace(",", "").replace(".", ""))
                #print "%d" % amountc
                #if amountc > 0:
                    #datab[amountc] = entry
            #except ValueError:
                #print "? %s" % entry[2].replace("R", "").replace(",", "")
                #pass
            #print
    return datab


# Pythonic entry point
def main(pname, argv):
    fname = None
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

    try:
        opts, fnames = getopt.gnu_getopt(argv,"h", \
                                   ["help"])
    except getopt.GetoptError:
        print("Error in options")
        # usage()
        return 1

    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            usage(pname)
        else:
            print("Something is wrong here")

    if len(fnames) == 0:
        print("No input file names")
        return 1
    elif len(fnames) != 2:
        print("No input file names")
        return 1

    datab = ReadBank(fnames[0])
    if len(datab) == 0:
        return 1

    datap = ReadPport(fnames[1])
    if len(datap) == 0:
        return 1

    #print "***************"
    for bnum in sorted(datab.iterkeys()):
        amountr = str(datab[bnum][2].replace("R", "").strip(" "))
        print "%6d : (%s) %s [%s]" % (bnum, datab[bnum][0], datab[bnum][1], amountr)
        rstr = ",%d," % bnum
        n = 0
        for line in datap:
            n += 1
            if re.search(rstr, line) :
                lfind = line.find(amountr)
                if lfind >= 0:
                    print "\t*%d*\t%s" % (n, line)
                else:
                    print "\t\t%s" % (line)
        print

    return 0


# Entry point
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        usage(sys.argv[0])
    main(sys.argv[0], sys.argv[1:])

