import os
import requests


os.system("cls" if os.name == "nt" else "clear")


logo = r"""
                                                       
  ▄▄▄▄▄                      ▄▄▄▄▄▄▄                   
▄███████▄                   ███▀▀▀▀▀                   
███   ███ ████▄ ▄█▀█▄ ████▄ ███▄▄    ██ ██ ▄█▀█▄ ▄█▀▀▀ 
███▄▄▄███ ██ ██ ██▄█▀ ██ ██ ███      ██▄██ ██▄█▀ ▀███▄ 
 ▀█████▀  ████▀ ▀█▄▄▄ ██ ██ ▀███████  ▀██▀ ▀█▄▄▄ ▄▄▄█▀ 
          ██                           ██              
          ▀▀                         ▀▀▀               
                          
                          IP LOOKUP
"""


print(logo)


ip = input("Target IP > ").strip()


try:

    response = requests.get(
        f"http://ip-api.com/json/{ip}?fields=status,message,query,country,countryCode,regionName,city,zip,lat,lon,isp,org,as,mobile,proxy,hosting",
        timeout=10
    )


    data = response.json()


    if data.get("status") != "success":

        print("\n[-] Invalid IP Address or lookup failed.")


    else:

        title = f"IP LOOKUP — {data['query']}"


        lines = [

            f"RESOLVED IP     : {data['query']}",
            f"COUNTRY         : {data['country']} ({data['countryCode']})",
            f"REGION          : {data['regionName']}",
            f"CITY            : {data['city']}",
            f"ZIP CODE        : {data['zip']}",
            f"COORDINATES     : {data['lat']}, {data['lon']}",
            f"ISP             : {data['isp']}",
            f"ORGANIZATION    : {data['org']}",
            f"ASN             : {data['as']}",
            f"PROXY / VPN     : {'Yes' if data['proxy'] else 'No'}",
            f"MOBILE          : {'Yes' if data['mobile'] else 'No'}",
            f"HOSTING         : {'Yes' if data['hosting'] else 'No'}"

        ]


        maps = (
            f"Google Maps : https://www.google.com/maps?q="
            f"{data['lat']},{data['lon']}"
        )


        longest = max(
            len(title),
            len(maps),
            *(len(line) for line in lines)
        )


        padding = 2
        width = longest + padding * 2


        def box(line=""):

            return (
                "│"
                + " " * padding
                + line.ljust(longest)
                + " " * padding
                + "│"
            )


        print()

        print(
            "┌"
            + "─" * width
            + "┐"
        )


        print(
            box(
                title.center(longest)
            )
        )


        print(
            "├"
            + "─" * width
            + "┤"
        )


        for line in lines:
            print(box(line))


        print(
            "├"
            + "─" * width
            + "┤"
        )


        print(
            box(maps)
        )


        print(
            "└"
            + "─" * width
            + "┘"
        )


except requests.exceptions.RequestException as e:

    print(
        f"\n[-] Network Error: {e}"
    )


except Exception as e:

    print(
        f"\n[-] Error: {e}"
    )


input("\nPress ENTER to exit...")