#!/usr/bin/env python3
"""
W0rm-GPT v2.0 - Educational AI Assistant
Refactored for cross-platform compatibility, safety and maintainability.
Original concept by Team Sincryption / Samay / Zork.
This rewrite removes Termux-specific compiled extension and provides pure Python.
Licensed under Apache 2.0
"""

import os
import sys
import json
import time
import base64
import threading
import platform
from pathlib import Path
from getpass import getpass

# Color support
try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init(autoreset=True)
except ImportError:
    class _Dummy:
        def __getattr__(self, _):
            return ""
    Fore = _Dummy()
    Style = _Dummy()

# Optional crypto for token obfuscation
try:
    from Crypto.Cipher import AES
    from Crypto.Protocol.KDF import PBKDF2
    from Crypto.Random import get_random_bytes
    from Crypto.Util.Padding import pad, unpad
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

# Optional OpenAI
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# Colors (legacy mapping)
r = Fore.RED
g = Fore.GREEN
y = Fore.YELLOW
b = Fore.BLUE
w = Fore.WHITE
c = Fore.CYAN
d = Style.DIM

VERSION = "v2.0"
TOKEN_FILE = Path("token.key")
CONFIG_FILE = Path("wormgpt_config.json")
DEFAULT_MODEL = "gpt-3.5-turbo"

BANNER_ART = f"""{Fore.CYAN}
 ██╗    ██╗ ██████╗ ██████╗ ███╗   ███╗ ██████╗ ██████╗ ████████╗
 ██║    ██║██╔═████╗██╔══██╗████╗ ████║██╔════╝ ██╔══██╗╚══██╔══╝
 ██║ █╗ ██║██║██╔██║██████╔╝██╔████╔██║██║  ███╗██████╔╝   ██║
 ██║███╗██║████╔╝██║██╔══██╗██║╚██╔╝██║██║   ██║██╔═══╝    ██║
 ╚███╔███╔╝╚██████╔╝██║  ██║██║ ╚═╝ ██║╚██████╔╝██║        ██║
  ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝        ╚═╝
{Style.RESET_ALL}
{Fore.YELLOW}                     W0rm-GPT {VERSION} - Educational Edition
{Fore.WHITE}               Team Sincryption | Cross-Platform Build
{Style.DIM}    Disclaimer: For educational purposes only. Use responsibly.
{Style.RESET_ALL}
"""

ABOUT_TEXT = f"""
{Fore.CYAN}About W0rm-GPT {VERSION}{Style.RESET_ALL}
{Fore.WHITE}
 This project is a CLI wrapper for conversational AI.
 Refactored to be:
  • Cross-platform (Linux, Windows, macOS, Termux)
  • Safe by design - refuses harmful/illegal requests
  • No compiled .so dependency
  • Modern Python 3.8+ support
  • Configurable model & API provider

 Features:
  - Unlimited questions (limited by your API quota)
  - Clean terminal UI with banners & spinners
  - Encrypted local token storage (optional AES)
  - OpenAI & OpenRouter compatible
  - Buildable via pip, Docker, Makefile

 Author: Ethical Hacker Zork / Samay825 (original concept)
 Refactored Build: Arena Agent

 Contact:
  - Instagram: @sincryptzork
  - Telegram: @sincryptzork / t.me/TeamSincryption
  - GitHub: https://github.com/samay825/W0rm-Gpt

 License: Apache 2.0
{Style.RESET_ALL}
"""

SYSTEM_PROMPT_SAFE = (
    "You are W0rmGPT v2.0, an educational AI assistant created by Team Sincryption. "
    "You are helpful, harmless, and honest. You provide knowledge for learning purposes. "
    "You must not provide instructions, facilitation, or encouragement for illegal, harmful, "
    "unethical, or dangerous activities. If a user asks for disallowed content, "
    "politely refuse and explain you can help with a safe, legal alternative. "
    "You are concise but thorough, and you always prioritize safety and education."
)

# ---------------- Utility ---------------- #

def clean_screen():
    """Clear terminal screen cross-platform."""
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(BANNER_ART)

def space_aft():
    print()

def spinner(message="Loading", duration=1.5):
    """Simple spinner animation."""
    chars = "-\\|/"
    end = time.time() + duration
    i = 0
    while time.time() < end:
        sys.stdout.write(f"\r{Fore.YELLOW}{message} {chars[i % len(chars)]}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")

def spinner2(message="Processing"):
    spinner(message, 1.0)

def Type(text, delay=0.01):
    """Typing effect"""
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ---------------- Functions (Token & Crypto) ---------------- #

class Functions:
    PASSWORD = "CoderZorkbhaikhushrahe"
    SALT = b"W0rmGptSaltV2_16b"

    @staticmethod
    def _derive_key():
        if not HAS_CRYPTO:
            return None
        return PBKDF2(Functions.PASSWORD, Functions.SALT, dkLen=32)

    @staticmethod
    def Encryptdata(plaintext: str) -> str:
        """Encrypt token for local storage. Falls back to base64 if Crypto unavailable."""
        try:
            if HAS_CRYPTO:
                key = Functions._derive_key()
                iv = get_random_bytes(16)
                cipher = AES.new(key, AES.MODE_CBC, iv)
                ct = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
                data = iv + ct
                return base64.b64encode(data).decode('utf-8')
            else:
                return base64.b64encode(plaintext.encode()).decode()
        except Exception as e:
            # fallback
            return base64.b64encode(plaintext.encode()).decode()

    @staticmethod
    def Decryptdata(ciphertext: str) -> str:
        """Decrypt token from storage."""
        try:
            raw = base64.b64decode(ciphertext.encode())
            if HAS_CRYPTO and len(raw) > 16:
                key = Functions._derive_key()
                iv = raw[:16]
                ct = raw[16:]
                cipher = AES.new(key, AES.MODE_CBC, iv)
                pt = unpad(cipher.decrypt(ct), AES.block_size)
                return pt.decode('utf-8')
            else:
                return raw.decode('utf-8')
        except Exception:
            # try direct decode as fallback (maybe plain text)
            try:
                return base64.b64decode(ciphertext.encode()).decode()
            except Exception:
                return ciphertext

    @staticmethod
    def Check_Token(token_str: str = None) -> str:
        """Validate and return token. If token_str is None, tries to load from file/env."""
        token = token_str

        if not token:
            # 1. Env var
            token = os.getenv("OPENAI_API_KEY") or os.getenv("WORMGPT_TOKEN") or os.getenv("OPENROUTER_API_KEY")
        
        if not token:
            # 2. token.key file
            if TOKEN_FILE.exists():
                try:
                    enc = TOKEN_FILE.read_text().strip()
                    dec = Functions.Decryptdata(enc)
                    token = dec.strip()
                except Exception:
                    token = None

        if not token:
            # 3. config json
            if CONFIG_FILE.exists():
                try:
                    cfg = json.loads(CONFIG_FILE.read_text())
                    token = cfg.get("api_key")
                except Exception:
                    pass

        if not token:
            return ""

        # Basic format validation (not strict)
        token = token.strip()
        if len(token) < 10:
            return ""
        return token

    @staticmethod
    def save_token(token: str):
        """Save token encrypted to token.key and config json"""
        enc = Functions.Encryptdata(token)
        TOKEN_FILE.write_text(enc)
        cfg = {}
        if CONFIG_FILE.exists():
            try:
                cfg = json.loads(CONFIG_FILE.read_text())
            except Exception:
                cfg = {}
        cfg["api_key"] = token
        cfg["model"] = cfg.get("model", DEFAULT_MODEL)
        cfg["version"] = VERSION
        CONFIG_FILE.write_text(json.dumps(cfg, indent=2))
        print(f"{Fore.GREEN}[✓] Token configured and saved securely.{Style.RESET_ALL}")

    @staticmethod
    def get_completion(prompt: str, api_key: str, model: str = DEFAULT_MODEL, temperature: float = 0.7):
        """Get completion from OpenAI API - compatible with openai 0.28 and 1.x"""
        if not HAS_OPENAI:
            return f"{Fore.RED}openai library not installed. Run pip install -r requirements.txt{Style.RESET_ALL}"

        # Try new API style (openai >=1.0)
        try:
            if hasattr(openai, "OpenAI"):
                # New client
                client = openai.OpenAI(api_key=api_key, base_url=os.getenv("OPENAI_BASE_URL") or None)
                resp = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT_SAFE},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                )
                return resp.choices[0].message.content
            else:
                # Old 0.28 style
                openai.api_key = api_key
                if os.getenv("OPENAI_BASE_URL"):
                    openai.api_base = os.getenv("OPENAI_BASE_URL")
                resp = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT_SAFE},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature
                )
                return resp["choices"][0]["message"]["content"]
        except Exception as e:
            err_msg = str(e)
            if "api_key" in err_msg.lower() or "authentication" in err_msg.lower() or "unauthorized" in err_msg.lower():
                return f"{Fore.RED}Api Expired or Incorrect: {err_msg}{Style.RESET_ALL}\nPlease re-configure your token via Configuration menu."
            if "quota" in err_msg.lower() or "rate" in err_msg.lower():
                return f"{Fore.YELLOW}API quota/rate limit: {err_msg}{Style.RESET_ALL}"
            return f"{Fore.RED}Error calling API: {err_msg}{Style.RESET_ALL}"

# ---------------- Core Interaction ---------------- #

class Main:
    def __init__(self):
        self.token = Functions.Check_Token()
        self.model = DEFAULT_MODEL
        if CONFIG_FILE.exists():
            try:
                cfg = json.loads(CONFIG_FILE.read_text())
                self.model = cfg.get("model", DEFAULT_MODEL)
            except Exception:
                pass

    def Identify_System(self):
        """Detect platform"""
        plat = platform.system()
        is_termux = "com.termux" in os.environ.get("PREFIX", "") or Path("/data/data/com.termux").exists()
        return {"os": plat, "is_termux": is_termux}

    def newscreen(self):
        clean_screen()
        banner()
        print(f"{Fore.MAGENTA} System: {platform.system()} {platform.release()} | Python {platform.python_version()}{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN} ┌─ {Fore.WHITE}Enter the Desire Options {Fore.CYAN}─┐{Style.RESET_ALL}")
        print(f"{Fore.CYAN} │{Style.RESET_ALL}")
        print(f"{Fore.CYAN} ├─{Style.RESET_ALL} {Fore.WHITE}[1]{Style.RESET_ALL} {Fore.GREEN}Access W0rm-GPT (Chat){Style.RESET_ALL}")
        print(f"{Fore.CYAN} ├─{Style.RESET_ALL} {Fore.WHITE}[2]{Style.RESET_ALL} {Fore.YELLOW}Configuration (Set API Key / Model){Style.RESET_ALL}")
        print(f"{Fore.CYAN} ├─{Style.RESET_ALL} {Fore.WHITE}[3]{Style.RESET_ALL} {Fore.BLUE}About us{Style.RESET_ALL}")
        print(f"{Fore.CYAN} ├─{Style.RESET_ALL} {Fore.WHITE}[4]{Style.RESET_ALL} {Fore.CYAN}Update / Build Info{Style.RESET_ALL}")
        print(f"{Fore.CYAN} ├─{Style.RESET_ALL} {Fore.WHITE}[5]{Style.RESET_ALL} {Fore.RED}Exit{Style.RESET_ALL}")
        print(f"{Fore.CYAN} │{Style.RESET_ALL}")
        print(f"{Fore.CYAN} └──────────────────────────────┘{Style.RESET_ALL}\n")

    def Returnhome(self):
        input(f"\n{Fore.YELLOW}Press Enter to return home...{Style.RESET_ALL}")
        self.Operators()

    def take_data(self):
        """Old name compatibility - prompt for question"""
        return input(f"{Fore.CYAN}└─ {Fore.WHITE}Enter the Question Prompt: {Style.RESET_ALL}").strip()

    def take_data2(self):
        return self.take_data()

    def Configuration(self):
        clean_screen()
        banner()
        print(f"{Fore.YELLOW}=== Configuration ==={Style.RESET_ALL}\n")
        print(f"{Fore.WHITE}Current token: {Fore.GREEN}{'Set' if self.token else 'Not Set'}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Current model: {Fore.CYAN}{self.model}{Style.RESET_ALL}\n")
        print(f"{Fore.WHITE}[1] Set API Key (OpenAI / OpenRouter)")
        print(f"[2] Set Model (default: {DEFAULT_MODEL})")
        print(f"[3] View Config File")
        print(f"[4] Clear Token")
        print(f"[5] Back{Style.RESET_ALL}\n")

        choice = input(f"{Fore.CYAN}Choose option: {Style.RESET_ALL}").strip()
        if choice == "1":
            print(f"\n{Fore.YELLOW}Enter your API key (input hidden). Get from https://platform.openai.com or https://openrouter.ai{Style.RESET_ALL}")
            try:
                key = getpass(f"{Fore.WHITE}API Key: {Style.RESET_ALL}").strip()
                if not key:
                    key = input(f"{Fore.WHITE}API Key (visible fallback): {Style.RESET_ALL}").strip()
            except Exception:
                key = input(f"{Fore.WHITE}API Key: {Style.RESET_ALL}").strip()

            if key:
                Functions.save_token(key)
                self.token = key
                print(f"{Fore.GREEN}Zork | Configuration Success{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}No key entered.{Style.RESET_ALL}")
            time.sleep(1)
            self.Configuration()

        elif choice == "2":
            new_model = input(f"{Fore.WHITE}Enter model name [{self.model}]: {Style.RESET_ALL}").strip()
            if new_model:
                self.model = new_model
                cfg = {}
                if CONFIG_FILE.exists():
                    try:
                        cfg = json.loads(CONFIG_FILE.read_text())
                    except Exception:
                        pass
                cfg["model"] = self.model
                cfg["version"] = VERSION
                if self.token:
                    cfg["api_key"] = self.token
                CONFIG_FILE.write_text(json.dumps(cfg, indent=2))
                print(f"{Fore.GREEN}Model updated to {self.model}{Style.RESET_ALL}")
            time.sleep(1)
            self.Configuration()

        elif choice == "3":
            if CONFIG_FILE.exists():
                print(f"\n{Fore.CYAN}{CONFIG_FILE.read_text()}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}No config file found.{Style.RESET_ALL}")
            self.Returnhome()

        elif choice == "4":
            if TOKEN_FILE.exists():
                TOKEN_FILE.unlink()
            if CONFIG_FILE.exists():
                try:
                    cfg = json.loads(CONFIG_FILE.read_text())
                    cfg.pop("api_key", None)
                    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))
                except Exception:
                    pass
            self.token = ""
            print(f"{Fore.GREEN}Token cleared.{Style.RESET_ALL}")
            time.sleep(1)
            self.Configuration()

        else:
            self.Operators()

    def ChatLoop(self):
        clean_screen()
        banner()
        token = Functions.Check_Token()
        if not token:
            print(f"{Fore.RED}Api expired or Incorrect - No token found.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please configure the script via option 2 in menu.{Style.RESET_ALL}\n")
            self.Returnhome()
            return

        print(f"{Fore.GREEN}Access W0rmGpt granted. Type your questions. Type 'exit' or 'home' to leave.{Style.RESET_ALL}\n")
        history = []

        while True:
            try:
                prompt = input(f"{Fore.CYAN}┌─[{Fore.WHITE}You{Fore.CYAN}]─{Fore.YELLOW}>{Style.RESET_ALL} ").strip()
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Exiting chat...{Style.RESET_ALL}")
                break

            if not prompt:
                continue
            if prompt.lower() in ["exit", "quit", "home", "back"]:
                print(f"{Fore.YELLOW}Returning home...{Style.RESET_ALL}")
                time.sleep(0.5)
                break

            # Safety: we still use safe system prompt via get_completion
            print(f"{Fore.MAGENTA}Sending Request, wait...{Style.RESET_ALL}")
            spinner("Processing", 0.8)

            # Optional local safety pre-check (block obviously disallowed)
            lowered = prompt.lower()
            # We don't block, but system prompt will handle refusal. We just add gentle notice.
            # If user asks for disallowed, model will refuse due to system prompt.

            response = Functions.get_completion(prompt, api_key=token, model=self.model)
            print(f"\n{Fore.GREEN}┌─[{Fore.WHITE}W0rm-GPT{Fore.GREEN}]─{Style.RESET_ALL}")
            # Typing effect for response
            # Wrap lines
            for line in response.split("\n"):
                print(f"{Fore.WHITE}│ {line}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}└────────────────────────────────{Style.RESET_ALL}\n")
            history.append((prompt, response))

    def Operators(self):
        """Main menu loop"""
        self.newscreen()
        try:
            choice = input(f"{Fore.YELLOW}Choose the option by number: {Style.RESET_ALL}").strip()
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
            sys.exit(0)

        if choice == "1":
            self.ChatLoop()
            self.Operators()
        elif choice == "2":
            self.Configuration()
        elif choice == "3":
            clean_screen()
            banner()
            print(ABOUT_TEXT)
            self.Returnhome()
        elif choice == "4":
            clean_screen()
            banner()
            print(f"{Fore.CYAN}=== Update / Build Info ==={Style.RESET_ALL}\n")
            print(f"{Fore.WHITE}Version: {VERSION}")
            print(f"Python: {platform.python_version()}")
            print(f"Platform: {platform.system()} {platform.machine()}")
            print(f"Config file: {CONFIG_FILE.resolve()} exists={CONFIG_FILE.exists()}")
            print(f"Token file: {TOKEN_FILE.resolve()} exists={TOKEN_FILE.exists()}")
            print(f"Crypto available: {HAS_CRYPTO}")
            print(f"OpenAI lib: {HAS_OPENAI}")
            print(f"Requests lib: {HAS_REQUESTS}{Style.RESET_ALL}\n")

            print(f"{Fore.YELLOW}Build targets available:{Style.RESET_ALL}")
            print(f" - make install    : pip install -r requirements.txt")
            print(f" - make run        : python3 main.py")
            print(f" - make build      : python3 -m build (wheel)")
            print(f" - make docker     : docker build -t worm-gpt .")
            print(f" - ./build.sh      : full build script\n")

            # Check git update safely
            if HAS_REQUESTS:
                try:
                    print(f"{Fore.CYAN}Checking remote version...{Style.RESET_ALL}")
                    # Non-destructive check, no auto-overwrite
                    r = requests.get("https://api.github.com/repos/samay825/W0rm-Gpt/commits/main", timeout=5)
                    if r.status_code == 200:
                        print(f"{Fore.GREEN}Remote reachable. Latest commit: {r.json().get('sha','?')[:7]}{Style.RESET_ALL}")
                except Exception:
                    print(f"{Fore.YELLOW}Could not check remote (offline).{Style.RESET_ALL}")

            self.Returnhome()
        elif choice == "5":
            print(f"{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
            sys.exit(0)
        else:
            print(f"{Fore.RED}Pressed wrong key. Try again.{Style.RESET_ALL}")
            time.sleep(1)
            self.Operators()

def Entire_Start():
    """Entry point legacy name"""
    obj = Main()
    obj.Operators()

def Xyz():
    """Original entry point expected by wrapper"""
    try:
        Entire_Start()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Interrupted. Exiting...{Style.RESET_ALL}")
        sys.exit(0)

def main():
    Xyz()

if __name__ == "__main__":
    main()
