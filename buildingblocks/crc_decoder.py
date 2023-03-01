#analyse the respons of the STM-peha unit
#C0 00 fe 06 16 01 01 f0 59 72 c1
#asuming the data-packet and crc was flawless and not corrupted

def decode_crc_usb_rs232( datastring):
    datastring = datastring.upper()
    list_datastring = datastring.split(' ')
    # remove start and stopbytes
    if list_datastring[0] == "C0":
        list_datastring.pop(0)
    if list_datastring[-1] == "C1":
        pass
        list_datastring.pop(-1)
    #find replace escaped characters to original characters
    # C0 is escaped by 7D E0
    # C1 is escaped by  7D E1
    # 7D is escaped by  7D 5D
    #find index of byte 7D , and check the following byte
    # get the index of '7D'
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
    print(" ".join(list_datastring).upper())

#example with escaped  char C0(crc_usb_rs232("fe 00 06 05 00 01 01"))  #expecting c0 fe 00 06 05 00 01 01 9e 7d e0 c1 = correct


datastring = "c0 00 fe 06 16 01 01 f0 59 72 c1"


#decode_crc_usb_rs232(datastring)
decode_crc_usb_rs232("c0 fe 00 06 05 00 01 01 9e 7d e0 c1") #expected fe 00 06 05 00 01 01





