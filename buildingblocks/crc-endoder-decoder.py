
def decode_crc_usb_rs232( datastring):
    datastring = datastring.upper()
    list_datastring = datastring.split(' ')
    # remove start and stopbytes
    if list_datastring[0] == "C0":
        list_datastring.pop(0) #remove startbyte
    if list_datastring[-1] == "C1":
        list_datastring.pop(-1) #remove last byte ( stopbyte)
    #find replace escaped characters to original characters
    # C0 is escaped by 7D E0
    # C1 is escaped by  7D E1
    # 7D is escaped by  7D 5D
    #find index of byte 7D , and check the following byte
    # get the index of '7D'
    if '7D' in list_datastring:
        escapeposition = list_datastring.index('7D')
        if escapeposition > 0 :
            pass #possibility that there was an  excaped byte
            if list_datastring[escapeposition +1 ] == "E0":
                list_datastring.pop(escapeposition + 1 )
                list_datastring[escapeposition] = "C0"
            elif list_datastring[escapeposition + 1] == "E1":
                list_datastring.pop(escapeposition + 1)
                list_datastring[escapeposition] = "C1"
            elif list_datastring[escapeposition + 1] == "5D":
                list_datastring.pop(escapeposition + 1 )
                list_datastring[escapeposition] = "7D"

    #remove the crc (2 bytes ) we don't need them anymore
    list_datastring.pop(-1)  # remove last byte crc
    list_datastring.pop(-1)  # remove last byte crc
    return  " ".join(list_datastring).upper()

#####################start functie crc berekenen
def crc_rs485( ext):
    tabelcrcberekenen = ext.split(' ')
    tempcrc = int(65535)
    for x in tabelcrcberekenen:
        yy = int(x, 16)
        tempcrc = tempcrc ^ yy
        for r in range(0, 8):
            som = tempcrc & int(1)
            if (som == 1):
                tempcrc = tempcrc >> 1
                tempcrc = tempcrc ^ 33800  # 0x8408 polynoom
            else:
                tempcrc = int(tempcrc / 2)
    tempcrc = tempcrc ^ 65535  # laaste grote berekening
    tempcrc = tempcrc + 65536  # postprocessing ,voorloopnul  ervoor , zorg dat je altijd 5 karkters hebt , waarvan de 4 rechtse de crc zijn
    CRCstring = str(tempcrc)
    crcstring = str(hex(tempcrc)).upper()
    crcdeel1 = crcstring[5] + crcstring[6]
    crcdeel2 = crcstring[3] + crcstring[4]
    tabelcrcberekenen.append(crcdeel1)
    tabelcrcberekenen.append(crcdeel2)
    return " ".join(tabelcrcberekenen).upper()
#####################end functie crc berekenen



#####################start functie crc berekenen
def crc_usb_rs232( ext):
    ext = ext.upper()
    tabelcrcberekenen = ext.split(' ')
    tempcrc = int(65535)
    for x in tabelcrcberekenen:
        yy = int(x, 16)
        tempcrc = tempcrc ^ yy
        for r in range(0, 8):
            som = tempcrc & int(1)
            if (som == 1):
                tempcrc = tempcrc >> 1
                tempcrc = tempcrc ^ 33800  # 0x8408 polynoom
            else:
                tempcrc = int(tempcrc / 2)
    tempcrc = tempcrc ^ 65535  # laaste grote berekening
    tempcrc = tempcrc + 65536  # postprocessing ,voorloopnul  ervoor , zorg dat je altijd 5 karkters hebt , waarvan de 4 rechtse de crc zijn
    CRCstring = str(tempcrc)
    crcstring = str(hex(tempcrc)).upper()
    crcdeel1 = crcstring[5] + crcstring[6]
    crcdeel2 = crcstring[3] + crcstring[4]
    tabelcrcberekenen.append(crcdeel1)
    tabelcrcberekenen.append(crcdeel2)
    startbyte = "C0"
    stopbyte = "C1"

    #C0 komt 7DE0    C1 komt 7DE1   7D komt 7D5D

    for value in range(len(tabelcrcberekenen)):
        if tabelcrcberekenen[value] == '7D':
            tabelcrcberekenen[value] = '7D 5D'


        if tabelcrcberekenen[value] == 'C0':
            tabelcrcberekenen[value] = '7D E0'

        if tabelcrcberekenen[value] == 'C1':
            tabelcrcberekenen[value] = '7D E1'

        if tabelcrcberekenen[value] == '7D':
            tabelcrcberekenen[value] = '7D 5D'


    return startbyte +" " + " ".join(tabelcrcberekenen).upper() + " " + stopbyte
#####################end functie crc berekenen
INPUT =  "fe 00 01 14 40 c0 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff"
expecting ="c0 fe 00 01 14 40 7d e0 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff 6e d4 c1"
INPUTcrc = crc_usb_rs232(INPUT.upper())
BACKtoINPUT = decode_crc_usb_rs232(INPUTcrc.upper())
print("***************")
print("calcrcr      ",INPUTcrc.upper())
print("expected     ",expecting.upper())
print("in           " ,INPUT.upper())
print("backto input " , BACKtoINPUT.upper())
print("***************")


INPUT =  "fe 00 06 05 00 01 01"
expecting ="c0 fe 00 06 05 00 01 01 9e 7d e0 c1"
INPUTcrc = crc_usb_rs232(INPUT.upper())
BACKtoINPUT = decode_crc_usb_rs232(INPUTcrc.upper())
print("***************")
print("calcrcr      ",INPUTcrc.upper())
print("expected     ",expecting.upper())
print("in           " ,INPUT.upper())
print("backto input " , BACKtoINPUT.upper())
print("***************")




INPUT =  "00 fe 01 44"
expecting ="c0 00 fe 01 44 09 7d 5d c1"
INPUTcrc = crc_usb_rs232(INPUT.upper())
BACKtoINPUT = decode_crc_usb_rs232(INPUTcrc.upper())
print("***************")
print("calcrcr      ",INPUTcrc.upper())
print("expected     ",expecting.upper())
print("in           " ,INPUT.upper())
print("backto input " , BACKtoINPUT.upper())
print("***************")



INPUT =  "00 fe 06 0e 1f 01 f0"
expecting ="c0 00 fe 06 0e 1f 01 f0 ae 7d e1 c1"
INPUTcrc = crc_usb_rs232(INPUT.upper())
BACKtoINPUT = decode_crc_usb_rs232(INPUTcrc.upper())
print("***************")
print("calcrcr      ",INPUTcrc.upper())
print("expected     ",expecting.upper())
print("in           " ,INPUT.upper())
print("backto input " , BACKtoINPUT.upper())
print("***************")


INPUT =  "00 fe 06 0e 1f 01 f0"
expecting ="c0 00 fe 06 0e 1f 01 f0 ae 7d e1 c1"
INPUTcrc = crc_usb_rs232(INPUT.upper())
BACKtoINPUT = decode_crc_usb_rs232(INPUTcrc.upper())
print("***************")
print("calcrcr      ",INPUTcrc.upper())
print("expected     ",expecting.upper())
print("in           " ,INPUT.upper())
print("backto input " , BACKtoINPUT.upper())
print("***************")


INPUT =  "FE 00 06 05 00 01 01"
expecting ="C0 FE 00 06 05 00 01 01 9E 7D E0 C1"
INPUTcrc = crc_usb_rs232(INPUT)
BACKtoINPUT = decode_crc_usb_rs232(INPUTcrc)
print("***************")
print("calcrcr      ",INPUTcrc.upper())
print("expected     ",expecting.upper())
print("in           " ,INPUT.upper())
print("backto input " , BACKtoINPUT.upper())
print("***************")



INPUT =  "fe 00 30 00 06"
expecting ="c0 fe 00 30 00 06 f1 d2 c1"
INPUTcrc = crc_usb_rs232(INPUT)
BACKtoINPUT = decode_crc_usb_rs232(INPUTcrc)
print("*****wat is u spanning?**********")
print("calcrcr      ",INPUTcrc.upper())
print("expected     ",expecting.upper())
print("in           " ,INPUT.upper())
print("backto input " , BACKtoINPUT.upper())
print("***************")



INPUT =  "00 fe 30 01 06 31 39 2c 35 56"
expecting ="c0 00 fe 30 01 06 31 39 2c 35 56 26 cb c1"
INPUTcrc = crc_usb_rs232(INPUT)
BACKtoINPUT = decode_crc_usb_rs232(INPUTcrc)
print("*****19,5V**********")
print("calcrcr      ",INPUTcrc.upper())
print("expected     ",expecting.upper())
print("in           " ,INPUT.upper())
print("backto input " , BACKtoINPUT.upper())
print("***************")