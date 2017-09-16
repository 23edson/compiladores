#!/usr/bin/env python
# -*- coding: utf-8 -*-
from detAfnd import *

class lexAlg:
	def __init__(self,tokens):
		self.ts = []
		self.n = determinizeAfnd(tokens)
		self.n.determinize()
		
	def lexicalAnalysis(self,source):
		
		counter = 1
		user_info = []
		fita = ""
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
					for j in symbol:
					
						#se o simbolo nao pertence ao alfabeto
						if ord(j) not in self.n.symbol:
							#self.ts.append([max(self.n.auto.keys()),symbol,counter])
							#fita = fita + str(max(self.n.auto.keys())) + ":" + str("symbol") + "\n"
							#user_info.append("Erro lexico, " + "Token : " + symbol + ";Linha : " + str(counter))
							break
						else:
							pos = self.n.symbol.index(ord(j))
					
							s = self.n.auto[s][pos]
					
					#se alcancou estado final
					if(s in self.n.finalStates):
						self.ts.append([s,symbol,counter])
						fita = fita + str(s) + ":" + str(symbol) + "\n"
					else:
						self.ts.append([max(self.n.auto.keys()),symbol,counter])
						fita = fita + str(max(self.n.auto.keys())) + ":" + str(symbol) + "\n"
						user_info.append("Erro lexico, " + "Token : " + symbol + ";Linha : " + str(counter))
					
			
			counter = counter + 1
		
		if(len(user_info) > 0):
			print(user_info)
		else : print("Nenhum erro lexico detectado")
		
		tape = open("output.txt","w")
		tape.write(fita)
		tape.close()
		arq.close()
		
	#p = lexAlg("tokens.txt")
	#p.lexicalAnalysis("test.txt")