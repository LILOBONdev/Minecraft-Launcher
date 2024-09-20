import eel,minecraft_launcher_lib,subprocess,json,re
from win10toast import *
MinecraftDerictory = minecraft_launcher_lib.utils.get_minecraft_directory()
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
    #Version = 'fabric-loader-0.16.5-1.19.4'
    print(Version)
    callback = {
        "setStatus": lambda text: print(text)
    }
    options = {
        'username': Name,
        'uuid': '',
        'token': '',
        "executablePath": "Java",
        "defaultExecutablePath": "java",
    }
    try:
        if type == 'classic':
            minecraft_launcher_lib.install.install_minecraft_version(versionid=Version,minecraft_directory=MinecraftDerictory,callback=callback)
        elif type == 'forge':
            pass
            #minecraft_launcher_lib.forge.install_forge_version(forgeVersion, MinecraftDerictory)
        elif type == 'fabric':
            print('fabric:',Version)
            Compilate = Version
            for version in minecraft_launcher_lib.utils.get_installed_versions(MinecraftDerictory):
                if re.search(version['id'],f'fabric-loader-0.16.5-{Version}'):
                    Version = f'fabric-loader-0.16.5-{Compilate}'
                    minecraft_launcher_lib.fabric.install_fabric(Compilate, MinecraftDerictory,callback=callback)
                else:
                    minecraft_launcher_lib.fabric.install_fabric(Compilate, MinecraftDerictory,callback=callback)

        subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version=Version,minecraft_directory=MinecraftDerictory,options=options))
    except Exception as ex:
        notifer = ToastNotifier()
        notifer.show_toast('Возикла ошибка при запуске',f'Ошибка: {ex}',duration=15)

for version in minecraft_launcher_lib.utils.get_installed_versions(MinecraftDerictory):
    print(version["id"])

eel.init('WebEdition')
eel.start('Embed.html',size=(1400,1400))
