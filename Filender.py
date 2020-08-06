import os
import json
import argparse
import sys
import re
import time
parser =  argparse.ArgumentParser(epilog =f"[****Note****\n PLEASE REMOVE ANY EXTERNAL DEVICES WHILE UPDATING DATABASE IF DIDN'T WANT TO SEARCH INSIDE IT]")
parser.add_argument("-f",help="give the filename to search or if you want to use regex put it inside double quotes and if you want to search using exact file name it is advised to give it like this ^filename$ inside double quotes")
parser.add_argument('-udb',help="update the already existing file database[if you want, only give True nothing other than ] and [****PLEASE DON'T GIVE THIS FOR THE FIRST TIME WHEN YOU DON'T HAVE ANY DATABASE, AS FOR THE FIRST TIME THE TOOL AUTOMATICALLY CREATES DATABASE]")
args =  parser.parse_args()
if args.f is None and args.udb is None:
     os.system(f'cmd /c "python {__file__} -h"')
     sys.exit()

def get_drives():
            response = os.popen("wmic logicaldisk get caption")
            list1 = []
            for line in response.readlines():
                        line = line.strip("\n")
                        line = line.strip("\r")
                        line = line.strip(" ")
                        if (line == "Caption" or line == ""):
                                    continue
                        list1.append(line)
            return list1

def update_db():
    drives = get_drives()
    wholefiledb={}
    for drive in drives:
        print(f"Storing {drive} file index data to dbs......")
        for root, dir, files in os.walk(f"{drive}/", topdown = True):
            for file in files:
                if file not in wholefiledb:
                    filelist=[root]
                    wholefiledb[file] = filelist
                elif file in wholefiledb and root !=wholefiledb[file]:
                    wholefiledb[file].append(root)
    with open("db/filedb.json",'w') as f:
        json.dump(wholefiledb,f)
    print(f"Database stored in {os.getcwd()}\db as filedb.json")
def search_file(filetobesearched):
    print("Searching for",filetobesearched,"........")
    f2 = open("db/filedb.json")
    db =  json.load(f2)
    list1 = []
    for i in db:
        if re.search(filetobesearched, i):
            list1.append(i)
    if list1  == []:
        print("File is not present ")
    for i in list1:
        print(f"\n{i} present in following directory/directories")
        print("----------------------------------------")
        for j in db[i]:
            j = j.replace('\\','\\')
            j = j.replace('/','\\')
            print(j)
            

flag = 0   
db_dir = os.path.isdir("db")
if not db_dir:
    print("Seems like, you have't created a File Database for Searching.\nLet me create that for you...........\nIt may take sometime")
    os.system(f'cmd /c "mkdir db"')
    update_db()
    flag = 1
def str_to_bool(value):
    if value == 'True' or value =="true":
         return True
    else:
        print("----> Please only give desired values [True or False]")
        os.system(f'cmd /c "python {__file__} -h"')
        sys.exit()



if args.udb is not None:
    args.udb=str_to_bool(args.udb)
    if args.udb:
        h = f"{os.getcwd()}"
        os.system(f'cmd /c "del /f {h}\db\\filedb.json"')
        if not os.path.isfile("db/filedb.json"):
            update_db()
        if args.f is not None:
            print("Searching based on newly created database")
            search_file(args.f)
        elif args.f is None:
            print("You didn't give any file name or regex to find....")
elif args.udb is None and args.f is not None:
    if flag ==1:
        print("Searching using new created database")
    else:
        print('Continuing with existing database......')
    search_file(args.f)

