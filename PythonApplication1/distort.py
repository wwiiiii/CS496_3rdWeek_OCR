from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time
from scipy import stats
from scipy.spatial import ConvexHull
import math

colstep = 5



def findBoundary(img):#img should be b/w
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
    points = []
    for i in range(len(hullX)):
        points.append([hullX[i],hullY[i]])
    points = np.array(points)
    hullPoints = findHull(hullX, hullY)
    asdf = Image.new('RGB', img.size, "white"); ImageDraw.Draw(asdf).line(hullPoints,fill=128,width=10); asdf = asdf.convert('L');# asdf.show()
    #print len(left)+len(right) , len(hullPoints)
    
    #img.show()
    #newimg.show()

    
    ####################Every points to Rectangle###########################
    points = minimum_bounding_rectangle(points); #points.append(points[0])
    rec = []
    for i in points:
        rec.append((int(i[0]),int(i[1])))
    ImageDraw.Draw(asdf).line(rec, fill = 128, width = 3)
    #asdf.show()
    lu = [width, 0]; ru = [0,0]; ld = [0, height]; rd = [0, 0];
    rec.sort()#sorted(rec, key=lambda aaa:aaa[0], reverse=True)
    print rec
    if rec[0][1] < rec[1][1]: lu = rec[0]; ld = rec[1];
    else : lu = rec[1]; ld = rec[0];
    if rec[2][1] < rec[3][1]: ru = rec[2]; rd = rec[3];
    else : ru = rec[3]; rd = rec[2];
    print lu, ld, rd, ru
    lu = [lu[0],lu[1]];ru = [ru[0],ru[1]];ld = [ld[0],ld[1]];rd = [rd[0],rd[1]];
    '''pointdiff = 1
    lu[0] -= pointdiff; lu[1] -= pointdiff; ld[0] -= pointdiff; ld[1] += pointdiff;
    ru[0] += pointdiff; ru[1] -= pointdiff; rd[0] += pointdiff; rd[1] += pointdiff;
    lu = [min(max(0,lu[0]),width) , min((max(0,lu[1])),height)]
    ru = [min(max(0,ru[0]),width) , min((max(0,ru[1])),height)]
    ld = [min(max(0,ld[0]),width) , min((max(0,ld[1])),height)]
    rd = [min(max(0,rd[0]),width) , min((max(0,rd[1])),height)]'''
    newwidth = distance(lu,ru) + distance(ld,rd); newwidth /=2; newwidth = int(newwidth*1.2)
    newheight = distance(lu,ld) + distance(ru,rd); newheight /=2; newheight = int(newheight*1.2)
    margin = min(newwidth/10, newheight/10)# * 2
    return TrapeToRect(img, (newwidth, newheight),[lu,ru,ld,rd],[[margin,margin],[newwidth-margin,margin],[margin,newheight-margin],[newwidth-margin,newheight-margin]])
    #########################################################################


def distance(p1, p2):
    a = (p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1])
    return pow(a, 0.5)

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
    res = []
    for i in hull.vertices:
        res.append((points[i][0], points[i][1]))
    res.append(res[0])
    return res

def TrapeToRect(img,newsize,  pa, pb):
    width, height = img.size
    coeffs = find_coeffs(pa, pb)
    img = img.convert('RGBA')
    fg = img.transform(newsize, Image.PERSPECTIVE, coeffs,
        Image.BICUBIC)
    bg = Image.new('RGBA',newsize,(255,)*4)
    out = Image.composite(fg,bg,fg)
    return out.convert('L')

def find_coeffs(pa, pb):
    t = pb; pb = pa; pa = t;
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = np.matrix(matrix, dtype=np.float)
    B = np.array(pb).reshape(8)

    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)




def minimum_bounding_rectangle(points):
    """
    Find the smallest bounding rectangle for a set of points.
    Returns a set of points representing the corners of the bounding box.

    :param points: an nx2 matrix of coordinates
    :rval: an nx2 matrix of coordinates
    """
    from scipy.ndimage.interpolation import rotate
    pi2 = np.pi/2.

    # get the convex hull for the points
    hull_points = points[ConvexHull(points).vertices]

    # calculate edge angles
    edges = np.zeros((len(hull_points)-1, 2))
    edges = hull_points[1:] - hull_points[:-1]

    angles = np.zeros((len(edges)))
    angles = np.arctan2(edges[:, 1], edges[:, 0])

    angles = np.abs(np.mod(angles, pi2))
    angles = np.unique(angles)

    # find rotation matrices
    # XXX both work
    rotations = np.vstack([
        np.cos(angles),
        np.cos(angles-pi2),
        np.cos(angles+pi2),
        np.cos(angles)]).T
#     rotations = np.vstack([
#         np.cos(angles),
#         -np.sin(angles),
#         np.sin(angles),
#         np.cos(angles)]).T
    rotations = rotations.reshape((-1, 2, 2))

    # apply rotations to the hull
    rot_points = np.dot(rotations, hull_points.T)

    # find the bounding points
    min_x = np.nanmin(rot_points[:, 0], axis=1)
    max_x = np.nanmax(rot_points[:, 0], axis=1)
    min_y = np.nanmin(rot_points[:, 1], axis=1)
    max_y = np.nanmax(rot_points[:, 1], axis=1)

    # find the box with the best area
    areas = (max_x - min_x) * (max_y - min_y)
    best_idx = np.argmin(areas)

    # return the best box
    x1 = max_x[best_idx]
    x2 = min_x[best_idx]
    y1 = max_y[best_idx]
    y2 = min_y[best_idx]
    r = rotations[best_idx]

    rval = np.zeros((4, 2))
    rval[0] = np.dot([x1, y2], r)
    rval[1] = np.dot([x2, y2], r)
    rval[2] = np.dot([x2, y1], r)
    rval[3] = np.dot([x1, y1], r)

    return rval