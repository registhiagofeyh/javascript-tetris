from bottle import run, get, post, view, request, redirect, route, static_file
import sys
import threading
import json

@get('/')
@view('index')
def index():
	return {}


@route('/static/<path:path>')
def send_static(path):
	return static_file(path, root='static')


run(host='localhost', port=8000)