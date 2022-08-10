import sys
from pyparsing import Word, alphas, Suppress, Combine, nums, string, Optional, Regex
from time import strftime
from datetime import datetime
import argparse
import logparsing.configs
from logparsing.parser import Parser

if __name__ == "__main__":
    
    p = Parser()
    f = open('./logfiles/syslog', encoding='utf8')
    l = f.readlines()
    
    out = []
    outfiltered = []
    
    for line in l:
        
        if 'kernel:' in line:
            continue
        
        try:
            out.append(p.parse(line))
        except:
            continue
    
    for line in out:
        if ('Started' in line['message'] or 'Consumed' in line['message']):
            if "snap.firefox.firefox" in line['message']:
                outfiltered.append(line)
    
    for line in outfiltered:
        line['timestamp'] = datetime.strptime(line['timestamp'], "%Y-%m-%d %H:%M:%S")
    
    outfiltered.sort(key=lambda x: x['timestamp'])
    
    activities = []
    
    i = 0
    while i < len(outfiltered):
        
        if 'Started' in outfiltered[i]['message']:
            newactivity = {}
            newactivity['start'] = outfiltered[i]['timestamp']
            i += 1
            while i < len(outfiltered):
                if 'Consumed' in outfiltered[i]['message']:
                    newactivity['end'] = outfiltered[i]['timestamp']
                    activities.append(newactivity)
                    break
                i += 1
                
        i += 1
        
    for activity in activities:
        start_time = activity['start'].strftime("%Y-%m-%d %H:%M:%S")
        end_time = activity['end'].strftime("%Y-%m-%d %H:%M:%S")
        duration = activity['end'] - activity['start']
        print("Browsed Firefox from " + start_time + " to " + end_time + ". Duration: ", duration)