import sys
from pyparsing import Word, alphas, Suppress, Combine, nums, string, Optional, Regex
from time import strftime
from datetime import datetime
import argparse
import configs
from parser import Parser

ap = argparse.ArgumentParser(description="parse input syslog file to generate input and outputdata")
ap.add_argument('--app', default='firefox')
args = ap.parse_args()

def gen_data(parsed):
    
    sigs = configs.signatures[args.app]
    temp_out = []
    
    for line in parsed:
        temp_out.append("No activity")
        if ('Started' in line['message'] or 'Consumed' in line['message']):
            for sig in sigs:
                if sig in line['message']:
                    temp_out[-1] = "Used " + sig           

if __name__ == "__main__":
    
    p = Parser()
    f = open('../logfiles/syslog', encoding='utf8')
    l = f.readlines()
    
    out = []
    
    for line in l:
        
        if 'kernel:' in line:
            continue
        
        try:
            out.append(p.parse(line))
        except:
            continue