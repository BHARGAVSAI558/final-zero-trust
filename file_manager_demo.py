"""
Zero Trust File Manager - Demo Tool
Interactive file operations with recycle bin
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
import shutil
import requests
from datetime import datetime

BACKEND_URL = "http://localhost:8000"
DEMO_FILES_DIR = "demo_files"
RECYCLE_BIN_DIR = "demo_files/recycle_bin"

class FileManagerDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Zero Trust File Manager - Demo")
        self.root.geometry("1200x700")
        self.root.configure(bg='#0a0e27')
        
        self.username = "mahesh"  # Demo user
        self.current_file = None
        
        self.create_ui()
        self.load_files()
        
    def create_ui(self):
        # Header
        header = tk.Frame(self.root, bg='#1a1f3a', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="📁 FILE MANAGER", font=('Arial', 20, 'bold'),
                bg='#1a1f3a', fg='#00d4ff').pack(side='left', padx=20)
        
        tk.Label(header, text=f"User: {self.username}", font=('Arial', 12),
                bg='#1a1f3a', fg='#00ff88').pack(side='right', padx=20)
        
        # Main container
        main = tk.Frame(self.root, bg='#0a0e27')
        main.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - File list
        left = tk.Frame(main, bg='#1a1f3a', width=400)
        left.pack(side='left', fill='both', padx=(0,5))
        
        tk.Label(left, text="MY FILES", font=('Arial', 14, 'bold'),
                bg='#1a1f3a', fg='#00d4ff').pack(pady=10)
        
        # File listbox
        list_frame = tk.Frame(left, bg='#0a0e27')
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.file_listbox = tk.Listbox(list_frame, font=('Consolas', 10),
                                       bg='#0a0e27', fg='#00d4ff',
                                       selectbackground='#00d4ff',
                                       selectforeground='#000000',
                                       yscrollcommand=scrollbar.set,
                                       height=20)
        self.file_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
        # Buttons
        btn_frame = tk.Frame(left, bg='#1a1f3a')
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text="🔄 REFRESH", command=self.load_files,
                 bg='#00d4ff', fg='#000000', font=('Arial', 10, 'bold'),
                 relief='flat', cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="🗑️ RECYCLE BIN", command=self.show_recycle_bin,
                 bg='#ff9500', fg='#000000', font=('Arial', 10, 'bold'),
                 relief='flat', cursor='hand2').pack(side='left', padx=5)
        
        # Right panel - File viewer/editor
        right = tk.Frame(main, bg='#1a1f3a')
        right.pack(side='right', fill='both', expand=True, padx=(5,0))
        
        # File info
        info_frame = tk.Frame(right, bg='#1a1f3a')
        info_frame.pack(fill='x', padx=10, pady=10)
        
        self.file_name_label = tk.Label(info_frame, text="No file selected",
                                        font=('Arial', 14, 'bold'),
                                        bg='#1a1f3a', fg='#00ff88')
        self.file_name_label.pack(side='left')
        
        self.sensitivity_label = tk.Label(info_frame, text="",
                                          font=('Arial', 10),
                                          bg='#1a1f3a', fg='#ff9500')
        self.sensitivity_label.pack(side='right')
        
        # Text editor
        self.text_editor = scrolledtext.ScrolledText(right, font=('Consolas', 10),
                                                     bg='#0a0e27', fg='#ffffff',
                                                     wrap='word', height=25)
        self.text_editor.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Action buttons
        action_frame = tk.Frame(right, bg='#1a1f3a')
        action_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(action_frame, text="📖 OPEN", command=self.open_file,
                 bg='#00d4ff', fg='#000000', font=('Arial', 10, 'bold'),
                 relief='flat', cursor='hand2', width=12).pack(side='left', padx=5)
        
        tk.Button(action_frame, text="✏️ EDIT", command=self.edit_file,
                 bg='#00ff88', fg='#000000', font=('Arial', 10, 'bold'),
                 relief='flat', cursor='hand2', width=12).pack(side='left', padx=5)
        
        tk.Button(action_frame, text="💾 SAVE", command=self.save_file,
                 bg='#22c55e', fg='#000000', font=('Arial', 10, 'bold'),
                 relief='flat', cursor='hand2', width=12).pack(side='left', padx=5)
        
        tk.Button(action_frame, text="🗑️ DELETE", command=self.delete_file,
                 bg='#ff4444', fg='#ffffff', font=('Arial', 10, 'bold'),
                 relief='flat', cursor='hand2', width=12).pack(side='left', padx=5)
        
    def load_files(self):
        """Load files from demo directory"""
        self.file_listbox.delete(0, tk.END)
        
        if not os.path.exists(DEMO_FILES_DIR):
            return
        
        files = []
        for filename in os.listdir(DEMO_FILES_DIR):
            filepath = os.path.join(DEMO_FILES_DIR, filename)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                files.append((filename, size))
        
        for filename, size in sorted(files):
            display = f"{filename:30} ({size} bytes)"
            self.file_listbox.insert(tk.END, display)
    
    def on_file_select(self, event):
        """Handle file selection"""
        selection = self.file_listbox.curselection()
        if selection:
            text = self.file_listbox.get(selection[0])
            self.current_file = text.split()[0]
            self.file_name_label.config(text=self.current_file)
            
            # Show sensitivity
            sensitivity_map = {
                "dashboard.html": "PUBLIC",
                "reports.pdf": "INTERNAL",
                "analytics.xlsx": "INTERNAL",
                "profile.json": "PUBLIC",
                "admin.config": "SENSITIVE",
                "credentials.txt": "SENSITIVE",
                "database.sql": "CRITICAL",
                "secrets.env": "CRITICAL"
            }
            sensitivity = sensitivity_map.get(self.current_file, "INTERNAL")
            color = {"PUBLIC": "#00ff88", "INTERNAL": "#00d4ff", 
                    "SENSITIVE": "#ff9500", "CRITICAL": "#ff4444"}
            self.sensitivity_label.config(text=f"[{sensitivity}]", 
                                         fg=color.get(sensitivity, "#ffffff"))
    
    def open_file(self):
        """Open and read file"""
        if not self.current_file:
            messagebox.showwarning("No File", "Please select a file first")
            return
        
        filepath = os.path.join(DEMO_FILES_DIR, self.current_file)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            self.text_editor.delete('1.0', tk.END)
            self.text_editor.insert('1.0', content)
            self.text_editor.config(state='disabled')
            
            # Log to backend
            try:
                requests.post(f"{BACKEND_URL}/files/access", json={
                    "user_id": self.username,
                    "file_name": self.current_file,
                    "action": "READ"
                }, timeout=2)
            except:
                pass
            
            messagebox.showinfo("Success", f"Opened {self.current_file}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def edit_file(self):
        """Enable editing"""
        if not self.current_file:
            messagebox.showwarning("No File", "Please select a file first")
            return
        
        self.text_editor.config(state='normal')
        messagebox.showinfo("Edit Mode", "You can now edit the file. Click SAVE when done.")
    
    def save_file(self):
        """Save file changes"""
        if not self.current_file:
            messagebox.showwarning("No File", "Please select a file first")
            return
        
        filepath = os.path.join(DEMO_FILES_DIR, self.current_file)
        try:
            content = self.text_editor.get('1.0', tk.END)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.text_editor.config(state='disabled')
            
            # Log to backend
            try:
                requests.post(f"{BACKEND_URL}/files/access", json={
                    "user_id": self.username,
                    "file_name": self.current_file,
                    "action": "WRITE"
                }, timeout=2)
            except:
                pass
            
            messagebox.showinfo("Success", f"Saved {self.current_file}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_file(self):
        """Move file to recycle bin"""
        if not self.current_file:
            messagebox.showwarning("No File", "Please select a file first")
            return
        
        if not messagebox.askyesno("Confirm Delete", 
                                   f"Move {self.current_file} to recycle bin?"):
            return
        
        filepath = os.path.join(DEMO_FILES_DIR, self.current_file)
        try:
            # Move to recycle bin with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            recycled_name = f"{timestamp}_{self.current_file}"
            recycle_path = os.path.join(RECYCLE_BIN_DIR, recycled_name)
            
            os.makedirs(RECYCLE_BIN_DIR, exist_ok=True)
            shutil.move(filepath, recycle_path)
            
            # Log to backend
            try:
                requests.post(f"{BACKEND_URL}/files/access", json={
                    "user_id": self.username,
                    "file_name": self.current_file,
                    "action": "DELETE"
                }, timeout=2)
            except:
                pass
            
            self.text_editor.delete('1.0', tk.END)
            self.current_file = None
            self.file_name_label.config(text="No file selected")
            self.load_files()
            
            messagebox.showinfo("Success", "File moved to recycle bin")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def show_recycle_bin(self):
        """Show recycle bin window"""
        RecycleBinWindow(self.root, self)

class RecycleBinWindow:
    def __init__(self, parent, file_manager):
        self.window = tk.Toplevel(parent)
        self.window.title("Recycle Bin")
        self.window.geometry("600x400")
        self.window.configure(bg='#0a0e27')
        self.file_manager = file_manager
        
        # Header
        tk.Label(self.window, text="🗑️ RECYCLE BIN", font=('Arial', 16, 'bold'),
                bg='#0a0e27', fg='#ff9500').pack(pady=10)
        
        # Listbox
        list_frame = tk.Frame(self.window, bg='#0a0e27')
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.listbox = tk.Listbox(list_frame, font=('Consolas', 10),
                                  bg='#1a1f3a', fg='#ffffff',
                                  selectbackground='#00d4ff',
                                  yscrollcommand=scrollbar.set)
        self.listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Buttons
        btn_frame = tk.Frame(self.window, bg='#0a0e27')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="♻️ RESTORE", command=self.restore_file,
                 bg='#00ff88', fg='#000000', font=('Arial', 10, 'bold'),
                 relief='flat', cursor='hand2', width=15).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="🗑️ DELETE FOREVER", command=self.permanent_delete,
                 bg='#ff4444', fg='#ffffff', font=('Arial', 10, 'bold'),
                 relief='flat', cursor='hand2', width=15).pack(side='left', padx=5)
        
        self.load_recycle_bin()
    
    def load_recycle_bin(self):
        """Load files from recycle bin"""
        self.listbox.delete(0, tk.END)
        
        if not os.path.exists(RECYCLE_BIN_DIR):
            return
        
        for filename in os.listdir(RECYCLE_BIN_DIR):
            self.listbox.insert(tk.END, filename)
    
    def restore_file(self):
        """Restore file from recycle bin"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No File", "Please select a file to restore")
            return
        
        filename = self.listbox.get(selection[0])
        original_name = "_".join(filename.split("_")[2:])
        
        recycle_path = os.path.join(RECYCLE_BIN_DIR, filename)
        restore_path = os.path.join(DEMO_FILES_DIR, original_name)
        
        if os.path.exists(restore_path):
            messagebox.showerror("Error", f"{original_name} already exists")
            return
        
        try:
            shutil.move(recycle_path, restore_path)
            self.load_recycle_bin()
            self.file_manager.load_files()
            messagebox.showinfo("Success", f"Restored {original_name}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def permanent_delete(self):
        """Permanently delete file"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No File", "Please select a file to delete")
            return
        
        filename = self.listbox.get(selection[0])
        
        if not messagebox.askyesno("Confirm", 
                                   f"Permanently delete {filename}?\nThis cannot be undone!"):
            return
        
        recycle_path = os.path.join(RECYCLE_BIN_DIR, filename)
        try:
            os.remove(recycle_path)
            self.load_recycle_bin()
            messagebox.showinfo("Success", "File permanently deleted")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerDemo(root)
    root.mainloop()
