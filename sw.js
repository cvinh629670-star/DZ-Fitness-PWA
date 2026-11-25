const CACHE = 'dz-fitness-pwa-v36';
const ASSETS = ['./index.html','./interface.css?v=31','./chart-layout.js?v=2','./training-hero.jpg?v=7954d46','./manifest.webmanifest','./icon-180.png','./icon-192.png','./icon-512.png'];
self.addEventListener('install', e => e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting())));
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('dz-fitness-pwa-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch', e => {
 if(e.request.method!=='GET'||new URL(e.request.url).origin!==self.location.origin) return;
 if(e.request.mode==='navigate') { e.respondWith(fetch(e.request).then(r=>{if(r.ok){const copy=r.clone(); e.waitUntil(caches.open(CACHE).then(c=>c.put('./index.html',copy)));}return r;}).catch(()=>caches.match('./index.html'))); return; }
 e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)));
});
