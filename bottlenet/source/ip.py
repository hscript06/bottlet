import os
import subprocess
import readline

script_dir = os.path.dirname(os.path.abspath(__file__))
script_inicio = os.path.join(script_dir, "script.py")

print(" -- cambiar ip -- ")
print("en cualquier momento de la configuracion puede volber atras con el comando back y para volver al inicio con exit")
print("1- estatica")
print("2- dhcp")
while True:
    tipo_ip = input(">>")
    if tipo_ip == "1":
        while True:
            print("adaptador de red:")
            adaptador = input("static@ip>>")
            if adaptador == "back":
                break
            elif adaptador == "exit":
                exit()
            else:
                while True:
                            
                    print("ip:")
                    ip = input(f"{adaptador}@ip>>")
                    if ip == "back":
                        break
                    elif ip == "exit":
                        exit()
                    else:
                        while True:
                            print("submascara:")
                            submascara = input(f"{adaptador}@{ip}>>")
                            if submascara == "back":
                                break
                            elif submascara == "exit":
                                exit()
                            else:
                                try:
                                    with open("/etc/network/interfaces", "r") as f:
                                        lineas = f.readlines()
                                except FileNotFoundError:
                                    lineas = []
                                except PermissionError:
                                    print("Error: necesitas permisos de superusuario para leer /etc/network/interfaces.")

                                # Buscar si el adaptador ya está configurado
                                inicio = None
                                fin = None
                                for i, linea in enumerate(lineas):
                                    if linea.strip() == f"auto {adaptador}":
                                        inicio = i
                                    if inicio is not None and linea.strip().startswith("iface") and i > inicio:
                                        fin = i
                                    if inicio is not None and fin is not None and (linea.strip().startswith("auto ") or i == len(lineas)-1):
                                        fin = i if linea.strip().startswith("auto ") else i+1
                                        break
                                nueva_conf = [
                                    f"auto {adaptador}\n",
                                    f"iface {adaptador} inet static\n",
                                    f"    address {ip}\n",
                                    f"    netmask {submascara}\n"
                                ]

                                if inicio is not None:
                                    lineas = lineas[:inicio] + nueva_conf + lineas[fin:]
                                else:
                                    if lineas and not lineas[-1].endswith("\n"):
                                        lineas[-1] += "\n"
                                    lineas += nueva_conf
                                try:
                                    with open("/etc/network/interfaces", "w") as f:
                                        f.writelines(lineas)
                                    print("Archivo /etc/network/interfaces actualizado correctamente.")
                                    exit()
                                except PermissionError:
                                    print("Error: necesitas permisos de superusuario para modificar /etc/network/interfaces.")
                                except Exception as e:
                                    print(f"Ocurrió un error: {e}")
                                    exit()
                                break
                        break
                break
        break
    elif tipo_ip == "2":
        while True:
            print("adaptador de red:")
            adaptador = input("dhcp@ip>>")
            if adaptador == "back":
                break
            elif adaptador == "exit":
                exit()
            else:
                # Leer el archivo actual
                try:
                    with open("/etc/network/interfaces", "r") as f:
                        lineas = f.readlines()
                except FileNotFoundError:
                    lineas = []
                except PermissionError:
                    print("Error: necesitas permisos de superusuario para leer /etc/network/interfaces.")
                    exit(1)
                inicio = None
                fin = None
                for i, linea in enumerate(lineas):
                    if linea.strip() == f"auto {adaptador}":
                        inicio = i
                    if inicio is not None and linea.strip().startswith("iface") and i > inicio:
                        fin = i
                    if inicio is not None and fin is not None and (linea.strip().startswith("auto ") or i == len(lineas)-1):
                        fin = i if linea.strip().startswith("auto ") else i+1
                        break
                nueva_conf = [
                    f"auto {adaptador}\n",
                    f"iface {adaptador} inet dhcp\n"
                ]

                if inicio is not None:
                    lineas = lineas[:inicio] + nueva_conf + lineas[fin:]
                else:
                    if lineas and not lineas[-1].endswith("\n"):
                        lineas[-1] += "\n"
                    lineas += nueva_conf
                try:
                    with open("/etc/network/interfaces", "w") as f:
                        f.writelines(lineas)
                    print("Archivo /etc/network/interfaces actualizado correctamente.")
                except PermissionError:
                    print("Error: necesitas permisos de superusuario para modificar /etc/network/interfaces.")
                except Exception as e:
                    print(f"Ocurrió un error: {e}")
                break
    elif tipo_ip == "exit":
        exit()
    else:
        print("❌","\033[31mopcion no valida, intente de nuevo o ejecute el comando h\033[0m")