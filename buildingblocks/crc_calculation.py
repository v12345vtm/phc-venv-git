


#####################start functie crc berekenen
def crc_rs485( ext):
    tabelcrcberekenen = list()
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
    tabelcrcberekenen = list()
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
            tabelcrcberekenen[value] = '7D*5D'


        if tabelcrcberekenen[value] == 'C0':
            tabelcrcberekenen[value] = '7D*E0'

        if tabelcrcberekenen[value] == 'C1':
            tabelcrcberekenen[value] = '7D*E1'

        if tabelcrcberekenen[value] == '7D':
            tabelcrcberekenen[value] = '7D*5D'


    return startbyte +" " + " ".join(tabelcrcberekenen).upper() + " " + stopbyte
#####################end functie crc berekenen
print(crc_usb_rs232("fe 00 01 14 40 c0 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff"))  #expecting c0 fe 00 01 14 40 7d e0 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff 6e d4 c1 = NOT correct
print(crc_usb_rs232("fe 00 06 05 00 01 01"))  #expecting c0 fe 00 06 05 00 01 01 9e 7d e0 c1 = correct
print(crc_usb_rs232("00 fe 01 44"))  #expecting c0 00 fe 01 44 09 7d 5d c1 = correct
print(crc_usb_rs232("00 fe 06 0e 1f 01 f0"))  #expecting c0 00 fe 06 0e 1f 01 f0 ae 7d e1 c1 = correct



print(crc_rs485("fe 00 05 0d"))  #expecting : fe 00 05 0d ea 80

print(crc_usb_rs232("fe 00 05 0d"))  #expecting : c0 fe 00 05 0d ea 80 c1


print(crc_usb_rs232("fe 00 06 7c 80 01 01"))  #expecting     c0 fe 00 06 7c 80 01 01 54 6f c1                  Àþ..|€..ToÁ

print(crc_usb_rs232("fe 00 06 7f 80 01 01"))  #expecting     c0 fe 00 06 7f 80 01 01 99 4a c1

#ene met 7dE1
# #C0 komt 7DE0    C1 komt 7DE1   7D komt 7D5D
print(crc_usb_rs232("fe 06 0e 1f 01 f0"))  #expecting         c0 00 fe 06 0e 1f 01 f0 ae 7d e1 c1               À.þ....ð®}áÁ

#c0 fe 00 01 14 40 7d e0 ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff 6e d4 c1



