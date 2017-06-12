# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 09:09:16 2017

@author: 3525162
"""

from html.parser import HTMLParser 


class MyHTMLParser(HTMLParser):
   
    def __init__(self):
        super().__init__()
        self.inAuthor = False           # si balise author
        self.inTitle = False		# si balise title
        self.inYear = False		# si balise year
        self.inJournal = False		# si balise journal ou booktitle
        self.authorD = None
        self.authorL = []
        self.author = []
        self.titleD = None
        self.title = []
        self.yearD = None
        self.year = []
        self.journalD = None
        self.journal = []

	
        
    
    def handle_starttag(self, name, attrs):
        if name == 'author':
            self.authorD = '' 
            self.inAuthor = True 
        if name == 'title': 
            self.inTitle = True
            self.titleD = ''
        if name == 'year':
            self.inYear = True 
            self.yearD = ''         
        if name == 'journal' or name == 'booktitle' :
            self.inJournal = True 
            self.journalD = ''

        
    def handle_endtag(self, tag):
        YEAR = 2011
        if tag == 'article' or  tag == 'mastersthesis' or tag == 'phdthesis' or tag == 'inproceedings' or tag == 'proceedings' or tag == 'book' or tag == 'incollection' :
            if int(self.yearD) > YEAR:
            	self.author.append(self.authorL)
            	self.journal.append(self.journalD) 
            	self.year.append(self.yearD) 
            	self.title.append(self.titleD)  
            self.authorL = [] 
            self.authorD = ''  
        if tag == 'author':
            self.inAuthor = False 
            self.authorL.append(self.authorD)     
        if tag == 'title':        		
            self.inTitle = False
        if tag == 'year':
            self.inYear = False
        if tag == 'journal' or tag == 'booktitle':		
            self.inJournal = False

        
    def handle_data(self, data):
        if self.inAuthor == True:
            self.authorD += data
        if self.inTitle == True:
            self.titleD += data
        if self.inYear ==  True:
            self.yearD += data
        if self.inJournal == True:
            self.journalD += data

    def handle_entityref(self, data):
        if self.inAuthor == True:
            self.authorD += '&'+data+';'
        if self.inTitle == True:
            self.titleD += '&'+data+';'
        if self.inYear ==  True:
            self.yearD += data
        if self.inJournal == True:
            self.journalD += data
 




