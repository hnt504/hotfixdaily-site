# Hotfix Daily: The Daily AI Builder Digest
<!-- title: Hotfix Daily #2: MiniMax M3.1 Flash, Claude Duet, Flint and more -->
<!-- description: Hotfix Daily #2: MiniMax M3.1 Flash pricing, Anthropic's Claude Duet agent, Recursive's local Flint coding model, AI at Steam Next Fest, and OPAL. -->
**Issue #2 · Thursday, Oct 22, 2026**

Five things from the last 48 hours worth your attention if you build with AI. No fluff.

[Read this issue on the web](https://hotfixdaily.com/issues/002/) · [Sponsor Hotfix Daily](https://hotfixdaily.com/sponsor/)

---

[MODEL]
**1. MiniMax ships M3.1 Flash at $0.15 per million input tokens**
MiniMax says its new Flash model runs agent tasks nearly 3x faster and about 70% cheaper than its predecessor, with a 1M-token context. Pricing is flat: $0.15 per million input tokens and $0.60 per million output. Weights are promised later.
*Why builders care:* If you tried the free `:free` variant on OpenRouter, it ends today at 12:00 UTC (7 AM CT). Switch to the base slug `minimax/minimax-m3.1-flash` so nothing breaks.
[source](https://www.minimax.io/blog/minimax-m31f)

[AGENTS]
**2. Anthropic previews Claude Duet, an agent that comes to you first**
Duet is a separate app (iOS, Android, claude.ai) that checks your connected apps every few hours, sends a morning brief, and keeps working on its own cloud computer after you close it. It asks for approval before it sends, pays, signs, or deletes anything. It's waitlist-only for US Pro and Max users.
*Why builders care:* Its background checks count against your plan's usage limits, which is a useful model for how to budget an always-on agent of your own.
[source](https://claude.com/resources/articles/claude-duet)

[CODING]
**3. Recursive's Flint: a coding model that runs on your laptop**
Flint is a 40B mixture-of-experts model that uses about 2.5B parameters per token. Recursive reports 74.2% on SWE-bench Verified and more than 125 tokens/sec on an M4 Pro MacBook Pro. It's Apache 2.0 on Hugging Face and works with Ollama, LM Studio, llama.cpp and vLLM.
*Why builders care:* A private, offline coding agent with no usage bill. Compare it with the hosted options in our [coding agent guide](https://hotfixdaily.com/guides/which-ai-coding-agent/).
[source](https://recursive.com/updates/introducing-recursive-flint)

[GAME DEV]
**4. More than a third of Steam Next Fest games now use generative AI**
TheGamer's count of SteamDB data found 2,595 of the 7,145 games in October's Next Fest (over 36%) carry Steam's AI tag, up from just over 19% in June. Players are pushing back, and many of the top-charting demos are AI-free.
*Why builders care:* Disclosed AI use is now normal on Steam, and players are watching. Being clear about how you used it can help you stand out.
[source](https://www.thegamer.com/steam-next-fest-ai-usage-has-jumped-from-one-in-five-to-one-in-three/)

[REPO]
**5. Repo of the day: OPAL, an optimizer an agent rewrites mid-training**
From MIT researchers: wrap your PyTorch optimizer in one line, and a coding agent (Claude Code by default) watches the run and rewrites the update rule, schedules, and loss-spike guards as it trains. MIT-licensed, with a cost cap you set.
*Why builders care:* For a new task with no tuned recipe, the authors report it matches or beats the best off-the-shelf recipe across their image and language tests.
[source](https://github.com/xingjian-bai/opal)

---

### Hotfix of the Day
Match reasoning effort to the step. On MiniMax-M3.1-Flash, `effort` defaults to `max` if you leave it out. Set it to `low` for routing, classification, and simple tool calls, and keep `high` or `max` for planning and debugging. Check what your provider defaults to.
[source](https://platform.minimax.io/docs/guides/text-generation)
