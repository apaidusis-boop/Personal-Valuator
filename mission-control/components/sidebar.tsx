"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Search,
  BarChart3,
  TrendingUp,
  Flame,
  Briefcase,
  PieChart,
  Shield,
  Bell,
  FileText,
  Newspaper,
  Users,
  Settings,
  User,
  Activity,
  ListChecks,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

type NavItem = {
  icon: LucideIcon;
  label: string;
  href?: string;          // present when active
  hidden?: boolean;       // true → "Não operacional · Ocultado"
};

type NavSection = {
  label: string;
  items: NavItem[];
};

/**
 * Mirrors the zip layout exactly. 5 active routes (Dashboard, Screening,
 * Portfolio, Alertas, Council) + 8 hidden placeholders that show "Não
 * operacional · Ocultado" so the eventual feature set is visible without
 * being interactive.
 */
const SECTIONS: NavSection[] = [
  {
    label: "ANÁLISE",
    items: [
      { icon: Search, label: "Buscar Ativos", href: "/screening" },
      { icon: BarChart3, label: "Comparador", hidden: true },
      { icon: TrendingUp, label: "Valuation", hidden: true },
      { icon: Flame, label: "Monitor de Mercado", hidden: true },
    ],
  },
  {
    label: "CARTEIRA",
    items: [
      { icon: Briefcase, label: "Minha Carteira", href: "/portfolio" },
      { icon: PieChart, label: "Diversificação", hidden: true },
      { icon: Shield, label: "Monitor de Risco", hidden: true },
    ],
  },
  {
    label: "INTELIGÊNCIA",
    items: [
      { icon: Bell, label: "Alertas", href: "/alertas" },
      { icon: FileText, label: "Filings (CVM/SEC)", href: "/filings" },
      { icon: Newspaper, label: "Calendário", href: "/events" },
      { icon: Users, label: "Council", href: "/council" },
    ],
  },
  {
    label: "PHASE FF",
    items: [
      { icon: Activity, label: "Calibration", href: "/calibration" },
      { icon: ListChecks, label: "Decisions", href: "/decisions" },
    ],
  },
  {
    label: "CONFIGURAÇÕES",
    items: [
      { icon: Settings, label: "Preferências", hidden: true },
      { icon: User, label: "Minha Conta", hidden: true },
    ],
  },
];

export default function Sidebar() {
  const path = usePathname();
  const isActive = (href?: string) => {
    if (!href) return false;
    return path === href || (href !== "/" && path.startsWith(href));
  };

  return (
    <aside
      className="fixed left-0 top-0 h-screen w-[240px] flex flex-col overflow-y-auto z-50"
      style={{
        background: "var(--bg-canvas)",
        borderRight: "1px solid var(--border-subtle)",
      }}
    >
      {/* Masthead — gold logo + title -------------------------- */}
      <div className="px-5 pt-6 pb-4">
        <Link href="/" className="block">
          <div className="flex items-center gap-2.5">
            <div
              className="w-9 h-9 rounded flex items-center justify-center shrink-0"
              style={{
                background:
                  "linear-gradient(135deg, var(--val-gold), var(--val-gold-deep))",
              }}
            >
              <span
                className="font-display font-bold text-base"
                style={{ color: "var(--val-navy)" }}
              >
                M
              </span>
            </div>
            <div className="leading-tight">
              <h1
                className="font-display font-semibold text-[15px]"
                style={{ color: "var(--text-primary)" }}
              >
                Mission Control
              </h1>
              <p
                className="text-[10px] tracking-wider uppercase mt-0.5"
                style={{ color: "var(--text-label)" }}
              >
                Hedge Fund OS
              </p>
            </div>
          </div>
        </Link>
      </div>

      {/* Standalone Dashboard link ----------------------------- */}
      <div className="px-3 mb-2">
        <Link
          href="/"
          className={
            "flex items-center gap-3 px-3 py-2.5 rounded text-sm transition-colors " +
            (path === "/"
              ? "border-l-2 -ml-0.5 pl-[10px]"
              : "")
          }
          style={
            path === "/"
              ? {
                  background: "rgba(201,161,91,0.10)",
                  borderLeftColor: "var(--val-gold)",
                  color: "var(--val-gold)",
                }
              : { color: "var(--text-tertiary)" }
          }
        >
          <LayoutDashboard size={17} />
          <span className="font-medium">Dashboard</span>
        </Link>
      </div>

      {/* Nav sections ------------------------------------------ */}
      <nav className="flex-1 px-3 space-y-4 mt-2 pb-3">
        {SECTIONS.map((section) => (
          <div key={section.label}>
            <p
              className="px-3 text-[10px] font-semibold tracking-wider mb-1.5"
              style={{ color: "var(--text-label)" }}
            >
              {section.label}
            </p>
            <ul className="space-y-px">
              {section.items.map((item) => (
                <NavRow key={item.label} item={item} active={isActive(item.href)} />
              ))}
            </ul>
          </div>
        ))}
      </nav>

      {/* Footer — Antonio Carlos avatar ------------------------ */}
      <div
        className="px-3 py-4"
        style={{ borderTop: "1px solid var(--border-subtle)" }}
      >
        <div
          className="flex items-center gap-2.5 px-2.5 py-2 rounded"
          style={{ background: "var(--bg-elevated)" }}
        >
          <div
            className="w-8 h-8 rounded-full flex items-center justify-center shrink-0"
            style={{
              background:
                "linear-gradient(135deg, var(--val-gold), var(--val-gold-deep))",
            }}
          >
            <span
              className="text-[11px] font-bold"
              style={{ color: "var(--val-navy)" }}
            >
              AC
            </span>
          </div>
          <div className="leading-tight min-w-0">
            <p
              className="text-xs font-medium truncate"
              style={{ color: "var(--text-primary)" }}
            >
              Antonio Carlos
            </p>
            <p
              className="text-[10px]"
              style={{ color: "var(--text-tertiary)" }}
            >
              Analista Principal
            </p>
          </div>
        </div>
      </div>
    </aside>
  );
}

function NavRow({ item, active }: { item: NavItem; active: boolean }) {
  const Icon = item.icon;

  if (item.hidden) {
    return (
      <li>
        <div
          className="flex items-center gap-3 px-3 py-2 rounded text-sm select-none"
          style={{ color: "var(--text-disabled)", cursor: "not-allowed" }}
          title="Não operacional · Ocultado"
        >
          <Icon size={15} />
          <span className="truncate">{item.label}</span>
          <span
            className="ml-auto text-[8px] tracking-wider uppercase font-semibold px-1.5 py-0.5 rounded shrink-0"
            style={{
              background: "var(--bg-elevated)",
              color: "var(--text-disabled)",
              border: "1px solid var(--border-subtle)",
            }}
          >
            ocultado
          </span>
        </div>
      </li>
    );
  }

  return (
    <li>
      <Link
        href={item.href!}
        className={
          "flex items-center gap-3 px-3 py-2 rounded text-sm transition-colors " +
          (active ? "" : "hover:bg-[var(--bg-elevated)]")
        }
        style={
          active
            ? {
                background: "rgba(201,161,91,0.10)",
                color: "var(--val-gold)",
              }
            : { color: "var(--text-secondary)" }
        }
      >
        <Icon size={15} />
        <span>{item.label}</span>
      </Link>
    </li>
  );
}
