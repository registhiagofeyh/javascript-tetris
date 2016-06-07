from matriz import Matriz

class PosPiece:
	piece= -1 #piece aqui é um número de 0 até 6, que represta os elementos i, j...
	x = -1
	y = -1
	pos = -1
	def __init__(self, _x, _y, _piece, _pos):
		self.x = _x
		self.y = _y
		self.piece = _piece
		self.pos = _pos
	
	def equal(self, p):
		return self.piece==p.piece and self.x == p.x and self.y == p.y and self.pos == p.pos


class IndVoto:
	'''a classe IndVoto, representa o voto de um único individuo, representado por playerId
	'''
	curVoto = Matriz() #tabuleiro CURrent (atual) para o qual o jogador esta jogando
	playerId = -1 #identificador do jogador
	voto = PosPiece(-1, -1, -1, -1) #identifica o voto propriamente dito, ou seja, o lugar e a peça onde será votado.
	
	def __init__(self, _playerId, _x, _y, _piece, _pos):
		self.curVoto = Matriz()
		self.playerId = _playerId
		self.voto = PosPiece(_x, _y, _piece, _pos)
	

	def equal(self, v):
		return v.voto.equal(self.voto) and self.curVoto.equal(v.curVoto)

class GroupVoto:
	"""	Repreenta o voto de um grupo de pessoas, os ids estão na lista playersId
	"""
	curVoto = Matriz() #tabuleiro CURrent (atual) para o qual o jogador esta jogando
	playersId = []#identificador do jogador
	voto = PosPiece(-1, -1, -1, -1)#identifica o voto propriamente dito, ou seja, o lugar e a peça onde será votado.
	
	def __init__(self, _curVoto, _playersId, _x, _y, _piece, _pos):
		self.curVoto = _curVoto
		self.playersId = []
		self.add(_playersId)
		self.voto = PosPiece(_x, _y, _piece, _pos)

	def equal(self, v):
		return v.voto.equal(self.voto) and self.curVoto.equal(v.curVoto)

	def add(self, _id):
		self.playersId.append(_id)

class VotosList:
	"""Guarda Todos os votos do servidor"""

	votos = []
	def __init__(self):
		self.votos = []
	
	def add(self, v, _playerId):
		for  i in self.votos:
			if i.equal(v):
				i.add(_playerId)
				return

		self.votos.append(v)