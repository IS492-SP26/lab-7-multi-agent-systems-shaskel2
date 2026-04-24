"""
CrewAI Multi-Agent Demo: Software Architecture Design
======================================================

EXERCISE 4: Custom Problem Domain

This demonstrates CrewAI's task-based orchestration applied to a NEW domain:
Software Architecture for a Cloud-Native E-Commerce Platform.

Four agents form a "crew" with sequentially executed tasks:
1. RequirementsAgent - Defines functional and non-functional requirements
2. ArchitectAgent    - Designs the system architecture and technology stack
3. RiskAgent         - Identifies technical risks and mitigation strategies
4. ArchReviewerAgent - Provides final assessment and implementation roadmap

Communication Style: Task-based (each agent completes their assigned task)

Compare with autogen_software_architecture.py which uses conversational GroupChat.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from crewai import Agent, Task, Crew
from crewai.tools import tool

sys.path.insert(0, str(Path(__file__).parent.parent))
from shared_config import Config, validate_config


# ============================================================================
# TOOLS
# ============================================================================

@tool
def analyze_system_requirements(system_description: str) -> str:
    """
    Analyze system requirements for a given application description.
    Returns structured functional and non-functional requirements.
    """
    requirements = {
        "e-commerce": {
            "functional": [
                "Product catalog with search, filtering, and recommendations",
                "Shopping cart with real-time price calculation",
                "Secure checkout with multiple payment methods (credit card, PayPal, crypto)",
                "Order management: create, track, cancel, return",
                "Inventory management with real-time stock updates",
                "User authentication: registration, login, profile management",
                "Seller portal for product listings and order fulfillment",
                "Review and rating system for products",
            ],
            "non_functional": [
                "Performance: < 200ms p95 latency for product search, < 500ms for checkout",
                "Scalability: Support 100,000 concurrent users, 10x spike during Black Friday",
                "Availability: 99.9% uptime (< 8.7 hours downtime/year), zero downtime deployments",
                "Security: PCI-DSS Level 1 compliance, OWASP Top 10 compliance, GDPR compliance",
                "Data durability: 99.999% (5 nines) for order and payment data",
                "Search response time: < 100ms for full-text product search",
                "Mobile-first: < 3s Time to Interactive on 3G networks",
            ],
            "constraints": [
                "6-month launch timeline for MVP",
                "12 full-stack engineers, 2 DevOps, 1 security engineer",
                "Budget: $500K/year cloud infrastructure",
                "Must integrate with existing ERP system via REST API",
                "Must support 15 currency types and international shipping",
            ]
        }
    }

    data = requirements.get("e-commerce", requirements["e-commerce"])

    output = f"Requirements Analysis: {system_description}\n"
    output += "=" * 60 + "\n"
    output += "\n--- Functional Requirements ---\n"
    for i, req in enumerate(data["functional"], 1):
        output += f"  F{i}. {req}\n"

    output += "\n--- Non-Functional Requirements (Quality Attributes) ---\n"
    for i, req in enumerate(data["non_functional"], 1):
        output += f"  NFR{i}. {req}\n"

    output += "\n--- Constraints ---\n"
    for i, c in enumerate(data["constraints"], 1):
        output += f"  C{i}. {c}\n"

    return output


@tool
def design_architecture(requirements: str) -> str:
    """
    Design a software architecture based on given requirements.
    Returns architecture decisions and technology stack recommendations.
    """
    architecture = {
        "pattern": "Microservices with Event-Driven Architecture",
        "hosting": "AWS (Primary), Multi-region deployment (us-east-1 + eu-west-1)",
        "services": [
            {"name": "API Gateway", "tech": "AWS API Gateway + Kong", "purpose": "Rate limiting, auth, routing"},
            {"name": "Product Service", "tech": "Node.js + PostgreSQL + Elasticsearch", "purpose": "Catalog, search, recommendations"},
            {"name": "Cart Service", "tech": "Go + Redis", "purpose": "Session-based cart, real-time price calc"},
            {"name": "Order Service", "tech": "Java/Spring Boot + PostgreSQL", "purpose": "Order lifecycle management"},
            {"name": "Payment Service", "tech": "Node.js + Stripe API (PCI scope isolation)", "purpose": "Secure payment processing"},
            {"name": "Inventory Service", "tech": "Go + PostgreSQL + Redis", "purpose": "Real-time stock tracking"},
            {"name": "User Service", "tech": "Node.js + PostgreSQL", "purpose": "Auth, profiles, OAuth2/JWT"},
            {"name": "Notification Service", "tech": "Python + AWS SES/SNS", "purpose": "Email, SMS, push notifications"},
        ],
        "data_stores": [
            "PostgreSQL (RDS Multi-AZ) — transactional data: orders, users, inventory",
            "Elasticsearch — product search with faceting and full-text",
            "Redis Cluster — sessions, cart, rate limiting, leaderboards",
            "S3 + CloudFront CDN — product images, static assets",
            "DynamoDB — session storage, real-time user activity",
        ],
        "infrastructure": [
            "Kubernetes (EKS) — container orchestration, auto-scaling",
            "Apache Kafka — async messaging between services (order events, inventory updates)",
            "Istio service mesh — service discovery, mTLS, circuit breakers",
            "Terraform + Helm — infrastructure as code",
            "GitHub Actions + ArgoCD — CI/CD pipeline (GitOps)",
            "Datadog — monitoring, APM, logging, alerting",
        ]
    }

    output = "Architecture Design: Cloud-Native E-Commerce Platform\n"
    output += "=" * 60 + "\n"
    output += f"\nPattern: {architecture['pattern']}\n"
    output += f"Hosting: {architecture['hosting']}\n"

    output += "\n--- Microservices ---\n"
    for svc in architecture["services"]:
        output += f"  • {svc['name']}: {svc['tech']}\n"
        output += f"    Purpose: {svc['purpose']}\n"

    output += "\n--- Data Stores ---\n"
    for ds in architecture["data_stores"]:
        output += f"  • {ds}\n"

    output += "\n--- Infrastructure & DevOps ---\n"
    for inf in architecture["infrastructure"]:
        output += f"  • {inf}\n"

    return output


@tool
def assess_technical_risks(architecture: str) -> str:
    """
    Assess technical risks in a proposed software architecture.
    Returns risk analysis with probability, impact, and mitigations.
    """
    risks = [
        {
            "name": "Distributed Transactions & Data Consistency",
            "probability": "High",
            "impact": "Critical",
            "description": "Microservices with separate databases make ACID transactions across services impossible. Order + inventory update must be atomic.",
            "mitigation": "Implement Saga pattern (choreography-based) for distributed transactions. Use event sourcing for order state changes. Implement idempotent APIs. Use compensating transactions for rollback."
        },
        {
            "name": "Cascading Service Failures",
            "probability": "Medium",
            "impact": "High",
            "description": "A failure in one service (e.g., Payment Service) can cascade to bring down dependent services.",
            "mitigation": "Implement circuit breakers via Istio. Define timeouts and retry policies for all inter-service calls. Use bulkhead pattern to isolate failure domains. Test with chaos engineering (Chaos Monkey)."
        },
        {
            "name": "PCI-DSS Compliance Scope Creep",
            "probability": "Medium",
            "impact": "Critical",
            "description": "If payment card data touches multiple services, PCI compliance scope expands dramatically, increasing audit cost and risk.",
            "mitigation": "Isolate Payment Service in a dedicated network segment. Use Stripe.js/tokenization to prevent card data ever hitting our servers. Regular penetration testing. Engage a QSA (Qualified Security Assessor) early."
        },
        {
            "name": "Black Friday Traffic Spikes (10x Load)",
            "probability": "Certain",
            "impact": "High",
            "description": "10x traffic spike with 100k concurrent users can overwhelm auto-scaling if not properly tested and tuned.",
            "mitigation": "Conduct load testing with k6/Locust before launch. Pre-scale 2x capacity before peak events. Implement queue-based load leveling for non-critical paths. Use read replicas and caching aggressively."
        },
        {
            "name": "Operational Complexity / Team Skill Gap",
            "probability": "High",
            "impact": "Medium",
            "description": "Kubernetes + Kafka + Istio + microservices is a steep learning curve for a 12-engineer team in 6 months.",
            "mitigation": "Start with a hybrid approach: modular monolith for MVP, extract services iteratively. Use managed services (RDS, ElastiCache, MSK) to reduce ops burden. Invest in Kubernetes training for 2+ engineers from day 1."
        },
    ]

    output = "Technical Risk Assessment: Cloud-Native E-Commerce Platform\n"
    output += "=" * 60 + "\n"

    for i, risk in enumerate(risks, 1):
        output += f"\nRisk {i}: {risk['name']}\n"
        output += f"  Probability: {risk['probability']} | Impact: {risk['impact']}\n"
        output += f"  Description: {risk['description']}\n"
        output += f"  Mitigation: {risk['mitigation']}\n"

    return output


# ============================================================================
# AGENT DEFINITIONS
# ============================================================================

def create_requirements_agent():
    """Create the Requirements Analyst agent."""
    return Agent(
        role="Requirements Analyst",
        goal="Define comprehensive functional and non-functional requirements for the cloud-native "
             "e-commerce platform, ensuring all quality attributes and constraints are captured.",
        backstory="You are a senior business analyst and systems architect with 10+ years experience "
                  "defining requirements for large-scale e-commerce platforms. You've worked with "
                  "companies like Amazon, Shopify, and Stripe defining system requirements. You know "
                  "that poorly defined NFRs are the #1 cause of architecture failures.",
        tools=[analyze_system_requirements],
        verbose=True,
        allow_delegation=False
    )


def create_architect_agent():
    """Create the Software Architect agent."""
    return Agent(
        role="Principal Software Architect",
        goal="Design a scalable, secure, and maintainable cloud-native architecture that meets "
             "all stated requirements within the team's constraints.",
        backstory="You are a principal software architect with deep expertise in distributed systems, "
                  "cloud-native architecture, and microservices. You've designed systems that handle "
                  "millions of transactions per day. You favor pragmatic solutions over theoretical "
                  "perfection, and always consider team capabilities when proposing architecture.",
        tools=[design_architecture],
        verbose=True,
        allow_delegation=False
    )


def create_risk_agent():
    """Create the Risk Assessment engineer agent."""
    return Agent(
        role="Senior SRE / Risk Engineer",
        goal="Identify and quantify technical risks in the proposed architecture, providing "
             "concrete mitigation strategies to ensure system reliability and security.",
        backstory="You are a senior Site Reliability Engineer with a background in security and "
                  "distributed systems. You've led post-mortems for major outages at tech companies "
                  "and know exactly where cloud-native architectures typically fail. You think in "
                  "failure modes: what could go wrong, how likely, and how to prevent it.",
        tools=[assess_technical_risks],
        verbose=True,
        allow_delegation=False
    )


def create_arch_reviewer_agent():
    """Create the Architecture Review Board agent."""
    return Agent(
        role="VP of Engineering / Architecture Reviewer",
        goal="Provide an authoritative final assessment of the proposed architecture, validating "
             "it against requirements, risk profile, and team capabilities. Produce a clear "
             "implementation roadmap and go/no-go recommendation.",
        backstory="You are a VP of Engineering who chairs the architecture review board. You have "
                  "approved and rejected dozens of architecture proposals. You evaluate designs holistically: "
                  "technical soundness, risk profile, team fit, cost, and long-term maintainability. "
                  "Your recommendations are evidence-based and actionable.",
        tools=[],  # Reviewer synthesizes rather than researching
        verbose=True,
        allow_delegation=False
    )


# ============================================================================
# TASK DEFINITIONS
# ============================================================================

def create_requirements_task(requirements_agent):
    return Task(
        description="Analyze the requirements for a cloud-native e-commerce platform. "
                   "Use the analyze_system_requirements tool to get structured requirements. "
                   "Then present a comprehensive requirements document covering: "
                   "(1) 5-8 functional requirements, "
                   "(2) non-functional requirements (performance, scalability, availability, security), "
                   "(3) key constraints (timeline, team size, budget). "
                   "Prioritize requirements as Must-Have vs Nice-to-Have.",
        agent=requirements_agent,
        expected_output="A structured requirements document with functional requirements, "
                       "non-functional requirements with measurable targets, and key constraints. "
                       "Requirements should be specific and testable."
    )


def create_architecture_task(architect_agent):
    return Task(
        description="Based on the requirements from the RequirementsAgent, design a complete "
                   "software architecture for the cloud-native e-commerce platform. "
                   "Use the design_architecture tool to get architecture patterns and tech stack. "
                   "Your architecture document must cover: "
                   "(1) Architectural pattern choice (microservices, monolith, etc.) with justification, "
                   "(2) Key services and their responsibilities, "
                   "(3) Data storage strategy (which databases for which data), "
                   "(4) Technology stack with specific versions/services, "
                   "(5) How each key requirement is addressed. "
                   "Reference specific requirements from the RequirementsAgent.",
        agent=architect_agent,
        expected_output="A detailed architecture design document with architectural pattern, "
                       "service decomposition, technology stack, data strategy, "
                       "and explicit mapping of architecture decisions to requirements."
    )


def create_risk_assessment_task(risk_agent):
    return Task(
        description="Assess the technical risks in the proposed architecture. "
                   "Use the assess_technical_risks tool to identify key risks. "
                   "For each of the top 4-5 risks, provide: "
                   "(1) Risk description and why it matters for this specific architecture, "
                   "(2) Probability (High/Medium/Low) and Impact (Critical/High/Medium), "
                   "(3) Concrete mitigation strategy with specific tools/patterns, "
                   "(4) Residual risk after mitigation. "
                   "Reference specific architectural decisions from the ArchitectAgent.",
        agent=risk_agent,
        expected_output="A risk register with 4-5 identified risks, each with probability/impact rating, "
                       "description, and actionable mitigation strategy tied to the specific architecture."
    )


def create_arch_review_task(arch_reviewer_agent):
    return Task(
        description="Review the complete architecture proposal (requirements + design + risk assessment) "
                   "and provide a final architecture board decision. Your review must cover: "
                   "(1) Assessment of whether architecture meets stated requirements, "
                   "(2) Evaluation of risk mitigation adequacy, "
                   "(3) 3-4 specific recommendations to improve the design, "
                   "(4) Implementation roadmap: Phase 1 (MVP, months 1-3), "
                   "Phase 2 (core features, months 4-6), Phase 3 (scale & optimize, months 7-12), "
                   "(5) Go / Conditional Go / No-Go decision with clear conditions. "
                   "Be specific — cite requirements, design choices, and risks from earlier agents.",
        agent=arch_reviewer_agent,
        expected_output="An architecture review decision with requirements assessment, risk evaluation, "
                       "specific recommendations, phased implementation roadmap, "
                       "and a clear Go/No-Go decision with conditions."
    )


# ============================================================================
# CREW ORCHESTRATION
# ============================================================================

def main():
    """Main function to orchestrate the software architecture crew."""

    print("=" * 80)
    print("CrewAI Multi-Agent Software Architecture Design System")
    print("Cloud-Native E-Commerce Platform")
    print("=" * 80)
    print()
    print("Domain: Software Architecture (EXERCISE 4 - Custom Problem Domain)")
    print("Task: Design cloud-native architecture for e-commerce platform")
    print("Team: 12 engineers | Timeline: 6 months | Scale: 100k concurrent users")
    print()

    if not validate_config():
        print("❌ Configuration validation failed.")
        exit(1)

    os.environ["OPENAI_API_KEY"] = Config.API_KEY
    os.environ["OPENAI_API_BASE"] = Config.API_BASE

    print("✅ Configuration validated\!")
    print()

    print("[1/4] Creating Requirements Analyst Agent...")
    requirements_agent = create_requirements_agent()

    print("[2/4] Creating Principal Architect Agent...")
    architect_agent = create_architect_agent()

    print("[3/4] Creating SRE Risk Engineer Agent...")
    risk_agent = create_risk_agent()

    print("[4/4] Creating Architecture Review Board Agent...")
    arch_reviewer_agent = create_arch_reviewer_agent()

    print("\n✅ All agents created\!")
    print()

    print("Creating architecture design tasks...")
    requirements_task = create_requirements_task(requirements_agent)
    architecture_task = create_architecture_task(architect_agent)
    risk_task = create_risk_assessment_task(risk_agent)
    review_task = create_arch_review_task(arch_reviewer_agent)

    print("Forming Architecture Design Crew...")
    print("Task Sequence: RequirementsAgent → ArchitectAgent → RiskAgent → ArchReviewerAgent")
    print()

    crew = Crew(
        agents=[requirements_agent, architect_agent, risk_agent, arch_reviewer_agent],
        tasks=[requirements_task, architecture_task, risk_task, review_task],
        verbose=True,
        process="sequential"
    )

    print("=" * 80)
    print("Starting Software Architecture Crew Execution...")
    print("=" * 80)
    print()

    try:
        result = crew.kickoff()

        print()
        print("=" * 80)
        print("✅ Software Architecture Design Complete\!")
        print("=" * 80)
        print()
        print("FINAL ARCHITECTURE REPORT:")
        print("-" * 80)
        print(result)
        print("-" * 80)

        output_path = Path(__file__).parent / "crewai_software_architecture_output.txt"
        with open(output_path, "w") as f:
            f.write("=" * 80 + "\n")
            f.write("CrewAI Software Architecture Design - Execution Report\n")
            f.write("Cloud-Native E-Commerce Platform\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Execution Time: {datetime.now()}\n")
            f.write("Exercise 4: Custom Problem Domain\n\n")
            f.write("FINAL ARCHITECTURE REPORT:\n")
            f.write("-" * 80 + "\n")
            f.write(str(result))
            f.write("\n" + "-" * 80 + "\n")

        print(f"\n✅ Output saved to crewai_software_architecture_output.txt")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
