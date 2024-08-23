from sexpdata import Quoted, Brackets, loads, dumps
from copy import deepcopy

'''
class Metamacro:
	def __init__(self, node, arg_names=[])
		self.node = node
		self.arg_names = arg_names

	def __call__(self, args=[])
'''

def modify(node, f):
	node = f(node)

	if not (isinstance(node, list) or isinstance(node, Quoted) or isinstance(node, Brackets)):
		return node

	if isinstance(node, list):
		node = [modify(child, f) for child in node]
	if isinstance(node, Quoted):
		node = Quoted(modify(node.x, f))
	if isinstance(node, Brackets):
		node = Brackets([modify(child, f) for child in node.I])

	return node

def compile_node(node, _metamacros={}):
	if isinstance(node, str) or isinstance(node, int): # includes Symbol
		return str(node)
	
	if isinstance(node, list):
		prev = node
		while True:
			if (metamacro := _metamacros.get(node[0])) is None: break

			# "*index" -> node[index]
			subst = deepcopy(metamacro)
			node = modify(subst,
				lambda x:
					node[int(x[1:])]
					if isinstance(x, str) and x[0] == '*' else
					x
			)

			if prev == node:
				break

		if node[0][0] == '*':
			command = node[0][1:]
			if command == 'define':
				# TODO better error
				assert node[1][0] != '*'
				_metamacros[node[1]] = node[2]
				return

		return '[' + '/'.join(compile_node(child, _metamacros) for child in node) + ']'

	if isinstance(node, Quoted):
		result = compile_node(node.x, _metamacros)
		for char in '\\', '[', ']', '/':
			result = result.replace(char, '\\' + char)
		return result
	
	if isinstance(node, Brackets):
		return ''.join(compile_node(child, _metamacros) or '' for child in node.I)

	raise TypeError(f'unsupported type "{type(node).__name__}"')

def compile(code):
	return compile_node(loads(code))
