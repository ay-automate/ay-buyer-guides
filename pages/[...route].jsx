import fs from "node:fs";
import Head from "next/head";
import Home from "../components/Home";
import { Worksheet, Decision } from "../components/Reading";
import { guides, guideData } from "../lib/guides.mjs";
import links from "../lib/related.json";

export const config = { unstable_runtimeJS: false };

export function getStaticPaths() {
  const paths = guides.flatMap((g) =>
    [[], ["worksheet"], [guideData(g).article.slug]].map((parts) => ({
      params: { route: [g.host, ...parts] },
    })),
  );
  return { paths, fallback: false };
}
export function getStaticProps({ params }) {
  const [host, slug = ""] = params.route,
    g = guides.find((item) => item.host === host);
  return {
    props: {
      ...guideData(g),
      slug,
      style: fs.readFileSync("guide.css", "utf8"),
      related: links[host].map((host) =>
        guides.find((item) => item.host === host),
      ),
    },
  };
}
export default function Guide(props) {
  const { g, slug, base, data, article, sheet, style } = props;
  const page = slug === "worksheet" ? sheet : article,
    title = slug ? page.title : g.title + " | 2026 buyer guide",
    desc = slug ? page.summary : g.intro,
    url = base + (slug ? slug + "/" : "");
  const schemas = [
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      name: g.name,
      ...(g.shortName ? { alternateName: g.shortName } : {}),
      url: base,
    },
  ];
  if (g.review_questions)
    schemas.push({
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      url: base,
      name: g.title,
      description: g.intro,
      publisher: {
        "@type": "Organization",
        name: data.publisher,
        url: "https://www.ayautomate.com/",
      },
      mainEntity: {
        "@type": "ItemList",
        itemListOrder: "https://schema.org/ItemListUnordered",
        numberOfItems: data.firms.length,
        itemListElement: data.firms.map((f, i) => ({
          "@type": "ListItem",
          position: i + 1,
          name: f.name,
          url: f.profile,
        })),
      },
    });
  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="description" content={desc} />
        <link rel="canonical" href={url} />
        <link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48" />
        <link rel="icon" href="/favicon.png" sizes="192x192" type="image/png" />
        <link rel="apple-touch-icon" href="/favicon.png" />
        {Object.entries({
          title,
          description: desc,
          url,
          site_name: g.name,
          type: "website",
        }).map(([k, v]) => (
          <meta key={k} property={"og:" + k} content={v} />
        ))}
        <style
          dangerouslySetInnerHTML={{
            __html: ":root{--ink:" + g.color + "}" + style,
          }}
        />
        {!slug &&
          schemas.map((s) => (
            <script
              key={s["@type"]}
              type="application/ld+json"
              dangerouslySetInnerHTML={{
                __html: JSON.stringify(s).replace(/</g, "\\u003c"),
              }}
            />
          ))}
      </Head>
      <a className="skip" href="#main">
        Skip to content
      </a>
      <header>
        <a className="brand" href="/">
          <img src="/favicon.png" alt="" width="35" height="35" />
          {g.name}
        </a>
        <nav aria-label="Primary">
          <a href="/#directory">Directory</a>
          <a href="/worksheet/">Worksheet</a>
          <a href="/#agent-access">For AI assistants</a>
        </nav>
      </header>
      <main id="main">
        {!slug ? (
          <Home {...props} />
        ) : slug === "worksheet" ? (
          <Worksheet {...props} />
        ) : (
          <Decision {...props} />
        )}
      </main>
      <footer>
        <a href="/">{g.name}</a> ·{" "}
        <a href="/#editorial">
          Submissions and corrections
        </a>
      </footer>
    </>
  );
}
