#!/usr/bin/env python
# -*- coding: utf-8 -*-


class lexAlg:
	def __init__(self,dfa_t,dfa_e):
		self.ts = []
		self.n = None
		self.terminals = None
		#self.n.determinize()
		self.fita = []
		self.readDFA(dfa_t,dfa_e)
		
	def readDFA(self,s,t):
		self.n = s
		self.terminals = t
		
	def getSymbol(self,source,s,token):
		#found = 0
		for i in range(0,len(self.n[s])):
			next = self.n[s][i].split(":")
			if(source in next[0]):
				nextt = int(next[1])
				return nextt,False
		
		return max(self.n.keys())+1,False
	
	
	def lexicalAnalysis(self,source):
		
		counter = 1
		user_info = []
		#self.fita = ""
		arq = open(source,"r")
		while True:
			line = arq.readline()
			if(line == ''): break
			
			line = line.strip()
			line = line.split()
			
			#se a linha nao esta sem texto
			if (line != ''):
			
				for symbol in line:
					s = 0
					error = 0
					for j in symbol:
						next = self.getSymbol(j,s,symbol)
						#se o simbolo nao pertence ao alfabeto
						if(next[0] > max(self.n.keys())):
							#self.ts.append([max(self.n.auto.keys()),symbol,counter])
							#fita = fita + str(max(self.n.auto.keys())) + ":" + str("symbol") + "\n"
							#user_info.append("Erro lexico, " + "Token : " + symbol + ";Linha : " + str(counter))
							if(s > 0):
								error = 1
							break
						else:
							s = next[0]
					
					#se alcancou estado final
					if(s in self.terminals.keys() and error == 0):
							self.ts.append([symbol,s,counter])
					else:
						error =1
						#self.fita.append([ str(symbol),str(s)])
					if(error==1):
						self.ts.append([symbol,max(self.n)+1,counter])
						#self.fita.append([ str(symbol),str(max(self.n.auto.keys())) ])
						user_info.append("Erro lexico, " + "Token : " + symbol + ";Linha : " + str(counter))
					
			
			counter = counter + 1
		
		if(len(user_info) > 0):
			print(user_info)
			return -1
		else: 
			print("Nenhum erro lexico detectado")
			return 0
		
		#tape = open("output.txt","w")
		#tape.write(self.fita)
		#tape.close()
		arq.close()
		
		
		
	#p = lexAlg()
	#p.lexicalAnalysis("test.txt")