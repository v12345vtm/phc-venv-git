#!/usr/bin/env python
import sys


if "/" in  (sys.executable) :
    machine = "raspi"
    print(f"deze machine is een {machine}-systeem")
    # importeer de GPIO bibliotheek voor raspberry pi
    import RPi.GPIO as GPIO
    import serial.tools.list_ports  # op raspi bestaat dit om de comport /dev/tty/USB te vinden

    overzichtcompoorten = ((serial.tools.list_ports.comports()))  # raspi comportd
    x=5



if ":" in  (sys.executable) :
    machine = "windows"
    print(f"deze machine is een {machine}-systeem")
    import wmi  # WMI voor win10laptop om u compoort te vinden COM

    query = "SELECT * FROM Win32_PnPEntity WHERE Name LIKE '%(COM%)'"
    overzichtcompoorten = wmi.WMI().query(query)

    for com in overzichtcompoorten:
        pass
        #print(com.Name) #vb 'USB-SERIAL CH340 (COM8)'
        #str_comport = com.name


if len(overzichtcompoorten) == 0:
    raise Exception("execptionvith : Geen comport aanwezig")


for uarts in   overzichtcompoorten:
    print(f' gevonden op {machine} maschine  : poort: {uarts.name} ')




def voorkeurscompoortnenem(lijstcompoorten):
    #we willen een COM indien windows , en usbomvormer ipv AMEA op de gpio
    for uarts in lijstcompoorten:
        if "ttyUSB"    in uarts.name:
            voorkeurpoort = uarts[0]
            print(f' voorkeurpoort {voorkeurpoort}   ')
            return  voorkeurpoort  #  "/dev/ttyUSB0" #usb to db9 convertor

        if "COM"    in uarts.name:
            temp = uarts.name
            startpos =  temp.find("(")
            stoppos = temp.find(")")
            voorkeurpoort = temp[startpos+1:stoppos]
            print(f' voorkeurpoort {voorkeurpoort}   ')
            return  voorkeurpoort







gevondencompoort= voorkeurscompoortnenem(overzichtcompoorten)
gevondencompoort= "COM9" #override as debug
from time import sleep
import serial

serielepoort = serial.Serial(
        port=gevondencompoort,
        baudrate = 19200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=None)

serielepoort.write(b'\n\nhello from python\n' )



while 1:

    sleep(0.2)
    commando = "c0 fe 00 06 15 01 01 01 e3 59 c1"  #stm0 what is your firmwareversion ? response is 2.28 :     c0 00 fe 05 0e 14 00 03 16 02 17 39 39 a1 91 c1
    commando = "c0 fe 00 06 15 01 01 01 e3 59 c1"  #stm0 what is status inputmod 01 ? :     c0 00 fe 06 16 01 04 01 ff 00 *80* 7a 15 c1
    zendtabel = commando.split(' ')
    for el in zendtabel:
        d = int(el ,16)
        dd = bytes([d]²&)
        serielepoort.write(dd)
    print(f"sended : {commando}")


    #x = ser.read_until(b'\xc1').hex()
    #x= ser.read_all().hex()
    sleep(1)
    bytesToRead = serielepoort.inWaiting()


    hoeveelbytekregenwebinnen = serielepoort.inWaiting()
    print("ik krijg xxx bytes binnen als respons : " + str(serielepoort.inWaiting()) + "\n")
    feedback = ""  # wistabel
    for aantalelementen in range(0, serielepoort.inWaiting()):
        x = serielepoort.read().hex()
        feedback = feedback + " " + x
        # print(feedback)
        if serielepoort.inWaiting() == 0:
            # print("\n")
            # print(feedback)

            print(f" ,ik krijg {hoeveelbytekregenwebinnen} bytes binnen als respons , en volgende data : {feedback}"  )

