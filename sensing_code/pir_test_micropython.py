import machine
import utime


pollingRate = 0.1 #seconds
pir = machine.Pin(3, machine.Pin.IN)
LIGHT = machine.Pin(13, machine.Pin.OUT) # GP13

while True:
    motion = pir.value()
    
    if motion == 1:
        LIGHT.on()
        print("MOTION DETECTED")
    else:
        LIGHT.off()
        print("NOTHING")
        
    utime.sleep(pollingRate)
    

        
    

