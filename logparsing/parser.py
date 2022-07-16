import sys
from pyparsing import Word, alphas, Suppress, Combine, nums, string, Optional, Regex
from time import strftime
from datetime import datetime
import argparse

class Parser(object):
    def __init__(self):
        ints = Word(nums)

        # priority
        priority = Optional(Suppress("<") + Suppress(ints) + Suppress(">"))

        # timestamp
        month = Word(string.ascii_uppercase , string.ascii_lowercase, exact=3)
        day   = ints
        hour  = Combine(ints + ":" + ints + ":" + ints)
        timestamp = month + day + hour

        # hostname
        hostname = Word(alphas + nums + "_" + "-" + ".")

        # appname
        appname = Word(alphas + "/" + "-" + "_" + "." + nums + '@') + Optional(Suppress("[") + Suppress(ints) + Suppress("]")) + Suppress(":")

        # message
        message = Regex(".*")
  
        # pattern build
        self.__pattern = timestamp + hostname + appname + message
    
    def parse(self, line):
        parsed = self.__pattern.parseString(line)
        payload = {}
        months = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12,
        }
        dt = datetime(datetime.now().year, months[parsed[0]], int(parsed[1]), hour=int(parsed[2].split(':')[0]), minute=int(parsed[2].split(':')[1]), second=int(parsed[2].split(':')[2]))
        payload["timestamp"] = dt.strftime("%Y-%m-%d %H:%M:%S")
        payload["hostname"]  = parsed[3]
        payload["appname"]   = parsed[4]
        payload["message"]   = parsed[5]
    
        return payload