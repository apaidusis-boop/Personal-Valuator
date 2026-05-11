import type { Metadata } from "next";
import Link from "next/link";
import fs from "fs";
import path from "path";
import { readCouncilStory } from "@/lib/vault";
import { DOSSIERS_DIR } from "@/lib/paths";
import { Pill, pillVariantFromMarket } from "@/components/ui";
import StancePill from "@/components/stance-pill";
import Markdown from "@/components/markdown";
import { FoolDossier } from "@/components/fool-dossier";
import { parseDossierToFool } from "@/lib/fool";

export const dynamic = "force-dynamic";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ ticker: string }>;
}): Promise<Metadata> {
  const { ticker } = await params;
  return { title: `${ticker.toUpperCase()} · Council` };
}

function listArchive(ticker: string): { date: string; path: string }[] {
  const archive = path.join(DOSSIERS_DIR, "archive");
  if (!fs.existsSync(archive)) return [];
  let files: string[];
  try {
    files = fs.readdirSync(archive);
  } catch {
    return [];
  }
  return files
    .map((f) =>
      f.match(new RegExp(`^${ticker}_STORY_(\\d{4}-\\d{2}-\\d{2})\\.md$`))
    )
    .filter((m): m is RegExpMatchArray => Boolean(m))
    .map((m) => ({ date: m[1], path: path.join(archive, m[0]) }))
    .sort((a, b) => b.date.localeCompare(a.date));
}

export default async function CouncilTickerPage({
  params,
}: {
  params: Promise<{ ticker: string }>;
}) {
  const { ticker } = await params;
  const tk = ticker.toUpperCase();
  const data = readCouncilStory(tk);

  if (!data) {
    return (
      <div className="p-5 max-w-[1200px] space-y-5">
        <div>
          <h1
            className="font-display text-xl font-bold"
            style={{ color: "var(--text-primary)" }}
          >
            {tk}
          </h1>
          <p
            className="text-xs mt-0.5"
            style={{ color: "var(--text-tertiary)" }}
          >
            <Link
              href="/council"
              className="hover:underline"
              style={{ color: "var(--accent-glow)" }}
            >
              Council
            </Link>{" "}
            · {tk}
          </p>
        </div>
        <div
          className="p-12 rounded text-center space-y-3"
          style={{
            background: "var(--bg-elevated)",
            border: "1px solid var(--border-subtle)",
          }}
        >
          <p
            className="text-sm"
            style={{ color: "var(--text-secondary)" }}
          >
            Sem dossier do Council
          </p>
          <p
            className="text-xs italic"
            style={{ color: "var(--text-tertiary)" }}
          >
            Este ticker ainda não foi avaliado. Aguarda o próximo overnight batch.
          </p>
          <Link
            href={`/ticker/${tk}`}
            className="inline-block text-[10px] hover:underline"
            style={{ color: "var(--accent-glow)" }}
          >
            ver ticker page →
          </Link>
        </div>
      </div>
    );
  }

  const { entry, body, council_md } = data;
  const archive = listArchive(tk);

  return (
    <div className="p-5 space-y-5 max-w-5xl">
      {/* Header --------------------------------------------- */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-2 flex-wrap">
            <h1
              className="font-display text-2xl font-bold"
              style={{ color: "var(--text-primary)" }}
            >
              {tk}
            </h1>
            <Pill variant={pillVariantFromMarket(entry.market)}>
              {entry.market.toUpperCase()}
            </Pill>
            {entry.is_holding && <span className="pill pill-gold">HOLDING</span>}
          </div>
          <p
            className="text-xs mt-1"
            style={{ color: "var(--text-tertiary)" }}
          >
            <Link
              href="/council"
              className="hover:underline"
              style={{ color: "var(--accent-glow)" }}
            >
              Council
            </Link>{" "}
            · {entry.sector || "—"}
            {entry.modo ? ` · Modo ${entry.modo}` : ""}
            {entry.elapsed_sec
              ? ` · ${entry.elapsed_sec.toFixed(1)}s`
              : ""}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <StancePill
            stance={entry.stance}
            confidence={entry.confidence}
            size="lg"
          />
          <Link
            href={`/ticker/${tk}`}
            className="text-[10px] px-2 py-1 rounded uppercase tracking-wider font-semibold transition-colors"
            style={{
              color: "var(--accent-glow)",
              border: "1px solid var(--border-subtle)",
            }}
          >
            ticker page →
          </Link>
        </div>
      </div>

      {/* Synthesis ------------------------------------------- */}
      {entry.synthesis && (
        <section
          className="rounded p-5 space-y-4"
          style={{
            background: "var(--bg-elevated)",
            border: "1px solid var(--border-subtle)",
            borderTop: "2px solid var(--val-gold)",
          }}
        >
          <h2
            className="text-[10px] font-semibold tracking-wider uppercase"
            style={{ color: "var(--text-label)" }}
          >
            ⚖ Council synthesis
          </h2>

          {entry.synthesis.consensus_points.length > 0 && (
            <SynthesisBlock
              title="Consensus"
              count={entry.synthesis.consensus_points.length}
              color="var(--verdict-buy)"
              items={entry.synthesis.consensus_points}
            />
          )}

          {entry.synthesis.dissent_points.length > 0 && (
            <SynthesisBlock
              title="Dissent"
              count={entry.synthesis.dissent_points.length}
              color="var(--verdict-hold)"
              items={entry.synthesis.dissent_points}
              symbol="◇"
            />
          )}

          {entry.synthesis.pre_publication_flags.length > 0 && (
            <SynthesisBlock
              title="Pre-publication flags"
              count={entry.synthesis.pre_publication_flags.length}
              color="var(--verdict-avoid)"
              items={entry.synthesis.pre_publication_flags}
              symbol="⚑"
            />
          )}

          {entry.synthesis.sizing_recommendation && (
            <div>
              <h3
                className="text-[10px] font-semibold tracking-wider uppercase mb-1.5"
                style={{ color: "var(--accent-glow)" }}
              >
                Sizing
              </h3>
              <p
                className="text-xs"
                style={{ color: "var(--text-secondary)" }}
              >
                {entry.synthesis.sizing_recommendation}
              </p>
            </div>
          )}

          {entry.seats.length > 0 && (
            <div>
              <h3
                className="text-[10px] font-semibold tracking-wider uppercase mb-1.5"
                style={{ color: "var(--text-label)" }}
              >
                Seats convocados ({entry.seats.length})
              </h3>
              <div className="flex flex-wrap gap-1.5">
                {entry.seats.map((s) => (
                  <span
                    key={s}
                    className="text-[10px] font-data px-2 py-0.5 rounded"
                    style={{
                      background: "var(--bg-overlay)",
                      border: "1px solid var(--border-subtle)",
                      color: "var(--text-secondary)",
                    }}
                  >
                    {s}
                  </span>
                ))}
              </div>
            </div>
          )}
        </section>
      )}

      {/* Fool-style structured view (renders when sections detected) */}
      <FoolDossier
        ticker={tk}
        fields={parseDossierToFool(body)}
        stance={entry.stance}
      />

      {/* Storytelling — full transcript ----------------------- */}
      <details
        className="rounded p-6"
        style={{
          background: "var(--bg-elevated)",
          border: "1px solid var(--border-subtle)",
        }}
      >
        <summary
          className="type-h3 cursor-pointer hover:underline"
          style={{ marginBottom: 12 }}
        >
          ✎ Full storytelling transcript
        </summary>
        <div style={{ marginTop: 16 }}>
          <Markdown source={body} />
        </div>
      </details>

      {/* Council transcript --------------------------------- */}
      {council_md && (
        <details
          className="rounded p-5"
          style={{
            background: "var(--bg-elevated)",
            border: "1px solid var(--border-subtle)",
          }}
        >
          <summary
            className="text-[10px] font-semibold tracking-wider uppercase cursor-pointer hover:underline"
            style={{ color: "var(--text-tertiary)" }}
          >
            ▾ Council transcript
          </summary>
          <div className="mt-4">
            <Markdown source={council_md} />
          </div>
        </details>
      )}

      {/* Archive -------------------------------------------- */}
      {archive.length > 0 && (
        <section
          className="rounded p-4"
          style={{
            background: "var(--bg-elevated)",
            border: "1px solid var(--border-subtle)",
          }}
        >
          <h3
            className="text-[10px] font-semibold tracking-wider uppercase mb-2"
            style={{ color: "var(--text-label)" }}
          >
            Archive ({archive.length})
          </h3>
          <ul className="text-[11px] font-data space-y-0.5">
            {archive.map((a) => (
              <li
                key={a.path}
                style={{ color: "var(--text-tertiary)" }}
              >
                {a.date}{" "}
                <span style={{ color: "var(--text-disabled)" }}>
                  — {a.path.split(/[\\/]/).slice(-2).join("/")}
                </span>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}

function SynthesisBlock({
  title,
  count,
  color,
  items,
  symbol,
}: {
  title: string;
  count: number;
  color: string;
  items: string[];
  symbol?: string;
}) {
  return (
    <div>
      <h3
        className="text-[10px] font-semibold tracking-wider uppercase mb-1.5"
        style={{ color }}
      >
        {symbol ? `${symbol} ${title}` : title} ({count})
      </h3>
      <ul
        className="text-xs space-y-1 list-disc pl-5"
        style={{ color: "var(--text-secondary)" }}
      >
        {items.map((p, i) => (
          <li key={i}>{p}</li>
        ))}
      </ul>
    </div>
  );
}
