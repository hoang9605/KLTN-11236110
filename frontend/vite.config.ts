import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Chạy dev: API ở http://127.0.0.1:8000 (uvicorn server.main:app), Vite chuyển tiếp /api
export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: { output: { manualChunks: { cytoscape: ["cytoscape"], react: ["react", "react-dom", "react-router-dom"] } } },
  },
  server: {
    port: 5173,
    proxy: { "/api": process.env.API_URL ?? "http://127.0.0.1:8000" },
  },
});
