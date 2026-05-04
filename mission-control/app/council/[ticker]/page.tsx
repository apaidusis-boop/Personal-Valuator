import Link from "next/link";
import fs from "fs";
import path from "path";
import { readCouncilStory } from "@/lib/vault";
import { DOSSIERS_DIR } from "@/lib/paths";
import { formatDate } from "@/lib/format";
import { PageHeader, Pill, EmptyState, pillVariantFromMarket } from "@/components/ui";
import StancePill from "@/components/stance-pill";
import Markdown from "@/components/markdown";

export const dynamic = "force-dynamic";

function listArchive(ticker: string): { date: string; path: string }[] {
  const archive = path.join(DOSSIERS_DIR, "archive");
  if (!fs.existsSync(archive)) return [];
  let files: string[];
  try { files = fs.readdirSync(archive); } catch { return []; }
  return files
    .map((f) => f.match(new RegExp(`^${ticker}_STORY_(\\d{4}-\\d{2}-\\d{2})\\.md$`)))
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
      <div className="p-8 max-w-[1200px] space-y-6">
        <PageHeader
          title={tk}
          crumbs={[
            { label: "Home", href: "/" },
            { label: "Council", href: "/council" },
            { label: tk },
          ]}
        />
        <EmptyState
          icon="◯"
          title="Sem dossier do Council"
          description="Este ticker ainda não foi avaliado pelo Council. Aguarda o próximo overnight batch."
          action={
            <Link href={`/ticker/${tk}`} className="pill pill-glow">
              ver ticker page →
            </Link>
          }
        />
      </div>
    );
  }

  const { entry, body, council_md } = data;
  const archive = listArchive(tk);

  return (
    <div className="p-8 space-y-6 max-w-5xl">
      <PageHeader
        title={tk}
        subtitle={`${entry.sector || ""}${entry.modo ? ` · Modo ${entry.modo}` : ""}${entry.elapsed_sec ? ` · ${entry.elapsed_sec.toFixed(1)}s` : ""}`}
        crumbs={[
          { label: "Home", href: "/" },
          { label: "Council", href: "/council" },
          { label: tk },
        ]}
        freshness={entry.date}
        actions={
          <div className="flex items-center gap-2">
            <Pill variant={pillVariantFromMarket(entry.market)}>{entry.market.toUpperCase()}</Pill>
            {entry.is_holding && <Pill variant="purple">holding</Pill>}
            <StancePill stance={entry.stance} confidence={entry.confidence} size="lg" />
            <Link
              href={`/ticker/${tk}`}
              className="pill pill-glow"
            >
              ticker page →
            </Link>
          </div>
        }
      />

      {entry.synthesis && (
        <section className="card-purple p-5 rounded-lg space-y-4">
          <h2 className="text-sm font-mono uppercase tracking-wider text-purple-300">
            ⚖ Council synthesis
          </h2>

          {entry.synthesis.consensus_points.length > 0 && (
            <div>
              <h3 className="text-[10px] font-mono uppercase tracking-wider text-green-300 mb-1">
                Consensus
              </h3>
              <ul className="text-xs space-y-1 list-disc pl-5 marker:text-green-400 text-zinc-300">
                {entry.synthesis.consensus_points.map((p, i) => (
                  <li key={i}>{p}</li>
                ))}
              </ul>
            </div>
          )}

          {entry.synthesis.dissent_points.length > 0 && (
            <div>
              <h3 className="text-[10px] font-mono uppercase tracking-wider text-orange-300 mb-1">
                ◇ Dissent ({entry.synthesis.dissent_points.length})
              </h3>
              <ul className="text-xs space-y-1 list-disc pl-5 marker:text-orange-400 text-zinc-300">
                {entry.synthesis.dissent_points.map((p, i) => (
                  <li key={i}>{p}</li>
                ))}
              </ul>
            </div>
          )}

          {entry.synthesis.pre_publication_flags.length > 0 && (
            <div>
              <h3 className="text-[10px] font-mono uppercase tracking-wider text-red-300 mb-1">
                ⚑ Pre-publication flags ({entry.synthesis.pre_publication_flags.length})
              </h3>
              <ul className="text-xs space-y-1 list-disc pl-5 marker:text-red-400 text-zinc-300">
                {entry.synthesis.pre_publication_flags.map((p, i) => (
                  <li key={i}>{p}</li>
                ))}
              </ul>
            </div>
          )}

          {entry.synthesis.sizing_recommendation && (
            <div>
              <h3 className="text-[10px] font-mono uppercase tracking-wider text-cyan-300 mb-1">
                Sizing
              </h3>
              <p className="text-xs text-zinc-300">{entry.synthesis.sizing_recommendation}</p>
            </div>
          )}

          {entry.seats.length > 0 && (
            <div>
              <h3 className="text-[10px] font-mono uppercase tracking-wider text-zinc-400 mb-1">
                Seats convocados
              </h3>
              <div className="flex flex-wrap gap-1.5">
                {entry.seats.map((s) => (
                  <span
                    key={s}
                    className="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-900/60 border border-[#1f1f3d] text-zinc-300"
                  >
                    {s}
                  </span>
                ))}
              </div>
            </div>
          )}
        </section>
      )}

      <section className="card p-6 rounded-lg">
        <h2 className="text-sm font-mono uppercase tracking-wider text-purple-300 mb-4">
          ✎ Storytelling
        </h2>
        <Markdown source={body} />
      </section>

      {council_md && (
        <details className="card p-5 rounded-lg">
          <summary className="text-sm font-mono uppercase tracking-wider text-zinc-400 cursor-pointer hover:text-cyan-300">
            ▾ Council transcript
          </summary>
          <div className="mt-4">
            <Markdown source={council_md} />
          </div>
        </details>
      )}

      {archive.length > 0 && (
        <section className="card p-4 rounded-lg">
          <h3 className="text-[10px] font-mono uppercase tracking-wider text-zinc-500 mb-2">
            Archive ({archive.length})
          </h3>
          <ul className="text-xs font-mono text-zinc-500 space-y-0.5">
            {archive.map((a) => (
              <li key={a.path}>
                {a.date}{" "}
                <span className="text-zinc-700">— {a.path.split(/[\\/]/).slice(-2).join("/")}</span>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
