# coding=utf-8
import subprocess
import optparse
import re

def get_arguments():
    #Dar aegumentos a la ejeccución
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest = "interface", help = "Interface para cambiar Direccion MAC")
    parser.add_option("-m", "--mac", dest = "new_mac", help = "Nueva Direccion MAC")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Por favor indicar una interface, usa --help para mas info.")
    elif not options.new_mac:
        parser.error("[-] Por favor indicar una Dirección MAC, usa --help para mas info.")
    return options

def change_mac(interface, new_mac):
    print("[+] Cambiando Direccion MAC para " + interface + " a " + new_mac)
    #Función Segura
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_results = subprocess.check_output(["ifconfig", options.interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_results)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] No pudimos leer la direccion MAC")

options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC > " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] La Direccion MAC cambio correctamente a " + current_mac)
else:
    print("[-] La Direccion MAC no ha sido cambiada")