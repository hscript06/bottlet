import subprocess
import os
import time
import readline
import sys

if os.geteuid() != 0:
    print("\033[31m❌ Debes ejecutar este script como superusuario (root). Usa 'sudo python3 script.py'\033[0m")
    sys.exit(1)

script_dir = os.path.dirname(os.path.abspath(__file__))
ip_script = os.path.join(script_dir, "source/ip.py")
dns_script = os.path.join(script_dir, "source/dns.py")
dns_server_script = os.path.join(script_dir, "source/dns_server.py")
web_server_script = os.path.join(script_dir, "source/web_server.py")
server_smb = os.path.join(script_dir, "source/server_smb.py")
server_nfs = os.path.join(script_dir, "source/server_nfs.py")
def flujo():
    if subprocess.call(["which", "iftop"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
        print("\033[33miftop no está instalado. Instalando...\033[0m")
        subprocess.run(["apt", "update"])
        subprocess.run(["apt", "install", "iftop", "-y"])
    print("\033[32mSe mostrará el flujo de conexiones en 3 segundos (Ctrl+C para salir)\033[0m")
    for i in range(3, 0, -1):
        print(f"{i}   ", end='\r', flush=True)
        time.sleep(1)
    print("    ", end='\r', flush=True)  # Limpia la línea
    try:
        subprocess.run(["iftop", "-n"])
    except KeyboardInterrupt:
        print("\n\033[33mVolviendo al menú Bottlenet...\033[0m")
def opciones():
    print("-help- mostrar opciones")
    print("-exit- salir")
    print("[if]- informacion")
    print("|--ip- ver las ips de los adaptadores de red")
    print("|--dns- ver las dns configuradas")
    print("|--flujo- ver el flujo de conexiones a los servicios")
    print("|--bottlenet- informacion del script")
    print("[config] configuraciones")
    print("|--ip- cambiar ip de un adaptador de red y su submascara")
    print("|--dns- configurar dns")
    print("[serv] servidores")
    print("|--dns- servidor dns")
    print("|--web- servidor web")
    print("|--smb- servidor samba")
    print("|--nfs- servidor nfs")
print("--- Bienvenido a Bottlenet ---")
print("Un script pensado para configurar servidores Debian (de momento)")
print("para ver las opciones ejecute el comando help")
try:
    while True:
        eleccion = input("\033[32mhome@bottlenet>>\033[0m")
        partes = eleccion.split()
        if len(partes) == 1:
            if partes[0] == "if":
                print("\033[31mespecifique que informacion desea ver: ip/dns/flujo/bottlenet\033[0m")
                continue
            elif partes[0] == "config":
                print("especifique que desea configurar: ip/dns")
                continue
            elif partes[0] == "serv":
                print("especifique que servidor desea configurar: dns/web/smb/nfs")
                continue
            elif partes[0] == "help":
                opciones()
                continue
            elif partes[0] == "exit":
                print("saliendo...")
                exit()
        if len(partes) == 2:
            if partes[0] == "if":
                if partes[1] == "ip":
                    subprocess.run(["ip", "a"])
                    continue
                elif partes[1] == "dns":
                    subprocess.run(["cat", "/etc/resolv.conf"])
                    continue
                elif partes[1] == "flujo":
                    flujo()
                    continue
                elif partes[1] == "bottlenet":
                    print("Bottlenet version 1.0")
                    print("bottlenet es un script de codigo abierto para configurar servidores basicos")
                    print("cualquier duda, sugerencia o peticion puede abrir el repositorio de github")
                    print("Repositorio: sin especificar aun")
                    continue
                else:
                    print("\033[31mespecifique que informacion desea ver: ip/dns/flujo/bottlenet\033[0m")
                    continue
            if partes[0] == "config":
                if partes[1] == "ip":
                    subprocess.run(["sudo","python3", ip_script])
                    continue
                elif partes[1] == "dns":
                    subprocess.run(["sudo","python3", dns_script])
                    continue
                else:
                    print("\033[31mespecifique que desea configurar: ip/dns\033[0m")
                    continue
            if partes[0] == "serv":
                if partes[1] == "dns":
                    subprocess.run(["sudo","python3", dns_server_script])
                    continue
                elif partes[1] == "web":
                    subprocess.run(["sudo","python3", web_server_script])
                    continue
                elif partes[1] == "smb":
                    print("⚠️ esta opcion esta en desarrollo ⚠️")
                    #subprocess.run(["python3", server_smb])
                    continue
                elif partes[1] == "nfs":
                    print("⚠️ esta opcion esta en desarrollo ⚠️")
                    #subprocess.run(["python3", server_nfs])
                    continue
                else:
                    print("\033[31mespecifique que servidor desea configurar: dns/web/smb/nfs\033[0m")
                    continue
            else:
                print("❌","\033[31mopcion no valida, intente de nuevo o ejecute el comando help\033[0m")
                continue
        else:
            print("❌","\033[31mopcion no valida, intente de nuevo o ejecute el comando help\033[0m")
            continue
except KeyboardInterrupt:
    exit
