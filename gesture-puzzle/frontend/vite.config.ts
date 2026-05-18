// frontend/vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Proxy API calls to FastAPI during development
    // so you don't need CORS workarounds in dev
    proxy: {
      "/api":        "http://localhost:8000",
      "/ws":         { target: "ws://localhost:8000", ws: true },
      "/health":     "http://localhost:8000",
    },
  },
  build: {
    outDir: "dist",
  },
});
