# procura um caminho recursivamente a partir do nosso diretorio
import os


def recursive_path(filename:str):
	filepath = ""
	for path, folders, files in os.walk(".\\"):
		if filename in files:
			filepath = os.path.join(path, filename)
			break
	return filepath

""" 	
This function reads a text file, and for each char that is not \n, is added to the array
as soon as we reach \n we stop adding to this array and create a new array where next char that is not \n is gonna be added, 
in the end, all arrays are added to the return array in order, meaning, the return array is a 2D array"""
# Basicamente: cada linha é um array de char, e o retornoe é um array de array de chars
def txt2list(filepath:str,*,fn):
	array2D 	= list()
	path:str	= recursive_path(filepath)

	with open( path,'r') as reader: 
		for line in reader.readlines(): 
			data = fn(line)
			if data is not None:
				array2D.append(data)
	return array2D


def measure(fn,*args,repeat=1,out:list=None):
	# Other option are: process_time , perf_counter
	from time import perf_counter as counter
	t = counter()

	for i in range(repeat): 
		result = fn(*args)
		if hasattr(out,"append"):
			out.append(result)

	elapsed = counter() - t
	print(f"Took {elapsed:.4f}s for {str(fn)} to run {repeat} times")
	return elapsed


def measure_all(fns:list,*args,repeat=1):
	# Other option are: process_time , perf_counter
	from time import process_time as counter
	for fn in fns:
		measure(fn, *args,repeat=repeat)

from itertools import cycle