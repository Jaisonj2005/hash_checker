import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import hashlib
import threading

def select_file():
    filepath = filedialog.askopenfilename(title="Select File to Hash")
    if filepath:
        entry_filepath.config(state=tk.NORMAL)
        entry_filepath.delete(0, tk.END)
        entry_filepath.insert(0, filepath)
        entry_filepath.config(state=tk.DISABLED)
        
        # Clear previous results
        entry_md5.config(state=tk.NORMAL)
        entry_md5.delete(0, tk.END)
        entry_md5.config(state="readonly")
        
        entry_sha1.config(state=tk.NORMAL)
        entry_sha1.delete(0, tk.END)
        entry_sha1.config(state="readonly")
        
        entry_sha256.config(state=tk.NORMAL)
        entry_sha256.delete(0, tk.END)
        entry_sha256.config(state="readonly")
        
        lbl_match_result.config(text="")
        
        # Start hashing in a background thread to keep UI responsive for large files
        threading.Thread(target=calculate_hashes, args=(filepath,), daemon=True).start()

def calculate_hashes(filepath):
    btn_browse.config(state=tk.DISABLED)
    lbl_status.config(text="Calculating hashes... (This may take a moment for large files)", fg="#e67e22")
    
    # Initialize hash objects
    md5_hash = hashlib.md5()
    sha1_hash = hashlib.sha1()
    sha256_hash = hashlib.sha256()
    
    try:
        # Read file in 8KB chunks to prevent RAM exhaustion on large files
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                md5_hash.update(chunk)
                sha1_hash.update(chunk)
                sha256_hash.update(chunk)
                
        # Update UI with hex digests
        update_hash_field(entry_md5, md5_hash.hexdigest())
        update_hash_field(entry_sha1, sha1_hash.hexdigest())
        update_hash_field(entry_sha256, sha256_hash.hexdigest())
        
        lbl_status.config(text="Hashing Complete", fg="#27ae60")
        
        # Trigger comparison if a hash is already pasted
        compare_hash()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file:\n{str(e)}")
        lbl_status.config(text="Error reading file", fg="#c0392b")
        
    finally:
        btn_browse.config(state=tk.NORMAL)

def update_hash_field(entry_widget, hash_val):
    entry_widget.config(state=tk.NORMAL)
    entry_widget.insert(0, hash_val)
    entry_widget.config(state="readonly")

def compare_hash(*args):
    target_hash = entry_compare.get().strip().lower()
    if not target_hash:
        lbl_match_result.config(text="")
        return
        
    md5 = entry_md5.get()
    sha1 = entry_sha1.get()
    sha256 = entry_sha256.get()
    
    if not md5 and not sha1 and not sha256:
        return # Hashes not calculated yet
        
    if target_hash in [md5, sha1, sha256]:
        lbl_match_result.config(text="✅ MATCH FOUND", fg="#2ecc71")
    else:
        lbl_match_result.config(text="❌ NO MATCH (TAMPERED?)", fg="#e74c3c")

# --- Tkinter GUI Layout ---
root = tk.Tk()
root.title("SOC Toolkit - File Integrity Hash Checker")
root.geometry("600x480")
root.resizable(False, False)

frame = ttk.Frame(root, padding="20")
frame.pack(fill=tk.BOTH, expand=True)

lbl_title = tk.Label(frame, text="Cryptographic File Integrity Checker", font=("Helvetica", 14, "bold"))
lbl_title.pack(anchor="w", pady=(0, 20))

# File Selection
frame_file = tk.Frame(frame)
frame_file.pack(fill=tk.X, pady=(0, 20))

entry_filepath = ttk.Entry(frame_file, width=55, font=("Consolas", 9))
entry_filepath.pack(side=tk.LEFT, padx=(0, 10))
entry_filepath.insert(0, "No file selected...")
entry_filepath.config(state=tk.DISABLED)

btn_browse = tk.Button(frame_file, text="Browse File", command=select_file, bg="#2980b9", fg="white", font=("Helvetica", 9, "bold"))
btn_browse.pack(side=tk.LEFT)

# Hash Outputs
frame_hashes = tk.LabelFrame(frame, text=" Generated Hashes ", font=("Helvetica", 9, "bold"), padx=10, pady=10)
frame_hashes.pack(fill=tk.X, pady=(0, 20))

tk.Label(frame_hashes, text="MD5:", font=("Helvetica", 9, "bold")).grid(row=0, column=0, sticky="w", pady=5)
entry_md5 = ttk.Entry(frame_hashes, width=65, font=("Consolas", 10), state="readonly")
entry_md5.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_hashes, text="SHA-1:", font=("Helvetica", 9, "bold")).grid(row=1, column=0, sticky="w", pady=5)
entry_sha1 = ttk.Entry(frame_hashes, width=65, font=("Consolas", 10), state="readonly")
entry_sha1.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_hashes, text="SHA-256:", font=("Helvetica", 9, "bold")).grid(row=2, column=0, sticky="w", pady=5)
entry_sha256 = ttk.Entry(frame_hashes, width=65, font=("Consolas", 10), state="readonly")
entry_sha256.grid(row=2, column=1, padx=10, pady=5)

# Verification / Comparison
frame_verify = tk.LabelFrame(frame, text=" Verify Integrity ", font=("Helvetica", 9, "bold"), padx=10, pady=10)
frame_verify.pack(fill=tk.X, pady=(0, 10))

tk.Label(frame_verify, text="Paste Expected Hash:", font=("Helvetica", 9)).grid(row=0, column=0, sticky="w")
entry_compare = ttk.Entry(frame_verify, width=50, font=("Consolas", 10))
entry_compare.grid(row=0, column=1, padx=10)
entry_compare.bind("<KeyRelease>", compare_hash) # Auto-check on typing/pasting

lbl_match_result = tk.Label(frame_verify, text="", font=("Helvetica", 11, "bold"))
lbl_match_result.grid(row=0, column=2, padx=10)

lbl_status = tk.Label(frame, text="Ready", font=("Helvetica", 9, "italic"), fg="#7f8c8d")
lbl_status.pack(anchor="w", side=tk.BOTTOM)

root.mainloop()