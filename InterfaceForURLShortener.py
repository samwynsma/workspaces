import os
import sys
import urllib.parse
import tkinter as tk
from tkinter import messagebox

class UserInterface:

    def __init__(self):
        self.urlText = ""

    def normalize_url(self, url: str) -> str | None:
        """Normalize and validate a URL string.

        Returns a normalized URL (with scheme) if valid, otherwise None.
        """
        if not url:
            return None
        url = url.strip()
        # Reject whitespace-containing strings
        if " " in url:
            return None

        parsed = urllib.parse.urlparse(url)
        # If no scheme, assume http and reparse
        if not parsed.scheme:
            url = "http://" + url
            parsed = urllib.parse.urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return None

        # Must have network location
        if not parsed.netloc:
            return None

        # Basic hostname check
        if "." not in parsed.netloc and parsed.hostname is None:
            return None

        # Rebuild and return normalized URL
        return urllib.parse.urlunparse(parsed)

    
    def create_GUI(self):
        window = tk.Tk()  
        window.title("Url Shortener")
        window.geometry("300x300")
        window.resizable(False, False)

        instructions = tk.Label(
            window,
            text="Type the URL you want below.",
            font=("Segoe UI", 10),
            wraplength=250,
            justify="center"
        )
        instructions.pack()

        url_frame = tk.Frame(window)
        url_frame.pack(pady=10)

        tk.Label(url_frame, text="URL: ", anchor="w").grid(row=0, column=0, sticky="w", pady=6)
        self.url_entry = tk.Entry(url_frame, width=50)
        self.url_entry.grid(row=0, column=1, pady=6)

        button_frame = tk.Frame(window)
        button_frame.pack(pady=10)

        self.info_label = tk.Label(window, text="", font=("Segoe UI", 10), fg="green", wraplength=420, justify="center")
        self.info_label.pack(pady=(8, 0))

        window.mainloop()

def main():
    user = UserInterface()
    user.create_GUI()

if __name__ == "__main__":
    main()
