import glob
import os
import time

from display import Display
from PIL import Image


from PIL import BdfFontFile

OUTPUT_DIR = 'images_to_display'
CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
IMAGE_TO_DISPLAY_DIR = '{0}/{1}'.format(CURRENT_DIR_PATH, OUTPUT_DIR)

if __name__ == "__main__":
    while True:
        try:
            image_files = glob.glob('{0}/*.pcx'.format(IMAGE_TO_DISPLAY_DIR))
          
            if len(image_files) > 0:
                display = Display()

                # show warnings
                with Image.open('{0}/logo/alert-full.gif'.format(CURRENT_DIR_PATH)) as alert_image:
                    display.displayGif(alert_image, 0.5, 3)
                    alert_image.close()


                for image in image_files:
                    with Image.open(image) as image_file:
                        display.displayRunningImage(image_file)
                        image_file.close()
                    os.remove(image)
        except Exception as err:
            print('Error caught: {0}'.format(err))

        time.sleep(10)


    # with open('fonts/5x8.bdf','rb') as fp:
    #     p = BdfFontFile.BdfFontFile(fp) 
    #     # won't overwrite, creates new .pil and .pdm files in same dir
    #     p.save('fonts/5x8.bdf')
