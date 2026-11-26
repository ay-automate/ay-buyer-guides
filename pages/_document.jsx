import { Html, Head, Main } from "next/document";
// These document-only guides work with scripting disabled on the production origin.
export default function Document() {
  return (
    <Html lang="en">
      <Head />
      <body>
        <Main />
      </body>
    </Html>
  );
}
