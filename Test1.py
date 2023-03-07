#-------------------------------------------------------------------------------- IMPORT STATEMENTS --------------------------------------------------------------------------------#
from RPi import GPIO
from datetime import datetime





#-------------------------------------------------------------------------------- PINS --------------------------------------------------------------------------------#
GPIO.setmode(GPIO.BCM)

re_clk = 17
re_dt = 18
re_sw = 23
GPIO.setup(re_clk, GPIO.IN)
GPIO.setup(re_dt, GPIO.IN)
GPIO.setup(re_sw, GPIO.IN)

btn_rotary = 24
btn_preset = 25
GPIO.setup(btn_rotary, GPIO.IN)
GPIO.setup(btn_preset, GPIO.IN)

sd_d1 = 12
sd_d2 = 16
sd_d3 = 20
sd_d4 = 21
sd_a = 26
sd_b = 13
sd_c = 9
sd_d = 5
sd_e = 6
sd_f = 19
sd_g = 10
sd_dp = 11
GPIO.setup(sd_d1, GPIO.OUT)
GPIO.setup(sd_d2, GPIO.OUT)
GPIO.setup(sd_d3, GPIO.OUT)
GPIO.setup(sd_d4, GPIO.OUT)
GPIO.setup(sd_a, GPIO.OUT)
GPIO.setup(sd_b, GPIO.OUT)
GPIO.setup(sd_c, GPIO.OUT)
GPIO.setup(sd_d, GPIO.OUT)
GPIO.setup(sd_e, GPIO.OUT)
GPIO.setup(sd_f, GPIO.OUT)
GPIO.setup(sd_g, GPIO.OUT)
GPIO.setup(sd_dp, GPIO.OUT)
GPIO.output(sd_d1, 1), GPIO.output(sd_d2, 1), GPIO.output(sd_d3, 1), GPIO.output(sd_d4, 1)
GPIO.output(sd_a, 0), GPIO.output(sd_b, 0), GPIO.output(sd_c, 0), GPIO.output(sd_d, 0), GPIO.output(sd_e, 0), GPIO.output(sd_f, 0), GPIO.output(sd_g, 0)





#-------------------------------------------------------------------------------- VARIABLES --------------------------------------------------------------------------------#
re_clkPrevious = GPIO.input(re_clk)
re_swPrevious = 0

btn_rotaryCurrent = 0
btn_rotaryPrevious = 0
btn_presetCurrent = 0
btn_presetPrevious = 0

currentDigit = 1

brightness_counter = 50 # change this to whatever you get from DDC/CI
contrast_counter = 50 # change this to whatever you get from DDC/CI


re_debounceDelay = 20000 # time in seconds * pythonMaxMicroseconds = re_debounceDelay


if len(str(brightness_counter)) == 1:   displayString = '0' + str(brightness_counter)
elif len(str(brightness_counter)) == 2: displayString = str(brightness_counter)
if len(str(contrast_counter)) == 1:     displayString += '0' + str(contrast_counter)
elif len(str(contrast_counter)) == 2:   displayString += str(contrast_counter)

second_current = datetime.now().second
second_previous = second_current
microsecond_current = datetime.now().microsecond
microsecond_previous = microsecond_current



re_debounce_prevCall_microsecond = microsecond_current
re_debounce_prevCall_second = second_current # don't listen to inputs that occur too quickly without a mechanical debounce

sd_refreshRate = 200 # change this number as is appropriate (it is in microseconds)
sd_prevCall_microsecond = microsecond_current
sd_prevCall_second = second_current

pythonMaxMicroseconds = 999999 # 980000 is what console is telling me, 999999 is what test gives me


#-------------------------------------------------------------------------------- FUNCTIONS --------------------------------------------------------------------------------#
def sd_displayNum(sd_digit, sd_num):
    if sd_digit == 1:
        GPIO.output(sd_d1, 0), GPIO.output(sd_d2, 1), GPIO.output(sd_d3, 1), GPIO.output(sd_d4, 1)
    elif sd_digit == 2:
        GPIO.output(sd_d1, 1), GPIO.output(sd_d2, 0), GPIO.output(sd_d3, 1), GPIO.output(sd_d4, 1)
    elif sd_digit == 3:
        GPIO.output(sd_d1, 1), GPIO.output(sd_d2, 1), GPIO.output(sd_d3, 0), GPIO.output(sd_d4, 1)
    elif sd_digit == 4:
        GPIO.output(sd_d1, 1), GPIO.output(sd_d2, 1), GPIO.output(sd_d3, 1), GPIO.output(sd_d4, 0)

    if sd_num == 1:
        GPIO.output(sd_a, 0), GPIO.output(sd_b, 1), GPIO.output(sd_c, 1), GPIO.output(sd_d, 0), GPIO.output(sd_e, 0), GPIO.output(sd_f, 0), GPIO.output(sd_g, 0)
    elif sd_num == 2:
        GPIO.output(sd_a, 1), GPIO.output(sd_b, 1), GPIO.output(sd_c, 0), GPIO.output(sd_d, 1), GPIO.output(sd_e, 1), GPIO.output(sd_f, 0), GPIO.output(sd_g, 1)
    elif sd_num == 3:
        GPIO.output(sd_a, 1), GPIO.output(sd_b, 1), GPIO.output(sd_c, 1), GPIO.output(sd_d, 1), GPIO.output(sd_e, 0), GPIO.output(sd_f, 0), GPIO.output(sd_g, 1)
    elif sd_num == 4:
        GPIO.output(sd_a, 0), GPIO.output(sd_b, 1), GPIO.output(sd_c, 1), GPIO.output(sd_d, 0), GPIO.output(sd_e, 0), GPIO.output(sd_f, 1), GPIO.output(sd_g, 1)
    elif sd_num == 5:
        GPIO.output(sd_a, 1), GPIO.output(sd_b, 0), GPIO.output(sd_c, 1), GPIO.output(sd_d, 1), GPIO.output(sd_e, 0), GPIO.output(sd_f, 1), GPIO.output(sd_g, 1)
    elif sd_num == 6:
        GPIO.output(sd_a, 1), GPIO.output(sd_b, 0), GPIO.output(sd_c, 1), GPIO.output(sd_d, 1), GPIO.output(sd_e, 1), GPIO.output(sd_f, 1), GPIO.output(sd_g, 1)
    elif sd_num == 7:
        GPIO.output(sd_a, 1), GPIO.output(sd_b, 1), GPIO.output(sd_c, 1), GPIO.output(sd_d, 0), GPIO.output(sd_e, 0), GPIO.output(sd_f, 0), GPIO.output(sd_g, 0)
    elif sd_num == 8:
        GPIO.output(sd_a, 1), GPIO.output(sd_b, 1), GPIO.output(sd_c, 1), GPIO.output(sd_d, 1), GPIO.output(sd_e, 1), GPIO.output(sd_f, 1), GPIO.output(sd_g, 1)
    elif sd_num == 9:
        GPIO.output(sd_a, 1), GPIO.output(sd_b, 1), GPIO.output(sd_c, 1), GPIO.output(sd_d, 1), GPIO.output(sd_e, 0), GPIO.output(sd_f, 1), GPIO.output(sd_g, 1)
    elif sd_num == 0:
        GPIO.output(sd_a, 1), GPIO.output(sd_b, 1), GPIO.output(sd_c, 1), GPIO.output(sd_d, 1), GPIO.output(sd_e, 1), GPIO.output(sd_f, 1), GPIO.output(sd_g, 0)





#-------------------------------------------------------------------------------- PRELOAD --------------------------------------------------------------------------------#
# testingMicrosecondsMax = 0
# currentlyTesting = True
rotary_changeCounter = 0
preset_changeCounter = 0
#-------------------------------------------------------------------------------- MAIN LOOP --------------------------------------------------------------------------------#
try:
    while True:
        # print(GPIO.input(re_sw))

        second_current = datetime.now().second
        microsecond_current = datetime.now().microsecond

        clkCurrent = GPIO.input(re_clk)
        dtCurrent = GPIO.input(re_dt)

        btn_rotaryCurrent = GPIO.input(btn_rotary)
        btn_presetCurrent = GPIO.input(btn_preset)


        if btn_rotaryCurrent != btn_rotaryPrevious:
            rotary_changeCounter += 1
            print("RTRY#", rotary_changeCounter, " change to", end=": ")
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




        # print("rotary(", btn_rotaryCurrent, "), preset(", btn_rotaryCurrent, ")")
        # the print function occuring so quickly causes the screen to stutter, but placing the print inside a delayed block does not fix the random input values











        # TESTING MICROSECOND MAX
        # if microsecond_current > testingMicrosecondsMax:
        #     testingMicrosecondsMax = microsecond_current
        # elif second_current != second_previous:
        #     print("second: ", second_current, ", maxMicro: ", testingMicrosecondsMax)
        #     testingMicrosecondsMax = 0














        

        
        if microsecond_current < re_debounce_prevCall_microsecond or microsecond_current > re_debounce_prevCall_microsecond + re_debounceDelay or second_current > re_debounce_prevCall_second or second_current < re_debounce_prevCall_second + 1:
            if clkCurrent == 0 and re_clkPrevious == 1:
                # print("working")
                if dtCurrent == 1 and brightness_counter == 99:  brightness_counter =  0
                elif dtCurrent == 1 and brightness_counter < 99: brightness_counter += 1
                elif dtCurrent == 0 and brightness_counter > 0:  brightness_counter -= 1
                elif dtCurrent == 0 and brightness_counter == 0: brightness_counter = 99
                
                rotary_print = "*" * brightness_counter
                rotary_print += str(brightness_counter)
                print(rotary_print)
                # print(microsecond_current)

                if len(str(brightness_counter)) == 1:   displayString =  '0' + str(brightness_counter)
                elif len(str(brightness_counter)) == 2: displayString =  str(brightness_counter)
                if len(str(contrast_counter)) == 1:     displayString += '0' + str(contrast_counter)
                elif len(str(contrast_counter)) == 2:   displayString += str(contrast_counter)

                re_debounce_prevCall_microsecond = microsecond_current
                re_debounce_prevCall_second = second_current
                if re_debounce_prevCall_microsecond + re_debounceDelay > pythonMaxMicroseconds: 
                    re_debounce_prevCall_microsecond = re_debounce_prevCall_microsecond - pythonMaxMicroseconds
                    re_debounce_prevCall_second += 1
                # print (brightness_counter, "(clk[", clkCurrent, "], clk-1[", re_clkPrevious, "], dt[", dtCurrent, "]")

            re_clkPrevious = clkCurrent
        



        sd_displayNum(currentDigit, int(displayString[currentDigit - 1]))
        # if microsecond_current < sd_prevCall_microsecond or microsecond_current > sd_prevCall_microsecond + sd_refreshRate or second_current > sd_prevCall_second or second_current < sd_prevCall_second:
        if microsecond_current < sd_prevCall_microsecond or (microsecond_current > sd_prevCall_microsecond + sd_refreshRate and second_current == sd_prevCall_second) or second_current > sd_prevCall_second or second_current < sd_prevCall_second - 1:
        # That didn't solve it, it just now stutters *off* instead of on
            # print(second_current, ", ", microsecond_current)
            currentDigit += 1
            if currentDigit > 4: currentDigit = 1
            sd_prevCall_microsecond = microsecond_current
            sd_prevCall_second = second_current
            if sd_prevCall_microsecond + re_debounceDelay > pythonMaxMicroseconds:
                sd_prevCall_microsecond = sd_prevCall_microsecond - pythonMaxMicroseconds 
                # there's a stutter every second, meaning when I set the sd_prevCall_microsecond ...
                # ... I am not requiring the secondCurrent to equal sd_prevCall and it triggers early
                sd_prevCall_second += 1






        second_previous = second_current
        microsecond_previous = microsecond_current
        
except:
    print("ERROR")


# Jan 10th(but actually the 9th) 2022. Today I went from not being able to interact with my buttons (they were acting randomly) to getting them to respond to electromagetism of my fingers
# Also, I managed to do it in such a way that didn't cause major stutter on my segment display.
# Additionally, I got rid of the constant flickering of my segment display and replaced it with flickering once a second (still figuring out how to get it to stop)
# Next steps are to: stop EM interference on buttons so it only responds to presses; reduce flickering of segment
# next next steps are to: establish button 'modes' so I can toggle between 'preset' values & set rotary values.
# next next... : Create 'long hold' action for buttons, create segment display animations for that
# next next... : get circuitry to shut up while DDC actions are being performed and resume after
# next next... : set up DDC to recognize monitors, get cables, initialize brightness and contrast values from DDC
# next next... : get DDC to update brightness & get program to run on startup (maybe figure out if you can prevent the pi from projecting to screens to save resources)
# next optional: solder circuitboard, create device case, mount