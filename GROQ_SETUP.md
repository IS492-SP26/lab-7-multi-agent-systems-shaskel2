# 🚀 Groq API Setup Guide

This project now supports **Groq API** in addition to OpenAI! Groq offers a free tier with generous rate limits, making it perfect for learning and experimentation.

## Quick Setup (3 Steps)

### Step 1: Get Your Groq API Key

1. Visit [Groq Console](https://console.groq.com)
2. Sign up or log in (it's free!)
3. Navigate to **API Keys** section
4. Click **Create API Key**
5. Copy your API key (it will look like: `gsk_...`)

### Step 2: Create `.env` File

In the project root directory, create a `.env` file:

```bash
cd /Users/yvw/Documents/teaching/Lab-7/multi-agents-lab
nano .env
```

Add your Groq API key:

```bash
GROQ_API_KEY=your-groq-api-key-here
```

**Optional:** Choose a specific model (default is `llama-3.3-70b-versatile`):

```bash
GROQ_API_KEY=your-groq-api-key-here
GROQ_MODEL=llama-3.3-70b-versatile
```

### Step 3: Verify Configuration

```bash
python shared_config.py
```

You should see:
```
✓ Using Groq API (endpoint: https://api.groq.com/openai/v1)
✅ Configuration validation passed!
```

## Available Groq Models

| Model | Description | Best For |
|-------|-------------|----------|
| `llama-3.3-70b-versatile` | Default, high quality | Complex reasoning, detailed analysis |
| `llama-3.3-8b-instant` | Fast, smaller model | Quick responses, simple tasks |
| `llama-3.1-8b-instant` | Alternative fast model | Quick responses |
| `gemma2-9b-it` | Balanced performance | General purpose |

To use a different model, add to your `.env`:
```bash
GROQ_MODEL=llama-3.3-8b-instant
```

**Important:** Groq frequently updates their model lineup. If you get a "model decommissioned" error:
1. Check [Groq's deprecations page](https://console.groq.com/docs/deprecations) for current recommendations
2. Visit [Groq's models page](https://console.groq.com/docs/models) for available models
3. Update your `GROQ_MODEL` in `.env` with a current model name

## Running the Demos

Once configured, run the demos exactly as before:

**AutoGen Demo:**
```bash
python autogen/autogen_simple_demo.py
```

**CrewAI Demo:**
```bash
python crewai/crewai_demo.py
```

The system will automatically detect and use your Groq API key!

## Switching Between Groq and OpenAI

The system automatically detects which API key you have configured:

- **If `GROQ_API_KEY` is set:** Uses Groq (priority)
- **If only `OPENAI_API_KEY` is set:** Uses OpenAI
- **If both are set:** Uses Groq (Groq has priority)

To switch to OpenAI, simply remove or comment out `GROQ_API_KEY` in your `.env`:

```bash
# GROQ_API_KEY=your-groq-key  # Commented out
OPENAI_API_KEY=sk-your-openai-key
```

## Example `.env` File

```bash
# Using Groq (recommended for free tier)
GROQ_API_KEY=gsk_your_actual_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Agent settings
AGENT_TEMPERATURE=0.7
AGENT_MAX_TOKENS=2000
VERBOSE=True
```

## Troubleshooting

### "No API key is configured"
- Make sure your `.env` file is in the project root directory
- Check that `GROQ_API_KEY=...` is on a single line (no spaces around `=`)
- Verify the file is named exactly `.env` (not `.env.txt`)

### "Invalid API key"
- Double-check your Groq API key from https://console.groq.com
- Make sure there are no extra spaces or quotes around the key
- Try regenerating a new API key

### "Model not found"
- Check that your model name is correct (see Available Models above)
- Some models may not be available in all regions
- Try using `llama-3.1-70b-versatile` (the default)

### Rate Limits
- Groq has generous free tier limits
- If you hit limits, wait a few minutes and try again
- Check your usage at https://console.groq.com

## Benefits of Using Groq

✅ **Free Tier Available** - No credit card required  
✅ **Fast Responses** - Optimized for speed  
✅ **OpenAI-Compatible** - Works with existing code  
✅ **Generous Limits** - Great for learning and experimentation  

## Need Help?

1. Verify configuration: `python shared_config.py`
2. Check Groq status: https://status.groq.com
3. Review Groq docs: https://console.groq.com/docs

---

**Ready to go?** Run `python shared_config.py` to verify your setup!

