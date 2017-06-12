from bottle import route, run, template, request
from MyHTMLParser import MyHTMLParser
from operationFile import parserFichier
import json
import requests 
import re


#Nombre de publication  3706767
############################################### Variables globales ############################################################


############################################### Fonctions ############################################################

def creatDictAuth(tab):
    d = dict()
    for i in range(len(tab.author)):
    	if len(tab.author[i]) >0:
    		if tab.author[i][0] not in d.keys() :
    			d[tab.author[i][0]] = list() 
    		for j in range(1,len(tab.author[i])):   		
    			d[tab.author[i][0]].append(tab.author[i][j])
    return d



parser = MyHTMLParser()
parser = parserFichier(parser, 'dblp.xml')	
dict_auth = creatDictAuth(parser)    # dictionnaire auteurs co_auteurs
F = {'author', 'year','journal', 'title', 'co_authors'}


def sortTab(tab):
    d = list()
    for i in range(len(tab)):
    	d.append([tab[i],i])
    d = sorted(d)
    return d

def orderTab(order):
        if order.lower() == "author":

        	newTab = list()
        	for i in range(len(parser.author)):
        		if len(parser.author[i]) > 0 :
        			newTab.append([parser.author[i][0],i])	
        	newTab = sorted(newTab)
        if order.lower() == "year":
        	newTab = sortTab(parser.year)
        if order.lower() == "title":
        	newTab = sortTab(parser.title)
        if order.lower() == "journal":
        	newTab = sortTab(parser.journal)
        return newTab

def elementMsg(l,i):
    res = dict()
    if "author" in l :
    	if len(parser.author[i]) > 0 :
    		res["Author"] = parser.author[i][0]
    	else:
    		res["Author"] = 'Author not specified'
    if "title" in l :
    	res["Title"] = parser.title[i]
    if "year" in l :
    	res["Year"] = parser.year[i]
    if "journal" in l :
    	if len(parser.journal[i]) > 0 :
    		res["Journal"] = parser.journal[i]
    	else:
    		res["Journal"] = 'Journal or Booktitle not specified'
    if "co_authors" in l :
    	res["Co_Authors"] = parser.author[i][1:]


    return res

def checkParams():
    l = list()
    bOrder = False
    a = list()
    b = list()
    try:
    	fields = request.query['fields']
    	for k in range(len(fields.split(','))):
    		p = fields.split(',')[k]
    		if p.lower() in F :
    			l.append(p.lower())
    		else:
        		return json.dumps({'Error':" Fields you entred are not defined !"})
    except:
    	l = list()   

    try:
    	count = int(request.query['count'])
    except ValueError:
        return json.dumps({'Error':" The parameter you foun entred is not defined !"}) 
    except:
    	count = 100

    try:
    	start = int(request.query['start'])
    except ValueError:
        return json.dumps({'Error':" The parameter you foun entred is not defined !"}) 
    except:
    	start = 0

    try:
        order = str(request.query['order'])  
        newTab = orderTab(order)
        for q in range(len(newTab)):
        	a.append(newTab[q][0])
        	b.append(newTab[q][1])

    except ValueError:
        return json.dumps({'Error':" The parameter you foun entred is not defined !"}) 
    except:
    	bOrder = True

    return l, count, start,a,b,bOrder   

def buildExp(s):
    new = ''
    for k in s :
    	if k =='*':
    		new += '.*'
    	elif k =='%':
    		new += '.'
    	else:
    		new += k


    if s[len(s)-1] != '*': #and  s[len(s)-1] != '%':
    	new += '$' 
    return '^'+new

