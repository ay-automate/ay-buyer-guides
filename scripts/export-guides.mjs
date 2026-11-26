import fs from "node:fs";
import path from "node:path";
import { guides, guideData } from "../lib/guides.mjs";
const keys = fs.existsSync("indexnow-keys.json")
  ? JSON.parse(fs.readFileSync("indexnow-keys.json"))
  : {};
for (const g of guides) {
  const { base, article, sheet, data } = guideData(g);
  const dest = path.join("dist", g.host);
  fs.mkdirSync(dest, { recursive: true });
  for (const route of ["", "worksheet", article.slug]) {
    const file = path.join(g.host, route, "index.html");
    const html = fs.readFileSync(path.join("out", file), "utf8");
    if (
      !html.includes('href="' + base + (route ? route + "/" : "") + '"') ||
      !html.includes('id="__next"')
    )
      throw Error("Invalid Next export " + file);
    fs.mkdirSync(path.dirname(path.join("dist", file)), { recursive: true });
    fs.copyFileSync(path.join("out", file), path.join("dist", file));
  }
  for (const file of ["favicon.ico", "favicon.png"])
    fs.copyFileSync(path.join("icons", g.host, file), path.join(dest, file));
  fs.copyFileSync(
    "illustrations/" + g.host + ".png",
    path.join(dest, "shortlist.png"),
  );
  const write = (file, body) => fs.writeFileSync(path.join(dest, file), body);
  write("firms.json", JSON.stringify(data, null, 2) + "\n");
  if (keys[g.host]) write("indexnow.txt", keys[g.host] + "\n");
  write(
    "robots.txt",
    "User-agent: *\nAllow: /\nSitemap: " + base + "sitemap.xml\n",
  );
  write(
    "sitemap.xml",
    '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
      ["", article.slug + "/", "worksheet/"]
        .map((route) => "<url><loc>" + base + route + "</loc></url>")
        .join("") +
      "</urlset>\n",
  );
  write(
    "llms.txt",
    "# " +
      g.name +
      "\n\n> " +
      g.intro +
      "\n\nPublished by AY Automate, a seller of AI implementation services. [Editorial policy and corrections](" +
      base +
      "#editorial).\n\n## Guide\n- [" +
      g.title +
      "](" +
      base +
      ")\n- [" +
      sheet.title +
      "](" +
      base +
      "worksheet/)\n- [" +
      article.title +
      "](" +
      base +
      article.slug +
      "/)\n\n## Provider sources\n" +
      data.firms
        .map(
          (f) =>
            "- [" +
            f.name +
            "](" +
            f.source +
            "): " +
            f.specialty +
            ". " +
            f.note,
        )
        .join("\n") +
      "\n- [Remote MCP](" +
      base +
      "mcp): search_firms, compare_firms and recommend_providers.\n",
  );
}
