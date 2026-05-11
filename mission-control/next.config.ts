import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // better-sqlite3 is a native binding; tell webpack/turbopack to leave it external.
  serverExternalPackages: ["better-sqlite3"],
  // Allow embedding into iframes/dashboards on the same machine.
  poweredByHeader: false,
};

export default nextConfig;
