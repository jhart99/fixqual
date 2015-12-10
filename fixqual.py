#!/usr/bin/env python

import gzip
import os
import sys
import argparse
import time
import cProfile

class fastq(object):
    def __init__(self, inFastq):
        self.fastq = inFastq
        filename, extension = os.path.splitext(inFastq)
        if inFastq == "stdio":
            self.fileHandle = sys.stdin
        elif inFastq == "stdout":
            self.fileHandle = sys.stdout
        else:
            self.fileHandle = None
            self.gzip = extension == '.gz' or extension == '.gzip'
    def read(self):
        if self.fileHandle == None:
            try:
                if self.gzip:
                    self.fileHandle = gzip.open(self.fastq, 'r')
                else:
                    self.fileHandle = open(self.fastq, 'r')
            except IOError:
                print "Could not read the input file:", self.fastq
                sys.exit()

        with self.fileHandle:
            while True:
                lines = []
                for i in range(4):
                    try:
                        lines.append(self.fileHandle.next())
                    except StopIteration:
                        return
                yield lines

    def write(self, lines):
        if self.fileHandle == None:
            try:
                if self.gzip:
                    self.fileHandle = gzip.open(self.fastq, 'w')
                else:
                    self.fileHandle = open(self.fastq, 'w')
            except IOError:
                print "Could not open the output file:", self.fastq
                sys.exit()

        for line in lines:
            self.fileHandle.write(line);
    def __del__(self):
        print "closing ", self.fastq
        self.fileHandle.close()

def fixquals33(read):
    fixedquals = [x if x < '~' else '~' for x in read[3][:-2]]
    fixedquals = [x if x > '!' else '!' for x in fixedquals]
    read[3] = "".join(fixedquals) + '\r\n'
    return read
def fixquals64(read):
    fixedquals = [x if x < '@' else '@' for x in read[3][:-2]]
    fixedquals = [x if x > '!' else '!' for x in fixedquals]
    read[3] = "".join(fixedquals) + '\r\n'
    return read

def main():
    parser = argparse.ArgumentParser(description="fix out of range quality scores in fastq")
    parser.add_argument('fastq', nargs='?', default='stdin')
    parser.add_argument('outFastq', nargs='?', default='stdout')
    parser.add_argument('--phred64', dest='fixquals', action='store_const',
            const=fixquals64, default=fixquals33,
            help='input values are on phred64 scale')
    args = parser.parse_args()
    inFastq = fastq(args.fastq)
    outFastq = fastq(args.outFastq)

    beginTime = time.clock()
    readsProcessed =0
    for reads in inFastq.read():
        fixedreads = args.fixquals(reads)
        outFastq.write(fixedreads)
        readsProcessed += 1
        if readsProcessed % 100000 == 0:
            print str(readsProcessed) ," reads processed ", time.clock()-beginTime


if __name__ == '__main__':
    cProfile.run('main()')
    #main()
