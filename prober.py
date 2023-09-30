#!/usr/bin/python3

import sys
import time
import math
import easysnmp
from easysnmp import Session

dataofagt = sys.argv[1]
Fs = float(sys.argv[2])
N = int(sys.argv[3])
T = 1 / Fs
dispoid = []
agtdata = dataofagt.split(':')
add_the_dir = agtdata[0]
prt_the_dir = agtdata[1]
cmty_the_dir = agtdata[2]

for raj in range(4, len(sys.argv)):
    dispoid.append(sys.argv[raj])
dispoid.insert(0, '1.3.6.1.2.1.1.3.0')

def get_rate(counter, prev_counter, time_diff):
    rate = (counter - prev_counter) / time_diff
    return round(rate)

def raks():
    global scenarioA, xt, xl
    session = Session(hostname=add_the_dir, remote_port=prt_the_dir, community=cmty_the_dir, version=2, timeout=5, retries=4)
    PASSa = session.get(dispoid)
    Log = int(PASSa[0].value) / 100
    scenarioB = []
    x = ""
    for me in range(1, len(PASSa)):
        if PASSa[me].value not in ('NOSUCHOBJECT', 'NOSUCHINSTANCE'):
            if PASSa[me].snmp_type in ['COUNTER64', 'GAUGE', 'COUNTER32', 'COUNTER']:
                scenarioB.append(int(PASSa[me].value))
            else:
                scenarioB.append(PASSa[me].value)

            if num != 0 and len(scenarioA) > 0:
                if Log > xt:
                    if PASSa[me].snmp_type in ['COUNTER', 'COUNTER32', 'COUNTER64']:
                        suboid = int(scenarioB[me - 1]) - int(scenarioA[me - 1])
                        subtym = (Log - xt)
                        rate = get_rate(suboid, 0, subtym)

                        if rate < 0:
                            if Log > xt:
                                if PASSa[me].snmp_type == 'COUNTER32':
                                    suboid = suboid + (2 ** 32)
                                elif PASSa[me].snmp_type == 'COUNTER64':
                                    suboid = suboid + 2 ** 64

                                if x != str(xl):
                                    print(xl, "|", round(suboid / subtym), end="|")
                                    x = str(xl)
                                else:
                                    print(round(suboid / subtym), end="|")
                            else:
                                print(" It appears that the system has been reset ")
                                break
                        else:
                            if x != str(xl):
                                print(xl, "|", round(rate), end="|")
                                x = str(xl)
                            else:
                                print(round(rate), end="|")
                    elif PASSa[me].snmp_type == 'GAUGE':
                        suboid = int(scenarioB[me - 1]) - int(scenarioA[me - 1])
                        if suboid >= 0:
                            sign = "+"
                        else:
                            sign = ""
                        if x != str(xl):
                            print(xl, "|", scenarioB[len(scenarioB) - 1], "(", sign + str(suboid), ")", end="|")
                            x = str(xl)
                        else:
                            print(scenarioB[len(scenarioB) - 1], "(", sign + str(suboid), ")", end="|")
                    elif PASSa[me].snmp_type == 'OCTETSTR':
                        if x != str(xl):
                            print(xl, "|", scenarioB[len(scenarioB) - 1], end="|")
                        else:
                            print(scenarioB[len(scenarioB) - 1], end="|")
                        x = str(xl)
                else:
                    print(" It appears that the system has been reset ")
                    break
            else:
                print(" This seems like the system was restarted ")
                break
    scenarioA = scenarioB
    xt = Log

if N == -1:
    num = 0
    while True:
        xl = time.time()
        raks()
        if num:
            print()
        function_T = time.time()
        if T >= function_T - xl:
            raj = xl + T
            while time.time() < raj:
                pass
        else:
            quotient, remainder = divmod(function_T - xl, T)
            m = math.ceil(quotient) if remainder > 0 else quotient
            print(m, "n", (m * T) - function_T + xl)
            raj = xl + (m) * (T)
            while time.time() < raj:
                pass
        num += 1
else:
    for num in range(N + 1):
        xl = time.time()
        raks()
        if num:
            print()
        function_T = time.time()
        if T >= function_T - xl:
            raj = xl + T
            while time.time() < raj:
                pass
        else:
            quotient, remainder = divmod(function_T - xl, T)
            m = math.ceil(quotient) if remainder > 0 else quotient
            raj = xl + (m) * (T)
            while time.time() < raj:
                pass

