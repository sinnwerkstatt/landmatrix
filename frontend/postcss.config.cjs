const tailwindcss = require("tailwindcss")
const autoprefixer = require("autoprefixer")
const postcss_import = require("postcss-import")

const config = {
  plugins: [
    postcss_import(),
    //Some plugins, like tailwindcss/nesting, need to run before Tailwind,
    tailwindcss(),
    //But others, like autoprefixer, need to run after,
    autoprefixer,
  ],
}

module.exports = config