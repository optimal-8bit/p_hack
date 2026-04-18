"""
Find large files and directories that may have consumed disk space
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

def find_large_items(root_path, min_size_gb=0.5):
    """Find directories and files larger than min_size_gb"""
    min_size_bytes = min_size_gb * 1024 * 1024 * 1024
    large_items = []
    
    try:
        for entry in os.scandir(root_path):
            try:
                if entry.is_file(follow_symlinks=False):
                    size = entry.stat().st_size
                    if size > min_size_bytes:
                        large_items.append(('file', entry.path, size))
                elif entry.is_dir(follow_symlinks=False):
                    # Skip system directories
                    if entry.name.lower() in ['system volume information', '$recycle.bin', 
                                               'windows', 'program files', 'program files (x86)',
                                               'programdata']:
                        continue
                    size = get_dir_size(entry.path)
                    if size > min_size_bytes:
                        large_items.append(('dir', entry.path, size))
            except (PermissionError, FileNotFoundError):
                continue
    except (PermissionError, FileNotFoundError):
        pass
    
    return large_items

print("=" * 80)
print("🔍 COMPREHENSIVE DISK SPACE ANALYSIS")
print("=" * 80)

# Check common locations that consume space
locations_to_check = [
    ("User Home", Path.home()),
    ("User AppData Local", Path.home() / "AppData" / "Local"),
    ("User AppData Roaming", Path.home() / "AppData" / "Roaming"),
    ("Temp Files", Path(os.environ.get('TEMP', 'C:\\Windows\\Temp'))),
]

print("\n📊 Checking common locations for large files/folders (>500 MB)...")
print("This may take a few minutes...\n")

all_large_items = []

for name, path in locations_to_check:
    if not path.exists():
        continue
    
    print(f"🔍 Scanning: {name} ({path})...")
    items = find_large_items(path, min_size_gb=0.5)
    
    if items:
        print(f"   Found {len(items)} large items")
        all_large_items.extend([(name, item_type, item_path, size) 
                                for item_type, item_path, size in items])
    else:
        print(f"   No large items found")

# Sort by size
all_large_items.sort(key=lambda x: x[3], reverse=True)

print("\n" + "=" * 80)
print("📦 LARGE FILES AND DIRECTORIES (>500 MB)")
print("=" * 80)

if all_large_items:
    for i, (location, item_type, path, size) in enumerate(all_large_items[:30], 1):
        icon = "📁" if item_type == "dir" else "📄"
        print(f"\n{i}. {icon} {format_size(size)}")
        print(f"   Location: {location}")
        print(f"   Path: {path}")
else:
    print("\n✅ No large items found in scanned locations")

# Specific checks for known space consumers
print("\n" + "=" * 80)
print("🎯 SPECIFIC CHECKS")
print("=" * 80)

checks = [
    ("Hugging Face Cache", Path.home() / ".cache" / "huggingface"),
    ("Pip Cache", Path.home() / "AppData" / "Local" / "pip" / "cache"),
    ("PyTorch Cache", Path.home() / ".cache" / "torch"),
    ("VS Code Extensions", Path.home() / ".vscode" / "extensions"),
    ("Node Modules (if any)", Path.home() / "node_modules"),
    ("Conda Environments", Path.home() / "anaconda3" / "envs"),
    ("Conda Environments", Path.home() / "miniconda3" / "envs"),
    ("Docker Images", Path("C:") / "ProgramData" / "Docker"),
    ("Windows Update Cache", Path("C:") / "Windows" / "SoftwareDistribution"),
]

for name, path in checks:
    if path.exists():
        size = get_dir_size(path)
        if size > 100 * 1024 * 1024:  # > 100 MB
            print(f"\n• {name}: {format_size(size)}")
            print(f"  Path: {path}")

# Recommendations
print("\n" + "=" * 80)
print("💡 RECOMMENDATIONS TO FREE SPACE")
print("=" * 80)

print("\n1️⃣  Move Hugging Face cache to D: drive (9.47 GB)")
print('   setx HF_HOME "D:\\huggingface_cache"')
print('   xcopy /E /I /H "C:\\Users\\Saarvik\\.cache\\huggingface" "D:\\huggingface_cache"')
print('   rmdir /s /q "C:\\Users\\Saarvik\\.cache\\huggingface"')

print("\n2️⃣  Clear pip cache")
print("   pip cache purge")

print("\n3️⃣  Clear Windows temp files")
print("   cleanmgr /d C:")

print("\n4️⃣  Check for large files manually")
print("   Use WinDirStat or TreeSize to visualize disk usage")
print("   Download: https://windirstat.net/")

print("\n5️⃣  Check Windows Update cache")
print("   Settings > System > Storage > Temporary files")

print("\n" + "=" * 80)
print("⚠️  If 30-40 GB is missing, likely culprits:")
print("=" * 80)
print("• Windows Update files (can be 10-20 GB)")
print("• System Restore points (can be 10-20 GB)")
print("• Hibernation file (hiberfil.sys, size of your RAM)")
print("• Page file (pagefile.sys, 1.5x your RAM)")
print("• Previous Windows installation (Windows.old, 10-20 GB)")
print("• Docker images (if Docker installed)")
print("• Other Python environments or conda")
print("\n💡 Use 'WinDirStat' or 'TreeSize' for visual analysis!")
print("=" * 80)
