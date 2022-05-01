# these imports are important
import os
from os.path import exists
import sys
import platform
import requests

pltfm = platform.system() # get user OS (for pltfm detection and host cmd)
hsarc = platform.machine() # get user arch (e.g. x86_64, armhf, i386, etc) (for host cmd)

if(pltfm!="Linux"): # if user is not using linux, warn them
	cptqn = input("MeltOS has detected your OS as " + pltfm +", but MeltOS is designed for Linux. Are you sure you want to continue? (Y/n): ")
	if(suphn!="y"):
		print("You selected " + cptqn)
		print("Exiting...")
		exit()

os.system("clear") # clear the screen
print("""------------------------------------------------
| MeltOS - v0.1.3.1 MIT License                |
| It's not really an OS, just a python script! |
------------------------------------------------
""") # this is the intro box thing
def read_cmd(cmd): # this reads the given command. coolio, right?
	if(cmd[0:4]=="exit" and len(cmd)==4): # this code exits back to the normal stuff
		print("Exiting gracefully...")
		os.system("clear")
		exit()
	elif(cmd[0:3]=="dir" and len(cmd)==3): # print the directory
		print(os.listdir(cwd)) # this is fine
	elif(cmd[0:3]=="cd " and len(cmd)>=4): # change the cwd... very simple
		try:
			os.chdir(cmd[3:len(cmd)]) # tries to change dir, errors are self-explanitory (i think i didn't spell that right)
		except FileNotFoundError:
			print("E: " + cmd[3:len(cmd)] + " does not exist")
		except NotADirectoryError:
			print("E: " + cmd[3:len(cmd)] + " is not a directory")
		except PermissionError:
			print("E: " + cmd[3:len(cmd)] + " is beyond your permissions")
	elif(cmd[0:5]=="clear" or cmd[0:3]=="cls"): # if command is clear or cls, clear screen. duh
		if(len(cmd)==3 or len(cmd)==5):
			os.system("clear")
		else:
			print("E: \"" + cmd + "'| not found or improper.") # this is here because of weird code stuff
	elif(cmd[0:5]=="wget " and len(cmd)>=5): # crudely use wget using os.system
		os.system("wget " + cmd[5:len(cmd)] + " >> " + homedir + "/tmp.txt")
		with open(homedir + "/tmp.txt", "r") as out: # this code sucks
			print(out.read())
	elif(cmd[0:6]=="shell " and len(cmd)>=6): # crudely use any normal command in normal normalness?
		os.system(cmd[6:len(cmd)] + " >> " + homedir + "/tmp.txt")
		with open(homedir + "/tmp.txt", "r") as out: # this code sucks x3
			print(out.read())
	elif(cmd[0:5]=="echo " and len(cmd)>=5): # echo the inputted text, simple
		print(cmd[5:len(cmd)])
	elif(cmd[0:4]=="scr " and len(cmd)>=4): # run a .moexe script
		filepath = cmd[4:len(cmd)]
		with open(filepath) as fp:
			for index, line in enumerate(fp):
				read_cmd(line.strip())
	elif(cmd[0:5]=="read " and len(cmd)>=5):
		filepath = cmd[5:len(cmd)]
		with open(filepath) as fp:
			for index, line in enumerate(fp):
				print(line.strip()) # use line.strip or i will come for you in your sleep
	elif(cmd[0:4]=="py3 " and len(cmd)>=4): # run a python script in a python script. sounds cool to me
		exec(open(cmd[4:len(cmd)]).read())
	elif(cmd[0:4]=="host" and len(cmd)==4): # give host info
		print("Host OS: " + pltfm + "\nHost Architecture: " + hsarc)
	elif(cmd[0:4]=="get " and len(cmd)>=4): # package manager thing ig
		if(cmd[4:7]=="-py"): # if py, get py, else get moexe
			print("Installing \"" + cmd[8:len(cmd)] + ".py\" from meltos.wens.cf...\n")
			read_cmd("shell curl -0 'https://meltos.wens.cf/python/" + cmd[8:len(cmd)] + ".py' -O")
		else:
			print("Installing \"" + cmd[4:len(cmd)] + ".moexe\" from meltos.wens.cf...\n")
			read_cmd("shell curl -0 'https://meltos.wens.cf/moexe/" + cmd[4:len(cmd)] + ".moexe' -O")
	else: # if all else fails, give an error
		print("E: \"" + cmd + "\" not found or improper.")
homedir = os.getcwd() # set the home directory to the init location

while True:
	cwd = os.getcwd() # get the cwd. simple
	username = os.getlogin() # get the user's username for the username@cwd combo
	tmpexists = exists(homedir + "/tmp.txt") # check if tmp.txt exists
	if(tmpexists): # if it exists, KILL IT WITH FIRE
		os.remove(homedir + "/tmp.txt")
	pcmd = input(username + "@" + cwd + ": ") # username@cwd combo
	read_cmd(pcmd) # run the cmd, duh
