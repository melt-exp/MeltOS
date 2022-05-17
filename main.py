# these imports are important
import os, platform, time
from os.path import exists

homedir = os.getcwd() # set the home directory to the init location
pltfm = platform.system() # get user OS (for pltfm detection and host cmd)
hsarc = platform.machine() # get user arch (e.g. x86_64, armhf, i386, etc) (for host cmd)

def getupdate(): # update
	print("Updating get...")
	prevdir = os.getcwd()
	os.chdir(f"{homedir}/tmp")
	print("Step 1/3 complete.")
	os.system(f"curl -s '{getrepo}moexe/list' -O")
	filepath = f"{homedir}/tmp/list"
	with open(filepath) as fp:
		for index, line in enumerate(fp):
			molst = line.strip()
	print("Step 2/3 complete.")
	os.system(f"curl -s '{getrepo}/python/list-py' -O")
	filepath = homedir + "/tmp/list-py"
	with open(filepath) as fp:
		for index, line in enumerate(fp):
			pylst = line.strip()
	print("Step 3/3 complete.")
	os.chdir(prevdir)
	print("Update completed.")

# create important dirs
moi = exists(f"{homedir}/apps")
if(not moi):
	os.mkdir(f"{homedir}/apps")
moi = exists(f"{homedir}/apps/mox")
if(not moi):
	os.mkdir(f"{homedir}/apps/mox")
moi = exists(f"{homedir}/apps/py3")
if(not moi):
	os.mkdir(f"{homedir}/apps/py3")
moi = exists(f"{homedir}/tmp")
if(not moi):
	os.mkdir(f"{homedir}/tmp")
	getupdate()
else: 
	filepath = f"{homedir}/tmp/list"
	with open(filepath) as fp:
		for index, line in enumerate(fp):
			molst = line.strip()
	filepath = f"{homedir}/tmp/list-py"
	with open(filepath) as fp:
		for index, line in enumerate(fp):
			pylst = line.strip()
# check for get config
moi = exists(f"{homedir}/tmp/getrepo.cfg")
if(moi):
	filepath = f"{homedir}/tmp/getrepo.cfg"
	with open(filepath) as fp:
		for index, line in enumerate(fp):
			getrepo = line.strip()
else:
	getrepo = "https://meltos.wens.cf/"

if(pltfm!="Linux"): # if user is not using linux, warn them
	cptqn = input(f"MeltOS has detected your OS as {pltfm}, but MeltOS is designed for Linux. Are you sure you want to continue? (Y/n): ")
	if(cptqn!="y"):
		print(f"You selected {cptqn}")
		print("Exiting...")
		exit()
		
mover = "v0.1.4.2"
os.chdir(f"{homedir}/tmp")
os.system("curl -s 'https://meltos.wens.cf/newest' -O")
filepath = f"{homedir}/tmp/newest"
with open(filepath) as fp:
	for index, line in enumerate(fp):
		monewestver = line.strip()
if(monewestver!=mover):
	verqn = input(f"MeltOS has detected you are running {str(mover)}, but the newest MeltOS version is " + str(monewestver) + ". Are you sure you want to continue? (Y/n): ")
	if(verqn!="y"):
		print(f"You selected {verqn}")
		print("Exiting...")
		os.remove("newest")
		exit()	
os.remove("newest")
os.chdir("..")

os.system("clear") # clear the screen
print(f"""------------------------------------------------
| MeltOS - { mover } MIT License                |
| It's not really an OS, just a python script! |
------------------------------------------------
""") # this is the intro box thing
cmds = ["exit", "dir", "cd", "clear", "cls", "curl", "shell", "echo", "scr", "read", "py3", "host", "get", "wait", "hd", "gr", "help", "cmpdocs"]
def read_cmd(cmd): # this reads the given command. coolio, right?
	global getrepo
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
			print(f"E: {cmd[3:len(cmd)]}  does not exist")
		except NotADirectoryError:
			print(f"E: {cmd[3:len(cmd)]} is not a directory")
		except PermissionError:
			print(f"E:  { cmd[3:len(cmd)] } is beyond your permissions")
	elif(cmd[0:5]=="clear" or cmd[0:3]=="cls"): # if command is clear or cls, clear screen. duh
		if(len(cmd)==3 or len(cmd)==5):
			os.system("clear")
		else:
			cmdnotfound(cmd)
	elif(cmd[0:5]=="curl " and len(cmd)>=5): # crudely use curl using shell
		read_cmd(f"shell curl { cmd[5:len(cmd)]}")
	elif(cmd[0:6]=="shell " and len(cmd)>=6): # crudely use any normal command in normal normalness?
		os.system(f"{cmd[6:len(cmd)]} >> {homedir}/tmp/old_out")
		with open(f"{homedir}/tmp/old_out", "r") as out: # this code sucks x3
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
		print(f"Host OS: {pltfm}\nHost Architecture: {hsarc}")
	elif(cmd[0:4]=="get " and len(cmd)>=4): # package manager thing ig
		if(pltfm!="Linux"):
			print(f'W: Your platform is \'{pltfm}\', but get is designed for Linux.')
		if(cmd[4:10]=="update"):
			getupdate()
		elif(cmd[4:7]=="-py"): # if py, get py, else get moexe
			if(cmd[8:len(cmd)] in pylst):
				prevdir = os.getcwd()
				read_cmd(f"cd {homedir}/apps/mox") # move to homedir/apps/mox
				print("I: Moved to homedir/apps/mox to allow support for moexe integration.")
				print(f"Installing '{cmd[8:len(cmd)]}.py' from meltos.wens.cf...\n")
				read_cmd(f"shell curl -0 '{getrepo}python/{cmd[8:len(cmd)]}.py' -O")
				read_cmd(f"cd {prevdir}")
			else:
				print(f"E: Could not find {cmd[8:len(cmd)]} in package list. Try running \"get update\".")
		else:
			if(cmd[4:len(cmd)] in molst):
				prevdir = os.getcwd()
				read_cmd(f"cd {homedir}/apps/py3") # move to homedir/apps/mox
				print("I: Moved to homedir/apps/py3 to allow support for python integration.")
				print(f"Installing \"{cmd[4:len(cmd)]}.moexe\" from meltos.wens.cf...\n")
				read_cmd(f"shell curl -0 '{getrepo}moexe/{cmd[4:len(cmd)]}.moexe' -O")
				read_cmd(f"cd {prevdir}")
			else:
				print(f"E: Could not find {cmd[4:len(cmd)]} in package list. Try running \"get update\".")
	elif(cmd[0:5]=="wait " and len(cmd)>=5):
		time.sleep(int(cmd[5:len(cmd)]))
	elif(cmd[0:2]=="hd" and len(cmd)==2):
		print(f"Your home directory is \"{homedir}\".")
	elif(cmd[0:2]=="gr" and len(cmd)>=2):
		if(len(cmd)==2):
			print(f"Your current get repository is \"{getrepo}\".")
		else:
			if(cmd[3:len(cmd)]=="default"):
				moi = exists(f"{homedir}/tmp/getrepo.cfg")
				if(moi):
					os.remove(f"{homedir}/tmp/getrepo.cfg")
				print('Set get repo to "https://meltos.wens.cf/".')
			else:
				getrepo = cmd[3:len(cmd)]
				moi = exists(f"{homedir}/tmp/getrepo.cfg")
				if(moi):
					os.remove(f"{homedir}/tmp/getrepo.cfg")
				# CRITICAL: make file and write new url
				print(f'Set get repo to "{cmd[3:len(cmd)]}".')
	elif(cmd[0:4]=="help" and len(cmd)==4):
		print(cmds)
	elif(cmd[0:7]=="cmpdocs" and len(cmd)==7):
		print("W: This is intended for development ONLY!")
		os.system(f"echo AUTOMATICALLY COMPILED COMMAND LIST FOR {mover}:{str(cmds)} >> DOCS.md")
	else: 
		splcmd = cmd.split(None, 1)
		if(splcmd!=[]):
			moe = exists(f"{homedir}/apps/mox/{splcmd[0]}.moexe")
			if(moe):
				read_cmd(f"scr{homedir}/apps/mox/{splcmd[0]}.moexe")
			else:
				moe = exists(f"{homedir}/apps/py3/{splcmd[0]}.py")
				if(moe):
					read_cmd(f"py3 {homedir}/apps/py3/{splcmd[0]}.py")
				else:
					cmdnotfound(cmd)
		else:
			pass
def cmdnotfound(cmd):
	if(cmd in molst and len(cmd)!=0):
		print(f'E: \'{cmd}\'not found, but can be installed using \"get \'{cmd} \'.')
	elif(cmd in molst and len(cmd)!=0):
		print(f'E: "{cmd}" not found, but can be installed using "get -py {cmd}".')
	else:
		print(f"E: \"{cmd}\" not found or improper.")

while True:
	cwd = os.getcwd() # get the cwd. simple
	username = os.getlogin() # get the user's username for the username@cwd combo
	tmpexists = exists(f"{homedir}/tmp/old_out") # check if tmp.txt exists
	if(tmpexists): # if it exists, KILL IT WITH FIRE
		os.remove(f"{homedir}/tmp/old_out")
	icmd = f"{username}@{cwd}:"
	try: # thanks to Mwalters75 on GitHub for the keyboard interrupt ignorer
		pcmd = input(icmd) # username@cwd combo
		read_cmd(pcmd) # run the cmd, duh
	except KeyboardInterrupt: # do this so that MeltOS doesn't exit
		print("")
