from machine import Pin, SPI, ADC, PWM, disable_irq, enable_irq

from ssd1306 import SSD1306_SPI
import utime
WIDTH  = 128    # oled display width
HEIGHT = 64     # oled display height
val_ant=0
val_act=0
timer_start_sensor=utime.ticks_us()
rpm=0
promedio=[0,0,0,0,0]
i=0

def conf_sensorRPM():
    sensor=Pin(16,Pin.IN,Pin.PULL_UP) 
    sensor.irq(trigger=Pin.IRQ_FALLING, handler= cuenta)
    return sensor

def cuenta(pin):
    global timer_start_sensor, val_act, val_ant, rpm, promedio, i
    
    val_act=sensor.value()
    if val_ant==1 and val_act==0 :
        #print(str(sensor.value())+"")
        timer_elapsed = utime.ticks_diff(utime.ticks_us(), timer_start_sensor)
        timer_start_sensor=utime.ticks_us()
        rpm_a=(pow(10,6))*60/(timer_elapsed*2)
        promedio[i]=int(rpm_a)
        promedio.sort()
        rpm=promedio[2]
        i+=1
        if i>4 :
            i=0
    val_ant=val_act
    
def conf_display() :
    spi = SPI(0, 100000, mosi=Pin(19), miso=Pin(16), sck=Pin(18))
    rst = Pin(20)
    dc  = Pin(17)
    cs = Pin(0) # not used in the display
    oled = SSD1306_SPI(WIDTH, HEIGHT, spi, dc,rst, cs)  # Init oled display
    return oled

def conf_puls():
    puls=Pin(2,Pin.IN,Pin.PULL_DOWN)
    return puls

def conf_POT():
    POT=ADC(0)
    return POT

def conf_ventilador():
    ventilador=PWM(Pin(27))
    ventilador.freq(25000)
    return ventilador

def conf_LED():
    LED=Pin(25,Pin.OUT)
    return LED

LED=conf_LED()
LED.value(0)
oled = conf_display()
puls=conf_puls()
POT=conf_POT()

sensor=conf_sensorRPM()
ventilador=conf_ventilador()
oled.fill(0)
oled.show()
oled.text("Raspberry Pi", 10,10)
oled.text("Pico", 10,25)
oled.text("EJERCITO", 10, 40)
oled.show()

timer_start = utime.ticks_ms()
LED.value(1)
while(True):
    if(POT.read_u16()>65534):
        pot_lect=65534
    else:
        pot_lect=POT.read_u16()
    ventilador.duty_u16(pot_lect)
    timer_elapsed = utime.ticks_diff(utime.ticks_ms(), timer_start)
    if timer_elapsed >= 0:
        if timer_elapsed >= 1000:
            oled.fill(0)
            oled.text("Raspberry Pi", 10,10)
            oled.text("Pico", 10,25)
            oled.text("EJERCITO", 10, 40)
            oled.text("RPM: " + str(rpm), 10, 55)
            oled.show()
            timer_start = utime.ticks_ms()
    else :
        timer_start=utime.ticks_ms()





