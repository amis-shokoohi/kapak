import re

def file_ext(f_path):
	p = re.compile('\.([\w]+)$')
	match = p.search(str(f_path))
	if match == None:
		return ''
	return match.group(1)

def replace_file_ext(f_path, new_ext):
	p = re.compile('\.[\w]+$')
	match = p.search(str(f_path))
	if match == None:
		return str(f_path) + '.' + new_ext
	return p.sub('.' + new_ext, str(f_path))
