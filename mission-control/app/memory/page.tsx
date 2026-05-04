import { listChatIds, listChiefMessages } from "@/lib/db";
import { listAutoMemory, listDailyEntries, readAutoMemoryIndex } from "@/lib/vault";
import { formatDate } from "@/lib/format";
import { PageHeader } from "@/components/ui";
import Link from "next/link";

export const dynamic = "force-dynamic";

type Tab = "daily" | "longterm" | "chats";

export default async function MemoryPage({
  searchParams,
}: {
  searchParams: Promise<{ tab?: string; entry?: string; chat?: string }>;
}) {
  const sp = await searchParams;
  const tab: Tab = (sp.tab as Tab) || "daily";

  return (
    <div className="p-8 space-y-6 max-w-[1400px]">
      <PageHeader
        title="Memory"
        subtitle="Daily Log · Long-term · Antonio Carlos chats"
        crumbs={[{ label: "Home", href: "/" }, { label: "Memory" }]}
      />

      {/* Tabs */}
      <div className="flex items-center gap-1 -mt-2">
        <TabButton href="?tab=daily"    active={tab === "daily"}    label="Daily Log" />
        <TabButton href="?tab=longterm" active={tab === "longterm"} label="Long-term" />
        <TabButton href="?tab=chats"    active={tab === "chats"}    label="Chats" />
      </div>

      {tab === "daily" && <DailyLog selectedPath={sp.entry} />}
      {tab === "longterm" && <LongTerm selectedName={sp.entry} />}
      {tab === "chats" && <Chats selectedChat={sp.chat} />}
    </div>
  );
}

function TabButton({ href, active, label }: { href: string; active: boolean; label: string }) {
  return (
    <Link
      href={href}
      className={
        "px-4 py-2 type-mono-sm rounded-md transition-colors " +
        (active
          ? "bg-[rgba(139,92,246,0.12)] border border-[rgba(139,92,246,0.3)] text-[var(--text-primary)]"
          : "text-[var(--text-tertiary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-overlay)] border border-transparent")
      }
    >
      {label}
    </Link>
  );
}

function DailyLog({ selectedPath }: { selectedPath?: string }) {
  const entries = listDailyEntries(60);
  const selected = entries.find((e) => e.path === selectedPath) || entries[0];

  return (
    <div className="grid grid-cols-12 gap-4">
      <aside className="col-span-12 md:col-span-4 card p-3 rounded-lg max-h-[70vh] overflow-y-auto">
        <h2 className="text-[10px] font-mono uppercase tracking-wider text-zinc-500 mb-2 px-2">
          {entries.length} entries
        </h2>
        <ul className="space-y-1">
          {entries.map((e) => {
            const active = e.path === selected?.path;
            return (
              <li key={e.path}>
                <Link
                  href={`?tab=daily&entry=${encodeURIComponent(e.path)}`}
                  className={
                    "block px-3 py-2 rounded text-sm " +
                    (active
                      ? "bg-purple-900/40 border border-purple-700/40 text-purple-100"
                      : "text-zinc-300 hover:bg-zinc-900/40 border border-transparent")
                  }
                >
                  <div className="type-mono text-[var(--accent-glow)]">{formatDate(e.date, "short")}</div>
                  <div className="type-mono-sm text-[var(--text-tertiary)] mt-0.5">{e.words} words · {formatDate(e.date, "relative")}</div>
                  <div className="type-body-sm text-[var(--text-secondary)] mt-1 line-clamp-1">{e.title}</div>
                </Link>
              </li>
            );
          })}
          {entries.length === 0 && (
            <li className="type-body-sm text-[var(--text-tertiary)] italic px-3 py-4">
              Nenhum daily log disponível ainda.
            </li>
          )}
        </ul>
      </aside>

      <section className="col-span-12 md:col-span-8 card p-5 rounded-lg max-h-[70vh] overflow-y-auto">
        {selected ? (
          <>
            <header className="flex items-center justify-between mb-4 pb-3 border-b border-[#1f1f3d]">
              <div>
                <h3 className="text-zinc-100 text-lg font-light">{selected.title}</h3>
                <div className="text-[10px] font-mono text-zinc-500 mt-0.5">
                  {selected.source} · {selected.words} words
                </div>
              </div>
              <span className="tag text-purple-300">{selected.date}</span>
            </header>
            <pre className="text-xs text-zinc-300 whitespace-pre-wrap font-mono leading-relaxed">
              {selected.body}
            </pre>
          </>
        ) : (
          <div className="text-zinc-500 italic">Selecciona uma entrada à esquerda.</div>
        )}
      </section>
    </div>
  );
}

function LongTerm({ selectedName }: { selectedName?: string }) {
  const entries = listAutoMemory(200);
  const selected = entries.find((e) => e.name === selectedName) || entries[0];
  const indexMd = readAutoMemoryIndex();

  // Group by type
  const byType: Record<string, typeof entries> = {};
  for (const e of entries) {
    const t = e.type || "note";
    if (!byType[t]) byType[t] = [];
    byType[t].push(e);
  }

  const TYPE_TONE: Record<string, string> = {
    user: "text-cyan-300",
    feedback: "text-yellow-300",
    project: "text-purple-300",
    reference: "text-green-300",
    note: "text-zinc-300",
  };

  return (
    <div className="grid grid-cols-12 gap-4">
      <aside className="col-span-12 md:col-span-4 card p-3 rounded-lg max-h-[70vh] overflow-y-auto">
        <h2 className="text-[10px] font-mono uppercase tracking-wider text-zinc-500 mb-2 px-2">
          {entries.length} memories
        </h2>
        {Object.entries(byType).map(([type, items]) => (
          <div key={type} className="mb-3">
            <div className={`text-[10px] font-mono uppercase tracking-wider mb-1 px-2 ${TYPE_TONE[type] || "text-zinc-400"}`}>
              {type} ({items.length})
            </div>
            <ul className="space-y-0.5">
              {items.map((e) => {
                const active = e.name === selected?.name;
                return (
                  <li key={e.path}>
                    <Link
                      href={`?tab=longterm&entry=${encodeURIComponent(e.name)}`}
                      className={
                        "block px-3 py-1.5 rounded text-xs " +
                        (active
                          ? "bg-purple-900/40 border border-purple-700/40 text-purple-100"
                          : "text-zinc-400 hover:bg-zinc-900/40 border border-transparent")
                      }
                    >
                      <div className="font-mono">{e.name}</div>
                      {e.description && (
                        <div className="text-[10px] text-zinc-500 line-clamp-1 mt-0.5">
                          {e.description.slice(0, 80)}
                        </div>
                      )}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </aside>

      <section className="col-span-12 md:col-span-8 card p-5 rounded-lg max-h-[70vh] overflow-y-auto">
        {selected ? (
          <>
            <header className="mb-4 pb-3 border-b border-[#1f1f3d]">
              <div className="flex items-center justify-between">
                <h3 className="text-zinc-100 text-lg font-light">{selected.name}</h3>
                <span className={`tag ${TYPE_TONE[selected.type] || "text-zinc-400"}`}>
                  {selected.type}
                </span>
              </div>
              {selected.description && (
                <p className="text-xs text-zinc-400 mt-2">{selected.description}</p>
              )}
              <div className="text-[10px] font-mono text-zinc-500 mt-1">
                {selected.words} words · modified {new Date(selected.modified).toISOString().slice(0, 16)}
              </div>
            </header>
            <pre className="text-xs text-zinc-300 whitespace-pre-wrap font-mono leading-relaxed">
              {selected.body}
            </pre>
          </>
        ) : (
          <div className="text-zinc-500 italic">
            <p>Memória auto vazia.</p>
            <p className="mt-2 text-xs">{indexMd.slice(0, 500)}</p>
          </div>
        )}
      </section>
    </div>
  );
}

function Chats({ selectedChat }: { selectedChat?: string }) {
  const chats = listChatIds();
  const selected = selectedChat || chats[0]?.chat_id || "";
  const messages = selected ? listChiefMessages(selected, 80) : [];

  return (
    <div className="grid grid-cols-12 gap-4">
      <aside className="col-span-12 md:col-span-3 card p-3 rounded-lg max-h-[70vh] overflow-y-auto">
        <h2 className="text-[10px] font-mono uppercase tracking-wider text-zinc-500 mb-2 px-2">
          Chats ({chats.length})
        </h2>
        {chats.length === 0 && (
          <div className="text-xs text-zinc-500 italic px-2">
            Sem chats. Fala com Antonio Carlos via Telegram ou{" "}
            <code>ii antonio &quot;...&quot;</code>
          </div>
        )}
        <ul className="space-y-1">
          {chats.map((c) => {
            const active = c.chat_id === selected;
            return (
              <li key={c.chat_id}>
                <Link
                  href={`?tab=chats&chat=${encodeURIComponent(c.chat_id)}`}
                  className={
                    "block px-2 py-1.5 rounded text-xs " +
                    (active
                      ? "bg-purple-900/40 border border-purple-700/40 text-purple-200"
                      : "text-zinc-400 hover:bg-zinc-900/40 border border-transparent")
                  }
                >
                  <div className="font-mono truncate">{c.chat_id}</div>
                  <div className="text-[9px] text-zinc-500 mt-0.5">
                    {c.n_messages} msgs · {c.last_ts.slice(5, 16)}
                  </div>
                </Link>
              </li>
            );
          })}
        </ul>
      </aside>

      <section className="col-span-12 md:col-span-9 card p-5 rounded-lg max-h-[70vh] overflow-y-auto">
        <h2 className="text-[10px] font-mono uppercase tracking-wider text-zinc-500 mb-3">
          {selected || "(no chat)"}
        </h2>
        <div className="space-y-3">
          {messages.map((m) => {
            const ts = m.ts.slice(11, 19);
            return (
              <div key={m.id} className={"text-xs " + roleColor(m.role)}>
                <div className="flex items-center gap-2 mb-0.5">
                  <span className="font-mono text-[10px] uppercase tracking-wider opacity-70">
                    {m.role}
                    {m.tool_name ? ` · ${m.tool_name}` : ""}
                  </span>
                  <span className="font-mono text-[10px] text-zinc-600">{ts}</span>
                </div>
                <pre className="whitespace-pre-wrap break-words font-sans">
                  {truncate(m.content, m.role === "tool" ? 600 : 1500)}
                </pre>
              </div>
            );
          })}
          {messages.length === 0 && (
            <div className="text-zinc-500 italic text-sm">Sem mensagens.</div>
          )}
        </div>
      </section>
    </div>
  );
}

function roleColor(role: string): string {
  if (role === "user") return "border-l-2 border-cyan-500/60 pl-3 text-zinc-200";
  if (role === "assistant") return "border-l-2 border-purple-500/60 pl-3 text-zinc-300";
  if (role === "tool") return "border-l-2 border-zinc-700 pl-3 text-zinc-500";
  return "pl-3 text-zinc-400";
}

function truncate(s: string, n: number): string {
  if (s.length <= n) return s;
  return s.slice(0, n) + "…";
}
