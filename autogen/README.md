# AutoGen Multi-Agent GroupChat Demo

## What is AutoGen?

**AutoGen** is Microsoft's open-source framework for building multi-agent AI applications. Agents communicate conversationally in a **GroupChat**, where a **GroupChatManager** uses LLM-based speaker selection to decide who speaks next each turn.

---

## What Are We Doing?

We've built a **multi-agent product planning system** where four AI agents collaborate in a GroupChat to create a product plan for an AI-powered interview platform.

```
┌─────────────────────────────────────────────────────────┐
│                      GroupChat                           │
│                                                         │
│  ProductManager (initiator)                             │
│       ↓ kicks off discussion                            │
│  ResearchAgent ←→ AnalysisAgent ←→ BlueprintAgent      │
│                         ↕                               │
│                   ReviewerAgent                          │
│                                                         │
│  GroupChatManager selects next speaker via LLM          │
└─────────────────────────────────────────────────────────┘
```

Unlike a sequential pipeline, agents here:
- **See the full conversation** — each agent reads all previous messages
- **Reference each other** — agents build on and respond to prior contributions
- **Emerge organically** — speaker order is selected by the LLM, not hardcoded

---

## Quick Start

```bash
# From the project root directory:
python autogen/autogen_simple_demo.py
```

Expected duration: 1-3 minutes depending on model speed.

---

## Project Structure

```
autogen/
├── README.md                  # This file
├── config.py                  # Configuration (extends shared_config)
└── autogen_simple_demo.py     # GroupChat demo — run this

Shared configuration (parent directory):
├── ../.env                    # API credentials
└── ../shared_config.py        # Shared config class
```

---

## How It Works

### Agents

| Agent | Role | When It Speaks |
|-------|------|----------------|
| **ProductManager** | UserProxyAgent — initiates discussion | First (once) |
| **ResearchAgent** | Competitive landscape analysis | After kickoff |
| **AnalysisAgent** | Identifies market opportunities | After research |
| **BlueprintAgent** | Designs features and user journey | After analysis |
| **ReviewerAgent** | Strategic recommendations, says TERMINATE | Last |

### Key AutoGen Concepts

```python
import autogen

# 1. Create specialized agents
research_agent = autogen.AssistantAgent(
    name="ResearchAgent",
    system_message="Your role in this group discussion is to...",
    llm_config=llm_config,
    description="Used by GroupChatManager for speaker selection.",
)

# 2. Assemble into GroupChat
groupchat = autogen.GroupChat(
    agents=[user_proxy, research_agent, analysis_agent, ...],
    messages=[],
    max_round=8,                        # Cost cap
    speaker_selection_method="auto",    # LLM picks next speaker
    allow_repeat_speaker=False,         # Each turn is a different agent
    send_introductions=True,            # Agents know who else is in the chat
)

# 3. GroupChatManager orchestrates
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# 4. Start the conversation
user_proxy.initiate_chat(manager, message="Team, let's plan...")
```

### Termination

The conversation ends when:
- **ReviewerAgent says "TERMINATE"** — instructed in its system message
- **max_round reached** (8) — hard cap to prevent runaway costs

---

## Configuration

Uses shared `.env` from parent directory:

```
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview
AGENT_TEMPERATURE=0.7
```

See `config.py` for AutoGen-specific extensions (`get_config_list()`, `validate_setup()`).

---

## Output

The demo produces:
- **Console output** — full conversation printed in real-time as agents speak
- **File output** — `groupchat_output_YYYYMMDD_HHMMSS.txt` with full transcript + executive summary

---

## Customization

### Change the Topic
Edit the `initial_message` in `autogen_simple_demo.py`:
```python
initial_message = """Team, we need to develop a product plan for a
[YOUR TOPIC HERE]..."""
```

### Modify Agent Behavior
Edit the `system_message` of any agent in `_create_agents()`. The key is making prompts **group-aware** — agents should know about each other and when to speak.

### Add a New Agent
1. Create an `AssistantAgent` in `_create_agents()` with a `description`
2. Add it to the agents list in `_setup_groupchat()`
3. Increase `max_round` to accommodate the extra turn

---

## Comparison with CrewAI

| Aspect | AutoGen (this demo) | CrewAI |
|--------|-------------------|--------|
| Pattern | GroupChat conversation | Task-based pipeline |
| Speaker order | LLM-selected (emergent) | Fixed sequential |
| Agent awareness | Full conversation history | Only previous task output |
| Orchestration | GroupChatManager | Crew with process="sequential" |
| Termination | Agent says TERMINATE | All tasks complete |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "API key not found" | Ensure `../.env` has `OPENAI_API_KEY=sk-...` |
| "Module not found" | Run from project root: `python autogen/autogen_simple_demo.py` |
| Slow responses | Switch to `gpt-3.5-turbo` in `.env` |
| High cost | `max_round=8` already limits this; reduce if needed |

---

## Resources

- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [GroupChat Tutorial](https://microsoft.github.io/autogen/docs/tutorial/conversation-patterns#group-chat)
- [AutoGen GitHub](https://github.com/microsoft/autogen)
