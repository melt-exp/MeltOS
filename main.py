# Import dependencies.
import os, platform, webbrowser, time
from colorama import Fore

# Prepare for homedir setting (and set homedir) by making/checking for meltos
cce = os.path.isdir(os.getcwd() +  '/meltos')
if(not cce):
  os.mkdir(os.getcwd() + '/meltos')

# Set homedir, machineos, and version.
home = os.getcwd() + '/meltos'
machineos = platform.system()
version = 'v1'

# Define 'spiterror' (throw colorized error)
def spiterror(error):
  print(Fore.RED + 'ERROR' + Fore.WHITE + ': ' + error)

# Define 'spitwarn' (throw colorized warning)
def spitwarn(warn):
  print(Fore.YELLOW + 'WARN' + Fore.WHITE + ': ' + warn)

# Define 'dlfile' (download file).
def dlfile(url):
  os.system(f"curl -s -f '{url}' -O") # Use cURL for downloading files.

# Define 'dlfilenamed' (download named file).
def dlfilenamed(url, name, parm):
  # Use cURL for downloading files.
  if(parm):
    os.system(f"curl -f '{url}' -o {name}")
  else:
    os.system(f"curl -s -f '{url}' -o {name}")

# Define 'changedir' (change current working directory):
def changedir(dir):
  try:
    os.chdir(dir)
  except FileNotFoundError:
    spiterror(f'{dir} does not exist!')
  except NotADirectoryError:
    spiterror(f'{dir} is not a valid directory!')
  except PermissionError:
    spiterror(f'{dir} requires greater permissions!')

# Define 'getupdates' (update get lists).	
def getupdates():
  print('Updating get repository lists...')
  previousdirectory = os.getcwd()
  changedir(f'{home}/tmp')
  dlfile('https://meltos.wens.cf/moexe/list')
  dlfile('https://meltos.wens.cf/python/list-py')
  changedir(previousdirectory)
  print('Update completed!')

# Define 'clearscreen' (clear the terminal).
def clearscreen():
  if(machineos=='Linux'):
    os.system('clear')
  elif(machineos=='Windows'):
    os.system('cls')
  else:
    spiterror('The clear function is not supported on your machine!')

clearscreen()
# Go to home directory
changedir(home)

# Check for needed files and folders, if they don't exist, make them.
cce = os.path.isdir(f'{home}/tmp')
if(cce): 
  if(os.path.exists(f"{home}/tmp/list") and os.path.exists(f"{home}/tmp/list-py")):
    filepath = f"{home}/tmp/list"
    with open(filepath) as fp:
      for index, line in enumerate(fp):
        moexelist = line.strip()
    filepath = f"{home}/tmp/list-py"
    with open(filepath) as fp:
      for index, line in enumerate(fp):
        pythonlist = line.strip()
  else:
    getupdates()
    filepath = f"{home}/tmp/list"
    with open(filepath) as fp:
      for index, line in enumerate(fp):
        moexelist = line.strip()
    filepath = f"{home}/tmp/list-py"
    with open(filepath) as fp:
      for index, line in enumerate(fp):
        pythonlist = line.strip()
else:
  os.mkdir(f'{home}/tmp')
  getupdates()
  filepath = f"{home}/tmp/list"
  with open(filepath) as fp:
    for index, line in enumerate(fp):
      moexelist = line.strip()
  filepath = f"{home}/tmp/list-py"
  with open(filepath) as fp:
    for index, line in enumerate(fp):
      pythonlist = line.strip()

cce = os.path.isdir(f'{home}/apps')
if(cce): 
  pass
else:
  os.mkdir(f'{home}/apps')
  os.mkdir(f'{home}/apps/moexe')
  os.mkdir(f'{home}/apps/python')

changedir(f'{home}/tmp')
dlfile("https://meltos.wens.cf/newest")
with open(f'{home}/tmp/newest') as nwv:
  for index, line in enumerate(nwv): 
    newestversion = line.strip()
if(newestversion!=version):
  outdatedprompt = input(f"You're on MeltOS {version}, but the newest version is {newestversion}. Would you like to update? (Y/n): ")
  if(outdatedprompt=="y"):
    webbrowser.open('https://meltos.wens.cf/timetoupdate?version={version}')
    time.sleep(1)
    exit()
  else:
    print("Alright then.")
changedir('..')
if(os.path.exists(f'{home}/color.mocfg')):
  with open(f'{home}/color.mocfg') as f:
    for line in f:
        color1 = eval('Fore.' + line)
        color2 = eval('Fore.' + next(f,None))
else:
  color1 = Fore.BLUE
  color2 = Fore.GREEN  
cmdlist = ['help', 'cd', 'dir', 'echo', 'sleep', 'run', 'clear', 'cls', 'curl', 'exit', 'get', 'script']
def interpretcmd(fullcmd):
  cmd = fullcmd.split(None, 1)
  if(cmd==[]):
    pass
  elif(cmd[0]=='help'):
    print(cmdlist)
  elif(cmd[0]=='cd'):
    lencmd = len(cmd[0]) + 1
    changedir(fullcmd[lencmd:len(fullcmd)])
  elif(cmd[0]=='dir'):
    print(os.listdir(os.getcwd()))
  elif(cmd[0]=='echo'):
    print(cmd[1])
  elif(cmd[0]=='sleep'):
    time.sleep(cmd[1])
  elif(cmd[0]=='run'):
    os.system(f'{cmd[1]} >> {home}/tmp/old_out')
    with open(f"{home}/tmp/old_out", "r") as out: # copied code from v0.1.4.2
      print(out.read())
  elif(cmd[0]=='clear' or cmd[0]=='cls'):
    clearscreen()
  elif(cmd[0]=='curl'):
    try:
      interpretcmd(f"run curl -s '{cmd[1]}' -O")
    except IndexError:
      spiterror('You must provide a URL for curl to get!')
  elif(cmd[0]=='exit'):
    exit()
  elif(cmd[0]=='get'):
    if(machineos!='Linux'):
      spitwarn(f'get is not designed for {machineos}. Experience may be impacted.')
    try:
      if(cmd[1]=='update'):
       getupdates()
      elif(cmd[1][0:3]=='-py'):
        previousdirectory = os.getcwd()
        changedir(f'{home}/apps/python')
        dlfilenamed(f'https://meltos.wens.cf/python/{cmd[1][4:len(cmd[1])]}.py', f'{cmd[1][4:len(cmd[1])]}.py', True)
        changedir(previousdirectory)
      else:
        previousdirectory = os.getcwd()
        changedir(f'{home}/apps/moexe')
        dlfilenamed(f'https://meltos.wens.cf/moexe/{cmd[1]}.moexe', f'{cmd[1]}.moexe', True)
        changedir(previousdirectory)
    except IndexError:
      spiterror('You must provide an argument! (-py package, package, update)')
  elif(cmd[0]=='script'):
    if(cmd[1][0:3]=='-py'):
      exec(open(cmd[1][4:len(cmd[1])]).read())
    else:
      filepath = cmd[1]
      with open(filepath) as fp:
        for index, line in enumerate(fp):
         interpretcmd(line.strip())
  else:
    try:
      if(os.path.exists(f'{home}/apps/moexe/{cmd[0]}.moexe')):
        interpretcmd(f'script {home}/apps/moexe/{cmd[0]}.moexe')
      elif(os.path.exists(f'{home}/apps/python/{cmd[0]}.py')):
        interpretcmd(f'script -py {home}/apps/python/{cmd[0]}.py')
      else:
        if(moexelist.__contains__(cmd[0])):
          spiterror(f'{cmd[0]} does not exist, but can be installed using "get {cmd[0]}"')
        elif(pythonlist.__contains__(cmd[0])):
          spiterror(f'{cmd[0]} does not exist, but can be installed using "get -py {cmd[0]}"')
        else:
          spiterror(f'{cmd[0]} does not exist!')
    except IndexError:
      pass

print(f'Welcome to MeltOS {version}.')
while True:
  tmpexists = os.path.exists(f"{home}/tmp/old_out")
  if(tmpexists):
    os.remove(f"{home}/tmp/old_out")
  try:
    inp = input(f'{color1}{os.getlogin()}&{platform.node()}{Fore.WHITE}@{color2}{os.getcwd()}{Fore.WHITE}: ')
    interpretcmd(inp)
  except KeyboardInterrupt:
    print('')
