import tkinter as tk
from tkinter import ttk
from json import loads
import urllib.request, sys, zipfile, psutil
from pathlib import Path
from shutil import rmtree, copytree
from subprocess import Popen
from time import sleep

with open(Path('steam_path.txt'), 'r') as file:
    path = file.readline()

steamPath = path
# steam_path = 'C:/Program Files (x86)/Steam'

with urllib.request.urlopen("https://raw.githubusercontent.com/TreeWall/AmongUs-TOUMira-Launcher/main/versions1.json") as response:
    data_str = response.read().decode('utf-8')
    versions = loads(data_str)

prelink = "https://github.com/AU-Avengers/TOU-Mira/releases/download/"

def steamRunning():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'steam.exe' in proc.info['name'].lower():
            return True
    return False

def AUrunning():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'among us.exe' in proc.info['name'].lower():
            return True
    return False

def ensureSteam():
    while not steamRunning():
        sleep(1)
    setConsoleText("Steam is now running - launching game...")

def checkDownloadedZips(path):
    fPath = Path(path)
    zip_files = [f.stem for f in fPath.iterdir() if f.is_file() and f.suffix == ".zip"]
    return zip_files

def checkFolder(path, subpath):
    folder_path = Path(path)
    subfolder_name = subpath

    subfolder_path = folder_path / subfolder_name
    return subfolder_path.is_dir()

def deleteFiles(path):
    fPath = Path(path)
    for item in fPath.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            rmtree(item)

def getZip(ver):
    dVer = checkDownloadedZips("instances")
    if ver not in dVer:
        urllib.request.urlretrieve(prelink + versions[ver], f'instances/{ver}.zip')
        setConsoleText(f'{ver} downloaded!')
    else:
        setConsoleText(f'{ver} already downloaded')

def extractZip(ver):
    if not checkFolder("cinstance", ver):
        deleteFiles("cinstance")
        with zipfile.ZipFile(f'instances/{ver}.zip', 'r') as zip:
            zip.extractall(f'cInstance/{ver}')
        setConsoleText("Zip extracted!")
    else:
        setConsoleText("Zip already extracted")

def constructGame(ver):
    base_dir = Path(f'cinstance/{ver}')
    src = next(base_dir.iterdir())
    dst = "Among Us Mira TOU"
    deleteFiles(dst)
    copytree(src, Path(dst), dirs_exist_ok=True)

    copytree(Path(f'{steamPath}/steamapps/common/Among Us'), Path(dst), dirs_exist_ok=True)

def launchGame():
    game_path = Path("Among Us Mira TOU/Among Us.exe")
    steam_path = Path(f'{steamPath}/Steam.exe')
    if not steamRunning():
        setConsoleText("Steam not running\nStarting Steam...")
        Popen(steam_path)
        ensureSteam()
    Popen(game_path)

def GameLauncher(pull):
    if not AUrunning():
        getZip(pull)
        extractZip(pull)
        constructGame(pull)
        launchGame()
        setConsoleText("Game Launched!")
    else:
        setConsoleText("Another instance of the game is already running!")

def setConsoleText(text):
    global consoleTxt
    consoleTxt.set(text)
    console.update()

version = "v1.0.0"

with urllib.request.urlopen("https://raw.githubusercontent.com/TreeWall/AmongUs-TOUMira-Launcher/main/versions1.json") as response:
    data_str = response.read().decode('utf-8')
    AUversions = loads(data_str)

with urllib.request.urlopen("https://raw.githubusercontent.com/TreeWall/AmongUs-TOUMira-Launcher/main/oldVer1.txt") as response:
    data_str2 = response.read().decode('utf-8')

AUverKeys = list(AUversions.keys())

keys = data_str2.strip().split('\n')

root = tk.Tk()
AmongUs_version = tk.StringVar()
consoleTxt = tk.StringVar(value="Launching the game may take time. Be patient.")

root.geometry("400x210")
root.resizable(width=False, height=False)
root.title(f'Among Us TOU - Mira Launcher {version}')
root.iconbitmap("logo.ico")

Header = tk.Label(root, text="Among Us TOU MIRA Launcher", font=("Arial", 20))
verSelect = tk.Label(root, text="Select TOU-Mira version:", font=("Arial", 10))

dropdown = ttk.Combobox(root, textvariable=AmongUs_version)
dropdown['values'] = (keys)
dropdown.current(0)
dropdown.state(["readonly"])

console = tk.Label(root, textvariable=consoleTxt, font=("Arial", 10))
launch = tk.Button(root, text="Launch!", font=("Arial", 18), command=lambda: GameLauncher(AUverKeys[keys.index(AmongUs_version.get())]))
note1 = tk.Label(root, text="Note: Versions marked with * may not work on the lastest release\n of Among Us", font=("Arial", 10))

Header.place(x=200, y=25, anchor="center")
verSelect.place(x=0, y=50)
dropdown.place(x=160, y=50)
console.place(x=200, y=95, anchor="center")
launch.place(x=200, y=140, anchor="center")
note1.place(x=0, y=170)

root.mainloop()