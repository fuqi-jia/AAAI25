import os
import sys
import shutil

source_dir = sys.argv[1]
target_dir = sys.argv[2]
sep = int(sys.argv[3])

def get_dir(s):
    dir = s[:s.rfind('/')]
    res = s.split("/")
    i = 0
    new_res = []
    while i < len(res):
        if(res[i] == '.' or res[i] == '..'):
            pass
        else:
            new_res.append(res[i])
        i += 1
    
    return '/'.join(new_res)


def list_allfile(path, all_files=[]):    
    if os.path.exists(path):
        files=os.listdir(path)
    else:
        print('this path not exist')
    for file in files:
        if os.path.isdir(os.path.join(path, file)):
            list_allfile(os.path.join(path, file), all_files)
        else:
            all_files.append(os.path.join(path, file))
    return all_files

def copy(cur, j):
    for source in cur:
        # print(source)
        new_dir = target_dir + '/' + str(j) + '/' + '/'.join(source.split('/')[1:-1])
        new_file = target_dir + '/' + str(j) + '/' + '/'.join(source.split('/')[1:])
        # print(new_dir)
        if(not os.path.exists(new_dir)):
            os.makedirs(new_dir)
        try:
            shutil.copyfile(source, new_file)
        except IOError as e:
            print("Unable to copy file. %s" % e)
        except:
            print("Unexpected error:", sys.exc_info())
    cur.clear()


all_files = []
list_allfile(source_dir, all_files)
if(len(all_files) > sep):
    i = 0
    j = 0
    res = []
    cur = []
    while i < len(all_files):
        if i != 0 and i % sep == 0:
            cur.append(all_files[i])
            copy(cur, j)
            print('---------------' + str(i) +'/' + str(len(all_files)) + '---------------')
            j += 1
        else:
            cur.append(all_files[i])
        i += 1

    if(len(cur) != 0):
        copy(cur, j)