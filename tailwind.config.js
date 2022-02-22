module.exports = {
  darkMode: 'class',
    content: ['./templates/**/*.html', './static/**/*.{js,css}',"./node_modules/flowbite/**/*.js"]
  
    theme: {
        extend: {}
    },
    plugins: [
        require('@tailwindcss/typography'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio')
        require('flowbite/plugin')
    ]
};
