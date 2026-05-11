"use client";

// Cross-band focus-ticker context for the home page.
// Band 1 (Lead) sets the spotlight from the briefing; Bands 2/3 react.
// Band 2 user actions (picking a ticker in Compare/DRIP) update focus
// → Band 3 (Deep Review) re-renders. Band 1 stays anchored on the
// "story of the day" — clicking elsewhere does not change the headline.

import { createContext, useContext, useState, ReactNode } from "react";

type Market = "br" | "us";

type FocusState = {
  ticker: string;
  market: Market;
  // Locked = chosen by the headline pipeline; not overwritten by clicks.
  // The state still updates for Deep Review, but the headline ignores it.
  source: "headline" | "user";
};

type FocusContextShape = {
  focus: FocusState;
  setFocus: (ticker: string, market: Market) => void;
  resetToHeadline: () => void;
};

const FocusTickerContext = createContext<FocusContextShape | null>(null);

export function FocusTickerProvider({
  initialTicker,
  initialMarket,
  children,
}: {
  initialTicker: string;
  initialMarket: Market;
  children: ReactNode;
}) {
  const headline = { ticker: initialTicker, market: initialMarket };
  const [focus, setFocusState] = useState<FocusState>({
    ...headline,
    source: "headline",
  });

  function setFocus(ticker: string, market: Market) {
    setFocusState({ ticker, market, source: "user" });
  }

  function resetToHeadline() {
    setFocusState({ ...headline, source: "headline" });
  }

  return (
    <FocusTickerContext.Provider value={{ focus, setFocus, resetToHeadline }}>
      {children}
    </FocusTickerContext.Provider>
  );
}

export function useFocusTicker() {
  const ctx = useContext(FocusTickerContext);
  if (!ctx) {
    throw new Error("useFocusTicker must be used inside <FocusTickerProvider>");
  }
  return ctx;
}
