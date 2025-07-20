import argparse
import math
import string
from colorama import Fore, Style, init

init(autoreset=True)

def calculate_entropy(password):
    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += len(string.punctuation)
    return len(password) * math.log2(charset_size) if charset_size > 0 else 0

def load_common_words():
    try:
        with open("common_words.txt", "r") as f:
            return set(line.strip().lower() for line in f if line.strip())
    except FileNotFoundError:
        return set()

def check_strength(password, common_words):
    score = 0
    suggestions = []

    if len(password) >= 12:
        score += 25
    elif len(password) >= 8:
        score += 15
    else:
        suggestions.append("Use a longer password (at least 12 characters).")

    if any(c.islower() for c in password):
        score += 10
    else:
        suggestions.append("Add lowercase letters.")

    if any(c.isupper() for c in password):
        score += 10
    else:
        suggestions.append("Add uppercase letters.")

    if any(c.isdigit() for c in password):
        score += 15
    else:
        suggestions.append("Add numbers.")

    if any(c in string.punctuation for c in password):
        score += 15
    else:
        suggestions.append("Add special characters (!, @, #, etc).")

    if len(set(password)) < len(password):
        suggestions.append("Avoid repeated characters.")

    if password.lower() in common_words:
        score -= 25
        suggestions.append("Avoid using common words or passwords.")

    entropy = calculate_entropy(password)

    return max(0, min(score, 100)), entropy, suggestions

def analyze(password, common_words):
    score, entropy, suggestions = check_strength(password, common_words)

    color = Fore.GREEN if score > 75 else Fore.YELLOW if score > 50 else Fore.RED
    print(f"{color}Password: {password}")
    print(f"{color}Score: {score}/100")
    print(f"{color}Entropy: {entropy:.2f} bits")

    if suggestions:
        print(Fore.CYAN + "\nSuggestions:")
        for tip in suggestions:
            print(f"- {tip}")
    print(Style.RESET_ALL + "-"*40)

def main():
    parser = argparse.ArgumentParser(description="Password Strength Analyzer (CLI)")
    parser.add_argument("--password", help="Single password to analyze")
    parser.add_argument("--file", help="File containing passwords (one per line)")

    args = parser.parse_args()
    if not args.password and not args.file:
        parser.error("You must specify either --password or --file")

    common_words = load_common_words()

    if args.password:
        analyze(args.password, common_words)
    elif args.file:
        try:
            with open(args.file, "r") as f:
                for line in f:
                    password = line.strip()
                    if password:
                        analyze(password, common_words)
        except FileNotFoundError:
            print("File not found.")

if __name__ == "__main__":
    main()
