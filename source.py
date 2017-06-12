# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 08:54:38 2017

@author: 3525162
"""
from bottle import route, run, template, request
from MyFunctions import *
import json
import requests 
import re
import copy
  
############################################### QUESTION 01 ############################################################
@route('/publications/<id>')  #L'identifiant d'une publication est le numéro de publication
def searchPub(id):

    l, count, start,a,b,bOrder  = checkParams()
    if len(l) == 0:
    	l = {"author", "year","journal", "title", "co_authors"}

    res = list()
    try:
    	a = int(id)
    except:
    	return json.dumps({'Error':"Wrong ID"})
    if a < len(parser.title):
    	res.append(elementMsg(l,a))
    	if len(res)!=0:
    		return "Here is the publication you look after" +json.dumps(res)	
    	else:
    		return json.dumps({'Error': "Publication doesn't exist, ID not Found"})
    else:
    	return json.dumps({'Error': "Publication doesn't exist, ID not Found"})    

############################################### QUESTION 02 ############################################################
@route('/publications')
def publications():
    try:
        limit = int(request.query['limit'])  
    except ValueError:
        return json.dumps({'Error':"Wrong type for limit"}) 
    except:
    	limit = 100
   
    l, count, start,a,b,bOrder = checkParams()
    if len(l) == 0:
    	l = {"author", "year","journal", "title", "co_authors"}

    d = list()
    for j in range(start,min(limit,count) + start) :
    	if not bOrder:
    		i = b[j]
    	else:  
        	i = j     
    	d.append(elementMsg(l,i))  	

    return str(min(count,limit))+ " publications starting from " + str(start)+ " : "+ json.dumps(d)	 

############################################### QUESTION 03 ############################################################

@route('/authors/<name>')
def searchAuthor(name):
    co_author = 0
    nb_publication = 0
    dicPub = dict()
    try:
    	i = list(dict_auth.keys()).index(name)
    except:
        return json.dumps({'Error': 'Author not found !'})
	
    for i in range(len(parser.author)):
    	if len(parser.author[i]) > 0:
    		if parser.author[i][0]== name:
    			co_author += len(parser.author[i]) - 1
    			nb_publication += 1    
    return json.dumps({"Author" : name, "Number of co_authors" : co_author, "Number of publications":nb_publication})


############################################### QUESTION 04 ############################################################

@route('/authors/<name>/publications')

def searchAuthPub(name):
    l, count, start,a,b,bOrder = checkParams()
    if len(l) == 0:
    	l = {"year","journal", "title", "co_authors"}
    d = list()

    try:
    	i = list(dict_auth.keys()).index(name)
    except:
        return json.dumps({'Error': 'Author not found !'})

    j,k = 0,0

    while j < len(parser.author) and k < (start + count):
    	if not bOrder:
    		i = b[j]
    	else:  
        	i = j     
    	if len(parser.author[i]) > 0 :
    		if parser.author[i][0]== name:
    			if k >= start:		
    				d.append(elementMsg(l,i))
    			k +=1
    	j = j+1
    return "List of publications of " +str(name)+" : " + json.dumps(d)
 

############################################### QUESTION 05 ############################################################

@route('/authors/<name>/coauthors')

def searchCoAuthPub(name):
    d = list()
    l, count, start,a,b,bOrder = checkParams()
    if len(l) == 0:
    	l = {"co_authors"}

    try:
    	i = list(dict_auth.keys()).index(name)
    except:
        return json.dumps({'Error': 'Author not found !'})

    j,k = 0,0
    while j < len(parser.author) and k < (start + count):
        if not bOrder:
        	i = b[j]
        else:  
        	i = j   
        if len(parser.author[i]) > 0 : 
        	if parser.author[i][0]== name and len(parser.author[i])>1:        	
        		if k >= start:	
        			d.append(elementMsg(l,i))
        		k +=1
        j = j+1

    return "List of "+str(name)+"'s co_authors :" + json.dumps(d)

############################################### QUESTION 06 ############################################################

@route('/search/authors/<searchString>')
def searchAuthByStr(searchString):
    d = list()
    l, count, start,a,b,bOrder = checkParams()
    if len(l) == 0:
    	l = {"author"}
    try:
    	i = int(searchString)
    	return json.dumps({'Error':"Wrong parameter"}) 
    	    
    except:
    	ss = searchString
    	searchString = buildExp(searchString.lower())

    j,k = 0,0
    while j < len(parser.author) and k < (start + count):
    	if not bOrder:
        	i = b[j]
    	else:  
    		i = j  
    	if len(parser.author[i]) > 0 :	    	
    		if  re.search(searchString,parser.author[i][0].lower()) :	
    			if k >= start:	
    				d.append(elementMsg(l,i))
    			k +=1
    	j = j+1                
    if len(d) > 0 :    
    	return "List of authors containing '"+ss+"' in their names : " +json.dumps(d)
    else :
        return "No author containing '"+ss+"' in his name. "
  

############################################### QUESTION 07 ############################################################

@route('/search/publications/<searchString>')

def searchTitleWithFilter(searchString): 
    d = dict()
    l, count, start,a,b,bOrder = checkParams()

    if len(l) == 0:
    	l = {"author", "year","journal", "title", "co_authors"}
    try:
    	i = int(searchString)
    	return json.dumps({'Error':"Wrong parameter"}) 
    except:
    	ss = searchString
    	searchString = buildExp(searchString.lower())

    if 'filter' in request.query:
        filtre = request.query['filter']    
        for i in filtre.split(','):
            d[i.split(':')[0]] = i.split(':')[1]

    continu = False
    j,kk = 0 , 0   

    numPub = list()
    while j < len(parser.title) and kk < (start + count):
    	if not bOrder:
        	i = b[j]
    	else:  
    		i = j 
   
    	t, continu = False, False
    	if re.search(searchString,parser.title[i].lower()):
    		if len(d.keys()) == 0 :
    			if kk >= start:
    				numPub.append(elementMsg(l,i))
    			kk +=1
    			j +=1
    		if len(d.keys()) == 1 :
    			continu = True
    		for k in d.keys():
    			if k == "author":
    				if len(parser.author[i]) > 0 :
    					if not(d[k].lower() in parser.author[i][0].lower()):
    			    			j +=1
    					elif ((len(d.keys()) - 1) == list(d.keys()).index(k) and d[k].lower() in parser.author[i][0].lower() ) and continu:
    						if kk >= start:
    							numPub.append(elementMsg(l,i))
    						continu = True
    						kk +=1
    						j +=1
    					else:
    						continu = True
    				else:
    			    		j +=1
    			if k == "title":
    				if not(d[k].lower() in parser.title[i].lower()):
    			    		j +=1
    				elif ((len(d.keys()) - 1) == list(d.keys()).index(k) and d[k].lower() in parser.title[i].lower()) and continu :
    					if kk >= start:
    						numPub.append(elementMsg(l,i))
    					continu = True
    					kk +=1
    					j +=1
    				else:
    					continu = True
    			if k == "journal":
    				if not(d[k].lower() in parser.journal[i].lower()):
    			    		j +=1
    				elif ((len(d.keys()) - 1) == list(d.keys()).index(k) and d[k].lower() in parser.journal[i].lower()) and continu:
    					if kk >= start:
    						numPub.append(elementMsg(l,i))
    					continu = True
    					kk +=1
    			
    					j +=1
    				else:
    					continu = True
    			if k == "year":
    				if d[k]!= parser.year[i]:
    					j +=1
    				elif ((len(d.keys()) - 1) == list(d.keys()).index(k) and int(d[k]) == int(parser.year[i])) and continu:
    					if kk >= start:
    						numPub.append(elementMsg(l,i))
    					continu = True
    					kk +=1
    				
    					j +=1
    				else:
    					continu = True
    			if k == "coauthor":
    				for j in range(1,len(parser.author[i])):
    					if (d[k].lower() in parser.author[i][j].lower()):
    						t = True

    				if t == False:
    					j +=1
    				elif ((len(d.keys()) - 1) == list(d.keys()).index(k) and t == True):
    					if kk >= start:
    						numPub.append(elementMsg(l,i))
    					continu = True
    					kk+=1
    					j +=1
    				else:
    					continu = True		
    	else:
    		j +=1  		

    return "List of publications containing '" +ss +"' in their titles : "+json.dumps(numPub)
 
############################################### QUESTION 09 ############################################################

@route('/authors/<name_origine>/distance/<name_destination>')

def collaboration(name_origine,name_destination):
    distance = path (name_origine,name_destination, parser) 
    if distance != "Error":        
        return "Distance between" + name_origine +" and "+name_destination+" : " + json.dumps({"Path":distance, "Distance" : len(distance)-1})   
    else :
        return json.dumps({'Erro': 'No path between Author1 and Author2'})   
        
    
def path(authorS,authorD, parser):
    listVisitedAuthor = dict()
    try: 
    	listToVisit = list()
    	for i in parser.author :
    		if len(i) > 0 :
    			if i[0] == authorS:
    				listVisitedAuthor[authorS] = list()
    				listVisitedAuthor[authorS].append(i[0])
    				listToVisit.append(authorS)
    				listToVisit = copy.copy(i[1:])
    				for l in i[1:]:
    					listVisitedAuthor[l] = listVisitedAuthor[authorS].copy()

    except:
         return "Error"  
    
    while len(listToVisit) != 0 :    
    	tmp = list()
    	for i in listToVisit :
    		if i == authorD:
    			listVisitedAuthor[i].append(authorD)  
    			return listVisitedAuthor[i]
    		if i not in listVisitedAuthor[i]:
    			listVisitedAuthor[i].append(i)
    			if i not in tmp:
    				tmp.append(i)
    			for k in parser.author:
    				if len(k) > 0:
    					if k[0] == i:
    						for l in k[1:]:
    							tmp.append(l)
    							listVisitedAuthor[l] = listVisitedAuthor[i].copy()
    	listToVisit = tmp
        
    return "Error"
        
run(host = 'localhost', port = 8091, debug = True)


