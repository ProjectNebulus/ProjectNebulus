if ('serviceWorker' in navigator) {
    // we are checking here to see if the browser supports the  service worker api
    window.addEventListener('load', function () {
        navigator.serviceWorker.register('/static/js/sw.js').then(
            function (registration) {
                // Registration was successful
                console.log(
                    'Service Worker registration was successful with scope: ',
                    registration.scope
                );
            },
            function (err) {
                // registration failed :(
                console.log('ServiceWorker registration failed: ', err);
            }
        );
    });
}

var CACHE_NAME = 'nebulus-offline';
var urlsToCache = [
    '/',
    '/static/tailwind.css',
    '/static/createCourse.css',
    '/static/createCourse.js',
    '/static/main.js',
    '/static/dashboard.js',
    '/static/profile.js',
    '/static/signin.js',
    '/static/signup.js',
    '/signin',
    '/signup',
    '/lms',
    '/dashboard',
    '/settings',
    '/profile',

    'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.0/jquery.min.js'
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
    // I have proof
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

var urlsToCache = [

    'https://nebulus.ml/',
    'https://nebulus.ml/static/styles.css',
    'https://nebulus.ml/static/tailwind.css',
    'https://nebulus.ml/static/createCourse.css',
    'https://nebulus.ml/static/createCourse.js',
    'https://nebulus.ml/static/main.js',
    'https://nebulus.ml/static/dashboard.js',
    'https://nebulus.ml/static/profile.js',
    'https://nebulus.ml/static/signin.js',
    'https://nebulus.ml/static/signup.js',
    'https://nebulus.ml/signin',
    'https://nebulus.ml/signup',
    'https://nebulus.ml/lms',
    'https://nebulus.ml/dashboard',
    'https://nebulus.ml/settings',
    'https://nebulus.ml/profile',
    '/',
    '/static/tailwind.css',
    '/static/createCourse.css',
    '/static/createCourse.js',
    '/static/main.js',
    '/static/dashboard.js',
    '/static/profile.js',
    '/static/signin.js',
    '/static/signup.js',
    '/signin',
    '/signup',
    '/lms',
    '/dashboard',
    '/settings',
    '/profile',


    'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.0/jquery.min.js'
];
