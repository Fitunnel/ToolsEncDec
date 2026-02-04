# -*- coding: UTF-8 -*-
# 🛠️ ALFI ENC DEC - Ultimate Shell Protector & Editor
import os, sys, time, shutil, subprocess, re

# --- 🎨 WARNA & EMOJI ---
green="\033[0;32m"; yellow="\033[0;33m"; red="\033[0;31m"
blue="\033[0;34m"; cyan="\033[0;36m"; white="\033[0;37m"
bold="\033[1m"; end="\033[0m"

ask = f"{green}[{white}?{green}] {yellow}"
success = f"{green}[{white}√{green}] {white}"
error = f"{red}[{white}!{red}] {white}"
info = f"{yellow}[{white}+{yellow}] {cyan}"

logo = r'''
  ___   _      _____  ___   🇮🇩
 / _ \ | |    |  ___||_ _|  🇮🇩
| |_| || |    | |_    | |   🇮🇩
|  _  || |___ |  _|   | |   🇮🇩
|_| |_||_____||_|    |___|  🇮🇩
      [ 🛠️  ALFI ENC DEC 🛠️  ]
  🚀 CUSTOM AES WRAPPER SYSTEM 🚀
'''

BASE_DIR = "/storage/emulated/0/Fidecrypt/menu/"
BACKUP_DIR = os.path.join(BASE_DIR, "backup/")
ENC_OUT = os.path.join(BASE_DIR, "encrypted/")
DEC_OUT = os.path.join(BASE_DIR, "decrypted/")

def setup_folders():
    for d in [BASE_DIR, BACKUP_DIR, ENC_OUT, DEC_OUT]:
        if not os.path.exists(d):
            os.makedirs(d, exist_ok=True)

# --- 🔐 MENU 4: AES ENCRYPT (CUSTOM PASS & ITER 1-200rb) ---
def aes_batch_encrypt():
    setup_folders()
    files = [f for f in os.listdir(BASE_DIR) if os.path.isfile(os.path.join(BASE_DIR, f))]
    if not files: print(f"{error}Folder kosong!"); return
    
    passwd = input(f"{ask}Masukkan Password Custom : {white}")
    if not passwd: passwd = "KangEnc"
    
    try:
        itern = input(f"{ask}Masukkan Iterasi (1-200.000) : {white}")
        if not itern: itern = "200000"
        itern_val = int(itern)
        # Batasan 1 ~ 200.000
        if itern_val > 200000: itern_val = 200000
        if itern_val < 1: itern_val = 1
    except: itern_val = 200000
    
    print(f"{info}Encrypting {len(files)} file...")
    print(f"{info}Pass: {yellow}{passwd} {white}| Iter: {yellow}{itern_val}")
    
    count = 0
    for filename in files:
        file_path = os.path.join(BASE_DIR, filename)
        output_path = os.path.join(ENC_OUT, filename)
        try:
            cmd_enc = f'cat "{file_path}" | openssl enc -aes-256-cbc -pbkdf2 -iter {itern_val} -pass pass:"{passwd}" | base64 -w 0'
            data_b64 = subprocess.check_output(cmd_enc, shell=True).decode().strip()
            
            cmd_mac = f'printf "%s" "{data_b64}" | openssl dgst -sha256 -hmac "{passwd}" | awk \'{{print $NF}}\''
            mac_expect = subprocess.check_output(cmd_mac, shell=True).decode().strip()

            wrapper = f'''#!/usr/bin/env bash
# Encrypted by ALFI ENC DEC
PASS="{passwd}"
ITER={itern_val}
MAC_EXPECT="{mac_expect}"
DATA_B64="{data_b64}"
MAC_GOT=$(printf "%s" "$DATA_B64" | openssl dgst -sha256 -hmac "$PASS" | awk '{{print $NF}}')
if [[ "$MAC_GOT" != "$MAC_EXPECT" ]]; then
  echo "❌ Protected file corrupted"
  exit 1
fi
exec bash <(printf "%s" "$DATA_B64" | base64 -d | openssl enc -d -aes-256-cbc -pbkdf2 -iter $ITER -pass pass:"$PASS")
'''
            with open(output_path, 'w') as f: f.write(wrapper)
            os.chmod(output_path, 0o755)
            print(f"{green}  {success}Encrypted: {filename}")
            count += 1
        except: print(f"{red}  {error}Gagal: {filename}")
    input(f"\n{success}Selesai! {count} file di /encrypted/. Enter...")

# --- 🔓 MENU 3: AES DECRYPT (AUTO DETECT) ---
def aes_batch_decrypt():
    setup_folders()
    files = [f for f in os.listdir(BASE_DIR) if os.path.isfile(os.path.join(BASE_DIR, f))]
    count = 0
    for filename in files:
        file_path = os.path.join(BASE_DIR, filename)
        with open(file_path, 'r', errors='ignore') as f: content = f.read()
        if "DATA_B64=" in content:
            try:
                p_m = re.search(r'PASS="([^"]+)"', content)
                d_m = re.search(r'DATA_B64="([^"]+)"', content)
                i_m = re.search(r'ITER=([0-9]+)', content)
                it = i_m.group(1) if i_m else "200000"
                if p_m and d_m:
                    p, d = p_m.group(1), d_m.group(1)
                    out = os.path.join(DEC_OUT, filename)
                    cmd = f'echo "{d}" | base64 -d | openssl enc -d -aes-256-cbc -pbkdf2 -iter {it} -pass pass:"{p}" > "{out}" 2>/dev/null'
                    if os.system(cmd) == 0:
                        os.chmod(out, 0o755); print(f"{green}  {success}Decrypted: {filename}"); count += 1
            except: pass
    input(f"\n{success}Selesai! {count} file di /decrypted/. Enter...")

# --- 📝 MENU 9: BATCH TEXT EDITOR ---
def batch_text_editor():
    setup_folders()
    files = [f for f in os.listdir(BASE_DIR) if os.path.isfile(os.path.join(BASE_DIR, f))]
    if not files: print(f"{error}Folder kosong!"); return
    search_text = input(f"{ask}Teks yang dicari : {white}")
    replace_text = input(f"{ask}Teks pengganti   : {white}")
    count = 0
    for filename in files:
        file_path = os.path.join(BASE_DIR, filename)
        try:
            with open(file_path, 'r', errors='ignore') as f: content = f.read()
            if search_text in content:
                with open(file_path, 'w') as f: f.write(content.replace(search_text, replace_text))
                print(f"{green}  {success}Updated: {filename}"); count += 1
        except: pass
    input(f"\n{success}Selesai! {count} file diubah. Enter...")

def main():
    while True:
        os.system("clear"); print(logo)
        print(f"{white}📍 Folder: {yellow}{BASE_DIR}")
        print(f"{white}------------------------------------------")
        print(f"{green}[1] {bold}🔓 BATCH DECRYPT (Obfuscate Loop){end}")
        print(f"{green}[2] {bold}🔐 BATCH ENCRYPT (Obfuscate Loop){end}")
        print(f"{cyan}[3] {bold}🚀 ONCLICK AES DECRYPT (Auto-Pass){end}")
        print(f"{cyan}[4] {bold}💎 BATCH AES ENCRYPT (Custom Pass/Iter){end}")
        print(f"{green}[9] {bold}📝 BATCH TEXT EDITOR{end}")
        print(f"{green}[0] {red}🚪 Keluar{end}")
        print(f"{white}------------------------------------------")
        p = input(f"{ask}Pilih Menu : {white}")
        if p == "3": aes_batch_decrypt()
        elif p == "4": aes_batch_encrypt()
        elif p == "9": batch_text_editor()
        elif p == "0": sys.exit()

if __name__ == '__main__':
    try: setup_folders(); main()
    except KeyboardInterrupt: sys.exit()
