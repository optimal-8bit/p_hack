"""
Analyze Hugging Face cache to find duplicates and unnecessary files
"""

import os
from pathlib import Path
from collections import defaultdict

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

print("=" * 80)
print("🔍 Hugging Face Cache Analysis")
print("=" * 80)

hf_cache = Path.home() / ".cache" / "huggingface"

if not hf_cache.exists():
    print("❌ Hugging Face cache not found")
    exit(1)

print(f"\n📁 Cache Location: {hf_cache}")
print(f"📊 Total Size: {format_size(get_dir_size(hf_cache))}")

# Analyze hub directory (where models are stored)
hub_dir = hf_cache / "hub"
if hub_dir.exists():
    print(f"\n{'=' * 80}")
    print("📦 Models in Cache:")
    print(f"{'=' * 80}")
    
    model_sizes = {}
    
    # List all model directories
    for model_dir in hub_dir.iterdir():
        if model_dir.is_dir():
            size = get_dir_size(model_dir)
            model_sizes[model_dir.name] = size
    
    # Sort by size (largest first)
    sorted_models = sorted(model_sizes.items(), key=lambda x: x[1], reverse=True)
    
    total_models_size = 0
    for i, (model_name, size) in enumerate(sorted_models, 1):
        print(f"\n{i}. {model_name}")
        print(f"   Size: {format_size(size)}")
        total_models_size += size
        
        # Check for snapshots (multiple versions)
        model_path = hub_dir / model_name
        snapshots_dir = model_path / "snapshots"
        if snapshots_dir.exists():
            snapshot_count = len(list(snapshots_dir.iterdir()))
            if snapshot_count > 1:
                print(f"   ⚠️  Multiple snapshots: {snapshot_count} versions")
                print(f"   💡 You may have duplicate model versions!")
    
    print(f"\n{'=' * 80}")
    print(f"📊 Total Models Size: {format_size(total_models_size)}")
    print(f"{'=' * 80}")

# Check for other cache directories
print(f"\n{'=' * 80}")
print("📂 Other Cache Directories:")
print(f"{'=' * 80}")

other_dirs = []
for item in hf_cache.iterdir():
    if item.is_dir() and item.name != "hub":
        size = get_dir_size(item)
        other_dirs.append((item.name, size))

if other_dirs:
    for name, size in sorted(other_dirs, key=lambda x: x[1], reverse=True):
        print(f"\n• {name}: {format_size(size)}")
else:
    print("\n✅ No other cache directories")

# Recommendations
print(f"\n{'=' * 80}")
print("💡 RECOMMENDATIONS:")
print(f"{'=' * 80}")

print("\n🎯 BEST OPTION: Move cache to D: drive (keeps LLM working)")
print("   1. Stop the backend server if running")
print("   2. Run these commands:")
print('      setx HF_HOME "D:\\huggingface_cache"')
print(f'      xcopy /E /I /H "{hf_cache}" "D:\\huggingface_cache"')
print(f'      rmdir /s /q "{hf_cache}"')
print("   3. Restart terminal and test")
print("   ✅ Frees 9.47 GB on C: drive")
print("   ✅ LLM continues working")

print("\n🔴 ALTERNATIVE: Disable LLM and delete cache")
print("   1. Set LLM_ENABLED = False in backend/config.py")
print(f'   2. rmdir /s /q "{hf_cache}"')
print("   ✅ Frees 9.47 GB on C: drive")
print("   ⚠️  LLM won't work (uses templates instead)")

print("\n🟢 MINIMAL: Clean old snapshots (if duplicates found)")
print("   Only if you see 'Multiple snapshots' warnings above")
print("   This removes old model versions but keeps latest")

print(f"\n{'=' * 80}")
