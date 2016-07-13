from PIL import Image
from distort import *
from bisect import *
import Queue
import time
import numpy as np

black = (255,255,255)
maxdiff = 100/3
path = 'C:\Users\q\Desktop\ocrtemp\\'

def isSame(a,b,mydiff = maxdiff):
    diff = abs(a-b)
    return diff < mydiff

def isSameTuple(p1,p2):
    a,b,c = p1; d,e,f = p2
    return isSame(a,b,c,d,e,f)

def addColor(colorList,a):
    for i in range(len(colorList)):
        a1,cnt1 = colorList[i][0], colorList[i][1]
        if isSame(a,a1):
            colorList[i] = [a1,cnt1+1]
            return
    colorList.append([a,1])

def ft(a):
    return max(0,min(255,a))

GRAD = 5

#[[0,1,0],[1,-4,1],[0,1,0]]

def ImageFilter(img, filter, ratio):
    newimg = Image.new('L', img.size, 255)
    newpx = newimg.load(); imgpx = img.load()
    width, height = img.size
    for i in range(1,width-1):
        for j in range(1,height-1):
            a = 0
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    b = imgpx[i+dx,j+dy]
                    #print dx,dy,rr,gg,bb
                    a += b * filter[dx+1][dy+1];
            #print ft(r), ft(g), ft(b)
            newpx[i,j] = ft(a/ratio)
    return newimg

def Binary(img):
    imgpx = img.load(); width,height = img.size
    newimg = Image.new('L', img.size, 255)
    newpx = newimg.load()
    for i in range(1,width-1):
        for j in range(1, height-1):
            a = imgpx[i,j]
            if a < 150: newpx[i,j] = 0
    return newimg

THRES = 200

def Contrast(img, GRAD):
    imgpx = img.load(); width,height = img.size
    for i in range(1,width-1):
        for j in range(1,height-1):
            a = imgpx[i,j]; a1 = a
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    a2 = imgpx[i+dx,j+dy]
                    if isSame(a,a2): continue
                    if a-a2 >= THRES:
                        imgpx[i+dx,j+dy] = 0
                        a1 = 255
                    elif a2-a>= THRES:
                        imgpx[i+dx,j+dx] = 255
                        a1= 0
            imgpx[i,j]=(ft(a1))
    return img

def ImageRemoveBg(img, at):
    imgpx = img.load();
    width, height = img.size
    chk = [[0 for col in range(height)] for row in range(width)]
    for i in range(1,width-1):
        for j in range(1,height-1):
            a = imgpx[i,j]
            if isSame(a,at):
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        chk[i+dx][j+dy] += 1
    for i in range(1,width-1):
        for j in range(1,height-1):
            if chk[i][j] == 9:
                imgpx[i,j] = 255

bfsdiff = 80


def bfs(img, i, j):
    imgpx = img.load(); q = Queue.Queue()
    width, height = img.size
    q.put([i,j])
    ddx = [1,-1,0,0]; ddy = [0,0,1,-1]
    while not q.empty():
        now = q.get(); 
        a = imgpx[now[0],now[1]];
        while a==255 and not q.empty():
            now = q.get(); a = imgpx[now[0],now[1]];
        if a==255: continue;
        for i in range(4):
            dx = ddx[i]; dy =ddy[i];
            if now[0]+dx <0 or now[0]+dx>=width or now[1]+dy<0 or now[1]+dy>=height: continue
            a1 = imgpx[now[0]+dx, now[1]+dy]
            if isSame(a,a1,bfsdiff):
                q.put([i+dx,j+dy])
        imgpx[now[0], now[1]] = 255

def ImageRemoveBgBfs(img,at):
    imgpx = img.load()
    width, height = img.size
    chk = [[0 for col in range(height)] for row in range(width)]
    for i in range(1,width-1):
        for j in range(1,height-1):
            a = imgpx[i,j]
            if isSame(at,a,bfsdiff):
                t1 = time.time()
                bfs(img,i,j)
                #print 'bfs : ' + str(time.time()-t1)
    return img
    
def ImageRemoveBgMedian(img,colorList):
    imgpx = img.load(); width, height = img.size
    list = [];
    for a,c in colorList:
        list.append(a)
    list.sort()
    if len(list) > 2: threshold = (list[1] + list[2])/2;
    else: threshold = (list[0] + list[1])/2;
    for i in range(width):
        for j in range(height):
            a = imgpx[i,j];
            if a > threshold: imgpx[i,j] = 255
            elif a < threshold: imgpx[i,j]= 0
    return img

def ImageReinforce(img):
    imgpx = img.load();
    width, height = img.size
    chk = [[0 for col in range(height)] for row in range(width)]
    for i in range(1,width-1):
        for j in range(1,height-1):
            a = imgpx[i,j]
            if a == 0:
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        chk[i+dx][j+dy] += 1
    i = 1;
    while i < width-1:
        j = 1;
        while j < height-1:
            if chk[i][j] >= 4:
                imgpx[i,j] = 0
            j+=1
        i+=1

def MedianFilterGray(img):
    newimg = Image.new('L', img.size, 255)
    newpx = newimg.load(); imgpx = img.load()
    width, height = img.size
    for i in range(1,width-1):
        for j in range(1,height-1):
            pixlist = []
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    pixlist.append(imgpx[i+dx,j+dy])
            pixlist.sort()
            newpx[i,j] = pixlist[4]
    return newimg

def ImagePreprocessing2(img):
    print 'now on 2'
    img = img.convert('L')
    imgpx = img.load();
    width, height = img.size
    colorList = []
    t1=time.time()
    for i in range(width):
        for j in range(height):
            a = imgpx[i,j]
            addColor(colorList, a)
    colorList = sorted(colorList, key=lambda arg1:arg1,reverse=True)
    print colorList
    print 'list', time.time() - t1;t1 = time.time()
    # first route : bgmedian => blur => binary => reinforce
    # second route : bgbfs => binary => reinforce
    img = ImageRemoveBgBfs(img, colorList[0][0]); #img.show()
    print 'bgbfs', time.time() - t1;t1 = time.time()
    #img = MedianFilterGray(img); #img.show()
    print 'filter', time.time() - t1;t1 = time.time()
    #img = Contrast(img, 20); img.show()
    print 'contra', time.time() - t1; t1 = time.time()
    #img = Extract(img,0,0,0); img.show()#onlyB filter
    img = Binary(img); #img.show()#B/W filter
    print 'binary', time.time() - t1;t1 = time.time()
    for i in range(0):
        img = MedianFilterGray(img); 
    for i in range(0):
        ImageReinforce(img);
    print 'reinf', time.time() - t1;t1 = time.time()
    #img.show()
    #img = ImageFilter(img, [[0,-2,0],[-2,+11,-2],[0,-2,0]], 3); img.show()#sharpen 1
    #img = ImageFilter(img, [[0,-1,0],[-1,+5,-1],[0,-1,0]], 1); img.show()#sharpen 2
    #findBoundary(img.convert('RGB'))
    return img


def ImagePreprocessing(img, autoRotate):
    if autoRotate==2:
        return ImagePreprocessing2(img)
    img = img.convert('L')
    width, height = img.size; imgpx = img.load()
    #Contrast Stretching
    maxpx = 0; minpx = 255; pixlist = range(width * (height+1)); pixcnt = 0;
    for i in range(width):
        for j in range(height):
            a = imgpx[i,j]
            if maxpx < a: maxpx = a
            if minpx > a: minpx = a
    for i in range(width):
        for j in range(height):
            a = imgpx[i,j]
            a = int((255.0/(maxpx-minpx)) * (a - minpx))
            pixlist[pixcnt] = a; pixcnt += 1;
            imgpx[i,j] = a
    pixlist = pixlist[:pixcnt]; pixlist.sort();
    print pixlist[len(pixlist)-1]
    sumpix = range(len(pixlist)); sumpix[0] = pixlist[0]; 
    for i in range(1,len(pixlist)): sumpix[i] = sumpix[i-1] + pixlist[i];
    prevmean = 0; nowmean = 0; pivot = len(pixlist)/2;
    for i in range(100000):#while True:
        print nowmean
        smallmean = sumpix[pivot] / pivot;
        bigmean = sumpix[len(pixlist)-1] - sumpix[pivot]
        bigmean /= len(pixlist)-1 - pivot
        nowmean = (smallmean + bigmean) / 2.0
        print smallmean, bigmean, nowmean
        if nowmean == prevmean: break
        prevmean = nowmean;
        pivot = bisect_left(pixlist, nowmean)
    #nowmean += 20
    for i in range(width):
        for j in range(height):
            a = imgpx[i,j]
            if a < nowmean: imgpx[i,j] = 0
            else : imgpx[i,j] = 255
    #img.show()
    if autoRotate == 2:
        for i in range(2):
            img = ImageFilter(img, [[1,1,1],[1,1,1],[1,1,1]], 9);# img.show()#blur 1
	#img = MedianFilterGray(img)
    img = Binary(img);# img.show()
    #img = ImageFilter(img, [[0,-2,0],[-2,+11,-2],[0,-2,0]], 3); img.show()#sharpen 1
    '''for i in range(5):
        img = MedianFilterGray(img); 
    img.show()
    for i in range(3):
            ImageReinforce(img);#img.show()
    img.show()'''
    if(autoRotate == 1):
        img = findBoundary(img.convert('RGB')).convert('L');
        img = MedianFilterGray(img);
        img = Binary(img);
    #closing(opening(img)).show()
    #return closing(img)
  #  img.show()
    return img
#http://bimage.interpark.com/milti/renewPark/evtboard/20110623131612851.jpg




def erosion(img):#img should be gray type, and bw
    newimg = img.copy()
    width, height = img.size; imgpx = img.load(); newpx = newimg.load()
    chk = [[0 for col in range(height)] for row in range(width)]
    for i in range(1,width-1):
        for j in range(1,height-1):
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    if imgpx[i+dx, j+dy] == 0:
                        chk[i][j] += 1
            if chk[i][j] == 9: newpx[i, j] = 0
            else: newpx[i,j] = 255
    return newimg

def dilation(img):#img should be gray type, and bw
    newimg = img.copy()
    width, height = img.size; imgpx = img.load(); newpx = newimg.load()
    chk = [[0 for col in range(height)] for row in range(width)]
    for i in range(1,width-1):
        for j in range(1,height-1):
            for dx in [-1,0,1]:
                if chk[i][j] == 1: break
                for dy in [-1,0,1]:
                    if imgpx[i+dx, j+dy] == 0:
                        chk[i][j] = 1
                        break
            if chk[i][j] == 1: newpx[i,j] = 0
            else: newpx[i,j] = 255
    return newimg

def opening(img):
    return dilation(erosion(img))

def closing(img):
    return erosion(dilation(img))