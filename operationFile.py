# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 08:54:38 2017

@author: 3525162
"""

def parserFichier(parser, name):
    f = open(name)
    ff = f.read()
    f.close()
    parser.feed(ff)
    return parser
