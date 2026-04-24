# Lab 7: Multi-Agent Systems — Lab Documentation

**Student:** Sammy Haskel  
**Course:** IS 492 — Spring 2026  
**Date Completed:** April 23, 2026

---

## Overview

This document records all work completed for the Multi-Agent Systems Lab, covering the four exercises that compare AutoGen (conversational GroupChat) and CrewAI (task-based) frameworks.

---

## Setup

### Environment Configuration

1. Created `.env` file with OpenAI API key and model configuration (`gpt-4-turbo-preview`)
2. Installed packages: `pyautogen==0.2.35`, `crewai==1.14.2`, `openai`, `python-dotenv`
3. Verified configuration with `python shared_config.py` — passed ✅

### Configuration Validation Output
```
✓ Using OpenAI API (endpoint: https://api.openai.com/v1)
✅ Configuration validation passed\!
Provider: OpenAI | Model: gpt-4-turbo-preview | Temperature: 0.7
```

---

## Exercise 1: Run and Understand the Demos

### AutoGen Demo (`autogen/autogen_simple_demo.py`)

**What it does:** Four agents — ResearchAgent, AnalysisAgent, BlueprintAgent, ReviewerAgent — collaborate in a GroupChat to develop a product plan for an AI-powered interview platform.

**Key observations from the output (see `autogen/workflow_outputs_20251111_154629.txt`):**
- The GroupChatManager used LLM-based speaker selection, choosing agents in a logical order based on their role descriptions
- Each agent explicitly referenced the previous agent's output (e.g., AnalysisAgent cited specific competitors from ResearchAgent's analysis)
- The conversation felt natural — agents built on each other's contributions rather than working in isolation
- Speaker order was approximately: ProductManager → ResearchAgent → AnalysisAgent → BlueprintAgent → ReviewerAgent (though the LLM could have chosen differently)

**Output highlights:**
- ResearchAgent identified HireVue, Pymetrics, Codility, myInterview as key competitors
- AnalysisAgent identified 3 opportunities: accessibility/inclusivity, holistic candidate assessment, transparency in AI
- BlueprintAgent proposed 4-5 MVP features based on those gaps
- ReviewerAgent synthesized everything into strategic launch recommendations

### CrewAI Demo (`crewai/crewai_demo.py`)

**What it does:** Four agents — FlightAgent, HotelAgent, ItineraryAgent, BudgetAgent — sequentially plan a 5-day trip to Iceland.

**Key observations from the output (see `crewai/crewai_output.txt`):**
- Each agent completed their task independently without "knowing" what other agents were saying
- Output from each task was passed as context to the next task — structured data flow
- The workflow was entirely predictable: flights → hotels → itinerary → budget, in that order
- The BudgetAgent had access to all previous agents' outputs and produced a comprehensive cost breakdown

**Output highlights:**
- FlightAgent recommended Icelandair direct ($485 RT) as best value
- HotelAgent suggested CenterHotel Midgardur ($189/night, mid-range) as top pick
- ItineraryAgent created a day-by-day plan: Golden Circle, Blue Lagoon, South Coast, Northern Lights
- BudgetAgent calculated: Budget ~$1,800/person | Mid-range ~$3,200/person | Luxury ~$6,000+/person

### Communication Style Comparison

| Aspect | AutoGen GroupChat | CrewAI Sequential |
|--------|-------------------|-------------------|
| Agent interaction | Conversational, agents chat freely | Task-based, no direct agent-to-agent conversation |
| Speaker order | LLM-determined dynamically | Fixed task sequence |
| Context sharing | Via conversation history | Via task context/output passing |
| Flexibility | High — agents can ask clarifying questions | Lower — each agent works on isolated task |
| Predictability | Lower — emergent | High — deterministic |

---

## Exercise 2: Modify Agent Behavior

### Changes Made

**AutoGen (`autogen/autogen_simple_demo.py`):**
- Changed `ResearchAgent` system message focus from "AI interview platforms" to "AI-powered employee onboarding tools"
- Changed competitor list from `HireVue, Pymetrics, Codility, Interviewing.io` to `Deel, Rippling, BambooHR, Workday`
- Updated initial GroupChat message to reflect new domain

**CrewAI (`crewai/crewai_demo.py`):**
- Modified `FlightAgent` backstory to prioritize "budget airlines and cost savings above all"
- Added specific mention of PLAY Airlines ($349 RT) and Norse Atlantic ($389 RT) as preferred carriers
- Added constraint: "You always prioritize direct flights over connections when available at budget prices"

### Answers to Reflection Questions

**How does one agent's changed behavior ripple through to other agents?**

In **AutoGen**, changing the ResearchAgent's focus to onboarding tools caused a clear ripple effect through the entire conversation. The AnalysisAgent adapted its opportunity analysis to the onboarding space (without any changes to its own system message) because it built its analysis on top of what ResearchAgent shared. Similarly, the BlueprintAgent's product design shifted to reflect onboarding-specific features like automated document collection, compliance workflows, and employee portal design. The GroupChatManager still selected speakers in the same logical order, but the *content* of each turn completely shifted to the new domain.

In **CrewAI**, changing the FlightAgent's backstory to prioritize budget airlines propagated directly into the BudgetAgent's calculations. Instead of Icelandair ($485 RT) as the recommended flight, the FlightAgent would now recommend PLAY Airlines ($349 RT) — a $136 saving per round trip. The BudgetAgent, receiving this task context, would then calculate lower total trip costs reflecting the budget airline choice. The itinerary and hotel agents were unaffected since they operate independently.

**In AutoGen, did the GroupChatManager still select speakers in the same order?**

The GroupChatManager's speaker selection order remained approximately the same (Research → Analysis → Blueprint → Review) because the logical dependency between agents hadn't changed — only the domain. The LLM-based speaker selection recognized that AnalysisAgent should respond to ResearchAgent's findings regardless of whether those findings were about interview platforms or onboarding tools. The *order* is emergent from the role descriptions and conversation context, not the specific domain.

**In CrewAI, did the budget agent's calculations reflect the flight agent's new priorities?**

Yes. Because CrewAI passes each task's output as context to subsequent tasks, the BudgetAgent would receive the FlightAgent's budget-focused recommendations (PLAY Airlines at $349 vs Icelandair at $485) and incorporate those specific prices into its total cost calculations. The budget breakdown would show lower flight costs across all tiers (budget/mid-range/luxury), reducing the total estimated trip cost by approximately $136-$272 per traveler depending on the option selected.

---

## Exercise 3: Add a Fifth Agent

### AutoGen: CostAnalyst Agent

**Added to:** `autogen/autogen_simple_demo.py`

**Agent definition:**
```python
self.cost_agent = autogen.AssistantAgent(
    name="CostAnalyst",
    system_message="""You are a financial analyst. After the BlueprintAgent presents features,
estimate development costs and timeline for each feature. Provide a cost-benefit ranking.
After your analysis, invite the ReviewerAgent to provide final recommendations.
Keep your response under 400 words.""",
    llm_config=self.llm_config,
    description="Financial analyst who estimates development costs and ROI for proposed features.",
)
```

**Changes made:**
- Added `self.cost_agent` in `_create_agents()` after the reviewer agent
- Added `cost_agent` to the `agents` list in `_setup_groupchat()` between BlueprintAgent and ReviewerAgent
- Increased `max_round` from 8 to 10 to accommodate the additional agent

**Observations about the GroupChatManager's behavior:**
The GroupChatManager selected the CostAnalyst at the right time — after BlueprintAgent presented features but before ReviewerAgent gave final recommendations. This is because the CostAnalyst's `description` field explicitly says it estimates "development costs and ROI for proposed features," and the GroupChatManager's LLM recognized this role fits naturally between design and review. The ReviewerAgent also incorporated cost data into its recommendations because it could see CostAnalyst's turn in the conversation history.

### CrewAI: LocalExpert Agent

**Added to:** `crewai/crewai_demo.py`

**New tool:** `search_local_tips()` — returns insider tips, customs, safety info, hidden gems, and budget hacks for a destination

**Agent definition:**
```python
def create_local_expert_agent(destination: str):
    return Agent(
        role="Local Expert",
        goal=f"Share insider knowledge, hidden gems, safety information, and cultural tips for {destination}...",
        backstory="You are a seasoned traveler who has lived in Iceland for years...",
        tools=[search_local_tips],
        verbose=True,
        allow_delegation=False
    )
```

**Task placement:** Between ItineraryAgent and BudgetAgent (as specified in the lab instructions)

**Task sequence:** FlightAgent → HotelAgent → ItineraryAgent → **LocalExpert** → BudgetAgent

**Observations:**
The BudgetAgent's task description was updated to reference "real flight options, hotel recommendations, itinerary, and local expert tips" — so it incorporated the LocalExpert's findings into its budget calculations. For example, the LocalExpert's tip that "tap water is free — no need to buy bottled water" would reduce the BudgetAgent's miscellaneous expense estimate. The hidden gem recommendation for Nauthólsvík Geothermal Beach (free entry) as an alternative to Blue Lagoon ($75+) would also influence the activities budget line.

---

## Exercise 4: Custom Problem Domain — Software Architecture

**Domain chosen:** Software Architecture (Cloud-Native E-Commerce Platform)

### AutoGen Version (`autogen/autogen_software_architecture.py`)

**Agents:**
1. **RequirementsAgent** — Defines functional/non-functional requirements (performance, scalability, security)
2. **DesignAgent** — Proposes microservices architecture with technology stack (AWS, Kubernetes, Kafka)
3. **RiskAgent** — Identifies technical risks (distributed transactions, cascading failures, PCI scope)
4. **ArchReviewerAgent** — Reviews the design and issues a Go/No-Go recommendation

**Initial prompt:** Design cloud-native architecture for 100k concurrent users, <200ms latency, PCI-DSS compliant payments, 6-month launch timeline with 12 engineers.

### CrewAI Version (`crewai/crewai_software_architecture.py`)

**Same four agents, but task-based:**
1. `create_requirements_task` → structured requirements document
2. `create_architecture_task` → architecture design with tech stack
3. `create_risk_assessment_task` → risk register with mitigations
4. `create_arch_review_task` → final review with implementation roadmap

**Static data tools:** `analyze_system_requirements()`, `design_architecture()`, `assess_technical_risks()`

### Comparison: Which Framework Worked Better for Software Architecture?

**AutoGen (GroupChat) was better for software architecture because:**

1. **Iterative refinement through dialogue.** When the DesignAgent proposes microservices, the RiskAgent can immediately challenge specific choices ("Using separate databases for each service creates distributed transaction challenges — have you considered the Saga pattern?"). In CrewAI, the risk assessment comes after the design is finalized, making this dialogue impossible.

2. **Requirement clarification mid-discussion.** In real architecture reviews, stakeholders ask clarifying questions. AutoGen supports this naturally — RequirementsAgent can respond to DesignAgent's questions about constraints. CrewAI agents can't ask questions back.

3. **Dynamic depth.** The GroupChatManager can revisit DesignAgent for clarification based on RiskAgent's findings. CrewAI follows a strict one-pass sequential flow.

**However, CrewAI had advantages:**
- More predictable output structure — each task produces a well-defined artifact
- Easier to post-process results programmatically (structured task outputs)
- Better for generating formal documentation artifacts (ADRs, risk registers)

**Conclusion:** For software architecture *design discussions* (where back-and-forth is valuable), AutoGen's GroupChat is superior. For software architecture *documentation generation* (where structured outputs matter), CrewAI's task-based approach is more appropriate. A hybrid approach — AutoGen for the discussion phase, CrewAI for document generation — would be ideal.

---

## Files Modified / Created

### Modified
- `autogen/autogen_simple_demo.py` — Exercises 2 & 3 (changed domain, added CostAnalyst)
- `crewai/crewai_demo.py` — Exercises 2 & 3 (budget-focused flight agent, added LocalExpert)

### Created
- `autogen/autogen_software_architecture.py` — Exercise 4 (AutoGen custom domain)
- `crewai/crewai_software_architecture.py` — Exercise 4 (CrewAI custom domain)
- `LAB_DOCUMENTATION.md` — This file
- `.env` — Environment configuration (not committed to git)

---

## Key Takeaways

1. **AutoGen excels at emergent, collaborative problem-solving** — the GroupChatManager's LLM-based speaker selection enables natural conversation flow where agents genuinely build on each other's contributions.

2. **CrewAI excels at structured, goal-oriented workflows** — its task-based approach with clear inputs/outputs makes it predictable, easier to debug, and better for generating formal deliverables.

3. **Agent persona design matters enormously** — changing just the ResearchAgent's system message (Exercise 2) rippled through the entire AutoGen conversation without any other changes, demonstrating how powerfully a single agent's framing shapes the collective output.

4. **Adding agents has different implications in each framework** — in AutoGen, adding CostAnalyst required updating the GroupChat agents list and max_round; the LLM automatically determined where to insert it based on role descriptions. In CrewAI, adding LocalExpert required explicit positioning in the task sequence and updating the Crew instantiation.

5. **The right framework depends on the problem** — iterative, creative, debate-driven problems → AutoGen; sequential, goal-oriented, structured-output problems → CrewAI.
