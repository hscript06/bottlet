import os
import subprocess
import time
import readline

def agregar_dns(dominio, ip_dns):
    #while True:
    #    print("introduce el dominio (ejemplo.com):")
    #    dominio = input("server@dns/add>>")
    #    if dominio == "back":
    #        break
    #    elif dominio == "exit":
    #        exit()
    #    else:
    #        while True:
    #            print("Introduce la IP del servidor DNS: ")
    #            ip_dns = input(f"server@dns/add/{dominio}>>")
    #            if ip_dns == "back":
    #                break
    #            elif ip_dns == "exit":
    #                exit()
    #            else:
    #                print(f"server@dns/add/{dominio}/{ip_dns}>> agregando DNS...")
    #                break
    #            break
    #        break
    bind_exists = os.path.isdir("/etc/bind")
    if not bind_exists:
        print("bind9 no está instalado. Instalando...")
        time.sleep(1)
        subprocess.run(["sudo","apt","install","bind9","-y"])
        time.sleep(1)
    # Crear la carpeta de zonas si no existe
    zonas_dir = "/etc/bind/zones"
    if not os.path.isdir(zonas_dir):
        print("creando la ")
        subprocess.run(["sudo", "mkdir", "-p", zonas_dir])
    zona_path = f"{zonas_dir}/db.{dominio}"
    subprocess.run(["sudo", "touch", zona_path])
    contenido = f"""$TTL    604800
@       IN      SOA     dns.{dominio}. admin.{dominio}. (
                  3     ; Serial
             604800     ; Refresh
              86400     ; Retry
            2419200     ; Expire
             604800 )   ; Negative Cache TTL
;
@       IN      NS      dns.{dominio}.
dns.{dominio}.    IN      A       {ip_dns}
"""
    with open(zona_path, "w") as f:
        f.write(contenido)
    print(f"Zona creada en {zona_path}")
    print(f"\033[32mañadido por defecto el servidor dns.{dominio}, si desea cambiarlo edite el archivo manualmente en {zona_path}\033[0m")
    print("habilitando la zona en /etc/bind/named.conf.local...")
    with open("/etc/bind/named.conf.local", "a") as f:
        f.write(f'\nzone "{dominio}" {{\n    type master;\n    file "/etc/bind/zones/db.{dominio}";\n}};\n')
    print("reiniciando bind9...")
    subprocess.run(["sudo","systemctl","restart","bind9"])

def quitar_dns(dominio):
#    while True:
#        print(" introduce el dominio (ejemplo.com):")
#        dominio = input("server@dns/remove_domain>>")
#        if dominio == "back":
#            break
#        elif dominio == "exit":
#            exit()
#        else:
    subprocess.run(["sudo", "rm","-rf", f"/etc/bind/zones/db.{dominio}"])
#            break
    print(f"Zona db.{dominio} eliminada.")
    print("eliminando la zona de /etc/bind/named.conf.local...")
    with open("/etc/bind/named.conf.local", "r") as f:
        lineas = f.readlines()
    with open("/etc/bind/named.conf.local", "w") as f:
        skip = False
        for linea in lineas:
            if f'zone "{dominio}"' in linea:
                skip = True
            if not skip:
                f.write(linea)
            if skip and '};' in linea:
                skip = False
    print("reiniciando bind9...")
    subprocess.run(["sudo","systemctl","restart","bind9"])

def quitar_ip_zona(dominio):
#    while True:
#        print("introduce el dominio (ejemplo.com):")
#        dominio = input("server@dns/remove_ip>>")
#        if dominio == "back":
#            break
#        elif dominio == "exit":
#            exit()
#        else:
            print("para quitar una ip de una zona debe editar el archivo manualmente")
            print("vera una linea similar a esta: www.ejemplo.com.    IN      A     192.168.x.x")
            print(f"abriendo el archivo db.{dominio} en 3 segundos (Ctrl+X para salir)")
            for i in range(3, 0, -1):
                print(f"{i}   ", end='\r', flush=True)
                time.sleep(1)
            print("    ", end='\r', flush=True)
            try:
                subprocess.run(["sudo","nano",f"/etc/bind/zones/db.{dominio}"])
            except KeyboardInterrupt:
                print("\n\033[33mVolviendo al menú Bottlenet...\033[0m")
#            break

def agregar_ip_zona(servicio, ip_servicio, dominio):
#    while True:
#        print("introduce el dominio (ejemplo.com):")
#        dominio = input("server@dns/add.ip>>")
#        if dominio == "back":
#            break
#        elif dominio == "exit":
#            exit()
#        else:
#            print("Introduce el servicio (ejemplo: www -> [www.domminio.com]):")               
#            servicio = input(f"server@dns/add.ip/{dominio}>>")
#            if servicio == "back":
#                break
#            elif servicio == "exit":
#                exit()
#            else:
#                print("Introduce la IP del servicio:") 
#                ip_servicio = input(f"server@dns/add.ip/{servicio}.{dominio}>>")
#                if ip_servicio == "back":
#                    break
#                elif ip_servicio == "exit":
#                    exit()
#                else:
#                    print(f"server@dns/add.ip/{servicio}.{dominio}/{ip_servicio}>> agregando ip a zona...")
#                    break
#            break
    print(f"agregando {servicio}.{dominio} con la ip {ip_servicio} a la zona db.{dominio}...")
    with open(f"/etc/bind/zones/db.{dominio}", "a") as f:
        f.write(f"{servicio}.{dominio}.    IN      A       {ip_servicio}\n")
def comprovar_ip_dns(ip_dns):
#    print(" Introduce la IP del DNS a comprobar:")
#    ip_dns = input("server@dns/check_ip>>")
#    while True:
#        if ip_dns == "back":
#            break
#        elif ip_dns == "exit":
#            exit()
#        else:
            os.system(f"nslookup {ip_dns}")
#        break
def comprovar_dominio_dns(dominio):
#    print(" Introduce el dominio a comprobar:")
#    dominio = input("server@dns/check_domain>>")
#    while True:
#        if dominio == "back":
#            break
#        elif dominio == "exit":
#            exit()
#        else:
            os.system(f"nslookup {dominio}")
#        break
def listar_zonas():
    zonas_dir = "/etc/bind/zones"
    if os.path.isdir(zonas_dir):
        zonas = os.listdir(zonas_dir)
        if zonas:
            print("Zonas disponibles:")
            for zona in zonas:
                print(f"- {zona}")
        else:
            print("No hay zonas disponibles.")
    else:
        print("El directorio de zonas no existe.")
def opciones():
    print("exit- volver al inicio")
    print("list- listado de zonas")
    print("help- mostrar opciones")
    print("help list- te muestra todas los comandos disponibles en un listado")
    print("[add]- Agregar")
    print("|--dns (ejemplo.com) (ip-servidor)- agregar dns")
    print("|--ip (www) (ejemplo.com) (ip-servicio)- Agregar ip a zona")
    print("[remove]- quitar")
    print("|--dns (dominio)- Quitar DNS")
    print("|--ip (dominio)- Quitar ip de zona")
    print("[com]- comprobar") 
    print("|--ip (ip)- comprobar dns por ip")
    print("|--dom (dominio)- comprobar dns por dominio")
    print("[serv]- comandos del servidor")
    print("|--stop (dominio)- detener servidor dns")
    print("|--restart (dominio)- reiniciar servidor dns")
    print("|--status (dominio)- estado del servidor dns")
    print("|--logs (dominio)- ver los logs del servidor dns")
    print("|--start (dominio)- iniciar servidor web")
print("\n--- Menú DNS-Server ---")
print("apartado para configurar un servidor dns mediante bind9")
print("para ver las opciones ejecute el comando help")
def main():
    while True:
        opcion = input("\033[32mserver@dns>>\033[0m")
        partes = opcion.split()
#1 parte
        if len(partes) == 1:
            if partes[0] == "add":
                print("especifique que desea agregar: dns/ip")
                continue
            elif partes[0] == "remove":
                print("especifique que desea quitar: dns/ip")
                continue
            elif partes[0] == "com":
                print("especifique que desea comprobar: ip/dom")
                continue
            elif partes[0] == "list":
                listar_zonas()
                continue
            elif partes[0] == "back":
                print("volviendo al menu principal...")
                time.sleep(0.5)
                break
            elif partes[0] == "help":
                opciones()
                continue
            elif partes[0] == "exit":
                print("Saliendo...")
                time.sleep(0.5)
                exit()
        if len(partes) >= 2:
            if partes[0] == "serv":
                if len(partes) != 2:
                    print("uso: serv stop/restart/status/logs/start")
                    continue
                if partes[1] == "stop":
                    print(f"deteniendo bind9...")
                    subprocess.run(["sudo","systemctl","stop","bind9"])
                    continue
                elif partes[1] == "restart":
                    print(f"reiniciando bind9...")
                    subprocess.run(["sudo","systemctl","restart","bind9"])
                    continue
                elif partes[1] == "status":
                    subprocess.run(["sudo","systemctl","status","bind9"])
                    continue
                elif partes[1] == "logs":
                    subprocess.run(["sudo","journalctl","-u","bind9","-e"])
                    continue
                elif partes[1] == "start":
                    print(f"iniciando bind9...")
                    subprocess.run(["sudo","systemctl","start","bind9"])
                    continue
                else:
                    print("uso: serv stop/restart/status/logs/start (dominio)")
                    continue
            if partes[0] == "help" and partes[1] == "list":
                print("-exit- volver al inicio")
                print("-list- listado de zonas")
                print("-help- mostrar opciones")
                print("-help list- te muestra todas los comandos disponibles en un listado")
                print("-add dns (ejemplo.com) (ip-servidor)- agregar dns")
                print("-add ip (www) (ejemplo.com) (ip-servicio)- Agregar ip a zona")
                print("-remove dns (dominio)- Quitar DNS")
                print("-remove ip (dominio)- Quitar ip de zona")
                print("-com ip (ip)- comprobar dns por ip")
                print("-com dom (dominio)- comprobar dns por dominio")
            if partes[0] == "add":
                if partes[1] == "dns":
                    if len(partes) != 4:
                        print("uso: add dns (ejemplo.com) (ip-servidor)")
                        continue
                    dominio = partes[2]
                    ip_dns = partes[3]
                    agregar_dns(dominio, ip_dns)
                    continue
                elif partes[1] == "ip":
                    if len(partes) != 5:
                        print("uso: add ip (www) (ejemplo.com) (ip-servicio)")
                        continue
                    servicio = partes[2]
                    ip_servicio = partes[3]
                    dominio= partes[4]
                    agregar_ip_zona(servicio, ip_servicio, dominio)
                    continue
                else:
                    print("uso: add dns (ejemplo.com) (ip-servidor) o add ip (www) (ejemplo.com) (ip-servicio)")
                    continue
            elif partes[0] == "remove":

                if partes[1] == "dns":
                    if len(partes) != 3:
                        print("uso: remove dns (dominio)")
                        continue
                    dominio = partes[2]
                    quitar_dns(dominio)
                    continue
                if partes[1] == "ip":
                    if len(partes) != 3:
                        print("uso: remove ip (dominio)")
                        continue
                    dominio = partes[2]
                    quitar_ip_zona(dominio)
                    continue
                else:
                    print("uso: remove dns/ip (dominio)")
                    continue
            elif partes[0] == "com":
                if partes[1] == "ip":
                    if len(partes) != 3:
                        print("uso: com ip (ip)")
                        continue
                    ip_dns = partes[2]
                    comprovar_ip_dns(ip_dns)
                    continue
                elif partes[1] == "dom":
                    if len(partes) != 3:
                        print("uso: com dom (dominio)")
                        continue
                    dominio = partes[2]
                    comprovar_dominio_dns(dominio)
                    continue
                else:
                    print("uso: com ip/dom (ip o dominio)")
                    continue
        else:
            print("❌","\033[31mopcion no valida, intente de nuevo o ejecute el comando h\033[0m")

if __name__ == "__main__":
    main()