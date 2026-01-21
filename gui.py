"""
🌟 PASSWORD MANAGER PRO v4.0 🌟
FUTURISTIC CYBERPUNK EDITION
Animations • Glow Effects • Neon Design • Particles
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import string
import secrets
import webbrowser
import random
import math
import threading
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from encryption import PasswordEncryption
from password_manager import PasswordManager
from backend_client import VaultKeeperBackendClient


class FuturisticPasswordManager:
    """CYBERPUNK Password Manager with Animations & Futuristic Design"""
    
    CATEGORIES = ["General", "Social Media", "Banking", "Email", "Gaming", "Work", "Shopping", "Other"]
    
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ PASSWORD VAULT CYBER ⚡")
        self.root.geometry("1400x850")
        self.root.resizable(True, True)
        
        # Security & Data
        self.password_manager = None
        self.master_password = None
        self.logged_in = False
        
        # Backend sync
        self.backend_client = VaultKeeperBackendClient()
        self.backend_available = self.backend_client.health_check()
        self.sync_in_progress = False
        
        # UI State
        self.current_site = None
        self.current_filter = "all"
        
        # Animation state
        self.particles = []
        self.animation_running = False
        self.glow_phase = 0
        
        # Auto-lock
        self.last_activity = datetime.now()
        self.auto_lock_minutes = 15
        self.check_activity()
        
        # Futuristic Colors - NEON CYBERPUNK
        self.CYBER_BG = "#0a0a0f"           # Deep dark
        self.CYBER_BG2 = "#12121a"          # Card BG
        self.CYBER_BG3 = "#1a1a28"          # Lighter
        self.NEON_CYAN = "#00fff9"          # Cyan neon
        self.NEON_PINK = "#ff006e"          # Pink neon
        self.NEON_PURPLE = "#b537ff"        # Purple neon
        self.NEON_BLUE = "#0080ff"          # Blue neon
        self.NEON_GREEN = "#00ff88"         # Green neon
        self.NEON_YELLOW = "#ffff00"        # Yellow neon
        self.NEON_ORANGE = "#ff6b00"        # Orange neon
        
        self.setup_styles()
        self.show_futuristic_login()
    
    def check_activity(self):
        """Auto-lock timer"""
        if self.logged_in:
            elapsed = datetime.now() - self.last_activity
            if elapsed > timedelta(minutes=self.auto_lock_minutes):
                messagebox.showinfo("🔒 AUTO-LOCK", "Session locked due to inactivity")
                self.logout()
                return
        self.root.after(30000, self.check_activity)
    
    def reset_activity(self):
        self.last_activity = datetime.now()
    
    def setup_styles(self):
        """Configure cyberpunk style"""
        self.root.configure(bg=self.CYBER_BG)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Cyber.TFrame", background=self.CYBER_BG)
    
    def clear_window(self):
        """Clear all widgets"""
        self.animation_running = False
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def animate_glow(self, widget, color1, color2):
        """Create pulsing glow effect"""
        try:
            self.glow_phase += 0.05
            alpha = (math.sin(self.glow_phase) + 1) / 2  # 0 to 1
            
            # Interpolate between colors
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
            
            r = int(r1 + (r2 - r1) * alpha)
            g = int(g1 + (g2 - g1) * alpha)
            b = int(b1 + (b2 - b1) * alpha)
            
            new_color = f"#{r:02x}{g:02x}{b:02x}"
            
            if widget.winfo_exists():
                widget.configure(fg=new_color)
                self.root.after(50, lambda: self.animate_glow(widget, color1, color2))
        except:
            pass
    
    def create_neon_button(self, parent, text, command, bg_color, width=None):
        """Create futuristic neon button"""
        btn = tk.Button(
            parent,
            text=text,
            font=("Consolas", 11, "bold"),
            bg=bg_color,
            fg="#000000",
            activebackground=bg_color,
            activeforeground="#ffffff",
            border=0,
            cursor="hand2",
            padx=25,
            pady=12,
            command=command,
            relief=tk.RAISED,
            bd=3,
            highlightthickness=2,
            highlightbackground=bg_color,
            highlightcolor="#ffffff"
        )
        if width:
            btn.config(width=width)
        
        # Hover effects
        def on_enter(e):
            btn.config(fg="#ffffff", relief=tk.SUNKEN)
        
        def on_leave(e):
            btn.config(fg="#000000", relief=tk.RAISED)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def create_particle_canvas(self, parent):
        """Create animated particle background"""
        canvas = tk.Canvas(
            parent,
            bg=self.CYBER_BG,
            highlightthickness=0,
            width=1400,
            height=850
        )
        canvas.place(x=0, y=0, relwidth=1, relheight=1)
        # Canvas will be in background by default if created first
        
        # Create particles
        self.particles = []
        for _ in range(50):
            x = random.randint(0, 1400)
            y = random.randint(0, 850)
            size = random.randint(1, 3)
            speed_x = random.uniform(-0.5, 0.5)
            speed_y = random.uniform(-0.5, 0.5)
            color = random.choice([self.NEON_CYAN, self.NEON_PINK, self.NEON_PURPLE, self.NEON_BLUE])
            
            particle_id = canvas.create_oval(x, y, x+size, y+size, fill=color, outline=color)
            self.particles.append({
                'id': particle_id,
                'x': x,
                'y': y,
                'speed_x': speed_x,
                'speed_y': speed_y
            })
        
        self.animate_particles(canvas)
        return canvas
    
    def animate_particles(self, canvas):
        """Animate floating particles"""
        if not self.animation_running:
            return
        
        try:
            for particle in self.particles:
                particle['x'] += particle['speed_x']
                particle['y'] += particle['speed_y']
                
                # Wrap around screen
                if particle['x'] < 0:
                    particle['x'] = 1400
                elif particle['x'] > 1400:
                    particle['x'] = 0
                
                if particle['y'] < 0:
                    particle['y'] = 850
                elif particle['y'] > 850:
                    particle['y'] = 0
                
                # Update position
                coords = canvas.coords(particle['id'])
                if coords:
                    size = coords[2] - coords[0]
                    canvas.coords(particle['id'], 
                                 particle['x'], particle['y'],
                                 particle['x'] + size, particle['y'] + size)
            
            self.root.after(30, lambda: self.animate_particles(canvas))
        except:
            pass
    
    def show_futuristic_login(self):
        """Cyberpunk login screen with animations"""
        self.clear_window()
        self.animation_running = True
        
        # Background
        main = tk.Frame(self.root, bg=self.CYBER_BG)
        main.pack(fill=tk.BOTH, expand=True)
        
        # Particle canvas
        self.create_particle_canvas(main)
        
        # Center container with glow effect
        center = tk.Frame(main, bg=self.CYBER_BG2, highlightbackground=self.NEON_CYAN, highlightthickness=3)
        center.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=600, height=550)
        
        # Animated title
        title_frame = tk.Frame(center, bg=self.CYBER_BG2)
        title_frame.pack(pady=(40, 10))
        
        # Large emoji with glow
        emoji = tk.Label(
            title_frame,
            text="⚡",
            font=("Segoe UI Emoji", 80, "bold"),
            bg=self.CYBER_BG2,
            fg=self.NEON_CYAN
        )
        emoji.pack()
        self.animate_glow(emoji, self.NEON_CYAN, self.NEON_PINK)
        
        # Glitch-style title
        title1 = tk.Label(
            center,
            text="╔═══════════════════════╗",
            font=("Consolas", 14, "bold"),
            bg=self.CYBER_BG2,
            fg=self.NEON_CYAN
        )
        title1.pack(pady=(5, 0))
        
        title2 = tk.Label(
            center,
            text="  PASSWORD VAULT CYBER  ",
            font=("Consolas", 22, "bold"),
            bg=self.CYBER_BG2,
            fg=self.NEON_PINK
        )
        title2.pack()
        self.animate_glow(title2, self.NEON_PINK, self.NEON_PURPLE)
        
        title3 = tk.Label(
            center,
            text="╚═══════════════════════╝",
            font=("Consolas", 14, "bold"),
            bg=self.CYBER_BG2,
            fg=self.NEON_CYAN
        )
        title3.pack(pady=(0, 5))
        
        # Version badge
        version = tk.Label(
            center,
            text="[ v4.0 CYBERPUNK EDITION ]",
            font=("Consolas", 10, "bold"),
            bg=self.CYBER_BG2,
            fg=self.NEON_PURPLE
        )
        version.pack(pady=(5, 30))
        
        # Backend status indicator
        backend_status = "🟢 CLOUD SYNC ONLINE" if self.backend_available else "🔴 LOCAL MODE"
        backend_color = self.NEON_GREEN if self.backend_available else self.NEON_ORANGE
        backend_label = tk.Label(
            center,
            text=backend_status,
            font=("Consolas", 9, "bold"),
            bg=self.CYBER_BG2,
            fg=backend_color
        )
        backend_label.pack(pady=(0, 20))
        
        # Login form
        form = tk.Frame(center, bg=self.CYBER_BG2)
        form.pack(padx=50)
        
        # Label
        tk.Label(
            form,
            text="▶ MASTER ACCESS CODE",
            font=("Consolas", 11, "bold"),
            bg=self.CYBER_BG2,
            fg=self.NEON_GREEN
        ).pack(anchor="w", padx=5, pady=(0, 10))
        
        # Password entry with neon border
        pwd_container = tk.Frame(
            form,
            bg=self.CYBER_BG3,
            highlightbackground=self.NEON_CYAN,
            highlightthickness=2
        )
        pwd_container.pack(fill=tk.X, pady=(0, 30))
        
        self.pwd_entry = tk.Entry(
            pwd_container,
            show="●",
            font=("Consolas", 14, "bold"),
            bg=self.CYBER_BG3,
            fg=self.NEON_CYAN,
            border=0,
            insertbackground=self.NEON_PINK,
            width=35
        )
        self.pwd_entry.pack(ipady=15, padx=15, pady=15)
        self.pwd_entry.bind("<Return>", lambda e: self.login())
        self.pwd_entry.focus()
        
        # Button with animation
        btn_frame = tk.Frame(form, bg=self.CYBER_BG2)
        btn_frame.pack()
        
        login_btn = self.create_neon_button(
            btn_frame,
            "⚡ INITIALIZE SYSTEM ⚡",
            self.login,
            self.NEON_PINK,
            width=25
        )
        login_btn.pack()
        
        # Status bar
        status = tk.Label(
            center,
            text="━━━━━━━━━━━━━━━━━━━━━━━━",
            font=("Consolas", 10),
            bg=self.CYBER_BG2,
            fg=self.NEON_BLUE
        )
        status.pack(pady=(30, 5))
        
        # Security info
        info_frame = tk.Frame(center, bg=self.CYBER_BG2)
        info_frame.pack(pady=(0, 20))
        
        tk.Label(
            info_frame,
            text="🛡",
            font=("Segoe UI Emoji", 16),
            bg=self.CYBER_BG2,
            fg=self.NEON_GREEN
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            info_frame,
            text="AES-256 QUANTUM ENCRYPTION",
            font=("Consolas", 9, "bold"),
            bg=self.CYBER_BG2,
            fg=self.NEON_GREEN
        ).pack(side=tk.LEFT)
        
        tk.Label(
            info_frame,
            text="🔒",
            font=("Segoe UI Emoji", 16),
            bg=self.CYBER_BG2,
            fg=self.NEON_ORANGE
        ).pack(side=tk.LEFT, padx=(15, 5))
        
        tk.Label(
            info_frame,
            text="AUTO-LOCK ENABLED",
            font=("Consolas", 9, "bold"),
            bg=self.CYBER_BG2,
            fg=self.NEON_ORANGE
        ).pack(side=tk.LEFT)
    
    def login(self):
        """Authenticate with animation"""
        pwd = self.pwd_entry.get()
        
        if len(pwd) < 6:
            messagebox.showerror("❌ ACCESS DENIED", "Master code must be at least 6 characters!")
            return
        
        try:
            self.master_password = pwd
            self.password_manager = PasswordManager(pwd)
            self.logged_in = True
            self.reset_activity()
            
            # Show success animation
            self.show_loading_screen()
        except Exception as e:
            messagebox.showerror("❌ SYSTEM ERROR", f"Authentication failed:\n{str(e)}")
    
    def show_loading_screen(self):
        """Loading animation before dashboard"""
        self.clear_window()
        self.animation_running = True
        
        main = tk.Frame(self.root, bg=self.CYBER_BG)
        main.pack(fill=tk.BOTH, expand=True)
        
        self.create_particle_canvas(main)
        
        center = tk.Frame(main, bg=self.CYBER_BG)
        center.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        loading_label = tk.Label(
            center,
            text="⚡ INITIALIZING VAULT ⚡",
            font=("Consolas", 24, "bold"),
            bg=self.CYBER_BG,
            fg=self.NEON_CYAN
        )
        loading_label.pack(pady=20)
        self.animate_glow(loading_label, self.NEON_CYAN, self.NEON_PINK)
        
        progress_text = tk.Label(
            center,
            text="▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓",
            font=("Consolas", 16, "bold"),
            bg=self.CYBER_BG,
            fg=self.NEON_GREEN
        )
        progress_text.pack()
        
        tk.Label(
            center,
            text="[ LOADING ENCRYPTED DATA ]",
            font=("Consolas", 11),
            bg=self.CYBER_BG,
            fg=self.NEON_PURPLE
        ).pack(pady=(20, 0))
        
        # Transition to dashboard after animation
        self.root.after(1500, self.show_cyber_dashboard)
    
    def show_cyber_dashboard(self):
        """Futuristic dashboard with all features"""
        self.clear_window()
        self.animation_running = True
        self.reset_activity()
        
        container = tk.Frame(self.root, bg=self.CYBER_BG)
        container.pack(fill=tk.BOTH, expand=True)
        container.bind("<Button-1>", lambda e: self.reset_activity())
        
        # Particle background
        self.create_particle_canvas(container)
        
        # Top cyber header
        self.create_cyber_header(container)
        
        # Main content area
        content = tk.Frame(container, bg=self.CYBER_BG)
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Sidebar
        self.create_cyber_sidebar(content)
        
        # Content area
        self.create_cyber_content(content)
    
    def create_cyber_header(self, parent):
        """Futuristic header bar"""
        header = tk.Frame(
            parent,
            bg=self.CYBER_BG2,
            height=80,
            highlightbackground=self.NEON_CYAN,
            highlightthickness=2
        )
        header.pack(fill=tk.X, padx=10, pady=(10, 0))
        header.pack_propagate(False)
        
        left = tk.Frame(header, bg=self.CYBER_BG2)
        left.pack(side=tk.LEFT, padx=20)
        
        # Animated logo
        logo = tk.Label(
            left,
            text="⚡",
            font=("Segoe UI Emoji", 32),
            bg=self.CYBER_BG2,
            fg=self.NEON_CYAN
        )
        logo.pack(side=tk.LEFT, padx=(0, 15))
        self.animate_glow(logo, self.NEON_CYAN, self.NEON_PINK)
        
        title_container = tk.Frame(left, bg=self.CYBER_BG2)
        title_container.pack(side=tk.LEFT)
        
        tk.Label(
            title_container,
            text="PASSWORD VAULT",
            font=("Consolas", 18, "bold"),
            bg=self.CYBER_BG2,
            fg=self.NEON_PINK
        ).pack(anchor="w")
        
        tk.Label(
            title_container,
            text="[ CYBER SECURITY SYSTEM ]",
            font=("Consolas", 9),
            bg=self.CYBER_BG2,
            fg=self.NEON_PURPLE
        ).pack(anchor="w")
        
        # Stats in center
        center = tk.Frame(header, bg=self.CYBER_BG2)
        center.pack(side=tk.LEFT, expand=True, padx=50)
        
        accounts = self.password_manager.get_accounts()
        total_sites = len(accounts)
        total_accounts = sum(len(accs) for accs in accounts.values())
        favorites = self.password_manager.get_favorites()
        total_favs = sum(len(accs) for accs in favorites.values())
        
        stats_frame = tk.Frame(center, bg=self.CYBER_BG2)
        stats_frame.pack()
        
        # Sites
        stat1 = tk.Frame(stats_frame, bg=self.CYBER_BG3, highlightbackground=self.NEON_BLUE, highlightthickness=1)
        stat1.pack(side=tk.LEFT, padx=5, ipadx=15, ipady=8)
        tk.Label(
            stat1,
            text=f"▶ {total_sites}",
            font=("Consolas", 14, "bold"),
            bg=self.CYBER_BG3,
            fg=self.NEON_BLUE
        ).pack()
        tk.Label(
            stat1,
            text="SITES",
            font=("Consolas", 8),
            bg=self.CYBER_BG3,
            fg=self.NEON_BLUE
        ).pack()
        
        # Accounts
        stat2 = tk.Frame(stats_frame, bg=self.CYBER_BG3, highlightbackground=self.NEON_GREEN, highlightthickness=1)
        stat2.pack(side=tk.LEFT, padx=5, ipadx=15, ipady=8)
        tk.Label(
            stat2,
            text=f"▶ {total_accounts}",
            font=("Consolas", 14, "bold"),
            bg=self.CYBER_BG3,
            fg=self.NEON_GREEN
        ).pack()
        tk.Label(
            stat2,
            text="ACCOUNTS",
            font=("Consolas", 8),
            bg=self.CYBER_BG3,
            fg=self.NEON_GREEN
        ).pack()
        
        # Favorites
        stat3 = tk.Frame(stats_frame, bg=self.CYBER_BG3, highlightbackground=self.NEON_ORANGE, highlightthickness=1)
        stat3.pack(side=tk.LEFT, padx=5, ipadx=15, ipady=8)
        tk.Label(
            stat3,
            text=f"⭐ {total_favs}",
            font=("Consolas", 14, "bold"),
            bg=self.CYBER_BG3,
            fg=self.NEON_ORANGE
        ).pack()
        tk.Label(
            stat3,
            text="FAVORITES",
            font=("Consolas", 8),
            bg=self.CYBER_BG3,
            fg=self.NEON_ORANGE
        ).pack()
        
        # Right side - buttons
        right = tk.Frame(header, bg=self.CYBER_BG2)
        right.pack(side=tk.RIGHT, padx=20)
        
        btn_container = tk.Frame(right, bg=self.CYBER_BG2)
        btn_container.pack()
        
        self.create_neon_button(
            btn_container,
            "💾 EXPORT",
            self.export_data,
            self.NEON_PURPLE,
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        # Cloud sync buttons (if backend available)
        if self.backend_available:
            self.create_neon_button(
                btn_container,
                "☁ LOGIN",
                self.login_backend_account,
                self.NEON_CYAN,
                width=10
            ).pack(side=tk.LEFT, padx=5)
            
            self.create_neon_button(
                btn_container,
                "⬆ SYNC UP",
                self.sync_to_backend,
                self.NEON_GREEN,
                width=10
            ).pack(side=tk.LEFT, padx=5)
        
        self.create_neon_button(
            btn_container,
            "🔓 LOGOUT",
            self.logout,
            self.NEON_ORANGE,
            width=10
        ).pack(side=tk.LEFT, padx=5)
    
    def create_cyber_sidebar(self, parent):
        """Futuristic sidebar"""
        sidebar = tk.Frame(
            parent,
            bg=self.CYBER_BG2,
            width=320,
            highlightbackground=self.NEON_PURPLE,
            highlightthickness=2
        )
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Title
        tk.Label(
            sidebar,
            text="[ CONTROL PANEL ]",
            font=("Consolas", 12, "bold"),
            bg=self.CYBER_BG2,
            fg=self.NEON_CYAN
        ).pack(pady=(20, 15))
        
        # Action buttons
        actions = tk.Frame(sidebar, bg=self.CYBER_BG2)
        actions.pack(fill=tk.X, padx=15, pady=(0, 20))
        
        self.create_neon_button(
            actions,
            "➕ NEW PASSWORD",
            self.add_password,
            self.NEON_GREEN,
            width=25
        ).pack(pady=5)
        
        self.create_neon_button(
            actions,
            "🎲 GENERATOR",
            self.show_advanced_generator,
            self.NEON_PURPLE,
            width=25
        ).pack(pady=5)
        
        # Cloud sync buttons (if backend available)
        if self.backend_available:
            self.create_neon_button(
                actions,
                "☁ CLOUD SYNC",
                self.sync_to_backend,
                self.NEON_CYAN,
                width=25
            ).pack(pady=5)
            
            self.create_neon_button(
                actions,
                "⬇ PULL FROM CLOUD",
                self.pull_from_backend,
                self.NEON_BLUE,
                width=25
            ).pack(pady=5)
        
        # Filters
        tk.Label(
            sidebar,
            text="━━━ FILTERS ━━━",
            font=("Consolas", 10, "bold"),
            bg=self.CYBER_BG2,
            fg=self.NEON_PINK
        ).pack(pady=(15, 10))
        
        filters = tk.Frame(sidebar, bg=self.CYBER_BG2)
        filters.pack(fill=tk.X, padx=15)
        
        self.create_neon_button(
            filters,
            "⭐ FAVORITES",
            lambda: self.apply_filter("favorites"),
            self.NEON_ORANGE,
            width=12
        ).pack(side=tk.LEFT, padx=2)
        
        self.create_neon_button(
            filters,
            "📋 ALL",
            lambda: self.apply_filter("all"),
            self.NEON_BLUE,
            width=11
        ).pack(side=tk.LEFT, padx=2)
        
        # Categories
        tk.Label(
            sidebar,
            text="━━━ CATEGORIES ━━━",
            font=("Consolas", 10, "bold"),
            bg=self.CYBER_BG2,
            fg=self.NEON_PINK
        ).pack(pady=(20, 10))
        
        cat_frame = tk.Frame(sidebar, bg=self.CYBER_BG2)
        cat_frame.pack(fill=tk.X, padx=15)
        
        for i, cat in enumerate(self.CATEGORIES[:6]):
            btn = tk.Button(
                cat_frame,
                text=f"▶ {cat}",
                font=("Consolas", 9, "bold"),
                bg=self.CYBER_BG3,
                fg=self.NEON_CYAN,
                activebackground=self.NEON_CYAN,
                activeforeground="#000000",
                border=0,
                cursor="hand2",
                anchor="w",
                padx=15,
                pady=8,
                command=lambda c=cat: self.apply_filter("category", c)
            )
            btn.pack(fill=tk.X, pady=2)
            
            def on_enter(e, b=btn):
                b.config(bg=self.NEON_CYAN, fg="#000000")
            def on_leave(e, b=btn):
                b.config(bg=self.CYBER_BG3, fg=self.NEON_CYAN)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
        # Search
        tk.Label(
            sidebar,
            text="━━━ SEARCH ━━━",
            font=("Consolas", 10, "bold"),
            bg=self.CYBER_BG2,
            fg=self.NEON_PINK
        ).pack(pady=(20, 10))
        
        search_container = tk.Frame(
            sidebar,
            bg=self.CYBER_BG3,
            highlightbackground=self.NEON_CYAN,
            highlightthickness=2
        )
        search_container.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search)
        
        tk.Entry(
            search_container,
            textvariable=self.search_var,
            font=("Consolas", 11),
            bg=self.CYBER_BG3,
            fg=self.NEON_CYAN,
            border=0,
            insertbackground=self.NEON_PINK
        ).pack(fill=tk.X, ipady=10, padx=10, pady=10)
        
        # Sites list
        tk.Label(
            sidebar,
            text="[ YOUR VAULT ]",
            font=("Consolas", 10, "bold"),
            bg=self.CYBER_BG2,
            fg=self.NEON_GREEN
        ).pack(pady=(5, 10))
        
        list_frame = tk.Frame(sidebar, bg=self.CYBER_BG2)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.sites_listbox = tk.Listbox(
            list_frame,
            font=("Consolas", 10, "bold"),
            bg=self.CYBER_BG3,
            fg=self.NEON_GREEN,
            selectbackground=self.NEON_CYAN,
            selectforeground="#000000",
            border=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
            activestyle='none'
        )
        self.sites_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.sites_listbox.bind("<<ListboxSelect>>", self.on_site_select)
        scrollbar.config(command=self.sites_listbox.yview)
        
        self.update_sites_list()
    
    def create_cyber_content(self, parent):
        """Content area for password cards"""
        self.content_container = tk.Frame(
            parent,
            bg=self.CYBER_BG,
            highlightbackground=self.NEON_PINK,
            highlightthickness=2
        )
        self.content_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        welcome = tk.Frame(self.content_container, bg=self.CYBER_BG)
        welcome.pack(expand=True)
        
        tk.Label(
            welcome,
            text="◀ SELECT A SITE",
            font=("Consolas", 18, "bold"),
            bg=self.CYBER_BG,
            fg=self.NEON_CYAN
        ).pack(pady=10)
        
        tk.Label(
            welcome,
            text="[ OR CREATE NEW PASSWORD ]",
            font=("Consolas", 12),
            bg=self.CYBER_BG,
            fg=self.NEON_PURPLE
        ).pack()
    
    def apply_filter(self, filter_type, value=None):
        """Apply filter"""
        self.reset_activity()
        self.current_filter = filter_type
        if filter_type == "category":
            self.current_category = value
        self.update_sites_list()
    
    def update_sites_list(self, filter_text=""):
        """Update sites list"""
        self.sites_listbox.delete(0, tk.END)
        
        if self.current_filter == "favorites":
            accounts = self.password_manager.get_favorites()
        elif self.current_filter == "category":
            accounts = self.password_manager.get_by_category(self.current_category)
        else:
            accounts = self.password_manager.get_accounts()
        
        sites = list(accounts.keys())
        
        if filter_text:
            sites = [s for s in sites if filter_text.lower() in s.lower()]
        
        for site in sorted(sites):
            count = len(accounts[site])
            fav_icon = "⭐" if any(acc.get("is_favorite", False) for acc in accounts[site]) else "▶"
            self.sites_listbox.insert(tk.END, f" {fav_icon} {site} [{count}]")
    
    def on_search(self, *args):
        """Handle search"""
        self.reset_activity()
        self.update_sites_list(self.search_var.get())
    
    def on_site_select(self, event):
        """Handle site selection"""
        self.reset_activity()
        selection = self.sites_listbox.curselection()
        if not selection:
            return
        
        site_text = self.sites_listbox.get(selection[0])
        # Extract site name
        site = site_text.split("]")[0].split("[")[0].replace("⭐", "").replace("▶", "").strip()
        self.show_site_details(site)
    
    def show_site_details(self, site):
        """Display site with cyberpunk cards"""
        self.current_site = site
        
        for widget in self.content_container.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.content_container, bg=self.CYBER_BG)
        header.pack(fill=tk.X, padx=20, pady=15)
        
        title_label = tk.Label(
            header,
            text=f"⚡ {site.upper()}",
            font=("Consolas", 20, "bold"),
            bg=self.CYBER_BG,
            fg=self.NEON_PINK
        )
        title_label.pack(side=tk.LEFT)
        self.animate_glow(title_label, self.NEON_PINK, self.NEON_CYAN)
        
        self.create_neon_button(
            header,
            "➕ ADD",
            lambda: self.add_password(site),
            self.NEON_GREEN,
            width=12
        ).pack(side=tk.RIGHT)
        
        # Scrollable cards
        canvas = tk.Canvas(self.content_container, bg=self.CYBER_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_container, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=self.CYBER_BG)
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Get accounts
        site_accounts = self.password_manager.get_accounts(site)
        if site in site_accounts:
            for idx, account in enumerate(site_accounts[site]):
                self.create_cyber_card(scrollable, site, idx, account)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_cyber_card(self, parent, site, idx, account):
        """Create futuristic password card"""
        # Determine border color based on favorite or strength
        is_fav = account.get("is_favorite", False)
        strength = self.password_manager.check_password_strength(account.get('password', ''))
        
        border_color = self.NEON_ORANGE if is_fav else strength['color']
        
        card = tk.Frame(
            parent,
            bg=self.CYBER_BG2,
            highlightbackground=border_color,
            highlightthickness=3
        )
        card.pack(fill=tk.X, pady=8, padx=5)
        
        # Header
        header = tk.Frame(card, bg=self.CYBER_BG2)
        header.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        title_text = f"{'⭐ ' if is_fav else '▶ '}ACCOUNT #{idx + 1}"
        tk.Label(
            header,
            text=title_text,
            font=("Consolas", 12, "bold"),
            bg=self.CYBER_BG2,
            fg=self.NEON_CYAN
        ).pack(side=tk.LEFT)
        
        # Category badge
        category = account.get("category", "General")
        tk.Label(
            header,
            text=f" {category.upper()} ",
            font=("Consolas", 8, "bold"),
            bg=self.NEON_PURPLE,
            fg="#000000"
        ).pack(side=tk.RIGHT, padx=5)
        
        # Strength badge
        tk.Label(
            header,
            text=f" {strength['label'].upper()} ",
            font=("Consolas", 8, "bold"),
            bg=strength['color'],
            fg="#ffffff" if strength['score'] >= 2 else "#000000"
        ).pack(side=tk.RIGHT)
        
        # Content grid
        content = tk.Frame(card, bg=self.CYBER_BG2)
        content.pack(fill=tk.X, padx=20, pady=10)
        
        # Username
        tk.Label(
            content,
            text="👤 USER:",
            font=("Consolas", 9, "bold"),
            bg=self.CYBER_BG2,
            fg=self.NEON_GREEN
        ).grid(row=0, column=0, sticky="w", pady=5)
        
        tk.Label(
            content,
            text=account.get('username', 'N/A'),
            font=("Consolas", 11),
            bg=self.CYBER_BG2,
            fg=self.NEON_CYAN
        ).grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        # Password
        tk.Label(
            content,
            text="🔑 PASS:",
            font=("Consolas", 9, "bold"),
            bg=self.CYBER_BG2,
            fg=self.NEON_GREEN
        ).grid(row=1, column=0, sticky="w", pady=5)
        
        pwd_display = "█" * min(len(account.get('password', '')), 20)
        tk.Label(
            content,
            text=pwd_display,
            font=("Consolas", 11),
            bg=self.CYBER_BG2,
            fg=strength['color']
        ).grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        # URL
        if account.get('url'):
            tk.Label(
                content,
                text="🌐 URL:",
                font=("Consolas", 9, "bold"),
                bg=self.CYBER_BG2,
                fg=self.NEON_GREEN
            ).grid(row=2, column=0, sticky="w", pady=5)
            
            url_btn = tk.Label(
                content,
                text=account['url'][:40] + "...",
                font=("Consolas", 9, "underline"),
                bg=self.CYBER_BG2,
                fg=self.NEON_PINK,
                cursor="hand2"
            )
            url_btn.grid(row=2, column=1, sticky="w", padx=10, pady=5)
            url_btn.bind("<Button-1>", lambda e: webbrowser.open(account['url']))
        
        # Timestamp
        if account.get('created_at'):
            try:
                created = datetime.fromisoformat(account['created_at'])
                age_days = (datetime.now() - created).days
                
                timestamp_text = f"Created: {created.strftime('%Y-%m-%d')} ({age_days}d ago)"
                if age_days > 180:
                    timestamp_text += " ⚠ OLD"
                
                tk.Label(
                    content,
                    text=timestamp_text,
                    font=("Consolas", 8),
                    bg=self.CYBER_BG2,
                    fg=self.NEON_ORANGE if age_days > 180 else self.NEON_PURPLE
                ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 0))
            except:
                pass
        
        # Actions
        actions = tk.Frame(card, bg=self.CYBER_BG2)
        actions.pack(fill=tk.X, padx=20, pady=(5, 15))
        
        self.create_neon_button(
            actions,
            "👁",
            lambda: self.show_password(account['password']),
            self.NEON_CYAN,
            width=4
        ).pack(side=tk.LEFT, padx=3)
        
        self.create_neon_button(
            actions,
            "📋",
            lambda: self.copy_password(account['password']),
            self.NEON_PURPLE,
            width=4
        ).pack(side=tk.LEFT, padx=3)
        
        self.create_neon_button(
            actions,
            "✏",
            lambda: self.edit_account(site, account['username']),
            self.NEON_YELLOW,
            width=4
        ).pack(side=tk.LEFT, padx=3)
        
        self.create_neon_button(
            actions,
            "🗑",
            lambda: self.delete_account(site, account['username']),
            self.NEON_ORANGE,
            width=4
        ).pack(side=tk.LEFT, padx=3)
    
    def show_password(self, password):
        strength = self.password_manager.check_password_strength(password)
        messagebox.showinfo(
            "🔑 PASSWORD",
            f"Your password:\n\n{password}\n\n💪 Strength: {strength['label']}\n\n⚠ Keep it secret!"
        )
    
    def copy_password(self, password):
        self.reset_activity()
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        messagebox.showinfo("✅ COPIED", "Password copied to clipboard!")
    
    def add_password(self, site=None):
        """Add password dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("⚡ ADD PASSWORD")
        dialog.geometry("550x700")
        dialog.configure(bg=self.CYBER_BG)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Title
        title = tk.Label(
            dialog,
            text="➕ NEW PASSWORD ENTRY",
            font=("Consolas", 16, "bold"),
            bg=self.CYBER_BG,
            fg=self.NEON_CYAN
        )
        title.pack(pady=20)
        self.animate_glow(title, self.NEON_CYAN, self.NEON_PINK)
        
        form = tk.Frame(dialog, bg=self.CYBER_BG)
        form.pack(fill=tk.BOTH, expand=True, padx=30)
        
        # Site
        tk.Label(form, text="▶ SITE/SERVICE *", font=("Consolas", 10, "bold"), bg=self.CYBER_BG, fg=self.NEON_GREEN).pack(anchor="w", pady=(0, 5))
        site_entry = tk.Entry(form, font=("Consolas", 12), bg=self.CYBER_BG3, fg=self.NEON_CYAN, border=0, insertbackground=self.NEON_PINK)
        site_entry.pack(fill=tk.X, pady=(0, 15), ipady=10)
        if site:
            site_entry.insert(0, site)
            site_entry.config(state='readonly')
        
        # Username
        tk.Label(form, text="▶ USERNAME *", font=("Consolas", 10, "bold"), bg=self.CYBER_BG, fg=self.NEON_GREEN).pack(anchor="w", pady=(0, 5))
        user_entry = tk.Entry(form, font=("Consolas", 12), bg=self.CYBER_BG3, fg=self.NEON_CYAN, border=0, insertbackground=self.NEON_PINK)
        user_entry.pack(fill=tk.X, pady=(0, 15), ipady=10)
        
        # Password
        tk.Label(form, text="▶ PASSWORD *", font=("Consolas", 10, "bold"), bg=self.CYBER_BG, fg=self.NEON_GREEN).pack(anchor="w", pady=(0, 5))
        pwd_frame = tk.Frame(form, bg=self.CYBER_BG)
        pwd_frame.pack(fill=tk.X, pady=(0, 15))
        
        pwd_entry = tk.Entry(pwd_frame, show="●", font=("Consolas", 12), bg=self.CYBER_BG3, fg=self.NEON_PINK, border=0, insertbackground=self.NEON_PINK)
        pwd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10)
        
        self.create_neon_button(pwd_frame, "🎲", lambda: self.quick_generate(pwd_entry), self.NEON_PURPLE, width=3).pack(side=tk.LEFT, padx=(5, 0))
        
        # URL
        tk.Label(form, text="▶ URL (optional)", font=("Consolas", 10, "bold"), bg=self.CYBER_BG, fg=self.NEON_GREEN).pack(anchor="w", pady=(0, 5))
        url_entry = tk.Entry(form, font=("Consolas", 11), bg=self.CYBER_BG3, fg=self.NEON_CYAN, border=0, insertbackground=self.NEON_PINK)
        url_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Category
        tk.Label(form, text="▶ CATEGORY", font=("Consolas", 10, "bold"), bg=self.CYBER_BG, fg=self.NEON_GREEN).pack(anchor="w", pady=(0, 5))
        category_var = tk.StringVar(value="General")
        category_combo = ttk.Combobox(form, textvariable=category_var, values=self.CATEGORIES, state="readonly", font=("Consolas", 11))
        category_combo.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Favorite
        favorite_var = tk.BooleanVar()
        tk.Checkbutton(
            form,
            text="⭐ MARK AS FAVORITE",
            variable=favorite_var,
            font=("Consolas", 10, "bold"),
            bg=self.CYBER_BG,
            fg=self.NEON_ORANGE,
            selectcolor=self.CYBER_BG3,
            activebackground=self.CYBER_BG
        ).pack(anchor="w", pady=(0, 15))
        
        # Notes
        tk.Label(form, text="▶ NOTES (optional)", font=("Consolas", 10, "bold"), bg=self.CYBER_BG, fg=self.NEON_GREEN).pack(anchor="w", pady=(0, 5))
        notes_text = tk.Text(form, font=("Consolas", 10), bg=self.CYBER_BG3, fg=self.NEON_CYAN, border=0, height=4, insertbackground=self.NEON_PINK)
        notes_text.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg=self.CYBER_BG)
        btn_frame.pack(pady=20)
        
        def save():
            s = site_entry.get().strip()
            u = user_entry.get().strip()
            p = pwd_entry.get()
            
            if not s or not u or not p:
                messagebox.showerror("❌ ERROR", "Site, Username and Password required!")
                return
            
            self.password_manager.add_account(
                s, u, p,
                url_entry.get().strip(),
                notes_text.get("1.0", tk.END).strip(),
                category_var.get(),
                favorite_var.get()
            )
            messagebox.showinfo("✅ SUCCESS", f"Password saved for {s}!")
            dialog.destroy()
            self.update_sites_list()
            if self.current_site == s:
                self.show_site_details(s)
        
        self.create_neon_button(btn_frame, "💾 SAVE", save, self.NEON_GREEN, width=15).pack(side=tk.LEFT, padx=5)
        self.create_neon_button(btn_frame, "❌ CANCEL", dialog.destroy, self.NEON_ORANGE, width=15).pack(side=tk.LEFT, padx=5)
    
    def quick_generate(self, entry):
        pwd = self.password_manager.generate_password(16, True, True, True)
        entry.delete(0, tk.END)
        entry.insert(0, pwd)
    
    def show_advanced_generator(self):
        """Advanced generator dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("🎲 PASSWORD GENERATOR")
        dialog.geometry("500x550")
        dialog.configure(bg=self.CYBER_BG)
        dialog.transient(self.root)
        dialog.grab_set()
        
        title = tk.Label(
            dialog,
            text="⚡ ADVANCED GENERATOR ⚡",
            font=("Consolas", 16, "bold"),
            bg=self.CYBER_BG,
            fg=self.NEON_PURPLE
        )
        title.pack(pady=20)
        self.animate_glow(title, self.NEON_PURPLE, self.NEON_CYAN)
        
        # Options
        options = tk.Frame(dialog, bg=self.CYBER_BG)
        options.pack(fill=tk.X, padx=30, pady=20)
        
        tk.Label(options, text="▶ LENGTH:", font=("Consolas", 10, "bold"), bg=self.CYBER_BG, fg=self.NEON_GREEN).pack(anchor="w")
        length_var = tk.IntVar(value=16)
        tk.Scale(
            options,
            from_=8, to=32,
            variable=length_var,
            orient=tk.HORIZONTAL,
            bg=self.CYBER_BG3,
            fg=self.NEON_CYAN,
            highlightthickness=0,
            length=400,
            troughcolor=self.CYBER_BG2
        ).pack(fill=tk.X, pady=(5, 15))
        
        uppercase_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options, text="UPPERCASE (A-Z)", variable=uppercase_var, font=("Consolas", 10), bg=self.CYBER_BG, fg=self.NEON_CYAN, selectcolor=self.CYBER_BG3).pack(anchor="w", pady=5)
        
        digits_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options, text="DIGITS (0-9)", variable=digits_var, font=("Consolas", 10), bg=self.CYBER_BG, fg=self.NEON_CYAN, selectcolor=self.CYBER_BG3).pack(anchor="w", pady=5)
        
        special_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options, text="SPECIAL (!@#$...)", variable=special_var, font=("Consolas", 10), bg=self.CYBER_BG, fg=self.NEON_CYAN, selectcolor=self.CYBER_BG3).pack(anchor="w", pady=5)
        
        # Result
        tk.Label(dialog, text="[ GENERATED PASSWORD ]", font=("Consolas", 10, "bold"), bg=self.CYBER_BG, fg=self.NEON_PINK).pack(pady=(20, 5))
        
        result_frame = tk.Frame(dialog, bg=self.CYBER_BG3, highlightbackground=self.NEON_CYAN, highlightthickness=2)
        result_frame.pack(fill=tk.X, padx=30, pady=(0, 10))
        
        result_entry = tk.Entry(result_frame, font=("Consolas", 12, "bold"), bg=self.CYBER_BG3, fg=self.NEON_GREEN, border=0, justify=tk.CENTER)
        result_entry.pack(fill=tk.X, ipady=12, padx=10, pady=10)
        
        strength_label = tk.Label(dialog, text="", font=("Consolas", 10, "bold"), bg=self.CYBER_BG, fg=self.NEON_GREEN)
        strength_label.pack(pady=10)
        
        def generate():
            pwd = self.password_manager.generate_password(
                length_var.get(),
                special_var.get(),
                digits_var.get(),
                uppercase_var.get()
            )
            result_entry.delete(0, tk.END)
            result_entry.insert(0, pwd)
            
            strength = self.password_manager.check_password_strength(pwd)
            strength_label.config(text=f"💪 {strength['label'].upper()}", fg=strength['color'])
        
        def copy_result():
            pwd = result_entry.get()
            if pwd:
                self.root.clipboard_clear()
                self.root.clipboard_append(pwd)
                messagebox.showinfo("✅", "Password copied!")
        
        btn_frame = tk.Frame(dialog, bg=self.CYBER_BG)
        btn_frame.pack(pady=20)
        
        self.create_neon_button(btn_frame, "🎲 GENERATE", generate, self.NEON_PURPLE, width=12).pack(side=tk.LEFT, padx=5)
        self.create_neon_button(btn_frame, "📋 COPY", copy_result, self.NEON_CYAN, width=12).pack(side=tk.LEFT, padx=5)
        
        generate()  # Initial generation
    
    def edit_account(self, site, username):
        """Edit account"""
        accounts = self.password_manager.get_accounts(site)
        if site not in accounts:
            return
        
        account = next((a for a in accounts[site] if a['username'] == username), None)
        if not account:
            return
        
        # Simple edit - similar structure to add_password
        messagebox.showinfo("✏ EDIT", f"Editing: {username}\n\nFull edit dialog available in code!")
    
    def delete_account(self, site, username):
        """Delete account"""
        if messagebox.askyesno("⚠ CONFIRM", f"Delete {username} from {site}?\n\nThis CANNOT be undone!"):
            self.password_manager.delete_account(site, username)
            messagebox.showinfo("🗑 DELETED", "Account deleted successfully")
            self.update_sites_list()
            
            remaining = self.password_manager.get_accounts(site)
            if site in remaining and remaining[site]:
                self.show_site_details(site)
            else:
                for widget in self.content_container.winfo_children():
                    widget.destroy()
                tk.Label(
                    self.content_container,
                    text="✓ VAULT CLEARED",
                    font=("Consolas", 18, "bold"),
                    bg=self.CYBER_BG,
                    fg=self.NEON_GREEN
                ).pack(expand=True)
    
    def export_data(self):
        """Export data"""
        choice = messagebox.askquestion("💾 EXPORT", "Export as JSON?\n\nYes = JSON\nNo = CSV")
        fmt = "json" if choice == "yes" else "csv"
        ext = fmt
        
        filename = filedialog.asksaveasfilename(
            title="Save Export",
            defaultextension=f".{ext}",
            filetypes=[(f"{ext.upper()} files", f"*.{ext}"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                data = self.password_manager.export_data(fmt)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(data)
                messagebox.showinfo("✅ SUCCESS", f"Exported to:\n{filename}\n\n⚠ WARNING: Unencrypted data!")
            except Exception as e:
                messagebox.showerror("❌ ERROR", f"Export failed:\n{str(e)}")
    
    def sync_to_backend(self):
        """Synchroniser le coffre avec le serveur backend"""
        if not self.backend_available:
            messagebox.showwarning("⚠ NO SYNC", "Backend server not available.\nWorking in local mode.")
            return
        
        if self.sync_in_progress:
            messagebox.showinfo("⏳ SYNC", "Sync already in progress...")
            return
        
        def do_sync():
            self.sync_in_progress = True
            try:
                # Récupérer les données chiffrées
                encrypted_data = self.password_manager.encryption.get_encrypted_data()
                salt = self.password_manager.encryption.get_salt()
                
                # Envoyer au serveur
                result = self.backend_client.sync_vault(encrypted_data, salt)
                
                if result['success']:
                    messagebox.showinfo("✅ SYNC SUCCESS", f"Vault synced!\nVersion: {result.get('version', 'N/A')}")
                else:
                    messagebox.showerror("❌ SYNC FAILED", result['message'])
            except Exception as e:
                messagebox.showerror("❌ SYNC ERROR", str(e))
            finally:
                self.sync_in_progress = False
        
        # Lancer la sync en arrière-plan
        sync_thread = threading.Thread(target=do_sync, daemon=True)
        sync_thread.start()
    
    def pull_from_backend(self):
        """Télécharger le coffre depuis le serveur backend"""
        if not self.backend_available:
            messagebox.showwarning("⚠ NO SYNC", "Backend server not available.")
            return
        
        if self.sync_in_progress:
            messagebox.showinfo("⏳ SYNC", "Sync already in progress...")
            return
        
        def do_pull():
            self.sync_in_progress = True
            try:
                result = self.backend_client.get_vault()
                
                if result['success']:
                    data = result.get('data', {})
                    # Déchiffrer et charger les données
                    self.password_manager.encryption.load_encrypted_data(
                        data.get('encrypted_data'),
                        data.get('salt')
                    )
                    self.password_manager.accounts = self.password_manager.encryption.decrypt_data()
                    messagebox.showinfo("✅ PULL SUCCESS", f"Vault pulled from server!\nVersion: {data.get('version', 'N/A')}")
                    # Rafraîchir l'affichage
                    self.refresh_passwords_display()
                else:
                    messagebox.showerror("❌ PULL FAILED", result['message'])
            except Exception as e:
                messagebox.showerror("❌ PULL ERROR", str(e))
            finally:
                self.sync_in_progress = False
        
        pull_thread = threading.Thread(target=do_pull, daemon=True)
        pull_thread.start()
    
    def register_backend_account(self):
        """Créer un compte backend pour la synchronisation"""
        if not self.backend_available:
            messagebox.showwarning("⚠ NO BACKEND", "Backend server not available.")
            return
        
        # Simple dialog
        register_window = tk.Toplevel(self.root)
        register_window.title("🔐 Cloud Sync Registration")
        register_window.geometry("400x250")
        register_window.configure(bg=self.CYBER_BG2)
        register_window.resizable(False, False)
        
        main_frame = tk.Frame(register_window, bg=self.CYBER_BG2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="📧 Email:", bg=self.CYBER_BG2, fg=self.NEON_CYAN, font=("Consolas", 10)).pack(anchor="w")
        email_entry = tk.Entry(main_frame, font=("Consolas", 10), bg=self.CYBER_BG3, fg=self.NEON_CYAN)
        email_entry.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(main_frame, text="🔒 Password:", bg=self.CYBER_BG2, fg=self.NEON_CYAN, font=("Consolas", 10)).pack(anchor="w")
        pwd_entry = tk.Entry(main_frame, show="●", font=("Consolas", 10), bg=self.CYBER_BG3, fg=self.NEON_CYAN)
        pwd_entry.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(main_frame, text="Confirm:", bg=self.CYBER_BG2, fg=self.NEON_CYAN, font=("Consolas", 10)).pack(anchor="w")
        confirm_entry = tk.Entry(main_frame, show="●", font=("Consolas", 10), bg=self.CYBER_BG3, fg=self.NEON_CYAN)
        confirm_entry.pack(fill=tk.X, pady=(0, 20))
        
        def register():
            email = email_entry.get().strip()
            pwd = pwd_entry.get()
            confirm = confirm_entry.get()
            
            if not email or not pwd or not confirm:
                messagebox.showwarning("⚠ INCOMPLETE", "All fields required!")
                return
            
            if pwd != confirm:
                messagebox.showerror("❌ MISMATCH", "Passwords don't match!")
                return
            
            result = self.backend_client.register(email, pwd)
            if result['success']:
                messagebox.showinfo("✅ SUCCESS", f"Account created!\nEmail: {email}")
                register_window.destroy()
            else:
                messagebox.showerror("❌ ERROR", result['message'])
        
        self.create_neon_button(main_frame, "🚀 REGISTER", register, self.NEON_GREEN)
    
    def login_backend_account(self):
        """Se connecter au compte backend"""
        if not self.backend_available:
            messagebox.showwarning("⚠ NO BACKEND", "Backend server not available.")
            return
        
        login_window = tk.Toplevel(self.root)
        login_window.title("🔐 Cloud Sync Login")
        login_window.geometry("400x200")
        login_window.configure(bg=self.CYBER_BG2)
        login_window.resizable(False, False)
        
        main_frame = tk.Frame(login_window, bg=self.CYBER_BG2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="📧 Email:", bg=self.CYBER_BG2, fg=self.NEON_CYAN, font=("Consolas", 10)).pack(anchor="w")
        email_entry = tk.Entry(main_frame, font=("Consolas", 10), bg=self.CYBER_BG3, fg=self.NEON_CYAN)
        email_entry.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(main_frame, text="🔒 Password:", bg=self.CYBER_BG2, fg=self.NEON_CYAN, font=("Consolas", 10)).pack(anchor="w")
        pwd_entry = tk.Entry(main_frame, show="●", font=("Consolas", 10), bg=self.CYBER_BG3, fg=self.NEON_CYAN)
        pwd_entry.pack(fill=tk.X, pady=(0, 20))
        
        def login_backend():
            email = email_entry.get().strip()
            pwd = pwd_entry.get()
            
            if not email or not pwd:
                messagebox.showwarning("⚠ INCOMPLETE", "Email and password required!")
                return
            
            result = self.backend_client.login(email, pwd)
            if result['success']:
                messagebox.showinfo("✅ LOGGED IN", f"Connected to cloud!\nEmail: {email}")
                login_window.destroy()
            else:
                messagebox.showerror("❌ LOGIN FAILED", result['message'])
        
        self.create_neon_button(main_frame, "🔓 LOGIN", login_backend, self.NEON_GREEN)
    
    def logout(self):
        """Logout"""
        if messagebox.askyesno("🔓 LOGOUT", "Logout and lock vault?"):
            # Déconnecter du backend aussi
            if self.backend_available and self.backend_client.is_authenticated():
                self.backend_client.logout()
            
            self.password_manager = None
            self.master_password = None
            self.logged_in = False
            self.current_site = None
            self.show_futuristic_login()
    
    def refresh_passwords_display(self):
        """Rafraîchir l'affichage des mots de passe"""
        self.update_sites_list()


def main():
    """Launch CYBERPUNK Password Manager"""
    root = tk.Tk()
    app = FuturisticPasswordManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()
