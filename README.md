# 🔐 Hash Auditor

A Python-based cybersecurity tool for generating, verifying, and analyzing cryptographic hashes.

## ✨ Features

- Generate MD5 hashes
- Generate SHA1 hashes
- Generate SHA256 hashes
- Generate SHA512 hashes
- Verify text hash
- Verify file hash
- Password strength analysis
- Interactive menu mode
- Command-line support

## 📦 Requirements

- Python 3.x

No external libraries are required.

## 🚀 Installation

```bash
git clone https://github.com/AyushSharma-arch/Hash-Auditor.git
cd Hash-Auditor
```

## ▶️ Usage

### Interactive Mode

```bash
python3 cracker.py --interactive
```

### Generate Text Hash

```bash
python3 cracker.py --text "hello" --algo sha256
```

### Generate File Hash

```bash
python3 cracker.py --file test.txt --algo sha256
```

### Verify Text Hash

```bash
python3 cracker.py --text "hello" --verify HASH --algo sha256
```

### Verify File Hash

```bash
python3 cracker.py --file test.txt --verify HASH --algo sha256
```

### Password Strength Check

```bash
python3 cracker.py --strength "MyPassword123!"
```

## 🛠 Technologies Used

- Python
- hashlib
- argparse
- hmac
- pathlib
- regex

## 📁 Project Structure

```
Hash-Auditor/
│
├── cracker.py
├── README.md
├── LICENSE
├── requirements.txt
└── screenshots/
```

## 👨‍💻 Author

Ayush Sharma

GitHub:
https://github.com/AyushSharma-arch

## Screenshots

### Generate Text Hash
![Generate Text Hash](Screenshots/generate_text_hash.png)

### Generate File Hash
![Generate File Hash](Screenshots/generate_file_hast_sha1.png)

### Verify Text Hash
![Verify Text Hash](Screenshots/verify_hash_txt.png)

### Password Strength Analysis
![Password Strength](Screenshots/password_strenth_analysis.png)

### Interactive Mode
![Interactive Mode](Screenshots/interactive_mode.png)

### Help Menu
![Help Menu](Screenshots/help_menu.png)

---

⭐ If you like this project, consider giving it a Star.
