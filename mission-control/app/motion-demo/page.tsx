"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";

const cardStyle: React.CSSProperties = {
  background: "var(--bg-elevated)",
  border: "1px solid var(--border-subtle)",
  padding: "1.5rem",
  borderRadius: "8px",
};

const labelStyle: React.CSSProperties = {
  color: "var(--text-label)",
  fontSize: "0.75rem",
  textTransform: "uppercase",
  letterSpacing: "0.08em",
  marginBottom: "1rem",
};

const dotStyle: React.CSSProperties = {
  width: 16,
  height: 16,
  background: "var(--val-gold)",
  borderRadius: "50%",
  display: "inline-block",
  margin: 4,
};

export default function MotionDemoPage() {
  const [show, setShow] = useState(true);
  const [items, setItems] = useState([1, 2, 3]);

  return (
    <div style={{ padding: "2rem", display: "grid", gap: "1.5rem", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))" }}>
      <h1 style={{ gridColumn: "1 / -1", fontFamily: "var(--font-playfair, serif)", color: "var(--text-primary)" }}>
        Motion API playground
      </h1>

      <section style={cardStyle}>
        <div style={labelStyle}>1 · animate (continuous)</div>
        <motion.ul
          style={{ ...dotStyle, listStyle: "none", padding: 0, margin: "0 auto" }}
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
        />
      </section>

      <section style={cardStyle}>
        <div style={labelStyle}>2 · initial → animate</div>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          style={{ color: "var(--text-primary)" }}
        >
          Fades in on mount.
        </motion.div>
      </section>

      <section style={cardStyle}>
        <div style={labelStyle}>3 · whileHover / whileTap</div>
        <motion.button
          whileHover={{ scale: 1.05, backgroundColor: "var(--val-gold)" }}
          whileTap={{ scale: 0.95 }}
          style={{
            padding: "0.75rem 1.25rem",
            background: "var(--val-graphite-2)",
            color: "var(--text-primary)",
            border: "1px solid var(--border-subtle)",
            borderRadius: 6,
            cursor: "pointer",
          }}
        >
          Hover &amp; press
        </motion.button>
      </section>

      <section style={cardStyle}>
        <div style={labelStyle}>4 · drag</div>
        <motion.div
          drag
          dragConstraints={{ left: -50, right: 50, top: -30, bottom: 30 }}
          whileDrag={{ scale: 1.1 }}
          style={{
            width: 60,
            height: 60,
            background: "var(--val-blue)",
            borderRadius: 8,
            cursor: "grab",
          }}
        />
      </section>

      <section style={cardStyle}>
        <div style={labelStyle}>5 · spring</div>
        <motion.div
          animate={{ x: show ? 80 : 0 }}
          transition={{ type: "spring", stiffness: 200, damping: 12 }}
          style={{ width: 40, height: 40, background: "var(--val-green)", borderRadius: "50%" }}
        />
        <button
          onClick={() => setShow((s) => !s)}
          style={{ marginTop: "1rem", color: "var(--accent-glow)", background: "transparent", border: "none", cursor: "pointer" }}
        >
          toggle →
        </button>
      </section>

      <section style={cardStyle}>
        <div style={labelStyle}>6 · AnimatePresence</div>
        <AnimatePresence mode="wait">
          {show && (
            <motion.div
              key="panel"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              style={{ color: "var(--text-primary)", overflow: "hidden" }}
            >
              Mount/unmount with exit animation.
            </motion.div>
          )}
        </AnimatePresence>
      </section>

      <section style={cardStyle}>
        <div style={labelStyle}>7 · variants (stagger)</div>
        <motion.ul
          style={{ listStyle: "none", padding: 0, margin: 0, display: "flex" }}
          initial="hidden"
          animate="visible"
          variants={{
            hidden: {},
            visible: { transition: { staggerChildren: 0.1 } },
          }}
        >
          {[0, 1, 2, 3, 4].map((i) => (
            <motion.li
              key={i}
              variants={{
                hidden: { opacity: 0, y: -10 },
                visible: { opacity: 1, y: 0 },
              }}
              style={dotStyle}
            />
          ))}
        </motion.ul>
      </section>

      <section style={cardStyle}>
        <div style={labelStyle}>8 · layout (FLIP)</div>
        <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: 6 }}>
          {items.map((n) => (
            <motion.li
              key={n}
              layout
              transition={{ type: "spring", stiffness: 300, damping: 25 }}
              onClick={() => setItems((xs) => xs.filter((x) => x !== n))}
              style={{
                padding: "0.5rem 0.75rem",
                background: "var(--val-graphite-2)",
                color: "var(--text-primary)",
                borderRadius: 4,
                cursor: "pointer",
              }}
            >
              item {n} (click to remove)
            </motion.li>
          ))}
        </ul>
        <button
          onClick={() => setItems((xs) => [...xs, Math.max(0, ...xs) + 1])}
          style={{ marginTop: "0.75rem", color: "var(--accent-glow)", background: "transparent", border: "none", cursor: "pointer" }}
        >
          + add
        </button>
      </section>
    </div>
  );
}
