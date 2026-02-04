# Update dan Upgrade sistem
apt update && apt upgrade -y

# Install Python (Wajib untuk menjalankan skrip .py)
apt install python -y

# Install OpenSSL (Wajib untuk fitur AES Encrypt/Decrypt)
apt install openssl-tool -y

# Install NodeJS dan NPM (Wajib untuk fitur Obfuscate Menu 1 & 2)
apt install nodejs -y

# Install bash-obfuscate secara global
npm install -g bash-obfuscate

# Memberikan izin akses penyimpanan (Agar folder Fidecrypt bisa terbaca)
termux-setup-storage
