"""
Check disk usage for the mental health chatbot project
"""

import os
from pathlib import Path

def get_dir_size(path):
    """Get total size of directory in bytes"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                total += entry.stat().st_size
            elif entry.is_dir(follow_symlinks=False):
                total += get_dir_size(entry.path)
    except (PermissionError, FileNotFoundError):
        pass
    return total

def format_size(bytes_size):
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

print("=" * 70)
print("💾 Disk Usage Analysis - Mental Health Chatbot")
print("=" * 70)

# Check project directory
project_root = Path(__file__).parent
print(f"\n📁 Project Location: {project_root}")

# 1. ONNX Models
onnx_dir = project_root / "backend" / "onnx_models"
if onnx_dir.exists():
    onnx_size = get_dir_size(onnx_dir)
    print(f"\n1️⃣  ONNX Models: {format_size(onnx_size)}")
    print(f"   Location: {onnx_dir}")
    print(f"   Contains: Emotion, Intent, Translation models")
else:
    print(f"\n1️⃣  ONNX Models: Not found")

# 2. Virtual Environment
venv_dir = project_root / "venv"
if venv_dir.exists():
    venv_size = get_dir_size(venv_dir)
    print(f"\n2️⃣  Virtual Environment: {format_size(venv_size)}")
    print(f"   Location: {venv_dir}")
    print(f"   Contains: Python packages (PyTorch, Transformers, etc.)")
else:
    print(f"\n2️⃣  Virtual Environment: Not found")

# 3. Hugging Face Cache (usually on C drive)
hf_cache = Path.home() / ".cache" / "huggingface"
if hf_cache.exists():
    hf_size = get_dir_size(hf_cache)
    print(f"\n3️⃣  Hugging Face Cache: {format_size(hf_size)}")
    print(f"   Location: {hf_cache}")
    print(f"   Contains: Phi-3 Mini model (~7.6 GB)")
    print(f"   ⚠️  This is on your C: drive!")
else:
    print(f"\n3️⃣  Hugging Face Cache: Not found")

# 4. Database
db_file = project_root / "backend" / "chat_history.db"
if db_file.exists():
    db_size = db_file.stat().st_size
    print(f"\n4️⃣  Database: {format_size(db_size)}")
    print(f"   Location: {db_file}")
else:
    print(f"\n4️⃣  Database: Not found")

# Total
total = 0
if onnx_dir.exists():
    total += onnx_size
if venv_dir.exists():
    total += venv_size
if hf_cache.exists():
    total += hf_size
if db_file.exists():
    total += db_size

print("\n" + "=" * 70)
print(f"📊 TOTAL SPACE USED: {format_size(total)}")
print("=" * 70)

print("\n💡 Space Saving Options:")
print("\n🔴 AGGRESSIVE (Free ~7.6 GB) - Disable LLM:")
print("   1. Set LLM_ENABLED = False in backend/config.py")
print("   2. Delete Hugging Face cache:")
print(f"      rmdir /s /q \"{hf_cache}\"")
print("   3. System will use fast template responses")

print("\n🟡 MODERATE (Free ~2-3 GB) - Keep LLM, remove unused:")
print("   1. Keep Phi-3 Mini (needed for LLM)")
print("   2. Remove translation models if only using English:")
print(f"      cd {onnx_dir}")
print("      rmdir /s /q translate_*")

print("\n🟢 MINIMAL (Free ~100 MB) - Clean cache only:")
print("   1. Clear pip cache: pip cache purge")
print("   2. Clear Python cache: find . -type d -name __pycache__ -exec rm -rf {} +")

print("\n" + "=" * 70)
