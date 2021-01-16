from pathlib import Path

def _has_flag(flag_name: str, argv: [str]) -> bool:
	flag_exists = False
	flag_count = 0
	if len(argv) == 0:
		return flag_exists
	for v in argv:
		if v == '-'+flag_name[0] or v == '--'+flag_name:
			flag_exists = True
			flag_count += 1
	if flag_count > 1:
		raise Exception('used "' + flag_name + '" flag more than once')
	return flag_exists

def has_remove_flag(argv: [str]) -> bool:
	return _has_flag('remove', argv)

def has_zip_flag(argv: [str]) -> bool:
	return _has_flag('zip', argv)

def get_path(argv: [str]) -> Path:
	if len(argv) == 0:
		return None
	for v in argv:
		if v[0:1] != '-':
			return Path(v)
