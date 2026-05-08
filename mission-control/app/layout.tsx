import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/sidebar";
import TopBar from "@/components/topbar";
import ChatWidget from "@/components/chat-widget";
import HedgeBanner from "@/components/hedge-banner";
import ThemeInit from "@/components/theme-init";
import TickerSideSheet from "@/components/ticker-sidesheet";
import { listOpenActions } from "@/lib/db";

export const metadata: Metadata = {
  title: "Mission Control — Hedge Fund OS",
  description:
    "Personal investment intelligence — local-first agent control panel",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  // Server-side count for the bell indicator on TopBar.
  let openActions = 0;
  try {
    openActions = listOpenActions(60).length;
  } catch {
    /* DBs missing on first boot — render with zero */
  }

  return (
    <html
      lang="pt-BR"
      className="h-full antialiased"
      suppressHydrationWarning
    >
      <head suppressHydrationWarning>
        <ThemeInit />
        <link
          rel="preconnect"
          href="https://fonts.googleapis.com"
        />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700&family=JetBrains+Mono:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </head>
      <body suppressHydrationWarning>
        <Sidebar />
        <TopBar openActions={openActions} />
        <main
          className="min-h-screen"
          style={{
            marginLeft: "var(--sidebar-w)",
            paddingTop: "var(--topbar-h)",
          }}
        >
          <HedgeBanner />
          {children}
        </main>
        <TickerSideSheet />
        <ChatWidget />
      </body>
    </html>
  );
}
