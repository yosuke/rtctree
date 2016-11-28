#!/bin/sh

sudo apt install subversion autoconf autotool-bin libpoco-dev
if [ ! -d "FSM4RTC" ]; then
    svn co http://svn.openrtm.org/OpenRTM-aist/branches/FSM4RTC
fi
cd FSM4RTC
svn update
patch -p0 -E < ../test/setup-fsm4rtc.patch
cd OpenRTM-aist
./autogen.sh 
./configure
make -j4

## To launch the test component:
# cd src/ext/sdo/fsm4rtc_observer/test/
# ./test.sh 
