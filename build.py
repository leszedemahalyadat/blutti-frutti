#!/usr/bin/env python3
# Blutti Frutti – build: src/blutti-frutti.html (forrás) -> index.html (kiadott PWA-lap)
# Használat: python3 build.py [kimenet]   (alapértelmezés: index.html a repo gyökerében)
import re, json, sys, os
ROOT=os.path.dirname(os.path.abspath(__file__))
OUT=sys.argv[1] if len(sys.argv)>1 else os.path.join(ROOT,'index.html')
src=open(os.path.join(ROOT,'src','blutti-frutti.html'),encoding='utf8').read()
# kiszedjük a személyes adatokat
alt=[]
# import: bevétel-csomag összefésülése
old='$("doImp").onclick=function(){try{var o=JSON.parse($("impText").value);'
assert old in src
src=src.replace(old,'$("doImp").onclick=function(){try{var o=JSON.parse($("impText").value);if(o&&o.kind==="bevetel-import"){var ids={};S.entries.forEach(function(e){ids[e.id]=1});var n=0;o.entries.forEach(function(e){if(!ids[e.id]){S.entries.push(e);n++}});save();resetCache();$("impBox").hidden=true;$("impText").value="";renderAll();toast(n+" bevételes nap betöltve");return}')
# banner: ha nincs bevétel
old='if(fixedSum()===0&&S.settings.manualLimit==null){'
assert old in src
src=src.replace(old,'if(expectedIncome()===0&&S.settings.manualLimit==null){b.innerHTML=\'<div class="banner warn"><div><b>Még nincs napi plafon.</b> Töltsd be a kezdő adatokat (Gépház → Visszatöltés), vagy írd be, mennyi lé jön havonta.</div><button class="btn" type="button" data-go="beall" style="padding:8px 12px;font-size:13px">Beállítom</button></div>\'}else '+old)
src=src.replace('Az Altegióból betöltött bevételek visszakerülnek.','A betöltött lé is törlődik.')
src=src.replace('S=fresh();S.settings=keep;','S=fresh();S.settings=keep;')
title,rest=src.split('\n',1)
head='''<!doctype html>
<html lang="hu">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
'''+title+'''
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Blutti Frutti">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#FFFFFF">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<!-- indítóképek: iPhone 13 / 13 Pro (390×844 @3x) és iPhone 16 Pro (402×874 @3x) -->
<link rel="apple-touch-startup-image" href="splash-1170x2532.png" media="(device-width: 390px) and (device-height: 844px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel="apple-touch-startup-image" href="splash-1206x2622.png" media="(device-width: 402px) and (device-height: 874px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)">
<link rel="icon" href="icon-192.png">
<style>html{padding-top:env(safe-area-inset-top,0px);min-height:100%}body{margin:0}</style>
</head>
<body>
'''
rest=rest.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','',1)
tail='''
<script>
// Ha Safariban nyitották meg (nem főképernyőről), mutassuk, hogyan kell felrakni
(function(){var ios=/iPhone|iPad/.test(navigator.userAgent),standalone=window.navigator.standalone===true||matchMedia("(display-mode: standalone)").matches;
  var seen=false;try{seen=localStorage.getItem("blutti-a2hs")==="1"}catch(e){}
  if(ios&&!standalone&&!seen){var b=document.createElement("div");b.className="banner warn";b.style.margin="12px 0 0";
    b.innerHTML='<div><b>Rakd a főképernyőre, spanom.</b> Lent a Megosztás gomb (négyzet, nyíllal felfelé) → <b>Főképernyőhöz adás</b>. Így lesz belőle igazi app.</div><button class="btn" type="button" style="padding:8px 12px;font-size:13px">Oké</button>';
    b.querySelector("button").onclick=function(){b.remove();try{localStorage.setItem("blutti-a2hs","1")}catch(e){}};
    var v=document.getElementById("v-ma");v.insertBefore(b,v.firstChild)}})();
if("serviceWorker" in navigator){window.addEventListener("load",function(){navigator.serviceWorker.register("sw.js").then(function(reg){function chk(){try{reg.update()}catch(e){}}document.addEventListener("visibilitychange",function(){if(document.visibilityState==="visible")chk()});setInterval(chk,15*60*1000)}).catch(function(){});var reloaded=false;navigator.serviceWorker.addEventListener("controllerchange",function(){if(reloaded||!navigator.serviceWorker.controller)return;reloaded=true;location.reload()})})}
try{if(navigator.storage&&navigator.storage.persist)navigator.storage.persist()}catch(e){}
</script>
</body>
</html>
'''
open(OUT,'w',encoding='utf8').write(head+rest+tail)
print('kész:',OUT,len(head+rest+tail),'bájt')
