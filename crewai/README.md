# CrewAI Multi-Agent System - Complete Manual

> 🎯 **This system is fully flexible!** Plan trips to ANY destination using command-line arguments.
> Just run: `python crewai_demo.py "France" "7 days" "Los Angeles"`

## What is CrewAI?

**CrewAI** is a framework for building and orchestrating multi-agent AI systems. It enables multiple specialized AI agents to work together to solve complex tasks by:

- **Creating Specialized Agents**: Each agent has a specific role, goal, and set of tools
- **Assigning Tasks**: Clear, structured tasks that define what each agent should do
- **Managing Workflows**: Agents work in sequence or parallel, with outputs feeding into subsequent tasks
- **Tool Integration**: Agents can use specialized tools (API calls, calculations, searches) to gather information
- **Autonomous Decision-Making**: Agents make recommendations and decisions based on available information

### Key Concepts

1. **Agents**: AI-powered entities with specific expertise and responsibilities
2. **Tasks**: Explicit work units assigned to agents with clear expected outputs
3. **Tools**: Functions agents use to gather data or perform actions
4. **Crew**: The orchestrator that manages all agents and coordinates task execution
5. **Process**: How tasks are executed (sequential, parallel, or hierarchical)

---

## What Are We Doing?

We've built a **CrewAI-based Travel Planning System** that demonstrates a real-world multi-agent workflow. This system plans complete trips to ANY destination by coordinating four specialized agents.

The system is **fully flexible** - you can plan trips to any destination, for any duration, with any budget preference.

### The Team

| Agent | Expertise | Responsibility |
|-------|-----------|-----------------|
| **FlightAgent** | ✈️ Flight Specialist | Research and recommend flight options for any destination |
| **HotelAgent** | 🏨 Accommodation Specialist | Find and recommend suitable hotels for any location |
| **ItineraryAgent** | 📅 Travel Planner | Create detailed itineraries for any destination |
| **BudgetAgent** | 💰 Financial Advisor | Calculate costs and identify savings for any trip |

### Workflow Overview

```
START: Choose any destination
  ↓
FlightAgent Task: Research flights to [destination]
  ↓ (generates flight options)
HotelAgent Task: Find hotels in [destination]
  ↓ (generates hotel recommendations)
ItineraryAgent Task: Plan itinerary for [destination]
  ↓ (generates day-by-day activities)
BudgetAgent Task: Calculate total costs
  ↓ (generates budget breakdown)
END: Comprehensive Travel Plan Report
```

### What Gets Delivered

When you run this system, you get:

1. **Flight Options** (2-3 alternatives with pricing and duration)
2. **Hotel Recommendations** (3-4 options with ratings and amenities)
3. **Detailed Itinerary** (day-by-day activities tailored to destination)
4. **Budget Analysis** (cost breakdown and savings tips)

---

## How Does It Work? (Detailed Workflow)

### Phase 1: Agent Creation
Each agent is initialized with:
- **Role**: Their area of expertise (e.g., "Flight Specialist")
- **Goal**: What they need to accomplish (e.g., "Research and recommend best flight options")
- **Backstory**: Their background and expertise (helps the AI model understand the role)
- **Tools**: Functions they can use (e.g., `search_flights()`, `search_hotels()`)
- **Verbose Mode**: For tracking agent reasoning and decisions

**Example Agent Creation:**
```
FlightAgent:
  - Role: "Flight Specialist"
  - Goal: "Research and recommend best flight options for travel"
  - Tools: [search_flights()]
  - Backstory: "Expert in airline industry with 10+ years experience"
```

### Phase 2: Task Definition
Tasks define the specific work each agent performs. Each task includes:
- **Description**: Detailed instructions for what to do
- **Agent Assignment**: Which agent should execute this task
- **Expected Output**: What the agent should produce

**Example Task:**
```
Task 1 - Flight Research:
  Description: "Search for flights to Iceland departing Jan 15"
  Agent: FlightAgent
  Expected Output: "2-3 flight options with pricing and duration"
```

### Phase 3: Sequential Execution
The crew executes tasks in order:

1. **Task 1 (FlightAgent)**: Uses `search_flights()` tool
   - Returns: 3 flight options with prices
   - This output becomes context for the next agent

2. **Task 2 (HotelAgent)**: Uses `search_hotels()` tool
   - Reads context from FlightAgent output
   - Returns: 4 hotel recommendations
   - This output becomes context for the next agent

3. **Task 3 (ItineraryAgent)**: Uses `get_iceland_attractions()` tool
   - Reads context from previous agents
   - Returns: Detailed 5-day itinerary
   - This output becomes context for the final agent

4. **Task 4 (BudgetAgent)**: Analyzes all previous outputs
   - Uses no external tools (analyzes agent outputs)
   - Returns: Comprehensive budget with savings tips

### Phase 4: Output Aggregation
The crew automatically:
- Collects all task outputs
- Combines them into a final report
- Saves the report to a file

---

## Project Structure

```
crewai/
├── crewai_demo.py              # Main implementation (now fully flexible)
│   ├── Tools section
│   │   ├── search_flight_prices()
│   │   ├── search_hotel_options()
│   │   ├── search_attractions_activities()
│   │   └── search_travel_costs()
│   ├── Agent definitions (parameterized)
│   │   ├── create_flight_agent(destination, trip_dates)
│   │   ├── create_hotel_agent(destination, trip_dates)
│   │   ├── create_itinerary_agent(destination, trip_duration)
│   │   └── create_budget_agent(destination)
│   ├── Task definitions (parameterized)
│   │   ├── create_flight_task(...)
│   │   ├── create_hotel_task(...)
│   │   ├── create_itinerary_task(...)
│   │   └── create_budget_task(...)
│   └── Main function with CLI support
│       ├── Accepts destination as parameter
│       ├── Supports command-line arguments
│       └── Generates destination-specific output files
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

### Key Feature: Full Flexibility

The system now works with ANY destination:
- **Agents** dynamically adapt to the destination
- **Tasks** personalize to specific locations
- **Output files** are named after the destination
- **Command-line arguments** allow easy parameter changes

---

## Getting Started

### Step 1: Install Dependencies
```bash
cd /Users/pranavhharish/Desktop/IS-492/multi-agent/crewai
pip install -r requirements.txt
```

### Step 2: Set OpenAI API Key
```bash
export OPENAI_API_KEY="sk-proj-xxxxx"  # Replace with your actual key
```

### Step 3: Run the Demo

**Plan a trip to Iceland (default):**
```bash
python crewai_demo.py
```

**Plan a trip to any destination:**
```bash
# France - 7 days from Los Angeles
python crewai_demo.py "France" "7 days" "Los Angeles"

# Japan - 10 days from San Francisco
python crewai_demo.py "Japan" "10 days" "San Francisco"

# Spain - 5 days from Boston
python crewai_demo.py "Spain" "5 days" "Boston"

# Thailand - 8 days from New York with custom dates
python crewai_demo.py "Thailand" "8 days" "New York" "February 15-22, 2026"
```

### Step 4: Review the Output
```bash
# Default Iceland output
cat crewai_output_iceland.txt

# France output
cat crewai_output_france.txt

# Japan output
cat crewai_output_japan.txt
```

The system automatically generates output files with names like `crewai_output_[destination].txt`

---

## How It Helps (Use Cases & Benefits)

### 1. **Structured Problem Solving**
Instead of a single AI trying to solve complex problems, CrewAI breaks them into specialized subtasks:
- Each agent focuses on their expertise
- Problems are decomposed into manageable pieces
- Quality improves through specialization

### 2. **Autonomous Workflow Management**
CrewAI handles the coordination automatically:
- No manual passing of information between agents
- Tasks execute in the correct order
- Outputs automatically become inputs for next tasks

### 3. **Tool-Augmented Intelligence**
Agents don't rely only on training data:
- Can access real-time information via APIs
- Can perform calculations and analysis
- Can use specialized functions for each domain

### 4. **Explainable Decision Making**
Each agent:
- Has clear responsibilities
- Makes decisions transparently
- Outputs explain the reasoning

### 5. **Scalability & Extensibility**
Easy to extend with:
- New agents for new capabilities
- New tools for new data sources
- Different workflow patterns (parallel, hierarchical)

### 6. **Real-World Applications**

CrewAI excels at:

**Research & Analysis**
- Market research with specialized analysts
- Competitive analysis with different perspectives
- Document analysis with specialized reviewers

**Content Creation**
- Blog posts: Researcher → Outline → Writer → Editor
- Code reviews: Developer → Architect → Tester → Reviewer
- Product design: Designer → Engineer → Marketing → Reviewer

**Business Operations**
- Software development: Architect → Developer → Tester → QA
- HR onboarding: Recruiter → Scheduler → Trainer → Manager
- Project management: Planner → Resource Manager → Risk Manager → Monitor

**Complex Decision Making**
- Travel planning (this demo): Flight → Hotel → Itinerary → Budget
- Investment analysis: Analyst → Risk Manager → Compliance → Advisor
- Medical diagnosis: Doctor → Specialist → Lab Tech → Coordinator

---

## Expected Output Example

When you run the system, you'll see:

```
================================
   ICELAND TRIP PLAN REPORT
================================

FLIGHTS
-------
✈️ Option 1: Icelandair
   Dates: January 15-16, 2025
   Duration: 6h 30m
   Price: $450
   Recommendation: Best value and comfort

HOTELS
------
🏨 ION Adventure Hotel
   Rating: 4.8 stars
   Price: $320/night
   Amenities: Spa, Hot tub, Restaurant

🏨 Golden Circle Hotel
   Rating: 4.5 stars
   Price: $210/night
   Amenities: Mountain views, Hiking trails

5-DAY ITINERARY
---------------
📅 Day 1: Arrival & Blue Lagoon
   - Arrive, rest, Blue Lagoon (geothermal spa)

📅 Day 2: Golden Circle
   - Þingvellir National Park
   - Geysir (active geysers)
   - Gullfoss (waterfall)

📅 Day 3: South Coast
   - Seljalandsfoss waterfall
   - Skógafoss waterfall
   - Black sand beach

📅 Day 4: Free day or North Iceland
   - Relax or explore Akureyri

📅 Day 5: Departure
   - Morning shopping, afternoon flight

BUDGET ANALYSIS
---------------
💰 Budget Option: $2,200
   - Flights: $450
   - Hotel (budget): $150/night × 3 = $450
   - Activities & meals: $1,300

💰 Mid-Range Option: $3,100
   - Flights: $450
   - Hotel (mid-range): $210/night × 3 = $630
   - Activities & meals: $2,020

💰 Luxury Option: $4,500+
   - Flights: $450-520
   - Hotel (luxury): $280+/night × 3 = $840+
   - Activities & exclusive tours: $3,200+

Savings Tips:
- Book 2-3 weeks in advance
- Visit free attractions (geysers, waterfalls)
- Use public transport instead of car rental
```

---

## Key Technologies

- **Python 3.8+**: Programming language
- **CrewAI Framework**: Multi-agent orchestration
- **OpenAI API**: Language models for agent reasoning
- **Python Functions**: Tool implementations

---

## Architecture Advantages

### Modularity
- Add/remove agents without affecting others
- Test agents independently
- Swap tools for different implementations

### Maintainability
- Clear agent responsibilities
- Explicit task definitions
- Well-documented code structure

### Extensibility
- Easy to add new agents
- Easy to add new tools
- Easy to change workflow patterns

### Reliability
- Automatic error handling
- Clear output validation
- Explicit task dependencies

---

## Customization Examples

### Change Destination (Command Line)

The system now accepts command-line arguments! Plan trips anywhere:

```bash
# Default: Iceland trip from New York
python crewai_demo.py

# France trip from Los Angeles
python crewai_demo.py "France" "7 days" "Los Angeles"

# Japan trip from San Francisco
python crewai_demo.py "Japan" "10 days" "San Francisco"

# Spain trip from Boston
python crewai_demo.py "Spain" "5 days" "Boston" "March 1-5, 2026"
```

### Programmatic Usage

You can also call the function directly with parameters:

```python
from crewai_demo import main

# Plan a trip to France
main(
    destination="France",
    trip_duration="7 days",
    trip_dates="March 15-21, 2026",
    departure_city="Los Angeles",
    travelers=2,
    budget_preference="luxury"
)

# Plan a trip to Japan
main(
    destination="Japan",
    trip_duration="10 days",
    trip_dates="April 1-10, 2026",
    departure_city="San Francisco",
    travelers=4,
    budget_preference="mid-range"
)
```

### Add a New Agent

Create a WeatherAgent (example):
```python
weather_agent = Agent(
    role="Weather Advisor",
    goal=f"Provide weather information and recommendations for {destination}",
    backstory="Expert meteorologist with global expertise",
    tools=[get_weather_forecast()],
    verbose=True
)
```

### Integrate Real APIs

Replace tools with real API implementations:
```python
def search_flights(destination, dates):
    return skyscanner_api.search(destination, dates)
```

### Change Execution Style

Use parallel execution for independent tasks:
```python
crew = Crew(
    agents=[...],
    tasks=[...],
    process="hierarchical"  # or "parallel"
)
```

---

## Comparison: Why CrewAI?

| Feature | CrewAI | Traditional Scripts | Single AI Model |
|---------|--------|-------------------|-----------------|
| **Specialization** | ✅ Multiple experts | ❌ Single focus | ❌ Single focus |
| **Workflow** | ✅ Explicit tasks | ❌ Ad-hoc | ❌ Ad-hoc |
| **Scalability** | ✅ Easy to extend | ❌ Complicated | ❌ Hit token limits |
| **Explainability** | ✅ Clear roles | ❌ Black box | ❌ Black box |
| **Tool Integration** | ✅ Built-in support | ✅ Manual | ❌ Limited |
| **Debugging** | ✅ Clear outputs | ✅ Manual | ❌ Hard to trace |

---

## Next Steps

### To Get Started
1. Run: `python crewai_demo.py`
2. Review the output in `crewai_output.txt`
3. Modify the destination in the code

### To Extend
1. Add new agents for different expertise
2. Integrate real APIs instead of mock data
3. Experiment with different workflow patterns

### To Learn More
- [CrewAI Official Documentation](https://docs.crewai.com/)
- [CrewAI GitHub Repository](https://github.com/joaomdmoura/crewai)
- [Multi-Agent Systems Overview](https://lilianweng.github.io/posts/2023-06-23-agent/)

---

## Summary

CrewAI provides a powerful framework for:
- ✅ Creating specialized AI agents
- ✅ Coordinating complex workflows
- ✅ Integrating external tools and APIs
- ✅ Building autonomous, explainable systems

This implementation demonstrates how multi-agent systems can solve complex, multi-step problems (like trip planning) more effectively than single AI models by leveraging specialization, autonomous decision-making, and structured workflows.

**Status**: ✅ Complete and Ready to Run

---

**Framework**: CrewAI
**Lab**: Multi-Agent Systems (IS-492)
**Language**: Python 3.8+
**Date**: January 11, 2025
