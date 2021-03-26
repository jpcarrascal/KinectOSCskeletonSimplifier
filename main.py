import time, threading, os, datetime
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc.udp_client import SimpleUDPClient
from signal import signal, SIGINT
from sys import exit
# Sample head message /bodies/72057594037928017/joints/Head

def run(addr, *args):
    global body, bodyFound, inferredCount
    newAddr = ""
    if addr.startswith("/bodies"):
        if addr.endswith("Head") and body != "":
            if args[3] == "Inferred":
                inferredCount += 1
                print(f"Losing body... {inferredCount}")
            if args[3] == "NotTracked" or inferredCount > 17:
                print(f"Body lost {body}, {args[3]}, {inferredCount}")
                inferredCount = 0
                body = ""
            if args[3] == "Tracked" and inferredCount > 0:
                inferredCount = 0
                print(f"Body is back... {inferredCount}")
        elif addr.endswith("Head") and body == "":
            if args[3] == "Tracked":
                body = addr.split("/")[2]
                inferredCount = 0
                print(f"Body found: {body}")
        if addr.split("/")[2] == body:
            if addr.endswith("Head"):
                newAddr = "/head"
            elif addr.endswith("hands/Left"):
                newAddr = "/leftHand/status"
            elif addr.endswith("hands/Right"):
                newAddr = "/rightHand/status"
            elif addr.endswith("HandTipLeft"):
                newAddr = "/leftHand/position"
            elif addr.endswith("HandTipRight"):
                newAddr = "/rightHand/position"
            else:
                newAddr = ""
            if newAddr != "":
                client.send_message(newAddr, args)
                if debug:
                    print(f"Sending {newAddr} {args} to {outAddress}:{outOSCport}")
        else:
            discarded = addr.split("/")[2]
            if debug:
                print(f"Another body found: {discarded} discarding...")

def stop(signal_received, frame):
    # Handle any cleanup here
    print("Exiting...")
    exit(0)

if __name__ == "__main__":
    # Change these defaults to suit your needs:
    inOSCport = 12345
    outOSCport = 56789
    inAddress = '192.168.1.130'
    outAddress = '192.168.1.130'
    body = ""
    inferredCount = 0
    debug = False
    signal(SIGINT, stop)

    client = SimpleUDPClient(outAddress, outOSCport)

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("*", run)

    server = osc_server.ThreadingOSCUDPServer(
        (inAddress, inOSCport), dispatcher)
    print("Receiving skeleton data on {}".format(server.server_address))
    server.serve_forever()

