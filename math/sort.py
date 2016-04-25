import os, sys
import Image
threshold = 140
buttondatum = {}
abovedatum = {}
originimagename = {}
orderimagename = {}
otherimagename ={}
leftdatum= {}
standardimage = {}
  
def isRowAllOne(row):
    for i in range(len(row)):
        if row[i] == 1:
            return 1
        else:
            return 0

def getLeftAge(imagedata, width, height):
    for i in range(width):
        for j in range(height):
            print imagedata[i][j],
        print ''

def getTransverseDatum(image, filename):
    width,height=image.size
    rgb_im = image.convert('RGB')
    sum_l = {}
    for h in range(height):
        n = 0
        for w in range(width):
            r, g, b = rgb_im.getpixel((w, h))
            if r < threshold or g < threshold or b < threshold:
                n+=1
        sum_l[h] = n
    #print sum_l
    above = {}
    button = {}
    key_a = 0
    key_b = 0
    for b in range(len(sum_l)):
        sum_f = 0
        # if b+1 < height and sum_l[b] == 0 and sum_l[b+1] != 0:
        #     for i in  range(15):
        #         if b-i == 0:
        #             break
        #         sum_f+=sum_l[b-i]
        #     if sum_f == 0:
        #         key_a+=1
        #         above[key_a] = b
        if b > 0 and sum_l[b] == 0 and sum_l[b-1] != 0:
            for i in range(15):
                if b+i == height:
                    break
                sum_f+=sum_l[b+i]
            if sum_f == 0:
                #print sum_f
                key_b+=1
                button[key_b] = b
    if len(button) == 1:
        button[2] = button[1]
    buttondatum[filename] = button
    abovedatum[filename] = above

def getVerticalDatum(image, filename):
    width,height=image.size
    rgb_im = image.convert('RGB')
    sum_l = {}
    for w in range(width):
        n = 0
        for h in range(height):
            r, g, b = rgb_im.getpixel((w, h))
            if r < threshold or g < threshold or b < threshold:
                n+=1
        sum_l[w] = n
    #print sum_l
    left = 0
    for l in range(len(sum_l)):
        if sum_l[l] == 0:
            left = l
        else:
            break
    leftdatum[filename] = left

def addStandardImage():
    for l in leftdatum:
        if leftdatum[l] > 11:
            standardimage[l] = l

def compareImage():
    for name in standardimage:
        a=0
        b ={}
       # print buttondatum[name]
        for button in buttondatum:
            if buttondatum[button][1] in range(buttondatum[name][1]-3,buttondatum[name][1]+3):
                a+=1
                b[button] = button
        if a==19:
            orderimagename[name] = b
            otherimagename[name] = name
            for i in b:
                otherimagename[i] = i
    #print orderimagename
    for name in originimagename:
        if name in otherimagename:
            continue
        a=0
        b ={}
       # print buttondatum[name]
        for button in buttondatum:
            if buttondatum[button][2] in range(buttondatum[name][1]-3,buttondatum[name][1]+3):
                a+=1
                b[button] = button
        if a>=18:
            orderimagename[name] = b
            otherimagename[name] = name
            for i in b:
                otherimagename[i] = i
    for name in originimagename:
        if name in otherimagename:
            continue
        a=0
        b ={}
       # print buttondatum[name]
        for button in buttondatum:
            if buttondatum[button][1] in range(buttondatum[name][2]-3,buttondatum[name][2]+3):
                a+=1
                b[button] = button
        if a>=18:
            orderimagename[name] = b
            otherimagename[name] = name
            for i in b:
                otherimagename[i] = i
    # for name in originimagename:
    #     if name in otherimagename:
    #         continue
    #     print name

    #print len(orderimagename)

#def sort_q():
    # b=[0]*len(buttondatum)
    # a = 0
    # for button in buttondatum:
    #     b[a] = buttondatum[button][1]
    #     a+=1
    # print sorted(b)
    #print b
    # for name in originimagename:
    #     if name in otherimagename:
    #         continue
    #     a=0
    #     b = {}
    #     for button in buttondatum:
    #         if buttondatum[button][1] in range(buttondatum[name][1]-2,buttondatum[name][1]+2):
    #             #print button
    #             a+=1
    #             b[button] = button
    #     if a==19:
    #         orderimagename[name] = b
    #         otherimagename[name] = name
    #         for i in b:
    #             otherimagename[i] = i
    #     else:

    # for a_name in originimagename:
    #     if a_name in otherimagename:
    #         continue
    #     a_a = 0
    #     a_b = {}
    #     for above in abovedatum:
    #         #if abovedatum[above][2] in range(abovedatum[a_name][1]-2, abovedatum[a_name][1]+2)
    #         print abovedatum[above][1] 
    #         print abovedatum[a_name][2]
    # #print len(orderimagename)

def loadImage():
    for item in os.listdir('.'):
        if os.path.isfile(item) and item.endswith('.bmp'):
            originimagename[item] = item
    #item = '102.bmp'
            eachimage = Image.open(item)
            getTransverseDatum(eachimage, item)
            getVerticalDatum(eachimage, item)
    addStandardImage()
    compareImage()
    print len(orderimagename)
    #print orderimagename['168.bmp']
    #print len(orderimagename['029.bmp'])
    # print buttondatum['168.bmp']
    # print buttondatum['100.bmp']
    # print abovedatum['170.bmp']
    #print standardimage
    # print standardimage
    
    #sort_q()
    # print buttondatum
    # print abovedatum

if __name__ == '__main__':
    loadImage()