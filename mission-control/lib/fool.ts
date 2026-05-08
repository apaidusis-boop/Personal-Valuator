// Server-safe parser for Fool.com-style dossier sections.
// The renderer is in components/fool-dossier.tsx (client component).

export type FoolFields = {
  foolish_thesis: string[];
  what_company_does: string | null;
  why_buy: string | null;
  what_could_go_wrong: string | null;
  bottom_line: string | null;
  portfolio_fit: string | null;
  who_else_to_watch: string | null;
  what_team_thinks: string | null;
  investing_type: string | null;
  est_annualized_return: string | null;
  est_max_drawdown: string | null;
};

const FIELD_HEADERS: { field: keyof FoolFields; aliases: string[] }[] = [
  { field: "foolish_thesis", aliases: ["foolish thesis", "tese", "tese central", "thesis", "thesis bullets"] },
  { field: "what_company_does", aliases: ["what does", "what x does", "o que faz", "o que a empresa faz", "company overview", "negócio"] },
  { field: "why_buy", aliases: ["why it's a buy", "why buy", "porque comprar", "porque é buy", "bull case"] },
  { field: "what_could_go_wrong", aliases: ["what could go wrong", "riscos", "bear case", "o que pode dar errado", "risks"] },
  { field: "bottom_line", aliases: ["bottom line", "linha final", "veredicto", "verdict", "conclusion", "conclusão"] },
  { field: "portfolio_fit", aliases: ["portfolio fit", "encaixe na carteira", "sizing", "fit"] },
  { field: "who_else_to_watch", aliases: ["who else to watch", "peers", "concorrentes", "competitors", "outros para observar"] },
  { field: "what_team_thinks", aliases: ["what our team thinks", "o que pensamos", "team view", "council view", "synthesis"] },
];

function normalize(h: string): string {
  return h
    .toLowerCase()
    .replace(/^[#\s_•·*-]+/, "")
    .replace(/[#\s_•·*-]+$/, "")
    .trim();
}

function findField(heading: string): keyof FoolFields | null {
  const norm = normalize(heading);
  for (const { field, aliases } of FIELD_HEADERS) {
    if (aliases.some((a) => norm === a || norm.startsWith(a + " ") || norm.startsWith(a + ":"))) {
      return field;
    }
  }
  return null;
}

export function parseDossierToFool(body: string): FoolFields {
  const lines = body.split(/\r?\n/);
  const sections: Partial<Record<keyof FoolFields, string[]>> = {};
  let currentField: keyof FoolFields | null = null;

  for (const raw of lines) {
    const line = raw.trimEnd();
    const headingMatch = line.match(/^(#{1,4})\s+(.+)$/);
    if (headingMatch) {
      currentField = findField(headingMatch[2]);
      continue;
    }
    if (currentField) {
      if (!sections[currentField]) sections[currentField] = [];
      sections[currentField]!.push(line);
    }
  }

  function joinText(lines: string[] | undefined): string | null {
    if (!lines) return null;
    const text = lines.join("\n").trim();
    return text || null;
  }

  function extractBullets(lines: string[] | undefined): string[] {
    if (!lines) return [];
    const out: string[] = [];
    for (const l of lines) {
      const m = l.match(/^\s*[-*•]\s+(.+)$/);
      if (m) out.push(m[1].trim());
    }
    return out;
  }

  function findInline(label: string): string | null {
    const re = new RegExp(`(?:^|\\n)\\s*[-*]?\\s*\\*?\\*?${label}\\*?\\*?\\s*[:\\-—]\\s*([^\\n]+)`, "i");
    const m = body.match(re);
    return m ? m[1].trim().replace(/[*_`]+$/g, "") : null;
  }

  return {
    foolish_thesis: extractBullets(sections.foolish_thesis),
    what_company_does: joinText(sections.what_company_does),
    why_buy: joinText(sections.why_buy),
    what_could_go_wrong: joinText(sections.what_could_go_wrong),
    bottom_line: joinText(sections.bottom_line),
    portfolio_fit: joinText(sections.portfolio_fit),
    who_else_to_watch: joinText(sections.who_else_to_watch),
    what_team_thinks: joinText(sections.what_team_thinks),
    investing_type:
      findInline("investing type") ||
      findInline("tipo de investimento") ||
      findInline("type"),
    est_annualized_return:
      findInline("est\\.? annualized return") ||
      findInline("annualized return") ||
      findInline("retorno anualizado est"),
    est_max_drawdown:
      findInline("est\\.? max drawdown") ||
      findInline("max drawdown") ||
      findInline("drawdown máximo"),
  };
}
