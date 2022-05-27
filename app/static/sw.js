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
    '/profile'
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
