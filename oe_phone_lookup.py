import os
import hashlib
import phonenumbers

from phonenumbers import (
    geocoder,
    carrier,
    timezone,
    region_code_for_number,
    is_valid_number,
    is_possible_number,
    number_type,
    PhoneNumberType,
    format_number,
    PhoneNumberFormat
)

os.system("cls" if os.name == "nt" else "clear")


logo = r"""

  ▄▄▄▄▄                      ▄▄▄▄▄▄▄
▄███████▄                   ███▀▀▀▀▀
███   ███ ████▄ ▄█▀█▄ ████▄ ███▄▄    ██ ██ ▄█▀█▄ ▄█▀▀▀
███▄▄▄███ ██ ██ ██▄█▀ ██ ██ ███      ██▄██ ██▄█▀ ▀███▄
 ▀█████▀  ████▀ ▀█▄▄▄ ██ ██ ▀███████  ▀██▀ ▀█▄▄▄ ▄▄▄█▀
          ██                           ██
          ▀▀                         ▀▀▀

                      PHONE LOOKUP
"""


print(logo)


phone = input("Target Phone > ").strip()


try:

    parsed = phonenumbers.parse(phone, None)

except:

    print("\n[-] Invalid number.")
    input("\nPress ENTER to exit...")
    exit()


valid = is_valid_number(parsed)
possible = is_possible_number(parsed)


country = geocoder.description_for_number(
    parsed,
    "en"
) or "Unknown"


carrier_name = carrier.name_for_number(
    parsed,
    "en"
) or "Unknown"


region = region_code_for_number(parsed) or "Unknown"


zones = timezone.time_zones_for_number(parsed)

if zones:
    timezone_info = ", ".join(zones)
else:
    timezone_info = "Unknown"



types = {

    PhoneNumberType.FIXED_LINE:
        "FIXED LINE",

    PhoneNumberType.MOBILE:
        "MOBILE",

    PhoneNumberType.FIXED_LINE_OR_MOBILE:
        "FIXED/MOBILE",

    PhoneNumberType.VOIP:
        "VOIP",

    PhoneNumberType.TOLL_FREE:
        "TOLL FREE",

    PhoneNumberType.PREMIUM_RATE:
        "PREMIUM",

    PhoneNumberType.UNKNOWN:
        "UNKNOWN"

}


ptype = types.get(
    number_type(parsed),
    "UNKNOWN"
)



e164 = format_number(
    parsed,
    PhoneNumberFormat.E164
)


international = format_number(
    parsed,
    PhoneNumberFormat.INTERNATIONAL
)


national = format_number(
    parsed,
    PhoneNumberFormat.NATIONAL
)


raw_digits = str(parsed.national_number)


fingerprint = hashlib.sha256(
    phone.encode()
).hexdigest()[:32]


prefix = "+" + str(parsed.country_code)


lines = [

    f"INPUT           : {phone}",
    f"VALID           : {'YES' if valid else 'NO'}",
    f"POSSIBLE        : {'YES' if possible else 'NO'}",

    f"",
    f"COUNTRY CODE    : {prefix}",
    f"ISO REGION      : {region}",
    f"LOCATION        : {country}",

    f"",
    f"CARRIER         : {carrier_name}",
    f"NUMBER TYPE     : {ptype}",
    f"TIMEZONE        : {timezone_info}",

    f"",
    f"E164            : {e164}",
    f"INTERNATIONAL   : {international}",
    f"NATIONAL        : {national}",

    f"",
    f"NSN             : {raw_digits}",
    f"DIGIT LENGTH    : {len(raw_digits)}",
    f"PREFIX          : {raw_digits[:3]}",
    f"SHA256 ID       : {fingerprint}"

]



title = "PHONE INFORMATION"


longest = max(
    len(title),
    *(len(x) for x in lines)
)


padding = 2
width = longest + padding * 2



def box(text=""):

    return (
        "│"
        + " " * padding
        + text.ljust(longest)
        + " " * padding
        + "│"
    )



print()

print(
    "┌" +
    "─" * width +
    "┐"
)


print(
    box(title.center(longest))
)


print(
    "├" +
    "─" * width +
    "┤"
)



for line in lines:

    if line == "":
        print(box())

    else:
        print(box(line))


print(
    "└" +
    "─" * width +
    "┘"
)



input("\nPress ENTER to exit...")