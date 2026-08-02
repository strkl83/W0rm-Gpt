<h1 align="center">W0rm-GPT v2.0<br></h1>
<img src="W0rmgptv2.png" alt="W0rmGPT Logo" class="center">

* `📱 💻` - Cross-Platform CLI Assistant
* `A W0rm-GPT for Termux, Linux, Windows, macOS, Docker`

## Disclaimer
*This tool is for educational purposes only !*
_Don't use this to take revenge_<br />
*I will not be responsible for any misuse*

> **Safety Notice (Refactored Build):** This v2.0 refactor removes any jailbreak/harmful prompts and implements a safe, helpful, harmless system prompt. It will refuse illegal/unethical requests and provide educational alternatives.

## About
* `Unlimited Questions` (limited by your API quota)
* `Cross Platform` - No more .so Termux-only binary
* `Supports newest Android, Linux, Windows, macOS`
* `Modern Python 3.8+`
* `Working APIs - OpenAI & OpenRouter compatible`
* `Encrypted local token storage (AES)`
* `Clean build system: pip, Makefile, Docker, PyPI`

## Tested On :
<ul>
  <li>Termux</li>
  <li>Ubuntu 22.04 / Debian 12</li>
  <li>Windows 11 + Python 3.11</li>
  <li>Docker</li>
</ul>

## Termux Issue:
* `Termux App is no longer receiving updates on Play Store`
* `due to recently introduced Google Play policy`

DON'T WORRY
* `We have a solution for that !`

You can download the latest Termux app from F-Droid:
<a href="https://f-droid.org/repo/com.termux_118.apk">Link</a>

---

## 🚀 Quick Build

### Option 1: Automated build script
```bash
chmod +x build.sh
./build.sh
```

### Option 2: Makefile
```bash
make install   # pip install -r requirements.txt
make test      # verify encrypt/decrypt & import
make run       # python3 main.py
make build     # build wheel -> dist/
make clean
```

### Option 3: Pip / PyProject
```bash
pip install -r requirements.txt
python3 main.py

# Or install as package:
pip install .
wormgpt
# or
python3 -m build
```

### Option 4: Docker
```bash
docker build -t worm-gpt:2.0 .
docker run -it --rm -e OPENAI_API_KEY=sk-... worm-gpt:2.0

# Or with env file:
echo "OPENAI_API_KEY=sk-..." > .env
docker run -it --rm --env-file .env worm-gpt:2.0
```

---

## Usage

#### For Termux
Update the packages
```bash
pkg up -y
pkg install git python -y
git clone https://github.com/samay825/W0rm-Gpt
cd W0rm-Gpt
pip install -r requirements.txt
python3 main.py
```

#### For Linux / macOS / Windows
```bash
git clone https://github.com/strkl83/W0rm-Gpt.git
cd W0rm-Gpt
pip install -r requirements.txt
python3 main.py
```

Run the script
```bash
python3 main.py
# Menu:
# [1] Access W0rm-GPT (Chat)
# [2] Configuration (Set API Key / Model)
# [3] About us
# [4] Update / Build Info
# [5] Exit
```

## Get the Token

- **OpenAI**: https://platform.openai.com/api-keys
- **OpenRouter**: https://openrouter.ai/keys

You can set via:
1. Environment variable: `export OPENAI_API_KEY=sk-...`
2. Menu option 2 -> Set API Key
3. Manually edit `wormgpt_config.json` or `token.key`

For legacy compatibility, the Telegram channel `t.me/TeamSincryption` previously distributed tokens.

## Configuration

Example `wormgpt_config.json`:
```json
{
  "api_key": "sk-...",
  "model": "gpt-3.5-turbo",
  "version": "v2.0"
}
```
Or see `config.example.json`.

Supported models:
- `gpt-3.5-turbo` (default)
- `gpt-4`
- `gpt-4o-mini`
- OpenRouter models like `deepseek/deepseek-chat-v3-0324:free`, `meta-llama/llama-3-8b-instruct`

You can set custom base URL via env `OPENAI_BASE_URL` for OpenRouter:
```bash
export OPENAI_BASE_URL=https://openrouter.ai/api/v1
export OPENAI_API_KEY=your_openrouter_key
```

## Version
* `v2.0 W0rm-Gpt - Refactored Build`
* Changelog:
  - Removed Termux-only `main.cpython-311.so`
  - Pure Python implementation with safety guardrails
  - Added AES token encryption, Makefile, Dockerfile, pyproject.toml, build.sh
  - Fixed update.py (no more rm -rf + wget)
  - Added .gitignore, lint, test targets

## Features
* `Educational AI assistant`
* `Safe, harmless, honest - refuses illegal requests`
* `All questions answered in good flow with typing effect`

## Project Structure
```
.
├── main.py              # Main CLI - entry point Xyz() / Entire_Start()
├── update.py            # Safe updater (git pull)
├── requirements.txt     # Dependencies
├── pyproject.toml       # Modern packaging
├── Makefile             # Build targets
├── build.sh             # Automated build script
├── Dockerfile           # Container build
├── config.example.json  # Example config
├── W0rmgptv2.png        # Logo
└── README.md
```

## Licence
Apache 2.0 © Samay825 / Team Sincryption

## Contact Us
* `If you have any feedback or queries`
* `Instagram: @sincryptzork`
* `Telegram: @sincryptzork`

## Telegram Channel
* `All updates of Team Sincryption will be posted here >> t.me/TeamSincryption`

<a href="https://t.me/TeamSincryption">
         <img src="https://smartiblogster.com/wp-content/uploads/2021/03/smartiblogster-iblogster-join-telegram-channel.png">
</a>
