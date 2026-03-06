#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Copyright 2026 AItool_Phishing
# Written by: AI & Ulises Garcia
# Facebook: Ulises Garcia
# Github: https://github.com/Kuaker123    

import os
import subprocess
import time
import shutil
from pathlib import Path
import random

# --- Constants ---
BLUE, RED, WHITE, CYAN, DEFAULT, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\033[36m', '\033[0m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'

TOOLS = {
    "Gophish (Phishing Framework)": {
        "repo": "https://github.com/gophish/gophish.git",
        "install": [
            "sudo apt install golang-go -y",
            "go build"
        ],
        "run": "./gophish",
        "description": "Plataforma profesional para campañas de phishing empresariales."
    },
    "Zphisher (Modern & Stable)": {
        "repo": "https://github.com/htr-tech/zphisher.git",
        "install": ["chmod +x zphisher.sh"],
        "run": "./zphisher.sh",
        "description": "La evolución moderna de Shellphish, más estable y con mejores túneles."
    },
    "Wifimosys (WiFi Phishing)": {
        "repo": "https://github.com/wi-fi-analyzer/wifimosys.git",
        "install": [
            "sudo apt install xterm isc-dhcp-server hostapd lighttpd php-cgi -y",
            "chmod +x wifimosys.sh"
        ],
        "run": "sudo ./wifimosys.sh",
        "description": "Ataques de Evil Twin para capturar contraseñas WPA mediante phishing WiFi."
    },
    "AdvPhishing (Advanced)": {
        "repo": "https://github.com/Ignitetch/AdvPhishing.git",
        "install": ["chmod +x setup.sh && ./setup.sh"],
        "run": "./AdvPhishing.sh",
        "description": "Herramienta avanzada con plantillas de OTP y autenticación en dos pasos."
    },
    "Modlishka (Reverse Proxy)": {
        "repo": None,
        "install": [
            "go get -u github.com/drk1wi/Modlishka"
        ],
        "run": "~/go/bin/Modlishka",
        "description": "Proxy inverso para bypass de 2FA en tiempo real."
    }
}

# --- Helper Functions ---

def is_root():
    """Checks if the script is running with root privileges."""
    return os.geteuid() == 0

def check_dependencies():
    """Checks if required system dependencies are installed."""
    if not shutil.which("git"):
        print(f"{RED}Error: Git no está instalado. Por favor, instálelo para continuar.{END}")
        exit(1)
    if not is_root():
        print(f"{YELLOW}ADVERTENCIA: No estás ejecutando como root. Algunas herramientas (como Wifimosys) fallarán.{END}")

def run_command(command, cwd=None):
    """Runs a command in the shell and returns True if successful, False otherwise."""
    try:
        # Using shell=True can be a security hazard if the command is constructed from external input.
        # In this case, commands are hardcoded, so the risk is mitigated.
        subprocess.run(command, shell=True, check=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error al ejecutar el comando: {command}{END}")
        print(f"{RED}Salida de error:\n{e.stderr.decode()}{END}")
        return False

def get_install_path():
    """Gets the installation path from the user."""
    while True:
        path_str = input(f"{YELLOW}Ingrese la ruta donde desea guardar las herramientas (Ej: /home/user/Desktop):{END}\n--> ")
        path = Path(path_str).expanduser()
        if path.is_dir():
            return path
        else:
            print(f"{RED}La ruta especificada no es un directorio válido. Inténtelo de nuevo.{END}")

def install_tool(tool_name, install_path):
    """Clones a tool's repository and runs its installation commands."""
    tool = TOOLS[tool_name]
    repo_url = tool.get("repo")
    install_commands = tool.get("install", [])
    
    # Special handling for Modlishka, which requires Go
    if tool_name == "Modlishka (Reverse Proxy)":
        if not shutil.which("go"):
            print(f"{RED}Error: Go no está instalado. Modlishka no puede ser instalada.{END}")
            print(f"{YELLOW}Por favor, instale Go y asegúrese de que esté en su PATH.{END}")
            print(f"{YELLOW}Instrucciones de instalación: https://golang.org/doc/install{END}")
            return False, None
        # Go tools are typically installed in the user's home directory
        tool_path = Path.home()
    elif repo_url:
        tool_path = install_path / tool_name
        if tool_path.exists():
            print(f"{YELLOW}El directorio {tool_path} ya existe. Omitiendo clonación.{END}")
        else:
            print(f"{GREEN}Clonando {tool_name}...{END}")
            if not run_command(f"git clone {repo_url} {tool_path}"):
                return False, None
    else:
        # Fallback for tools without a repo, though none should exist now except Modlishka
        tool_path = install_path

    print(f"{GREEN}Instalando dependencias para {tool_name}...{END}")
    for command in install_commands:
        if not run_command(command, cwd=tool_path):
            return False, None
            
    return True, tool_path

def execute_tool(tool_name, tool_path):
    """Executes the main script of a tool."""
    run_command_str = TOOLS[tool_name].get("run")
    if not run_command_str:
        print(f"{YELLOW}No hay un comando de ejecución definido para {tool_name}.{END}")
        return

    if input(f"{CYAN}¿Desea ejecutar {tool_name}? (y/n){END}\n--> ").upper() == "Y":
        print(f"{GREEN}Ejecutando {tool_name}...{END}")
        time.sleep(2)
        if not run_command(run_command_str, cwd=tool_path):
            print(f"{RED}La ejecución de {tool_name} falló.{END}")

# --- Main Logic ---

def matrix_animation():
    """Displays a matrix-style animation."""
    os.system('clear')
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()"
    for _ in range(50):
        line = ''.join(random.choice(chars) for _ in range(os.get_terminal_size().columns))
        print(f"{GREEN}{line}{END}")
        time.sleep(0.05)
    os.system('clear')

def display_banner():
    """Displays the main banner of the application."""
    print(f"""{GREEN}
---------------------------------------------------------------->
|                                                               |
|       ████████╗ ██████╗  ██████╗ ██╗     ███████╗             |
|       ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝             |
|          ██║   ██║   ██║██║   ██║██║     ███████╗             |
|          ██║   ██║   ██║██║   ██║██║     ╚════██║             |
|          ██║   ╚██████╔╝╚██████╔╝███████╗███████║             |
|                                                               | 
|   ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗██╗███╗   ██╗ ██████╗    |
|   ██╔══██╗██║  ██║██║██╔════╝██║  ██║██║████╗  ██║██╔════╝    |
|   ██████╔╝███████║██║███████╗███████║██║██╔██╗ ██║██║  ███╗   |
|   ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██║██║╚██╗██║██║   ██║   |
|   ██║     ██║  ██║██║███████║██║  ██║██║██║ ╚████║╚██████╔╝   |
|   ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝    |
<---------------------------------------------------------------- {END}""")
    print(f'{RED}AITool-Phishing{END}'.center(65))
    print(f'{GREEN} EL ROBO DE CREDENCIALES MEDIANTE ESTA TECNICA ES LA MAS EFICAZ.{END}')
    print(f'{YELLOW}Creado por: {BLUE}AI & Ulises Garcia {YELLOW}({RED}Kuaker123{YELLOW}) {YELLOW}Version: {BLUE}3.0{YELLOW}{END}'.center(110))
    print(f'{GREEN}================================================================={END}')

def display_menu():
    """Displays the tool selection menu and returns the user's choice."""
    print(f"\n{CYAN}Escoja la herramienta que desea instalar en su equipo (Herramientas de Alto Poder):{END}")
    for i, (tool_name, data) in enumerate(TOOLS.items(), 1):
        print(f"\n #{i} --- {tool_name}")
        print(f"       {WHITE}{data.get('description', '')}{END}")
    
    while True:
        try:
            choice = int(input(f"\n{YELLOW}Seleccione una opción (1-{len(TOOLS)}): {END}"))
            if 1 <= choice <= len(TOOLS):
                return list(TOOLS.keys())[choice - 1]
            else:
                print(f"{RED}Opción no válida. Inténtelo de nuevo.{END}")
        except ValueError:
            print(f"{RED}Por favor, ingrese un número.{END}")

def main():
    """Main function of the program."""
    matrix_animation()
    check_dependencies()
    display_banner()
    
    if input(f"""{YELLOW}ADVERTENCIA: Este programa instala herramientas que pueden ser utilizadas para realizar ataques de phishing. El uso de estas herramientas con fines maliciosos es ilegal y puede tener graves consecuencias legales. ¿Acepta utilizar esta herramienta únicamente con fines educativos y éticos? (y/n){END}\n--> """).upper() != "Y":
        os.system('clear')
        print(f'\n{RED}NO HAS ACEPTADO LOS TÉRMINOS DE USO ÉTICO.{END}')
        exit(0)

    install_path = get_install_path()
    
    while True:
        chosen_tool = display_menu()
        
        if chosen_tool == "Modlishka (Reverse Proxy)":
            print(f"""{YELLOW}ADVERTENCIA: La instalación de Modlishka requiere que Go esté instalado y configurado en su PATH.{END}""")
            if input(f"{CYAN}¿Desea continuar de todas formas? (y/n){END}\n--> ").upper() != "Y":
                continue

        success, tool_path = install_tool(chosen_tool, install_path)
        
        if success:
            print(f"{GREEN}{chosen_tool} se ha instalado correctamente.{END}")
            execute_tool(chosen_tool, tool_path)
        else:
            print(f"{RED}La instalación de {chosen_tool} ha fallado.{END}")

        if input(f"\n{CYAN}¿Desea instalar otra herramienta? (y/n){END}\n--> ").upper() != "Y":
            print(f"{GREEN}GRACIAS POR UTILIZAR AITool-Phishing{END}")
            break

if __name__ == "__main__":
    main()
