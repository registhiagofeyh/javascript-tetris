from bottle import run, get, post, view, request, redirect, route, static_file, response
import sys
import threading
import json
import copy
from matriz import Matriz
from random import randint
from constants import i, j, l, o, s, t, z, KEY, DIR, speed, nx, ny, nu, pieces

currentID = 1
# Seleção de peças.
sendedPieces = {0: {'y': 0, 'dir': 0, 'x': 7, 'type': o, 'id': 0}} # peça 0 sempre é a mesma
jogadas = {}
nextPiece = None
gameMatriz = Matriz()

@post('/next-piece/')
def setNextPiece():
	global gameMatriz
	global response, nextPiece, currentID, sendedPieces
	response.content_type = 'application/json'
	
	if int(request.forms.get('curID')) <= currentID-2:	
		tipo = pieces[gameMatriz.hashIntValue()]
		nextPiece = {
			'type': tipo, 
			'dir': DIR['UP'], 
			'x': 4,
			'y': 0,
			'id': currentID
		}

		sendedPieces[currentID] = nextPiece
		currentID += 1
	
	return json.dumps(sendedPieces[currentID-1])




@get('/matriz')
def printMatriz():
	global gameMatriz
	return {'matrizJogada': gameMatriz.getMatriz()}


@get('/matrizToJs')
def returnMatriz():
	global gameMatriz
	response.content_type = 'application/json'

	return json.dumps({'ready': True, 'blocks': gameMatriz.prepareToJS()})
	

@post('/jogada/')
def sendjogada():
	global gameMatriz
	global nextPiece, sendedPieces, jogadas
	jogadas[int(request.forms.get('id'))] = {
		'type': sendedPieces[int(request.forms.get('id'))]['type'],
		'dir': int(request.forms.get('dir')),
		'x': int(request.forms.get('x')),
		'y': int(request.forms.get('y')),
	}
	
	index = int(request.forms.get('id'))
	x = jogadas[index]['x']
	y = jogadas[index]['y']
	Jdir = jogadas[index]['dir']
	tipo = jogadas[index]['type']

	if tipo == i:
		if Jdir == 0:
			gameMatriz.updateMatrix(x, y, 0x0F00, 0)
		elif Jdir == 1:
			gameMatriz.updateMatrix(x, y, 0x2222, 0)
		elif Jdir == 2:
			gameMatriz.updateMatrix(x, y, 0x00F0, 0)
		elif Jdir == 3:
			gameMatriz.updateMatrix(x, y, 0x4444, 0)
	elif tipo == j:
		if Jdir == 0:
			gameMatriz.updateMatrix(x, y, 0x44C0, 1)
		elif Jdir == 1:
			gameMatriz.updateMatrix(x, y, 0x8E00, 1)
		elif Jdir == 2:
			gameMatriz.updateMatrix(x, y, 0x6440, 1)
		elif Jdir == 3:
			gameMatriz.updateMatrix(x, y, 0x0E20, 1)
	elif tipo == l:
		if Jdir == 0:
			gameMatriz.updateMatrix(x, y, 0x4460, 2)
		elif Jdir == 1:
			gameMatriz.updateMatrix(x, y, 0x0E80, 2)
		elif Jdir == 2:
			gameMatriz.updateMatrix(x, y, 0xC440, 2)
		elif Jdir == 3:
			gameMatriz.updateMatrix(x, y, 0x2E00, 2)
	elif tipo == o:
		gameMatriz.updateMatrix(x, y, 0xCC00, 3)
	elif tipo == s:
		if Jdir == 0:
			gameMatriz.updateMatrix(x, y, 0x06C0, 4)
		elif Jdir == 1:
			gameMatriz.updateMatrix(x, y, 0x8C40, 4)
		elif Jdir == 2:
			gameMatriz.updateMatrix(x, y, 0x6C00, 4)
		elif Jdir == 3:
			gameMatriz.updateMatrix(x, y, 0x4620, 4)
	elif tipo == t:
		if Jdir == 0:
			gameMatriz.updateMatrix(x, y, 0x0E40, 5)
		elif Jdir == 1:
			gameMatriz.updateMatrix(x, y, 0x4C40, 5)
		elif Jdir == 2:
			gameMatriz.updateMatrix(x, y, 0x4E00, 5)
		elif Jdir == 3:
			gameMatriz.updateMatrix(x, y, 0x4640, 5)
	elif tipo == z:
		if Jdir == 0:
			gameMatriz.updateMatrix(x, y, 0x0C60, 6)
		elif Jdir == 1:
			gameMatriz.updateMatrix(x, y, 0x4C80, 6)
		elif Jdir == 2:
			gameMatriz.updateMatrix(x, y, 0xC600, 6)
		elif Jdir == 3:
			gameMatriz.updateMatrix(x, y, 0x2640, 6)



@get('/jogada/')
@view('jogada')
def getjogada():
	global jogadas
	return {'jogadas': jogadas}


@get('/reset/')
def resetgame():
	global jogadas, currentID, sendedPieces, gameMatriz
	jogadas = {}
	gameMatriz.reset()

	return {}


@get('/')
@view('index')
def index():
	return {}


@route('/static/<path:path>')
def send_static(path):
	return static_file(path, root='static')


run(host='localhost', port=8000)
