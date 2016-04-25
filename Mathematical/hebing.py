import os, sys
import Image

orderimagename = ['13.bmp','06.bmp','02.bmp','07.bmp','15.bmp','18.bmp','11.bmp','00.bmp','05.bmp','01.bmp','09.bmp','13.bmp','10.bmp','08.bmp','12.bmp','14.bmp','17.bmp','16.bmp','04.bmp']

THRESHORD = 127
UNIT_SIZE = 72
TARGET_WIDTH = 19 * UNIT_SIZE
TARGET_HEIGHY = 180

target = Image.new('RGB', (TARGET_WIDTH, TARGET_HEIGHY))
left = 0
right = UNIT_SIZE
#print orderimagename
for name in orderimagename:
    #print name 
    image = Image.open(name)
    #image.show()
    temp = image.resize((UNIT_SIZE, TARGET_HEIGHY), Image.ANTIALIAS)
    target.paste(temp, (left, 0, right, TARGET_HEIGHY))
    left += UNIT_SIZE
    right += UNIT_SIZE
    quality_value = 1000
target.save('11.jpg', quality = quality_value)
print 'done!'