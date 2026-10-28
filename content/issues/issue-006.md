# Hotfix Daily: The Daily AI Builder Digest
<!-- title: Hotfix Daily #6: Liquid's LFM3, Genie 4, Entire's Trails, Judgment Labs and Ling 3.1 Flash -->
<!-- description: Hotfix Daily #6: Liquid AI's LFM3 puts 2B-class agent models on-device, DeepMind's Genie 4 adds audio to world simulation, ex-GitHub CEO's Entire swaps pull requests for Trails, Judgment Labs opens agent monitoring, and Ling-3.1-flash-1019 ships MIT weights. -->
**Issue #6 · Wednesday, Oct 28, 2026**

Five things from the last few days worth your attention if you build with AI. No fluff.

[Read this issue on the web](https://hotfixdaily.com/issues/006/) · [Sponsor Hotfix Daily](https://hotfixdaily.com/sponsor/)

---

[MODEL]
**1. Liquid AI's LFM3 brings small agent models to your device**
Six open-weight models around 2B parameters (text, vision, audio, omni and two decision models) share one 1.7B backbone. The text model has a 256K context window, fits in about 1 GB at 4-bit, and Liquid says it beats Qwen3.5-9B on WebArena-Verified and AutomationBench. Every model can be fine-tuned on a single GPU.
*Why builders care:* Background agents that run on a laptop cost nothing per token. Liquid admits bigger models still win on agentic coding, so use it for tool calls and triage, not refactors.
[source](https://www.liquid.ai/blog/lfm3)

[GAME DEV]
**2. DeepMind's Genie 4 adds sound and dialogue to playable worlds**
The new world model generates photorealistic scenes you steer with the keyboard and text prompts, plus ambient audio, music and interactive dialogue. Trusted testers get it first; Google AI Ultra subscribers and early Gemini API partners are next.
*Why builders care:* Google pitches it for prototyping game ideas. It also warns that details and object permanence drift in longer sessions, so treat it as a sketchpad, not an engine.
[source](https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/)

[DEVTOOLS]
**3. Ex-GitHub CEO's Entire replaces pull requests with Trails**
Thomas Dohmke's Git-compatible forge scores every push with agent-run evals (security, quality, "slop") shown at the top of the page, so your coding agent can keep fixing until the scores settle. It also syncs agent sessions into the repo as searchable memory. It's open to any developer now.
*Why builders care:* If your agents open more PRs than you can read, this is a real alternative workflow. Merging on scores alone is a choice, so decide which evals you actually trust.
[source](https://entire.com/blog/the-git-forge-for-agent-human-collaboration)

[AGENTS]
**4. Judgment Labs opens its agent monitoring platform to everyone**
It traces long-running agents down to subagents and tool calls, runs your own judges over the traces (filters, code checks or agentic judges), and lets you test fixes offline.
*Why builders care:* Most agent bugs show up in production as complaints. Turning traces into alerts finds them before your users do.
[source](https://x.com/alexshander03/status/2115111288066171211)

[REPO]
**5. Repo of the day: Ling-3.1-flash-1019, MIT-licensed weights**
inclusionAI's upgraded mixture-of-experts model has 560B total parameters, 25B active and a 1M-token context. The card reports AutomationBench-AA rising from 62% to 68% after more post-training.
*Why builders care:* The recommended self-hosting setup is eight H200s, so most of us will try it through an API first.
[source](https://huggingface.co/inclusionAI/Ling-3.1-flash-1019)

---

### Hotfix of the Day
In Cursor's Design Mode, Shift-click two components into one note and ask the agent to make one match the other. Turn on Batch edits to collect a round of notes and send them as one message.
[source](https://cursor.com/docs/agent/design-mode)
