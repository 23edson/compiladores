#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' 
PROJETO I : Análise léxica.

Aluno: Edson Lemes da Silva;
Disciplina: Compiladores;
Professor: Braulio Adriano de Mello;

A Classe lexAlg define os atributos e métodos utilizados para
execução da análise léxica de um código-fonte. A verificação
acontece a partir da construção do autômato finito com a implementação 
executada na disciplina de LFA.

'''

from detAfnd import *

class lexAlg:

	#Construtor para as estruturas necessarias
	def __init__(self,tokens):
		self.ts = [] #Tabela de simbolos
		self.n = determinizeAfnd(tokens)
		self.n.determinize() #Automato finito
		self.fita = []
	
	def lexicalAnalysis(self,source):
		
		counter = 1
		
		#Lista com os possiveis erros lexicos
		user_info = []
		#self.fita = ""
		arq = open(source,"r")
		while True:
			line = arq.readline()
			if(line == ''): break
			
			#Separador de tokens: espaço em branco
			line = line.strip()
			line = line.split()
			
			#se a linha nao esta sem texto
			if (line != ''):
				#Verificado token a token
				for symbol in line:
					s = 0
					error = 0
					#Verifica simbolo a simbolo
					for j in symbol:
					
						#se o simbolo nao pertence ao alfabeto
						if ord(j) not in self.n.symbol:
							#self.ts.append([max(self.n.auto.keys()),symbol,counter])
							#fita = fita + str(max(self.n.auto.keys())) + ":" + str("symbol") + "\n"
							#user_info.append("Erro lexico, " + "Token : " + symbol + ";Linha : " + str(counter))
							if(s > 0):
								error = 1
							break
						else:
							pos = self.n.symbol.index(ord(j))
					
							s = self.n.auto[s][pos]
					
					#se alcancou estado final
					if(s in self.n.finalStates and error==0):
						self.ts.append([symbol,s,counter])
						#self.fita.append([ str(symbol),str(s)])
					else:
						self.ts.append([symbol,max(self.n.auto.keys()),counter])
						#self.fita.append([ str(symbol),str(max(self.n.auto.keys())) ])
						user_info.append("Erro lexico, " + "Token : " + symbol + ", Linha : " + str(counter))
					
			
			counter = counter + 1
		
		if(len(user_info) > 0):
			print(user_info)
		else : print("Nenhum erro lexico detectado")
		
		arq.close()
		
	#p = lexAlg("temp.txt")
	#p.lexicalAnalysis("test.txt")
