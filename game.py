from bottle import run, get, post, view, request, redirect, route, static_file, response
import sys
import threading
import json
import copy
from random import randint
from constants import i, j, l, o, s, t, z, KEY, DIR, speed, nx, ny, nu, pieces

currentID = 1
# Seleção de peças.
sendedPieces = {0: {'y': 0, 'dir': 0, 'x': 7, 'type': o}} # peça 0 sempre é a mesma
jogadas = {}
nextPiece = None
matrizJogada = []


@get('/next-piece/')
def setNextPiece():
	global response, nextPiece, currentID, sendedPieces
	response.content_type = 'application/json'
		
	tipo = pieces[newPice()]
	nextPiece = {
		'type': tipo, 
		'dir': DIR['UP'], 
		'x': 4,
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


@get('/matrizToJs')
def returnMatriz():
	global matrizJogada
	response.content_type = 'application/json'
	ll = []
	
	for jj in range(nx):
		nl = []
		for ii in range(ny):
			element = None
			mn = matrizJogada[ii][jj] 
			if mn == 0:
				element = copy.copy(i)
			elif mn == 1:
				element = copy.copy(j)
			elif mn == 2:
				element = copy.copy(l)
			elif mn == 3:
				element = copy.copy(o)
			elif mn == 4:
				element = copy.copy(s)
			elif mn == 5:
				element = copy.copy(t)
			elif mn == 6:
				element = copy.copy(z)
			if element is not None:
				element['color'] = 'silver'
			nl.append(element)
		ll.append(nl)
	return json.dumps({'ready': True, 'blocks': ll})


def newPice():
	global matrizJogada
	somatot = 0
	for ii in range(ny):
		soma = 0
		for jj in range(nx):
			if matrizJogada[ii][jj] != -1:
				soma += matrizJogada[ii][jj]*(jj + 1)
		somatot = soma*(ii + 1)
	return somatot % 7


def rmLine(n):
	global matrizJogada

	for ii in range(n, -1, -1):
		linha = []
		for jj in range(0, nx):
			if ii == 0:
				linha.append(-1)
			else:
				linha.append(matrizJogada[ii-1][jj])
		matrizJogada[ii] = 	linha


def lineisFull(ii):
	global matrizJogada

	isFull = 0
	for jj in range(nx):
		if matrizJogada[ii][jj]== -1:
			return False
	
	return True
	


def someLineIsFull():
	global matrizJogada
	for ii in range(ny - 1, -1, -1):
		while lineisFull(ii) == True:
			rmLine(ii)
	

def atualizaMatriz(x, y, block, value):
	global matrizJogada
	
	for ii in range(3, -1, -1):
		a = block % 16
		block = int(block / 16)
		print (str(a) + " " + str(block))
		if a >= 8:
			matrizJogada[y + ii][x] = value
			a = a - 8
		
		if a >= 4:
			matrizJogada[y + ii][x + 1] = value
			a = a - 4
			
		if a >=2:
			a = a-2
			matrizJogada[y + ii][x + 2] = value
			
		if a >= 1:
			a = a -1
			matrizJogada[y + ii][x + 3] = value
	
	someLineIsFull()
	for ii in matrizJogada:
		print (ii)

	

@post('/jogada/')
def sendjogada():
	global nextPiece, sendedPieces, jogadas, matrizJogada
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

	print (tipo)
	print (i)
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


for ii in range(0, ny):
	linha = []
	for jj in range(0, nx):
		linha.append(-1)
	matrizJogada.append(linha)

run(host='localhost', port=8000)
