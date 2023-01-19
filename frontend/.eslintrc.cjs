module.exports = {
  root: true,
  parser: "@typescript-eslint/parser",
  extends: ["eslint:recommended", "plugin:@typescript-eslint/recommended", "prettier"],
  plugins: ["svelte3", "@typescript-eslint", "testing-library", "jest-dom"],
  ignorePatterns: ["*.cjs"],
  overrides: [{ files: ["*.svelte"], processor: "svelte3/svelte3" }],
  settings: {
    "svelte3/typescript": () => require("typescript"),
  },
  parserOptions: {
    sourceType: "module",
    ecmaVersion: 2020,
  },
  globals: {
    google: "readonly",
  },
  env: {
    browser: true,
    es2017: true,
    node: true,
  },
}
