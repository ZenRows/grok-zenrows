# Zenrows for Grok Build

Live web data for Grok Build. This plugin connects Grok to the Zenrows MCP server, so Grok can fetch the current content of any public page, pull structured fields from it, run batch jobs over many URLs, and drive a hosted browser for pages that need clicks, forms or pagination. It also adds skills that tell Grok which Zenrows tool fits each task and how to keep requests efficient.

## What you get

- The Zenrows MCP server (`https://mcp.zenrows.com/mcp`). You sign in to your Zenrows account with OAuth; there is no API key to copy.
- Nine skills:

| Skill | Use it for |
|---|---|
| `zenrows` | Overview: tools, defaults, errors and plan limits |
| `zenrows-getting-started` | First-run checks and troubleshooting |
| `zenrows-scrape` | Reading one page |
| `zenrows-extract` | Named fields or JSON from one page |
| `zenrows-batch` | A list of five or more URLs as one job |
| `zenrows-crawl` | Many pages under one site section |
| `zenrows-map` | Listing a site's URLs without fetching them |
| `zenrows-browser` | Clicks, forms, pagination and multi-step flows |
| `zenrows-capture-api-calls` | Finding the API calls a page makes |

The skills are prefixed `zenrows-` because Grok loads skills from every enabled plugin into one namespace.

## Requirements

A Zenrows account. Requests use credits on your Zenrows plan. You can [sign up here](https://app.zenrows.com/register).

## Setup

Run `/plugins` in Grok Build, open the Marketplace tab and install `zenrows`.

Then connect it: run `/mcps`, select `zenrows` and press `i`. Grok opens your browser to sign in to Zenrows and stores the token in `~/.grok/mcp_credentials.json`.

Then ask Grok something like: "Use Zenrows to get the product names and prices from https://www.scrapingcourse.com/ecommerce/".

If a Zenrows tool is missing or a call returns `AUTH003`, run `grok mcp doctor zenrows`, or ask Grok to run its `zenrows-getting-started` skill.

## Network endpoints

This plugin calls two hosts, both operated by Zenrows:

| Host | Why |
|---|---|
| `mcp.zenrows.com` | The MCP server itself, over HTTP. Every tool call goes here. |
| `app.zenrows.com` | OAuth only: authorization, token exchange and dynamic client registration. |

Pages you ask Grok to fetch are retrieved by Zenrows, not by this plugin, so the plugin makes no direct request to the target site.

## Credentials and permissions

- An OAuth token for your Zenrows account, scope `api`, obtained through the browser sign-in and stored by Grok in `~/.grok/mcp_credentials.json`. The plugin never reads or writes that file.
- No API key, no environment variables, no hooks, no scripts, no filesystem access of its own. The plugin is a `.mcp.json` pointing at a hosted server, plus nine Markdown skills.
- Two skills suggest that Grok save large result sets under `./.zenrows/` in the working directory, and only when the user asked for the data. Grok's own file-write permissions apply.

## Privacy

The plugin sends the URLs and options you ask Grok to fetch to Zenrows, which processes them under the [Zenrows privacy policy](https://www.zenrows.com/legal/privacy).

## Support

- Documentation: [docs.zenrows.com](https://docs.zenrows.com)
- Contact: [success@zenrows.com](mailto:success@zenrows.com)

## License

MIT
