import {
  listResearchDigests,
  listKnowledgeCards,
  readTopicScores,
  type Topic,
} from "@/lib/vault";

export const dynamic = "force-dynamic";

const TIER_META: Record<
  Topic["tier"],
  { label: string; bg: string; pill: string }
> = {
  make_now: {
    label: "MAKE NOW",
    bg: "border-red-500/40 bg-gradient-to-r from-red-950/30 to-zinc-950",
    pill: "bg-red-900/50 text-red-300 border-red-700/40",
  },
  rising: {
    label: "RISING",
    bg: "border-yellow-500/30 bg-gradient-to-r from-yellow-950/20 to-zinc-950",
    pill: "bg-yellow-900/40 text-yellow-300 border-yellow-700/40",
  },
  watch: {
    label: "WATCH",
    bg: "border-purple-500/30 bg-gradient-to-r from-purple-950/30 to-zinc-950",
    pill: "bg-purple-900/40 text-purple-300 border-purple-700/40",
  },
  background: {
    label: "BACKGROUND",
    bg: "border-zinc-700 bg-zinc-900/40",
    pill: "bg-zinc-800 text-zinc-400 border-zinc-700",
  },
};

export default function ContentPage() {
  const scores = readTopicScores();
  const topics = scores?.topics || [];
  const digests = listResearchDigests(10);
  const cards = listKnowledgeCards(20);

  const counts = {
    make_now: topics.filter((t) => t.tier === "make_now").length,
    rising: topics.filter((t) => t.tier === "rising").length,
    watch: topics.filter((t) => t.tier === "watch").length,
    background: topics.filter((t) => t.tier === "background").length,
  };

  return (
    <div className="p-8 space-y-6">
      <header className="border-b border-[#1f1f3d] pb-4">
        <div className="flex items-end justify-between">
          <div>
            <h1 className="text-3xl font-light text-zinc-100">
              <span className="text-purple-400">❖</span> Content
            </h1>
            <p className="text-xs font-mono text-zinc-500 mt-1">
              Topic Watchlist · Research Digests · Knowledge Cards
            </p>
          </div>
          {scores && (
            <span className="text-[10px] font-mono text-zinc-500">
              updated {scores.computed_at.slice(0, 16)}
            </span>
          )}
        </div>
      </header>

      {/* Topic Watchlist (primary) */}
      <section>
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-mono uppercase tracking-wider text-purple-300">
            Topic Watchlist <span className="text-zinc-500">({topics.length})</span>
          </h2>
          <div className="flex items-center gap-3 text-[10px] font-mono">
            <span className="text-red-400">🔴 {counts.make_now} make now</span>
            <span className="text-yellow-400">🟡 {counts.rising} rising</span>
            <span className="text-purple-400">🟣 {counts.watch} watch</span>
            <span className="text-zinc-500">⚪ {counts.background} bg</span>
          </div>
        </div>

        {topics.length === 0 ? (
          <div className="card p-12 rounded-lg text-center text-zinc-500">
            Sem scores. Corre <code>python -m analytics.topic_scorer</code>.
          </div>
        ) : (
          <div className="space-y-3">
            {topics.map((t) => (
              <TopicCard key={t.id} topic={t} />
            ))}
          </div>
        )}
      </section>

      {/* Research Digests */}
      <section>
        <h2 className="text-sm font-mono uppercase tracking-wider text-purple-300 mb-3">
          Research Digests ({digests.length})
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {digests.map((d) => (
            <article key={d.path} className="card-purple p-4 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-zinc-100 font-medium text-sm">{d.title}</h3>
                <span className="text-[10px] font-mono text-zinc-500">
                  {new Date(d.modified).toISOString().slice(0, 10)}
                </span>
              </div>
              <pre className="text-[11px] text-zinc-300 whitespace-pre-wrap font-mono leading-relaxed line-clamp-6">
                {d.preview}
              </pre>
            </article>
          ))}
          {digests.length === 0 && (
            <div className="col-span-full card p-12 rounded-lg text-center text-zinc-500">
              Sem digests. Corre <code>python scripts/research_digest.py</code>.
            </div>
          )}
        </div>
      </section>

      {/* Knowledge Cards */}
      <section>
        <h2 className="text-sm font-mono uppercase tracking-wider text-purple-300 mb-3">
          Knowledge Cards ({cards.length})
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {cards.map((c) => (
            <article
              key={c.path}
              className="card p-3 rounded-lg hover:border-purple-700/50 transition-colors"
            >
              <h3 className="text-zinc-200 font-medium text-sm truncate">{c.title}</h3>
              <p className="text-xs text-zinc-400 line-clamp-3 mt-1">
                {c.preview.replace(/^---[\s\S]*?---/, "").trim().slice(0, 200)}
              </p>
              <div className="text-[9px] font-mono text-zinc-600 mt-2">
                {c.relpath.split("/").slice(-2).join("/")}
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}

function TopicCard({ topic }: { topic: Topic }) {
  const meta = TIER_META[topic.tier];
  return (
    <article className={`p-4 rounded-lg border ${meta.bg}`}>
      <div className="flex items-start gap-4">
        <div className="flex flex-col items-center min-w-[70px]">
          <div className="text-3xl font-light text-zinc-100 tabular">{topic.score}</div>
          <span className={`mt-1 px-2 py-0.5 rounded border text-[9px] font-mono ${meta.pill}`}>
            {meta.label}
          </span>
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="text-zinc-100 font-medium">{topic.name}</h3>
            {topic.tags.map((t) => (
              <span key={t} className="tag text-zinc-400">{t}</span>
            ))}
          </div>
          <p className="text-xs text-zinc-400 mt-1 line-clamp-2">{topic.summary}</p>
          <div className="flex items-center gap-4 mt-2 text-[10px] font-mono text-zinc-500">
            <span>{topic.mentions_recent} mentions / 14d</span>
            <span>tracked {topic.weeks_tracked}w</span>
            {topic.holdings_hit.length > 0 && (
              <span className="text-cyan-300">
                {topic.holdings_hit.slice(0, 4).join(" · ")}
                {topic.holdings_hit.length > 4 && ` +${topic.holdings_hit.length - 4}`}
              </span>
            )}
            {topic.open_triggers > 0 && (
              <span className="text-yellow-400">
                {topic.open_triggers} open trigger{topic.open_triggers > 1 ? "s" : ""}
              </span>
            )}
          </div>
        </div>
      </div>
    </article>
  );
}
