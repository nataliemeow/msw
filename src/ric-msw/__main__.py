from . import compile
from sys import argv, stdin
from collections import deque

args = deque(argv)
args.popleft()

try:
	path = args.popleft()
except IndexError:
	path = None
path = None if path == '-' else path

if path is None:
	try:
		code = stdin.read()
	except KeyboardInterrupt:
		raise SystemExit()
else:
	with open(path, 'r') as f:
		code = f.read()

print(compile.compile(code))
