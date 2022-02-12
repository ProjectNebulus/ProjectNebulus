module.exports = {
  content: ["./templates/**/*.html", "./static/**/*.{js,css}"],
  theme: {
    extend: {},
  },
  plugins: [
      require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
    require('@tailwindcss/line-clamp'),
    require('@tailwindcss/aspect-ratio'),],
}
