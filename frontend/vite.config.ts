import { sentrySvelteKit } from "@sentry/sveltekit"
import { sveltekit } from "@sveltejs/kit/vite"
import { defineConfig } from "vite"
import { isoImport } from "vite-plugin-iso-import"

export default defineConfig({
  plugins: [
    sentrySvelteKit({
      autoUploadSourceMaps: false,
    }),
    sveltekit(),
    isoImport(),
  ],
  envDir: "..",
  test: {
    include: ["src/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}"],
    globals: true,
    environment: "jsdom",
  },
  server: { port: 3000, host: "0.0.0.0" },
  preview: { port: 3000 },
})
