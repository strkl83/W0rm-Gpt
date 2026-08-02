#!/usr/bin/env bash
set -e

echo "=== W0rm-GPT Build Script v2.0 ==="

# Detect python
PY=python3
if ! command -v $PY &>/dev/null; then
  PY=python
fi

echo "[*] Python: $($PY --version)"

echo "[*] Cleaning old artifacts..."
rm -rf __pycache__ .pytest_cache build dist *.egg-info
rm -f main.cpython-*.so
rm -rf __pycache__/ _main_wrapper.py || true

echo "[*] Installing dependencies..."
$PY -m pip install --upgrade pip --break-system-packages || $PY -m pip install --upgrade pip
$PY -m pip install -r requirements.txt --break-system-packages || $PY -m pip install -r requirements.txt

echo "[*] Verifying imports..."
$PY -c "
import main
print('✓ main.py import OK')
from main import Functions
enc = Functions.Encryptdata('sk-test-123')
dec = Functions.Decryptdata(enc)
assert dec == 'sk-test-123', 'encrypt/decrypt failed'
print('✓ Encrypt/Decrypt OK')
print('✓ Banner:')
main.banner()
"

echo "[*] Linting..."
$PY -m py_compile main.py update.py
echo "✓ Lint OK"

echo "[*] Building wheel (optional)..."
$PY -m pip install build --break-system-packages -q || $PY -m pip install build -q || true
if $PY -m build --wheel --sdist 2>&1 | tee build.log; then
  echo "✓ Wheel built: $(ls dist/ 2>/dev/null || echo 'no dist')"
else
  echo "⚠ Build failed, but runtime is OK (build tool optional)"
fi

echo ""
echo "=== Build Successful ==="
echo "Run: $PY main.py"
echo "Or: make run"
echo "Docker: docker build -t worm-gpt:2.0 ."
echo ""

