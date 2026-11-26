import { Hero } from "./Reading";
function Editorial({ g }) {
  const tracker = "https://github.com/ay-automate/ay-buyer-guides/issues";
  const link = (request) =>
    tracker +
    "/new?" +
    new URLSearchParams({
      title: request + " for " + g.name,
      body:
        "Guide: " +
        g.host +
        "\nProvider or page URL:\nProposed addition or change:\nPublic source supporting it:\nYour connection to the provider:",
    });
  return (
    <section id="editorial">
      <h2>Submissions and corrections</h2>
      <p>Published by AY Automate.</p>
      <p>
        Any provider or reader can propose an addition or correction. Include a
        public source and disclose your connection to the provider. Requests
        open on GitHub and are public.
      </p>
      <p>
        <a href={link("Provider submission")}>{g.shortName === "TAA" ? "Submit an agency" : "Submit a provider"}</a> ·{" "}
        <a href={link("Editorial correction")}>Request a correction</a> ·{" "}
        <a href={tracker + "?q=is%3Aissue"}>View editorial requests</a>
      </p>
    </section>
  );
}
export default function Home({
  g,
  field,
  article,
  sheet,
  base,
  data,
  selection,
  related,
}) {
  const firms = Object.fromEntries(data.firms.map((f) => [f.id, f]));
  return (
    <>
      <Hero
        field={field}
        label={field.label + " / 2026 buyer guide"}
        title={g.title}
        intro={g.intro}
        action={[g.actionTarget, g.actionLabel]}
      />
      <section id="shortlist">
        <h2>{selection.title}</h2>
        <p>{selection.intro}</p>
        <p>
          We chose these examples for the specific work documented in a client
          case or product guide. Client outcomes are provider-reported.
        </p>
        <img
          src="/shortlist.png"
          width="1056"
          height="370"
          style={{ maxWidth: "100%", height: "auto" }}
          alt="Project needs and their shortlisted providers, detailed below"
          loading="lazy"
        />
        <ol>
          {selection.picks.map((p) => (
            <li key={p.id}>
              <h3>
                {firms[p.id].name} · {p.fit}
              </h3>
              <p>{p.detail}</p>
              <a href={p.source}>Read the source from {firms[p.id].name}</a>
            </li>
          ))}
        </ol>
      </section>
      <section className="guidance">
        <h2>What to ask before you buy</h2>
        <ol>
          {g.checklist.map((s) => (
            <li key={s}>{s}</li>
          ))}
        </ol>
      </section>
      <section>
        <h2>Buyer resources</h2>
        <div className="resources">
          {[
            [sheet, "/worksheet/", "Working document"],
            [article, "/" + article.slug + "/", "Decision guide"],
          ].map(([r, url, label]) => (
            <a key={url} className="resource" href={url}>
              <span className="card-label">{label}</span>
              <h3>{r.title}</h3>
              <p>{r.summary}</p>
            </a>
          ))}
        </div>
      </section>
      <section id="match" className="guidance">
        <h2>{g.matching.title}</h2>
        <p>
          Choose what you need. Open a profile to see the provider’s specialty
          and the source behind its listing.
        </p>
        {Object.entries(g.matching.needs).map(([need, ids]) => (
          <details key={need}>
            <summary>{need}</summary>
            <ul>
              {ids
                .map((id) => firms[id])
                .sort((a, b) => a.name.localeCompare(b.name))
                .map((f) => (
                  <li key={f.id}>
                    <a href={"#firm-" + f.id}>{f.name}</a> · {f.specialty}
                  </li>
                ))}
            </ul>
          </details>
        ))}
      </section>
      <section id="directory">
        <h2>Directory</h2>
        <p className="method">{g.criteria}</p>
        <p className="footnote">
          Entries link to provider materials. The guide gives no numerical
          ratings.
        </p>
        <div className="grid">
          {data.firms.map((f) => (
            <article key={f.id} className="entry" id={"firm-" + f.id}>
              <p className="tag">{f.specialty}</p>
              <h3>{f.name}</h3>
              <p>{f.note}</p>
              <a href={f.source}>Source from {f.name}</a>
            </article>
          ))}
        </div>
      </section>
      <section id="pricing">
        <h2>How to compare prices</h2>
        <p>{g.price}</p>
      </section>
      <section>
        <h2>A worked example to review</h2>
        <p>{g.case}</p>
        <a href={g.source}>Read the provider’s example</a>
      </section>
      <section id="faq">
        <h2>{g.faq}</h2>
        <p>{g.answer}</p>
      </section>
      <section id="agent-access">
        <h2>Compare these providers in your AI assistant</h2>
        <p>
          Add a remote MCP server using Streamable HTTP. Paste the URL below
          into your client. No API key is required.
        </p>
        <p>
          <code>{base}mcp</code>
        </p>
        <p>
          Try “
          {selection.agent_example ||
            "Which provider fits my project, and what evidence supports that choice?"}
          ”
        </p>
        <a href="/firms.json">Download the directory as JSON</a> ·{" "}
        <a href="/.well-known/mcp.json">
          View MCP connection details
        </a>
      </section>
      <Editorial g={g} />
      <section>
        <h2>Related buyer guides</h2>
        <ul>
          {related.map((r) => (
            <li key={r.host}>
              <a href={"https://" + r.host + "/"}>{r.title}</a>
            </li>
          ))}
        </ul>
      </section>
    </>
  );
}
