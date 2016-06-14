from bottle import run, get, post, view, request, redirect, route, static_file, response
import sys
import json
import copy
from threading import Thread
import requests
from matriz import Matriz
from random import randint
from constants import i, j, l, o, s, t, z, KEY, DIR, speed, nx, ny, nu, pieces
from voto import PosPiece, IndVoto, GroupVoto, VotosList
from urllib3.exceptions import MaxRetryError
import time

currentID = 1
# Seleção de peças.
sendedPieces = {0: {'y': 0, 'dir': 0, 'x': 7, 'type': o, 'id': 0}} # peça 0 sempre é a mesma
jogadas = {}
nextPiece = None
gameMatriz = Matriz()
votos = VotosList()
GlobalVotos = VotosList()
userID = 0
PS = set(['localhost:8000', 'localhost:8001', 'localhost:8002'])
gameReady = True

# Atualmente está gerando um novo ID cada requisição do /matrizToJs, necessário verificar isso
# ainda não sei qual a melhor solução. Talvez verificando se houve um registro da jogada
# desde a última requisição. Seto uma flag e reseto no registro da jogada. Se a flag estiver
# ligada dou a última peça ao invés de gerar uma nova. Olha só, escrevendo encontrei uma solução,
# mas não vou fazer isso agora. flw. vlw.

def setNextPiece():
	global gameMatriz, response, nextPiece, currentID, sendedPieces, gameReady
	
	tipo = pieces[gameMatriz.hashIntValue()]
	nextPiece = {
		'type': tipo, 
		'dir': DIR['UP'], 
		'x': 4,
		'y': 0,
		'id': currentID
	}

	sendedPieces[currentID] = nextPiece
	return nextPiece

@get('/matrizToJs')
def returnMatriz():
	global gameMatriz, gameReady
	
	response.content_type = 'application/json'
	print(gameReady)
	return json.dumps({'ready': gameReady, 'blocks': gameMatriz.prepareToJS(), 'nextpiece': setNextPiece()})


@post('/jogada/')
def recievejogada():
	global gameMatriz, userID, gameReady, currentID
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

	print('############')
	print(x)
	print(y)
	print(Jdir)
	print(tipo)
	print('############')

	gameReady = False
	currentID += 1

	pieceId = -1
	userID+=1
	posp = -1

	crrMatriz = Matriz()
	crrMatriz.cp(gameMatriz)

	if tipo == i:
		pieceId = 0
		if Jdir == 0:
			posp =0x0F00
		elif Jdir == 1:
			posp =0x2222
		elif Jdir == 2:
			posp =0x00F0
		elif Jdir == 3:
			posp =0x4444
	elif tipo == j:
		pieceId = 1
		if Jdir == 0:
			posp =0x44C0
		elif Jdir == 1:
			posp =0x8E00
		elif Jdir == 2:
			posp =0x6440
		elif Jdir == 3:
			posp =0x0E20
	elif tipo == l:
		pieceId = 2
		if Jdir == 0:
			posp =0x4460
		elif Jdir == 1:
			posp =0xC440
		elif Jdir == 2:
			posp =0x2E00
		elif Jdir == 3:
			posp =0x2E00
	elif tipo == o:
		pieceId = 3
		posp =0xCC00
	elif tipo == s:
		pieceId = 4
		if Jdir == 0:
			posp =0x06C0
		elif Jdir == 1:
			posp =0x8C40
		elif Jdir == 2:
			posp =0x6C00
		elif Jdir == 3:
			posp =0x4620
	elif tipo == t:
		pieceId = 5
		if Jdir == 0:
			posp =0x0E40
		elif Jdir == 1:
			posp =0x4C40
		elif Jdir == 2:
			posp =0x4E00
		elif Jdir == 3:
			posp =0x4640
	elif tipo == z:
		pieceId = 6
		if Jdir == 0:
			posp =0x0C60
		elif Jdir == 1:
			posp =0x4C80
		elif Jdir == 2:
			posp =0xC600
		elif Jdir == 3:
			posp =0x2640
	#votos = VotosList()
	votos.add(GroupVoto(crrMatriz, userID, x, y, pieceId, posp), userID)
'''
	mainloopV()
	for ii in votos.votos:
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
	global votos
	lt = []
	llt = []
	for ii in votos.votos:
		llt = []
		cont = 0

		for jj in ii.playersId:
			cont+=1
		llt.append(cont)
		llt.append(ii.curVoto.matrizJogada)
		llt.append(str(ii.voto.piece)+" "+str(ii.voto.x)+" "+str(ii.voto.y)+" "+str(ii.voto.pos))
			
		lt.append(llt)
	json_data = json.dumps(lt)
	return json_data

@get('/matriz')
@view('matriz')
def printMatrizHTML():
	global gameMatriz
	return {'tabela': gameMatriz.matrizJogada}


def getVotosFrom(host):
	link = "http://"+ host + "/votos"
	try:
		print('Try get from: ' + link)
		r = requests.get(link)
		print(r)
		obj=json.loads(r.text)
		return obj
	except MaxRetryError:
		print ("Conection Error, número maximo de tentativas!")
	except requests.exceptions.ConnectionError:
		print("request.get(" + link + ") error")

	return []

def atualizaTabuleiro(voto):
	global gameMatriz, userID, gameReady, currentID
	global nextPiece, sendedPieces, jogadas, votos

	print(voto.x)
	print(voto.y)
	print(voto.pos)
	print(voto.piece)

	gameMatriz.updateMatrix(voto.y, voto.x, voto.pos, voto.piece)
	
	gameReady = True
	print('MATRIZMATRIZMATRIZMATRIZMATRIZMATRIZMATRIZ')
	print(gameMatriz.matrizJogada)


def mainloopV():
	global PS, GlobalVotos
	while True:
		time.sleep(1)
		for p in PS:
			Vt = getVotosFrom(p)
			for v in Vt:
			#	print("asasgyasd")
				cont = 0
				nvotos = 0
				matriz = Matriz()
				voto = PosPiece(-1,-1,-1,-1)
				for ii in v:
					if cont == 0:
						nvotos+=ii
					elif cont == 1:
						matriz.matrizJogada = ii
					else:
						ll = ii.split(' ')
						voto = PosPiece(int(str(ll[2])), int(str(ll[1])), int(str(ll[0])), int(str(ll[3])))
					cont+=1
		
				if voto.x == voto.y and voto.piece == voto.x:
					continue
		
				GlobalVotos.add(GroupVoto(matriz, p, voto.x, voto.y, voto.piece, voto.pos), p)


def mainloopE():
	global GlobalVotos
	while True:
		time.sleep(10)
		voto = PosPiece(-1, -1, -1, -1)
		eleito = 0
		for i in GlobalVotos.votos:
			if len(i.playersId) > eleito:
				eleito = len(i.playersId)
				voto = PosPiece(i.voto.x, i.voto.y, i.voto.piece, i.voto.pos)
		atualizaTabuleiro(voto)
		votos = VotosList()
		GlobalVotos = VotosList()


thGetVotos = Thread(None, mainloopV, (), {}, None)
thGetVotos.start()

theEleicao = Thread(None, mainloopE, (), {}, None)
theEleicao.start()

port = int(sys.argv[1])
run(host='localhost', port=port)

