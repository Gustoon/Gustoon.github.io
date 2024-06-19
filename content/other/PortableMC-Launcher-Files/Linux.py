import subprocess
import pyglet
import requests
import customtkinter   
import psutil
import tkinter
import platform
import os
import json
import threading
import sys
import PathMePy
import time
import configparser as cp
from tkinter import PhotoImage
from SimpleTkMessageBox import ShowMSBox
from termcolor import colored
from CTkColorPicker import *
from PIL import Image, ImageTk



if platform.system() != "Windows" and platform.system() != "Linux":
    print("This Launcher is only supported on Windows and on Linux")
    sys.exit(1)

if platform.system() == "Linux":
    print(colored("Info : ", "light_red") + colored("This launcher is less beautiful on Linux than on Windows.", "light_red"))
    time.sleep(1.5)

if not PathMePy.UserScriptFolderIsAlreadyOnPath:
    if platform.system() == "Windows":
        PathMePy.PathMePyUserScriptFolder()



if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')

print(colored("Python Launcher by Gustoon, original Java Launcher by Bricklou", "light_cyan"))

pyglet.font.add_file("./Resources/segoe-ui.ttf")

config = cp.RawConfigParser()
config.read('config.properties')

LauncherTitle = config.get('LauncherInfo', 'LauncherInfo.name').replace('||', '\n')
LauncherWindowTitle = config.get('LauncherInfo', 'LauncherInfo.name').replace("||", "")
LauncherLoginWindowTitle = LauncherWindowTitle + " Login"
LauncherTitleX = int(config.get('LauncherInfo', 'LauncherInfo.name.x'))
LauncherTitleY = int(config.get('LauncherInfo', 'LauncherInfo.name.y'))
PlaySectionButtonY = LauncherTitleY + 65
SettingsSectionButtonY = LauncherTitleY + 115


JsonUrl = config.get('ModsInfo', 'ModsInfo.JsonUrl')
VersionTxtUrl = config.get('ModsInfo', 'ModsInfo.VersionUrl')
ModsFolderUrl = config.get('ModsInfo', 'ModsInfo.ModsUrl')
ServerAdress = config.get('Server', 'Server.Adress')
ServerPort = config.get('Server', 'Server.Port')

if not os.path.exists("./Saver/"):
    os.makedirs("./Saver/")

if not os.path.exists("./Saver/connection.txt"):
    f = open("./Saver/connection.txt", 'x')
    f.close()


if not os.path.exists("./Saver/username.txt"):
    f = open("./Saver/username.txt", 'x')
    f.close()

if not os.path.exists("./MC/"):
    os.makedirs("./MC/")

if not os.path.exists("./Personal/mods/"):
    os.makedirs("./Personal/mods/")

def OfflineConnect():
    username = Username.get()
    if username.isalnum() and len(username) >= 3 and len(username) <= 16:
        Error.configure(text="", text_color="white")
        with open("./Saver/username.txt", "w") as f:
            f.write(Username.get())
            f.close()
        URl = "https://minotar.net/helm/MHF_Steve/55.png"
        response = requests.get(URl)
        open("./Saver/user.png", "wb").write(response.content)
        root.destroy()
        MainWindow()
    else :
        Error.configure(text="Error: Please enter a valid username.", text_color="red")   


def OnlineConnect():
    Error.configure(text="", text_color="white")
    email = Username.get()
    if platform.system() == "Windows":
        os.system("portablemc  --main-dir ./MC/ --work-dir ./Personal/ login " + email)
    else:
        os.system("~/.local/bin/portablemc  --main-dir ./MC/ --work-dir ./Personal/ login " + email)
    f = open("./Saver/connection.txt", 'w')
    f.write(Username.get())
    f.close()
    with open('./Personal/portablemc_auth.json', 'r') as f:
        data = json.load(f)
        f.close()
    mcusername = data['microsoft']['sessions'][email]['username']
    URl = "https://minotar.net/helm/" + mcusername + "/55.png"
    with open("./Saver/username.txt", "w") as f:
        f.write(mcusername)
        f.close()
    response = requests.get(URl)
    open("./Saver/user.png", "wb").write(response.content)
    root.destroy()
    MainWindow()


def disconnect():
    root.destroy()
    with open("./Saver/connection.txt", "w") as f:
        f.close()
    with open("./Saver/username.txt", "w") as f:
        f.close()
    try :
        os.remove("./Personal/portablemc_auth.json")
    except FileNotFoundError:
        pass
    Login()


def Login():
    fhc = open("./Saver/Hover.txt", "r+")
    hover_color = fhc.readline()
    fhc.close()
    global root
    customtkinter.set_default_color_theme("./Resources/SCraft.json")
    root = customtkinter.CTk()
    try:
        root.iconbitmap("./Resources/icon.ico")
    except:
        root.iconphoto(False, PhotoImage(file="./Resources/icon.png"))
    root.title(LauncherLoginWindowTitle)
    root.geometry("700x500")
    root.resizable(False, False)


    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    BGCanva = tkinter.Canvas(root, width=800, height=600)
    BGImage = Image.open("./Resources/BG.png")
    BGImage = BGImage.resize((800, 600))
    ShowBGImage = ImageTk.PhotoImage(BGImage)
    BGLabel = tkinter.Label(BGCanva, image=ShowBGImage)
    BGLabel.grid(row=0, column=0, sticky="nsew")
    BGCanva.grid()


    os_font = "Segoe UI"


    Ilus_image = customtkinter.CTkImage(Image.open("./Resources/icon.png"), size=(100, 100))
    Ilus_label = customtkinter.CTkLabel(master=root, image=Ilus_image, text="", bg_color="white")
    Ilus_label.place(x=50, y=5)


    Title = customtkinter.CTkLabel(master=root, text=LauncherTitle, bg_color="white", text_color="black", font=(os_font, 22))
    Title.place(x=LauncherTitleX, y=LauncherTitleY)


    UsernameText = customtkinter.CTkLabel(master=root, text="Email of account \n (username if this is a \noffline account)", bg_color="white", text_color="black", font=(os_font, 12))
    UsernameText.place(x=40, y=175)


    global Error
    Error = customtkinter.CTkLabel(master=root, bg_color="white", width=180, text="", font=(os_font, 11))
    Error.place(x=10, y=225)


    global Username
    Username = customtkinter.CTkEntry(master=root, bg_color="white", corner_radius=5, width=180, placeholder_text="Username/Email", font=(os_font, 12))
    Username.place(x=10, y=250)


    ConnectOffline = customtkinter.CTkButton(master=root, text="Connect Offline", bg_color="white", font=(os_font, 12), command=OfflineConnect, border_width=1, hover_color=hover_color)
    ConnectOffline.place(x=30, y=310)


    MSText = customtkinter.CTkLabel(master=root, text="Or, connect with a Microsoft account", bg_color="white", font=(os_font, 12))
    MSText.place(x=5, y=350)


    MSImage = Image.open("./Resources/microsoft.png")
    MSImage =  customtkinter.CTkImage(MSImage, size=(170, 45))
    ConnectMicrosoft = customtkinter.CTkButton(master=root, bg_color="white", text="", image=MSImage, width=180, command=OnlineConnect, border_width=1, hover_color=hover_color)
    ConnectMicrosoft.place(x=10, y=400)


    if os.path.getsize("./Saver/connection.txt") > 0:
        with open("./Saver/connection.txt", "r") as f:
            Username.insert(0, f.read().strip())
            f.close()
    root.mainloop()


def MainWindow():
    global root
    customtkinter.set_default_color_theme("./Resources/SCraft.json")
    root = customtkinter.CTk()
    try:
        root.iconbitmap("./Resources/icon.ico")
    except:
        root.iconphoto(False, PhotoImage(file="./Resources/icon.png"))
    root.title(LauncherWindowTitle)
    root.geometry("700x500")
    root.resizable(False, False)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    image = Image.open('./Resources/BG2.png')
    image = image.resize((700, 600))
    photo = ImageTk.PhotoImage(image)
    label = tkinter.Label(root, image=photo)
    label.place(x=0, y=0, relwidth=1, relheight=1)

    os_font = "Segoe UI"


    Ilus_image = customtkinter.CTkImage(Image.open("./Resources/icon.png"), size=(100, 100))
    Ilus_label = customtkinter.CTkLabel(master=root, image=Ilus_image, text="", bg_color="white")
    Ilus_label.place(x=50, y=5)


    Title = customtkinter.CTkLabel(master=root, text=LauncherTitle, bg_color="white", text_color="black", font=(os_font, 22))
    Title.place(x=LauncherTitleX, y=LauncherTitleY)
    with open("./Saver/username.txt", "r") as f:
        mcusername = f.readlines()
        f.close()


    Pcolor = "#3FFF5C"
    HoverColor = "light blue"


    PPlayerFrame = customtkinter.CTkFrame(master=root, fg_color=Pcolor, bg_color=Pcolor, border_width=0, corner_radius=0, width=203, height=86)
    PPlayerFrame.place(x=0, y=414)



    Player_image = customtkinter.CTkImage(Image.open("./Saver/user.png"), size=(55, 55))
    Player_label = customtkinter.CTkLabel(master=root, image=Player_image, text="", bg_color="white")
    Player_label.place(x=10, y=429)


    Player_name = customtkinter.CTkLabel(master=root, text=mcusername, bg_color=Pcolor, text_color="white", font=(os_font, 14), height=25, width=130)
    Player_name.place(x=69, y=425)



    Disconnect_image = customtkinter.CTkImage(Image.open("./Resources/logout.png"), size=(25, 25))
    Disconnect_button = customtkinter.CTkButton(master=root, image=Disconnect_image, text="", hover_color=HoverColor, fg_color=Pcolor, bg_color=Pcolor, width=26, height=26, command=disconnect)
    Disconnect_button.place(x=114, y=460)



    PlaySection_image = customtkinter.CTkImage(Image.open("./Resources/controller.png"), size=(25, 25))
    PlaySection = customtkinter.CTkButton(master=root, image=PlaySection_image, text="Play", text_color="black", bg_color="white", hover_color=HoverColor, fg_color="white", width=2, command=lambda: PlayFrame.tkraise(), font=(os_font, 12))
    PlaySection.place(x=15, y=175)


    SettingsSection_image = customtkinter.CTkImage(Image.open("./Resources/settings.png"), size=(25, 25))
    SettingsSection = customtkinter.CTkButton(master=root, image=SettingsSection_image, text="Settings", text_color="black", bg_color="white", hover_color=HoverColor, fg_color="white", width=2, command=lambda: SettingsFrame.tkraise(), font=(os_font, 12))
    SettingsSection.place(x=15, y=225)


    PlayFrame = customtkinter.CTkFrame(master=root, width=480, height=480, border_width=0, corner_radius=0)
    PlayFrame.place(x=210, y=10)


    SettingsFrame = customtkinter.CTkFrame(master=root, width=480, height=480, border_width=0, corner_radius=0)
    SettingsFrame.place(x=210, y=10)

    total_memory_gigabytes = psutil.virtual_memory().total / (1024 * 1024 * 1024)
    total_memory_gigabytes = round(total_memory_gigabytes, 1)

    i_values = []
    i = 0.5
    while i < total_memory_gigabytes:
        i_values.append(str(i) + " GB")
        i = i + 0.5

    def optionmenu_callback(choice):
        global memory_mb
        memory_gb = float(choice.split(" ")[0])
        memory_mb = round(memory_gb * 1024, 1)
        with open("./Saver/RAM.txt", "w+") as f:
            f.write(str(int(memory_mb)))
            f.close()

    RAMText = customtkinter.CTkLabel(master=SettingsFrame, text="RAM :", font=(os_font, 12))
    RAMText.place(x=120, y=10)

    combobox = customtkinter.CTkOptionMenu(master=SettingsFrame, values=i_values, command=optionmenu_callback, font=(os_font, 12))
    combobox.place(x=170, y=10)

    ColorText = customtkinter.CTkLabel(master=SettingsFrame, text="Color : ", font=(os_font, 30))
    ColorText.place(x=10, y=100)


    def HoverBTN() :
        with open("./Saver/Hover.txt") as f:
            aHover = f.readline()
            f.close()
        hover_color = None
        Hover_pick_color = AskColor()
        hover_color = Hover_pick_color.get()
        while hover_color == None :
            hover_color = aHover
        with open("./Saver/Hover.txt", "w+") as f:
            f.write(hover_color)
            f.close()
        ActualHoverColor.configure(text="Actual color : " + hover_color)
        HoverColorBTN.configure(fg_color=hover_color, hover_color=hover_color)
        Disconnect_button.configure(hover_color=hover_color)
        PlaySection.configure(hover_color=hover_color)
        PlayButton.configure(hover_color=hover_color)
        SettingsSection.configure(hover_color=hover_color)
        ReturnHoverColorBTN.configure(hover_color=hover_color)
        ReturnframeColorBTN.configure(hover_color=hover_color)
        ShowLogBTN.configure(hover_color=hover_color)
        combobox.configure(button_hover_color=hover_color)



    HoverColorBTN = customtkinter.CTkButton(master=SettingsFrame, text="hover", width=74, height=50, border_width=3, font=(os_font, 12), command=HoverBTN, corner_radius=0, border_color="dark gray")
    HoverColorBTN.place(x=20, y=150)

    ActualHoverColor = customtkinter.CTkLabel(master=SettingsFrame, text="Actual color : light blue", font=(os_font, 12))
    ActualHoverColor.place(x=102, y=145)


    def ReturnHoverColorToDefault() :
        with open("./Saver/Hover.txt", "r+") as f:
            f.write("light blue")
            f.close()
        ActualHoverColor.configure(text="Actual color : light blue")
        PlaySection.configure(hover_color="light blue")
        SettingsSection.configure(hover_color="light blue")
        Disconnect_button.configure(hover_color="light blue")
        PlayButton.configure(hover_color="light blue")
        ReturnHoverColorBTN.configure(hover_color="light blue")
        ReturnframeColorBTN.configure(hover_color="light blue")
        ShowLogBTN.configure(hover_color="light blue")
        HoverColorBTN.configure(hover_color="light blue", fg_color="light blue")
        combobox.configure(button_hover_color="light blue")


    ReturnHoverColorBTN = customtkinter.CTkButton(master=SettingsFrame, text="Return color to default", width=60, command=ReturnHoverColorToDefault, font=(os_font, 12), border_width=1)
    ReturnHoverColorBTN.place(x=100, y=170)


    def frameBTN() :
        with open("./Saver/frame.txt") as f:
            aFrame = f.readline()
            f.close()
        frame_color = None
        frame_pick_color = AskColor()
        frame_color = frame_pick_color.get()
        while frame_color == None :
            frame_color = aFrame
        with open("./Saver/frame.txt", "w+") as f:
            f.write(frame_color)
            f.close()
        ActualframeColor.configure(text="Actual color : " + frame_color)
        frameColorBTN.configure(fg_color=frame_color, hover_color=frame_color)
        PPlayerFrame.configure(fg_color=frame_color, bg_color=frame_color)
        Player_name.configure(fg_color=frame_color, bg_color=frame_color)
        Disconnect_button.configure(fg_color=frame_color, bg_color=frame_color)

    
    frameColorBTN = customtkinter.CTkButton(master=SettingsFrame, text="frame", width=74, height=50, border_width=3, font=(os_font, 12), command=frameBTN, corner_radius=0, border_color="dark gray")
    frameColorBTN.place(x=255, y=150)


    ActualframeColor = customtkinter.CTkLabel(master=SettingsFrame, text="Actual color : light blue", font=(os_font, 12))
    ActualframeColor.place(x=337, y=145)


    def ReturnframeColorToDefault() :
        with open("./Saver/frame.txt", "r+") as f:
            f.write("#3FFF5C")
            f.close()
        ActualframeColor.configure(text="Actual color : #3FFF5C")
        frameColorBTN.configure(hover_color="#3FFF5C", fg_color="#3FFF5C")
        PPlayerFrame.configure(fg_color="#3FFF5C", bg_color="#3FFF5C")
        Player_name.configure(fg_color="#3FFF5C", bg_color="#3FFF5C")
        Disconnect_button.configure(fg_color="#3FFF5C", bg_color="#3FFF5C")
    ReturnframeColorBTN = customtkinter.CTkButton(master=SettingsFrame, text="Return color to default", width=60, command=ReturnframeColorToDefault, font=(os_font, 12), border_width=1)
    ReturnframeColorBTN.place(x=335, y=170)


    def OpenLog():
        if not os.path.exists("./Personal/logs/"):
            ShowMSBox(master=SettingsFrame, Title="Log folder error", text="There is no folder for logs. Maybe because\nyou didn't start the game?", button1="OK", IconStyle="Windows 11", Icon='Error')
        else :
            logpath = os.path.abspath("./Personal/logs/")
            if platform.system() == "Windows":
                subprocess.Popen(["explorer", logpath])
            else:
                os.system("open ./Personal/logs")

    ShowLogBTN = customtkinter.CTkButton(master=SettingsFrame, text="Show log folder", font=(os_font, 12), command=OpenLog, border_width=1)
    ShowLogBTN.place(x=175, y=420)

    Info = customtkinter.CTkLabel(master=PlayFrame, text="")
    Info.place(x=180, y=5)


    ProgressBar = customtkinter.CTkProgressBar(master=PlayFrame, width=400)
    ProgressBar.place(x=40, y=40)
    ProgressBar.set(0)


    def Play():
        ProgressBar.set(0)
        Disconnect_button.configure(state='disabled')
        PlaySection.configure(state='disabled')
        SettingsSection.configure(state='disabled')
        PlayButton.configure(state='disabled')
        Json_url = JsonUrl
        print("Downloading JSON file from " + Json_url)
        jsonResponse = requests.get(Json_url)
        print("Download completed with status " + str(jsonResponse.status_code))
        open("mods.json", "wb").write(jsonResponse.content)
        json_file_path = "./mods.json"
        VersionUrl = VersionTxtUrl
        print("Downloading file with version name from " + VersionUrl)
        VersionResponse = requests.get(VersionUrl)
        print("Download completed with status " + str(VersionResponse.status_code))
        open("Version.txt", "wb").write(VersionResponse.content)
        mods_url = ModsFolderUrl
        with open(json_file_path, "r") as json_file:
            json_obj = json.load(json_file)
        local_mods_path = os.path.abspath("./Personal/mods/")
        print("Mods will be saved in " + local_mods_path)
        total = sum(len(value) for value in json_obj.values())
        count = 0
        Info.configure(text="Downloading mods...")
        for value in json_obj.values():
            for element in value:
                local_file_path = os.path.join(local_mods_path, element)
                if not os.path.isfile(local_file_path):
                    print(element + " does not exist, downloading...")
                    response = requests.get(mods_url + element)
                    print("Download completed with status " + str(response.status_code))
                    with open(local_file_path, "wb") as f:
                        f.write(response.content)
                        f.close()
                    count += 1
                    ProgressBar.set(count / total)
                    root.update_idletasks()
                else:
                    count += 1
                    ProgressBar.set(count / total)
                    root.update_idletasks()
                    print(element + " already exists at " + local_file_path)
        for filename in os.listdir(local_mods_path):
            local_file_path = os.path.join(local_mods_path, filename)
            if not any(filename == element for value in json_obj.values() for element in value):
                print(filename + " is not present in the JSON, deleting...")
                os.remove(local_file_path)
            else:
                print(filename + " exists at " + local_file_path)
        Info.configure(text="Starting the game...")
        with open("Version.txt", "r+") as f:
            version = f.readline()
            f.close()
        with open("./Saver/RAM.txt", "r+") as f:
            MCRam = f.readline()
            f.close()
        if ServerAdress != None:
            if os.path.getsize("./Saver/connection.txt") == 0:
                with open("./Saver/username.txt", "r+") as f:
                    MCUsername = f.readline()
                    f.close()
                os.system('~/.local/bin/portablemc --main-dir ./MC/ --work-dir ./Personal/ start -s "' + ServerAdress + '" -p "' + ServerPort + '" --jvm-args="-Xmx' + str(int(MCRam)) + "M -Xms" + str(int(MCRam)) + 'M" --username ' + MCUsername + " " + version)
            else:
                with open("./Saver/connection.txt", "r+") as f:
                    MCLogin = f.readline()
                    f.close()
                os.system('~/.local/bin/portablemc --main-dir ./MC/ --work-dir ./Personal/ start -s "' + ServerAdress + '" -p "' + ServerPort + '" --jvm-args="-Xmx' + str(int(MCRam)) + "M -Xms" + str(int(MCRam)) + 'M" -l ' + MCLogin + " " + version)
        else:
            if os.path.getsize("./Saver/connection.txt") == 0:
                with open("./Saver/username.txt", "r+") as f:
                    MCUsername = f.readline()
                    f.close()
                os.system('~/.local/bin/portablemc --main-dir ./MC/ --work-dir ./Personal/ start --jvm-args="-Xmx' + str(int(MCRam)) + "M -Xms" + str(int(MCRam)) + 'M" --username ' + MCUsername + " " + version)
            else:
                with open("./Saver/connection.txt", "r+") as f:
                    MCLogin = f.readline()
                    f.close()
                os.system('~/.local/bin/portablemc --main-dir ./MC/ --work-dir ./Personal/ start --jvm-args="-Xmx' + str(int(MCRam)) + "M -Xms" + str(int(MCRam)) + 'M" -l ' + MCLogin + " " + version)
        PlaySection.configure(state='normal')
        SettingsSection.configure(state='normal')
        PlayButton.configure(state='normal')
        Disconnect_button.configure(state='normal')
        ProgressBar.set(0)
        Info.configure(text="")
    def startPlayThread():
        Playthread = threading.Thread(target=Play)
        Playthread.start()
    PlayButtonImage = customtkinter.CTkImage(Image.open("./Resources/play.png"))
    PlayButton = customtkinter.CTkButton(master=PlayFrame, image=PlayButtonImage, text="Play!", command=startPlayThread, border_width=1)
    PlayButton.place(x=170, y=70)


    with open("./Saver/RAM.txt", "r+") as f:
        ram = int(f.readline()) / 1024
        combobox.set(str(ram) + " GB")
        f.close()

    with open("./Saver/Hover.txt", "r+") as f:
        hover_color = f.readline()
        ActualHoverColor.configure(text="Actual color : " + hover_color)
        HoverColorBTN.configure(fg_color=hover_color, hover_color=hover_color)
        Disconnect_button.configure(hover_color=hover_color)
        PlaySection.configure(hover_color=hover_color)
        SettingsSection.configure(hover_color=hover_color)
        PlayButton.configure(hover_color=hover_color)
        ReturnHoverColorBTN.configure(hover_color=hover_color)
        ReturnframeColorBTN.configure(hover_color=hover_color)
        ShowLogBTN.configure(hover_color=hover_color)
        combobox.configure(button_hover_color=hover_color)
        f.close()

    with open("./Saver/frame.txt", "r+") as f:
        frame_color = f.readline()
        ActualframeColor.configure(text="Actual color : " + frame_color)
        frameColorBTN.configure(hover_color=frame_color, fg_color=frame_color)
        PPlayerFrame.configure(fg_color=frame_color, bg_color=frame_color)
        Player_name.configure(fg_color=frame_color, bg_color=frame_color)
        Disconnect_button.configure(fg_color=frame_color, bg_color=frame_color)
        f.close()

    PlayFrame.tkraise()
    root.mainloop()


if not os.path.exists("./Saver/RAM.txt") :
    with open("./Saver/RAM.txt", "w+") as f:
        f.write("3072")
        f.close()

if not os.path.exists("./Saver/Hover.txt") :
    with open("./Saver/Hover.txt", "w+") as f:
        f.write("light blue")
        f.close()

if not os.path.exists("./Saver/frame.txt") :
    with open("./Saver/frame.txt", "w+") as f:
        f.write("#3FFF5C")
        f.close()

if not os.path.getsize("./Saver/username.txt") > 0:
    Login()
else :
    MainWindow()