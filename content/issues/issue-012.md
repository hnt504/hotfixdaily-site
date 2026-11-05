# Hotfix Daily: The Daily AI Builder Digest
<!-- title: Kimi K3.1 Pro open weights, Factory buys HumanLayer and more -->
<!-- description: Moonshot publishes Kimi K3.1 Pro's weights, Factory buys HumanLayer, Together's agents tune inference, and 40% of 2026 Steam games disclose AI. -->
**Issue #12 · Thursday, Nov 5, 2026**

Five things from the last day worth your attention if you build with AI. No fluff.

[Read this issue on the web](https://hotfixdaily.com/issues/012/) · [Sponsor Hotfix Daily](https://hotfixdaily.com/sponsor/)

---

[MODEL]
**1. Moonshot publishes the Kimi K3.1 Pro weights**
Kimi K3.1 Pro is now on Hugging Face: a 2.8T-parameter mixture-of-experts model with 104B active, a 1M-token context and image input. The license reads like MIT, except API resellers over $20M a year need a separate deal and huge products must show the Kimi name.
*Why builders care:* A frontier-class open agent model you can self-host or fine-tune, though it needs data-center hardware.
[source](https://huggingface.co/moonshotai/Kimi-K3.1-Pro)

[AGENTS]
**2. Factory buys HumanLayer, the multiplayer coding-agent IDE**
HumanLayer's founders Dex Horthy and Kyle Mistele are joining Factory. The hosted platform stays up for at least 30 days so users can export data, move to Factory or self-host the Apache 2.0 open-source version. Recent paying customers get refunds.
*Why builders care:* If your team runs on HumanLayer, pick self-host or migrate before the window closes.
[source](https://factory.com/news/humanlayer)

[DEVTOOLS]
**3. Together AI lets agents tune its inference kernels**
Together Compiler has a swarm of agents propose GPU kernel changes, while a persistent engine checks each one for speed and correctness. Only verified changes ship. Together says it reached up to 2.6x higher tokens per second on open models in under 24 hours, and it's on by default for supported serverless models at the same price.
*Why builders care:* Cheaper, faster open-model endpoints with nothing to configure.
[source](https://www.together.ai/blog/together-compiler-continual-compilation-for-ai-inference)

[GAME DEV]
**4. 40% of 2026 Steam releases now disclose AI content**
A daily count by PCGame.com of Valve's own AI flag finds 10,661 of 26,486 Steam games released this year disclose AI content (as of Nov 5). Flagged games are 40% of releases but just 12% of reviews.
*Why builders care:* Disclosure is self-reported and art leads the uses. Players are filtering, so be specific about what AI did in your game.
[source](https://www.pcgame.com/steam-ai-statistics)

[REPO]
**5. Axiom formalizes the whole Stacks Project in Lean**
Axiom used coordinated swarms of AI agents to turn the roughly 7,500-page algebraic geometry reference into about 16 million lines of machine-checked Lean. Along the way it found dozens of statements needing fixes, like missing hypotheses.
*Why builders care:* A real blueprint for agent swarms on one huge codebase: stable interfaces, audits and downstream checks.
[source](https://axiommath.ai/research/the-stacks-project-formalized/)

---

### Hotfix of the Day
Give reasoning models room to think before you judge them. webAI's new TwIL-8B card says it averages about 19.5k output tokens per AIME 2026 problem and that a short budget "truncates the reasoning and scores far worse." Its example sets `max_new_tokens=32768`. Check your eval harness's token cap before you call a small model bad.
[source](https://huggingface.co/webAI-Official/TwIL-8B)
