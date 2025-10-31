import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

const proxyTarget = process.env.VITE_API_PROXY || "http://localhost:5000";
const backendStatic = resolve(__dirname, "../backend/app/static/frontend");

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: proxyTarget,
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: backendStatic,
    emptyOutDir: true,
    sourcemap: true
  }
});
