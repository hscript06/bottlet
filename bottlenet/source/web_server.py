import readline
import subprocess
import os
import time
import shutil
import webbrowser
def añadir_web (ip,puerto,dominio,ruta):
    print(f"añadiendo pagina web {dominio}...")
    print(f"creando la ruta /var/www/{dominio}...")
    subprocess.run(["sudo","mkdir","-p",f"/var/www/{dominio}"])
    print(f"asignando la propiedad del directorio con la variable de entorno $USER a la ruta /var/www/{dominio}...")
    subprocess.run(["sudo","chown","-R","$USER:$USER",f"/var/www/{dominio}"])
    print(f"asignando los permisos a la ruta /var/www/{dominio}")
    subprocess.run(["sudo","chmod","-R","755"f"/var/www/{dominio}..."])
    print(f"copiando la ruta {ruta} a /var/www/{dominio}...")
    subprocess.run(["sudo","cp","-r", f"{ruta}", f"/var/www/{dominio}"])
    print(f"creando el archivo de configuracion /etc/apache2/sites-available/{dominio}.conf...")
    subprocess.run(["sudo","touch",f"/etc/apache2/sites-available/{dominio}.conf"])
    print(f"añadiendo toda la configuracion con todos los parametros. puerto:{puerto}, dominio:{dominio}...")
    contenido = f"""<VirtualHost *:{puerto}>
    ServerAdmin root@localhost
    ServerName {dominio}
    ServerAlias www.{dominio}
    DocumentRoot /var/www/{dominio}
    ErrorLog ${{{{APACHE_LOG_DIR}}}}/error.log
    CustomLog ${{{{APACHE_LOG_DIR}}}}/access.log combined
    </VirtualHost> """

    with open(f"/etc/apache2/sites-available/{dominio}.conf", "w") as f:
        f.write(contenido)
    print(f"no olvides de abilitar la zona con start {dominio}")
    while True:
        decision = input(f"¿ejecutar ahora? (s/n)").lower
        if decision == "s":
            abilitar_dominio(dominio)
        elif decision == "n":
            break
        else:
            print("decision no valida porfavor elija (s) o (n)")
def eliminar_web(dominio):
    print("¿esta seguro?, se eliminaran las siguientes carpetas/ficheros:")
    print(f"/etc/apache2/sites-available/{dominio}.conf")
    print(f"/var/www/{dominio}")
    while True:
        decision = input("(s/n)").lower
        if decision == "s":
            subprocess.run(["sudo","rm","-rf",f"/etc/apache2/sites-available/{dominio}.conf"])
            subprocess.run(["sudo","rm","-rf",f"/var/www/{dominio}"])
        elif decision == "n":
            break
        else:
            print("decision no valida porfavor elija (s) o (n)")
def reiniciar_dominio(dominio):
    deshabilitar_dominio(dominio)
    abilitar_dominio(dominio)
def abilitar_dominio(dominio):
    print(f"habilitando {dominio}.com...")
    subprocess.run("sudo","a2ensite",f"{dominio}.conf")
    print("deshabilitando la pagina por defecto...")
    subprocess.run("sudo","a2dissite","000-default.conf")
    print("reiniciando apache...")
    subprocess.run("sudo","systemctl","restart","apache2")
def deshabilitar_dominio (dominio):
    print(f"deshabilitando {dominio}")
    subprocess.run("sudo","a2dissite",f"{dominio}")
    print("reiniciando apache...")
    subprocess.run("sudo","systemctl","restart","apache2")
def comprovar_web(dominio):
    webbrowser.open(f"http://www.{dominio}.com")
def stop_server():
    subprocess.run(["sudo","systemctl","stop","apache2"])
def start_server():
    subprocess.run(["sudo","systemctl","start","apache2"])
def status_server():
    subprocess.run(["sudo","systemctl","status","apache2"])
def logs():
    subprocess.run(["sudo", "tail" ,"-f" "/var/log/apache2/access.log"])
def restart_server():
    subprocess.run(["sudo","systemctl","restart","apache2"])
def list():
    subprocess.run(["ls","/var/www/"])

def opciones():
    print("-list- listar paginas web")
    print("-help- mostrar opciones")
    print("-help list- mostrar comandos en lista")
    print("-add (puerto) (dominio) (ruta de archivo)- agregar pagina web")
    print("-rm (dominio)- eliminar pagina web")
    print("-com start (dominio)- iniciar pagina web")
    print("-stop (dominio)- deshabilitar dominio")
    print("-restart (dominio)- reiniciar dominio")
    print("-start (dominio)- iniciar dominio")
    print("-status (dominio)- estado del dominio")
    print("[serv]")
    print("|--stop- detener servidor web")
    print("|--restart- reiniciar servidor web")
    print("|--status- estado del servidor web")
    print("|--logs- ver los logs del servidor web")
    print("|--start- iniciar servidor web")
    print("-exit- salir del configurador de servidor web")
def opciones_list():
    print("-list- listar paginas web")
    print("-help- mostrar opciones")
    print("-help list- mostrar comandos en lista")
    print("-add (puerto) (dominio) (ruta de archivo)- agregar pagina web")
    print("-rm (dominio)- eliminar pagina web")
    print("-com start (dominio)- iniciar pagina web")
    print("-stop (dominio)- deshabilitar dominio")
    print("-restart (dominio)- reiniciar dominio")
    print("-start (dominio)- iniciar dominio")
    print("-status (dominio)- estado del dominio")
    print("-serv stop- detener servidor web")
    print("-serv restart- reiniciar servidor web")
    print("-serv status- estado del servidor web")
    print("-serv logs- ver los logs del servidor web")
    print("-serv start- iniciar servidor web")
    print("-exit- salir del configurador de servidor web")
def is_apache_installed():
    result = subprocess.run(
        ["dpkg", "-s", "apache2"],
        capture_output=True,
        text=True
    )
    return "install ok installed" in result.stdout

if not is_apache_installed():
    print("Apache no está instalado")
    while True:
        instalacion = input("para su usuo se necesitara instalarlo, esta de acuerdo? (s/n):").lower
        if instalacion == "s":
            subprocess.run(["sudo","apt","install","apache2","-y"], check=True)
            break
        if instalacion == "n":
            print("volviendo al inicio")
            exit()
        else:
            print("opcion no valida, ejecute (s) o (n)")
print("\n--- Menú WEB-Server ---")
print("apartado para configurar un servidor web mediante apache2")
print("para ver las opciones ejecute el comando help o help list")
def main():
    while True:
        opcion = input("\033[32mweb-server@bottlenet>>\033[0m")
        partes = opcion.split()
        if len(partes) == 1:
            if partes[0] == "list":
                os.system("ls /etc/apache2/sites-available/")
                continue
            elif partes[0] == "help":
                opciones()
                continue
            elif partes[0] == "exit":
                print("saliendo...")
                exit()
            elif partes[0] == "add":
                print("uso: add (ip) (puerto) (dominio)")
                continue
            elif partes[0] == "rm":
                print("uso: rm (dominio)")
                continue
            elif partes[0] == "com":
                print("euso: com (dominio)")
                continue
            elif partes[0] == "serv":
                print("uso: serv stop/restart/status/logs/start")
                continue
            else:
                print("❌","\033[31mopcion no valida, intente de nuevo o ejecute el comando help\033[0m")
                continue
        elif len(partes) >= 2:
            if partes[0] == "help":
                if partes[1] != "list":
                    print("uso: help list")
                elif partes [1] == "list":
                    opciones_list()
            if partes[0] == "add":
                if len(partes) < 5:
                    print("uso: add (ip) (puerto) (dominio) (ruta del archivo)")
                    continue
                else:
                    ip = partes[1]
                    puerto = partes[2]
                    dominio = partes[3]
                    ruta = partes[4]
                    añadir_web(ip, puerto, dominio, ruta)
                    continue
            if partes[0] == "rm":
                dominio = partes[1]
                eliminar_web(dominio)
                continue
            if partes [0] == "com":
                if len(partes) > 2:
                    print("uso: com (dominio)")
                    continue
                else:
                    dominio = partes [1]
                    comprovar_web(dominio)
                    continue
            if partes [0] == "serv":
                if len(partes) == 3:
                    if partes [1] == "stop":
                        dominio = partes [2]
                        stop_server(dominio)
                        continue
                    if partes [1] == "start":
                        dominio = partes[2]
                        start_server(dominio)
                        continue
                    if partes [1] == "restart":
                        dominio = partes[2]
                        restart_server(dominio)
                        continue
                    if partes [1] == "status":
                        dominio = partes[2]
                        status_server(dominio)
                        continue
                elif len(partes) == 4:
                    if partes[2] != "server":
                        print("comando no reconocido")
                        while True:
                            decision = input("quieres ver todas las conmvinaciones de serv? (s/n)").lower
                            if decision == "s":
                                print("uso:")
                                print("serv stop (dominio)- deshabilitar dominio")
                                print("serv stop server- detener servidor web")
                                print("serv restart (dominio)- reiniciar dominio")
                                print("serv restart server- reiniciar servidor web")
                                print("serv status (dominio)- estado del dominio")
                                print("serv status server- estado del servidor web")
                                print("serv logs- ver los logs del servidor web")
                                print("serv start (dominio)- iniciar dominio")
                                print("serv start server- iniciar servidor web")
                                break
                            elif decision == "n":
                                break
                            else:
                                print("no reconocido: escriba (s) o (n) porfavor")
                        continue
                    elif partes [1] == "stop":
                        subprocess.run(["sudo","systemctl","stop","apache2"])
                        continue
                    elif partes [1] == "start":
                        subprocess.run(["sudo","systemctl","start","apache2"])
                        subprocess.run(["sudo","systemctl","enable","apache2"])
                        continue
                    elif partes [1] == "restart":
                        subprocess.run(["sudo","systemctl","restart","apache2"])
                        continue
                    elif partes [1] == "status":
                        subprocess.run(["sudo","systemctl","status","apache2"])
                        continue
        else:
            print("escriba algo porfavor")    

if __name__ == "__main__":
    main()