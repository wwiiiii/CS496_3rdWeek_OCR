from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time
from scipy import stats
from scipy.spatial import ConvexHull
import math

colstep = 5



def findBoundary(img):#img should be b/w
    '''new = Image.new('RGB',(100,100),"white")
    ImageDraw.Draw(new).line([(0,0),(0,100)], fill = 128, width = 3)
    new.show()'''
    asdf = img.copy()
    width, height = img.size
    newimg = img.copy(); bdpoints = []; asdf = img.copy();
    data = np.asarray(img); data = np.transpose(data, (1,0,2))
    hullX = []; hullY = []
    
    left, X, Y = findLeft(data,width,height); hullX.extend(X); hullY.extend(Y)
    X = np.array(X); Y = np.array(Y);
    slope, intercept, r_value, p_value, slope_std_error = stats.linregress(X,Y)
    ImageDraw.Draw(newimg).line(left, fill = 128 , width = 3)
    print slope, intercept, r_value, p_value, slope_std_error

    right, X, Y = findRight(data,width,height); hullX.extend(X); hullY.extend(Y)
    X = np.array(X); Y = np.array(Y);
    slope, intercept, r_value, p_value, slope_std_error = stats.linregress(X,Y)
    ImageDraw.Draw(newimg).line(right, fill = 0 , width = 3)
    print slope, intercept, r_value, p_value, slope_std_error
    hullPoints = findHull(hullX, hullY)
    print len(left)+len(right) , len(hullPoints)
    ImageDraw.Draw(asdf).line(hullPoints, fill = 128, width = 3)
    #img.show()
    newimg.show()
    asdf.show()


def findLeft(data, width, height):
    left = []; X=[]; Y=[];
    j = 0
    while j < height:
        i = 0
        templist = [data[i][j][0], data[i][j][1], data[i][j][2]]
        while (templist == [255,255,255]): 
            i+=1
            if i == width: break
            templist = [data[i][j][0], data[i][j][1], data[i][j][2]]
        if i < width:
            left.append((i,j)); X.append(i); Y.append(j);
        j += colstep
    return left, X, Y

def findRight(data, width, height):
    right = []; X=[]; Y=[];
    j = 0
    while j < height:
        i = width-1
        templist = [data[i][j][0], data[i][j][1], data[i][j][2]]
        while (templist == [255,255,255]): 
            i-=1
            if i == -1: break
            templist = [data[i][j][0], data[i][j][1], data[i][j][2]]
        if i > -1:
            right.append((i,j)); X.append(i); Y.append(j);
        j += colstep
    return right,X,Y


def findHull(X, Y):
    points = []
    for i in range(len(X)):
        points.append([X[i],Y[i]])
    points = np.array(points)
    hull = ConvexHull(points)
    '''import matplotlib.pyplot as plt
    plt.plot(points[:,0], points[:,1], 'o')
    plt.plot(points[hull.vertices,0], points[hull.vertices,1], 'r--', lw=2)
    plt.plot(points[hull.vertices[0],0], points[hull.vertices[0],1], 'ro')
    plt.show()'''
    res = []
    for i in hull.vertices:
        res.append((points[i][0], points[i][1]))
    res.append(res[0])
    return res
