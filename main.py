import time, threading, os, datetime
from pythonosc import dispatcher
from pythonosc import osc_server

def start(addr, *stuff):
    global f, recording
    if recording == False:
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
        basename = str(stuff[0])
        filename = basename+"_"+timestamp+".txt"
        f = open(filename, 'w')
        print ("Logging ON")
        print ("Logging to file "+filename)
        recording = True

def stop(addr, *stuff):
    print(addr+" received")
    global f, recording
    if recording == True:
        recording = False
        print ("Disabling logging, saving file...")
        f.close()
    print ("Logging OFF")

def recordData(addr, *stuff):
    global f, recording
    if recording == True and addr != "/start" and addr != "/stop":
        toString = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S.%f')
        toString = toString + "\t" + addr
        toString = toString + "\t" + "\t".join(map(str, stuff))
        toString.strip()
        print("Logged: "+toString)
        f.write(toString+'\n')

if __name__ == "__main__":
    # Change these defaults to suit your needs:
    OSCport = 6655
    OSCaddress = '127.0.0.1'

    dispatcher = dispatcher.Dispatcher()
    recording = False
    test = "xyz"
    dispatcher.map("/start", start)
    dispatcher.map("/stop", stop)
    dispatcher.map("*", recordData)

    server = osc_server.ThreadingOSCUDPServer(
        (OSCaddress, OSCport), dispatcher)
    print("Logging OSC data on {}".format(server.server_address))
    print ("Logging OFF")
    server.serve_forever()
