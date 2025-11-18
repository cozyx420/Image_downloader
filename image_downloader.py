"""
Image Downloader Tool
Ein einfaches Desktop-Tool zum Herunterladen aller Bilder von einer Webseite.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import threading

class ImageDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Bilder Downloader")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # URL Eingabe
        tk.Label(root, text="Webseiten-URL:", font=("Arial", 10)).pack(pady=(20,5))
        self.url_entry = tk.Entry(root, width=60, font=("Arial", 10))
        self.url_entry.pack(pady=5)
        
        # Zielordner Auswahl
        tk.Label(root, text="Zielordner:", font=("Arial", 10)).pack(pady=(20,5))
        
        folder_frame = tk.Frame(root)
        folder_frame.pack(pady=5)
        
        self.folder_entry = tk.Entry(folder_frame, width=45, font=("Arial", 10))
        self.folder_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(folder_frame, text="Durchsuchen", command=self.select_folder).pack(side=tk.LEFT)
        
        # Namensschema Auswahl
        tk.Label(root, text="Namensschema:", font=("Arial", 10)).pack(pady=(20,5))
        
        self.naming_var = tk.StringVar(value="original")
        
        radio_frame = tk.Frame(root)
        radio_frame.pack(pady=5)
        
        tk.Radiobutton(radio_frame, text="Original-Namen", variable=self.naming_var, 
                      value="original", font=("Arial", 10)).pack(side=tk.LEFT, padx=20)
        tk.Radiobutton(radio_frame, text="SEITENNAME-000", variable=self.naming_var, 
                      value="numbered", font=("Arial", 10)).pack(side=tk.LEFT, padx=20)
        
        # Download Button
        self.download_btn = tk.Button(root, text="Bilder herunterladen", 
                                      command=self.start_download, 
                                      font=("Arial", 11, "bold"),
                                      bg="#4CAF50", fg="white",
                                      padx=20, pady=10)
        self.download_btn.pack(pady=30)
        
        # Fortschrittsanzeige
        self.progress_label = tk.Label(root, text="", font=("Arial", 9))
        self.progress_label.pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(root, length=500, mode='determinate')
        self.progress_bar.pack(pady=5)
        
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)
    
    def get_page_name(self, url):
        parsed = urlparse(url)
        domain = parsed.netloc.replace('www.', '').replace('.', '_')
        return domain
    
    def download_images(self):
        url = self.url_entry.get().strip()
        folder = self.folder_entry.get().strip()
        
        if not url or not folder:
            messagebox.showerror("Fehler", "Bitte URL und Zielordner angeben!")
            return
        
        if not os.path.exists(folder):
            messagebox.showerror("Fehler", "Der Zielordner existiert nicht!")
            return
        
        try:
            self.progress_label.config(text="Lade Webseite...")
            self.download_btn.config(state=tk.DISABLED)
            
            # Webseite abrufen
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Alle Bilder finden
            img_tags = soup.find_all('img')
            
            if not img_tags:
                messagebox.showinfo("Info", "Keine Bilder auf der Seite gefunden!")
                self.download_btn.config(state=tk.NORMAL)
                self.progress_label.config(text="")
                return
            
            # Fortschrittsbalken vorbereiten
            self.progress_bar['maximum'] = len(img_tags)
            self.progress_bar['value'] = 0
            
            page_name = self.get_page_name(url)
            downloaded = 0
            
            for idx, img in enumerate(img_tags, 1):
                img_url = img.get('src')
                if not img_url:
                    continue
                
                # Relative URLs zu absoluten machen
                img_url = urljoin(url, img_url)
                
                try:
                    img_response = requests.get(img_url, headers=headers, timeout=10)
                    img_response.raise_for_status()
                    
                    # Dateiname bestimmen
                    if self.naming_var.get() == "original":
                        filename = os.path.basename(urlparse(img_url).path)
                        if not filename:
                            filename = f"image_{idx}.jpg"
                    else:
                        ext = os.path.splitext(urlparse(img_url).path)[1] or '.jpg'
                        filename = f"{page_name}-{idx:03d}{ext}"
                    
                    # Datei speichern
                    filepath = os.path.join(folder, filename)
                    
                    # Doppelte Dateinamen vermeiden
                    counter = 1
                    base_name, ext = os.path.splitext(filename)
                    while os.path.exists(filepath):
                        filename = f"{base_name}_{counter}{ext}"
                        filepath = os.path.join(folder, filename)
                        counter += 1
                    
                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)
                    
                    downloaded += 1
                    self.progress_label.config(text=f"Heruntergeladen: {downloaded}/{len(img_tags)}")
                    self.progress_bar['value'] = idx
                    self.root.update_idletasks()
                    
                except Exception as e:
                    print(f"Fehler beim Herunterladen von {img_url}: {e}")
                    continue
            
            messagebox.showinfo("Fertig", f"{downloaded} Bilder erfolgreich heruntergeladen!")
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Webseite:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{str(e)}")
        finally:
            self.download_btn.config(state=tk.NORMAL)
            self.progress_label.config(text="")
            self.progress_bar['value'] = 0
    
    def start_download(self):
        # Download in separatem Thread starten
        thread = threading.Thread(target=self.download_images)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDownloader(root)
    root.mainloop()
