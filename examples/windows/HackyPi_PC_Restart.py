# This Program of HackyPi makes your PC/Laptop restart  
# Code tested for Windows based PC/Laptop but can be modified for Other OS
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
#tft_bl  = board.GP13
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

tft_bl  = board.GP13
led = digitalio.DigitalInOut(tft_bl)
led.direction = digitalio.Direction.OUTPUT
led.value=True

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

def inner_rectangle():
    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(display.width - BORDER * 2, display.height - BORDER * 2, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = FOREGROUND_COLOR
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER)
    splash.append(inner_sprite)
inner_rectangle()

# Draw a label
text = "Welcome to"
text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
text_group = displayio.Group(scale=FONTSCALE,x=30,y=40,)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)

# Draw a label
text1 = "HackyPi"
text_area1 = label.Label(terminalio.FONT, text=text1, color=TEXT_COLOR)
text_group1 = displayio.Group(scale=FONTSCALE,x=50,y=80,)
text_group1.append(text_area1)  # Subgroup for text scaling
splash.append(text_group1)

try:
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayout(keyboard)
    time.sleep(1)
    keyboard.send(Keycode.WINDOWS, Keycode.R)
    time.sleep(0.3)
    
    keyboard_layout.write('cmd.exe')
    keyboard.send(Keycode.ENTER)
    time.sleep(0.5)
    keyboard.send(Keycode.F11)
    time.sleep(1.2)
    keyboard_layout.write("start shutdown /r") #restart command for PC/Laptop
    keyboard.send(Keycode.ENTER)
    time.sleep(1)    
    inner_rectangle()

    # Draw a label
    text = "Window will"
    text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
    text_group = displayio.Group(scale=FONTSCALE,x=20,y=30,)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)

    # Draw a label
    text1 = "Restart in"
    text_area1 = label.Label(terminalio.FONT, text=text1, color=TEXT_COLOR)
    text_group1 = displayio.Group(scale=FONTSCALE,x=20,y=60,)
    text_group1.append(text_area1)  # Subgroup for text scaling
    splash.append(text_group1)
    
    text2 = "In seconds.."
    text_area2 = label.Label(terminalio.FONT, text=text2, color=TEXT_COLOR)
    text_group2 = displayio.Group(scale=FONTSCALE,x=20,y=90,)
    text_group2.append(text_area2)  # Subgroup for text scaling
    splash.append(text_group2)
    
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


