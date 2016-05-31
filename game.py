from bottle import run, get, post, view, request, redirect, route, static_file, response
import sys
import threading
import json
import copy
from matriz import Matriz
from random import randint
from constants import i, j, l, o, s, t, z, KEY, DIR, speed, nx, ny, nu, pieces
from voto import PosPiece, IndVoto, GroupVoto, VotosList
from urllib3.exceptions import MaxRetryError

currentID = 1
# Seleção de peças.
sendedPieces = {0: {'y': 0, 'dir': 0, 'x': 7, 'type': o, 'id': 0}} # peça 0 sempre é a mesma
jogadas = {}
nextPiece = None
gameMatriz = Matriz()
votos = VotosList()
GlobalVotos = VotosList()
userID = 0
PS = set(['localhost:8000', 'localhost:8080'])

# Atualmente está gerando um novo ID cada requisição do /matrizToJs, necessário verificar isso
# ainda não sei qual a melhor solução. Talvez verificando se houve um registro da jogada
# desde a última requisição. Seto uma flag e reseto no registro da jogada. Se a flag estiver
# ligada dou a última peça ao invés de gerar uma nova. Olha só, escrevendo encontrei uma solução,
# mas não vou fazer isso agora. flw. vlw.

def setNextPiece():
	global gameMatriz, response, nextPiece, currentID, sendedPieces
	
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
	return nextPiece

@get('/matrizToJs')
def returnMatriz():
	global gameMatriz
	
	response.content_type = 'application/json'

	return json.dumps({'ready': True, 'blocks': gameMatriz.prepareToJS(), 'nextpiece': setNextPiece()})


@post('/jogada/')
def sendjogada():
	global gameMatriz, userID
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

	
	pieceId = -1
	userID+=1
	crrMatriz = Matriz()
	crrMatriz.cp(gameMatriz)

	if tipo == i:
		pieceId = 0
		if Jdir == 0:
			gameMatriz.updateMatrix(x, y, 0x0F00, 0)
		elif Jdir == 1:
			gameMatriz.updateMatrix(x, y, 0x2222, 0)
		elif Jdir == 2:
			gameMatriz.updateMatrix(x, y, 0x00F0, 0)
		elif Jdir == 3:
			gameMatriz.updateMatrix(x, y, 0x4444, 0)
	elif tipo == j:
		pieceId = 1
		if Jdir == 0:
			gameMatriz.updateMatrix(x, y, 0x44C0, 1)
		elif Jdir == 1:
			gameMatriz.updateMatrix(x, y, 0x8E00, 1)
		elif Jdir == 2:
			gameMatriz.updateMatrix(x, y, 0x6440, 1)
		elif Jdir == 3:
			gameMatriz.updateMatrix(x, y, 0x0E20, 1)
	elif tipo == l:
		pieceId = 2
		if Jdir == 0:
			gameMatriz.updateMatrix(x, y, 0x4460, 2)
		elif Jdir == 1:
			gameMatriz.updateMatrix(x, y, 0x0E80, 2)
		elif Jdir == 2:
			gameMatriz.updateMatrix(x, y, 0xC440, 2)
		elif Jdir == 3:
			gameMatriz.updateMatrix(x, y, 0x2E00, 2)
	elif tipo == o:
		pieceId = 3
		gameMatriz.updateMatrix(x, y, 0xCC00, 3)
	elif tipo == s:
		pieceId = 4
		if Jdir == 0:
			gameMatriz.updateMatrix(x, y, 0x06C0, 4)
		elif Jdir == 1:
			gameMatriz.updateMatrix(x, y, 0x8C40, 4)
		elif Jdir == 2:
			gameMatriz.updateMatrix(x, y, 0x6C00, 4)
		elif Jdir == 3:
			gameMatriz.updateMatrix(x, y, 0x4620, 4)
	elif tipo == t:
		pieceId = 5
		if Jdir == 0:
			gameMatriz.updateMatrix(x, y, 0x0E40, 5)
		elif Jdir == 1:
			gameMatriz.updateMatrix(x, y, 0x4C40, 5)
		elif Jdir == 2:
			gameMatriz.updateMatrix(x, y, 0x4E00, 5)
		elif Jdir == 3:
			gameMatriz.updateMatrix(x, y, 0x4640, 5)
	elif tipo == z:
		pieceId = 6
		if Jdir == 0:
			gameMatriz.updateMatrix(x, y, 0x0C60, 6)
		elif Jdir == 1:
			gameMatriz.updateMatrix(x, y, 0x4C80, 6)
		elif Jdir == 2:
			gameMatriz.updateMatrix(x, y, 0xC600, 6)
		elif Jdir == 3:
			gameMatriz.updateMatrix(x, y, 0x2640, 6)

	votos.add(GroupVoto(crrMatriz, userID, x, y, pieceId), userID)

	mainloopV()
'''	for ii in votos.votos:
		print("nv")
		print (ii.curVoto.printMaToStr())
		print(ii.playersId)
		print(str(ii.voto.piece)+" "+str(ii.voto.x)+" "+str(ii.voto.y))
'''
	

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


@get('/votos')# get peers retorna a quem pedir a lista de votos do server em formato json
def getVotos():
	lt = []
	for ii in votos.votos:
		llt = []
		cont = 0

		for jj in ii.playersId:
			cont+=1
		llt.append(cont)
		llt.append(ii.curVoto.matrizJogada)
		llt.append(str(ii.voto.piece)+" "+str(ii.voto.x)+" "+str(ii.voto.y))
		
		lt.append(llt)
	jason_data = json.dumps(lt)
	return jason_data

def getVotosFrom(host):
	link = "http://"+ host + "/votos"
	try:
		r = request.get(link)
		if r.status_code == 200:
			obj=json.loads(r.text)
			return obj
	except MaxRetryError:
		print ("Conection Error, número maximo de tentativas!")
	except request.exceptions.ConnectionError:
		print ("Conection Error!")

	return []

def mainloopV():
	for p in PS:
		Vt = getVotosFrom(p)
		for v in Vt:
			print (v)

run(host='localhost', port=8000)
