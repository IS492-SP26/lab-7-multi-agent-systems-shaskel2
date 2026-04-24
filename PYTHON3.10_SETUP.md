# Python 3.10 Setup Guide

This project now uses **Python 3.10** for CrewAI compatibility. Python 3.10 has been installed via Homebrew.

## Quick Reference

### Running Scripts with Python 3.10

**AutoGen Demo:**
```bash
python3.10 autogen/autogen_simple_demo.py
```

**CrewAI Demo:**
```bash
python3.10 crewai/crewai_demo.py
```

**Configuration Check:**
```bash
python3.10 shared_config.py
```

### Installing Packages

When you need to install new packages, use `pip3.10`:

```bash
pip3.10 install package-name
```

Or install from requirements:
```bash
pip3.10 install -r requirements.txt
```

### Python 3.10 Location

Python 3.10 is installed at:
```
/opt/homebrew/bin/python3.10
```

### Creating an Alias (Optional)

To make `python3` point to Python 3.10 by default, add to your `~/.zshrc`:

```bash
alias python3=/opt/homebrew/bin/python3.10
alias pip3=/opt/homebrew/bin/pip3.10
```

Then reload:
```bash
source ~/.zshrc
```

### Verifying Installation

Check Python version:
```bash
python3.10 --version
# Should show: Python 3.10.19
```

Check pip version:
```bash
pip3.10 --version
```

## Why Python 3.10?

- **CrewAI** requires Python 3.10+ (uses modern type hints like `|` union syntax)
- **AutoGen** works with Python 3.9+, but we use 3.10 for consistency
- **Groq API** works with both versions

## Troubleshooting

### "Command not found: python3.10"
- Make sure Homebrew is installed: `brew --version`
- Reinstall: `brew install python@3.10`

### "Module not found" errors
- Install dependencies: `pip3.10 install -r requirements.txt`
- Make sure you're using `python3.10` not `python3`

### Version conflicts
- Each Python version has its own package directory
- Packages installed for Python 3.9 won't be available to Python 3.10
- Always use `pip3.10` to install packages for this project

---

**All set!** Use `python3.10` to run the demos.

