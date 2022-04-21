
module.exports = {
    purge: false,
    darkMode: 'class',
    content: ['./app/templates/**/*.html', './app/static/**/*.{js,css}', './app/static/flowbite/**/*.js'],
    theme: {
            fontFamily: {
                sans: ['Spotify-Font', "sans-serif"],
            },

    },
    plugins: [
        require('@tailwindcss/typography'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
        require('./app/static/flowbite/plugin')
    ]
};
