import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/sidebar";
import ChatWidget from "@/components/chat-widget";

export const metadata: Metadata = {
  title: "Mission Control — LocalClaw",
  description: "Personal investment intelligence — local-first agent control panel",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="pt-BR" className="h-full antialiased">
      <body className="min-h-screen flex">
        <Sidebar />
        <main className="flex-1 overflow-y-auto">
          {children}
        </main>
        <ChatWidget />
      </body>
    </html>
  );
}
