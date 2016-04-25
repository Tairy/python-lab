import os, sys
import Image


UNIT_SIZE = 72
TARGET_WIDTH = 19 * UNIT_SIZE
HEIGHY = 180
TARGET_HEIGHY = 180 * 11

target = Image.new('RGB', (TARGET_WIDTH, TARGET_HEIGHY))
above = 0
button = HEIGHY

orderimage = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg','10.jpg','11.jpg']
for item in orderimage:
    eachimage = Image.open(item)
    temp = eachimage.resize((TARGET_WIDTH, HEIGHY), Image.ANTIALIAS)
    target.paste(temp, (0, above, TARGET_WIDTH, button))
    above += HEIGHY
    button += HEIGHY
    quality_value = 1000
target.save('all.jpg', quality = quality_value)
print 'done!'