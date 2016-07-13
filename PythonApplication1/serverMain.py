# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, session, send_file, send_from_directory, redirect, url_for
from werkzeug.wrappers import BaseRequest, BaseResponse
from urlparse import urlparse
from PIL import Image
import sys, time, io, os
import urllib
import i2sMain

reload(sys)

def uri_validator(x):
	if x.find('myfile:') != -1:
		return True
	try:
		result = urlparse(x)
		if result.scheme!='' and result.netloc!='' and result.path !='': return True
		else: return False
	except:
		return False

UPLOAD_FOLDER ='C:\Users\q\Documents\Visual Studio 2015\Projects\PythonApplication1\PythonApplication1\upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
  
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
	autoRotate = int(request.form['rotate']);
	if lang != 'eng' and lang != 'kor':
		return '현재 지원되는 문자는 [알파벳 : eng / 한글 : kor]입니다.'
	print uri_validator(imgpath)
	if uri_validator(imgpath) == False:
		return '유효하지 않은 URL입니다.'
	imgname = str(time.time())
	res, img = i2sMain.i2sWrapper(imgpath, lang, autoRotate); img.save(imgname+'.jpeg');
	time.sleep(2)
	myimgpath = 'http://143.248.48.228:12345/showimg/';
	print res; return render_template('noteshow.html', resultstr=res.split('\n'), imgpath = myimgpath+imgname+'.jpeg');

@app.route('/showimg/<filename>')
def showimg(filename):
	return send_file(filename,mimetype='image/jpeg')

@app.route('/uploadedimg/<filename>')
def showuploadedimg(filename):
	return send_file(UPLOAD_FOLDER + '\\\\' + filename,mimetype='image/jpeg')

@app.route("/upload", methods=['GET', 'POST'])
def uploadf():
	print request
	if request.method == 'POST':
		file = request.files['file']
		if file:
			filename = file.filename
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return render_template('notescan.html', mypath = 'myfile:'+filename);
	res = """
	<!doctype html>
	<title>Upload new File</title>
	<h1>Upload new File</h1>
	<form action="" method=post enctype=multipart/form-data>
	  <p><input type=file name=file>
		<input type=submit value=Upload>
	</form>
	<p>%s</p>
	""" % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))
	print res
	return res

if __name__ == "__main__":
	if len(sys.argv) == 1:
		myport = 12345
	else:
		myport = int(sys.argv[1])
	print 'asdf'
	app.run(host='0.0.0.0', port=myport)
	
	
	
