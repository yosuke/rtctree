# -*- Python -*-
# -*- coding: utf-8 -*-

'''rtctree

Copyright (C) 2009-2015
    Geoffrey Biggs
    RT-Synthesis Research Group
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the GNU Lesser General Public License version 3.
http://www.gnu.org/licenses/lgpl-3.0.en.html

SDO client objects.

'''


from rtctree.rtc import OpenRTM__POA
from rtctree.rtc import RTC__POA


class RTCObserver(RTC__POA.ComponentObserver):
    def __init__(self, target):
        self._tgt = target

    def update_status(self, kind, hint):
        kind = str(kind)
        if kind == 'COMPONENT_PROFILE':
            self._tgt._profile_update([x.strip() for x in hint.split(',')])
        elif kind == 'RTC_STATUS':
            status, ec_handle = hint.split(':')
            if status == 'INACTIVE':
                status = self._tgt.INACTIVE
            elif status == 'ACTIVE':
                status = self._tgt.ACTIVE
            elif status == 'ERROR':
                status = self._tgt.ERROR
            self._tgt._set_state_in_ec(int(ec_handle), status)
        elif kind == 'EC_STATUS':
            event, ec_handle = hint.split(':')
            if event == 'ATTACHED':
                event = self._tgt.EC_ATTACHED
            elif event == 'DETACHED':
                event = self._tgt.EC_DETACHED
            elif event == 'RATE_CHANGED':
                event = self._tgt.EC_RATE_CHANGED
            elif event == 'STARTUP':
                event = self._tgt.EC_STARTUP
            elif event == 'SHUTDOWN':
                event = self._tgt.EC_SHUTDOWN
            self._tgt._ec_event(int(ec_handle), event)
        elif kind == 'PORT_PROFILE':
            event, port_name = hint.split(':')
            if event == 'ADD':
                event = self._tgt.PORT_ADD
            elif event == 'REMOVE':
                event = self._tgt.PORT_REMOVE
            elif event == 'CONNECT':
                event = self._tgt.PORT_CONNECT
            elif event == 'DISCONNECT':
                event = self._tgt.PORT_DISCONNECT
            self._tgt._port_event(port_name, event)
        elif kind == 'CONFIGURATION':
            event, arg = hint.split(':')
            if event == 'UPDATE_CONFIGSET':
                event = self._tgt.CFG_UPDATE_SET
            elif event == 'UPDATE_PARAMETER':
                event = self._tgt.CFG_UPDATE_PARAM
            elif event == 'SET_CONFIG_SET':
                event = self._tgt.CFG_SET_SET
            elif event == 'ADD_CONFIG_SET':
                event = self._tgt.CFG_ADD_SET
            elif event == 'REMOVE_CONFIG_SET':
                event = self._tgt.CFG_REMOVE_SET
            elif event == 'ACTIVATE_CONFIG_SET':
                event = self._tgt.CFG_ACTIVATE_SET
            self._tgt._config_event(arg, event)
        elif kind == 'HEARTBEAT' or kind == 'RTC_HEARTBEAT' or kind == 'EC_HEARTBEAT':
            self._tgt._heartbeat(kind)
        elif kind == 'FSM_PROFILE' or kind == 'FSM_STATUS' or kind == 'FSM_STRUCTURE':
            self._tgt._fsm_event(kind, hint)


class RTCLogger(OpenRTM__POA.Logger):
    def __init__(self, target, callback):
        self._tgt = target
        self._cb = callback

    def publish(self, record):
        ts = record.time.sec + record.time.nsec / 1e9
        self._cb(self._tgt.name, ts, loggername, level, message)


# vim: set expandtab tabstop=8 shiftwidth=4 softtabstop=4 textwidth=79
