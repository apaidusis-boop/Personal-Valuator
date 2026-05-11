import { buildStocksData } from "@/lib/stocks-data";
import { StocksView } from "@/components/stocks/stocks-view";
import type { Metadata } from "next";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "Stocks · Mission Control" };

export default function StocksPage() {
  const data = buildStocksData();
  return <StocksView data={data} />;
}
