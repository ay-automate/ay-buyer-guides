import fs from "node:fs";
const json = (name) => JSON.parse(fs.readFileSync(name + ".json", "utf8"));
export const guides = json("guides");
const sheets = json("worksheets"),
  decisions = json("decisions"),
  fields = json("fieldwork"),
  picks = json("picks");
const providers = Object.fromEntries(
  fs
    .readFileSync("catalog.tsv", "utf8")
    .trimEnd()
    .split("\n")
    .map((row) => {
      const [id, name, specialty, note, source] = row.split("\t");
      return [id, { id, name, specialty, note, source }];
    }),
);
const supplements = {
  "ai-rfp-template": [
    "compare-finalists",
    "Compare two finalist bids",
    "finalist-comparison",
  ],
  "ai-vendor-security-questionnaire": [
    "file-expiry",
    "Review a file expiry decision",
    "file-expiry",
  ],
  "ai-consulting-pricing": [
    "published-scopes",
    "Compare two published scopes",
    "scope-comparison",
  ],
  "ai-agent-evaluation": ["trial", "Run the four test cases", "agent-trial"],
};
export function guideData(g) {
  const base = "https://" + g.host + "/",
    article = decisions[g.host],
    selection = picks[g.host];
  const firms = g.providers.split(/\s+/).map((id) => {
    const firm = providers[id];
    let note = firm.note;
    if (g.review_questions?.[id])
      note =
        note.split(". ")[0].replace(/\.$/, "") + ". " + g.review_questions[id];
    if (id === "ay") note += " This provider publishes the guide.";
    return { ...firm, note, profile: base + "#firm-" + id };
  });
  const matched = new Set(Object.values(g.matching.needs).flat());
  if (matched.size !== firms.length || firms.some((f) => !matched.has(f.id)))
    throw Error("Invalid matching groups: " + g.host);
  const data = {
    picks: selection.picks,
    guide: g.name,
    publisher: "AY Automate",
    methodology: g.criteria,
    editorial_policy: base + "#editorial",
    commercial_relationship: "The publisher sells AI implementation services.",
    questions: g.checklist,
    pricing: g.price,
    firms,
  };
  const supplement = supplements[article.slug];
  let extra = "";
  if (supplement) {
    extra = fs.readFileSync(supplement[2] + ".html", "utf8");
    if (supplement[2] === "agent-trial")
      extra = extra.replace(
        "{downloads}",
        ["cases.json", "observed.json", "reference.json", "score.py"]
          .map(
            (n) =>
              '<li><a download="' +
              n +
              '" href="data:application/octet-stream;base64,' +
              fs.readFileSync("agent-trial/" + n).toString("base64") +
              '">' +
              n +
              "</a></li>",
          )
          .join(""),
      );
  }
  return {
    g,
    base,
    data,
    selection,
    article,
    sheet: sheets[g.host],
    field: fields[g.host],
    supplement: supplement || null,
    extra,
  };
}
