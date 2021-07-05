


import _thread

import signal

#from subprocess import Popen, PIPE
import subprocess
global compProc
_thread.start_new_thread(
try:
    # capture_output = True gets stderr and stdout as elements of the returned compProc
    # Exceptions raised in the child process, before the new program has 
    # started to execute, will be re-raised in the parent.
    compProc = subprocess.Popen(['rec',  '/media/pi/MACBANK/twattock.wav'], \
        stdout = subprocess.PIPE, stderr = subprocess.PIPE, text=True)
    # following line will trigger a python calledProcessError if rerturncode is none zero
    #compProc.communicate()
    # POLL method
    #x = compProc.poll()
    #print("output from poll: ", x)
    # COMMUNICATE
    x = compProc.communicate()
    print("output from communicate: ", x[1])
    # STDERR
    #x = compProc.stderr
    #print("output from stderr: ", x)
    #subprocess.

except subprocess.CalledProcessError: # as inst:
    #print(compProc)
    print("We had a called process error")
    #print(type(inst))    # the exception instance
    #print(inst.args)     # arguments stored in .args
    #print(inst)          # __str__ allows args to be printed directly,
                          # but may be overridden in exception subclasses
    #x, y = inst.args     # unpack args
    #print('x =', x)
    #print('y =', y)
except KeyboardInterrupt:
    #x = compProc.communicate()
    #print (x[1])
    print("We had a keyboard interrupt!!!")


)

x = input("press space to stop")
#stderr = proc.communicate()

#print(stderr)
compProc.send_signal(signal.SIGINT) ## Send interrupt signal
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