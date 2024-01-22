
# Basic Program to run some networking commands
# Code also display some text on TFT screen
# This code works for Windows based PC/Laptop but can be modified for Other OS
import time
import os
import usb_hid
import digitalio
import board
import busio
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_hid.keyboard import Keyboard, Keycode
from keyboard_layout_win_uk import KeyboardLayout
from adafruit_st7789 import ST7789

# First set some parameters used for shapes and text
BORDER = 12
FONTSCALE = 3
BACKGROUND_COLOR = 0xFF0000  # red
FOREGROUND_COLOR = 0xFFFF00  # Purple
TEXT_COLOR = 0x0000ff

# Release any resources currently in use for the displays
displayio.release_displays()

tft_clk = board.GP10 # must be a SPI CLK
tft_mosi= board.GP11 # must be a SPI TX
tft_rst = board.GP12
tft_dc  = board.GP8
tft_cs  = board.GP9
spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)

# Make the displayio SPI bus and the GC9A01 display
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7789(display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR

#define led (as backlight) pin as output
tft_bl  = board.GP13 #GPIO pin to control backlight LED
led = digitalio.DigitalInOut(tft_bl)
led.direction = digitalio.Direction.OUTPUT
led.value=True

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# This function creates colorful rectangular box 
def inner_rectangle():
    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(display.width - BORDER * 2, display.height - BORDER * 2, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = FOREGROUND_COLOR
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER)
    splash.append(inner_sprite)
    
#Function to print data on TFT
def print_onTFT(text, x_pos, y_pos): 
    text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
    text_group = displayio.Group(scale=FONTSCALE,x=x_pos,y=y_pos,)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)
    
inner_rectangle()
print_onTFT("Welcome to", 30, 40)
print_onTFT("HackyPi", 60, 80)
time.sleep(3)

try:
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayout(keyboard)
    time.sleep(1)
    keyboard.send(Keycode.WINDOWS, Keycode.R)
    time.sleep(0.3)
    
    inner_rectangle()
    FONTSCALE = 2
    print_onTFT("Running", 20, 30)
    print_onTFT("Networking", 20, 60)
    print_onTFT("cmd..", 20, 90)
    
    #open cmd
    keyboard_layout.write('cmd.exe')
    keyboard.send(Keycode.ENTER)
    time.sleep(0.5)
    keyboard.send(Keycode.F11)
    time.sleep(1.2)
    
    #commands are OS specific make sure to provide correct commands
    keyboard_layout.write("for /f "skip=9 tokens=1,2 delims=:" %i in ('netsh wlan show profiles') do @echo %j | findstr -i -v echo | netsh wlan show profiles %j key=clear") 
    keyboard.send(Keycode.ENTER)
    time.sleep(1)
    
    keyboard_layout.write("tracert www.google.com") 
    keyboard.send(Keycode.ENTER)
    time.sleep(1)
    
    keyboard_layout.write("ping www.facebook.com") 
    keyboard.send(Keycode.ENTER)
    time.sleep(1)
    
    keyboard_layout.write("netstat") # similarly many more...
    keyboard.send(Keycode.ENTER)
    time.sleep(1)
    
    lst = [0.5,0.2,0,0.1,0.01]
    for i in range(len(lst)):
        for j in range(10):
            led.value = True
            time.sleep(lst[i])
            led.value = False
            time.sleep(lst[i])

    led.value = True
    keyboard.release_all()
    
except Exception as ex:
    keyboard.release_all()
    raise ex
