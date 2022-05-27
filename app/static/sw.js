const CACHE_NAME = 'nebulus-offline';
const urlsToCache = [
    '/',
    '/lms',
    '/dashboard',
    '/settings',
    'https://fonts.googleapis.com/icon?family=Material+Icons|Material+Icons+Outlined|Material+Icons+Two+Tone|Material+Icons+Round|Material+Icons+Sharp',
    "/static/css/tailwind.css",
    "/static/css/common-menus.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.1.0/css/font-awesome.min.css",
    "/static/flowbite/dist/flowbite.js",
    "/static/js/common-menus.js",
    "/static/js/main.js",
    "https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/js/bootstrap.min.js",
    "/static/js/createObjects/lms.js",
    '/profile',
    "/static/images/darkwallpaper.png",
    "/static/images/nebulusCats/v3.gif",
    "/static/images/imageHome.png",
    "/about",
    "points",
    "pricing",
    '/api/developers',
    '/static/people/aaryan.PNG',
    '/static/people/aryav.png',
    '/static/people/gam33r.png',
    '/static/people/jumperplayer.png',
    '/static/people/kevin.gif',
    '/static/people/neel.gif',
    '/static/people/nicholas.png',
    '/static/people/rhyley.webp',
    '/static/people/rishaan.jpg',
    '/static/people/rishaan.jpeg',
    '/static/people/timothy1.webp',
    '/static/people/timothy2.webp',
    '/static/people/vedh.jpeg',
    '/static/people/vivian.webp',
    '/static/images/icons/calculator.png',
    '/static/images/icons/art.svg',
    '/static/images/icons/chem.png',
    '/static/images/icons/dictionary.png',
    '/static/images/icons/history.svg',
    '/static/images/icons/language.svg',
    '/static/images/icons/map.png',
    '/static/images/icons/next.svg',
    '/static/images/icons/periodic table.png',
    '/static/images/icons/physics.png',
    '/static/images/icons/science.svg',
    '/static/images/icons/sports.png',
    '/static/images/icons/sport.svg',
    '/static/images/logos/apple.png',
    '/static/images/logos/battlenet.png',
    '/static/images/logos/calendar.png',
    '/static/images/logos/canvas.png',
    '/static/images/logos/classroom.png',
    '/static/images/logos/discord.png',
    '/static/images/logos/docs.png',
    '/static/images/logos/drive.png',
    '/static/images/logos/dropbox.png',
    '/static/images/logos/facebook.png',
    '/static/images/logos/github.png',
    '/static/images/logos/gmail.png',
    '/static/images/logos/google.png',
    '/static/images/logos/instagram.png',
    '/static/images/logos/meet.png',
    '/static/images/logos/microsoft.png',
    '/static/images/logos/paypal.png',
    '/static/images/logos/reddit.png',
    '/static/images/logos/replit.png',
    '/static/images/logos/schoology.png',
    '/static/images/logos/sheets.png',
    '/static/images/logos/slides.png',
    '/static/images/logos/spotify.png',
    '/static/images/logos/steam.png',
    '/static/images/logos/twitch.png',
    '/static/images/logos/twitter.png',
    '/static/images/logos/wechat.png',
    '/static/images/logos/xbox.png',
    '/static/images/logos/youtube.png',
    '/static/images/logos/zoom.png',
    '/static/images/nebulusCats/100_cat.png',
    '/static/images/nebulusCats/black_cat.png',
    '/static/images/nebulusCats/blue_cat.png',
    '/static/images/nebulusCats/blurple_cat.png',
    '/static/images/nebulusCats/cake_cat.png',
    '/static/images/nebulusCats/cat1.png',
    '/static/images/nebulusCats/green_cat.png',
    '/static/images/nebulusCats/mainLogo.png',
    '/static/images/nebulusCats/mountains.png',
    '/static/images/nebulusCats/newBlue.png',
    '/static/images/nebulusCats/newBlurple.png',
    '/static/images/nebulusCats/newGreen.png',
    '/static/images/nebulusCats/newJade.png',
    '/static/images/nebulusCats/newPink.png',
    '/static/images/nebulusCats/newRed.png',
    '/static/images/nebulusCats/newYellow.png',
    '/static/images/nebulusCats/ocean_cat.png',
    '/static/images/nebulusCats/pink_cat.png',
    '/static/images/nebulusCats/pizza.png',
    '/static/images/nebulusCats/popTart.png',
    '/static/images/nebulusCats/red_cat.png',
    '/static/images/nebulusCats/river_cat.png',
    '/static/images/nebulusCats/v1.png',
    '/static/images/nebulusCats/v2.gif',
    //'/static/images/nebulusCats/v3.gif',
    '/static/images/nebulusCats/yellow_cat.png',



];

self.addEventListener('install', function (event) {
    // install files needed offline
    event.waitUntil(
        caches.open(CACHE_NAME).then(function (cache) {
            console.log('Opened cache');
            return cache.addAll(urlsToCache);
        })
    );
});

self.addEventListener('fetch', function (event) {
    // every request from our site, passes through the fetch handler
    console.log('I am a request with url:', event.request.clone().url);
    event.respondWith(
        // check all the caches in the browser and find
        // out whether our request is in any of them
        caches.match(event.request).then(function (response) {
            if (response) {
                // if we are here, that means there's a match
                //return the response stored in browser
                return response;
            }

            // no match in cache, use the network instead
            return fetch(event.request);
        })
    );
});
