from pathlib import Path

def _has_flag(flag_name, argv, arg_count_min, arg_count_max):
	flag_exists = False
	flag_count = 0
	l = len(argv)
	if l >= arg_count_min or l <= arg_count_max:
		for v in argv:
			if v == '-'+flag_name[0] or v == '--'+flag_name:
				flag_exists = True
				flag_count += 1

		if flag_count > 1:
			raise Exception('used "' + flag_name + '" flag more than once')

	return flag_exists

def has_remove_flag(argv):
	return _has_flag('remove', argv, 2, 3)

def has_zip_flag(argv):
	return _has_flag('zip', argv, 2, 3)

def get_path(argv):
	l = len(argv)
	if l >= 1 or l <= 3:
		for v in argv:
			if v[0:1] != '-':
				return Path(v)
	return None