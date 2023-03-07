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

#---------- ---------- ---------- ---------- VARIABLES ---------- ---------- ---------- ----------#
# rtc_second_current = datetime.now().second
# rtc_second_prev = rtc_second_current
# rtc_microsecond_current = datetime.now().microsecond
# rtc_microsecond_prev = rtc_microsecond_current
# pythonMaxMicroseconds = 999999 # 980000 is what console is telling me, 999999 is what test gives me

re_clk_current = GPIO.input(re_clk)
re_clk_prev = re_clk_current

re_dt_current = GPIO.input(re_dt)
re_dt_prev = re_dt_current

re_sw_current = GPIO.input(re_sw)
re_sw_prev = re_sw_current

re_counter = 0

# re_debounce_delay = 20000 # delay in seconds * pythonMaxMicroseconds = re_debounceDelay
# re_debounce_prevCall_second = rtc_second_current
# re_debounce_prevCall_microsecond = rtc_microsecond_current
#---------- ---------- ---------- ---------- FUNCTIONS ---------- ---------- ---------- ----------#
#---------- ---------- ---------- ---------- PRELOAD ---------- ---------- ---------- ----------#
#---------- ---------- ---------- ---------- MAIN LOOP ---------- ---------- ---------- ----------#
try:
    while True:
        re_clk_current = GPIO.input(re_clk)
        re_dt_current = GPIO.input(re_dt)
        re_sw_current = GPIO.input(re_sw)
        # print("clk(", re_clk_current, "), clk-1(", re_clk_prev, "), dt(", re_dt_current, ")")
        # print(re_clk_current)
        if re_clk_current != re_clk_prev:
            # print("clk(", re_clk_current, "), clk-1(", re_clk_prev, "), dt(", re_dt_current, ")")
            # print(re_clk_current)
            if re_dt_current != re_clk_current:
                re_counter += 1
            elif re_dt_current == re_clk_current:
                re_counter -= 1
            else:
                print("fuckywucky")
            print(re_counter)
        # sleep(0.01)




















        re_clk_prev = re_clk_current
        re_dt_prev = re_dt_current
        re_sw_prev = re_sw_current
        # rtc_second_current = datetime.now().second
        # rtc_microsecond_current = datetime.now().microsecond
        # # print(rtc_second_current)


        # if rtc_microsecond_current < re_debounce_prevCall_microsecond \
        # or rtc_microsecond_current > re_debounce_prevCall_microsecond + re_debounce_delay \
        # or rtc_second_current > re_debounce_prevCall_second \
        # or rtc_second_current < re_debounce_prevCall_second + 1:
        #     print("thing")



        
            # if re_clk_current == 0 and re_clk_prev == 1:
        #     # print(re_dt_current)
        #     # print("before(", sd_minute, ") after(", end=" ")
        #     # if re_dt_current == 1 and sd_minute < 60:
        #     #     sd_minute += 1
        #     # elif re_dt_current == 0 and sd_minute > 1:
        #     #     sd_minute -= 1
        #     # print(sd_minute, ")")

except:
    print("ERROR")
finally:
    GPIO.cleanup()