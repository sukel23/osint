import os
from dotenv import load_dotenv
import requests

# Cargamos las variables del archivo .env
load_dotenv()

class OsintTool:
    def __init__(self):
        # Ejemplo: Obtener una API Key de Shodan guardada en el entorno
        self.shodan_key = os.getenv("SHODAN_API_KEY")

    def search_shodan(self, ip):
        if not self.shodan_key:
            return "Error: No se encontró la API Key de Shodan."
        
        print(f"[*] Consultando Shodan para la IP: {ip}...")
        url = f"https://api.shodan.io/shodan/host/{ip}?key={self.shodan_key}"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else "Sin resultados."

    def search_username(self, username):
        print(f"[*] Buscando usuario '{username}' en redes sociales comunes...")
        urls = [
            f"https://www.instagram.com/{username}",
            f"https://twitter.com/{username}",
            f"https://github.com/{username}"
        ]
        results = {}
        for url in urls:
            resp = requests.get(url)
            results[url] = "Existe" if resp.status_code == 200 else "No encontrado"
        return results

def main():
    tool = OsintTool()
    print("--- OSINT FRAMEWORK (GitHub Ready) ---")
    opcion = input("1. Buscar Usuario\n2. Buscar IP (Shodan)\nSeleccion: ")
    
    if opcion == "1":
        user = input("Username: ")
        print(tool.search_username(user))
    elif opcion == "2":
        ip = input("IP: ")
        print(tool.search_shodan(ip))

if __name__ == "__main__":
    main()