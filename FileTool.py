import sys
import time
import re
import os
import shutil
import zipfile


def findSpecial():
    """
    this function searches whole computers memory to find and print files name and location of files names are from the form -
    [any combination of symbols]__[any combination of symbols]__ .[any postfix]
    """
    # this lambda func used to search all computer drives
    a_to_z = lambda: (chr(i) + ":\\" for i in range(ord("A"), ord("Z") + 1))
    # this used to measure how  much time the search took
    starting_time = time.time()
    # this var used to count how many file are there - and to index them in the output
    how_many_files_count = 1
    # iterating over all drives, using "os.walk" function, looking for the "special" file name using python regex
    for drive in a_to_z():
        for dirpath, _, files in os.walk(drive):
            for file in files:
                result = re.search(r'.*__[a-zA-z]+__.*', file)
                if result:
                    if not result.group().endswith('.py') and not result.group().endswith('.pyc'):
                        path = os.path.abspath(os.path.join(dirpath, file))
                        # printing the while - absolute path
                        print(str(how_many_files_count) + ') ' + result.group() + '\nabsoute path: ' + path + '\n')
                        how_many_files_count += 1
    # printing more info about the operation
    elapsed_time = time.time() - starting_time
    print('the operation took: %d seconds \nfound %d files' % (elapsed_time, how_many_files_count - 1))


def copyFile(s_path, d_path):
    """
    this function is using the "shutil.copy" python function to copy a file from the source path to dest path provided
    :param s_path:
    source path to take the file from
    :param d_path:
     destination path to copy the file to
    """
    print('starting to copy file..')
    starting_time = time.time()
    try:
        shutil.copy(s_path, d_path)
    except shutil.Error as e:
        print('operation error: %s' % e)
    except IOError as e:
        print('I/O error: %s' % e.strerror)
    elapsed_time = time.time() - starting_time
    print('file copied successfully, the operation took: %d seconds' % (elapsed_time))


def zipFile(s_path, d_path):
    """
    this function is using zipfile python module to zip a file from the source path and move the zipped file to the dest path
    *if you want the zipped file to stay in the same folder - just input the same path both times
    :param s_path:
    source path to take the file from
    :param d_path:
     destination path to copy the file to
    """
    d_path_final = d_path + r'\newZip.zip'
    # this is done to make both paths "raw string"
    d_path_final = r"{}".format(d_path_final)
    s_path_final = r"{}".format(s_path)
    starting_time = time.time()
    with zipfile.ZipFile(d_path_final, 'a') as myzip:
        myzip.write(s_path_final)
    elapsed_time = time.time() - starting_time
    print('file zipped successfully, the operation took: %d seconds' % (elapsed_time))


def main():
    # checking minimum length of "sys.argv" for any flag
    if len(sys.argv) < 2:
        print('WRONG USAGE: tool should be used as: [name of program file.py] --[flag] [optional path argument]')
        sys.exit(1)
    # checking that the expression got a "--" for flag
    flag = sys.argv[1]
    if flag[:2] != '--':
        print('WRONG USE: cannot find "--" symbol for flag')
        sys.exit(1)

    if flag[2:] == 'help':
        print(
            'USAGE: [name of program file.py] --[flag] [optional path argument]\nFLAGS:\n1)findSpecial: finds all files which name is of the form "(SOMETHING)__(WORD)__(SOMETHING)" from computer file system\n\n2)copyFile: copies a file from the first argument given path to the dest one, this operation requireds two more flags\n\n3)zipFile: zips a file from the source path - and copies it to the dest path given, this operation requireds two more flags')
        sys.exit(0)

    if flag[2:] == 'findSpecial':
        findSpecial()

    elif flag[2:] != 'copyFile' and flag[2:] != 'zipFile':
        print(
            'WRONG USAGE: only flags you can use are "findSpecial", "copyFile" and "zipFile", for more information type the flag "--help" ')
        sys.exit(1)

    else:
        if len(sys.argv) != 4:
            print('WRONG USAGE: for "copyFile" and "zipFile" you should provide path for the source and the dest!')
            sys.exit(1)

        else:
            s_path = sys.argv[2]
            d_path = sys.argv[3]
            if not os.path.exists(s_path):
                print("WRONG USAGE: source path doesn't exist")
                sys.exit(1)
            if not os.path.exists(d_path):
                print("WRONG USAGE: destination path doesn't exist")
                sys.exit(1)
            if not os.path.isfile(s_path):
                print("WRONG USAGE: source path isn't a file")
                sys.exit(1)
            if flag[2:] == 'copyFile':
                copyFile(s_path, d_path)
                if s_path == d_path:
                    print('WRONG USE: both paths given are the same')
                    sys.exit(1)
            else:
                zipFile(s_path, d_path)


if __name__ == '__main__':
    main()
