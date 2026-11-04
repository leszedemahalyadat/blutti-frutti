const C="blutti-v16";
const FILES=["./","index.html","manifest.webmanifest","icon-180.png","icon-192.png","icon-512.png","splash-1170x2532.png","splash-1206x2622.png"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(C).then(c=>Promise.all(FILES.map(u=>fetch(u,{cache:"reload"}).then(r=>{if(r.ok)return c.put(u,r.clone())}).catch(()=>{})))));self.skipWaiting()});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))));self.clients.claim()});
self.addEventListener("fetch",e=>{if(e.request.method!=="GET")return;
  e.respondWith(caches.match(e.request).then(r=>{const f=fetch(e.request,{cache:"no-cache"}).then(res=>{if(res&&res.status===200&&(res.type==="basic"||res.type==="cors")){const cp=res.clone();caches.open(C).then(c=>c.put(e.request,cp))}return res}).catch(()=>r);return r||f}))});
