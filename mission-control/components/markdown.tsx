// Minimal markdown→React renderer.
// Handles the subset used in dossier outputs: headings, paragraphs, lists,
// tables (pipe syntax), blockquotes, hr, bold/italic/code/links and Obsidian
// wikilinks ([[name]]). Inline parsing uses a forward scanner rather than
// regex sentinels — robust against arbitrary content.
import React from "react";

type Block =
  | { kind: "h"; level: 1 | 2 | 3 | 4; text: string }
  | { kind: "p"; text: string }
  | { kind: "ul"; items: string[] }
  | { kind: "ol"; items: string[] }
  | { kind: "quote"; text: string }
  | { kind: "table"; head: string[]; rows: string[][] }
  | { kind: "hr" }
  | { kind: "code"; text: string };

function parseBlocks(md: string): Block[] {
  const lines = md.split(/\r?\n/);
  const out: Block[] = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) { i++; continue; }

    if (/^\s*---+\s*$/.test(line)) { out.push({ kind: "hr" }); i++; continue; }

    const h = line.match(/^(#{1,4})\s+(.*)$/);
    if (h) {
      out.push({ kind: "h", level: h[1].length as 1 | 2 | 3 | 4, text: h[2].trim() });
      i++;
      continue;
    }

    if (/^\s*```/.test(line)) {
      const buf: string[] = [];
      i++;
      while (i < lines.length && !/^\s*```/.test(lines[i])) { buf.push(lines[i]); i++; }
      i++;
      out.push({ kind: "code", text: buf.join("\n") });
      continue;
    }

    // table — current line has pipes, next line is separator
    if (
      line.includes("|") &&
      i + 1 < lines.length &&
      /^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$/.test(lines[i + 1])
    ) {
      const head = splitRow(line);
      i += 2;
      const rows: string[][] = [];
      while (i < lines.length && lines[i].includes("|") && lines[i].trim()) {
        rows.push(splitRow(lines[i]));
        i++;
      }
      out.push({ kind: "table", head, rows });
      continue;
    }

    if (/^\s*>\s?/.test(line)) {
      const buf: string[] = [];
      while (i < lines.length && /^\s*>\s?/.test(lines[i])) {
        buf.push(lines[i].replace(/^\s*>\s?/, ""));
        i++;
      }
      out.push({ kind: "quote", text: buf.join(" ") });
      continue;
    }

    if (/^\s*[-*]\s+/.test(line)) {
      const items: string[] = [];
      while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) {
        items.push(lines[i].replace(/^\s*[-*]\s+/, ""));
        i++;
      }
      out.push({ kind: "ul", items });
      continue;
    }

    if (/^\s*\d+\.\s+/.test(line)) {
      const items: string[] = [];
      while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) {
        items.push(lines[i].replace(/^\s*\d+\.\s+/, ""));
        i++;
      }
      out.push({ kind: "ol", items });
      continue;
    }

    const buf: string[] = [line];
    i++;
    while (
      i < lines.length &&
      lines[i].trim() &&
      !/^(#{1,4}\s|\s*---+\s*$|\s*[-*]\s+|\s*\d+\.\s+|\s*>\s?|```)/.test(lines[i]) &&
      !lines[i].includes("|")
    ) {
      buf.push(lines[i]);
      i++;
    }
    out.push({ kind: "p", text: buf.join(" ") });
  }
  return out;
}

function splitRow(line: string): string[] {
  return line
    .replace(/^\s*\|/, "")
    .replace(/\|\s*$/, "")
    .split("|")
    .map((c) => c.trim());
}

// Inline scanner. Walks the string forward and emits typed tokens.
type InlineTok =
  | { t: "txt"; s: string }
  | { t: "b"; s: string }
  | { t: "i"; s: string }
  | { t: "code"; s: string }
  | { t: "wiki"; s: string }
  | { t: "link"; s: string; href: string };

function scanInline(text: string): InlineTok[] {
  const out: InlineTok[] = [];
  let buf = "";
  const flush = () => { if (buf) { out.push({ t: "txt", s: buf }); buf = ""; } };
  let i = 0;
  while (i < text.length) {
    const c = text[i];

    // inline code
    if (c === "`") {
      const close = text.indexOf("`", i + 1);
      if (close > i) {
        flush();
        out.push({ t: "code", s: text.slice(i + 1, close) });
        i = close + 1;
        continue;
      }
    }

    // wikilink [[label]]
    if (c === "[" && text[i + 1] === "[") {
      const close = text.indexOf("]]", i + 2);
      if (close > i) {
        flush();
        const label = text.slice(i + 2, close);
        out.push({ t: "wiki", s: label });
        i = close + 2;
        continue;
      }
    }

    // markdown link [label](url)
    if (c === "[") {
      const closeB = text.indexOf("]", i + 1);
      if (closeB > i && text[closeB + 1] === "(") {
        const closeP = text.indexOf(")", closeB + 2);
        if (closeP > closeB) {
          flush();
          out.push({
            t: "link",
            s: text.slice(i + 1, closeB),
            href: text.slice(closeB + 2, closeP),
          });
          i = closeP + 1;
          continue;
        }
      }
    }

    // bold **text**
    if (c === "*" && text[i + 1] === "*") {
      const close = text.indexOf("**", i + 2);
      if (close > i + 2) {
        flush();
        out.push({ t: "b", s: text.slice(i + 2, close) });
        i = close + 2;
        continue;
      }
    }

    // italic *text* — single asterisk, not adjacent to another
    if (c === "*" && text[i + 1] !== "*" && text[i - 1] !== "*") {
      const close = text.indexOf("*", i + 1);
      // next char before close should not be '*' (would be malformed)
      if (close > i + 1 && text[close + 1] !== "*" && !text.slice(i + 1, close).includes("\n")) {
        flush();
        out.push({ t: "i", s: text.slice(i + 1, close) });
        i = close + 1;
        continue;
      }
    }

    buf += c;
    i++;
  }
  flush();
  return out;
}

function inline(text: string, keyPrefix: string): React.ReactNode[] {
  return scanInline(text).map((tok, idx) => {
    const k = `${keyPrefix}-${idx}`;
    switch (tok.t) {
      case "txt":
        return <React.Fragment key={k}>{tok.s}</React.Fragment>;
      case "b":
        return <strong key={k} className="text-zinc-100">{tok.s}</strong>;
      case "i":
        return <em key={k} className="text-zinc-300">{tok.s}</em>;
      case "code":
        return (
          <code key={k} className="px-1 py-0.5 rounded bg-purple-900/20 text-cyan-200 font-mono text-[12px]">
            {tok.s}
          </code>
        );
      case "wiki":
        return (
          <span key={k} className="text-purple-300 underline decoration-dotted underline-offset-2">
            {tok.s.split("|").pop()}
          </span>
        );
      case "link":
        return (
          <a
            key={k}
            href={tok.href}
            target="_blank"
            rel="noopener noreferrer"
            className="text-cyan-300 underline decoration-dotted underline-offset-2 hover:text-cyan-200"
          >
            {tok.s}
          </a>
        );
    }
  });
}

export default function Markdown({ source }: { source: string }) {
  const blocks = parseBlocks(source);
  return (
    <div className="markdown space-y-3 text-[14px] leading-relaxed text-zinc-300">
      {blocks.map((b, i) => {
        const k = `b-${i}`;
        if (b.kind === "hr") return <hr key={k} className="border-[#1f1f3d]" />;
        if (b.kind === "h") {
          const sizes = {
            1: "text-2xl font-light text-zinc-100 mt-6 mb-3",
            2: "text-lg font-mono uppercase tracking-wider text-purple-300 mt-5 mb-2",
            3: "text-sm font-mono uppercase tracking-wider text-cyan-300 mt-4 mb-1",
            4: "text-xs font-mono uppercase tracking-wider text-zinc-400 mt-3 mb-1",
          } as const;
          const Tag = (`h${b.level}` as "h1" | "h2" | "h3" | "h4");
          return React.createElement(Tag, { key: k, className: sizes[b.level] }, inline(b.text, k));
        }
        if (b.kind === "p") return <p key={k}>{inline(b.text, k)}</p>;
        if (b.kind === "ul")
          return (
            <ul key={k} className="list-disc pl-5 space-y-1.5 marker:text-purple-400">
              {b.items.map((it, j) => <li key={`${k}-${j}`}>{inline(it, `${k}-${j}`)}</li>)}
            </ul>
          );
        if (b.kind === "ol")
          return (
            <ol key={k} className="list-decimal pl-5 space-y-1.5 marker:text-purple-400">
              {b.items.map((it, j) => <li key={`${k}-${j}`}>{inline(it, `${k}-${j}`)}</li>)}
            </ol>
          );
        if (b.kind === "quote")
          return (
            <blockquote
              key={k}
              className="border-l-4 border-purple-700/50 pl-4 italic text-zinc-300 bg-purple-900/5 py-2"
            >
              {inline(b.text, k)}
            </blockquote>
          );
        if (b.kind === "code")
          return (
            <pre key={k} className="bg-[#0a0a1f] border border-[#1f1f3d] rounded p-3 text-[12px] font-mono text-zinc-300 overflow-x-auto">
              {b.text}
            </pre>
          );
        // table
        return (
          <div key={k} className="overflow-x-auto">
            <table className="text-xs font-mono w-full border border-[#1f1f3d]">
              <thead>
                <tr className="bg-purple-900/10 text-purple-300">
                  {b.head.map((h, j) => (
                    <th key={`${k}-h-${j}`} className="px-2 py-1.5 text-left border-b border-[#1f1f3d]">
                      {inline(h, `${k}-h-${j}`)}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {b.rows.map((row, ri) => (
                  <tr key={`${k}-r-${ri}`} className="border-b border-[#1f1f3d]/50">
                    {row.map((c, ci) => (
                      <td key={`${k}-r-${ri}-c-${ci}`} className="px-2 py-1.5 text-zinc-300">
                        {inline(c, `${k}-r-${ri}-c-${ci}`)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
      })}
    </div>
  );
}
