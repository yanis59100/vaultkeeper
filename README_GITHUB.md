# 🔐 VaultKeeper - Secure Password Manager

<div align="center">

![VaultKeeper](https://img.shields.io/badge/VaultKeeper-v1.0.0-blue)
![Windows](https://img.shields.io/badge/Windows-10%2B-0078D4?logo=windows)
![License](https://img.shields.io/badge/License-MIT-green)
![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)

**A futuristic password manager with cyberpunk design and military-grade AES-256 encryption**

[Download](#-quick-download) • [Features](#-features) • [Security](#-security) • [FAQ](#-faq)

</div>

---

## ✨ Features

🔐 **Military-Grade Security**
- AES-256 Encryption (Fernet)
- PBKDF2 Password Hashing
- Auto-lock after 15 minutes
- Encrypted local storage

🎨 **Cyberpunk Design**
- 50 animated floating particles
- Neon colors (Cyan, Pink, Purple, Green, Orange)
- Pulsing glow effects
- 3D button hover effects
- Professional dark theme

🚀 **Easy to Use**
- Single .exe file - No installation
- Double-click to run
- Intuitive interface
- Supports 6 password categories

💾 **Password Management**
- Add/Edit/Delete passwords
- Real-time search
- ⭐ Favorites system
- 📁 Categories (Banking, Email, Social, Work, Gaming, Other)
- 📝 Notes and URLs
- ⏰ Automatic timestamps

💪 **Advanced Tools**
- Password strength indicator (4-level scale)
- Advanced password generator
- Export to JSON/CSV
- Password history tracking

🔒 **Privacy First**
- 100% local storage
- No cloud, no servers
- No tracking or analytics
- No internet required
- Your data never leaves your computer

---

## 🚀 Quick Download

### Latest Release: v1.0.0

**Download: [VaultKeeper_v1.0.0.exe](https://github.com/YourUsername/vaultkeeper/releases/download/v1.0.0/VaultKeeper_v1.0.0.exe)**

Size: 14.6 MB | Windows 10/11 | 64-bit

---

## ⚡ Quick Start (30 seconds)

1. **Download** VaultKeeper_v1.0.0.exe (14.6 MB)
2. **Extract** the ZIP if downloaded as ZIP
3. **Run** the .exe file (double-click)
4. **Create** a strong master password
5. **Start** adding your passwords!

That's it! No installation, no configuration, no hassle.

---

## 🔐 Security Details

### Encryption
- **Algorithm**: AES-256-CBC (Fernet)
- **Standard**: FIPS-approved
- **Same as**: Banks, governments, military
- **Strength**: 256-bit keys
- **Additional**: PBKDF2 key derivation

### Storage
- **Location**: Local machine (.users/local/ folder)
- **Format**: Encrypted binary (AES)
- **Backup**: Users responsible for backups
- **Recovery**: Impossible if master password forgotten (by design)

### Auto-lock
- **Timing**: 15 minutes of inactivity
- **Purpose**: Prevents unauthorized access if left unattended
- **Behavior**: Locks automatically, requires master password to unlock

### Zero-Knowledge
- No cloud storage
- No remote servers
- No data transmission
- No tracking
- 100% offline capable

---

## 💻 System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|------------|
| **OS** | Windows 10 (64-bit) | Windows 11 |
| **RAM** | 100 MB | 500 MB |
| **Disk Space** | 50 MB | 100 MB |
| **Internet** | Not required | Not required |
| **GPU** | Any | Any |

---

## 📋 What's Inside

### Core Features
- ✅ Password storage & management
- ✅ AES-256 encryption
- ✅ Search functionality
- ✅ Categories (6 types)
- ✅ Favorites system
- ✅ Timestamps
- ✅ Export (JSON/CSV)

### UI/UX
- ✅ Cyberpunk design
- ✅ 50 animated particles
- ✅ Glow effects
- ✅ Hover animations
- ✅ Responsive layout
- ✅ Dark theme (anti-fatigue)

### Security
- ✅ Password strength meter
- ✅ Password generator
- ✅ Auto-lock timer
- ✅ Local storage only
- ✅ No data collection

---

## 🎮 Usage Guide

### Adding a Password

1. Click "➕ Add Password"
2. Fill in the details:
   - **Site Name**: Website or service name
   - **Username**: Email or username
   - **Password**: Your password
   - **URL**: Website link (optional)
   - **Notes**: Additional info (optional)
   - **Category**: Choose category
   - **Favorite**: Check if important
3. Click "Save"

### Searching

- Use the search box at the top
- Real-time filtering
- Searches in all fields

### Exporting

1. Click "📤 Export"
2. Choose format: JSON or CSV
3. Select save location
4. File is saved (unencrypted, keep safe!)

### Managing Passwords

- **Edit**: Click password → Edit button
- **Copy**: Click password → Copy to clipboard
- **Delete**: Click password → Delete (confirmation required)
- **Favorite**: Click star icon

---

## 🛠️ For Developers

### Building from Source

```bash
# Clone repository
git clone https://github.com/YourUsername/vaultkeeper.git
cd vaultkeeper

# Install dependencies
pip install -r requirements.txt

# Run application
python gui.py
```

### Building Executable

```bash
# Requires PyInstaller
pip install pyinstaller>=6.0.0

# Build executable
python build_exe.py

# Standalone .exe created in dist/
```

### Project Structure

```
vaultkeeper/
├── gui.py                      # Main interface (Tkinter)
├── password_manager.py         # Core logic
├── encryption.py               # AES-256 encryption
├── config.py                   # Configuration
├── build_exe.py                # PyInstaller build script
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

### Dependencies

```
cryptography>=41.0.0           # AES-256 encryption
pyperclip>=1.8.2               # Clipboard handling
pyinstaller>=6.0.0             # Executable building
```

All dependencies are included in the .exe file.

---

## ❓ FAQ

### General

**Q: Is VaultKeeper free?**
A: Yes! Completely free and open source (MIT License).

**Q: Is it safe to use?**
A: Yes. AES-256 encryption, local storage only, no data collection. Auditable source code.

**Q: Can I use it at work?**
A: Yes! Suitable for personal and work use. MIT License allows commercial use.

**Q: Is it open source?**
A: Yes! Source code available on GitHub for transparency and auditing.

### Security

**Q: Where are my passwords stored?**
A: Encrypted locally on your computer in the `.users/local/` folder.

**Q: Can anyone access my passwords?**
A: Only if they have your master password. It's encrypted with AES-256.

**Q: What if I forget my master password?**
A: Unfortunately, recovery is impossible. The encryption is designed to prevent even developers from recovering it.

**Q: Is internet required?**
A: No! VaultKeeper works completely offline.

**Q: Can you see my passwords?**
A: No way! Your data never leaves your computer. We have no access to your data.

### Technical

**Q: What encryption algorithm is used?**
A: AES-256-CBC via Fernet (cryptography library).

**Q: How strong is the password hashing?**
A: PBKDF2 with 100,000 iterations (industry standard).

**Q: Can I export my passwords?**
A: Yes! To JSON or CSV format. They'll be unencrypted, so keep the export file safe.

**Q: Can I import passwords?**
A: Currently no, but it's on the roadmap.

**Q: Does it sync across devices?**
A: No. VaultKeeper is local-only. You can manually backup and restore.

### Compatibility

**Q: Does it work on Mac/Linux?**
A: Currently Windows only. Mac and Linux support planned for v2.0.

**Q: Does it work on Windows 7/8?**
A: Windows 10+ required due to Tkinter compatibility.

**Q: Does it work on 32-bit Windows?**
A: No, 64-bit only.

---

## 🐛 Bug Reports & Feature Requests

Found a bug? Have an idea? Please open an issue:

**[GitHub Issues](https://github.com/YourUsername/vaultkeeper/issues)**

Include:
- Description of the issue
- Steps to reproduce
- Expected behavior
- System details (Windows version, etc.)

---

## 📈 Roadmap

### v1.0 ✅ (Current)
- Core password management
- AES-256 encryption
- Cyberpunk UI
- Export functionality

### v1.1 (Planned)
- Master password change
- Backup/restore
- Cloud sync (optional)
- Import from other managers

### v2.0 (Future)
- Mac/Linux support
- Browser extension
- Mobile app
- Biometric authentication (fingerprint)

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

**TL;DR**: You can use, modify, and distribute VaultKeeper freely. Attribution appreciated but not required.

---

## 🙏 Acknowledgments

Built with:
- **Python 3.14** - Programming language
- **Tkinter** - GUI framework
- **cryptography** - Encryption library
- **PyInstaller** - Executable building

Inspired by:
- Bitwarden (design)
- 1Password (UX)
- Cyberpunk aesthetic (style)

---

## 📧 Contact & Support

- **Website**: Coming soon
- **Email**: your-email@example.com
- **Twitter**: [@YourHandle](https://twitter.com)
- **GitHub**: [github.com/YourUsername/vaultkeeper](https://github.com/YourUsername/vaultkeeper)

---

## 🎉 Support VaultKeeper

If you like VaultKeeper, consider:

⭐ **Star the repository** on GitHub
🐦 **Share** on social media
🐛 **Report bugs** and suggest features
📖 **Write reviews** online

---

<div align="center">

**Made with ❤️ for secure password management**

![VaultKeeper](https://img.shields.io/badge/VaultKeeper-Secure%2C%20Simple%2C%20Free-blue?style=for-the-badge)

</div>
