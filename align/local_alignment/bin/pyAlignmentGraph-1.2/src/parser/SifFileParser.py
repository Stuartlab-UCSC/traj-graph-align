#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

'''
ISSUES: only nodes are saved, not the whole network

'''

__author__="Marco Mina"
__email__="marco.mina.85@gmail.com"

import sys
import os
from Parser import *
from FileParser import *
from RowParser import *

class SifFileParser(Parser):
	#comment_symbol = None
	column_separator = '\t'
	self_loop = False
	#one_column_listfile_format = True
	#two_columns_listfile_format = False
	#key_pos = 0
	#value_pos = 0
	#name_first = True
	#use_relative_paths = True
# to maiuscolo 
# header ?

	def __init__(self):
		super(SifFileParser, self).__init__()

	def process_file(self):
		#self.tempfileparser.reset()
		self.next_level_parser.input(self.input_data)
		self.next_level_parser.parse()

	def initialize_output(self):
		self.output_data = {}
		#if len(self.chain) == 0:
		self.chain = []
		self.chain.append(RowParser())
		self.chain[0].split = True
		self.chain[0].separator_symbol = ' '
		self.next_level_parser = FileParser()
		self.next_level_parser.set_chain(self.chain)

	def finalize_output(self):
		temp_nodes = {}
		temp_edges = {}
		temp = self.next_level_parser.output_data
		#print temp
		for i in self.next_level_parser.output_data:
			if type(i) == list and len(i)==1:
				temp_nodes[i[0]] = None
			elif type(i) == list and len(i)<=2:
				temp_nodes[i[0]] = float(i[1])
			elif type(i) == list and len(i)>2:
				if i[0] not in temp_nodes:
					temp_nodes[i[0]] = None
				if i[2] not in temp_nodes:
					temp_nodes[i[2]] = None
				if not self.self_loop and i[0] == i[2]:
					continue
				if i[0] not in temp_edges:
					temp_edges[i[0]] = {}
				temp_edges[i[0]][i[2]] = float(i[1])
			else:
				print "??" + str(i)
		self.output_data = []
		self.output_data.append(temp_nodes)
		self.output_data.append(temp_edges)

	def parse(self):
		if self.input_data == None:
			return
		if not type(self.input_data) == str:
			return
		self.initialize_output()
		self.process_file()
		self.next_level_parser.output_data
		self.finalize_output()
		#print self.output_data