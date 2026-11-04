# Hotfix Daily: The Daily AI Builder Digest
<!-- title: Tencent Hy4, GitBook's AI-agent breach, itch.io No AI and more -->
<!-- description: Tencent Hy4 adds vision and computer use, GitBook rotates tokens after an AI-agent attack, itch.io adds No AI filters, plus QuickProof and Crouton Alpha. -->
**Issue #11 · Wednesday, Nov 4, 2026**

Five things from the last day worth your attention if you build with AI. No fluff.

[Read this issue on the web](https://hotfixdaily.com/issues/011/) · [Sponsor Hotfix Daily](https://hotfixdaily.com/sponsor/)

---

[MODEL]
**1. Tencent ships Hy4 with vision and computer use**
Hy4 is the first Hy model that can see, and the first that does computer use across CLIs and GUIs, with targeted training on tools like Blender and CAD. It's live on Tencent Cloud and OpenRouter at $0.834 input and $2.501 output per million tokens, and Tencent says it plans to release the weights later with a system card.
*Why builders care:* A cheap, soon-to-be-open model aimed at agents and game dev. Tencent itself says a notable gap to top proprietary models remains, so test before you switch.
[source](https://hy.tencent.ai/research/hy4)

[AGENTS]
**2. GitBook says an attacker used AI agents to get in**
An attacker using AI agents got some of GitBook's infrastructure credentials on Nov 2. Integration tokens, Git Sync secrets, API tokens and Assistant visitor questions may have been accessed. GitBook revoked all personal API tokens and restored service Nov 3.
*Why builders care:* If your docs live on GitBook, rotate your GitBook and third-party tokens and re-authenticate its MCP server today.
[source](https://www.gitbook.com/status/security-incident-2026-11-03)

[GAME DEV]
**3. itch.io adds AI-disclosure filtering to search**
After deleting "a couple terabytes of ai slop," itch.io is adding generative AI disclosure filtering to more of the site, including search results. Tabletop games, books, comics and soundtracks now need an AI disclosure before you can create or edit a page, joining game assets.
*Why builders care:* If you sell on itch.io, fill in your disclosure accurately. It now decides who finds you.
[source](https://bsky.app/profile/itch.io/post/3mzezjvqexs2h)

[CODING]
**4. Crouton Alpha: a free stealth model on OpenRouter**
OpenRouter listed Crouton Alpha on Nov 3. It's free, with a 1,048,576-token context, multimodal input, tool calling and structured outputs. The provider is anonymous, and prompts may be retained, though not used for training.
*Why builders care:* A free long-context model to try for agent sub-tasks. Just keep secrets and client code out of it.
[source](https://openrouter.ai/stealth/crouton-alpha)

[REPO]
**5. QuickProof: write C specs like tests, let agents prove them**
GenProof's QuickProof turns a small C program into a Rocq theorem that AI agents then prove, and `qp verify` checks that nobody weakened the statement. GenProof says it found more than 300 bugs across 20 C projects, including Redis and zstd.
*Why builders care:* Practical formal verification for C. Note that it's under the PolyForm Noncommercial license.
[source](https://github.com/genproof/quickproof-public)

---

### Hotfix of the Day
Check what other apps have wired into your coding agents. A GitHub report shows Postman Desktop auto-installed plugins into Claude Code and Codex, including a SessionStart hook. Look at `enabledPlugins` and `hooks` in `~/.claude/settings.json`, and the `[plugins]` and `[hooks.state]` sections in `~/.codex/config.toml`. Remove what you didn't add.
[source](https://github.com/postmanlabs/postman-app-support/issues/14370)
