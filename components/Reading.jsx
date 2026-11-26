export function Hero({ field, label, title, intro, action }) {
  return (
    <section className="hero">
      <div>
        <p className="meta">{label}</p>
        <h1>{title}</h1>
        <p className="intro">{intro}</p>
        {action && (
          <a className="button" href={action[0]}>
            {action[1]} →
          </a>
        )}
      </div>
      <aside className="board">
        <h2>{field.board}</h2>
        <ol>
          {field.stages.map(([s, d]) => (
            <li key={s}>
              <b>{s}</b>
              <span>{d}</span>
            </li>
          ))}
        </ol>
      </aside>
    </section>
  );
}
function Table({ title, columns, rows }) {
  return (
    <table>
      <caption>{title}</caption>
      <thead>
        <tr>
          {columns.map((v) => (
            <th key={v} scope="col">
              {v}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map(([label, ...values]) => (
          <tr key={label}>
            <th scope="row">{label}</th>
            {values.map((v, i) => (
              <td key={i}>{v}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
function Reading({ toc, children }) {
  return (
    <div className="reading">
      <aside>
        <p className="reading-label">On this page</p>
        <nav aria-label="On this page">
          {toc.map(([id, title]) => (
            <a key={id} href={"#" + id}>
              {title}
            </a>
          ))}
        </nav>
      </aside>
      <article>{children}</article>
    </div>
  );
}
export function Worksheet({ sheet: s, field: f, article: a }) {
  return (
    <>
      <Hero
        field={f}
        label="Buyer worksheet"
        title={s.title}
        intro={s.summary}
        action={["#record", "Fill out the decision record"]}
      />
      <Reading
        toc={Object.entries({
          scenario: "Worked example",
          worksheet: "Worksheet",
          record: "Your decision record",
          next: "Next decision",
        })}
      >
        <section id="scenario">
          <h2>Worked example</h2>
          <p>{s.example}</p>
        </section>
        <section id="worksheet">
          <Table title="Worksheet" {...s} />
        </section>
        <section id="record">
          <h2>Your decision record</h2>
          <p>
            Type in the fields below or print a blank copy. Use your browser’s
            Print or Save as PDF before closing the page. Entries stay in this
            open tab.
          </p>
          {f.record.map((v, i) => (
            <div key={v}>
              <p id={"prompt-" + (i + 1)} className="prompt">
                {v}
              </p>
              <div
                className="write-in"
                contentEditable="plaintext-only"
                role="textbox"
                aria-multiline="true"
                aria-labelledby={"prompt-" + (i + 1)}
              />
            </div>
          ))}
          <p>
            <label>
              <input type="checkbox" />
              Evidence reviewed with the responsible owner
            </label>
          </p>
        </section>
        <section className="example" id="next">
          <h2>{s.close_title}</h2>
          <p>{s.close}</p>
          <p>{f.next}</p>
          <a href={"/" + a.slug + "/"}>{a.title}</a>
        </section>
      </Reading>
    </>
  );
}
export function Decision({ article: a, field: f, extra, supplement }) {
  const steps = a.sections.map(([title], i) => ["step-" + (i + 1), title]);
  return (
    <>
      <Hero
        field={f}
        label="Decision guide"
        title={a.title}
        intro={a.opening}
      />
      <Reading
        toc={[
          ...(supplement ? [supplement] : []),
          ...steps,
          ["decision-table", "Decision table"],
          ["rehearsal", "Worked buyer scenario"],
          ["decision", "Make the decision"],
        ]}
      >
        {extra && <div dangerouslySetInnerHTML={{ __html: extra }} />}
        {a.sections.map(([h, p], i) => (
          <section key={h} id={steps[i][0]}>
            <h2>{h}</h2>
            <p>{p}</p>
          </section>
        ))}
        <section id="decision-table">
          <Table title="Decision table" {...a} />
        </section>
        <section id="rehearsal">
          <p className="meta">Illustrative buyer scenario</p>
          <h2>{f.headline}</h2>
          <p>{f.scenario}</p>
          <p>{f.test}</p>
          <div className="fieldnotes">
            <div>
              <h3>What to keep</h3>
              <p>{f.evidence}</p>
            </div>
            <div>
              <h3>When to pause</h3>
              <p>{f.hold}</p>
            </div>
          </div>
        </section>
        <section className="example" id="decision">
          <h2>Make the decision</h2>
          <p>{a.decision}</p>
          <a className="button" href="/worksheet/">
            Open the buyer worksheet →
          </a>
        </section>
        <section>
          <h2>Further reading</h2>
          <a href={a.url}>{a.source}</a>
        </section>
      </Reading>
    </>
  );
}
