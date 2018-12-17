#!/usr/bin/env python

def convert(in_array):

	out_str = 'set'
	out_str += ';0'

	for element in in_array:
		out_str += ';'
		out_str += str(element);

	out_str += ';0'
	out_str += ';0'


	return out_str