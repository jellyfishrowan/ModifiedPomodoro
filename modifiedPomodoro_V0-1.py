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
re_debounce_prevCall_second = rtc_second_current
re_debounce_prevCall_microsecond = rtc_microsecond_current

sd_currentDigit = 1
sd_minute = 1
sd_second = 0
sd_string = "0000"
sd_refresh_rate = 200 #microseconds
sd_refresh_prevCall_second = rtc_second_current
sd_refresh_prevCall_microsecond = rtc_microsecond_current


#---------- ---------- ---------- ---------- FUNCTIONS ---------- ---------- ---------- ----------#
def sd_displayNum(sd_digit, sd_num):
    if sd_digit == 1:
        GPIO.output(sd_1, 0), GPIO.output(sd_2, 1), GPIO.output(sd_3, 1), GPIO.output(sd_4, 1)
    elif sd_digit == 2:
        GPIO.output(sd_1, 1), GPIO.output(sd_2, 0), GPIO.output(sd_3, 1), GPIO.output(sd_4, 1)
    elif sd_digit == 3:
        GPIO.output(sd_1, 1), GPIO.output(sd_2, 1), GPIO.output(sd_3, 0), GPIO.output(sd_4, 1)
    elif sd_digit == 4:
        GPIO.output(sd_1, 1), GPIO.output(sd_2, 1), GPIO.output(sd_3, 1), GPIO.output(sd_4, 0)

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
#---------- ---------- ---------- ---------- PRELOAD ---------- ---------- ---------- ----------#
#---------- ---------- ---------- ---------- MAIN LOOP ---------- ---------- ---------- ----------#
try:
    while True:
        rtc_second_current = datetime.now().second
        rtc_microsecond_current = datetime.now().microsecond
        # print(rtc_second_current)

        re_clk_current = GPIO.input(re_clk)
        re_dt_current = GPIO.input(re_dt)
        if rtc_microsecond_current < re_debounce_prevCall_microsecond and rtc_second_current > rtc_second_prev \
        or rtc_microsecond_current > re_debounce_prevCall_microsecond + re_debounce_delay \
        or rtc_second_current > re_debounce_prevCall_second \
        or rtc_second_current + 1 < re_debounce_prevCall_second: # 
            if re_clk_current == 0 and re_clk_prev == 1:
                if re_dt_current == 1 and sd_minute < 60:
                    sd_minute += 1
                elif re_dt_current == 0 and sd_minute > 1:
                    sd_minute -= 1
                print(sd_minute)

                if len(str(sd_minute)) == 1:
                    sd_string = '0' + str(sd_minute) + '00'
                else:
                    sd_string = str(sd_minute) + '00'

                re_debounce_prevCall_microsecond = rtc_microsecond_current
                re_debounce_prevCall_second = rtc_second_current
                if re_debounce_prevCall_microsecond + re_debounce_delay > pythonMaxMicroseconds: 
                    re_debounce_prevCall_microsecond = re_debounce_prevCall_microsecond + re_debounce_delay - pythonMaxMicroseconds # this results in negative number i think
                    re_debounce_prevCall_second += 1
        re_clk_prev = re_clk_current



        # print("A")
        sd_displayNum(sd_currentDigit, int(sd_string[sd_currentDigit - 1]))
        # print("B")
        if rtc_microsecond_current < sd_refresh_prevCall_microsecond and rtc_second_current > sd_refresh_prevCall_second \
        or rtc_microsecond_current > sd_refresh_prevCall_microsecond + sd_refresh_rate and rtc_second_current >= sd_refresh_prevCall_second \
        or rtc_second_current > sd_refresh_prevCall_second \
        or rtc_second_current + 1 < sd_refresh_prevCall_second:
            sd_currentDigit +=1
            if sd_currentDigit > 4: sd_currentDigit = 1

            sd_refresh_prevCall_microsecond = rtc_microsecond_current
            sd_refresh_prevCall_second = rtc_second_current
            if sd_refresh_prevCall_microsecond + sd_refresh_rate > pythonMaxMicroseconds:
                sd_refresh_prevCall_microsecond = sd_refresh_prevCall_microsecond + sd_refresh_rate - pythonMaxMicroseconds
                sd_refresh_prevCall_second += 1


        # if microsecond_current < sd_prevCall_microsecond or 
        # (microsecond_current > sd_prevCall_microsecond + sd_refreshRate and second_current == sd_prevCall_second) 
        # or second_current > sd_prevCall_second or 
        # second_current < sd_prevCall_second - 1:




# 25.999999 --- 25.0022 current() 
except:
    print("ERROR")
# finally:
#     GPIO.cleanup()