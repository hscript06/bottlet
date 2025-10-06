import os
import subprocess
import time
import readline

script_dir = os.path.dirname(os.path.abspath(__file__))
script_inicio = os.path.join(script_dir, "script.py")
def agregar_dns(ip_dns):
	try:
		with open("/etc/resolv.conf", "r") as f:
			lineas = f.readlines()
	except FileNotFoundError:
		lineas = []
	except PermissionError:
		print("Error: necesitas permisos de superusuario para leer /etc/resolv.conf.")
		return

	nueva_linea = f"nameserver {ip_dns}\n"
	# Solo agregar si no existe ya
	if nueva_linea not in lineas:
		if lineas and not lineas[-1].endswith("\n"):
			lineas[-1] += "\n"
		lineas.append(nueva_linea)

	try:
		with open("/etc/resolv.conf", "w") as f:
			f.writelines(lineas)
		print(f"DNS {ip_dns} agregado correctamente.")
	except PermissionError:
		print("Error: necesitas permisos de superusuario para modificar /etc/resolv.conf.")
	except Exception as e:
		print(f"Ocurrió un error: {e}")

def quitar_dns(ip_dns):
	try:
		with open("/etc/resolv.conf", "r") as f:
			lineas = f.readlines()
	except FileNotFoundError:
		print("El archivo /etc/resolv.conf no existe.")
		return
	except PermissionError:
		print("Error: necesitas permisos de superusuario para leer /etc/resolv.conf.")
		return

	nueva_lineas = [l for l in lineas if l.strip() != f"nameserver {ip_dns}"]

	try:
		with open("/etc/resolv.conf", "w") as f:
			f.writelines(nueva_lineas)
		print(f"DNS {ip_dns} eliminado correctamente.")
	except PermissionError:
		print("Error: necesitas permisos de superusuario para modificar /etc/resolv.conf.")
	except Exception as e:
		print(f"Ocurrió un error: {e}")
def opciones():
	print("  ")
	print("1- Agregar DNS")
	print("2- Quitar DNS")
	print("3- comprobar dns por ip")
	print("4- comprobar dns por dominio")
	print("0- home")

print("\n--- Configuración DNS ---")
print("para ver las opciones ejecute el comando help")
if __name__ == "__main__":
	while True:
		opcion = input("config@dns>>")

		if opcion == "1":
			ip_dns = input("dns@add>> introduce la IP del DNS:")
			agregar_dns(ip_dns)
			time.sleep(1)
		elif opcion == "2":
			ip_dns = input("dns@remove>> Introduce la IP del DNS a quitar: ")
			quitar_dns(ip_dns)
			time.sleep(1)
		elif opcion == "3":
			ip_dns = input("dns@check/ip>> Introduce la IP del DNS a comprobar: ")
			os.system(f"nslookup {ip_dns}")
			time.sleep(1)
		elif opcion == "4":
			print("Introduce el dominio a comprobar: ")
			dominio = input("dns@check/domain>>")
			os.system(f"nslookup {dominio}")
			time.sleep(1)
		elif opcion == "h":
			opciones()
		elif opcion == "exit":
			print("Saliendo...")
			exit()
		else:
			print("❌","\033[31mopcion no valida, intente de nuevo o ejecute el comando h\033[0m")
			time.sleep(0.3)
