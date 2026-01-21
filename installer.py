#!/usr/bin/env python3
"""
Gestionnaire de Mots de Passe - Installateur Windows
Convertir en EXE avec: pyinstaller installer.py --name=PasswordManagerInstaller --onefile --windowed
"""

import sys
import os
import subprocess
import shutil
from pathlib import Path
from tkinter import Tk, messagebox, ttk
import tkinter as tk


class PasswordManagerInstaller:
    def __init__(self):
        self.root = Tk()
        self.root.title("Gestionnaire de Mots de Passe - Installer")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Variables
        self.install_path = Path.home() / "Desktop" / "Gestionnaire de Mots de Passe"
        self.status = tk.StringVar(value="En attente...")
        
        # UI
        self.setup_ui()
        
    def setup_ui(self):
        """Créer l'interface d'installation"""
        
        # Titre
        title = ttk.Label(
            self.root,
            text="Gestionnaire de Mots de Passe",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=20)
        
        # Sous-titre
        subtitle = ttk.Label(
            self.root,
            text="Installer l'application sur le Bureau",
            font=("Arial", 10)
        )
        subtitle.pack()
        
        # Chemin d'installation
        path_frame = ttk.LabelFrame(self.root, text="Chemin d'installation", padding=10)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        path_label = ttk.Label(path_frame, text=str(self.install_path))
        path_label.pack()
        
        # Barre de progression
        progress_frame = ttk.LabelFrame(self.root, text="Installation", padding=10)
        progress_frame.pack(fill="x", padx=20, pady=10)
        
        self.progress = ttk.Progressbar(
            progress_frame,
            mode="indeterminate",
            length=400
        )
        self.progress.pack(fill="x", pady=5)
        
        # Status
        status_label = ttk.Label(
            progress_frame,
            textvariable=self.status,
            font=("Arial", 9)
        )
        status_label.pack(pady=5)
        
        # Boutons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        self.install_btn = ttk.Button(
            button_frame,
            text="Installer",
            command=self.install
        )
        self.install_btn.pack(side="left", padx=5)
        
        self.cancel_btn = ttk.Button(
            button_frame,
            text="Annuler",
            command=self.root.quit
        )
        self.cancel_btn.pack(side="left", padx=5)
        
    def update_status(self, message):
        """Mettre à jour le statut"""
        self.status.set(message)
        self.root.update()
        
    def run_command(self, cmd, description):
        """Exécuter une commande"""
        try:
            self.update_status(description)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=True,
                check=False
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)
    
    def install(self):
        """Lancer l'installation"""
        self.install_btn.config(state="disabled")
        self.cancel_btn.config(state="disabled")
        self.progress.start()
        
        try:
            # 1. Vérifier Python
            self.update_status("Verifi: Python...")
            success, output = self.run_command("python --version", "Verification de Python")
            if not success:
                raise Exception("Python n'est pas installe ou accessible")
            
            # 2. Installer dépendances
            self.update_status("Installation: cryptography...")
            success, _ = self.run_command(
                "python -m pip install --quiet cryptography pyinstaller",
                "Installation des dependances"
            )
            if not success:
                raise Exception("Erreur lors de l'installation des dependances")
            
            # 3. Créer l'exécutable
            self.update_status("Creation: executable...")
            current_dir = Path(__file__).parent
            build_script = current_dir / "build_exe.py"
            
            if build_script.exists():
                success, output = self.run_command(
                    f"cd \"{current_dir}\" && python build_exe.py",
                    "Creation de l'executable"
                )
                if not success:
                    raise Exception(f"Erreur lors de la creation de l'executable:\n{output}")
            else:
                # Créer l'exe avec PyInstaller directement
                success, output = self.run_command(
                    f"cd \"{current_dir}\" && pyinstaller main.py --name=PasswordManager --onefile --windowed",
                    "Creation de l'executable"
                )
                if not success:
                    raise Exception(f"Erreur: {output}")
            
            # 4. Vérifier l'exécutable
            exe_path = current_dir / "dist" / "PasswordManager.exe"
            if not exe_path.exists():
                raise Exception(f"L'executable n'a pas ete cree: {exe_path}")
            
            # 5. Créer le dossier d'installation
            self.update_status("Creation: dossier d'installation...")
            self.install_path.mkdir(parents=True, exist_ok=True)
            
            # 6. Copier l'exécutable
            self.update_status("Copie: executable...")
            shutil.copy(exe_path, self.install_path / "PasswordManager.exe")
            
            # 7. Copier les données (si existantes)
            self.update_status("Copie: donnees...")
            for file in ["salt.bin", "passwords.enc"]:
                src = current_dir / file
                if src.exists():
                    shutil.copy(src, self.install_path / file)
            
            # 8. Créer le raccourci
            self.update_status("Creation: raccourci Bureau...")
            self.create_desktop_shortcut()
            
            # 9. Succès !
            self.progress.stop()
            self.update_status("Installation terminee !")
            
            messagebox.showinfo(
                "Succes",
                f"Installation terminee avec succes !\n\n"
                f"Dossier: {self.install_path}\n\n"
                f"Vous pouvez maintenant utiliser l'application:\n"
                f"- Double-clic sur le raccourci du Bureau\n"
                f"- Ou ouvrez le dossier et lancez PasswordManager.exe"
            )
            
            self.root.quit()
            
        except Exception as e:
            self.progress.stop()
            self.install_btn.config(state="normal")
            self.cancel_btn.config(state="normal")
            
            messagebox.showerror(
                "Erreur d'installation",
                f"Une erreur est survenue:\n\n{str(e)}\n\n"
                f"Solutions:\n"
                f"1. Verifiez que Python 3.7+ est installe\n"
                f"2. Cochez 'Add Python to PATH' lors de l'installation de Python\n"
                f"3. Redemarrez l'ordinateur\n"
                f"4. Relancez cet installateur"
            )
    
    def create_desktop_shortcut(self):
        """Créer un raccourci sur le Bureau"""
        try:
            # Import Windows-specific
            from win32com.client import Dispatch
            
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "PasswordManager.lnk"
            
            shell = Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(str(shortcut_path))
            shortcut.TargetPath = str(self.install_path / "PasswordManager.exe")
            shortcut.WorkingDirectory = str(self.install_path)
            shortcut.Description = "Gestionnaire de Mots de Passe Securise"
            shortcut.IconLocation = str(self.install_path / "PasswordManager.exe")
            shortcut.Save()
        except ImportError:
            # Fallback: créer un raccourci simple avec VBScript
            try:
                desktop = Path.home() / "Desktop"
                shortcut_path = desktop / "PasswordManager.lnk"
                
                vbs_script = f"""
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{self.install_path / 'PasswordManager.exe'}"
oLink.WorkingDirectory = "{self.install_path}"
oLink.Description = "Gestionnaire de Mots de Passe Securise"
oLink.Save
"""
                vbs_file = self.install_path / "create_shortcut.vbs"
                vbs_file.write_text(vbs_script)
                subprocess.run(f'cscript "{vbs_file}"', shell=True, capture_output=True)
                vbs_file.unlink()
            except:
                pass
    
    def run(self):
        """Lancer l'application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = PasswordManagerInstaller()
    app.run()
