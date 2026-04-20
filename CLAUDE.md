# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **educational lab for comparing multi-agent frameworks**: AutoGen (Microsoft) vs CrewAI. Students learn how multiple AI agents can collaborate to solve complex problems, understand different architectural approaches, and make informed framework choices.

Two parallel demo workflows exist:
1. **AutoGen Demo** (`autogen/autogen_simple_demo.py`) - Conversational agent coordination for product planning
2. **CrewAI Demo** (`crewai/crewai_demo.py`) - Task-based agent orchestration for travel planning

## Architecture & Key Design Decisions

### Unified Configuration System

All configuration is centralized in two files:
- **`shared_config.py`** (root) - Single source of truth for both frameworks
  - Loads from `.env` file at project root using `python-dotenv`
  - Provides `Config` class with OpenAI API settings, agent parameters, logging flags
  - Accessible to both frameworks via `from shared_config import Config`

- **`autogen/config.py`** - Extends `shared_config.Config` with AutoGen-specific settings
  - Adds AutoGen configuration methods: `get_config_list()`, `validate_setup()`, `get_summary()`
  - Defines agent configurations via `AgentConfig` class (roles, temperatures, etc.)
  - Defines workflow phases via `WorkflowConfig` class

- **`crewai/crewai_demo.py`** - Imports and uses `shared_config.Config` directly
  - Configuration imported at module level: `from shared_config import Config, validate_config`
  - Creates CrewAI agents with `Agent(role="...", goal="...", backstory="...")`
  - Creates tasks with `Task(description="...", agent=..., expected_output="...")`

### Framework Integration Patterns

**AutoGen Pattern:**
```python
# In autogen/ directory
from config import Config  # Extends shared_config
config_list = Config.get_config_list()  # Returns list of dicts for LLM config
llm_config = {"config_list": config_list, "temperature": Config.AGENT_TEMPERATURE}
# Agents placed in GroupChat, GroupChatManager orchestrates conversation
groupchat = autogen.GroupChat(agents=[...], messages=[], max_round=8)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
user_proxy.initiate_chat(manager, message="...")
```

**CrewAI Pattern:**
```python
# In crewai/ directory, import from parent
import sys; sys.path.insert(0, str(Path(__file__).parent.parent))
from shared_config import Config
# Agents receive tasks, execute independently, output passed to next task
```

### Project Structure

```
multi-agent/
├── README.md                    # Complete student lab guide
├── requirements.txt             # Single unified dependencies file
├── CLAUDE.md                    # This file
├── .env.example                 # Configuration template
├── .env                         # Actual config (students fill this)
├── shared_config.py             # Unified config module
│
├── autogen/
│   ├── config.py               # AutoGen-specific config (extends shared_config)
│   ├── autogen_simple_demo.py  # GroupChat demo - run this
│   └── README.md               # AutoGen-specific details
│
└── crewai/
    ├── crewai_demo.py          # Travel planning demo - run this
    └── README.md               # CrewAI-specific details
```

## Running & Testing

### Initial Setup
```bash
# 1. Configure environment
cp .env.example .env
# Edit .env - add OPENAI_API_KEY=sk-...

# 2. Install all dependencies (single command)
pip install -r requirements.txt

# 3. Verify configuration
python shared_config.py
```

### Run Demos

**AutoGen Demo:**
```bash
python autogen/autogen_simple_demo.py
```
- Uses GroupChat with GroupChatManager for true multi-agent conversation
- Five participants: UserProxyAgent (initiator) + four AssistantAgents
- LLM-based speaker selection decides who speaks each turn
- Focus: Understanding conversational multi-agent collaboration

**CrewAI Demo:**
```bash
python crewai/crewai_demo.py
```
- Uses task-based agent orchestration
- Four agents executing sequential tasks (Flight → Hotel → Itinerary → Budget)
- Focus: Understanding structured task workflows

### Validation

The `shared_config.Config.validate()` method checks for:
- Required `OPENAI_API_KEY` presence
- Prints helpful error messages if configuration is missing
- Called by both framework demos before execution

```bash
# Direct validation
python shared_config.py
```

## Configuration Management

### Environment Variables (in .env)

**Required:**
- `OPENAI_API_KEY` - OpenAI API key for LLM access

**Optional (have defaults):**
- `OPENAI_API_BASE` - API endpoint (default: `https://api.openai.com/v1`)
- `OPENAI_MODEL` - Model to use (default: `gpt-4-turbo-preview`)
- `AGENT_TEMPERATURE` - Creativity level (default: 0.7)
- `AGENT_MAX_TOKENS` - Response limit (default: 2000)
- `AGENT_TIMEOUT` - Timeout seconds (default: 300)
- `VERBOSE` - Enable detailed output (default: True)
- `DEBUG` - Enable debug mode (default: False)

### Adding New Configuration

1. Add to `.env.example` and `.env`
2. Add to `shared_config.Config` class with defaults
3. Document in README.md
4. Both frameworks automatically have access via `Config.ATTRIBUTE_NAME`

## Common Development Tasks

### Modify Agent Definitions

**For AutoGen:**
- Edit `autogen/config.py` - Update `AgentConfig` and `WorkflowConfig` classes
- Add/modify agent roles, descriptions, and workflow phases
- Framework-specific: `get_config_list()` handles conversion to AutoGen format

**For CrewAI:**
- Edit `crewai/crewai_demo.py` - Update agent creation functions
- Modify `Agent(role="...", goal="...", backstory="...")` definitions
- Add/modify tasks with `Task(description="...", expected_output="...")`

### Add New Framework Features

- **AutoGen:** Implement in `autogen_simple_demo.py`
- **CrewAI:** Implement in `crewai_demo.py` (single comprehensive file)
- Both have access to shared configuration - no duplication needed

### Extend Configuration

All configuration changes go in `shared_config.py`:
- Add class attribute with default
- Use `os.getenv("KEY", "default")`
- Both frameworks will automatically have access

## Key Implementation Details

### Agent Communication (AutoGen vs CrewAI)

**AutoGen:**
- GroupChat: all agents placed in a shared conversation
- GroupChatManager uses LLM to select next speaker each turn
- Agents see full conversation history and reference each other's contributions
- File: `autogen_simple_demo.py` creates agents, GroupChat, and calls `user_proxy.initiate_chat(manager)`

**CrewAI:**
- Task-based: each agent receives structured task input
- Sequential: output of one agent becomes context for next
- File: `crewai_demo.py` defines agents, tasks, then `crew.kickoff()`

### Output Handling

**AutoGen:**
- `groupchat.messages` contains full conversation history
- `chat_result.summary` provides LLM-generated reflection summary
- Saves conversation + summary to timestamped file

**CrewAI:**
- Returns `expected_output` from each task
- Provides task execution summary
- Saves results to file (`crewai_output.txt`)

### Error Handling Patterns

Both demos include:
- Configuration validation at startup (exit if invalid)
- ImportError catching for missing framework (helpful message)
- Try/except around crew execution with detailed error messages
- Troubleshooting hints in error output

## Testing Approach

### Quick Validation
```bash
python shared_config.py
# Validates .env configuration without running full demos
```

### Demo Execution
- AutoGen: Lightweight version first (`autogen_simple_demo.py`)
- CrewAI: Single comprehensive version (`crewai_demo.py`)
- Both print detailed output for understanding agent behavior

### Configuration Testing
Change `.env` variables and re-run demos to test:
- Temperature adjustment (affects response creativity)
- Model switching (if you want to test different models)
- Timeout values (test with slow API responses)

## Important Notes for Future Development

1. **Configuration is centralized** - Any config change affects both frameworks
2. **Students should NOT edit individual framework config files** - Only edit `.env` and `shared_config.py`
3. **Framework-specific settings** live in their config.py (AutoGen) or demo file (CrewAI)
4. **Path resolution** - Both frameworks use `sys.path.insert(0, parent_dir)` to import shared_config from root
5. **API costs** - Both frameworks use real OpenAI API calls - monitor usage
6. **.env file is NOT committed** - It's in `.gitignore` for security (students create their own)

## Documentation References

- **Student Guide:** See `README.md` (comprehensive lab manual)
- **Framework Specifics:** See `autogen/README.md` and `crewai/README.md`
- **AutoGen Docs:** https://microsoft.github.io/autogen/
- **CrewAI Docs:** https://docs.crewai.com/
