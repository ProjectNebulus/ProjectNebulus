
module.exports = {
    purge: false,
    darkMode: 'class',
    content: ['./app/templates/**/*.html', './app/static/**/*.{js,css}', './app/static/flowbite/**/*.js'],
    theme: {
            fontFamily: {
                sans: ['Spotify-Font', "Noto Sans", "Noto Sans SC", "Noto Sans TC", "Noto Sans JP",  "Noto Sans KR",  "Noto Sans Thai", "sans-serif"],
            },
        extend: {
                backgroundImage: {
                    'signin-bg': "url('/static/images/background-images/signin-background.png')",
                }
        }

    },
    plugins: [
        require('@tailwindcss/typography'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
        require('./app/static/flowbite/plugin'),
        require('@tailwindcss/line-clamp'),
    ]
};
