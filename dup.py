import os, sys
import hashlib, ntpath

#TODO: Need to add an option to search other directories for possible duplicates.
folders = ["C:\Users\jwells\Google Drive\Jds Echopass Folder\Documentation\EPFILE BACKUP"]

def findDup(parentFolder):
	"""
	looks at all files in all folders for duplicates
	:param parentFolder:
	:return: dictionary of duplicate files in the same folder
	"""
	# Dups in format {hash:[names]}
	dups = {}
	for dirName, subdirs, fileList in os.walk(parentFolder):
		print('Scanning %s...' % dirName)
		for filename in fileList:
			# Get the path to the file
			path = os.path.join(dirName, filename)
			# Calculate hash
			skip = False
			try:
				with open(path, 'rb'):
					pass
			except IOError:
				skip = True

			if not filename.startswith("~") and not skip:
				file_hash = hashfile(path)
				# Add or append the file path
				if file_hash in dups:
					dups[file_hash].append(path)
				else:
					dups[file_hash] = [path]
	return dups


def joinDicts(dict1, dict2):
	"""
	Joins two dictionaries
	:param dict1:
	:param dict2:
	:return:
	"""
	for key in dict2.keys():
		if key in dict1:
			dict1[key] = dict1[key] + dict2[key]
		else:
			dict1[key] = dict2[key]


def hashfile(path, blocksize=65536):
	"""

	:param path:
	:param blocksize:
	:return:
	"""
	with open(path, 'rb') as afile:
		hasher = hashlib.md5()
		buf = afile.read(blocksize)
		while len(buf) > 0:
			hasher.update(buf)
			buf = afile.read(blocksize)
	return hasher.hexdigest()


def delete_duplicates(results):
	"""

	:param results: list of results.
	:return:
	"""
	files_to_delete = []
	files_to_not_delete = []
	for res in results:
		for file in res:
			theval = path_leaf(file)
			# print theval
			# print os.path.basename(file)
			if theval.find("(1)") != -1:
				print "found {f}".format(f=file)
				files_to_delete.append(file)
			elif theval.find("(2)") != -1:
				print "found {f}".format(f=file)
				files_to_delete.append(file)
			elif theval.find("(3)") != -1:
				print "found {f}".format(f=file)
				files_to_delete.append(file)
			else:
				files_to_not_delete.append(file)

	#TODO Need to check the list of files to see if it is a duplicate. 
	print "Report: \n"
	print "number of files to delete = {numd}\n" \
		  "number of files to total = {numt}\n" \
		  "number of files to keep = {numk}".format(
		numd=len(files_to_delete),numt=len(results), numk=len(files_to_not_delete))
	print "*" * 100
	for file in files_to_not_delete:
		print "Do not delete {f}".format(f=file)
	print "*" * 100
	delete_files(files_to_delete)


def delete_files(files):
	print "This is the files to delete"
	for file in files:
		print file
	result = raw_input("Do you want to delete these files?")
	# print result
	if result == "y":
		for file in files:
			os.remove(file)
			print "{f} Deleted! ".format(f=file)


def path_leaf(path):
	head, tail = ntpath.split(path)
	return tail or ntpath.basename(head)


def printResults(dict1):
	results = list(filter(lambda x: len(x) > 1, dict1.values()))
	if len(results) > 0:
		print('Duplicates Found:')
		print('The following files are identical. The name could differ, but the content is identical')
		print('___________________')
		for result in results:
			for subresult in result:
				print('\t\t%s' % subresult)
			print('___________________')
		answer = raw_input("Do you want to delete all the files that have (1) in them?")
		print answer
		if answer == "y":
			delete_duplicates(results)
		else:
			print "OK! "
	else:
		print('No duplicate files found.')


if __name__ == '__main__':
	dups = {}
	for i in folders:
		# Iterate the folders given
		if os.path.exists(i):
			# Find the duplicated files and append them to the dups
			joinDicts(dups, findDup(i))
		else:
			print('%s is not a valid path, please verify' % i)
			sys.exit()
	printResults(dups)
