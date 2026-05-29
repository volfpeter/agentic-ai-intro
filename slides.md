---
theme: seriph
colorSchema: auto
class: text-left
highlighter: shiki
lineNumbers: true
title: Introduction to Agentic AI
---

# Agentic AI

Getting started

---

# About me

Peter Volf

What I do:

- Senior engineer at Collmot Robotics Ltd. (https://collmot.com/)
- Contracting: Python and web development, mentoring
- Open source: mostly on my own projects, related to FastAPI and HTMX

Find me at:

- GitHub: https://github.com/volfpeter
- Mastodon: https://mastodon.social/@volfpeter
- Twitter/X: https://x.com/volfpeter

---
layout: section
---

# From chat to agents

---
layout: two-cols-header
---

# From chat to agents

::left::

_Traditional AI (chat):_

- Model: one _prompt_ → one _response_
- No concept of an environment
- No autonomy

<br>

_Agentic AI:_

Model and environment, connected by a _harness_:

- Context initialization and management
- Iterative loop: think → interact → observe
- Interact with _tools_ (read, write, bash, ask)

::right::

```python
def run_agent(task, tools, model):
    context = [
        SystemPrompt(model),
        Description(tools),
        UserMessage(task),
    ]

    while not should_terminate(context):
        # Think
        response = model.generate(context)
        context.append(response.message)

        if response.is_final_answer:
            break

        # Interact with environment
        observation = tools.execute(
            response.tool_calls
        )

        # Observe
        context.append(observation.describe())
```

---
layout: two-cols-header
---

# From chat to agents - workflow comparison

::left::

_Chat workflow:_

1. Copy code into chat, "Fix this for me"
2. Copy response back to codebase
3. Run → error
4. Copy error into chat, "Fix this for me"
5. Copy response back to codebase
6. Run → error
7. …repeat until done

::right::

_Agent workflow:_

1. "I have this issue in this file"
2. **Loop:** study input, activate tools, check result
3. **Loop:** study result, decide necessary changes, request edits
4. **Loop:** study edit result, request execution
5. **Loop:** study execution output, decide next step, act if not done

---

# From chat to agents - takeaways

- The model sees the environment through the context: _context engineering_ is key
- The agent loop replaces the human between the model and the environment
- _Project environment_ is important: typing, linters, tests, documentation, ...
- The _harness_ can be customized: _AGENTS.md_, _skills_, _system prompt_, ...
- Asking the user can be a tool for the agent, instruct the model to use it
- The loop continues until the model believes its goal is met

---
layout: two-cols-header
---

# Harness customization

Guidance, memory, convenience, extension

Think of it like software, keep it minimal and improve iteratively

::left::

<p style="opacity: 1"><code>AGENTS.md</code>:</p>

- General guidance and instructions
- Prevent common failure modes

_Commands:_

- Reusable prompts
- Triggered by the user
- Implemented as skills in some harnesses

::right::

_Skills:_

- Reusable instructions, scripts, resources
- Requested by user or agent

_Agent configuration:_

- System prompt
- Model configuration, e.g. temperature

_MCP:_

- Extra tools and resources

---
layout: section
---

# Landscape

Labs, models, and trade-offs

---

# Model landscape - proprietary

- OpenAI: GPT, GPT mini, GPT nano
- Anthropic: Claude Opus, Sonnet, and Haiku
- Google: Gemini Pro, Flash, Flash Light
- (xAI: Grok 4.3, 4.1 fast)

The best and most expensive models.

Usually available with subscription and token/API pricing directly from the lab.

Subscription may not work in all agent harnesses.

---

# Model landscape - open weight

- Moonshot AI: Kimi k2.6
- DeepSeek: DeepSeek v4 Pro and v4 Flash
- Z.AI: GLM 5.1
- Xiaomi: Mimo v2.5 Pro and v2.5 Flash
- Alibaba: Qwen 3.7 Max
- Minimax: Minimax m2.5 and m2.7

Close to proprietary models (at least for coding) with far better pricing.

Available from inference providers with subscription or token/API pricing.

Subscription can be used in all harnesses.

Can't be run on consumer hardware.

---

# Model landscape - local

- Alibaba: Qwen 3.6 (27B)
- Google: Gemma 4 (31B, 26B)
- Nvidia: Nemotron 3 Super
- Mistral: Mistral Small 4, Mistral Medium 3.5
- OpenAI: GPT OSS 120B and 20B
- ...

Less capable than hosted models, but can be competitive in some tasks.

Can run on consumer hardware locally.

They work in all harnesses.

Private, can be fine-tuned for specific tasks.

---

# Costs, privacy, and security

<p style="opacity: 1"><em>Costs:</em></p>

- API pricing (per million tokens): input, output, and cache read
- Agentic AI is token-hungry; cache read is often the dominant factor
- Subscriptions are heavily subsidised vs. API pricing, >10-20x

_Privacy:_

- Free models: provider likely keeps and uses your data
- Zero data retention: inference providers may promise not to keep data
- Codebase reconstruction: feasible but unlikely, value is in human feedback for RL

_Security:_

- Trust but verify: agents can be confidently wrong
- Tool misuse: malicious skills, broad tool access and permissions, data leaks via tool calls
- Prompt injection: data and instructions are indistinguishable, data can contain hidden motives

---
layout: two-cols-header
---

# Hype versus reality

Every coin has two sides

::left::

Productivity gains:

- 0 to 1, for example personal software
- 10-100x??? Real value: exploration, prototyping, second opinion, review
- ~1x, but better quality or less mental effort

::right::

Trade-offs:

- Cognitive debt
- No upskilling, downskilling / skill atrophy
- Technical debt and complexity

---

# Model landscape - overview

<img src="/intelligence-vs-cost.png" style="border-radius: 4px;">

<p style="opacity: 0.5; text-align: end;"><a href="https://artificialanalysis.ai/">https://artificialanalysis.ai/</a></p>

---
layout: two-cols-header
---

# Model landscape - resources

::left::

_Resources:_

- Artificial Analysis: https://artificialanalysis.ai
- Hugging Face: https://huggingface.co
- Unsloth: https://unsloth.ai
- Arena/LMArena: https://huggingface.co/spaces/lmarena-ai/arena-leaderboard, https://arena.ai

::right::

_Inference providers/routers:_

- OpenCode Zen/Go: https://opencode.ai/zen
- OpenRouter: https://openrouter.ai
- GitHub Copilot: https://github.com/features/copilot

---
layout: section
---

# AI tools

---
layout: two-cols-header
---

# AI tools

Cambrian explosion

::left::

_Agent-first tools:_

- OpenCode: https://opencode.ai
- Pi: https://pi.dev
- Claude Code, Codex, Antigravity...
- Aider: https://aider.chat
- Warp: https://www.warp.dev
- T3Code: https://t3.codes

_Assistants ("claws"):_

- OpenClaw: https://openclaw.ai
- Countless copycats

::right::

_IDEs with agent features:_

- Zed: https://zed.dev
- VS Code and forks (Cursor)
- Your favorite editor + agent extensions

_Research synthesis:_

- NotebookLM: https://notebooklm.google

_For non-coders:_

- Claude Cowork: https://claude.com/product/cowork
- OpenWork: https://openworklabs.com
- Open WebUI: https://openwebui.com

---

# AI tools - local inference

<p style="opacity: 1"><em>Running models locally:</em></p>

- Llama.cpp: https://github.com/ggml-org/llama.cpp
- LM Studio: https://lmstudio.ai
- Ollama: https://ollama.com
- vLLM: https://vllm.ai

Community: https://www.reddit.com/r/LocalLLaMA

_Llama.cpp quickstart:_

```sh {lines:false}
$ brew install llama.cpp
$ llama-cli -hf unsloth/gemma-4-26B-A4B-it-GGUF
> hello
"Hello! How can I help you today?"

$ llama-server -hf unsloth/gemma-4-26B-A4B-it-GGUF --port 9090
```

---

# AI tools - agent development

LangChain, PydanticAI, transformers, CrewAI, Smoleagents, ...

_PydanticAI quickstart:_

```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIChatModel(
    model_name="unsloth/gemma-4-26B-A4B-it-GGUF",
    provider=OpenAIProvider("http://127.0.0.1:9090/v1"),
)

agent = Agent(model, instructions="Always respond with a haiku.")

result = agent.run_sync("What is agentic AI?")
print(result.output)
```

---
layout: section
---

# Practice

---
layout: two-cols-header
---

# Before you start

::left::

_Tips:_

- Always use version control
- Start with a vanilla harness
- Start with simple, scoped tasks
- Instruct the agent to ask questions
- Save your prompts
- Read the agent's output
- Review every change
- Question the agent's thinking
- Explain how the result will be evaluated

::right::

_Every interaction gives feedback on:_

- The model's capabilities
- The model's limits and failure modes
- How well your project is set up for agents
- Your prompts

---
layout: two-cols-header
---

# Preparation - OpenCode

Terminal UI + web application + desktop application

::left::

_Install:_

- Homebrew: `brew install anomalyco/tap/opencode`
- curl: `curl -fsSL https://opencode.ai/install | bash`
- npm: `npm i -g opencode-ai`
- Other: https://opencode.ai

Start from terminal: `opencode`

Free model: `DeepSeek V4 Flash Free`

::right::

_Cheat sheet_:

- `/model`: select model
- `/sessions`, `/new`: manage sessions
- `@<resource>`: reference resource
- `/<command>`: use command
- `/<skill>` or prompt: use skill
- `/connect`: connect to inference provider
- _Tab_: switch agent
- _CTRL + P_: command palette
- _CTRL + J_: line break :)

---

# Preparation - practice repo

Slides, practice problems, and example configuration

- Clone: `git clone git@github.com:volfpeter/agentic-ai-intro.git`
- Download: https://github.com/volfpeter/agentic-ai-intro/archive/refs/heads/main.zip

_`practice/` folder:_

- Pre-configured Python environment (using `uv`)
- `AGENTS.md`: General agent instructions
- `.agents/`: Example skills
- `.opencode/`: OpenCode config (commands, local provider config, custom agents)
- `challenges/`: Coding challenges
- `projects/`: Project ideas for experimentation
- `arxiv-md/`: Implementation milestones of the `arxiv-markdown-download.md` project

---

# Communication patterns

<p style="opacity: 1"><em>Ask, don't instruct:</em></p>

- Instead of "Do this ..." ask "How would you do this ..."
- The agent articulates the problem and the possible solutions
- Opportunity for correction and learning

_Self-analysis:_

- Why do you think that?
- Where did you find this information?
- What led you to that decision?
- What would make you change your mind?
- Why not use a simpler, more standard approach?

---

# Prompting techniques

<p style="opacity: 1"><em>Prompt inversion:</em></p>

- Before acting: ask the agent to draft a better prompt
- After failure: ask what prompt would have worked better

_Declarative prompting (`/declarative`):_

- State your goal and success criteria, not the solution
- Let the agent decide the approach

_Summarize (`/checkpoint`):_

- Produce a self-contained prompt for a new session
- Start fresh with clean, informative context

---

# Learning - agent

Iterative agent and project improvement

_Reflection (`/learn`):_

- Reflect on user corrections
- Propose `AGENTS.md` or skill updates

_Session analysis (`/what-went-wrong`):_

- Why wasn't this session more efficient?
- What did you miss?
- What misled you?

---

# Learning - user

Learn what you don't want to outsource

_Ask for explanation (`/explain`, `/review`):_

- Explain concepts, patterns, terminology
- Provide pointers and topics for learning
- Does it need to be this complicated?

_Special agents (`teacher`):_

- Explain, review, guide when stuck
- Do not solve the problem
- Assess the user's understanding through questions

---

# Pseudocode

Not just for algorithms

Define agent workflow with pseudocode:

```
list steps in task, ask to execute
for step in task:
    if ambiguous: ask
    implement
    briefly explain
    request review
    mark as done after approval
```

Confirm understanding and reinforce intent in context:

> "Do you understand? Don't implement."

---

# Complex tasks

Not spec-driven development

_Discuss (chat or `/grill-me`):_

- Reach shared understanding of the problem
- Identify potential solutions

_Prototype or plan:_

- Prototype for better understanding
- Create implementation plan if necessary (`/to-plan`)

_Execute (prompt or `/to-tasks` + `/do-tasks`):_

- Execute directly if task is small enough
- Break into subtasks, execute and review one by one

---

# Resources

<p style="opacity: 1"><em>Reading:</em></p>

- Agentic Coding is a Trap: https://larsfaye.com/articles/agentic-coding-is-a-trap

_Skills:_

- https://github.com/hunvreus/skill-issue
- https://github.com/mitsuhiko/agent-stuff
- https://github.com/multica-ai/andrej-karpathy-skills
- https://github.com/mattpocock/skills
- https://github.com/anthropics/skills

---
layout: two-cols-header
---

# How to keep up

::left::

Twitter/X:

- Andrej Karpathy, @karpathy
- Mitchell Hashimoto, @mitchellh
- Dax Raad, @thdxr
- Armin Ronacher, @mitsuhiko
- Ronan Berder, @hunvreus
- David Heinemeier Hansson, @dhh
- Mario Zechner, @badlogicgames
- Simon Willison, @simonw
- Demis Hassabis, @demishassabis
- Matt Pocock, @mattpocockuk
- Peter Steinberger, @steipete

::right::

YouTube, podcast:

- Lex Fridman Podcast: https://lexfridman.com/podcast
- Dwarkesh Podcast: https://www.dwarkesh.com/podcast
- AI Explained, YT: @aiexplained-official
- Theo Browne, YT: @t3dotgg
- Michael Paulson, YT: @ThePrimeTimeagen

---

<p style="text-align: center;">Thanks for your patience</p>

<img src="/karpathy-microgpt.jpg" style="border-radius: 4px; height: 75%; margin: auto;">

<p style="opacity: 0.5; text-align: end;"><a href="https://x.com/karpathy/status/2021862247568642485">https://x.com/karpathy/status/2021862247568642485</a></p>
