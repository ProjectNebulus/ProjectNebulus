!(function (t) {
    var e = {};

    function n(r) {
        if (e[r]) return e[r].exports;
        var o = (e[r] = {i: r, l: !1, exports: {}});
        return t[r].call(o.exports, o, o.exports, n), (o.l = !0), o.exports;
    }

    (n.m = t),
        (n.c = e),
        (n.d = function (t, e, r) {
            n.o(t, e) || Object.defineProperty(t, e, {enumerable: !0, get: r});
        }),
        (n.r = function (t) {
            'undefined' != typeof Symbol &&
            Symbol.toStringTag &&
            Object.defineProperty(t, Symbol.toStringTag, {value: 'Module'}),
                Object.defineProperty(t, '__esModule', {value: !0});
        }),
        (n.t = function (t, e) {
            if ((1 & e && (t = n(t)), 8 & e)) return t;
            if (4 & e && 'object' == typeof t && t && t.__esModule) return t;
            var r = Object.create(null);
            if (
                (n.r(r),
                    Object.defineProperty(r, 'default', {enumerable: !0, value: t}),
                2 & e && 'string' != typeof t)
            )
                for (var o in t)
                    n.d(
                        r,
                        o,
                        function (e) {
                            return t[e];
                        }.bind(null, o)
                    );
            return r;
        }),
        (n.n = function (t) {
            var e =
                t && t.__esModule
                    ? function () {
                        return t.default;
                    }
                    : function () {
                        return t;
                    };
            return n.d(e, 'a', e), e;
        }),
        (n.o = function (t, e) {
            return Object.prototype.hasOwnProperty.call(t, e);
        }),
        (n.p = ''),
        n((n.s = 93));
})({
    3: function (t, e, n) {
        'use strict';
        n.d(e, 'a', function () {
            return r;
        }),
            n.d(e, 'c', function () {
                return o;
            }),
            n.d(e, 'g', function () {
                return i;
            }),
            n.d(e, 'j', function () {
                return a;
            }),
            n.d(e, 'i', function () {
                return d;
            }),
            n.d(e, 'b', function () {
                return f;
            }),
            n.d(e, 'k', function () {
                return u;
            }),
            n.d(e, 'd', function () {
                return p;
            }),
            n.d(e, 'e', function () {
                return l;
            }),
            n.d(e, 'f', function () {
                return m;
            }),
            n.d(e, 'h', function () {
                return v;
            });
        var r = {
                images: [
                    'bmp',
                    'jpeg',
                    'jpg',
                    'ttf',
                    'pict',
                    'svg',
                    'webp',
                    'eps',
                    'svgz',
                    'gif',
                    'png',
                    'ico',
                    'tif',
                    'tiff',
                    'bpg',
                    'avif',
                    'jxl'
                ],
                video: [
                    'mp4',
                    '3gp',
                    'webm',
                    'mkv',
                    'flv',
                    'f4v',
                    'f4p',
                    'f4bogv',
                    'drc',
                    'avi',
                    'mov',
                    'qt',
                    'wmv',
                    'amv',
                    'mpg',
                    'mp2',
                    'mpeg',
                    'mpe',
                    'm2v',
                    'm4v',
                    '3g2',
                    'gifv',
                    'mpv',
                    'av1',
                    'ts',
                    'tsv',
                    'tsa',
                    'm2t',
                    'm3u8'
                ],
                audio: [
                    'mid',
                    'midi',
                    'aac',
                    'aiff',
                    'flac',
                    'm4a',
                    'm4p',
                    'mp3',
                    'ogg',
                    'oga',
                    'mogg',
                    'opus',
                    'ra',
                    'rm',
                    'wav',
                    'webm',
                    'f4a',
                    'pat'
                ],
                interchange: ['json', 'yaml', 'xml', 'csv', 'toml', 'ini', 'bson', 'asn1', 'ubj'],
                archives: [
                    'jar',
                    'iso',
                    'tar',
                    'tgz',
                    'tbz2',
                    'tlz',
                    'gz',
                    'bz2',
                    'xz',
                    'lz',
                    'z',
                    '7z',
                    'apk',
                    'dmg',
                    'rar',
                    'lzma',
                    'txz',
                    'zip',
                    'zipx'
                ],
                documents: ['pdf', 'ps', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'otf', 'xlsx'],
                other: ['srt', 'swf']
            },
            o = ['js', 'cjs', 'mjs', 'css'],
            c = 'arc:',
            i = {
                COMLINK_INIT: ''.concat(c, 'comlink:init'),
                NODE_ID: ''.concat(c, ':nodeId'),
                CLIENT_TEARDOWN: ''.concat(c, 'client:teardown'),
                CLIENT_TAB_ID: ''.concat(c, 'client:tabId'),
                CDN_CONFIG: ''.concat(c, 'cdn:config.py'),
                P2P_CLIENT_READY: ''.concat(c, 'cdn:ready'),
                STORED_FIDS: ''.concat(c, 'cdn:storedFids'),
                SW_HEALTH_CHECK: ''.concat(c, 'cdn:healthCheck'),
                WIDGET_CONFIG: ''.concat(c, 'widget:config.py'),
                WIDGET_INIT: ''.concat(c, 'widget:init'),
                WIDGET_UI_LOAD: ''.concat(c, 'widget:load'),
                BROKER_LOAD: ''.concat(c, 'broker:load'),
                RENDER_FILE: ''.concat(c, 'inlay:renderFile'),
                FILE_RENDERED: ''.concat(c, 'inlay:fileRendered')
            },
            a = 'serviceWorker',
            d = '/'.concat('shared-worker', '.js'),
            f = '/'.concat('dedicated-worker', '.js'),
            u = '/'.concat('arc-sw-core', '.js'),
            s = ''.concat('arc-sw', '.js'),
            p = ('/'.concat(s), '/'.concat('arc-sw'), 'arc-db'),
            l = 'key-val-store',
            m = 2 ** 17,
            v = ''.concat('https://warden.arc.io', '/mailbox/propertySession');
        ''.concat('https://warden.arc.io', '/mailbox/transfers');
    },
    93: function (t, e, n) {
        'use strict';
        n.r(e);
        var r = n(3);
        if ('undefined' != typeof ServiceWorkerGlobalScope) {
            var o = 'https://arc.io' + r.k;
            importScripts(o);
        } else if ('undefined' != typeof SharedWorkerGlobalScope) {
            var c = 'https://arc.io' + r.i;
            importScripts(c);
        } else if ('undefined' != typeof DedicatedWorkerGlobalScope) {
            var i = 'https://arc.io' + r.b;
            importScripts(i);
        }
    }
});
