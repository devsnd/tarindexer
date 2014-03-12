#!/usr/bin/python3
#
# tarindexer
# index tar files for fast access
#
# Copyright (c) 2013 Tom Wallroth
#
# Sources on github:
#   http://github.com/devsnd/tarindexer/
#
# licensed under GNU GPL version 3 (or later)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#


import tarfile
import sys
import os
import time
import codecs

usage = """create index file:
    tarindexer -i tarfile.tar indexfile.index
lookup file using indexfile:
    tarindexer -l tarfile.tar indexfile.index lookuppath
"""

starttime = time.time()

def human(size):
    a = 'B','kB','mB','gB','tB','pB'
    curr = 'B'
    while( size > 1024 ):
        size/=1024
        curr = a[a.index(curr)+1]
    return str(int(size*10)/10)+curr
    
def indextar(dbtarfile,indexfile):
    filesize = os.path.getsize(dbtarfile)
    lastpercent = 0
    

    with tarfile.open(dbtarfile, 'r|') as db:
        if os.path.isfile(indexfile):
            print('file exists. exiting')

        with open(indexfile, 'w') as outfile:
            counter = 0
            print('One dot stands for 1000 indexed files.')
            #tarinfo = db.next()
            for tarinfo in db:
                currentseek = tarinfo.offset_data
                rec = "%s %d %d\n" % (tarinfo.name, tarinfo.offset_data, tarinfo.size)
                outfile.write(rec)
                counter += 1
                if counter % 1000 == 0:
                    # free ram...
                    db.members = []
                if(currentseek/filesize>lastpercent):
                    print('')
                    percent = int(currentseek/filesize*1000.0)/10
                    print(str(percent)+'%')
                    lastpercent+=0.01
                    print(human(currentseek)+'/'+human(filesize))
                    if(percent!=0):
                        estimate = ((time.time()-starttime)/percent)*100
                        eta = (starttime+estimate)-time.time()
                        print('ETA: '+str(int(eta))+'s (estimate '+str(int(estimate))+'s)')
    print('done.')

def lookup(dbtarfile,indexfile,path):
    with open(dbtarfile, 'rb') as tar:
        with  open(indexfile, 'r') as outfile:
            for line in outfile.readlines():
                m = line[:-1].rsplit(" ", 2)
                if path == m[0]:
                    tar.seek(int(m[1]))
                    a = codecs.decode(tar.read(int(m[2])),'ASCII')
                    print(a)


def main():
    MODE = ''
    dbtarfile = ''
    indexfile = ''
    path = ''

    if len(sys.argv)<2:
        print(usage)
        exit(0)

    if sys.argv[1] == '-i':
        MODE = 'index'
        dbtarfile = sys.argv[2]
        indexfile = sys.argv[3]
    elif sys.argv[1] == '-l':
        MODE = 'lookup'
        dbtarfile = sys.argv[2]
        indexfile = sys.argv[3]
        path = sys.argv[4]
    else:
        print(usage)
        exit(0)
    
    if MODE == 'index':
        indextar(dbtarfile,indexfile)
    elif MODE == 'lookup':
        lookup(dbtarfile,indexfile,path)

if __name__ == "__main__":
    main()    

    
