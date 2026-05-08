import type { Metadata } from "next";
import FilingsView from "./view";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Filings · Mission Control" };

export default function FilingsPage() {
  return <FilingsView />;
}
