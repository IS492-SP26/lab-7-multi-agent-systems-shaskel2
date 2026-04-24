"""
AutoGen GroupChat Demo - Software Architecture Design
======================================================

EXERCISE 4: Custom Problem Domain

This demonstrates AutoGen's GroupChat approach applied to a NEW domain:
Software Architecture for a Cloud-Native E-Commerce Platform.

Four agents collaborate in a GroupChat (LLM selects who speaks next):
1. RequirementsAgent - Gathers and analyzes system requirements
2. DesignAgent      - Proposes high-level architecture and technology stack
3. RiskAgent        - Identifies technical risks and mitigation strategies
4. ArchReviewerAgent - Reviews design and provides final recommendations

Communication Style: Conversational GroupChat (agents build on each other's ideas)

Compare with crewai_software_architecture.py which uses task-based orchestration.
"""

import os
from datetime import datetime
from config import Config

try:
    import autogen
except ImportError:
    print("ERROR: AutoGen is not installed\!")
    print("Please run: pip install -r ../requirements.txt")
    exit(1)


class SoftwareArchitectureGroupChat:
    """Multi-agent GroupChat workflow for software architecture design using AutoGen"""

    def __init__(self):
        if not Config.validate_setup():
            print("ERROR: Configuration validation failed\!")
            exit(1)

        self.config_list = Config.get_config_list()
        self.llm_config = {"config_list": self.config_list, "temperature": Config.AGENT_TEMPERATURE}

        self._create_agents()
        self._setup_groupchat()
        print("All AutoGen architecture agents created and GroupChat initialized.")

    def _create_agents(self):
        """Create UserProxyAgent and 4 specialist AssistantAgents for software architecture"""

        self.user_proxy = autogen.UserProxyAgent(
            name="ProductOwner",
            system_message="A product owner who initiates the architecture discussion for the cloud-native e-commerce platform.",
            human_input_mode="NEVER",
            code_execution_config=False,
            max_consecutive_auto_reply=0,
            is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
        )

        self.requirements_agent = autogen.AssistantAgent(
            name="RequirementsAgent",
            system_message="""You are a senior systems analyst specializing in cloud-native applications.
Your role is to START the conversation by defining clear system requirements.

Your responsibilities:
- Define functional requirements (what the system must DO): search, cart, checkout, orders, inventory
- Define non-functional requirements (NFRs): performance (< 200ms latency), scalability (100k concurrent users),
  availability (99.9% uptime), security (PCI-DSS compliance for payments)
- Identify key constraints: budget, team size, timeline, existing tech debt
- Define quality attributes that will drive architecture decisions

After presenting requirements, invite the DesignAgent to propose an architecture based on these requirements.
Keep your response focused and under 400 words.""",
            llm_config=self.llm_config,
            description="Senior systems analyst who defines functional and non-functional requirements.",
        )

        self.design_agent = autogen.AssistantAgent(
            name="DesignAgent",
            system_message="""You are a principal software architect with expertise in cloud-native systems.
Your role is to BUILD ON the RequirementsAgent's findings and propose an architecture.

Your responsibilities:
- Propose a high-level architecture (microservices, event-driven, etc.) that meets the requirements
- Define key architectural components: API Gateway, service mesh, databases, caching, messaging
- Recommend a technology stack (AWS/GCP/Azure, Kubernetes, specific databases)
- Explain how the architecture addresses each key requirement
- Identify any architectural trade-offs being made

Reference specific requirements from the RequirementsAgent when justifying choices.
After presenting the architecture, invite the RiskAgent to identify technical risks.
Keep your response focused and under 400 words.""",
            llm_config=self.llm_config,
            description="Principal software architect who proposes architecture and technology stack.",
        )

        self.risk_agent = autogen.AssistantAgent(
            name="RiskAgent",
            system_message="""You are a senior DevOps/SRE engineer specializing in risk analysis.
Your role is to IDENTIFY technical risks in the proposed architecture.

Your responsibilities:
- Identify 3-4 key technical risks in the proposed architecture
- For each risk: describe it, rate its probability/impact, and propose a mitigation strategy
- Highlight single points of failure, data consistency challenges, or scalability bottlenecks
- Suggest monitoring, alerting, and incident response considerations
- Address operational concerns: deployment complexity, team skill gaps, maintenance burden

Reference specific architectural choices from the DesignAgent when identifying risks.
After presenting risks, invite the ArchReviewerAgent to give final recommendations.
Keep your response focused and under 400 words.""",
            llm_config=self.llm_config,
            description="Senior SRE who identifies technical risks and mitigation strategies in the architecture.",
        )

        self.arch_reviewer_agent = autogen.AssistantAgent(
            name="ArchReviewerAgent",
            system_message="""You are a VP of Engineering and architecture review board chair.
Your role is to REVIEW the proposed architecture and provide a final decision.

Your responsibilities:
- Evaluate whether the architecture adequately meets the stated requirements
- Assess whether the risk mitigations proposed are sufficient
- Provide 3-4 actionable recommendations for implementation
- Suggest an implementation roadmap (Phase 1: foundation → Phase 2: scale → Phase 3: optimize)
- Give a final go/no-go recommendation with specific conditions

Reference the requirements, architecture, and risks from the earlier discussion.
End your review with the word TERMINATE.""",
            llm_config=self.llm_config,
            description="VP of Engineering who reviews the architecture and provides final recommendations.",
        )

    def _setup_groupchat(self):
        """Create the GroupChat and GroupChatManager"""
        self.groupchat = autogen.GroupChat(
            agents=[
                self.user_proxy,
                self.requirements_agent,
                self.design_agent,
                self.risk_agent,
                self.arch_reviewer_agent,
            ],
            messages=[],
            max_round=10,
            speaker_selection_method="auto",
            allow_repeat_speaker=False,
            send_introductions=True,
        )

        self.manager = autogen.GroupChatManager(
            groupchat=self.groupchat,
            llm_config=self.llm_config,
            is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
        )

    def run(self):
        """Execute the GroupChat workflow"""
        print("\n" + "=" * 80)
        print("AUTOGEN GROUPCHAT - SOFTWARE ARCHITECTURE DESIGN")
        print("Cloud-Native E-Commerce Platform")
        print("=" * 80)
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Model: {Config.OPENAI_MODEL}")
        print(f"Max Rounds: {self.groupchat.max_round}")
        print("\nAgents in GroupChat:")
        for agent in self.groupchat.agents:
            print(f"  - {agent.name}")
        print("\n" + "=" * 80)
        print("MULTI-AGENT ARCHITECTURE DISCUSSION BEGINS")
        print("=" * 80 + "\n")

        initial_message = """Team, we need to design a cloud-native e-commerce platform architecture.

The platform needs to support:
- 100,000 concurrent users during peak traffic (Black Friday)
- Sub-200ms response times for product search and browsing
- Payment processing (must be PCI-DSS compliant)
- Real-time inventory management
- A 6-month launch timeline with a team of 12 engineers

Let's collaborate:
1. RequirementsAgent: Start by defining functional and non-functional requirements
2. DesignAgent: Propose an architecture that meets those requirements
3. RiskAgent: Identify technical risks and mitigation strategies
4. ArchReviewerAgent: Review the design and provide final recommendations

RequirementsAgent, please begin with the requirements analysis."""

        chat_result = self.user_proxy.initiate_chat(
            self.manager,
            message=initial_message,
            summary_method="reflection_with_llm",
            summary_args={
                "summary_prompt": "Summarize the complete software architecture plan developed through this discussion. Include: key requirements, proposed architecture, identified risks, and final recommendations."
            },
        )

        self._print_summary(chat_result)
        output_file = self._save_results(chat_result)
        print(f"\nFull results saved to: {output_file}")
        print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

    def _print_summary(self, chat_result):
        """Print summary of architecture discussion"""
        print("\n" + "=" * 80)
        print("ARCHITECTURE DISCUSSION COMPLETE")
        print("=" * 80)
        print(f"\nTotal conversation rounds: {len(self.groupchat.messages)}")
        print("\nSpeaker order (as selected by GroupChatManager):")
        for i, msg in enumerate(self.groupchat.messages, 1):
            speaker = msg.get("name", "Unknown")
            content = msg.get("content", "")
            preview = content[:80].replace("\n", " ") + "..." if len(content) > 80 else content.replace("\n", " ")
            print(f"  {i}. [{speaker}]: {preview}")

        if chat_result.summary:
            print("\n" + "-" * 80)
            print("ARCHITECTURE SUMMARY (LLM-generated reflection)")
            print("-" * 80)
            print(chat_result.summary)

        print("\n" + "-" * 80)
        print("EXERCISE 4 NOTE: AutoGen vs CrewAI for Software Architecture")
        print("-" * 80)
        print("""
AutoGen's CONVERSATIONAL approach for software architecture:
- Agents freely debate trade-offs (e.g., microservices vs monolith)
- RequirementsAgent and DesignAgent can clarify ambiguities in real-time
- RiskAgent can challenge DesignAgent's specific choices directly
- GroupChatManager dynamically selects the most relevant speaker each turn
- Better for complex architectural decisions where back-and-forth is needed

CrewAI's TASK-BASED approach (see crewai_software_architecture.py):
- Each agent completes their phase without interruption
- Output from requirements feeds directly into design task context
- More predictable workflow but less opportunity for iterative refinement
- Better for well-understood domains where the workflow is clear upfront
""")

    def _save_results(self, chat_result):
        """Save architecture discussion and summary to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(output_dir, f"architecture_output_{timestamp}.txt")

        with open(output_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("AUTOGEN GROUPCHAT - SOFTWARE ARCHITECTURE DESIGN\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Model: {Config.OPENAI_MODEL}\n")
            f.write(f"Conversation Rounds: {len(self.groupchat.messages)}\n\n")

            f.write("=" * 80 + "\n")
            f.write("MULTI-AGENT CONVERSATION\n")
            f.write("=" * 80 + "\n\n")

            for i, msg in enumerate(self.groupchat.messages, 1):
                speaker = msg.get("name", "Unknown")
                content = msg.get("content", "")
                f.write(f"--- Turn {i}: {speaker} ---\n")
                f.write(content + "\n\n")

            if chat_result.summary:
                f.write("=" * 80 + "\n")
                f.write("ARCHITECTURE SUMMARY\n")
                f.write("=" * 80 + "\n")
                f.write(chat_result.summary + "\n")

        return output_file


if __name__ == "__main__":
    try:
        workflow = SoftwareArchitectureGroupChat()
        workflow.run()
        print("\nArchitecture GroupChat workflow completed successfully\!")
    except Exception as e:
        print(f"\nError during workflow execution: {str(e)}")
        import traceback
        traceback.print_exc()
