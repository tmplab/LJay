
#!/usr/bin/env python


# Process events coming from Mcontroller (midi over serial version) in a separate thread. 
def MSerialinProcess():

    MESSAGE = 0xFF
    
    '''
    previously : to manually decode midi message. Switched to Mido functions (type, attributes)
    CONTROL_CHANGE = 0xB0
    PLAY_NOTE = 0x90
    END_NOTE = 0x80
    counter = 0
    cmd = 0
    channel = 0
    '''
    sermsg = [0,0,0]
    
    # pack bytes from serial port by 3. todo : check for different sizes midi message
    # mido convert 3 bytes array in midi message for decoding channel number,...
    
    while True:
        sermsg[0] = ord(Mser.read())
        #print b, b & MESSAGE, b - 144
        if sermsg[0] = MESSAGE:
            # command
            #cmd = sermsg[0]
            #channel = cmd - 144 + 1
            #print "cmd, chan",cmd,channel
            sermsg[1]= ord(Mser.read()[0])
            sermsg[2]= ord(Mser.read()[0])
            sermsg[3]= ord(Mser.read()[0])
            print sermsg
            
            #MMessage = mido.Message.from_bytes(sermsg)
            
            if MMessage.type == 'note_on':
                MidiNoteOn(MMessage.note, MMessage.velocity)
            if MMessage.type == 'note_off':
                MidiNoteOff(MMessage.note, MMessage.velocity)
            if MMessage.type == 'control_change':
                MidiMsg(sermsg)           
            
            '''
            if cmd == CONTROL_CHANGE:
                number = int(b)
                value = ord(Mser.read()[0])
                print(channel, 'CC : ',  number,value)
                cmd = 0
            if cmd == PLAY_NOTE:
                note = int(b)
                velocity = ord(Mser.read()[0])
                print( 'play note', channel,note, velocity)
                MidiNoteOn(note, velocity)
                cmd = 0
            if cmd == END_NOTE:
                note = int(b)
                velocity = ord(Mser.read()[0])
                print('end note', channel,note, velocity)
                cmd = 0
            '''
            
        time.sleep(0.02)
#

print("")
print("Available serial devices")
ports = list(list_ports.comports())
for p in ports:
    print(p)

try:
    cdc = next(list_ports.grep("USB2.0-Serial"))
    print ("Serial Picked : ",cdc[0])
    Mser = serial.Serial(cdc[0],31250) 
    thread = Thread(target=MSerialinProcess, args=())
    thread.setDaemon(True)
    thread.start()
    
except StopIteration:
    print ("No device found")
    Mser = False
  
#    

