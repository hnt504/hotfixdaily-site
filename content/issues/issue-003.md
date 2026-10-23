# Hotfix Daily: The Daily AI Builder Digest
<!-- title: Hotfix Daily #3: Agent Skills goes neutral, Canva Craft, Coding Agent Index v2.0 and more -->
<!-- description: Hotfix Daily #3: Anthropic donates Agent Skills to the Agentic AI Foundation, Canva's Craft image model hits the API, Coding Agent Index v2.0, Epic's AI MegaJam, and Base Labs' decision models. -->
**Issue #3 · Friday, Oct 23, 2026**

Five things from the last 48 hours worth your attention if you build with AI. No fluff.

[Read this issue on the web](https://hotfixdaily.com/issues/003/) · [Sponsor Hotfix Daily](https://hotfixdaily.com/sponsor/)

---

[AGENTS]
**1. Anthropic hands Agent Skills to the Agentic AI Foundation**
The SKILL.md folder format now lives at the Linux Foundation's AAIF, next to MCP and AGENTS.md, with maintainers from Anthropic, Google, OpenAI and others. Anthropic says more than 70 agent platforms support it, with 1 million skills published and nearly 280 million installs. The proposed roadmap covers versioned releases, a formal proposal process and security guidance.
*Why builders care:* Skills you write once should keep working across Claude Code, Cursor, Copilot and the rest, with no single vendor steering the spec.
[source](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation)

[MODEL]
**2. Canva ships Craft, its first in-house image model**
Craft plans the layout and text first, then renders at up to 2K in more than 30 aspect ratios. It's live for all Canva users and in the API as `craft_v1_2k`, with text in 55 languages.
*Why builders care:* It's built for posters, infographics and social graphics with readable text. Jobs take roughly 50 to 60 seconds, so poll with backoff.
[source](https://community.canva.dev/t/connect-api-canva-craft-is-now-available-for-image-generation/8999)

[CODING]
**3. Artificial Analysis resets its Coding Agent Index**
Version 2.0 scores model-plus-harness pairs on 290 tasks, swapping in Cognition's FrontierCode, which grades whether a maintainer would merge the change. Claude Opus 5.5 in Claude Code leads at 61.7. Scores fell for 20 of 21 setups tested on both versions, with the mean dropping from 54.8 to 47.4.
*Why builders care:* Don't compare v2.0 numbers with older charts. Check the per-benchmark and cost-per-task columns for your kind of work.
[source](https://x.com/ArtificialAnlys/status/2113424551396934134)

[GAME DEV]
**4. Epic announces the AI MegaJam, with grants up to $50,000**
From November 12 to 15, teams of up to five build an Unreal Engine or UEFN game with as many AI agents as they like. There's $65,000 in cash prizes plus continuation grants. Epic first said AI was required, then walked that back: AI is optional.
*Why builders care:* Epic's tip is to get your agents and Unreal MCP working before kickoff, since setup on day one eats build time.
[source](https://itch.io/jam/2026-epic-ai-megajam)

[REPO]
**5. Repo of the day: Base Labs' open decision models**
Mammoth-1 (27B) and Elephant-1 (9B) take a state plus a set of questions and return a calibrated probability for every option in one pass, with no text to parse. Mammoth-1 ranks first of 208 models on the Jev Decision Index 0.4. Weights are on Hugging Face, and Elephant-1 is free on Baseten's API until Oct 27.
*Why builders care:* Routing, spam checks and yes/no gates get faster and cheaper than calling a full reasoning model.
[source](https://huggingface.co/baselabs/mammoth-1)

---

### Hotfix of the Day
Write skill descriptions for the agent, not for people. Agents load only each skill's `name` and `description` at startup and open the full SKILL.md when a task matches, so say what the skill does, when to use it, and the keywords a request would contain. "Helps with PDFs" won't get picked.
[source](https://agentskills.io/specification)
