import datetime
import os, sys
import hashlib, ntpath

# TODO: Need to add an option to search other directories for possible duplicates.
import time


def findDup(parentFolder):
    """
	looks at all files in all folders for duplicates
	:param parentFolder:
	:return: dictionary of duplicate files in the same folder
	"""
    # Dups in format {hash:[names]}
    dups = {}
    waiting = ['.', '*']
    dotcnt = 0
    for dirName, subdirs, fileList in os.walk(parentFolder):
        print(('\nScanning %s...' % dirName))
        for filename in fileList:
            if dotcnt > 50:
                print('\n')
                dotcnt = 0
            dotcnt = dotcnt + 1
            print((waiting[1]), end=' ')
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
                # TODO: Need to add the path to a new dup array with the md5 and remove the matching dup from this array.
                # then the new array can be presented to the user to choose what to delete.
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
    for key in list(dict2.keys()):
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
            # TODO: Make the lookup a regex rather than multiple conditions
            if theval.find("(1)") != -1:
                print("found {f}".format(f=file))
                files_to_delete.append(file)
            elif theval.find("(2)") != -1:
                print("found {f}".format(f=file))
                files_to_delete.append(file)
            elif theval.find("(3)") != -1:
                print("found {f}".format(f=file))
                files_to_delete.append(file)
            else:
                files_to_not_delete.append(file)

    # TODO Need to check the list of files to see if it is a duplicate.
    print("Report: \n")
    print("number of files to delete = {numd}\n" \
          "number of duplicated files = {numt}\n" \
          "number of files to keep = {numk}".format(
        numd=len(files_to_delete), numt=len(results), numk=len(files_to_not_delete)))
    print("*" * 100)
    for file in files_to_not_delete:
        print("Do not delete {f}".format(f=file))
    print("*" * 100)
    delete_files(files_to_delete)


def delete_files(files):
    print("This is the files to delete")
    if len(files) > 0:
        for file in files:
            print(file)
        result = input("Do you want to delete these files? y/n \nIf you choose y the files will be deleted. n to exit.")
        # print result
        if result == "y":
            for file in files:
                os.remove(file)
                print("{f} Deleted! ".format(f=file))
    else:
        print("There are no files to delete!")


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def get_option(delFiles, tempresult):
    answer = input("Select the corresponding number of the file you want to delete? otherwise enter n")
    print(("You chose: " + answer + "\n"))
    if answer == "n":
        print("OK! ")
    elif answer.isdigit():
        # todo: need to get the corresponding file that matches the counter from answer.
        try:
            delFiles.append(tempresult[int(answer) - 1])
            print(("The file to delete is: %s" % delFiles[0]))
            delete_files(delFiles)
        except IndexError as e:
            print(("%s is not an option!" % answer))
            get_option(delFiles, tempresult)


def select_delete_result(f, result):
    """
	Displays all the items in the list and asks user to select items to delete.
	:param f: The log file
	:param result: The list of files that were found to be duplicates.
	:return:
	"""
    delFiles = []
    tempresult = []
    counter = 0
    for subresult in result:
        created = os.path.getctime(subresult)

        counter = counter + 1
        print(('\t(%s)\t%s \t- File Size: %sMb - Date created: %s\n' % (counter, subresult,
                                                                        str(os.path.getsize(subresult)),
                                                                        datetime.datetime.fromtimestamp(
                                                                            created).strftime('%Y-%m-%d %H:%M:%S'))))

        f.write('\t(%s)\t%s \t- File Size: %sMb - Date created: %s\n' % (counter, subresult,
                                                                         str(os.path.getsize(subresult)),
                                                                         datetime.datetime.fromtimestamp(
                                                                             created).strftime('%Y-%m-%d %H:%M:%S')))
        # TODO: Get the file size and created date

        tempresult.append(subresult)
    print('___________________')
    f.write("___________________\n")
    answer = input("Options: \n\tSelect the corresponding number of the file you want to delete from above? \n"
                   "\t(n) for None \n"
                   "\t(x) for Exit")
    print(("You chose: " + answer + "\n"))
    if answer == "n":
        print("OK! ")
    elif answer.isdigit():
        # todo: need to get the corresponding file that matches the counter from answer.
        try:
            delFiles.append(tempresult[int(answer) - 1])
            print(("The file to delete is: %s" % delFiles[0]))
            delete_files(delFiles)
        except IndexError as e:
            print(("%s is not an option!" % answer))
            get_option(delFiles, tempresult)
    elif answer == "x":
        print("Goodbye!")
        return "exit"
    else:
        print("OK! ")

def output_list(results):
    for r in results:
        print("********** Duplicates of each other *************")
        for sub in r:
            print("file: %s " %sub)


def printReport(results):
    print("This is the report.")
    print("There are %s duplicated files." % len(results))
    total = 0
    totalSize = 0
    for r in results:
        total = total + len(r)
        for i in r:
            totalSize = totalSize + os.path.getsize(i)
            kb = totalSize / 1000
            mb = kb * 0.0009765625

    print("Of the %s duplicates there are a total of %s duplicate files." % (len(results), total))
    print("If you delete all the duplicates you should save %sbytes of space." % totalSize)
    print("%sKb" % kb)
    print("%sMb" % mb)
    option = input("\nselect an Option: \n"
                    "(l) for listing all the duplicates. \n"
                    "() for  \n"
                    "(c) to continue?")
    if option == "l":
        output_list(results)
    elif option == "":
        pass
    elif option == "c":
        print("OK!")

    option = input("\nContinue? ")
    if option == "y":
        print("Continuing.....!")
    else:
        print("Continuing anyway!")






def processDuplicateResults(dict1):
    results = list([x for x in list(dict1.values()) if len(x) > 1])
    with open("duplog.txt", "a") as f:
        if len(results) > 0:
            printReport(results)
            print('Duplicates Found:')
            f.write("Duplicates Found:\n")
            print('The following files are identical. The name could differ, but the content is identical')
            f.write("The following files are identical. The name could differ, but the content is identical\n")
            print('___________________')
            f.write("___________________\n")

            for result in results:
                conclusion = select_delete_result(f, result)
                if conclusion == "exit":
                    return

            answer = input("\nDo you want to delete all the files that have (1) in them?")
            print(answer)
            if answer == "y":
                delete_duplicates(results)
            elif answer == 'n':
                print("\nNo files to be deleted.")
            else:
                print("OK! ")
        else:
            print('\nNo duplicate files found.')
    f.closed


if __name__ == '__main__':
    try:
        folders = [str(sys.argv[1])]
    except IndexError:
        print("Missing Directory to search!")
        raise ValueError("Missing Directory to search please try again.")
    dups = {}
    for i in folders:
        # Iterate the folders given
        if os.path.exists(i):
            # Find the duplicated files and append them to the dups
            joinDicts(dups, findDup(i))
        else:
            print(('%s is not a valid path, please verify' % i))
            sys.exit()
    processDuplicateResults(dups)
