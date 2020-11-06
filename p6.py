from z3 import *
import sys
import numpy as np
import ast
import json
# weighted stability


# get input from either input txt file or script
# format in input file: 
# - [100, 100, 100, 1, 100]
# - [[0, 7, 1, 0, 8],[7, 0, 5, 4, 3],[1, 5, 0, 2, 6],[0, 4, 2, 0, 1],[8, 3, 6, 1, 0]]
# format in script as descripbed below and in the description from hw 8 (w, c)

if len(sys.argv)>1:
	file = sys.argv[1]
	print('input file loaded: '+ str(file))
	with open(file, 'r') as fi:
		inputline = fi.readline()
		weight = ast.literal_eval(inputline)
		inputline_ = fi.readline()
		capacity = ast.literal_eval(inputline_)
else:
	weight = [100, 100, 100, 1, 100]
	capacity = [[0, 7, 1, 0, 8], \
     			[7, 0, 5, 4, 3], \
     			[1, 5, 0, 2, 6], \
     			[0, 4, 2, 0, 1], \
     			[8, 3, 6, 1, 0]]

def main():
	s = Optimize()
	constraint = []
	function = objectiveFunction()
	constraints(constraint)
	s.add(constraint)
	s.maximize(function)
	if s.check() == sat:
		model = s.model()
		for a in model:
			if '-' not in str(a):
				print('variable: ' + str(a) + ' value = ' + str(model[a]))
	else:
		print('False, error to solve the problem!')

# setting up objective function
def objectiveFunction():
	function = 0
	for i, weights in enumerate(weight):
		if weights > 0:
			function += weights * Int('x_%s' % (i+1))

	panalty = 0
	for i, lists in enumerate(capacity):
		for j, capacity_ij in enumerate(lists):
			if j >= i and capacity_ij > 0:
				panalty += capacity_ij * Int('x_%s' % (i+1)) * Int('x_%s' % (j+1))
	panalty *= (max(weight)+1)
	function -= panalty
	

	return function

# setting up constraints: variables can only assume values 0 or 1
def constraints(constraint):
	for i, x in enumerate(weight):
		constraint.append(Or(Int('x_' + str(i+1)) == 1, Int('x_' + str(i+1)) == 0))


if __name__== "__main__":
    main()