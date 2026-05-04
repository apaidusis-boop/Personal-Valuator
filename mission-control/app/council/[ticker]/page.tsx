import Link from "next/link";
import fs from "fs";
import path from "path";
import { readCouncilStory } from "@/lib/vault";
import { DOSSIERS_DIR } from "@/lib/paths";
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
      <div className="p-8 space-y-4">
        <Link href="/council" className="text-[10px] font-mono text-zinc-500 hover:text-cyan-300">
          ← Council
        </Link>
        <h1 className="text-2xl text-zinc-100">{tk}</h1>
        <p className="text-zinc-500">
          Sem dossier do Council para este ticker. Corre{" "}
          <code className="text-cyan-300">python -m agents.council.story {tk}</code>.
        </p>
      </div>
    );
  }

  const { entry, body, council_md } = data;
  const archive = listArchive(tk);

  return (
    <div className="p-8 space-y-6 max-w-5xl">
      <header className="border-b border-[#1f1f3d] pb-4">
        <div className="flex items-center justify-between">
          <Link href="/council" className="text-[10px] font-mono text-zinc-500 hover:text-cyan-300">
            ← Council index
          </Link>
          <Link
            href={`/ticker/${tk}`}
            className="text-[10px] font-mono text-zinc-500 hover:text-cyan-300"
          >
            ticker page →
          </Link>
        </div>
        <div className="flex items-end justify-between mt-2">
          <div>
            <h1 className="text-3xl font-light text-zinc-100">
              <span className="text-cyan-300 font-mono">{tk}</span>
              <span className="ml-3 text-base text-zinc-400">
                {entry.market.toUpperCase()}{entry.modo && ` · Modo ${entry.modo}`}
                {entry.sector && ` · ${entry.sector}`}
              </span>
            </h1>
            <div className="text-xs font-mono text-zinc-500 mt-1">
              {entry.date}
              {entry.elapsed_sec ? ` · ${entry.elapsed_sec.toFixed(1)}s` : ""}
              {entry.is_holding && <span className="text-purple-300 ml-2">· holding</span>}
            </div>
          </div>
          <StancePill stance={entry.stance} confidence={entry.confidence} size="lg" />
        </div>
      </header>

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
