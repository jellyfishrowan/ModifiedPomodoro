#-------------------------------------------------------------------------------- IMPORT STATEMENTS --------------------------------------------------------------------------------#
from RPi import GPIO
from datetime import datetime





#-------------------------------------------------------------------------------- PINS --------------------------------------------------------------------------------#
GPIO.setmode(GPIO.BCM)

btn_rotary = 24
btn_preset = 25
GPIO.setup(btn_rotary, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btn_preset, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)





#-------------------------------------------------------------------------------- VARIABLES --------------------------------------------------------------------------------#
btn_rotaryCurrent = GPIO.input(btn_rotary)
btn_rotaryPrevious = btn_rotaryCurrent
btn_presetCurrent = GPIO.input(btn_preset)
btn_presetPrevious = btn_presetCurrent

rotary_changeCounter = 0
preset_changeCounter = 0

#-------------------------------------------------------------------------------- FUNCTIONS --------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------- PRELOAD --------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------- MAIN LOOP --------------------------------------------------------------------------------#
try:
    while True:
        btn_rotaryCurrent = GPIO.input(btn_rotary)
        btn_presetCurrent = GPIO.input(btn_preset)






        # print("rotary(", btn_rotaryCurrent, "), preset(", btn_presetCurrent, ")")




        if btn_rotaryCurrent != btn_rotaryPrevious:
            rotary_changeCounter += 1
            print("#", rotary_changeCounter, " change to", end=": ")
            if btn_rotaryCurrent == 1:
                print("ON")
            elif btn_rotaryCurrent == 0:
                print("OFF")
            else:
                print("error")
        if btn_presetCurrent != btn_presetPrevious:
            preset_changeCounter += 1
            print("PRST#", preset_changeCounter, " change to", end=": ")
            if btn_presetCurrent == 1:
                print("ON")
            elif btn_presetCurrent == 0:
                print("OFF")
            else:
                print("error")






        btn_rotaryPrevious = btn_rotaryCurrent
        btn_presetPrevious = btn_presetCurrent
        
        
except:
    print("ERROR")