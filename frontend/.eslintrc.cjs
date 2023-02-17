module.exports = {
  root: true,
  parser: "@typescript-eslint/parser",
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:import/recommended",
    "plugin:import/typescript",
    "prettier", // should be last
  ],
  plugins: ["svelte3", "@typescript-eslint", "testing-library", "jest-dom"],
  ignorePatterns: ["*.cjs"],
  overrides: [
    {
      files: ["*.svelte"],
      processor: "svelte3/svelte3",
      rules: {
        // https://github.com/sveltejs/eslint-plugin-svelte3/blob/master/OTHER_PLUGINS.md
        "import/no-unresolved": [
          "error",
          {
            ignore: ["^\\$app/"],
          },
        ],
      },
    },
  ],
  settings: {
    "svelte3/typescript": true,
    "import/resolver": {
      typescript: true,
      node: true,
    },
  },
  rules: {
    "import/no-named-as-default-member": "off",
    "import/order": [
      "warn",
      {
        groups: [
          "builtin", // Built-in imports (come from NodeJS native) go first
          "external", // <- External imports
          "internal", // <- Absolute imports
          ["sibling", "parent"], // <- Relative imports
          "unknown", // <- unknown
        ],
        pathGroups: [
          {
            pattern: "$app/**",
            group: "internal",
            position: "before",
          },
          {
            pattern: "$lib/**",
            group: "internal",
            position: "before",
          },
          {
            pattern: "$components/**",
            group: "internal",
            position: "before",
          },
        ],
        "newlines-between": "always",
        alphabetize: {
          caseInsensitive: true,
        },
      },
    ],
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
