import { listDepartments } from "@/lib/agents";
import { PageHeader } from "@/components/ui";

export const dynamic = "force-dynamic";

const MASCOTS = ["🐙", "🤖", "👁", "🦉", "🐢", "🦊", "🐺", "🦅", "🐉", "🐝", "🦋", "🦞", "🦂", "🪼"];

function mascotFor(name: string): string {
  // deterministic pick from agent name hash
  let h = 0;
  for (const c of name) h = (h * 31 + c.charCodeAt(0)) >>> 0;
  return MASCOTS[h % MASCOTS.length];
}

function statusBg(s: string | null | undefined) {
  if (s === "ok")        return "from-cyan-900/60 to-cyan-950";
  if (s === "no_action") return "from-purple-900/40 to-zinc-950";
  if (s === "failed")    return "from-red-900/60 to-red-950";
  return "from-zinc-900/60 to-zinc-950";
}

function statusBorder(s: string | null | undefined) {
  if (s === "ok")        return "border-cyan-500/50";
  if (s === "no_action") return "border-purple-700/40";
  if (s === "failed")    return "border-red-500/60";
  return "border-zinc-700";
}

function statusLabel(s: string | null | undefined): string {
  if (s === "ok") return "ACTIVE";
  if (s === "no_action") return "IDLE";
  if (s === "failed") return "ALERT";
  return "—";
}

function timeAgo(iso: string | null | undefined): string {
  if (!iso) return "never";
  const ts = new Date(iso).getTime();
  if (isNaN(ts)) return iso;
  const diff = Date.now() - ts;
  const m = Math.floor(diff / 60000);
  if (m < 1) return "now";
  if (m < 60) return `${m}m ago`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}h ago`;
  const d = Math.floor(h / 24);
  return `${d}d ago`;
}

export default function VisualOfficePage() {
  const departments = listDepartments();
  const allAgents = departments
    .flatMap((d) => d.members)
    .filter((m) => m.enabled);

  // Antonio Carlos in the center (chief)
  const chief = allAgents.find((a) => a.name === "antonio_carlos");
  const others = allAgents.filter((a) => a.name !== "antonio_carlos");

  return (
    <div className="p-8 space-y-6 max-w-[1400px]">
      <PageHeader
        title="Agent Office"
        subtitle="Quem está a trabalhar, quem está em standby, quem precisa de atenção"
        crumbs={[{ label: "Home", href: "/" }, { label: "Visual Office" }]}
        freshnessLabel="live"
        freshness={new Date()}
      />

      {/* Chief of Staff feature */}
      {chief && (
        <section
          className={`relative rounded-xl border-2 ${statusBorder(chief.status?.last_status)} bg-gradient-to-br ${statusBg(
            chief.status?.last_status
          )} p-8 overflow-hidden`}
        >
          <div className="absolute inset-0 opacity-[0.03] pointer-events-none"
               style={{
                 backgroundImage:
                   "repeating-linear-gradient(0deg, #fff 0, #fff 1px, transparent 1px, transparent 8px), repeating-linear-gradient(90deg, #fff 0, #fff 1px, transparent 1px, transparent 8px)",
               }}
          ></div>
          <div className="absolute top-2 right-3 text-[10px] font-mono text-cyan-300 tracking-wider">
            CHIEF·OF·STAFF
          </div>
          <div className="flex items-center gap-6">
            <div className="text-7xl pixelated drop-shadow-[0_0_12px_rgba(168,85,247,0.6)] animate-pulse">
              {mascotFor(chief.name)}
            </div>
            <div>
              <div className="text-3xl font-light text-zinc-100">{chief.employee_name}</div>
              <div className="text-sm text-purple-300 font-mono">{chief.title}</div>
              <div className="text-xs text-zinc-400 mt-2 max-w-2xl line-clamp-2">{chief.bio}</div>
              <div className="flex items-center gap-3 mt-3 text-[10px] font-mono">
                <span className="px-2 py-0.5 rounded border border-cyan-500/40 bg-cyan-900/30 text-cyan-300">
                  {statusLabel(chief.status?.last_status)}
                </span>
                <span className="text-zinc-500">
                  last seen {timeAgo(chief.status?.last_run)}
                </span>
                <span className="text-zinc-500">
                  · {chief.status?.run_count || 0} runs
                </span>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Office grid */}
      <section>
        <h2 className="text-sm font-mono uppercase tracking-wider text-zinc-400 mb-3">
          The Office <span className="text-purple-400">({others.length} desks)</span>
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {others.map((a) => (
            <Room key={a.name} agent={a} />
          ))}
        </div>
      </section>

      {/* Status legend */}
      <section className="card p-4 rounded-lg flex flex-wrap items-center gap-6 text-xs font-mono text-zinc-400">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-cyan-400 dot-live"></span>
          ACTIVE — corre algoritmo
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-purple-700"></span>
          IDLE — em standby
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-red-400 dot-fail"></span>
          ALERT — falhou último run
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-zinc-700"></span>
          UNKNOWN — sem state ainda
        </div>
      </section>
    </div>
  );
}

function Room({ agent }: { agent: ReturnType<typeof listDepartments>[number]["members"][number] }) {
  const status = agent.status?.last_status;
  const isAlert = status === "failed";
  const isLive = status === "ok";
  return (
    <div
      className={`relative rounded-lg border-2 ${statusBorder(status)} bg-gradient-to-br ${statusBg(
        status
      )} p-4 aspect-[4/3] overflow-hidden hover:scale-[1.02] transition-transform`}
    >
      {/* pixel grid overlay */}
      <div
        className="absolute inset-0 opacity-[0.04] pointer-events-none"
        style={{
          backgroundImage:
            "repeating-linear-gradient(0deg, #fff 0, #fff 1px, transparent 1px, transparent 6px), repeating-linear-gradient(90deg, #fff 0, #fff 1px, transparent 1px, transparent 6px)",
        }}
      ></div>

      {/* corner status pill */}
      <div className="absolute top-2 right-2 flex items-center gap-1 text-[9px] font-mono">
        <span
          className={`w-1.5 h-1.5 rounded-full ${
            isLive ? "bg-cyan-400 dot-live" : isAlert ? "bg-red-400 dot-fail" : "bg-purple-700"
          }`}
        ></span>
        <span className={isLive ? "text-cyan-300" : isAlert ? "text-red-300" : "text-zinc-500"}>
          {statusLabel(status)}
        </span>
      </div>

      {/* mascot center */}
      <div className="h-full flex flex-col items-center justify-end gap-2 relative">
        <div
          className={`text-5xl pixelated ${isLive ? "animate-pulse" : ""} ${
            isAlert ? "grayscale" : ""
          }`}
          style={{
            filter: isLive
              ? "drop-shadow(0 0 8px rgba(77,212,255,0.6))"
              : isAlert
              ? "drop-shadow(0 0 8px rgba(248,113,113,0.6))"
              : "none",
            animationDuration: "3s",
          }}
        >
          {mascotFor(agent.name)}
        </div>
        <div className="text-center">
          <div className="text-xs text-zinc-100 font-medium truncate max-w-[10rem]">
            {agent.employee_name}
          </div>
          <div className="text-[10px] font-mono text-zinc-500">{agent.title}</div>
        </div>
        <div className="text-[9px] font-mono text-zinc-600">
          {timeAgo(agent.status?.last_run)}
        </div>
      </div>
    </div>
  );
}
