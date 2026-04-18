"""
Quick script to check GPU availability and PyTorch CUDA support
"""

import sys

print("=" * 60)
print("🔍 GPU & CUDA Detection")
print("=" * 60)

# Check PyTorch
try:
    import torch
    print(f"✅ PyTorch installed: {torch.__version__}")
    
    # Check CUDA availability
    cuda_available = torch.cuda.is_available()
    print(f"\n{'✅' if cuda_available else '❌'} CUDA Available: {cuda_available}")
    
    if cuda_available:
        print(f"✅ CUDA Version: {torch.version.cuda}")
        print(f"✅ GPU Count: {torch.cuda.device_count()}")
        
        for i in range(torch.cuda.device_count()):
            print(f"\n🎮 GPU {i}:")
            print(f"   Name: {torch.cuda.get_device_name(i)}")
            print(f"   Memory: {torch.cuda.get_device_properties(i).total_memory / 1024**3:.2f} GB")
            print(f"   Compute Capability: {torch.cuda.get_device_properties(i).major}.{torch.cuda.get_device_properties(i).minor}")
        
        # Test tensor on GPU
        print("\n🧪 Testing GPU tensor creation...")
        try:
            test_tensor = torch.randn(100, 100).cuda()
            print(f"✅ Successfully created tensor on GPU: {test_tensor.device}")
            del test_tensor
            torch.cuda.empty_cache()
        except Exception as e:
            print(f"❌ Failed to create tensor on GPU: {e}")
    else:
        print("\n⚠️  CUDA not available. Possible reasons:")
        print("   1. PyTorch CPU-only version installed")
        print("   2. NVIDIA drivers not installed")
        print("   3. No NVIDIA GPU detected")
        print("\n💡 To install CUDA-enabled PyTorch:")
        print("   pip uninstall torch")
        print("   pip install torch --index-url https://download.pytorch.org/whl/cu118")
    
except ImportError:
    print("❌ PyTorch not installed")
    print("   Install with: pip install torch")
    sys.exit(1)

# Check transformers
try:
    import transformers
    print(f"\n✅ Transformers installed: {transformers.__version__}")
except ImportError:
    print("\n❌ Transformers not installed")
    print("   Install with: pip install transformers")

# Check accelerate
try:
    import accelerate
    print(f"✅ Accelerate installed: {accelerate.__version__}")
except ImportError:
    print("❌ Accelerate not installed")
    print("   Install with: pip install accelerate")

print("\n" + "=" * 60)
print("📊 Summary")
print("=" * 60)

if cuda_available:
    print("✅ Your system is ready for GPU-accelerated LLM!")
    print("✅ Set LLM_ENABLED = True in backend/config.py")
    print("✅ Expected response time: 1-3 seconds")
else:
    print("⚠️  GPU not available - will use CPU fallback")
    print("⚠️  Expected response time: 30-60 seconds")
    print("💡 Consider installing CUDA-enabled PyTorch for faster inference")

print("=" * 60)
