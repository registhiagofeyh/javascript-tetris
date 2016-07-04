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
psID = {} #armazena o último ID do host
gameReady = True
remainingTimeMainSleep = 0

@get('vectorClockId')
def getVectorClock():
	return currentID

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
	global gameMatriz, gameReady, remainingTimeMainSleep
	
	response.content_type = 'application/json'
	return json.dumps({'ready': gameReady, 'remaining':  remainingTimeMainSleep, 'blocks': gameMatriz.prepareToJS(), 'nextpiece': setNextPiece()})


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

	gameReady = False
	currentID += 1

	pieceId = -1
	userID+=1
	posp = -1

	crrMatriz = copy.copy(gameMatriz)
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


@get('/gameMatriz')
def returnMatriz():
	global gameMatriz
	print('Matriz solicitada')
	return json.dumps(gameMatriz.matrizJogada);

@get('/votos')# get peers retorna a quem pedir a lista de votos do server em formato json
def getVotos():
	global votos, currentID, remainingTimeMainSleep
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
	json_data = {'v': json.dumps(lt), 'id': currentID, 't': remainingTimeMainSleep}
	return json_data

@get('/matriz')
@view('matriz')
def printMatrizHTML():
	global gameMatriz
	return {'tabela': gameMatriz.matrizJogada}


def getVotosFrom(host):
	global psID, remainingTimeMainSleep
	link = "http://"+ host + "/votos"
	try:
		#print('Try get from: ' + link)
		r = requests.get(link)
		obj=json.loads(r.text)
		psID[host] = obj['id']
		if obj['t'] < remainingTimeMainSleep:
			remainingTimeMainSleep = obj['t']
		return json.loads(obj['v'])
	except MaxRetryError:
		print ("Conection Error, número maximo de tentativas!")
	except requests.exceptions.ConnectionError:
		print("request.get(" + link + ") error")
	except json.decoder.JSONDecodeError:
		print('Invalid returned value')
	return []

def atualizaTabuleiro(voto):
	global gameMatriz, userID, gameReady, currentID
	global nextPiece, sendedPieces, jogadas, votos
	print("voto\n\n\n")
	print(voto.x)
	print(voto.y)
	print(voto.pos)
	print(voto.piece)

	try:
		gameMatriz.updateMatrix(voto.y, voto.x, voto.pos, voto.piece)
	except IndexError:
		print('Índice inválido, ignora')

	
	gameReady = True



def mainloopV():
	global PS, GlobalVotos, gameMatriz
	while True:
		time.sleep(1)
		for p in PS:
			Vt = getVotosFrom(p)
			for v in Vt:
				cont = 0
				nvotos = 0
				matriz = copy.copy(gameMatriz)
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
				GlobalVotos.add(GroupVoto(gameMatriz, p, voto.x, voto.y, voto.piece, voto.pos), p)


def mainloopE():
	global GlobalVotos, votos, remainingTimeMainSleep
	sleepTime = 30
	remainingTimeMainSleep = sleepTime
	while True:
		if remainingTimeMainSleep:
			time.sleep(1)
			remainingTimeMainSleep -= 1
			continue
		remainingTimeMainSleep = sleepTime
		voto = PosPiece(-1, -1, -1, -1)
		eleito = 0
		for i in GlobalVotos.votos:
			if len(i.playersId) > eleito:
				eleito = len(i.playersId)
				voto = PosPiece(i.voto.x, i.voto.y, i.voto.piece, i.voto.pos)
			elif len(i.playersId) == eleito and (i.voto.x > voto.x or (i.voto.x and voto.x and i.voto.y > voto.y)):
				eleito = len(i.playersId)
				voto = PosPiece(i.voto.x, i.voto.y, i.voto.piece, i.voto.pos)
		if not(voto.x == -1 and voto.y == -1 and voto.piece == -1): 
			atualizaTabuleiro(voto)
			votos = VotosList()
			GlobalVotos = VotosList()



def getIdFrom(host):
	link = "http://"+ host + "/vectorClockId"
	try:
		r = requests.get(link)
		obj=json.loads(r.text)
		return obj
	except MaxRetryError:
		print ("Conection Error, número maximo de tentativas!")
	except requests.exceptions.ConnectionError:
		print("request.get(" + link + ") error")
	except ValueError:
		print('Valor inválido')
	return 0

def getMatrizFrom(host):
	link = "http://"+ host + "/gameMatriz"
	try:
		r = requests.get(link)
		obj=json.loads(r.text)
		return obj
	except MaxRetryError:
		print ("Conection Error, número maximo de tentativas!")
	except requests.exceptions.ConnectionError:
		print("request.get(" + link + ") error")
	return []

def mainloopVector():
	global gameMatriz, currentID, psID
	_p = 0
	while True:
		time.sleep(1)
		print(psID)
		try:
			for p in PS:
				_p = p
				if psID[p] > currentID:
					m = getMatrizFrom(p)
					gameMatriz.cp(m)
		except KeyError:
			psID[_p] = getIdFrom(_p)
	

thGetVotos = Thread(None, mainloopV, (), {}, None)
thGetVotos.start()

theEleicao = Thread(None, mainloopE, (), {}, None)
theEleicao.start()

thVectorClocks = Thread(None, mainloopVector, (), {}, None)
thVectorClocks.start()

port = int(sys.argv[1])
run(host='localhost', port=port, quiet=True)


