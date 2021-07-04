



import signal

#from subprocess import Popen, PIPE
import subprocess
try:
    # capture_output = True gets stderr and stdout as elements of the returned compProc
    compProc = subprocess.run(['rec',  'twattock.wav'], capture_output=True, check = True)
    # following line will trigger a python calledProcessError if rerturncode is none zero
    compProc.check_returncode()
    subprocess.

except subprocess.CalledProcessError:
    print(compProc)
    print("We had a called process error")
except KeyboardInterrupt:
    print("We had a keyboard interrupt!!!")




x = input("press space to stop")
#stderr = proc.communicate()

#print(stderr)
proc.send_signal(signal.SIGINT) ## Send interrupt signal
 """

#process = Popen(['ls', '-l'], stdout=PIPE, stderr=PIPE)

#stdout, stderr = process.communicate()

#print(stdout)

 


import signal

import subprocess 

# -r: sample rate
# -b: bit rate
sRate = "48000"

numChans = "2"
bitDepth = "16"
global proc
try:
    proc = subprocess.Popen(["rec", "sunday.bollo"], \
        stdout = subprocess.PIPE, stderr = subprocess.PIPE, text=True)     
except:
    print("load of old bollocks!")


x = input("press space to stop")
#stderr = proc.communicate()

#print(stderr)
proc.send_signal(signal.SIGINT) ## Send interrupt signal
"""