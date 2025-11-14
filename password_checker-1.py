import re
import math
import sys

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR_ENABLED = True
except ImportError:
    COLOR_ENABLED = False

def print_banner():
    banner_lines = [
        r"'########:::::'###:::::'######:::'######:::'######::'##::::'##:'########::'######::'##:::'##:",
        r" ##.... ##:::'## ##:::'##... ##:'##... ##:'##... ##: ##:::: ##: ##.....::'##... ##: ##::'##::",
        r" ##:::: ##::'##:. ##:: ##:::..:: ##:::..:: ##:::..:: ##:::: ##: ##::::::: ##:::..:: ##:'##:::",
        r" ########::'##:::. ##:. ######::. ######:: ##::::::: #########: ######::: ##::::::: #####::::",
        r" ##.....::: #########::..... ##::..... ##: ##::::::: ##.... ##: ##...:::: ##::::::: ##. ##:::",
        r" ##:::::::: ##.... ##:'##::: ##:'##::: ##: ##::: ##: ##:::: ##: ##::::::: ##::: ##: ##:. ##::",
        r" ##:::::::: ##:::: ##:. ######::. ######::. ######:: ##:::: ##: ########:. ######:: ##::. ##:",
        r"..:::::::::..:::::..:::......::::......::::......:::..:::::..::........:::......:::..::::..::",
        r"",
        r"                                MADE BY SNEHASISH DAS                                "
    ]

    if COLOR_ENABLED:
        print(Fore.CYAN + Style.BRIGHT + "\n".join(banner_lines) + Style.RESET_ALL + "\n")
    else:
        print("\n".join(banner_lines) + "\n")

# Common passwords list
COMMON_PASSWORDS = {
    "123456", "password", "12345678", "qwerty", "123456789", "12345",
    "1234", "111111", "1234567", "dragon", "123123", "abc123", "monkey",
    "letmein", "football", "iloveyou", "admin", "welcome"
}

def calculate_entropy(password: str) -> float:
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"\d", password): charset += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): charset += 32
    return len(password) * math.log2(charset) if charset else 0

def get_strength_color_label(score: int) -> str:
    if score <= 2:
        return (Fore.RED + "❌ Weak") if COLOR_ENABLED else "❌ Weak"
    elif 3 <= score <= 4:
        return (Fore.YELLOW + "⚠️  Moderate") if COLOR_ENABLED else "⚠️  Moderate"
    elif 5 <= score <= 6:
        return (Fore.GREEN + "✅ Strong") if COLOR_ENABLED else "✅ Strong"
    else:
        return (Fore.BLUE + "🔐 Very Strong") if COLOR_ENABLED else "🔐 Very Strong"

def check_strength(password: str) -> (str, float):
    length = len(password)
    entropy = calculate_entropy(password)

    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
    is_common = password.lower() in COMMON_PASSWORDS

    score = 0
    if length >= 8: score += 1
    if has_upper: score += 1
    if has_lower: score += 1
    if has_digit: score += 1
    if has_special: score += 1
    if length >= 12: score += 1
    if entropy >= 50: score += 1
    if is_common: score -= 2

    label = get_strength_color_label(score)
    return label, entropy

def main():
    print_banner()

    try:
        prompt = (Fore.WHITE + "Enter a password to check: ") if COLOR_ENABLED else "Enter a password to check: "
        password = input(prompt)
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit()

    if not password:
        print("No password entered.")
        sys.exit()

    strength_label, entropy = check_strength(password)

    print("\n" + ("--- Password Analysis ---" if not COLOR_ENABLED else Fore.MAGENTA + "--- Password Analysis ---"))
    print(f"{'→ Strength:':<12} {strength_label}")
    print(f"{'→ Entropy :':<12} {entropy:.2f} bits\n")

if __name__ == "__main__":
    main()
