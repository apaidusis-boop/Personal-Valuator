"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

type NavItem = { href: string; label: string; icon: string };

const NAV: NavItem[] = [
  { href: "/",           label: "Home",      icon: "◇" },
  { href: "/council",    label: "Council",   icon: "⚖" },
  { href: "/tasks",      label: "Tasks",     icon: "▤" },
  { href: "/content",    label: "Content",   icon: "❖" },
  { href: "/calendar",   label: "Calendar",  icon: "▦" },
  { href: "/projects",   label: "Projects",  icon: "❑" },
  { href: "/memory",     label: "Memory",    icon: "✶" },
  { href: "/docs",       label: "Docs",      icon: "≡" },
  { href: "/team",       label: "Team",      icon: "◉" },
  { href: "/visual",     label: "Visual",    icon: "▦" },
];

export default function Sidebar() {
  const path = usePathname();

  return (
    <aside className="w-56 shrink-0 border-r border-[#1f1f3d] bg-[#08081a] flex flex-col">
      <div className="px-4 py-6 border-b border-[#1f1f3d]">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-600 to-cyan-500 grid place-items-center text-2xl">
            🐙
          </div>
          <div>
            <div className="font-mono text-[11px] tracking-[0.18em] text-purple-300">MISSION</div>
            <div className="font-mono text-[11px] tracking-[0.18em] text-purple-300">CONTROL</div>
          </div>
        </div>
        <div className="mt-3 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-cyan-400 dot-live animate-pulse"></span>
          <span className="font-mono text-[10px] uppercase tracking-wider text-cyan-300">
            Antonio Carlos · Online
          </span>
        </div>
      </div>

      <nav className="flex-1 px-2 py-4 space-y-1">
        {NAV.map((item) => {
          const active = path === item.href || (item.href !== "/" && path.startsWith(item.href));
          return (
            <Link
              key={item.href}
              href={item.href}
              className={
                "flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-all " +
                (active
                  ? "bg-purple-900/40 border border-purple-700/40 text-purple-200"
                  : "text-zinc-400 hover:text-zinc-100 hover:bg-zinc-900/40")
              }
            >
              <span className="text-lg w-5 text-center">{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="px-4 py-3 border-t border-[#1f1f3d] text-[10px] font-mono text-zinc-600">
        LocalClaw · Phase EE
      </div>
    </aside>
  );
}
