import time
import yaml  
import math
import os

from os import path
from qhue import Bridge, QhueException, create_new_username
# 1 grab lights and save current state
# 2 start a timer for 30 seconds and keep track
# 2 disco the lights to the music stop after timer is done
# 3 after done, put lights back

from timeit import default_timer as timer
from datetime import timedelta

start = timer()
end = timer()
#print(timedelta(seconds=end-start))

# the IP address of your bridge
BRIDGE_IP = "192.168.0.134"
# the path for the username credentials file
CRED_FILE_PATH = "/home/pi/code/flyers/qhue_username.txt"

def EnhanceColor(normalized):
    if normalized > 0.04045:
        return math.pow( (normalized + 0.055) / (1.0 + 0.055), 2.4)
    else:
        return normalized / 12.92

def RGBtoXY(r, g, b):
    rNorm = r / 255.0
    gNorm = g / 255.0
    bNorm = b / 255.0

    rFinal = EnhanceColor(rNorm)
    gFinal = EnhanceColor(gNorm)
    bFinal = EnhanceColor(bNorm)
    
    X = rFinal * 0.649926 + gFinal * 0.103455 + bFinal * 0.197109
    Y = rFinal * 0.234327 + gFinal * 0.743075 + bFinal * 0.022598
    Z = rFinal * 0.000000 + gFinal * 0.053077 + bFinal * 1.035763

    if X + Y + Z == 0:
        return (0,0)
    else:
        xFinal = X / (X + Y + Z)
        yFinal = Y / (X + Y + Z)
    
        return (xFinal, yFinal)

def main():
    # check for a credential file
    with open(CRED_FILE_PATH, "r") as cred_file:
        username = cred_file.read()

    # create the bridge resource, passing the captured username
    b = Bridge(BRIDGE_IP, username)
    # create a lights resource
    lights = b.lights

    # query the API and print the results
    #print(lights())
    #print(yaml.safe_dump(lights(), indent=4))
    
    white =RGBtoXY(1,1,1) # blakc
    orange=RGBtoXY(255,131,0) # orange rgba(255, 132, 0, 1)
    #orange=RGBtoXY(255,103,61) # orange rgba(255, 132, 0, 1)
        
    

    light_ids = [1,2,3,4]
    STATES=[1,2,3,4,5];

    maxer = 26 #music is 26 seconds long
    end = timer();
    i=end-start


    #shut them all off
    for id in light_ids:
        lights[id].state(on = False)

    time.sleep(0.1)
    
    lights[1].state(on = True, bri=154, xy = white)
    lights[2].state(on = True, bri=254, xy = orange)
    lights[3].state(on = False);
    lights[4].state(on = True, bri=254, xy = orange)
    
    STATES[1]="white"
    STATES[2]="orange"
    STATES[3]="black"
    STATES[4]="orange"

    while i < maxer:
        print("TIMER:"+str(i))
        for id in light_ids:
            if(STATES[id]=="orange"): 
                STATES[id]="white"
                lights[id].state(on = True, bri=154, xy = white,transitiontime=1)
            elif(STATES[id]=="white"): 
                #myxy=black
                STATES[id]="black"
                lights[id].state(on = False,transitiontime=1)

            else:
                STATES[id]="orange"
                lights[id].state(on = True, bri=254, xy = orange,transitiontime=1)

            time.sleep(0.1)


        
        end = timer();
        time.sleep(0.5)
        i=end-start # set our counter
    
    #shut them all off
    for id in light_ids:
        lights[id].state(on = False)
    	time.sleep(0.4)

    time.sleep(3) #pause

    #fade to white
    for id in light_ids:
        lights[id].state(on = True, bri=254, xy = white,transitiontime=20)
        time.sleep(0.4)

    #myx,myy =RGBtoXY(3,3,3) # blakc
    #lights[1].state(on = True, bri=254, xy = [myx, myy])
    #myx,myy =RGBtoXY(255,131,0) # orange rgba(255, 132, 0, 1)
    #lights[2].state(on = True, bri=254, xy = [myx, myy])

if __name__ == "__main__":
    #kill our player/start music/start the show.    
    os.system('killall -9 omxplayer.bin');
    os.system('omxplayer -o local --no-keys /home/pi/code/flyers/flyershorn_cut.mp3&') #26 seconds long, run it in the background and then start the show
    main()




