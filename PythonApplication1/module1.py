from PIL import Image, ImageDraw
from scipy import stats
import numpy as np
X = [10,20,30,40,50]
Y = []
a=2; b = 10
for x in X:
    Y.append(a*x+b)
X = np.array(X); Y = np.array(Y)

img = Image.new('RGB',(100,100),"white")
points = []

slope, intercept, r_value, p_value, slope_std_error = stats.linregress(X,Y)
for x in X:
    points.append((x, x*slope+intercept))
ImageDraw.Draw(img).line(points, fill = 128, width = 3)
print slope, intercept

img.show()