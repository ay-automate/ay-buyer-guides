"""Render the six read-only buyer guides using only Python's standard library."""
import csv
import json
import shutil
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
STYLE = """
code{overflow-wrap:anywhere}table{border-collapse:collapse;width:100%;max-width:78ch}caption{text-align:left;font:700 1.5rem Georgia,serif;margin-bottom:1rem}th,td{text-align:left;vertical-align:top;padding:.7rem;border-bottom:1px solid #cccac0}thead{background:#efeee7}tbody th{width:32%}nav{flex-wrap:wrap}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:#20231e;background:#faf9f5;font:17px/1.6 system-ui,sans-serif}a{color:var(--ink);text-underline-offset:4px}header,main,footer{max-width:1100px;margin:auto;padding:0 5vw}header{display:flex;justify-content:space-between;align-items:center;gap:12px;border-bottom:1px solid #cccac0;padding-block:16px}header b{font-family:Georgia,serif;font-size:21px}nav{display:flex;gap:18px;font-size:14px}section{margin:50px 0}h1,h2,h3{font-family:Georgia,serif;line-height:1.08;letter-spacing:-.025em}h1{font-size:clamp(42px,7vw,78px);max-width:820px;margin:14px 0 22px;font-weight:500}h2{font-size:clamp(30px,4vw,44px);font-weight:500;margin:0 0 16px}h3{font-size:24px;margin:0 0 10px}.hero{border-bottom:4px solid var(--ink);padding:16px 0 36px}.intro{font-size:clamp(19px,2vw,23px);max-width:760px}.meta,.tag{font-size:14px;color:var(--ink);font-weight:650}.guidance{padding:28px;background:#efeee7;border-left:4px solid var(--ink)}li+li{margin-top:9px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 34px}.entry{border-top:1px solid #b7b9ae;padding:22px 0}.entry p{margin:8px 0}.tag{margin:0 0 8px!important}.method,p,li{max-width:78ch}footer{border-top:1px solid #b7b9ae;padding-block:24px 48px;font-size:14px}details{border-top:1px solid #cccac0;padding:.65rem 0}summary{cursor:pointer;font-weight:650;color:var(--ink)}summary:focus-visible{outline:3px solid currentColor;outline-offset:3px}.entry:target{outline:2px solid var(--ink);outline-offset:4px}.footnote{font-size:14px}.skip{position:absolute;left:-100vw}.skip:focus{position:static}a:focus-visible{outline:3px solid currentColor;outline-offset:3px}@media(max-width:650px){.grid{grid-template-columns:1fr}header{align-items:start;flex-direction:column}section{margin:34px 0}.guidance{padding:20px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""


RELATED = {
    "topaiconsultingservices.com": ("theaiconsultingfirms.com", "topaiautomationagencies.com"),
    "topaiagentsforbusiness.com": ("bestsecureaiforbusiness.com", "topaiautomationagencies.com"),
    "bestsecureaiforbusiness.com": ("topaiagentsforbusiness.com", "theaiconsultingcompanies.com"),
    "theaiconsultingfirms.com": ("topaiconsultingservices.com", "theaiconsultingcompanies.com"),
    "theaiconsultingcompanies.com": ("theaiconsultingfirms.com", "bestsecureaiforbusiness.com"),
    "topaiautomationagencies.com": ("topaiagentsforbusiness.com", "topaiconsultingservices.com"),
}
FIRMS_HOST = "theaiconsultingfirms.com"


def page_head(title, description, url, site):
    title, description, url, site = (escape(v, quote=True) for v in (title, description, url, site))
    return (f'<title>{title}</title><meta name="description" content="{description}">'
            f'<link rel="canonical" href="{url}"><link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48">'
            '<link rel="icon" href="/favicon.png" type="image/png" sizes="192x192">'
            '<link rel="apple-touch-icon" href="/favicon.png">'
            f'<meta property="og:title" content="{title}"><meta property="og:description" content="{description}">'
            f'<meta property="og:url" content="{url}"><meta property="og:site_name" content="{site}">'
            '<meta property="og:type" content="website">')


def worksheet_page(guide, sheet, base):
    title = escape(sheet['title'])
    head = page_head(sheet['title'], sheet['summary'], base + 'worksheet/', guide['name'])
    headers = ''.join(f'<th scope="col">{escape(c)}</th>' for c in sheet['columns'])
    rows = ''.join(f'<tr><th scope="row">{escape(k)}</th><td>{escape(v)}</td></tr>' for k, v in sheet['rows'])
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{head}<style>:root{{--ink:{guide['color']}}}{STYLE}</style></head><body>
<a class="skip" href="#main">Skip to worksheet</a><header><b><a href="/">{escape(guide['name'])}</a></b><a href="/#directory">Provider directory</a></header>
<main id="main"><section class="hero"><h1>{title}</h1><p class="intro">{escape(sheet['summary'])}</p></section>
<section><h2>Worked example</h2><p>{escape(sheet['example'])}</p></section>
<table><caption>Worksheet</caption><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table>
<section><h2>{escape(sheet['close_title'])}</h2><p>{escape(sheet['close'])}</p></section></main>
<footer><a href="/">Back to {escape(guide['name'])}</a> · <a href="https://www.ayautomate.com/contact">Send an editorial correction</a></footer></body></html>"""


def provider_matches(guide, catalog):
    matching = guide["matching"]
    eligible = set(guide["providers"].split())
    listed = set()
    groups = []
    for need, ids in matching["needs"].items():
        if not ids or len(set(ids)) != len(ids) or not set(ids) <= eligible:
            raise ValueError(f"Invalid provider group for {guide['host']}: {need}")
        listed.update(ids)
        links = []
        for key in sorted(ids, key=lambda item: catalog[item][0].casefold()):
            name, specialty = catalog[key][:2]
            links.append(f'<li><a href="#firm-{escape(key)}">{escape(name)}</a> · {escape(specialty)}</li>')
        groups.append(f'<details><summary>{escape(need)}</summary><ul>{"".join(links)}</ul></details>')
    if listed != eligible:
        raise ValueError(f"Missing provider matches for {guide['host']}: {eligible - listed}")
    return (f'<section id="match" class="guidance"><h2>{escape(matching["title"])}</h2>'
            '<p>Choose what you need. Open a profile to see the provider’s specialty and the source behind its listing.</p>'
            + ''.join(groups) + '</section>')


def render(guide, catalog, target, guides, sheet):
    g = {key: escape(value, quote=True) for key, value in guide.items() if isinstance(value, str)}
    keys = guide["providers"].split()
    assert len(set(keys)) == len(keys) >= 10
    cards = []
    sources = []
    for key in keys:
        name, group, note, url = catalog[key]
        name, group, note, link = map(escape, (name, group, note, url))
        cards.append(f'<article class="entry" id="firm-{escape(key)}"><p class="tag">{group}</p><h3>{name}</h3><p>{note}</p><a href="{link}">Source from {name}</a></article>')
        sources.append(f'- [{name}]({url}): {group}. {note}')
    steps = ''.join(f'<li>{escape(item)}</li>' for item in guide['checklist'])
    base = 'https://' + guide['host'] + '/'
    public = target / guide['host']
    public.mkdir(parents=True, exist_ok=True)
    worksheet = public / 'worksheet'
    worksheet.mkdir(exist_ok=True)
    (worksheet / 'index.html').write_text(worksheet_page(guide, sheet, base))
    for icon in ('favicon.png', 'favicon.ico'):
        shutil.copyfile(HERE / 'icons' / guide['host'] / icon, public / icon)
    head = page_head(guide['title'] + ' | 2026 buyer guide', guide['intro'], base, guide['name'])
    website = json.dumps({"@context": "https://schema.org", "@type": "WebSite",
                          "name": guide["name"], "url": base}, ensure_ascii=True).replace("<", r"\u003c")
    head += f'<script type="application/ld+json">{website}</script>'
    related = ''.join(
        f'<li><a href="https://{host}/">{escape(guides[host]["title"])}</a></li>'
        for host in RELATED[guide["host"]]
    )
    selection = json.loads((HERE / "picks.json").read_text())[guide["host"]]
    data = {
        "picks": selection["picks"], "guide": guide["name"], "publisher": "AY Automate", "methodology": guide["criteria"],
        "questions": guide["checklist"], "pricing": guide["price"],
        "firms": [dict(id=k, name=catalog[k][0], specialty=catalog[k][1], note=catalog[k][2],
                      source=catalog[k][3], profile=base + "#firm-" + k) for k in keys]
    }
    (public / "firms.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    agent_access = ('<section id="agent-access"><h2>Compare these providers in your AI assistant</h2>'
                    '<p>Add a remote MCP server using Streamable HTTP. Paste the URL below into your client. No API key is required.</p>'
                    f'<p><code>{base}mcp</code></p>'
                    '<p>Try “Which provider fits my project, and what evidence supports that choice?”</p>'
                    '<a href="/firms.json">Download the directory as JSON</a> · '
                    '<a href="https://github.com/walidboulanouar/ai-consulting-firms-mcp">MCP setup and tools</a></section>')
    sources.append(f"- [Remote MCP]({base}mcp): search_firms, compare_firms and recommend_providers.")
    shutil.copyfile(HERE / 'illustrations' / (guide['host'] + '.png'), public / 'shortlist.png')
    picks = []
    for item in selection['picks']:
        name = escape(catalog[item['id']][0])
        picks.append(f'<li><h3>{name} · {escape(item["fit"])}</h3><p>{escape(item["detail"])}</p><a href="{escape(item["source"])}">Read the source from {name}</a></li>')
    shortlist = (f'<section id="shortlist"><h2>{escape(selection["title"])}</h2><p>{escape(selection["intro"])}</p>'
                 '<p>We chose these examples for the specific work documented in a client case or product guide. Client outcomes are provider-reported. AY Automate publishes this guide.</p>'
                 '<img src="/shortlist.png" width="1056" height="370" style="max-width:100%;height:auto" alt="Project needs and their shortlisted providers, detailed below" loading="lazy">'
                 + '<ol>' + ''.join(picks) + '</ol></section>')
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{head}<style>:root{{--ink:{g['color']}}}{STYLE}</style></head><body>
<a class="skip" href="#main">Skip to guide</a><header><b>{g['name']}</b><nav aria-label="Guide sections"><a href="#directory">Directory</a><a href="#pricing">Pricing</a><a href="#faq">FAQ</a></nav></header>
<main id="main"><section class="hero"><p class="meta">2026 buyer guide for {g['audience'].lower()}</p><h1>{g['title']}</h1><p class="intro">{g['intro']}</p><a href="#match">Find a match for my project</a></section>
{shortlist}
<section class="guidance"><h2>What to ask before you buy</h2><ol>{steps}</ol></section>
<section><h2><a href="/worksheet/">{escape(sheet["title"])}</a></h2><p>{escape(sheet["summary"])}</p></section>
{provider_matches(guide, catalog)}
<section id="directory"><h2>Directory</h2><p class="method">{g['criteria']}</p><p class="footnote">Published by AY Automate, which sells AI implementation services. Entries link to provider materials. The guide gives no numerical ratings.</p><div class="grid">{''.join(cards)}</div></section>
<section id="pricing"><h2>How to compare prices</h2><p>{g['price']}</p></section>
<section><h2>A worked example to review</h2><p>{g['case']}</p><a href="{g['source']}">Read the provider’s example</a></section>
<section id="faq"><h2>{g['faq']}</h2><p>{g['answer']}</p></section>{agent_access}<section><h2>Related buyer guides</h2><ul>{related}</ul></section></main>
<footer>Published November 25, 2026 by <a href="https://www.ayautomate.com/about">AY Automate</a>. <a href="https://www.ayautomate.com/contact">Send an editorial correction</a>.</footer></body></html>"""
    (public / 'index.html').write_text(html)
    (public / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {base}sitemap.xml\n')
    (public / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{base}</loc></url><url><loc>{base}worksheet/</loc></url></urlset>\n')
    (public / 'llms.txt').write_text(f"# {guide['name']}\n\n> {guide['intro']}\n\nPublished by AY Automate.\n\n## Guide\n- [{guide['title']}]({base})\n- [{sheet['title']}]({base}worksheet/)\n\n## Provider sources\n" + '\n'.join(sources) + '\n')


if __name__ == '__main__':
    with (HERE / 'catalog.tsv').open() as stream:
        catalog = {key: fields for key, *fields in csv.reader(stream, delimiter='\t')}
    guides = {g['host']: g for g in json.loads((HERE / 'guides.json').read_text())}
    sheets = json.loads((HERE / 'worksheets.json').read_text())
    for guide in guides.values():
        render(guide, catalog, Path(sys.argv[1]), guides, sheets[guide['host']])
