"""Render the six read-only buyer guides using only Python's standard library."""
import csv
import json
import shutil
import sys
from html import escape
from xml.etree import ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
STYLE = (HERE / 'guide.css').read_text()
FIELDWORK = json.loads((HERE / 'fieldwork.json').read_text())
ARTICLES = json.loads((HERE / 'decisions.json').read_text())

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


def masthead(guide):
    name = escape(guide['name'])
    return (f'<header><a class="brand" href="/"><img src="/favicon.png" alt="" width="35" height="35">{name}</a>'
            '<nav aria-label="Primary"><a href="/#directory">Directory</a><a href="/worksheet/">Worksheet</a>'
            '<a href="/#agent-access">For AI assistants</a></nav></header>')


def hero(guide, label, title, intro, action=None):
    field = FIELDWORK[guide['host']]
    stages = ''.join(f'<li><b>{escape(stage)}</b><span>{escape(detail)}</span></li>' for stage, detail in field['stages'])
    cta = f'<a class="button" href="{escape(action[0])}">{escape(action[1])} &rarr;</a>' if action else ''
    return (f'<section class="hero"><div><p class="meta">{escape(label)}</p><h1>{escape(title)}</h1>'
            f'<p class="intro">{escape(intro)}</p>{cta}</div><aside class="board"><h2>{escape(field["board"])}</h2>'
            f'<ol>{stages}</ol></aside></section>')


def reading_layout(toc, body):
    links = ''.join(f'<a href="#{key}">{escape(label)}</a>' for key, label in toc)
    return (f'<div class="reading"><aside><p class="reading-label">On this page</p>'
            f'<nav aria-label="On this page">{links}</nav></aside><article>{body}</article></div>')


def wrap_page(guide, head, content):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{head}<style>:root{{--ink:{guide['color']}}}{STYLE}</style></head><body>
<a class="skip" href="#main">Skip to content</a>{masthead(guide)}<main id="main">{content}</main>
<footer>Published by <a href="https://www.ayautomate.com/about">AY Automate</a>. <a href="/">Guide home</a> · <a href="https://www.ayautomate.com/contact">Send an editorial correction</a></footer></body></html>"""


def worksheet_page(guide, sheet, base):
    field = FIELDWORK[guide['host']]
    head = page_head(sheet['title'], sheet['summary'], base + 'worksheet/', guide['name'])
    headers = ''.join(f'<th scope="col">{escape(c)}</th>' for c in sheet['columns'])
    rows = ''.join(f'<tr><th scope="row">{escape(k)}</th><td>{escape(v)}</td></tr>' for k, v in sheet['rows'])
    notes = ''.join(f'<p id="prompt-{i}" class="prompt">{escape(name)}</p><div class="write-in" contenteditable="plaintext-only" role="textbox" aria-multiline="true" aria-labelledby="prompt-{i}"></div>'
                    for i, name in enumerate(field['record'], 1))
    article = ARTICLES[guide['host']]
    body = f"""<section id="scenario"><h2>Worked example</h2><p>{escape(sheet['example'])}</p></section>
<section id="worksheet"><table><caption>Worksheet</caption><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table></section>
<section id="record"><h2>Your decision record</h2><p>Type in the fields below or print a blank copy. Use your browser’s Print or Save as PDF before closing the page. Entries stay in this open tab.</p>{notes}
<p><label><input type="checkbox">Evidence reviewed with the responsible owner</label></p></section>
<section class="example" id="next"><h2>{escape(sheet['close_title'])}</h2><p>{escape(sheet['close'])}</p><p>{escape(field['next'])}</p>
<a href="/{escape(article['slug'])}/">{escape(article['title'])}</a></section>"""
    toc = [('scenario', 'Worked example'), ('worksheet', 'Worksheet'), ('record', 'Your decision record'), ('next', 'Next decision')]
    opening = hero(guide, 'Buyer worksheet', sheet['title'], sheet['summary'], ('#record', 'Fill out the decision record'))
    return wrap_page(guide, head, opening + reading_layout(toc, body))


def decision_page(guide, article, base):
    field = FIELDWORK[guide['host']]
    url = base + article['slug'] + '/'
    head = page_head(article['title'], article['summary'], url, guide['name'])
    toc = [(f'step-{i}', h) for i, (h, _) in enumerate(article['sections'], 1)]
    sections = ''.join(f'<section id="{key}"><h2>{escape(h)}</h2><p>{escape(body)}</p></section>'
                       for (key, h), (_, body) in zip(toc, article['sections']))
    headers = ''.join(f'<th scope="col">{escape(c)}</th>' for c in article['columns'])
    rows = []
    for label, *values in article['rows']:
        cells = ''.join(f'<td>{escape(v)}</td>' for v in values)
        rows.append(f'<tr><th scope="row">{escape(label)}</th>{cells}</tr>')
    evidence = ''.join(f'<div><h3>{title}</h3><p>{escape(field[key])}</p></div>'
                       for key, title in [('evidence', 'What to keep'), ('hold', 'When to pause')])
    body = f"""{sections}<section id="decision-table"><table><caption>Decision table</caption><thead><tr>{headers}</tr></thead><tbody>{''.join(rows)}</tbody></table></section>
<section id="rehearsal"><p class="meta">Illustrative buyer scenario</p><h2>{escape(field['headline'])}</h2><p>{escape(field['scenario'])}</p><p>{escape(field['test'])}</p><div class="fieldnotes">{evidence}</div></section>
<section class="example" id="decision"><h2>Make the decision</h2><p>{escape(article['decision'])}</p><a class="button" href="/worksheet/">Open the buyer worksheet &rarr;</a></section>
<section><h2>Further reading</h2><a href="{escape(article['url'])}">{escape(article['source'])}</a></section>"""
    if article['slug'] == 'ai-consulting-pricing':
        toc.insert(0, ('published-scopes', 'Compare two published scopes'))
        body = (HERE / 'scope-comparison.html').read_text() + body
    toc += [('decision-table', 'Decision table'), ('rehearsal', 'Worked buyer scenario'), ('decision', 'Make the decision')]
    return wrap_page(guide, head, hero(guide, 'Decision guide', article['title'], article['opening']) + reading_layout(toc, body))


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
    questions = guide.get('review_questions', {})
    if questions and set(questions) != set(keys):
        raise ValueError(f"Incomplete buying criteria for {guide['host']}")
    descriptions = {}
    cards = []
    sources = []
    for key in keys:
        name, group, note, url = catalog[key]
        if key in questions:
            note = note.partition(". ")[0].rstrip(".") + ". " + questions[key]
        descriptions[key] = note
        name, group, note, link = map(escape, (name, group, note, url))
        cards.append(f'<article class="entry" id="firm-{escape(key)}"><p class="tag">{group}</p><h3>{name}</h3><p>{note}</p><a href="{link}">Source from {name}</a></article>')
        sources.append(f'- [{name}]({url}): {group}. {note}')
    steps = ''.join(f'<li>{escape(item)}</li>' for item in guide['checklist'])
    base = 'https://' + guide['host'] + '/'
    public = target / guide['host']
    public.mkdir(parents=True, exist_ok=True)
    article = ARTICLES[guide['host']]
    decision = public / article['slug']
    decision.mkdir(exist_ok=True)
    (decision / 'index.html').write_text(decision_page(guide, article, base))
    article_path = '/' + article['slug'] + '/'
    worksheet = public / 'worksheet'
    worksheet.mkdir(exist_ok=True)
    (worksheet / 'index.html').write_text(worksheet_page(guide, sheet, base))
    for icon in ('favicon.png', 'favicon.ico'):
        shutil.copyfile(HERE / 'icons' / guide['host'] / icon, public / icon)
    head = page_head(guide['title'] + ' | 2026 buyer guide', guide['intro'], base, guide['name'])
    website = json.dumps({"@context": "https://schema.org", "@type": "WebSite",
                          "name": guide["name"], "url": base}, ensure_ascii=True).replace("<", r"\u003c")
    head += f'<script type="application/ld+json">{website}</script>'
    if questions:
        directory = {"@context": "https://schema.org", "@type": "CollectionPage",
                     "url": base, "name": guide['title'], "description": guide['intro'],
                     "publisher": {"@type": "Organization", "name": "AY Automate", "url": "https://www.ayautomate.com/"},
                     "mainEntity": {"@type": "ItemList", "itemListOrder": "https://schema.org/ItemListUnordered",
                                    "numberOfItems": len(keys),
                                    "itemListElement": [{"@type": "ListItem", "position": i, "name": catalog[k][0],
                                                         "url": base + "#firm-" + k} for i, k in enumerate(keys, 1)]}}
        structured = json.dumps(directory, ensure_ascii=True).replace("<", r"\u003c")
        head += f'<script type="application/ld+json">{structured}</script>'
    related = ''.join(
        f'<li><a href="https://{host}/">{escape(guides[host]["title"])}</a></li>'
        for host in RELATED[guide["host"]]
    )
    selection = json.loads((HERE / "picks.json").read_text())[guide["host"]]
    data = {
        "picks": selection["picks"], "guide": guide["name"], "publisher": "AY Automate", "methodology": guide["criteria"],
        "questions": guide["checklist"], "pricing": guide["price"],
        "firms": [dict(id=k, name=catalog[k][0], specialty=catalog[k][1], note=descriptions[k],
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
    field = FIELDWORK[guide['host']]
    opening = hero(guide, field['label'] + ' / 2026 buyer guide', guide['title'], guide['intro'], ('#match', 'Find a provider by need'))
    body = f"""{opening}
{shortlist}
<section class="guidance"><h2>What to ask before you buy</h2><ol>{steps}</ol></section>
<section><h2>Buyer resources</h2><div class="resources"><a class="resource" href="/worksheet/"><span class="card-label">Working document</span><h3>{escape(sheet["title"])}</h3><p>{escape(sheet["summary"])}</p></a>
<a class="resource" href="{article_path}"><span class="card-label">Decision guide</span><h3>{escape(article["title"])}</h3><p>{escape(article["summary"])}</p></a></div></section>
{provider_matches(guide, catalog)}
<section id="directory"><h2>Directory</h2><p class="method">{g['criteria']}</p><p class="footnote">Published by AY Automate, which sells AI implementation services. Entries link to provider materials. The guide gives no numerical ratings.</p><div class="grid">{''.join(cards)}</div></section>
<section id="pricing"><h2>How to compare prices</h2><p>{g['price']}</p></section>
<section><h2>A worked example to review</h2><p>{g['case']}</p><a href="{g['source']}">Read the provider’s example</a></section>
<section id="faq"><h2>{g['faq']}</h2><p>{g['answer']}</p></section>{agent_access}<section><h2>Related buyer guides</h2><ul>{related}</ul></section>"""
    html = wrap_page(guide, head, body)
    (public / 'index.html').write_text(html)
    (public / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {base}sitemap.xml\n')
    sitemap = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for page in sorted(public.rglob('index.html')):
        route = page.parent.relative_to(public).as_posix()
        location = base if route == '.' else base + route + '/'
        if f'<link rel="canonical" href="{location}">' not in page.read_text():
            raise ValueError(f'Canonical does not match sitemap URL {location}')
        ET.SubElement(ET.SubElement(sitemap, 'url'), 'loc').text = location
    ET.ElementTree(sitemap).write(public / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    (public / 'llms.txt').write_text(f"# {guide['name']}\n\n> {guide['intro']}\n\nPublished by AY Automate.\n\n## Guide\n- [{guide['title']}]({base})\n- [{sheet['title']}]({base}worksheet/)\n- [{article['title']}]({base}{article['slug']}/)\n\n## Provider sources\n" + '\n'.join(sources) + '\n')


if __name__ == '__main__':
    with (HERE / 'catalog.tsv').open() as stream:
        catalog = {key: fields for key, *fields in csv.reader(stream, delimiter='\t')}
    guides = {g['host']: g for g in json.loads((HERE / 'guides.json').read_text())}
    sheets = json.loads((HERE / 'worksheets.json').read_text())
    for guide in guides.values():
        render(guide, catalog, Path(sys.argv[1]), guides, sheets[guide['host']])
