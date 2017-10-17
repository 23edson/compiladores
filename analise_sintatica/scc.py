import sys
from collections import defaultdict
from lex import *
from ap import Pilha
slr = defaultdict(list)
dfa_t = defaultdict(list)
#slr[-1] = [['+','*','(',')','id','$'],['E','T','F']]
#slr[0] =  [['','','s4','','s5',''],['1','2','3']]
#slr[1] =  [['s6','','','','','acc'],['','','']]
#slr[2] = [['r2','s7','','r2','','r2'],['','','']]
#slr[3] = [['r4','r4','','r4','','r4'],['','','']]
#slr[4] = [['','','s4','','s5',''],['8','2','3']]
#slr[5] = [['r6','r6','','r6','','r6'],['','','']]
#slr[6] = [['','','s4','','s5',''],['','9','3']]
#slr[7] = [['','','s4','','s5',''],['','','10']]
#slr[8] = [['s6','','','s11','',''],['','','']]
#slr[9] = [['r1','s7','','r1','','r1'],['','','']]
#slr[10] = [['r3','r3','','r3','','r3'],['','','']]
#slr[11] = [['r5','r5','','r5','','r5'],['','','']]

nro_terminals = 0
nro_nonterminals = 0
stage = -1
lalrFlag = 0
rules = []

dfa = {}
la = {}
terminals = {}
nonterminals = {}
def readGOLDParserFile(arq):
	lalrFlag = 0
	slrFlag = 0
	l = open(arq)
	
	while(1):
		
		f = l.readline()
		if(f == ''): break
		elif("Terminals" in f ):
			st = f.strip()
			st = st.split()
			stage = 0
			slr[-1] = [[],[]]
			counter = 0
		elif((("Terminals" in st[0]) and stage==0)and counter < int(st[1])):
			f = f.strip()
			f = f.split()
			slr[-1][0].append(f[1])
			terminals[int(f[0])] = f[1]
			counter = counter + 1
		elif(("Nonterminals") in f ):
			st = f.strip()
			st = st.split()
			stage = 1
			counter	 = 0
			#slr[-1].append(['']*st[1])
		elif((("Nonterminals" in st[0]) and stage==1)and counter < int(st[1])):
			f = f.strip()
			f = f.split()
			slr[-1][1].append(f[1])
			nonterminals[int(f[0])] = f[1]
			counter = counter + 1
		elif("Rules" in f):
			
			st = f.strip()
			st = st.split()
			stage = 2
			counter= 0
		elif((("Rules" in st[0]) and stage==2)and counter < int(st[1])):
			f = f.strip()
			f = f.split()
			
			temp = f[1]
			rules.append([f[0],temp,' '.join(f[3:])])
			
			counter = counter + 1
		elif("DFA" in f):
			st = f.strip()
			st = st.split()
			stage = 3
			counter  =0
			#state = 0
		elif((("DFA" in st[0]) and stage==3)and counter < int(st[2])):
			
			f = f.strip()
			f = f.split()
			if("State" in f):
				state = int(f[1])
				dfa_t[state] = []
				#counter= counter + 1
				#print(state)
				#continue
			#print(f)		
			if("Accept" in f):
				dfa[state] = f[1]
				
			elif("Goto" in f):
				string = f[2] + ":" +f[1]
				#print(string + str(f[1]))
				#print(str(counter))
				dfa_t[state].append(str(string))
			counter = counter + 1
		elif("LALR States" in f):
			
			st = f.strip()
			st = st.split()
			stage = 4
			counter= 0
			
		elif((("LALR" in st[0]) and stage==4)and counter < int(st[2])+1):
			
			f = f.strip()
			f = f.split()
			
			if("State" in f):
				state = int(f[1])
				counter = counter + 1
				lalrFlag = 0
				slrFlag = 0
			if("tb" in f):
				slrFlag = 1
				lalrFlag = 0
				#print("sim")
				continue
			if("la" in f):
				lalrFlag = 1
				slrFlag = 0
				continue
			
			if(lalrFlag == 1):
				#print(f)
				#print(la.keys())
				if(state not in la.keys()):
					la[state] = []
				
				la[state].append([' '.join(f)])
			
			if(slrFlag == 1):
				#state = int(f[1])
				letIn = 0
				if(state not in slr.keys()):
					slr[state] = [['']*len(slr[-1][0]),['']*len(slr[-1][1])]
				if("<" == f[0][1] and len(f[0])==3):
					letIn = 1
				if("<" not in f[0] or letIn == 1):
					indice = slr[-1][0].index(f[0])
					if(len(f)==2):
						slr[state][0][indice] = str(f[1])
					else:slr[state][0][indice] = str(f[1]+f[2])
				else:
					indice = slr[-1][1].index(f[0])
					slr[state][1][indice] = str(f[2])
					
					

			

def getError(source,target):
	indx = [ i[0] for i in enumerate(slr[source][0]) if i[1]!='']
	
	rt = [slr[-1][0][i] for i in indx]
	rt = ' , '.join(rt)
	ft = [i[1][0] for i in enumerate(p.ts) if i[0] < target]
	ft = ' '.join(ft)
	ft = ft + ' >#<'
	
	return rt,ft
def syntaxAnalysis(debug = False):
	
	pilha = Pilha()
	pilha.empilha(["",0])
	
	#prox = p.f[0]
	#p#rox = prox.split(":")
	#pilha.append([ 
	pos = 1
	pos_fita = 0
	while(1):
		if(pos_fita >= len(p.ts)):
			ind = 0
		else:
			prox = p.ts[pos_fita]
			ps = dfa[prox[1]]
			ind = slr[-1][0].index(ps)
		
		
		rs = slr[pilha.topo()[1]][0][ind]
		if(debug):
			print("Pilha: " + str(pilha.dados))
		if("r" in rs):
			reduce = int(rs[1:])
			tam = len(rules[reduce][2].split())
			#pos_fita = pos_fita - tam
			pilha.desempilha(tam)
			
			index_nonterminals = slr[-1][1].index(rules[reduce][1])
			#rule = nonterminals.keys()[nonterminals.values().index(rules[reduce][1])]
			
			next = slr[pilha.topo()[1]][1][index_nonterminals]
			
			pilha.empilha([rules[reduce][1],int(next)])
			#pos_fita = pos_fita + 1
			
		
		elif("s" in rs):
			pilha.empilha([prox[0],int(rs[1:])])
			pos_fita = pos_fita + 1
			pos = pos +1
		elif("a" in rs):
			print("Sintaticamente correto")
			break
		else:
			rt = getError(pilha.topo()[1],pos_fita)
			print("Erro sintatico")
			print("Esperava algum dos tokens:" + str(rt[0]) +" na Linha:" +str(p.ts[pos_fita-1][2]))
			print(" Apos: "+ str(rt[1]))
			
			break
		#if(pilha.tam == 2 and pilha.topo[0]==nonterminals[1] and pos >= len(p.ts)):
		#	print("Sintaticamente correto")
		#	break
readGOLDParserFile("gramatica.txt")
p = lexAlg(dfa_t,dfa)
p.lexicalAnalysis("test.txt")
syntaxAnalysis(True)
#syntaxAnalysis(True)