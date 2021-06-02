import re
from pathlib import Path

def file_ext(f_path: Path) -> str:
	return f_path.suffix[1:]

def replace_file_ext(f_path: Path, new_ext: str) -> Path:
	new_ext = new_ext if new_ext == '' else '.' + new_ext
	p = re.compile('\.[\w]+$')
	f_path_str = str(f_path)
	match = p.search(f_path_str)
	if match == None:
		return Path(f_path_str + new_ext)
	return Path(p.sub(new_ext, f_path_str))
