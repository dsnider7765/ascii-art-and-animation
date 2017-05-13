#chrome sleep timer


import time
import os; import sys; import subprocess as cmd


hours, minutes, seconds = input("How long?(HH MM SS): ").split()

timer = ((int(hours)*60*60)+(int(minutes)*60)+int(seconds))

for i in range(timer,-1,-1):
    hr = i//3600
    newTimer = i - (hr*3600)
    minute = newTimer//60
    second = newTimer - (minute*60)

    #cmd.call(['CLS'])
    print(str(hr)+":"+str(minute)+":"+str(second))
    time.sleep(1)
    
    

cmd.call(['taskkill','/F','/IM','chrome.exe'],shell=True)

