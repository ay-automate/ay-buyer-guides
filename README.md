# AI buyer guides

Six buyer guides for teams buying AI services. Each directory entry includes the provider’s own source. AY Automate publishes the guides.

| Guide | Site | Sitemap |
| --- | --- | --- |
| AI Consulting Services | [topaiconsultingservices.com](https://topaiconsultingservices.com/) | [XML](https://topaiconsultingservices.com/sitemap.xml) |
| Business Agent Guide | [topaiagentsforbusiness.com](https://topaiagentsforbusiness.com/) | [XML](https://topaiagentsforbusiness.com/sitemap.xml) |
| Secure AI for Business | [bestsecureaiforbusiness.com](https://bestsecureaiforbusiness.com/) | [XML](https://bestsecureaiforbusiness.com/sitemap.xml) |
| AI Consulting Firms | [theaiconsultingfirms.com](https://theaiconsultingfirms.com/) | [XML](https://theaiconsultingfirms.com/sitemap.xml) |
| AI Consulting Companies | [theaiconsultingcompanies.com](https://theaiconsultingcompanies.com/) | [XML](https://theaiconsultingcompanies.com/sitemap.xml) |
| AI Automation Agencies | [topaiautomationagencies.com](https://topaiautomationagencies.com/) | [XML](https://topaiautomationagencies.com/sitemap.xml) |

## Build the guides

Run `npm ci --ignore-scripts` followed by `npm run build` from the repository root. Open `dist/<domain>/index.html` or serve that directory with any static web server. Each site has its own favicon, canonical URLs, robots.txt, llms.txt and XML sitemap. Each sitemap includes the homepage, the buyer worksheet and a domain-specific decision guide. Edit decisions.json for the decision guides. Edit worksheets.json to update the examples and decision tables. Source icons live under icons/. Each site generates its own firms.json catalog.

The public source corresponds to the published guides. Live releases run through the publisher’s separate deployment repository.

## Agent access

Choose the guide that matches your purchase. Paste its endpoint into a remote MCP client and leave authentication empty.

| Guide | Streamable HTTP endpoint | JSON data |
| --- | --- | --- |
| Secure AI for Business | `https://bestsecureaiforbusiness.com/mcp` | [Catalog](https://bestsecureaiforbusiness.com/firms.json) |
| AI Consulting Companies | `https://theaiconsultingcompanies.com/mcp` | [Catalog](https://theaiconsultingcompanies.com/firms.json) |
| AI Consulting Firms | `https://theaiconsultingfirms.com/mcp` | [Catalog](https://theaiconsultingfirms.com/firms.json) |
| Business AI Agents | `https://topaiagentsforbusiness.com/mcp` | [Catalog](https://topaiagentsforbusiness.com/firms.json) |
| AI Automation Agencies | `https://topaiautomationagencies.com/mcp` | [Catalog](https://topaiautomationagencies.com/firms.json) |
| AI Consulting Services | `https://topaiconsultingservices.com/mcp` | [Catalog](https://topaiconsultingservices.com/firms.json) |

[MCP setup and tools](https://github.com/walidboulanouar/ai-consulting-firms-mcp)

## Related AY directories

These Cloudflare Pages projects have separate sitemaps.

| Directory | Sitemap |
| --- | --- |
| [mcp-index](https://mcp-index.pages.dev/) | [XML](https://mcp-index.pages.dev/sitemap.xml) |
| [skill-shelf](https://skill-shelf-2oq.pages.dev/) | [XML](https://skill-shelf-2oq.pages.dev/sitemap.xml) |
| [agent-atlas](https://agent-atlas-961.pages.dev/) | [XML](https://agent-atlas-961.pages.dev/sitemap.xml) |
| [geo-stack](https://geo-stack.pages.dev/) | [XML](https://geo-stack.pages.dev/sitemap.xml) |
| [code-agents](https://code-agents-a8g.pages.dev/) | [XML](https://code-agents-a8g.pages.dev/sitemap.xml) |
| [outbound-stack](https://outbound-stack-7jo.pages.dev/) | [XML](https://outbound-stack-7jo.pages.dev/sitemap.xml) |
| [model-desk](https://model-desk.pages.dev/) | [XML](https://model-desk.pages.dev/sitemap.xml) |
| [launch-list](https://launch-list.pages.dev/) | [XML](https://launch-list.pages.dev/sitemap.xml) |
| [automation-atlas](https://automation-atlas.pages.dev/) | [XML](https://automation-atlas.pages.dev/sitemap.xml) |
| [open-alt](https://open-alt.pages.dev/) | [XML](https://open-alt.pages.dev/sitemap.xml) |
| [gen-media](https://gen-media.pages.dev/) | [XML](https://gen-media.pages.dev/sitemap.xml) |
| [vibe-builders](https://vibe-builders.pages.dev/) | [XML](https://vibe-builders.pages.dev/sitemap.xml) |
| [voice-agents](https://voice-agents.pages.dev/) | [XML](https://voice-agents.pages.dev/sitemap.xml) |
| [data-wells](https://data-wells.pages.dev/) | [XML](https://data-wells.pages.dev/sitemap.xml) |
| [ai-agencies](https://ai-agencies.pages.dev/) | [XML](https://ai-agencies.pages.dev/sitemap.xml) |

The design system is in guide.css. Edit fieldwork.json for the six buyer scenarios, decision diagrams and editable worksheet prompts. The renderer includes every generated canonical HTML page in its site’s sitemap.

The six sites share Next.js Pages Router components. The production build exports each domain to its own directory under `dist/`. Native links, details and worksheet controls work without client JavaScript.
