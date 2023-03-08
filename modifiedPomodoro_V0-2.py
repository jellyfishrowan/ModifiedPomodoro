# based on version 0.1, making a new file so I can test out changing sd_minute_start to sd_minute_end
# If this test is successful, this will become the new working file.
#---------- ---------- ---------- ---------- MADE BY ROWAN ABRAHAM ---------- ---------- ---------- ----------#
#---------- ---------- ---------- ---------- IMPORT STATEMENTS ---------- ---------- ---------- ----------#
from RPi import GPIO
from datetime import datetime

#---------- ---------- ---------- ---------- PINS ---------- ---------- ---------- ----------#
GPIO.setmode(GPIO.BCM)# GPIO.setmode: BCM = GPIO numbers; BOARD = pin numbers
#| power -------------- 3V3 01|02 5V                      |
#| re_clk ----------- GPIO2 03|04 5V                      |
#| re_dt ------------ GPIO3 05|06 GND                     |
#| re_sw ------------ GPIO4 07|08 GPIO14 -------- rtc_i/o |
#| ground ------------- GND 09|10 GPIO15 -------- rtc_rst |
#| rtc_scl --------- GPIO17 11|12 GPIO18                  |
#|                   GPIO27 13|14 GND                     |
#|                   GPIO22 15|16 GPIO23                  |
#|                      3V3 17|18 GPIO24                  |
#|                   GPIO10 19|20 GND                     |
#|                    GPIO9 21|22 GPIO25                  |
#|                   GPIO11 23|24 GPIO8 ------------ sd_b |
#|                      GND 25|26 GPIO7 ------------ sd_3 |
#| sd_f ------------- GPIO0 27|28 GPIO1 ------------ sd_2 |
#| sd_a ------------- GPIO5 29|30 GND                     |
#| sd_1 ------------- GPIO6 31|32 GPIO12 --------- vm_vcc | * vm_vcc is PWM
#| sd_e ------------ GPIO13 33|34 GND                     |
#| sd_d ------------ GPIO19 35|36 GPIO16 ----------- sd_c |
#| sd_p ------------ GPIO26 37|38 GPIO20 ----------- sd_g |
#|                      GND 39|40 GPIO21 ----------- sd_4 |
#----------------------------------------------------------
# 3.3V |             GND | 
#      | re_vcc          | re_gnd
#      | rtc_vcc         | rtc_gnd
#      |                 | vm_gnd
#----------------------------------------------------------
re_clk = 2;   GPIO.setup(re_clk,  GPIO.IN)
re_dt = 3;    GPIO.setup(re_dt,   GPIO.IN)
re_sw = 4;    GPIO.setup(re_sw,   GPIO.IN)
rtc_scl = 17; GPIO.setup(rtc_scl, GPIO.IN) # serial clock
rtc_io = 14;  GPIO.setup(rtc_io,  GPIO.IN) # serial data
rtc_rst = 15; GPIO.setup(rtc_rst, GPIO.IN) # reset
# for the time being we are not using the RTC ds1302
# for future RTC integration check out (on github)
# DS1302_rtc_raspberrypi4

vm_vcc = 12;  GPIO.setup(vm_vcc,  GPIO.OUT)
sd_1 = 6;     GPIO.setup(sd_1,    GPIO.OUT)
sd_2 = 1;     GPIO.setup(sd_2,    GPIO.OUT)
sd_3 = 7;     GPIO.setup(sd_3,    GPIO.OUT)
sd_4 = 21;    GPIO.setup(sd_4,    GPIO.OUT)
sd_a = 5;     GPIO.setup(sd_a,    GPIO.OUT)
sd_b = 8;     GPIO.setup(sd_b,    GPIO.OUT)
sd_c = 16;    GPIO.setup(sd_c,    GPIO.OUT)
sd_d = 19;    GPIO.setup(sd_d,    GPIO.OUT)
sd_e = 13;    GPIO.setup(sd_e,    GPIO.OUT)
sd_f = 0;     GPIO.setup(sd_f,    GPIO.OUT)
sd_g = 20;    GPIO.setup(sd_g,    GPIO.OUT)
sd_p = 26;    GPIO.setup(sd_p,    GPIO.OUT)

#---------- ---------- ---------- ---------- VARIABLES ---------- ---------- ---------- ----------#
rtc_hour_current = datetime.now().hour
rtc_minute_current = datetime.now().minute
rtc_second_current = datetime.now().second
rtc_second_prev = rtc_second_current
rtc_microsecond_current = datetime.now().microsecond
rtc_microsecond_prev = rtc_microsecond_current
pythonMaxMicroseconds = 999999 # 980000 is what console is telling me, 999999 is what test gives me

re_clk_current = GPIO.input(re_clk)
re_clk_prev = re_clk_current
re_dt_current = GPIO.input(re_dt)
re_sw_current = GPIO.input(re_sw)
re_sw_prev = re_sw_current
re_debounce_delay = 20000 # delay in seconds * pythonMaxMicroseconds = re_debounceDelay
re_debounce_prevCall_minute = rtc_minute_current
re_debounce_prevCall_second = rtc_second_current
re_debounce_prevCall_microsecond = rtc_microsecond_current
sd_mode_timer_changed = False
sd_mode_timer_begin_second = 0
sd_mode_timer_begin_minute = 0

sd_currentDigit = 1
sd_minute_duration = 15
sd_minute_start = rtc_minute_current
sd_second_duration = 0
sd_second_start = rtc_second_current
sd_string = "0100" # this should be the current duration selection, I can figure out a way to define it early
sd_refresh_rate = 200 #microseconds
sd_refresh_prevCall_second = rtc_second_current
sd_refresh_prevCall_microsecond = rtc_microsecond_current
sd_mode_timer_delay = 10


#---------- ---------- ---------- ---------- FUNCTIONS ---------- ---------- ---------- ----------#
def sd_displayNum(sd_digit, sd_num):
    if sd_digit == 1:
        GPIO.output(sd_1, 0), GPIO.output(sd_2, 1), GPIO.output(sd_3, 1), GPIO.output(sd_4, 1), GPIO.output(sd_p, 0)
    elif sd_digit == 2:
        GPIO.output(sd_1, 1), GPIO.output(sd_2, 0), GPIO.output(sd_3, 1), GPIO.output(sd_4, 1), GPIO.output(sd_p, 1)
    elif sd_digit == 3:
        GPIO.output(sd_1, 1), GPIO.output(sd_2, 1), GPIO.output(sd_3, 0), GPIO.output(sd_4, 1), GPIO.output(sd_p, 0)
    elif sd_digit == 4:
        GPIO.output(sd_1, 1), GPIO.output(sd_2, 1), GPIO.output(sd_3, 1), GPIO.output(sd_4, 0), GPIO.output(sd_p, 0)

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



def timeOut(currentMicrosecond, currentSecond, lastCallMS, lastCallS, timeoutDelay):
    if currentMicrosecond < lastCallMS and currentSecond > lastCallS:
        return True
    if currentMicrosecond > lastCallMS + timeoutDelay and currentSecond >= lastCallS:
        return True
    if currentSecond > lastCallS:
        return True
    if currentSecond + 1 < lastCallS:
        return True



def sd_displayString(timer_minute_duration, timer_second_duration, timer_minute_start, timer_second_start, sd_mode_timer_delay):
    print("thing")
    # if re_debounce_prevCall_second:
    if sd_mode_timer_changed == True:
        # print("waiting to set timer")
        if rtc_second_current > re_debounce_prevCall_second + sd_mode_timer_delay \
        or (re_debounce_prevCall_second + sd_mode_timer_delay > 60 and rtc_second_current > re_debounce_prevCall_second + sd_mode_timer_delay - 60 and (rtc_minute_current >= re_debounce_prevCall_minute + 1 or rtc_minute_current < re_debounce_prevCall_minute - 1)):
            # if second > prevCall second + delay
            # or if prevCall second + delay > 60 && second is past new minute time
            # --- and is at least in the same minute, or in the following hour
            # then set the timer
            print("setting timer, initializing countdown")
            sd_mode_timer_changed = False
            sd_minute_start = rtc_minute_current
            sd_second_start = rtc_second_current
            formatString(sd_minute_start, sd_second_start)

        else:
            print("displaying duration selection, countdown not started")
            formatString(sd_minute_duration, sd_second_duration)
    elif sd_mode_timer_changed == False:
        print("timer unchanged, displaying countdown")
        if sd_minute_start + sd_minute_duration > 60:
            print("next hour")
        if sd_second_start + sd_second_duration > 60:
            print("next minute")
        # display countdown
        # hour, minute, second
        # rtc_hour_current
        # rtc_minute_current
        # rtc_second_current
        # sd_minute_start
        # sd_second_start
        # sd_minute_duration
        # sd_second_duration



def formatString(value1, value2):
    # here's where I would save some resources by first checking if the old value is the same as the new value, so I don't need to update it.
    if len(str(value1)) == 1:
        sd_string = '0' + str(value1)
    elif len(str(value1)) == 2:
        sd_string = '0' + str(value1)
    else:
        print("ERROR, 1st display num out of bounds")
        quit()
    
    if len(str(value2)) == 1:
        sd_string += '0' + str(value2)
    elif len(str(value2)) == 2:
        sd_string += '0' + str(value2)
    else:
        print("ERROR, 2nd display num out of bounds")
        quit()
    
#---------- ---------- ---------- ---------- PRELOAD ---------- ---------- ---------- ----------#
#---------- ---------- ---------- ---------- MAIN LOOP ---------- ---------- ---------- ----------#
try:
    while True:
        rtc_second_current = datetime.now().second
        rtc_microsecond_current = datetime.now().microsecond
        # print(rtc_second_current)

        re_clk_current = GPIO.input(re_clk)
        re_dt_current = GPIO.input(re_dt)
        if timeOut(rtc_microsecond_current, rtc_second_current, re_debounce_prevCall_microsecond, re_debounce_prevCall_second, re_debounce_delay):
            if re_clk_current == 0 and re_clk_prev == 1:
                if re_dt_current == 1 and sd_minute_duration < 60:
                    sd_minute_duration += 1
                elif re_dt_current == 0 and sd_minute_duration > 1:
                    sd_minute_duration -= 1
                print(sd_minute_duration)

                if len(str(sd_minute_duration)) == 1:
                    sd_string = '0' + str(sd_minute_duration) + '00'
                else:
                    sd_string = str(sd_minute_duration) + '00'
                
                sd_mode_timer_changed = True
                # if rtc_second_current + sd_mode_timer_delay > 60:
                #     sd_mode_timer_begin_second = sd_mode_timer_begin_second + sd_mode_timer_delay - 60
                #     if rtc_minute_current + 1 > 60:
                #         sd_mode_timer_begin_minute = rtc_minute_current + 1 - 60
                #     else:
                #         sd_mode_timer_begin_minute = rtc_minute_current + 1
                # else:
                #     sd_mode_timer_begin_second = rtc_second_current + sd_mode_timer_delay
                #     sd_mode_timer_begin_minute = rtc_minute_current



                re_debounce_prevCall_microsecond = rtc_microsecond_current
                re_debounce_prevCall_second = rtc_second_current
                re_debounce_prevCall_minute = rtc_minute_current
                if re_debounce_prevCall_microsecond + re_debounce_delay > pythonMaxMicroseconds: 
                    re_debounce_prevCall_microsecond = re_debounce_prevCall_microsecond + re_debounce_delay - pythonMaxMicroseconds
                    re_debounce_prevCall_second += 1
        re_clk_prev = re_clk_current



        sd_displayNum(sd_currentDigit, int(sd_string[sd_currentDigit - 1]))
        if timeOut(rtc_microsecond_current, rtc_second_current, sd_refresh_prevCall_microsecond, sd_refresh_prevCall_second, sd_refresh_rate):
            sd_currentDigit +=1
            if sd_currentDigit > 4: sd_currentDigit = 1

            sd_refresh_prevCall_microsecond = rtc_microsecond_current
            sd_refresh_prevCall_second = rtc_second_current
            if sd_refresh_prevCall_microsecond + sd_refresh_rate > pythonMaxMicroseconds:
                sd_refresh_prevCall_microsecond = sd_refresh_prevCall_microsecond + sd_refresh_rate - pythonMaxMicroseconds
                sd_refresh_prevCall_second += 1

except:
    print("ERROR")
finally:
    GPIO.cleanup()




# todo
# 
# connect displayString() to displayNum() function, 
# have countdown functionality
#
# after 10 seconds, the timer begins and the displays counts down
# when the counter reaches zero the motor vibrates for 10 seconds
# Have countdown as the default state, change it to display the selection when rotary encoder
# if the user rotates the timer back to the orginal number DONT interrupt the timer (prevent slip?)
# 
# 