# -*- coding: utf-8 -*-

from google.appengine.api import urlfetch
from google.cloud import translate
import json, urllib
from flask import Flask, render_template, request
from collections import deque
from urllib import urlencode

import requests
from requests_toolbelt.adapters import appengine

appengine.monkeypatch()

app = Flask(__name__)
app.debug = True

translate_client = translate.Client()

@app.route('/')

def root():
	return render_template('hello.html')

@app.route('/section3')
def section3():
	pata = request.args.get('a', '') + request.args.get('b', '')
	return render_template('section3.html', pata=pata)

@app.route('/section1')
def section1():
	pata = request.args.get('a', '') + request.args.get('b', '')
	return render_template('section1.html', pata=pata)


@app.route('/section2')
def section2():
	pata = request.args.get('a', '') + request.args.get('b', '')
	return render_template('section2.html', pata=pata)
