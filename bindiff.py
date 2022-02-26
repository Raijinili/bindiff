#!/usr/bin/env python

'''
@author: Adel Daouzli

Adapted for Python3 by Mario Orlandi (2021)
Add from nixx to compare 3 files
'''

import os
import sys
import time

class CompareFiles():
    '''Comparing two binary files'''

    def __init__(self, file1, file2):
        '''Get the files to compare and initialise message, offset and diff list.
        :param file1: a file
        :type file1: string
        :param file2: an other file to compare
        :type file2: string
        '''
        self._buffer_size = 512

        self.message = None
        '''message of diff result: "not found", "size", "content", "identical"'''
        self.offset = None
        '''offset where files start to differ'''
        self.diff_list = []
        self.diff_list2 = {}
        '''list of diffs made of tuples: (offset, hex(byte1), hex(byte2))'''

        self.file1 = file1
        self.file2 = file2

    def compare(self):
        '''Compare the two files

        :returns: Comparison result: True if similar, False if different.
        Set vars offset and message if there's a difference.

        '''
        self.message = None
        self.offset_differs = None
        offset = 0
        offset_diff = 0
        first = False
        if not os.path.isfile(self.file1) or not os.path.isfile(self.file2):
            self.message = "not found"
            return False
        if os.path.getsize(self.file1) != os.path.getsize(self.file2):
            self.message = "size"
            return False
        same = True
        with open(self.file1,'rb') as f1, open(self.file2,'rb') as f2:
            while True:
                buffer1 = f1.read(self._buffer_size)
                buffer2 = f2.read(self._buffer_size)
                if len(buffer1) == 0 or len(buffer2) == 0:
                    break
                # for e in range(len(zip(buffer1, buffer2))):
                #     if buffer1[e] != buffer2[e]:
                #         if first == False:
                #             first = True
                #         same = False
                #         self.diff_list.append((hex(offset),
                #                                hex(ord(buffer1[e])),
                #                                hex(ord(buffer2[e]))))
                # Adapted to Python3
                for byte1, byte2 in zip(buffer1, buffer2):
                    if byte1 != byte2:
                        if not first:
                            first = True
                        same = False
                        self.diff_list.append((offset, byte1, byte2))
                        self.diff_list2[offset] = byte2

                    offset += 1
                    if not first:
                        offset_diff += 1

        if not same:
            self.message = 'content'
            self.offset = hex(offset_diff)
        else:
            self.message = 'identical'

        return same

def help_msg(cmd):
    print ("Compare Binary Files - Adel Daouzli")
    print ("Usage: " + cmd + " [-l] file1 file2")
    print ("option -l will list all differences with offsets.")


def ascii_display(e):
    if e < 32:
        text = "%3d" % e
    else:
        text = "'%s'" % chr(e)
    return text


def compare_files(f1, f2, ls):
    c = CompareFiles(f1, f2)
    result = c.compare()
    print("Result of comparison:", c.message)
    print("File 1 length: ", os.stat(f1).st_size)
    print("File 2 length: ", os.stat(f2).st_size)
    print("Num. differences: ", len(c.diff_list))
    if not result and c.message == 'content':
        print(c.diff_list)
        print("offset differs:", c.offset)
        if ls:
            print ("List of differences:")
            for o, e1, e2 in c.diff_list:
                print ("offset 0x%08x: 0x%02x != 0x%02x (%s != %s)" % (
                    o, e1, e2, repr(e1), repr(e2),
                ))

def compare_files_v2(f1, f2, f3, ls):
    pf2size = os.stat(f2).st_size
    pf3size = os.stat(f3).st_size
    
    if pf2size != pf3size:
        return False
    
    a = CompareFiles(f1, f2)
    resulta = a.compare()
    b = CompareFiles(f1, f3)
    resultb = b.compare()
    

    # Using dict.keys() as a set and doing an intersection.
    for key in a.diff_list2.keys() & b.diff_list2.keys():
        if a.diff_list2[key] != b.diff_list2[key]:
            if ls:
                print(key)
            # Shouldn't it only return if not ls?
            return False

    return True


if __name__ == '__main__':
    if not (2 < len(sys.argv) < 6):
        help_msg(os.path.basename(sys.argv[0]))
        sys.exit()
    if len(sys.argv) >= 5:
        if sys.argv[1].strip() != '-l':
            help_msg(os.path.basename(sys.argv[0]))
            sys.exit()
        ls = True
        f1, f2, f3 = sys.argv[2:5]
    else:
        # How are you using 1,2,3 if you only guaranteed >2?
        ls = False
        f1, f2, f3 = sys.argv[1:4]

    t0 = time.time()
    x = compare_files_v2(f1, f2, f3, ls)
    if x:
        print("OK")
    else:
        print("NOK")
    t1 = time.time()
    if ls:
        print('Elapsed time: ', time.strftime("%H:%M:%S", time.gmtime(t1 - t0)))


