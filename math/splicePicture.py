import os, sys
import Image
import time

THRESHORD = 127
UNIT_SIZE = 72
TARGET_WIDTH = 19 * UNIT_SIZE
TARGET_HEIGHY = 1980
originimagename = {}
orderimagename = {}
firstrowdata = {}
laserowdate = {}

def getRowInfo(imagename, image, lastrow, wrange):
    width, height = image.size
    rgb_image = image.convert('RGB')
    result = {}
    flag = 0

    for h in range(height):
        for w in range(lastrow-wrange, lastrow):
            r, g, b = rgb_image.getpixel((w, h))
            if r < THRESHORD or g < THRESHORD or b < THRESHORD:
                result[h] = 0
            else:
                result[h] = 1
                flag += 1
            #if first row is blank
            if flag == height and lastrow != width:
                orderimagename[0] = imagename
                del originimagename[imagename]
                continue
            else:
                break

    return result
def getSimilarNum(firstrow, lastrow):
    similarnum = 0
    for num in range(len(firstrow)):
        if firstrow[num] == 0 and lastrow[num] == 0:
            similarnum+=1
    return similarnum
    
def orderData():
    currentnum = 0
    for name in originimagename:
        temp = getSimilarNum(laserowdate[orderimagename[len(orderimagename)-1]], firstrowdata[name])
        if currentnum < temp:
            currentnum = temp
            currentname = name
    orderimagename[len(orderimagename)] = currentname
    del originimagename[currentname]
    if len(originimagename) <= 0:
        return 
    orderData()

def spliceImage():
    target = Image.new('RGB', (TARGET_WIDTH, TARGET_HEIGHY))
    left = 0
    right = UNIT_SIZE
    for name in orderimagename:
       # print orderimagename[name]
        image = Image.open(orderimagename[name])
        temp = image.resize((UNIT_SIZE, TARGET_HEIGHY), Image.ANTIALIAS)
        target.paste(temp, (left, 0, right, TARGET_HEIGHY))
        left += UNIT_SIZE
        right += UNIT_SIZE
    quality_value = 1000
    target.save('header_1.jpg', quality = quality_value)
    print 'done!'

def getOriginData():
    for item in os.listdir('.'):
        if os.path.isfile(item) and item.endswith('.bmp'):
            eachimage = Image.open(item)
            originimagename[item] = item
            firstrowdata[item] = getRowInfo(item, eachimage, 5, 5)
            laserowdate[item] = getRowInfo(item, eachimage, eachimage.size[0], 1)
    orderData()
    spliceImage()

if __name__ == '__main__':
    start = time.clock()
    getOriginData()
    elapsed = (time.clock() - start)
    print("Time used:",elapsed)