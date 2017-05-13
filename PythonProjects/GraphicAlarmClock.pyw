# GraphicAlarmClock
# David Snider
# 4/19/17

"""This is for making an alarm clock that should actually work"""
import tkinter as tk
# from VolumeOnlyAlarm.py-----------------------------
import time
from comtypes import *
import comtypes.client
from ctypes import POINTER
from ctypes.wintypes import DWORD, BOOL
import glob
import os
import random
import winsound
import threading as thread

MMDeviceApiLib = \
    GUID('{2FDAAFA3-7523-4F66-9957-9D5E7FE698F6}')
IID_IMMDevice = \
    GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
IID_IMMDeviceEnumerator = \
    GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')
CLSID_MMDeviceEnumerator = \
    GUID('{BCDE0395-E52F-467C-8E3D-C4579291692E}')
IID_IMMDeviceCollection = \
    GUID('{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
IID_IAudioEndpointVolume = \
    GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')


class IMMDeviceCollection(IUnknown):
    _iid_ = GUID('{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
    pass


class IAudioEndpointVolume(IUnknown):
    _iid_ = GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')
    _methods_ = [
        STDMETHOD(HRESULT, 'RegisterControlChangeNotify', []),
        STDMETHOD(HRESULT, 'UnregisterControlChangeNotify', []),
        STDMETHOD(HRESULT, 'GetChannelCount', []),
        COMMETHOD([], HRESULT, 'SetMasterVolumeLevel',
            (['in'], c_float, 'fLevelDB'),
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'SetMasterVolumeLevelScalar',
            (['in'], c_float, 'fLevelDB'),
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'GetMasterVolumeLevel',
            (['out','retval'], POINTER(c_float), 'pfLevelDB')
        ),
        COMMETHOD([], HRESULT, 'GetMasterVolumeLevelScalar',
            (['out','retval'], POINTER(c_float), 'pfLevelDB')
        ),
        COMMETHOD([], HRESULT, 'SetChannelVolumeLevel',
            (['in'], DWORD, 'nChannel'),
            (['in'], c_float, 'fLevelDB'),
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'SetChannelVolumeLevelScalar',
            (['in'], DWORD, 'nChannel'),
            (['in'], c_float, 'fLevelDB'),
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'GetChannelVolumeLevel',
            (['in'], DWORD, 'nChannel'),
            (['out','retval'], POINTER(c_float), 'pfLevelDB')
        ),
        COMMETHOD([], HRESULT, 'GetChannelVolumeLevelScalar',
            (['in'], DWORD, 'nChannel'),
            (['out','retval'], POINTER(c_float), 'pfLevelDB')
        ),
        COMMETHOD([], HRESULT, 'SetMute',
            (['in'], BOOL, 'bMute'),
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'GetMute',
            (['out','retval'], POINTER(BOOL), 'pbMute')
        ),
        COMMETHOD([], HRESULT, 'GetVolumeStepInfo',
            (['out','retval'], POINTER(c_float), 'pnStep'),
            (['out','retval'], POINTER(c_float), 'pnStepCount'),
        ),
        COMMETHOD([], HRESULT, 'VolumeStepUp',
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'VolumeStepDown',
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'QueryHardwareSupport',
            (['out','retval'], POINTER(DWORD), 'pdwHardwareSupportMask')
        ),
        COMMETHOD([], HRESULT, 'GetVolumeRange',
            (['out','retval'], POINTER(c_float), 'pfMin'),
            (['out','retval'], POINTER(c_float), 'pfMax'),
            (['out','retval'], POINTER(c_float), 'pfIncr')
        ),

    ]


class IMMDevice(IUnknown):
    _iid_ = GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
    _methods_ = [
        COMMETHOD([], HRESULT, 'Activate',
            (['in'], POINTER(GUID), 'iid'),
            (['in'], DWORD, 'dwClsCtx'),
            (['in'], POINTER(DWORD), 'pActivationParans'),
            (['out','retval'], POINTER(POINTER(IAudioEndpointVolume)), 'ppInterface')
        ),
        STDMETHOD(HRESULT, 'OpenPropertyStore', []),
        STDMETHOD(HRESULT, 'GetId', []),
        STDMETHOD(HRESULT, 'GetState', [])
    ]
    pass


class IMMDeviceEnumerator(comtypes.IUnknown):
    _iid_ = GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')

    _methods_ = [
        COMMETHOD([], HRESULT, 'EnumAudioEndpoints',
            (['in'], DWORD, 'dataFlow'),
            (['in'], DWORD, 'dwStateMask'),
            (['out','retval'], POINTER(POINTER(IMMDeviceCollection)), 'ppDevices')
        ),
        COMMETHOD([], HRESULT, 'GetDefaultAudioEndpoint',
            (['in'], DWORD, 'dataFlow'),
            (['in'], DWORD, 'role'),
            (['out','retval'], POINTER(POINTER(IMMDevice)), 'ppDevices')
        )
    ]

enumerator = comtypes.CoCreateInstance(
    CLSID_MMDeviceEnumerator,
    IMMDeviceEnumerator,
    comtypes.CLSCTX_INPROC_SERVER
)

# print enumerator
endpoint = enumerator.GetDefaultAudioEndpoint(0, 1)
# print endpoint
volume = endpoint.Activate(IID_IAudioEndpointVolume, comtypes.CLSCTX_INPROC_SERVER, None)
# print volume
# print volume.GetMasterVolumeLevel()
# print volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-65, None) uncomment for 0 volume
# volume.SetMasterVolumeLevel(-1, None) # uncomment for full volume
# volume.SetMasterVolumeLevel(-25, None) # Change the first argument for controlling the volume remember it should be
# -ve not less than -65

'''answer = ''
while answer != 'y':
    alarmTime = input("Give time for alarm(HH:MM)(24hr time) ")
    answer = input("Is "+alarmTime+" the correct time?(y/n) ")

alarmTime = alarmTime.split(":")
hour = int(alarmTime[0])
minute = int(alarmTime[1])
isAlarm = False
while not isAlarm:
    now = time.localtime()
    if now.tm_hour == hour and now.tm_min == minute:
        isAlarm = True
    else:
        time.sleep(5)
# volume.SetMasterVolumeLevel(-1, None)
# os.chdir("C:\\Users\\My PC\\Desktop\\sounds")
songs = []
for file in glob.glob("*.wav"):
    songs.append(file)
for file in glob.glob("*.mp3"):
    songs.append(file)
random.shuffle(songs)'''
'''def slow_volume():
    for i in range(-65,0,-1):
        volume.SetMasterVolumeLevel(i,None)
        time.sleep(1)
t = thread.Thread(target=slow_volume)
t.start()'''
'''while True:
    winsound.PlaySound("PrettyRaveGir.wav",winsound.SND_FILENAME)'''
# volume.SetMasterVolumeLevel(-1,None)

# winsound.PlaySound('polarize.wav',winsound.SND_FILENAME)
# end VolumeOnlyAlarm.py-----------------------------------

# make application


class AlarmClock(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()

        tk.Label(master, text="Select Time:").grid(row=1, column=0)
        tk.Label(master, text="Hour").grid(row=0, column=1, pady=10)
        tk.Label(master, text="Minute").grid(row=0, column=2, pady=10)
        self.hourPicker = tk.Listbox(master)
        self.hourPicker.grid(row=1, column=1, padx=10)
        for i in range(0, 24):
            self.hourPicker.insert(tk.END, str(i))

        self.minutePicker = tk.Listbox(master)
        self.minutePicker.grid(row=1, column=2, padx=10)
        for i in range(0, 60):
            self.minutePicker.insert(tk.END, str(i))

        self.submit = tk.Button(master, text="SUBMIT", command=self.setAlarm)
        self.submit.grid(row=2, column=1, columnspan=2)

        self.timeLabel = tk.Label(master, font='-size 44')
        self.timeLabel.grid(row=1, column=3)

    def setAlarm(self):
        alarmTime = [self.hourPicker.get(tk.ACTIVE), self.minutePicker.get(tk.ACTIVE)]
        # print(alarmTime)
        hour = int(alarmTime[0])
        minute = int(alarmTime[1])
        isAlarm = False
        while not isAlarm:
            now = time.localtime()
            # print("got time")
            if now.tm_hour == hour and now.tm_min == minute:
                isAlarm = True
            else:
                # print("else")
                self.set_time(now.tm_hour, now.tm_min, now.tm_sec)
                self.timeLabel.update()
                self.after(1)

        volume.SetMasterVolumeLevel(-1, None)

        def play():
            while True:
                winsound.PlaySound("shit.wav", winsound.SND_FILENAME)
        t = thread.Thread(target=play)
        t.start()

    def set_time(self, hr, mnt, sec):
        if len(str(hr)) == 1:
            hr = '0'+str(hr)
        if len(str(mnt)) == 1:
            mnt = '0'+str(mnt)
        if len(str(sec)) == 1:
            sec = '0' + str(sec)
        self.timeLabel['text'] = "{}:{}:{}".format(hr, mnt, sec)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Alarm Clock")
    root.geometry("600x300+300+300")
    app = AlarmClock(root)
    root.mainloop()
