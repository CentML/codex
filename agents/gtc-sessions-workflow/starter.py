"""Script to run the GTC session filtering workflow using Temporal.io."""
import asyncio
import json
import os
import sys

from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter

from activities import Session, Prompt
from workflows import TopTenGTCSessionsWorkflow, TopTenGTCSessionsWorkflowInput

# Prompts used for session evaluation
FILTER_SYSTEM_PROMPT = """You are an expert at evaluating AI/ML conference sessions, specifically focusing on identifying sessions that discuss optimizations of AI/ML systems themselves."""

FILTER_USER_PROMPT_TEMPLATE = """Analyze the following GTC session title and abstract. Determine if it meets MANY of the following criteria for inclusion:

**Core Focus**: The session must explicitly address technical methods for optimizing the computational efficiency of AI/ML systems themselves. This includes:
- Reducing computational costs (e.g., energy, hardware, cloud expenses) of AI/ML models or training processes.
- Improving efficiency (e.g., faster training, optimized inference, reduced latency, smaller models).
- Techniques such as quantization, pruning, sparsity, distillation, parallelization, or novel architectures aimed at making AI/ML systems more efficient.

**Important**: The session must focus on improving the AI/ML techniques or systems, not on applying AI/ML to optimize other domains or processes.

**Technical Depth**: The session should:
- Mention frameworks/libraries (e.g., TensorFlow, PyTorch, CUDA) or tools (e.g., Triton, TensorRT) used in the optimization process.
- Describe algorithms, workflows, or provide measurable results (e.g., '40% fewer FLOPs,' '2x speedup on A100') related to AI/ML system optimization.
- Avoid vague claims (e.g., 'revolutionary,' 'industry-leading') without technical justification.

**Exclusion Rules**: Reject sessions that:
- Avoid workshop sessions, ie those that include 'Learn how to'
- Avoid session that Focus on applying AI/ML to optimize other domains or processes, rather than optimizing the AI/ML systems themselves.
- Avoid sessions that are product demos, company announcements, or partnerships without technical detail on AI/ML optimization.
- Use excessive marketing language (e.g., 'transform your business,' 'exclusive solution').
- Lack concrete methodologies for AI/ML optimization (e.g., only high-level use cases, no benchmarks).

**Examples**:
**Included**:
Title: 'Dynamic Sparsity for Efficient Transformer Training'
Abstract: 'We present a PyTorch-based method to dynamically prune attention heads during training, reducing memory usage by 35% on GPT-3-scale models without accuracy loss.'
→ Rationale: Focuses on optimizing an AI/ML system (transformer training) with technical details (pruning, PyTorch, 35% memory reduction).

**Excluded**:
Title: 'Using AI to Optimize Energy Consumption in Data Centers'
Abstract: 'Learn how our AI-powered platform can reduce energy costs by predicting and optimizing data center cooling systems.'
→ Rationale: Focuses on applying AI to optimize data center energy use, not on optimizing the AI system itself.

**Another Excluded**:
Title: 'Accelerate AI with XYZ Corporation's Cloud Platform'
Abstract: 'Discover how our industry-leading platform empowers teams to deploy models faster and cut costs!'
→ Rationale: Lacks technical details on AI/ML optimization methods; uses promotional language.

**Session to Evaluate**:
Title: ```{title}```
Abstract: ```{abstract}```
Based on the criteria above, should this session be included? Provide a brief justification."""

COMPARE_SYSTEM_PROMPT = """You are an expert at comparing GTC conference sessions given their titles and abstracts."""

COMPARE_USER_PROMPT_TEMPLATE = """You will analyze Titles & Abstracts of two GTC sessions (A and B) to determine which better emphasizes an academic discussions of techniques that lead to cost reduction and/or improved time/resource efficiency in AI/ML workflows, deployments, or applications.
Prioritize abstacts that include evidence of concrete benefits over superficial buzz.

Template for Analysis
Step-by-Step Instructions:

Analyze Criteria for Section A - Assign scores ((1-5): Cost/Efficiency Emphasis | Avoidance of Self-Promotion | Accessibility Generality | Supported Claims.

Analyze Criteria for Section B - Same framework.
(Compare relative strengths for each criteria).

Make Final Call. Consider:

• It must be related to AI/ML systems engineering, no using AI/ML to solve some problems such as autonomous driving, or cancer etc.
• Does A/B discuss actual financial metrics (e.g., 20%↑ inference speed) rather than ROI hype?
• If A focuses on custom ASIC chip design & B improves PyTorch pipeline design → B has wider ML impact.

VERDICT Format → {{-1 if A>B, 1 if B>=A}}: {{Return only "-1" or "1" without explanation.}}

Sessions Provided: 
Title for paper a: ```{title_a}```
Abstract for paper a: ```{abstract_a}```
Title for paper b: ```{title_b}```
Abstract for paper b: ```{abstract_b}```"""


CENTML_API_KEY = os.getenv("CENTML_API_KEY") or ""
if not CENTML_API_KEY:
    print("Error: CENTML_API_KEY environment variable not set")
    sys.exit(1)

async def main():
    """Execute the GTC session filtering workflow to find top AI/ML system optimization talks."""
    # Connect to the Temporal server
    client = await Client.connect("localhost:7233", data_converter=pydantic_data_converter)

    filter_prompt = Prompt(
        system_prompt=FILTER_SYSTEM_PROMPT,
        user_prompt_template=FILTER_USER_PROMPT_TEMPLATE,
        #model="deepseek-ai/DeepSeek-R1"
        model="centml/DeepSeek-R1-Slim-INT4"
    )
    
    compare_prompt = Prompt(
        system_prompt=COMPARE_SYSTEM_PROMPT,
        user_prompt_template=COMPARE_USER_PROMPT_TEMPLATE, 
        model="deepseek-ai/DeepSeek-R1"
        #model="centml/DeepSeek-R1-Slim-INT4"
    )

    # Run the workflow and get the result
    try:
        result: list[Session] = await client.execute_workflow(
            TopTenGTCSessionsWorkflow.run,
            TopTenGTCSessionsWorkflowInput(
                api_key=CENTML_API_KEY,
                filter_prompt=filter_prompt,
                compare_prompt=compare_prompt
            ),
            id="fetch-sessions-workflow-id",
            task_queue="fetch-sessions-queue"
        )

        print(json.dumps([session.model_dump() for session in result]))  # Print the list of sessions

    except Exception as e:  # pylint: disable=broad-except
        print(f"Error running workflow: {e}")

if __name__ == "__main__":
    asyncio.run(main())