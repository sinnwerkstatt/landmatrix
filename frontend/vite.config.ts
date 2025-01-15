import { sentrySvelteKit } from "@sentry/sveltekit"
import { sveltekit } from "@sveltejs/kit/vite"
import { svelteTesting } from "@testing-library/svelte/vite"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [
    sentrySvelteKit({
      autoUploadSourceMaps: false,
    }),
    sveltekit(),
    svelteTesting(),
  ],
  envDir: "..",
  test: {
    include: ["src/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}"],
    globals: true,
    environment: "jsdom",
    setupFiles: "./setupTests.ts",
  },
  server: { port: 3000, host: "0.0.0.0" },
  preview: { port: 3000 },
})
