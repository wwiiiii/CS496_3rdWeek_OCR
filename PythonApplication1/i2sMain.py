#-*- coding: utf-8 -*-
import sys, os
reload(sys)
sys.setdefaultencoding('utf-8')

from PIL import Image
from StringIO import StringIO
from imgmodulegray import *
from grammar import *
import subprocess, time, Queue, requests
dx = [1,-1,0,0]
dy = [0,0,1,-1]
maxdiff = 115
flag = True
output_file_path = 'C:\Users\q\Documents\Visual Studio 2015\Projects\PythonApplication1\PythonApplication1\\temp'
input_file_name_base = 'imgtemp'
UPLOAD_FOLDER ='C:\Users\q\Documents\Visual Studio 2015\Projects\PythonApplication1\PythonApplication1\upload'
  
def getImageByPath(path):#path is url
    url = path
    print 'opening image by path'
    if path.find('myfile:') != -1:
        url = path[7:];
        i = Image.open(UPLOAD_FOLDER + '\\\\' + url)
    else:
        r = requests.get(url)
        i = Image.open(StringIO(r.content))
    return i


def i2s(img,lang,psm):
    input_file_name = 'C:\Users\q\Desktop\ocrtemp\\' + 'imgtemp' +'.bmp'
    img.save(input_file_name,'bmp')
    if lang == 'kor':command = ['C:\Program Files (x86)\Tesseract-OCR\\tesseract',input_file_name,output_file_path,'-psm', psm, '-l',lang,'onlykor']#4,6,7,8
    elif lang == 'eng':command = ['C:\Program Files (x86)\Tesseract-OCR\\tesseract',input_file_name,output_file_path,'-psm', psm, '-l',lang,'onlyeng']#4,6,7,8
    proc = subprocess.Popen(command,stderr=subprocess.PIPE)
    return proc

def subImage(img,left,right,top,bottom):
    pixel = img.load()
    result = Image.new("RGB",(right-left+10,bottom-top+10),"white")
    res = result.load()
    for i in range(left-3,right+3):
        for j in range(top,bottom+3):
            if isSameTuple(pixel[i,j],(255,255,255)) == False:
                res[i-left+3,j-top] = (0,0,0)
    return result

def ImageToString(img, lang, psm):
    p1 = i2s(img,lang,psm)
    p1.wait(); time.sleep(1);
    f = open(output_file_path+'.txt'); rstr = f.read().strip(); f.close()
    os.remove(output_file_path+'.txt')
    f = open(output_file_path+'.txt','w'); f.close();
    return rstr


def test():
    while True:
        i = input()
        img = Image.open('C:\Users\q\Pictures\\' + 'mysam_' + str(i) + '.jpg')
        img = ImagePreprocessing(img)
        lang = 'eng'
        for j in range(11):
            if lang == 'kor':ans = unicode(ImageToString(img.convert('RGB'), 'kor',str(j)), 'utf-8').replace('<br>',"\n")
            else : ans = ImageToString(img.convert('RGB'), 'eng',str(j)).replace('',"")
            print str(j)+': '+ ans
            if lang == 'kor':print str(j)+': '+correctGrammar(ans)
            print ''

def main():
    hello = unicode('안녕!','utf-8')#.encode('utf-8')#u'안녕!'#
    print hello
    while True:
        #path = raw_input()
        path = 'http://bimage.interpark.com/milti/renewPark/evtboard/20110623131612851.jpg'
        t1 = time.time()
        if len(path) < 2: continue
        img = getImageByPath(path)
        img = ImagePreprocessing(img)
        asdfasdasdf = raw_input()
        """ans = unicode(ImageToString(img.convert('RGB'), 'eng'), 'utf-8')
        print 'time is ' + str(time.time()-t1)
        print 'text is ' + ans"""


def i2sWrapper(imgpath, lang, autoRotate):
    img = getImageByPath(imgpath)#Image.open('C:\Users\q\Pictures\\' + 'mysam_' + str(i) + '.jpg')
    img = ImagePreprocessing(img, autoRotate)
    if lang == 'kor':ans = unicode(ImageToString(img.convert('RGB'), 'kor','6'), 'utf-8').replace('<br>',"\n")
    else : ans = ImageToString(img.convert('RGB'), 'eng','6').replace('',"")
    if lang == 'kor':correctGrammar(ans)
    print ''
    return ans, img
'''
if __name__=='__main__':
    test()#main()
else:
    test()#main()'''
