"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import ThemeToggle from "./theme-toggle";

type NavItem = { href: string; label: string };
type NavGroup = { label: string; items: NavItem[] };

const GROUPS: NavGroup[] = [
  {
    label: "Today",
    items: [
      { href: "/", label: "Home" },
      { href: "/tasks", label: "Tasks" },
    ],
  },
  {
    label: "Decide",
    items: [
      { href: "/allocation", label: "Allocation" },
      { href: "/council", label: "Council" },
    ],
  },
  {
    label: "Research",
    items: [
      { href: "/content", label: "Content" },
      { href: "/memory", label: "Memory" },
      { href: "/docs", label: "Docs" },
    ],
  },
  {
    label: "System",
    items: [
      { href: "/calendar", label: "Calendar" },
      { href: "/team", label: "Team" },
    ],
  },
];

/**
 * Editorial-style sidebar — masthead at top, sections like FT supplements.
 * No icons (icons drift toward consumer SaaS); active state is a left rule.
 */
export default function Sidebar() {
  const path = usePathname();
  const isActive = (href: string) =>
    path === href || (href !== "/" && path.startsWith(href));

  return (
    <aside
      className="w-48 shrink-0 border-r border-[var(--border-subtle)] flex flex-col"
      style={{ background: "var(--bg-deep)" }}
    >
      {/* Masthead — broadsheet vibe */}
      <div className="px-4 pt-6 pb-4 border-b-2 border-[var(--rule)]">
        <Link href="/" className="block group">
          <div
            className="serif text-[var(--text-primary)] leading-none"
            style={{ fontSize: 22, fontWeight: 700, letterSpacing: "-0.01em" }}
          >
            Mission
          </div>
          <div
            className="serif text-[var(--text-primary)] leading-none mt-0.5"
            style={{ fontSize: 22, fontWeight: 700, letterSpacing: "-0.01em" }}
          >
            Control
          </div>
          <div className="type-byline mt-2">
            est. 2026 · LocalClaw edition
          </div>
        </Link>
        <div className="mt-3 flex items-center gap-2">
          <span
            className="w-1.5 h-1.5 rounded-full bg-[var(--verdict-buy)] dot-live"
            aria-hidden
          />
          <span className="type-mono-sm text-[var(--text-secondary)]">
            antonio carlos · live
          </span>
        </div>
      </div>

      {/* Nav — section labels small caps, items plain serif */}
      <nav className="flex-1 px-3 py-4 space-y-5 overflow-y-auto">
        {GROUPS.map((g) => (
          <div key={g.label}>
            <div className="px-1 mb-1.5">
              <span className="type-h3">{g.label}</span>
            </div>
            <ul className="space-y-px">
              {g.items.map((item) => {
                const active = isActive(item.href);
                return (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      className={
                        "block px-2 py-1 type-body-sm transition-colors " +
                        (active
                          ? "text-[var(--text-primary)] border-l-2 border-[var(--accent-primary)] -ml-0.5 pl-[10px] font-medium"
                          : "text-[var(--text-secondary)] hover:text-[var(--text-primary)]")
                      }
                    >
                      {item.label}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </nav>

      {/* Footer — visual office + theme toggle + version */}
      <div className="px-4 py-3 border-t border-[var(--border-subtle)] space-y-2">
        <Link
          href="/visual"
          className={
            "block type-mono-sm text-[var(--text-tertiary)] hover:text-[var(--accent-glow)] transition-colors " +
            (isActive("/visual") ? "text-[var(--accent-glow)]" : "")
          }
        >
          visual office
        </Link>
        <ThemeToggle />
        <div className="type-mono-sm text-[var(--text-disabled)]">
          v3 · broadsheet
        </div>
      </div>
    </aside>
  );
}
