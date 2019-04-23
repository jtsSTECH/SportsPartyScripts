import os
import subprocess
import time

#built from the speech-recog.sh script found in the package https://github.com/jtsSTECH/PiAUISuite
#Its constantly listening and searching for our command phrases.

hardware="plughw:1,0"
duration="2"
lang="en"
hw_bool=0
dur_bool=0
lang_bool=0
cmd="arecord -D %s -t wav -d %s -r 16000 | flac - -f --best -o /dev/shm/out.flac 1>/dev/shm/voice.log 2>/dev/shm/voice.log; curl -sS -X POST --data-binary @/dev/shm/out.flac --user-agent 'Mozilla/5.0' --header 'Content-Type: audio/x-flac; rate=16000;' 'https://www.google.com/speech-api/v2/recognize?output=json&lang=%s&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw&client=Mozilla/5.0' | sed -e 's/[{}]/''/g' | awk -F"":"" '{print $4}' | awk -F"","" '{print $1}' " % (hardware, duration,lang)
#print cmd


try:
    while True:
		## call command
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		## Wait for date to terminate. Get return returncode ##
		p_status = p.wait()
		#print "Command output : ", output
		#print "Command exit status/return code : ", p_status
		output = output.replace("\n", "")
		output = output.replace('"', "")
		output=output.lower()
		print "Our string: "+output

		#cheap command processing:
		flyerscoms = ("go flyers", "nice flyers", "awesome flyers", "flyers goal", "the flyers","little flyers", "flyers score")
		philliescoms = ("go phillies", "homerun", "grandslam", "out of here", "phillies homerun")

		if any(s in output for s in flyerscoms):
		        print "yay Flyers matched!"
		        #do stuff here

		if any(s in output for s in philliescoms):
		        print "yay phillies matched!"
		        #do stuff here
		#time.sleep(3) #pause
except KeyboardInterrupt:
    print('interrupted!')
#rm /dev/shm/out.flac
