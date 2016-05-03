from bottle import run, get, post, view, request, redirect, route, static_file, response
import sys
import threading
import json
from random import randint

# Game constants
i = { 'size': 4, 'blocks': [0x0F00, 0x2222, 0x00F0, 0x4444], 'color': 'cyan'   }
j = { 'size': 3, 'blocks': [0x44C0, 0x8E00, 0x6440, 0x0E20], 'color': 'blue'   }
l = { 'size': 3, 'blocks': [0x4460, 0x0E80, 0xC440, 0x2E00], 'color': 'orange' }
o = { 'size': 2, 'blocks': [0xCC00, 0xCC00, 0xCC00, 0xCC00], 'color': 'yellow' }
s = { 'size': 3, 'blocks': [0x06C0, 0x8C40, 0x6C00, 0x4620], 'color': 'green'  }
t = { 'size': 3, 'blocks': [0x0E40, 0x4C40, 0x4E00, 0x4640], 'color': 'purple' }
z = { 'size': 3, 'blocks': [0x0C60, 0x4C80, 0xC600, 0x2640], 'color': 'red'    }

KEY     = { 'ESC': 27, 'SPACE': 32, 'LEFT': 37, 'UP': 38, 'RIGHT': 39, 'DOWN': 40 }
DIR     = { 'UP': 0, 'RIGHT': 1, 'DOWN': 2, 'LEFT': 3, 'MIN': 0, 'MAX': 3 }
speed   = { 'start': 0.6, 'decrement': 0.005, min: 0.1 } # how long before piece drops by 1 row (seconds)
nx      = 10 # width of tetris court (in blocks)
ny      = 20 # height of tetris court (in blocks)
nu      = 5  # width/height of upcoming preview (in blocks)


currentID = 1
# Seleção aleatória de peças.
pieces = []
sendedPieces = {0: {'y': 0, 'dir': 0, 'x': 7, 'type': o}} # peça 0 sempre é a mesma
jogadas = {}
nextPiece = None # sorteada
matrizJogada = []

@get('/next-piece/')
def randomPiece():
	global response, pieces, nextPiece, currentID, sendedPieces
	response.content_type = 'application/json'

	if (pieces.__len__() == 0):
		pieces = [i,i,i,i,j,j,j,j,l,l,l,l,o,o,o,o,s,s,s,s,t,t,t,t,z,z,z,z];
	type = pieces[randint(0, pieces.__len__()-1)]
	nextPiece = {
		'type': type, 
		'dir': DIR['UP'], 
		'x': randint(0, nx - int (type['size'])), 
		'y': 0,
		'id': currentID
	}
	sendedPieces[currentID] = nextPiece
	currentID = currentID + 1

	return json.dumps(nextPiece)


@get('/matriz')
def printMatriz():
	global matrizJogada
	return {'matrizJogada': matrizJogada}
	
def atualizaMatriz(x, y, block, value):
	global matrizJogada
	print (str(x) + " " + str(y) + " " + str(block))
	#a = block % 16
	#block = block / 16
	
	for i in range(3, 0):
		a = block % 16
		block = block / 16
		
		if a >= 8:
			matrizJogada[x + i][y] = value
			a = a - 8
		
		if a >= 4:
			matrizJogada[x + i][y + 1] = value
			a = a - 4
			
		if a >=2:
			a = a-2
			matrizJogada[x + i][y + 2] = value
			
		if a >= 1:
			a = a -1
			matrizJogada[x + i][y + 3] = value
			
			
@post('/jogada/')
def sendjogada():
	global nextPiece, sendedPieces, jogadas
	global matrizJogada
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
	
	print ("ent")
	if tipo == i:
		if Jdir == 0:
			atualizaMatriz(x, y, 0x0F00, 0)
		elif Jdir == 1:
			atualizaMatriz(x, y, 0x2222, 0)
		elif Jdir == 2:
			atualizaMatriz(x, y, 0x00F0, 0)
		elif Jdir == 3:
			atualizaMatriz(x, y, 0x4444, 0)
	elif tipo == j:
		if Jdir == 0:
			atualizaMatriz(x, y, 0x44C0, 1)
		elif Jdir == 1:
			atualizaMatriz(x, y, 0x8E00, 1)
		elif Jdir == 2:
			atualizaMatriz(x, y, 0x6440, 1)
		elif Jdir == 3:
			atualizaMatriz(x, y, 0x0E20, 1)
	elif tipo == l:
		if Jdir == 0:
			atualizaMatriz(x, y, 0x4460, 2)
		elif Jdir == 1:
			atualizaMatriz(x, y, 0x0E80, 2)
		elif Jdir == 2:
			atualizaMatriz(x, y, 0xC440, 2)
		elif Jdir == 3:
			atualizaMatriz(x, y, 0x2E00, 2)
	elif tipo == o:
		atualizaMatriz(x, y, 0xCC00, 3)
	elif tipo == s:
		if Jdir == 0:
			atualizaMatriz(x, y, 0x06C0, 4)
		elif Jdir == 1:
			atualizaMatriz(x, y, 0x8C40, 4)
		elif Jdir == 2:
			atualizaMatriz(x, y, 0x6C00, 4)
		elif Jdir == 3:
			atualizaMatriz(x, y, 0x4620, 4)
	elif tipo == t:
		if Jdir == 0:
			atualizaMatriz(x, y, 0x0E40, 5)
		elif Jdir == 1:
			atualizaMatriz(x, y, 0x4C40, 5)
		elif Jdir == 2:
			atualizaMatriz(x, y, 0x4E00, 5)
		elif Jdir == 3:
			atualizaMatriz(x, y, 0x4640, 5)
	elif tipo == z:
		if Jdir == 0:
			atualizaMatriz(x, y, 0x0C60, 6)
		elif Jdir == 1:
			atualizaMatriz(x, y, 0x4C80, 6)
		elif Jdir == 2:
			atualizaMatriz(x, y, 0xC600, 6)
		elif Jdir == 3:
			atualizaMatriz(x, y, 0x2640, 6)

@get('/jogada/')
@view('jogada')
def getjogada():
	global jogadas
	return {'jogadas': jogadas}


@post('/reset/')
def resetgame():
	global jogadas
	jogadas = {}


@get('/reset/')
def resetgame():
	global jogadas, currentID, sendedPieces
	sendedPieces.clear()
	sendedPieces = {0: {'y': 0, 'dir': 0, 'x': 7, 'type': o}}
	currentID = 1
	jogadas = {}
	return {}


@get('/')
@view('index')
def index():
	return {}


@route('/static/<path:path>')
def send_static(path):
	return static_file(path, root='static')

for i in range(0, nx):
	linha = []
	for j in range(0, ny):
		linha.append(-1)
	matrizJogada.append(linha)

run(host='localhost', port=8000)
