"""Start, stop, and check a stunnel process"""

from __future__ import print_function

import os
import sys
import re
import subprocess
import getopt


class StunnelConfig:
    """Represent a stunnel configuration"""

    _section_re = re.compile(r"\[(.*)\]")
    _foreground_re = re.compile(r"foreground\s*=\s*(.*)")
    _pid_file_re = re.compile(r"pid\s*=\s*(.*)")

    def __init__(self, config_file):
        self.config_file = config_file
        self.pid_file = None
        self.foreground = False
        self._read_config()

    def _read_config(self):
        if self.config_file and os.path.isfile(self.config_file):
            lines = []
            with open(self.config_file, "rt") as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                match = self._section_re.match(line)
                if match:
                    return
                match = self._pid_file_re.match(line)
                if match:
                    self.pid_file = match.group(1)
                else:
                    match = self._foreground_re.match(line)
                    if match:
                        if match.group(1) == "yes":
                            self.foreground = True


class Stunnel(StunnelConfig):
    """Start and stop a stunnel instance given a configuration file

    The config file must contain a pid = /path/to/pid-file line.

    Example:
        from pystunnel import Stunnel
        stunnel = Stunnel("/path/to/config-file")

        rc = stunnel.start()
        print("stunnel started with rc", rc)

        if stunnel.check() == 0:
            print("stunnel is running with pid", stunnel.getpid())
        else:
            print("stunnel is not running")

        rc = stunnel.stop()
        print("stunnel stopped with rc", rc)

    Return Codes:
        0 means OK, 1 or higher means error.

        The start command can fail for a variety of reasons, the most common
        being bad or missing configuration files. Inspecting the config_file,
        pid_file, and foreground attributes may provide hints on the nature
        of the error.
    """

    def __init__(self, config_file):
        StunnelConfig.__init__(self, config_file)

    def start(self):
        if self.pid_file and not self.foreground and self.check() == 1:
            return subprocess.call('stunnel "%s"' % self.config_file, shell=True);
        return 1

    def stop(self):
        if self.check() == 0:
            return subprocess.call("kill %d" % self.getpid(), shell=True)
        return 1

    def check(self):
        pid = self.getpid()
        return 0 if pid >= 0 else 1

    def getpid(self):
        pid = -1
        if self.pid_file and os.path.isfile(self.pid_file):
            with open(self.pid_file, "rb") as f:
                bpid = f.read(16)
                if bpid:
                    try:
                        pid = int(bpid, 10)
                    except ValueError:
                        pass
        return pid


class PyStunnel(Stunnel):
    """Usage: pystunnel options [command]

Start and stop a stunnel instance from the command line

Options:
  -c config-file, --stunnel-config=config-file
                      Use config-file to drive the stunnel instance.
                      The stunnel configuration must specify a PID file.

  -h, --help          Print this help message and exit.
  -v, --version       Print the version string and exit.

Commands:
  start               Start the stunnel instance.
  stop                Stop the stunnel instance.
  check               Check if stunnel is running.
  getpid              Return PID of running stunnel instance.

  If the command is omitted, pystunnel enters an interactive shell.
"""

    def __init__(self, args=None):
        Stunnel.__init__(self, None)
        self.args = args

    def parse_args(self, args):
        try:
            options, args = getopt.gnu_getopt(args, "c:hv", ("stunnel-config=", "help", "version"))
        except getopt.GetoptError, e:
            print(e.msg)
            sys.exit(1)

        for name, value in options:
            if name in ("-c", "--stunnel-config"):
                Stunnel.__init__(self, value)
            elif name in ("-h", "--help"):
                print(self.__doc__)
                sys.exit(0)
            elif name in ("-v", "--version"):
                import pkg_resources
                print("pystunnel", pkg_resources.get_distribution("pystunnel").version)
                sys.exit(0)

        if not self.config_file:
            print("option -c is required")
            sys.exit(1)
        elif not os.path.isfile(self.config_file):
            print("no such file:", self.config_file)
            sys.exit(1)
        elif not self.pid_file:
            print("must set pid = /path/to/pid-file in", self.config_file)
            sys.exit(1)
        elif self.foreground:
            print("must set foreground = no in", self.config_file)
            sys.exit(1)

        return args

    def perform(self, command):
        rc = 0
        if command == "start":
            rc = self.start()
            if rc == 0:
                print("started")
            elif self.check() == 0:
                print("already started (%s)" % self.getpid())
            else:
                print("not started!")
        elif command == "stop":
            rc = self.stop()
            if rc == 0:
                print("stopped")
            elif self.check() == 1:
                print("already stopped")
            else:
                print("not stopped!")
        elif command == "check":
            rc = self.check()
            if rc == 0:
                print("running (%s)" % self.getpid())
            else:
                print("not running")
        elif command == "getpid":
            pid = self.getpid()
            print(pid)
            rc = 0 if pid >= 0 else 1
        return rc

    def single(self, command):
        rc = 0
        if command in ("start", "stop", "check", "getpid"):
            rc = self.perform(command)
        else:
            print("valid commands: start, stop, check, getpid")
            rc = 1
        return rc

    def loop(self):
        rc = 0
        while True:
            try:
                command = raw_input("pystunnel> ")
                command = command.strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break;
            if command in ("start", "stop", "check", "getpid"):
                rc = self.perform(command)
            elif command in ("q", "quit"):
                break;
            elif command == "":
                pass
            else:
                print("valid commands: start, stop, check, getpid, quit")
                rc = 1
        return rc

    def run(self):
        args = self.parse_args(self.args)
        if args:
            return self.single(args[0])
        else:
            return self.loop()


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    try:
        return PyStunnel(args).run()
    except SystemExit as e:
        return e.code


if __name__ == "__main__":
    sys.exit(main())
