import { listDossiers, listDeepdiveJSON } from "@/lib/vault";

export const dynamic = "force-dynamic";

export default function DocsPage() {
  const dossiers = listDossiers(40);
  const deepdiveJsons = listDeepdiveJSON(20);

  return (
    <div className="p-8 space-y-6">
      <header className="border-b border-[#1f1f3d] pb-4">
        <h1 className="text-3xl font-light text-zinc-100">
          <span className="text-purple-400">≡</span> Docs
        </h1>
        <p className="text-xs font-mono text-zinc-500 mt-1">
          Dossiers (Obsidian) + raw deepdive JSON (reports/deepdive/).
        </p>
      </header>

      <section>
        <h2 className="text-sm font-mono uppercase tracking-wider text-purple-300 mb-3">
          Dossiers ({dossiers.length})
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {dossiers.map((d) => {
            const fm = d.data as Record<string, unknown>;
            const piotroski = fm.piotroski as number | undefined;
            const altman = fm.altman_z as number | undefined;
            const beneish = fm.beneish_m as number | undefined;
            const ticker = fm.ticker as string | undefined;
            return (
              <article
                key={d.path}
                className="card-cyan p-4 rounded-lg hover:border-cyan-400/50 transition-colors"
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-mono text-cyan-300 font-medium">{ticker || d.title}</h3>
                  <span className="text-[10px] font-mono text-zinc-500">
                    {new Date(d.modified).toISOString().slice(0, 10)}
                  </span>
                </div>
                {(piotroski !== undefined || altman !== undefined || beneish !== undefined) && (
                  <div className="grid grid-cols-3 gap-1 text-[10px] font-mono mt-2">
                    <ScoreBox label="F" value={piotroski} max={9} />
                    <ScoreBox label="Z" value={altman} threshold={2.99} kind="hi" />
                    <ScoreBox label="M" value={beneish} threshold={-2.22} kind="lo" />
                  </div>
                )}
                {fm.sector && (
                  <div className="text-[10px] text-zinc-500 mt-2">{String(fm.sector)}</div>
                )}
              </article>
            );
          })}
          {dossiers.length === 0 && (
            <div className="col-span-full card p-12 rounded-lg text-center text-zinc-500">
              Sem dossiers. Corre <code>ii deepdive &lt;TK&gt; --save-obsidian</code>.
            </div>
          )}
        </div>
      </section>

      <section>
        <h2 className="text-sm font-mono uppercase tracking-wider text-purple-300 mb-3">
          Deepdive JSON history ({deepdiveJsons.length})
        </h2>
        <div className="card p-3 rounded-lg max-h-96 overflow-y-auto">
          <table className="w-full text-xs font-mono">
            <thead>
              <tr className="text-zinc-500 text-left">
                <th className="py-1">Ticker</th>
                <th className="py-1">When</th>
                <th className="py-1">Path</th>
              </tr>
            </thead>
            <tbody>
              {deepdiveJsons.map((j) => (
                <tr key={j.path} className="border-t border-[#1f1f3d]">
                  <td className="py-1.5 text-cyan-300">{j.ticker}</td>
                  <td className="py-1.5 text-zinc-500">
                    {j.ts.slice(0, 4)}-{j.ts.slice(4, 6)}-{j.ts.slice(6, 8)}{" "}
                    {j.ts.slice(9, 11)}:{j.ts.slice(11, 13)}
                  </td>
                  <td className="py-1.5 text-zinc-600 truncate">
                    {j.path.split(/[\\/]/).slice(-2).join("/")}
                  </td>
                </tr>
              ))}
              {deepdiveJsons.length === 0 && (
                <tr>
                  <td colSpan={3} className="text-zinc-500 italic py-4 text-center">
                    Sem JSON. Corre <code>ii deepdive &lt;TK&gt;</code>.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

function ScoreBox({
  label,
  value,
  max,
  threshold,
  kind,
}: {
  label: string;
  value: number | undefined;
  max?: number;
  threshold?: number;
  kind?: "hi" | "lo";
}) {
  if (value == null) {
    return <div className="bg-zinc-900/40 p-1.5 rounded text-zinc-600 text-center">{label}: —</div>;
  }
  let tone = "bg-zinc-900/40 text-zinc-300";
  if (max != null) {
    tone = value >= 7 ? "bg-green-900/30 text-green-300"
         : value >= 4 ? "bg-yellow-900/30 text-yellow-300"
         : "bg-red-900/30 text-red-300";
  } else if (threshold != null) {
    const ok = kind === "hi" ? value > threshold : value < threshold;
    tone = ok ? "bg-green-900/30 text-green-300" : "bg-red-900/30 text-red-300";
  }
  return (
    <div className={`p-1.5 rounded text-center ${tone}`}>
      {label}: {typeof value === "number" ? value.toFixed(2) : value}
    </div>
  );
}
