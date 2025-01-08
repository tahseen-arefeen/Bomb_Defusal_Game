'''
WELCOME TO PRESENT DEFUSER
TAHSEEN AREFEEN

Rules:
Step 1: Remove a wire of of your choosing from the present
Step 2: Pass the present to the next player
Step 3: Repeat

There are no winners, only losers

Disclaimer:
THIS IS PARODY/PROP/JOKE DEVICE NOT AN ACTUAL EXPLOSIVE DEVICE
ANY ATTEMPT TO POTRAY THE DEVICE AS A REAL EXPLOSIVE IS AGAINST THE CREATOR'S WISHES
'''

########################### IMPORT STATEMENTS ###########################
import board
import digitalio
import time
import random


########################### INIT FEATHER ###########################
'''
Initializes wire Sensors on Board 
'''
def SetWires():
    global wire_1, wire_2, wire_3, wire_4, wire_5, wire_6, wire_7, wire_all

    wire_1 = digitalio.DigitalInOut(board.A0)
    wire_1.direction = digitalio.Direction.INPUT

    wire_2 = digitalio.DigitalInOut(board.A1)
    wire_2.direction = digitalio.Direction.INPUT

    wire_3 = digitalio.DigitalInOut(board.A2)
    wire_3.direction = digitalio.Direction.INPUT

    wire_4 = digitalio.DigitalInOut(board.A3)
    wire_4.direction = digitalio.Direction.INPUT

    wire_5 = digitalio.DigitalInOut(board.D24)
    wire_5.direction = digitalio.Direction.INPUT

    wire_6 = digitalio.DigitalInOut(board.D25)
    wire_6.direction = digitalio.Direction.INPUT

    wire_7 = digitalio.DigitalInOut(board.SCK)
    wire_7.direction = digitalio.Direction.INPUT

    wire_all = [wire_1, wire_2, wire_3, wire_4, wire_5, wire_6, wire_7]

'''
Initializes LEDs on Board 
'''
def SetLeds():
    global led_1, led_2, led_3, led_4, led_5, led_all

    led_1 = digitalio.DigitalInOut(board.D9)
    led_1.direction = digitalio.Direction.OUTPUT

    led_2 = digitalio.DigitalInOut(board.D10)
    led_2.direction = digitalio.Direction.OUTPUT

    led_3 = digitalio.DigitalInOut(board.D11)
    led_3.direction = digitalio.Direction.OUTPUT

    led_4 = digitalio.DigitalInOut(board.D12)
    led_4.direction = digitalio.Direction.OUTPUT

    led_5 = digitalio.DigitalInOut(board.D13)
    led_5.direction = digitalio.Direction.OUTPUT
    
    led_all = [led_1, led_2, led_3, led_4, led_5]

'''
Initializes Motor 
'''
def SetMotor():
    global motor

    motor = digitalio.DigitalInOut(board.D5)
    motor.direction = digitalio.Direction.OUTPUT

'''
Initializes Power Switch on Board 
'''
def SetSwitches():
    global power

    power = digitalio.DigitalInOut(board.D4)
    power.direction = digitalio.Direction.INPUT

'''
Master Set Up 
'''
def SetAll():
    SetWires()
    SetLeds()
    SetMotor()
    SetSwitches()
    
    global wire
    wire = [1, 2, 3, 4, 5, 6, 7]

    global boom_wire
    boom_wire = WirePick(wire)

    #Power state determined by var being odd or even
    global power_toggle
    power_toggle = 1

    ## for debugging ##
    print(boom_wire)
    print(WireDiagnose())


########################### GAMEPLAY FUNCTIONS ###########################
'''
Creates wire end state
''' 
def BOOM():

    motor.value = True

    while (power_toggle % 2) == 0:
        for i in led_all:
            i.value = True

        time.sleep(.25)
        
        for i in led_all:
            i.value = False

        time.sleep(.25)

    motor.value = False
    for i in led_all:
        i = False
    
    #Change Boom wire for next game
    global boom_wire
    boom_wire = WirePick(wire)

'''
Pick Wire from set to be Live 
Takes a selection of wires
Returns a randomly selected wire
'''
def WirePick(sample):
    pick = random.randint(0, len(sample) - 1)
    live_wire = sample[pick]
    return live_wire

'''
Diagnoses which wires are Connected
Returns which wires are cut and which are connected
'''
def WireDiagnose():
    cut_wire = []
    uncut_wire = []

    for i in wire_all:
        count = wire_all.index(i) + 1

        if wire_1.value is False:
            cut_wire.append(count)
        if wire_1.value is True:
            uncut_wire.append(count)

    return cut_wire, uncut_wire

########################### GAMEPLAY LOOP ###########################
'''
Main Gameplay Loop
'''
def GameOriginal():
    print('game has begun') 

    tick = time.monotonic() + 1

    motor.value = False

    while power.value is False:
        cut_wire, uncut_wire = WireDiagnose()
        
        if boom_wire in cut_wire:
            print('BOOM')
            print(cut_wire, uncut_wire)
            BOOM()
            break

        if time.monotonic() == tick:
            
            motor.value = True
            print('go')
            time.sleep(.35)

            tick = time.monotonic() + .5
        motor.value = False


########################### DEBUGGING TOOLS ###########################
'''
Troubleshoot LEDs
If LEDs blink every second, LEDs are functional
'''
def TestLeds():
    for i in led_all:
        i = True
    time.sleep(1)
    for i in led_all:
        i = False
    time.sleep(1)

'''
Troubleshoot Power Switch
If LEDs Turn on with Switch, Switch is functional
'''
def TestSwitches():
    if power.value is True:
        for i in led_all:
            i = True
    else:
        for i in led_all:
            i = False

'''
Troubleshoot Power Code
If LEDs turn on with Switch, Switch code is functional
'''
def TestSwitchCode():
    if (power_toggle % 2) == 0:
        for i in led_all:
            i = True

    else:
        for i in led_all:
            i = False


'''
Troubleshoot Motor
If mosfet is functional motor will pulse
'''
def TestMotor():
    motor.value = True
    time.sleep(1)
    motor.value = False
    time.sleep(1)


########################### MAIN RUN ###########################
SetAll()

while True:
    if power.value is True:
        power_toggle = power_toggle +1

    if (power_toggle % 2) == 0:
        for i in led_all:
            i = True
            time.sleep(.5)

        GameOriginal()

    else:
        for i in led_all:
            i = False
