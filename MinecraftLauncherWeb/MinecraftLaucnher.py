import eel,minecraft_launcher_lib,subprocess,json
from win10toast import *
from time import sleep
with open('WebEdition/json/Data.json','r') as UserData:
    p = json.load(UserData)
@eel.expose #Check User Data
def CheckUser():
    if p['User']['Registrable'] == 'true':
        return p['User']['Name']
    elif p['User']['Registrable'] == 'true' or p['User']['Name'] == '0':
        return 'unlog'
    else:
        return 'unlog'

@eel.expose #Reg User
def RegUser(Name):
    p['User']['Registrable'] = 'true'
    with open('WebEdition/json/Data.json','w') as UserData:
        json.dump(p,UserData,indent=4)

    p['User']['Name'] = Name
    with open('WebEdition/json/Data.json','w') as UserData:
        json.dump(p,UserData,indent=4)

@eel.expose #StartGame Java Minecraft
def PlayMinecraft(Name,Version,type):
    callback = {
        "setStatus": lambda text: print(text)
    }
    options = {
        'username': Name,
        "executablePath": "Java",
        "defaultExecutablePath": "java",
    }
    try:
        MinecraftDerictory = minecraft_launcher_lib.utils.get_minecraft_directory()
        if type == 'classic':
            minecraft_launcher_lib.install.install_minecraft_version(versionid=Version,minecraft_directory=MinecraftDerictory,callback=callback)
        elif type == 'forge':
            pass
            #minecraft_launcher_lib.forge.install_forge_version(forgeVersion, MinecraftDerictory)
        elif type == 'fabric':
            minecraft_launcher_lib.fabric.install_fabric(Version, MinecraftDerictory)
        subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version=Version,minecraft_directory=MinecraftDerictory,options=options))
    except Exception as ex:
        notifer = ToastNotifier()
        notifer.show_toast('Возикла ошибка при запуске',f'Ошибка: {ex}',duration=15)

eel.init('WebEdition')
eel.start('Embed.html',size=(1400,1400))