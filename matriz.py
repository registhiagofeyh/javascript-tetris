from constants import i, j, l, o, s, t, z, KEY, DIR, speed, nx, ny, nu, pieces
import copy

class Matriz:
	matrizJogada = []

	def __init__(self):
		for ii in range(0, ny):
			linha = []
			for jj in range(0, nx):
				linha.append(-1)
			self.matrizJogada.append(linha)


	def equal(self, m):
		for ii in range(0, ny):
			for jj in range(0, nx):
				if m.matrizJogada[ii][jj] != self.matrizJogada[ii][jj]:
					return False
		return True


	def cp(self, m):
		self.matrizJogada = []

		for ii in range(ny):
			ll = []
			for jj in range(nx):
				ll.append(m.matrizJogada[ii][jj])
			self.matrizJogada.append(ll)



	def getMatriz(self):
		return self.matrizJogada


	def reset(self):
		self.matrizJogada = []
		self.__init__()


	def prepareToJS(self):
		ll = []
	
		for jj in range(nx):
			nl = []
			for ii in range(ny):
				element = None
				mn = self.matrizJogada[ii][jj] 
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
		return ll
	

	def hashIntValue(self):
		somatot = 0
		for ii in range(ny):
			soma = 0
			for jj in range(nx):
				soma += self.matrizJogada[ii][jj]*(jj + 1)
			somatot += soma*(ii + 1)
		return somatot % 7


	def rmLine(self, n):
		for ii in range(n, -1, -1):
			linha = []
			for jj in range(0, nx):
				if ii == 0:
					linha.append(-1)
				else:
					linha.append(self.matrizJogada[ii-1][jj])
			self.matrizJogada[ii] = linha


	def isLineFull(self, ii):
		isFull = 0
		for jj in range(nx):
			if self.matrizJogada[ii][jj]== -1:
				return False
		
		return True


	def existsLineFull(self):
		for ii in range(ny - 1, -1, -1):
			while self.isLineFull(ii):
				self.rmLine(ii)


	def updateMatrix(self, x, y, block, value):
		for ii in range(3, -1, -1):
			a = block % 16
			block = int(block / 16)
			#print (str(a) + " " + str(block))
			if a >= 8:
				self.matrizJogada[y + ii][x] = value
				a = a - 8
			
			if a >= 4:
				self.matrizJogada[y + ii][x + 1] = value
				a = a - 4
				
			if a >=2:
				a = a-2
				self.matrizJogada[y + ii][x + 2] = value
				
			if a >= 1:
				a = a -1
				self.matrizJogada[y + ii][x + 3] = value
		
		self.existsLineFull()
		#for ii in self.matrizJogada:
			#print (ii)
	
	def printMa(self):
		for ii in range(ny):
			print(self.matrizJogada[ii])

	def printMaToStr(self):
		st = ""
		for ii in range(ny):
			st+=str(self.matrizJogada[ii])+"\n"
		return st
			