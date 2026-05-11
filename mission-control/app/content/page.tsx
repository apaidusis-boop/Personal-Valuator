import {
  listResearchDigests,
  listKnowledgeCards,
  readTopicScores,
  type Topic,
} from "@/lib/vault";
import { formatDate } from "@/lib/format";
import { PageHeader, EmptyState } from "@/components/ui";

export const dynamic = "force-dynamic";

const TIER_META: Record<
  Topic["tier"],
  { label: string; bg: string; pill: string }
> = {
  make_now: {
    label: "MAKE NOW",
    bg: "border-[rgba(239,68,68,0.35)] bg-gradient-to-r from-[rgba(239,68,68,0.06)] to-transparent",
    pill: "bg-[rgba(239,68,68,0.1)] text-[var(--verdict-avoid)] border-[rgba(239,68,68,0.35)]",
  },
  rising: {
    label: "RISING",
    bg: "border-[rgba(245,158,11,0.3)] bg-gradient-to-r from-[rgba(245,158,11,0.05)] to-transparent",
    pill: "bg-[rgba(245,158,11,0.08)] text-[var(--verdict-hold)] border-[rgba(245,158,11,0.3)]",
  },
  watch: {
    label: "WATCH",
    bg: "border-[rgba(139,92,246,0.3)] bg-gradient-to-r from-[rgba(139,92,246,0.05)] to-transparent",
    pill: "bg-[rgba(139,92,246,0.08)] text-[var(--accent-primary)] border-[rgba(139,92,246,0.3)]",
  },
  background: {
    label: "BACKGROUND",
    bg: "border-[var(--border-subtle)] bg-[var(--bg-elevated)]",
    pill: "bg-[var(--bg-overlay)] text-[var(--text-tertiary)] border-[var(--border-subtle)]",
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
    <div className="p-8 space-y-8 max-w-[1400px]">
      <PageHeader
        title="Content"
        subtitle="Topic Watchlist · Research Digests · Knowledge Cards"
        crumbs={[{ label: "Home", href: "/" }, { label: "Content" }]}
        freshness={scores?.computed_at}
      />

      {/* Topic Watchlist (primary) */}
      <section>
        <div className="flex items-center justify-between mb-3">
          <h2 className="type-h3">topic watchlist · {topics.length}</h2>
          <div className="flex items-center gap-2">
            <span className="pill pill-avoid">{counts.make_now} make now</span>
            <span className="pill pill-hold">{counts.rising} rising</span>
            <span className="pill pill-purple">{counts.watch} watch</span>
            <span className="pill pill-neutral">{counts.background} bg</span>
          </div>
        </div>

        {topics.length === 0 ? (
          <EmptyState
            icon="◯"
            title="Sem topic scores"
            description="O scorer corre durante o overnight batch. Aguarda a próxima execução."
          />
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
        <h2 className="text-sm font-mono uppercase tracking-wider text-[var(--text-tertiary)] mb-3">
          research digests · {digests.length}
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {digests.map((d) => (
            <article key={d.path} className="card-purple p-4">
              <div className="flex items-center justify-between mb-2">
                <h3 className="type-body text-[var(--text-primary)] font-medium">{d.title}</h3>
                <span className="type-mono-sm text-[var(--text-tertiary)]">
                  {formatDate(d.modified, "relative")}
                </span>
              </div>
              <p className="type-body-sm text-[var(--text-secondary)] line-clamp-5 leading-relaxed whitespace-pre-wrap">
                {d.preview}
              </p>
            </article>
          ))}
          {digests.length === 0 && (
            <div className="col-span-full">
              <EmptyState icon="◯" title="Sem research digests" description="Os digests são gerados pelo daily research." />
            </div>
          )}
        </div>
      </section>

      {/* Knowledge Cards */}
      <section>
        <h2 className="type-h3 mb-3">knowledge cards · {cards.length}</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {cards.map((c) => (
            <article
              key={c.path}
              className="card p-4 hover:border-[var(--border-strong)] transition-colors"
            >
              <h3 className="type-body text-[var(--text-primary)] font-medium truncate mb-1">
                {c.title}
              </h3>
              <p className="type-body-sm text-[var(--text-secondary)] line-clamp-3">
                {c.preview.replace(/^---[\s\S]*?---/, "").trim().slice(0, 200)}
              </p>
              <div className="type-mono-sm text-[var(--text-disabled)] mt-2">
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
