import tkinter as tk
from tkinter import messagebox, scrolledtext
from zxcvbn import zxcvbn
import itertools

LEET_MAP = {
    'a': ['a', '@', '4'],
    'e': ['e', '3'],
    'i': ['i', '1', '!'],
    'o': ['o', '0'],
    's': ['s', '$', '5'],
    't': ['t', '7']
}

COMMON_SUFFIXES = ['123', '!', '2025', '2024', '2023', '321', '007']
COMMON_PASSWORDS = [
    '123456', 'password', '123456789', '12345', '12345678', 'qwerty', 'abc123', 'football',
    'monkey', 'letmein', 'dragon', '111111', 'baseball', 'iloveyou', 'master', 'sunshine',
    'ashley', 'bailey', 'passw0rd', 'shadow'
]

def generate_leetspeak_variants(word):
    char_options = [LEET_MAP.get(c.lower(), [c]) for c in word]
    variants = list(map(''.join, itertools.product(*char_options)))
    return variants

def append_suffixes(words):
    extended_words = []
    for word in words:
        extended_words.append(word)
        for suffix in COMMON_SUFFIXES:
            extended_words.append(word + suffix)
    return extended_words

def generate_case_variants(word):
    # Generate variants with different casing (lower, upper, title)
    return [word.lower(), word.upper(), word.title()]

def generate_best_wordlist(inputs):
    base_words = [val for val in inputs if val]
    wordlist = set(COMMON_PASSWORDS)  # start with common passwords
    for word in base_words:
        case_variants = generate_case_variants(word)
        for variant in case_variants:
            leet_variants = generate_leetspeak_variants(variant)
            extended = append_suffixes(leet_variants)
            wordlist.update(extended)

        # Also include reversed variants
        reversed_variants = [w[::-1] for w in case_variants]
        for rev_variant in reversed_variants:
            leet_variants = generate_leetspeak_variants(rev_variant)
            extended = append_suffixes(leet_variants)
            wordlist.update(extended)

    return sorted(wordlist)

def format_crack_time(seconds):
    if seconds < 60:
        return f"{int(seconds)} seconds"
    minutes = seconds / 60
    if minutes < 60:
        return f"{int(minutes)} minutes"
    hours = minutes / 60
    if hours < 24:
        return f"{int(hours)} hours"
    days = hours / 24
    if days < 365:
        return f"{int(days)} days"
    years = days / 365
    return f"{years:.2f} years"

def analyze_password_strength(password):
    result = zxcvbn(password)
    score = result['score']
    feedback = result['feedback']
    crack_time = format_crack_time(result['crack_times_seconds']['offline_slow_hashing_1e4_per_second'])
    warnings = []
    if feedback['warning']:
        warnings.append(f"Warning: {feedback['warning']}")
    suggestions = feedback.get('suggestions', [])
    # Additional checks
    if len(password) < 12:
        warnings.append("Password is shorter than 12 characters; longer passwords are generally stronger.")
    if password.islower() or password.isupper():
        warnings.append("Password should include a mix of uppercase and lowercase letters.")
    if password.isdigit():
        warnings.append("Password should not be only digits.")
    return score, warnings, suggestions, crack_time

class PasswordToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Accurate Password Strength Checker & Best Wordlist Generator")
        self.wordlist = []
        self.create_widgets()

    def create_widgets(self):
        # Password Analysis Section
        pwd_frame = tk.LabelFrame(self.root, text="Password Analysis", padx=10, pady=10)
        pwd_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        tk.Label(pwd_frame, text="Password to Analyze:").grid(row=0, column=0, sticky="w")
        self.pwd_entry = tk.Entry(pwd_frame, width=30, show="*")
        self.pwd_entry.grid(row=0, column=1)

        self.analyze_btn = tk.Button(pwd_frame, text="Analyze Password", command=self.analyze_password)
        self.analyze_btn.grid(row=0, column=2, padx=(10,0))

        self.pwd_result_text = scrolledtext.ScrolledText(pwd_frame, height=10, width=60)
        self.pwd_result_text.grid(row=1, column=0, columnspan=3, pady=10)

        # Wordlist Generation Section
        wordlist_frame = tk.LabelFrame(self.root, text="Custom Wordlist Generation", padx=10, pady=10)
        wordlist_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        tk.Label(wordlist_frame, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(wordlist_frame, width=30)
        self.name_entry.grid(row=0, column=1)

        tk.Label(wordlist_frame, text="Date of Birth (YYYYMMDD):").grid(row=1, column=0, sticky="w")
        self.dob_entry = tk.Entry(wordlist_frame, width=30)
        self.dob_entry.grid(row=1, column=1)

        tk.Label(wordlist_frame, text="Pet's Name:").grid(row=2, column=0, sticky="w")
        self.pet_entry = tk.Entry(wordlist_frame, width=30)
        self.pet_entry.grid(row=2, column=1)

        tk.Label(wordlist_frame, text="Favorite Word:").grid(row=3, column=0, sticky="w")
        self.fav_entry = tk.Entry(wordlist_frame, width=30)
        self.fav_entry.grid(row=3, column=1)

        self.wordlist_result_text = scrolledtext.ScrolledText(wordlist_frame, height=15, width=60)
        self.wordlist_result_text.grid(row=5, column=0, columnspan=3, pady=10)

        self.generate_btn = tk.Button(wordlist_frame, text="Generate Wordlist", command=self.generate_wordlist)
        self.generate_btn.grid(row=4, column=0, sticky="w", pady=5)

        self.clear_wordlist_btn = tk.Button(wordlist_frame, text="Clear Wordlist", command=self.clear_wordlist)
        self.clear_wordlist_btn.grid(row=4, column=1)

    def analyze_password(self):
        password = self.pwd_entry.get()
        self.pwd_result_text.delete(1.0, tk.END)
        if not password:
            self.pwd_result_text.insert(tk.END, "Please enter a password to analyze.\n")
            return
        score, warnings, suggestions, crack_time = analyze_password_strength(password)
        self.pwd_result_text.insert(tk.END, f"Password strength score (0-4): {score}\n")
        self.pwd_result_text.insert(tk.END, f"Estimated crack time (offline, slow hashing): {crack_time}\n\n")
        for warn in warnings:
            self.pwd_result_text.insert(tk.END, f"{warn}\n")
        if suggestions:
            self.pwd_result_text.insert(tk.END, "\nSuggestions:\n")
            for s in suggestions:
                self.pwd_result_text.insert(tk.END, f" - {s}\n")

    def generate_wordlist(self):
        name = self.name_entry.get()
        dob = self.dob_entry.get()
        pet = self.pet_entry.get()
        fav = self.fav_entry.get()
        inputs = [name, dob, pet, fav]

        self.wordlist = generate_best_wordlist(inputs)
        self.wordlist_result_text.delete(1.0, tk.END)
        if self.wordlist:
            self.wordlist_result_text.insert(tk.END, f"Generated wordlist with {len(self.wordlist)} entries:\n\n")
            # Show only first 500 entries to keep UI responsive
            display_count = min(500, len(self.wordlist))
            for word in self.wordlist[:display_count]:
                self.wordlist_result_text.insert(tk.END, word + "\n")
            if len(self.wordlist) > display_count:
                self.wordlist_result_text.insert(tk.END, f"\n...and {len(self.wordlist)-display_count} more entries not displayed.")
        else:
            self.wordlist_result_text.insert(tk.END, "No valid inputs provided for wordlist generation.\n")

    def clear_wordlist(self):
        self.wordlist = []
        self.wordlist_result_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordToolGUI(root)
    root.mainloop()
