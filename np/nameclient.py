#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2011, 2012 SMHI

# Author(s):

#   Martin Raspaud <martin.raspaud@smhi.se>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Asking for the address of a module.
"""

import zmq
from posttroll.message import Message
class TimeoutException(BaseException):
    pass

import warnings

def get_address(data_type, timeout=2):

    warnings.warn("nameclient.get_address shouldn't be used, " +
                  "use posttroll.subscriber.get_address instead...",
                  DeprecationWarning)

    context = zmq.Context()

    # Socket to talk to server
    socket = context.socket(zmq.REQ)
    try:
        socket.connect("tcp://localhost:5555")

        msg = Message("/oper/ns", "request", {"type": data_type})
        socket.send(str(msg))


        # Get the reply.
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)
        s = poller.poll(timeout=timeout * 1000)
        if s:
            if s[0][0] == socket:
                m = Message.decode(socket.recv(zmq.NOBLOCK))
                return m.data
            else:
                raise RuntimeError("Unknown socket ?!?!?")
        else:
            raise TimeoutException("Didn't get an address after %d seconds."
                                   %timeout)
        print "Received reply to ", data_type, ": [", m, "]"
    finally:
        socket.close()
