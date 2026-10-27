# Changelog

## 0.1.1

- The `zenrows-extract` and `zenrows` skills no longer say `fallback_autoparse` retries with autoparse: it has had no effect since the Zenrows MCP server removed that fallback. They now handle `REQS007` by its `reason`: `domain_not_prepared` (prepare the domain with `prepare_domain`, then wait for `prepared_domain_status`), `page_not_recognised` and `domain_not_enabled`. `mode='autoparse'` is marked deprecated, and `include_html` is listed.

## 0.1.0

- First release for Grok Build: the Zenrows MCP server (OAuth sign-in) and nine skills: `zenrows`, `zenrows-getting-started`, `zenrows-scrape`, `zenrows-extract`, `zenrows-batch`, `zenrows-crawl`, `zenrows-map`, `zenrows-browser` and `zenrows-capture-api-calls`.
- The capability skills are ported from [copilot-zenrows](https://github.com/ZenRows/copilot-zenrows) at `v0.1.0` (`0ef055161cef564ab5a495bda0df473d19ee2b28`), with setup steps rewritten for Grok Build.
- Skill names carry a `zenrows-` prefix here, unlike the Claude and Copilot plugins. Grok loads skills from every enabled plugin into one namespace, so bare names like `batch` or `map` would collide with other plugins' skills.
