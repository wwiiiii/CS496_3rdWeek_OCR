# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, session
from werkzeug.wrappers import BaseRequest, BaseResponse
from urlparse import urlparse
import sys, time
import urllib
import i2sMain

reload(sys)

def uri_validator(x):
	try:
		result = urlparse(x)
		if result.scheme!='' and result.netloc!='' and result.path !='': return True
		else: return False
	except:
		return False

app = Flask(__name__)
  
@app.route('/')
def home():
  return render_template('home.html')
  
@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/notescan')
def notescan():
	print 'asdf'
	return render_template('notescan.html')

@app.route('/notecalc',methods = ['POST'])
def notecalc():
	print 'note'
	print request
	if request.method != 'POST':
		return 'Access Denied'
	print request.form
	imgpath = request.form['imgpath']; lang = request.form['lang'];#.encode('utf-8')
	if lang != 'eng' and lang != 'kor':
		return '현재 지원되는 문자는 [알파벳 : eng / 한글 : kor]입니다.'
	print uri_validator(imgpath)
	if uri_validator(imgpath) == False:
		return '유효하지 않은 URL입니다.'
	res = i2sMain.i2sWrapper(imgpath, lang)
	print res
	return res.replace('\n','<br/>')


if __name__ == "__main__":
	if len(sys.argv) == 1:
		myport = 12345
	else:
		myport = int(sys.argv[1])
	print 'asdf'
	app.run(host='0.0.0.0', port=myport)
	
	
	
