const defaultTheme = require("tailwindcss/defaultTheme")

const config = {
  content: ["./src/**/*.{html,js,svelte,ts}"],

  theme: {
    extend: {
      fontFamily: {
        sans: ["Open Sans", ...defaultTheme.fontFamily.sans],
        oswald: ["Oswald", ...defaultTheme.fontFamily.sans],
      },
      colors: {
        //ToDo: rename "lm-orange"
        orange: {
          DEFAULT: "#FC941E",
          50: "#FFF3E6",
          100: "#FEE7CD",
          200: "#FECF9A",
          300: "#FDB768",
          400: "#FCA036",
          500: "#FC941E",
          600: "#E07803",
          700: "#A95A02",
          800: "#713D02",
          900: "#3A1F01",
        },
        "lm-orange": {
          DEFAULT: "#FC941E",
          50: "#FFF3E6",
          100: "#FEE7CD",
          200: "#FECF9A",
          300: "#FDB768",
          400: "#FCA036",
          500: "#FC941E",
          600: "#E07803",
          700: "#A95A02",
          800: "#713D02",
          900: "#3A1F01",
        },
        //ToDO: rename "lm-pelorous"
        pelorous: {
          DEFAULT: "#44B7B5",
          50: "#ECF8F8",
          100: "#DAF1F1",
          200: "#B5E3E3",
          300: "#8FD6D4",
          400: "#6AC8C6",
          500: "#44B7B5",
          600: "#358E8D",
          700: "#266565",
          800: "#163C3C",
          900: "#071313",
        },
        "lm-pelorous": {
          DEFAULT: "#44B7B5",
          50: "#ECF8F8",
          100: "#DAF1F1",
          200: "#B5E3E3",
          300: "#8FD6D4",
          400: "#6AC8C6",
          500: "#44B7B5",
          600: "#358E8D",
          700: "#266565",
          800: "#163C3C",
          900: "#071313",
        },
        "lm-purple": {
          DEFAULT: "#7886EC",
          50: "#F1F3FD",
          100: "#D6DBF9",
          200: "#BBC2F5",
          300: "#A0AAF2",
          400: "#8592EE",
          500: "#7886EC",
        },
        "lm-violet": {
          DEFAULT: "#AA70DD",
          50: "#F7F1FC",
          100: "#E6D4F5",
          200: "#D5B8EE",
          300: "#C49BE7",
          400: "#B37FE0",
          500: "#AA70DD",
        },
        "lm-green": {
          DEFAULT: "#A0D875",
          50: "#F5FBF1",
          100: "#E2F3D6",
          200: "#D0EBBA",
          300: "#BDE39E",
          400: "#AADC83",
          500: "#A0D875",
          700: "#477722",
          light: "#E2F3D6",
          dark: "#477722",
        },
        "lm-red": {
          DEFAULT: "#E8726A",
          50: "#FDF1F0",
          100: "#F8D5D2",
          200: "#F3B8B5",
          300: "#EF9C97",
          400: "#EA8079",
          500: "#E8726A",
          700: "#B11B1B",
          light: "#F8D5D2",
          dark: "#B11B1B",
        },
        "lm-yellow": {
          DEFAULT: "#E7CC41",
          50: "#FDFAEC",
          100: "#F8F0C6",
          200: "#F3E6A0",
          300: "#EEDB7A",
          400: "#E9D154",
          500: "#E7CC41",
        },
        "lm-red-deleted": "hsl(0,33%,68%)",
        gray: {
          dark: "#666666",
          medium: "#999999",
          light: "#CCCCCC",
        },
        "lm-black": "#190E00",
        "lm-dark": "#4a4a4a",
        "lm-lightgray": "#f9f9f9",
        "lm-darkgray": "#c4c4c4",
      },
      dropShadow: {
        marker: "3.5px 2.5px 0px rgba(0, 0, 0, 0.35)",
      },
      animation: {
        fadeToWhite: "fadeToWhite 1s ease-in-out normal forwards",
        fadeToGray: "fadeToGray 1s ease-in-out normal forwards",
      },
      keyframes: theme => ({
        fadeToWhite: {
          "0%": { backgroundColor: theme("colors.white") },
          "10%": { backgroundColor: theme("colors.orange.200") },
          "100%": { backgroundColor: theme("colors.orange.50") },
        },
        fadeToGray: {
          "0%": { backgroundColor: theme("colors.white") },
          "100%": { backgroundColor: theme("colors.gray.700") },
        },
      }),
    },
  },

  plugins: [
    function ({ addBase, theme }) {
      function extractColorVars(colorObj, colorGroup = "") {
        return Object.keys(colorObj).reduce((vars, colorKey) => {
          const value = colorObj[colorKey]

          const newVars =
            typeof value === "string"
              ? { [`--color${colorGroup}-${colorKey}`]: value }
              : extractColorVars(value, `-${colorKey}`)

          return { ...vars, ...newVars }
        }, {})
      }

      addBase({
        ":root": extractColorVars(theme("colors")),
      })
    },
  ],
}

module.exports = config
