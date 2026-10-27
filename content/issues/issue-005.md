# Hotfix Daily: The Daily AI Builder Digest
<!-- title: Hotfix Daily #5: GPT-6.1 Terra, Mirendil Fern, Cursor's Agent SDK, Uchikoshi on AI and tstack -->
<!-- description: Hotfix Daily #5: OpenAI's GPT-6.1 Terra halves API prices, Mirendil's Fern holds 10M tokens, Cursor's Agent SDK turns agents into code, Kotaro Uchikoshi on AI after a canceled game, and Theo's tstack skills. -->
**Issue #5 · Tuesday, Oct 27, 2026**

Five things from the last few days worth your attention if you build with AI. No fluff.

[Read this issue on the web](https://hotfixdaily.com/issues/005/) · [Sponsor Hotfix Daily](https://hotfixdaily.com/sponsor/)

---

[MODEL]
**1. OpenAI ships GPT-6.1 Terra at half the price**
The new middle model targets computer use, visual reasoning and writing. API prices are $1 per million input tokens and $5 per million output, 50% below GPT-5.6 Terra and GPT-6.1 Sol. At max effort it solves 50.3% of Terminal-Bench 4.0, up from 21.5% for GPT-5.6 Terra.
*Why builders care:* It's `gpt-6.1-terra` in the API now. OpenAI still points you to Sol or Astra for the hardest coding work, so try Terra on high-volume agent and form-filling jobs first.
[source](https://openai.com/index/introducing-gpt-6-1-terra/)

[CODING]
**2. Mirendil's first model, Fern, holds 10M tokens of context**
The new lab pretrained Fern from scratch for a window of up to 10 million tokens, which it puts at about half a million lines of code. Fern 0.1 is the first and smallest of three models, and access is listed as coming soon.
*Why builders care:* It's aimed at whole-repo work, long logs and agent traces. Retrieval at that length is one thing, reasoning across it is another, so wait for independent tests before planning around it.
[source](https://mirendil.com/news/introducing-fern/)

[AGENTS]
**3. Cursor's Agent SDK makes an agent a folder of code**
`instructions.md` is the prompt, each file in `tools/` is a typed action, and `agent-sdk eval` checks which tools ran and what the bot replied. Agents wake on GitHub, Slack, webhooks or cron, and deploy to Cursor or your own servers. Version 0.3.0 is the GA release.
*Why builders care:* Your review bots and triagers get version control and tests like the rest of your code. Start with `npx @cursor/agent-sdk init ./my-bot`.
[source](https://cursor.com/changelog/agent-sdk)

[GAME DEV]
**4. Kotaro Uchikoshi says mid-size studios now have to use AI**
In a Famitsu interview, the Zero Escape writer said a game his team worked on for about a year and a half was fully canceled after a publisher change of direction. He argued mid-size teams now compete with small AI-assisted indies, and that ideas stay human while AI handles endless polish passes.
*Why builders care:* His pitch is using AI to sweat the details, not to cut corners. That framing works well with a skeptical team.
[source](https://www.famitsu.com/article/202610/92056)

[REPO]
**5. Repo of the day: tstack, Theo's everyday agent skills**
Nine MIT-licensed skills for Claude Code and Codex covering the pull request lifecycle: proving a change, a three-model review "council," filing, babysitting CI, rebasing and merging.
*Why builders care:* Saying "full send" lets the agent merge on its own. Use `full-stop` if you want the last click.
[source](https://github.com/t3dotgg/tstack)

---

### Hotfix of the Day
Never start a coding agent in your Downloads folder. Forever Security found a planted `AGENTS.md` there that told Codex to install malware, and websites can drop files into Downloads. If you ever have, check `~/.codex/config.toml` for MCP servers you didn't add.
[source](https://forever.security/blog/hijacking-ai-agents-via-downloads-folder/)
