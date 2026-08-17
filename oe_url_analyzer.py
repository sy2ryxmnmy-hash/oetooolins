import os
import socket
import ssl
import requests
from urllib.parse import urlparse
from datetime import datetime


os.system("cls" if os.name == "nt" else "clear")


logo = r"""
                                                       
  ▄▄▄▄▄                      ▄▄▄▄▄▄▄                   
▄███████▄                   ███▀▀▀▀▀                   
███   ███ ████▄ ▄█▀█▄ ████▄ ███▄▄    ██ ██ ▄█▀█▄ ▄█▀▀▀ 
███▄▄▄███ ██ ██ ██▄█▀ ██ ██ ███      ██▄██ ██▄█▀ ▀███▄ 
 ▀█████▀  ████▀ ▀█▄▄▄ ██ ██ ▀███████  ▀██▀ ▀█▄▄▄ ▄▄▄█▀ 
          ██                           ██              
          ▀▀                         ▀▀▀               

                    URL ANALYZER
"""


print(logo)


def box(title, lines):

    longest = max(
        len(title),
        *(len(line) for line in lines)
    )

    padding = 2
    width = longest + padding * 2


    def line(text=""):

        return (
            "│"
            + " " * padding
            + text.ljust(longest)
            + " " * padding
            + "│"
        )


    print()
    print("┌" + "─" * width + "┐")
    print(line(title.center(longest)))
    print("├" + "─" * width + "┤")

    for item in lines:
        print(line(item))

    print("└" + "─" * width + "┘")


def scan_port(ip, port):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.settimeout(0.5)

    result = sock.connect_ex(
        (ip, port)
    )

    sock.close()

    return result == 0



url = input("URL > ").strip()


try:

    if not url.startswith(("http://", "https://")):
        url = "https://" + url


    parsed = urlparse(url)

    domain = parsed.netloc


    ip = socket.gethostbyname(domain)


    response = requests.get(
        url,
        timeout=10,
        allow_redirects=True
    )


    ports = [
        21,
        22,
        25,
        53,
        80,
        110,
        143,
        443,
        3306,
        8080
    ]


    open_ports = []


    for port in ports:

        if scan_port(ip, port):
            open_ports.append(str(port))


    ssl_status = "Disabled"


    if parsed.scheme == "https":

        ssl_status = "Enabled"


    try:

        certificate = ssl.get_server_certificate(
            (domain, 443)
        )

        ssl_valid = "Available"

    except:

        ssl_valid = "Unavailable"



    headers = response.headers


    lines = [

        f"DOMAIN        : {domain}",
        f"IP ADDRESS    : {ip}",
        f"PROTOCOL      : {parsed.scheme.upper()}",
        f"STATUS CODE   : {response.status_code}",
        f"HTTPS         : {ssl_status}",
        f"SSL CERT      : {ssl_valid}",
        f"SERVER        : {headers.get('server','Unknown')}",
        f"CONTENT TYPE  : {headers.get('content-type','Unknown')}",
        f"REDIRECTS     : {len(response.history)}",
        f"OPEN PORTS    : {', '.join(open_ports) if open_ports else 'None'}",
        f"SCAN TIME     : {datetime.now().strftime('%H:%M:%S')}"

    ]


    box(
        "URL ANALYSIS RESULT",
        lines
    )


except Exception as e:

    print(
        f"\n[-] Error: {e}"
    )


input(
    "\nPress ENTER to exit..."
)