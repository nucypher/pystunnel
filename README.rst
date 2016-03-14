=========
pystunnel
=========
---------------------------------------------------------------------
Python library and command line utility to control a stunnel instance
---------------------------------------------------------------------

Overview
========

Start and stop a `stunnel`_ instance given a `stunnel configuration file`_.

The ``stunnel`` executable must be available on the system PATH.
The configuration file must specify a PID file.


.. _`stunnel`: https://www.stunnel.org
.. _`stunnel configuration file`: https://www.stunnel.org/static/stunnel.html#CONFIGURATION-FILE

Installation
============

Use your favorite installer to install the pystunnel library and script.
E.g.::

    $ pip install pystunnel

Examples
========

From the command line::

    $ pystunnel -c /path/to/stunnel.conf start
    started
    $ pystunnel -c /path/to/stunnel.conf check
    running
    $ pystunnel -c /path/to/stunnel.conf stop
    stopped

If the command is omitted, pystunnel enters an interactive shell::

    $ pystunnel -c /path/to/stunnel.conf
    pystunnel> start
    started
    pystunnel> check
    running
    pystunnel> stop
    stopped
    pystunnel> quit
    $

From Python::

    from pystunnel import Stunnel
    stunnel = Stunnel("/path/to/stunnel.conf")

    rc = stunnel.start()
    print("stunnel started with rc", rc)

    if stunnel.check() == 0:
        print("stunnel is running with pid", stunnel.getpid())
    else:
        print("stunnel is not running")

    rc = stunnel.stop()
    print("stunnel stopped with rc", rc)

Return Codes
------------

0 means OK, 1 or higher means error.

