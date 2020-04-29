import signal
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

import requests
import json
import csv

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Initialize library.
disp.begin()
# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
print(width,height)
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = 0
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 10
# Load default font.
font = ImageFont.load_default()
kaiti = ImageFont.truetype('kaiti.ttf', 12)
def systemSituation():
        # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    ### read some system situation from raspberryPi
    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )
    print(type(Disk))
    
    draw.text((x, top),       'IP: ' + str(IP),  font=font, fill=255)
    draw.text((x, top+8),     str(MemUsage), font=font, fill=255)
    draw.text((x, top+16),    str(CPU) + 'GHz',  font=font, fill=255)
    draw.text((x, top+25),    str(Disk),  font=font, fill=255)
    
    disp.image(image)
    disp.display()
    

def PrintWeather():
    url = 'https://free-api.heweather.net/s6/weather/forecast?location=苏州&key=94ac9a3854e14126898910ff31410db5'
    res = requests.get(url).json() #转换成字典模式
    result = res['HeWeather6'][0]['daily_forecast']
    names = ['城市','时间','天气状况','最高温','最低温','日出','日落']
    print(result)
    count = 0

    for data in result:
        count = count + 1

        cond = data['cond_txt_d']
        humidity = data['hum']
        tmp_max = data['tmp_max']
        tmp_min = data['tmp_min']
        wind_sc = data['wind_sc'] 

        if count == 1:
            weather = cond
            #weather = bytes(weather, encoding = "utf8")
            hum = humidity
            temperature_min = tmp_min
            temperatrue_max = tmp_max
            wind = wind_sc

            
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            # draw.text((x,top), u'测试', font=kaiti, fill=255)
            if '晴' == weather:
                draw.text((x, top),  u'晴', font=kaiti, fill=255)
            draw.text((x, top+8), 'Humidity: ' + str(hum),  font=font, fill=255)
            draw.text((x, top+16), 'Temperature: ' + str(temperature_min) + '~' + str(temperatrue_max),  font=font, fill=255)
            draw.text((x, top+24),  'Wind: ' + str(wind),  font=font, fill=255)
    
    disp.image(image)
    disp.display()


    
def myHandler(signum, frame):

    # systemSituation()
    PrintWeather()
    




signal.signal(signal.SIGALRM, myHandler)
signal.setitimer(signal.ITIMER_REAL,1,2)
while (1):
    pass


    

    
    
    
    

