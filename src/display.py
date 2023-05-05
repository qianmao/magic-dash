import argparse
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from PIL import Image

LED_GPIO_MAPPING = 'adafruit-hat'
LED_ROWS = 32
LED_COLS = 64
LED_CHAIN_LENGTH = 2

SHOW_REFRESH_RATE = False

SLEEP_SEC_PER_FRAME = 0.02
DIRECTION_CHANGE_PAUSE_SEC = 1

class Display(object):
    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument("-r", "--led-rows", action="store", help="Display rows. 16 for 16x32, 32 for 32x32. Default: 32", default=32, type=int)
        self.parser.add_argument("--led-cols", action="store", help="Panel columns. Typically 32 or 64. (Default: 32)", default=32, type=int)
        self.parser.add_argument("-c", "--led-chain", action="store", help="Daisy-chained boards. Default: 1.", default=1, type=int)
        self.parser.add_argument("-P", "--led-parallel", action="store", help="For Plus-models or RPi2: parallel chains. 1..3. Default: 1", default=1, type=int)
        self.parser.add_argument("-p", "--led-pwm-bits", action="store", help="Bits used for PWM. Something between 1..11. Default: 11", default=11, type=int)
        self.parser.add_argument("-b", "--led-brightness", action="store", help="Sets brightness level. Default: 100. Range: 1..100", default=100, type=int)
        self.parser.add_argument("-m", "--led-gpio-mapping", help="Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm" , choices=['regular', 'regular-pi1', 'adafruit-hat', 'adafruit-hat-pwm'], type=str)
        self.parser.add_argument("--led-scan-mode", action="store", help="Progressive or interlaced scan. 0 Progressive, 1 Interlaced (default)", default=1, choices=range(2), type=int)
        self.parser.add_argument("--led-pwm-lsb-nanoseconds", action="store", help="Base time-unit for the on-time in the lowest significant bit in nanoseconds. Default: 130", default=130, type=int)
        self.parser.add_argument("--led-show-refresh", action="store_true", help="Shows the current refresh rate of the LED panel")
        self.parser.add_argument("--led-slowdown-gpio", action="store", help="Slow down writing to GPIO. Range: 0..4. Default: 1", default=1, type=int)
        self.parser.add_argument("--led-no-hardware-pulse", action="store", help="Don't use hardware pin-pulse generation")
        self.parser.add_argument("--led-rgb-sequence", action="store", help="Switch if your matrix has led colors swapped. Default: RGB", default="RGB", type=str)
        self.parser.add_argument("--led-pixel-mapper", action="store", help="Apply pixel mappers. e.g \"Rotate:90\"", default="", type=str)
        self.parser.add_argument("--led-row-addr-type", action="store", help="0 = default; 1=AB-addressed panels; 2=row direct; 3=ABC-addressed panels; 4 = ABC Shift + DE direct", default=0, type=int, choices=[0,1,2,3,4])
        self.parser.add_argument("--led-multiplexing", action="store", help="Multiplexing type: 0=direct; 1=strip; 2=checker; 3=spiral; 4=ZStripe; 5=ZnMirrorZStripe; 6=coreman; 7=Kaler2Scan; 8=ZStripeUneven... (Default: 0)", default=0, type=int)
        self.parser.add_argument("--led-panel-type", action="store", help="Needed to initialize special panels. Supported: 'FM6126A'", default="", type=str)
        self.parser.add_argument("--led-no-drop-privs", dest="drop_privileges", help="Don't drop privileges from 'root' after initializing the hardware.", action='store_false')
        self.parser.set_defaults(drop_privileges=True)

        self.args = self.parser.parse_args()

        options = RGBMatrixOptions()

        options.hardware_mapping = LED_GPIO_MAPPING
        options.rows = LED_ROWS
        options.cols = LED_COLS
        options.chain_length = LED_CHAIN_LENGTH

        options.parallel = self.args.led_parallel
        options.row_address_type = self.args.led_row_addr_type
        options.multiplexing = self.args.led_multiplexing
        options.pwm_bits = self.args.led_pwm_bits
        options.brightness = self.args.led_brightness
        options.pwm_lsb_nanoseconds = self.args.led_pwm_lsb_nanoseconds
        options.led_rgb_sequence = self.args.led_rgb_sequence
        options.pixel_mapper_config = self.args.led_pixel_mapper
        options.panel_type = self.args.led_panel_type


        if SHOW_REFRESH_RATE:
          options.show_refresh_rate = 1

        if self.args.led_slowdown_gpio != None:
            options.gpio_slowdown = self.args.led_slowdown_gpio
        if self.args.led_no_hardware_pulse:
          options.disable_hardware_pulsing = True
        if not self.args.drop_privileges:
          options.drop_privileges=False

        self.matrix = RGBMatrix(options = options)

    
    def displayGif(self, image, frame_seconds, seconds):
       # image = image.resize((self.matrix.width, self.matrix.height))
       # self.matrix.SetImage(image.convert('RGB'))
       
        image.load()
        pics = []

        try:
            while True:
                pics.append(image.copy().convert('RGB'))
                image.seek(len(pics))
        except EOFError:
            pass
        
        self.matrix.Clear()
        count = 0

        while count < seconds:
            for pic in pics:
                self.matrix.SetImage(pic, 0,  0)
                time.sleep(frame_seconds)
                count += frame_seconds

        self.matrix.Clear()

    def displayRunningImage(self, image):
        #image = image.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)

        buffer = self.matrix.CreateFrameCanvas()
        img_width, img_height = image.size

        # Move downward
        for ypos in range(-img_height+1, 1):
            buffer.Clear()
            buffer.SetImage(image, 0, ypos)
            buffer = self.matrix.SwapOnVSync(buffer)
            time.sleep(SLEEP_SEC_PER_FRAME)

        # Pause for a while
        time.sleep(DIRECTION_CHANGE_PAUSE_SEC)

        # Move leftward
        for xpos in range(-1, -img_width, -1):
            buffer.Clear()
            buffer.SetImage(image, xpos)
            buffer = self.matrix.SwapOnVSync(buffer)
            time.sleep(SLEEP_SEC_PER_FRAME)

        # Clear the last frame
        buffer.Clear()
