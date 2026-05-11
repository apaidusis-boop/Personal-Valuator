import { buildDeskData } from "@/lib/desk-data";
import { DeskView } from "@/components/desk/desk-view";
import type { Metadata } from "next";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Desk · Mission Control" };

export default function DeskPage() {
  const data = buildDeskData();
  return <DeskView data={data} />;
}
