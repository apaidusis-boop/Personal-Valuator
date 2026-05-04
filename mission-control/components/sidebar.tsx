"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

type NavItem = { href: string; label: string; icon: string };
type NavGroup = { label: string; items: NavItem[] };

const GROUPS: NavGroup[] = [
  {
    label: "Today",
    items: [
      { href: "/", label: "Home", icon: "◇" },
      { href: "/tasks", label: "Tasks", icon: "▤" },
    ],
  },
  {
    label: "Decide",
    items: [
      { href: "/allocation", label: "Allocation", icon: "▲" },
      { href: "/council", label: "Council", icon: "⚖" },
    ],
  },
  {
    label: "Research",
    items: [
      { href: "/content", label: "Content", icon: "❖" },
      { href: "/memory", label: "Memory", icon: "✶" },
      { href: "/docs", label: "Docs", icon: "≡" },
    ],
  },
  {
    label: "System",
    items: [
      { href: "/calendar", label: "Calendar", icon: "▦" },
      { href: "/team", label: "Team", icon: "◉" },
    ],
  },
];

export default function Sidebar() {
  const path = usePathname();
  const isActive = (href: string) =>
    path === href || (href !== "/" && path.startsWith(href));

  return (
    <aside
      className="w-56 shrink-0 border-r border-[var(--border-subtle)] flex flex-col"
      style={{ background: "var(--bg-deep)" }}
    >
      {/* Brand */}
      <div className="px-4 py-5 border-b border-[var(--border-subtle)]">
        <Link href="/" className="flex items-center gap-3 group">
          <div
            className="w-9 h-9 rounded grid place-items-center text-xl font-mono"
            style={{
              background:
                "linear-gradient(135deg, var(--accent-primary), var(--accent-glow))",
            }}
          >
            <span aria-hidden>◈</span>
          </div>
          <div>
            <div className="type-mono-sm text-[var(--text-secondary)]">
              MISSION
            </div>
            <div className="type-mono-sm text-[var(--text-secondary)]">
              CONTROL
            </div>
          </div>
        </Link>
        <div className="mt-3 flex items-center gap-2">
          <span
            className="w-1.5 h-1.5 rounded-full bg-[var(--accent-glow)] dot-live animate-pulse"
            aria-hidden
          />
          <span className="type-mono-sm text-[var(--accent-glow)]">
            antonio carlos · online
          </span>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-2 py-4 space-y-5 overflow-y-auto">
        {GROUPS.map((g) => (
          <div key={g.label}>
            <div className="px-3 mb-1.5">
              <span className="type-h3">{g.label}</span>
            </div>
            <ul className="space-y-0.5">
              {g.items.map((item) => {
                const active = isActive(item.href);
                return (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      className={
                        "flex items-center gap-3 px-3 py-1.5 rounded-md type-body-sm transition-colors " +
                        (active
                          ? "bg-[rgba(139,92,246,0.12)] text-[var(--text-primary)] border-l-2 border-[var(--accent-primary)] -ml-0.5 pl-[14px]"
                          : "text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-overlay)]")
                      }
                    >
                      <span
                        className="w-4 text-center text-[var(--text-tertiary)]"
                        aria-hidden
                      >
                        {item.icon}
                      </span>
                      <span>{item.label}</span>
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </nav>

      {/* Footer — extras + version */}
      <div className="px-4 py-3 border-t border-[var(--border-subtle)] space-y-2">
        <Link
          href="/visual"
          className={
            "flex items-center gap-2 type-mono-sm text-[var(--text-tertiary)] hover:text-[var(--accent-glow)] transition-colors " +
            (isActive("/visual") ? "text-[var(--accent-glow)]" : "")
          }
        >
          <span aria-hidden>▦</span>
          <span>visual office</span>
        </Link>
        <div className="type-mono-sm text-[var(--text-disabled)]">
          localclaw · phase ee
        </div>
      </div>
    </aside>
  );
}
