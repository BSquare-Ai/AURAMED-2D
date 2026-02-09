# Enabling BiomedGPT - Quick Guide

## ✅ What I've Done

1. **Updated BiomedGPT Model Wrapper** (`src/models/biomedgpt_model.py`):
   - Now automatically tries to load from HuggingFace if no local path is provided
   - Attempts models in order: `PanaceaAI/BiomedGPT-base`, `medium`, `tiny`
   - Falls back gracefully if models aren't available

2. **Updated Reasoning Agent** (`src/agents/reasoning_agent.py`):
   - Will attempt to load BiomedGPT even if path is `null`
   - Tries HuggingFace automatically
   - Uses fallback if model not available

3. **Updated Configuration**:
   - `biomedgpt_path: null` now means "try HuggingFace first"
   - Can still specify local path if you have checkpoints

## 🚀 How It Works Now

**Automatic Loading (Recommended):**
```yaml
# configs/pipeline_config.yaml
agents:
  reasoning:
    biomedgpt_path: null  # Will try HuggingFace automatically
    device: "cuda"
    max_tokens: 512
```

The system will:
1. Try to load from HuggingFace (PanaceaAI/BiomedGPT-*)
2. Download model on first use (may take time)
3. Use fallback if download fails or models unavailable

**Manual Path (If you have local checkpoints):**
```yaml
agents:
  reasoning:
    biomedgpt_path: "/path/to/biomedgpt/checkpoint"
    device: "cuda"
```

## 📥 Downloading Models

### Option 1: Automatic (HuggingFace)
Models will download automatically on first use when you run the demo.

### Option 2: Manual Download
1. **HuggingFace Collection**: https://huggingface.co/collections/PanaceaAI/biomedgpt-v1-66ca7c51e378662e15178be3
2. **Dropbox (Original)**: https://www.dropbox.com/sh/cu2r5zkj2r0e6zu/AADZ-KHn-emsICawm9CM4MqVa?dl=0

## ✅ Verification

To check if BiomedGPT is enabled:

```python
from src.agents.reasoning_agent import ReasoningAgent
import yaml

with open('configs/pipeline_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

agent = ReasoningAgent(config=config['agents']['reasoning'])
print(f"Model loaded: {agent.model is not None}")
if agent.model and hasattr(agent.model, 'model'):
    print(f"BiomedGPT ready: {agent.model.model is not None}")
```

**Expected Output:**
- ✅ `Model loaded: True` → BiomedGPT is enabled
- ❌ `Model loaded: False` → Using fallback (normal if models not downloaded)

## 🔍 Check Logs

When you run the demo, check for:
- ✅ `"✓ BiomedGPT reasoning model loaded successfully"` → Enabled
- ⚠️ `"BiomedGPT model not available, using fallback"` → Fallback (still works)

## 📝 Notes

- **First Run**: May take time to download models from HuggingFace
- **Internet Required**: For HuggingFace model download
- **Fallback Works**: Even without BiomedGPT, reasoning agent provides responses
- **Model Size**: BiomedGPT models are large (several GB)

## 🎯 Next Steps

1. **Run the demo** - It will attempt to load BiomedGPT automatically
2. **Check logs** - See if model loaded successfully
3. **Test queries** - BiomedGPT will be used if loaded, fallback otherwise

The system is now configured to automatically try to enable BiomedGPT!

