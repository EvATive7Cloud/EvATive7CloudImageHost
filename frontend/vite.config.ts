import vue from "@vitejs/plugin-vue";
// @ts-expect-error type missing in export map
import eruda from "vite-plugin-eruda";
import { fileURLToPath, URL } from "node:url";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const backendUrl = env.BACKEND_URL ?? "http://127.0.0.1:8000";

  return {
    plugins: [vue(), eruda()],
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
    server: {
      proxy: {
        "/api": {
          target: backendUrl,
          changeOrigin: true,
        },
        "/imgs": {
          target: backendUrl,
          changeOrigin: true,
        },
      },
    },
  };
});
