const defaultTheme = require("tailwindcss/defaultTheme");

const config = {
  content: ["./src/**/*.{vue,html,js,ts}"],

  theme: {
    extend: {
      colors: {
        orange: {
          50: "hsl(32, 97%, 95%)",
          200: "hsl(32, 97%, 65%)",
          DEFAULT: "hsl(32, 97%, 55%)",
          600: "hsl(32, 97%, 45%)",
        },
        teal: {
          200: "hsl(179, 46%, 59%)",
          DEFAULT: "hsl(179, 46%, 49%)",
          600: "hsl(179, 46%, 39%)",
        },
        "lm-dark": "#4a4a4a",
        "lm-light": "#f9f9f9",
      },
      animation: {
        "fadeToWhite": "fadeToWhite 1s ease-in-out normal forwards",
      },

      // that is actual animation
      keyframes: (theme) => ({
        fadeToWhite: {
          "0%": { backgroundColor: theme("colors.white") },
          "10%": { backgroundColor: theme("colors.orange.200") },
          "100%": { backgroundColor: theme("colors.orange.50") },
        },
      }),
    },
  },
  // plugins: [require("@tailwindcss/forms")],
};

module.exports = config;
