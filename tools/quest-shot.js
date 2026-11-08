const {chromium}=require('playwright');const fs=require('fs');
// Tündér Quest 3D füstteszt + képernyőképek (WebGL swiftshaderrel). Futtatás: node tools/quest-shot.js
const path=require('path');const dir=path.join(__dirname,'..','src')+path.sep;const tmp=path.join(__dirname,'.tmp')+path.sep;require('fs').mkdirSync(tmp,{recursive:true});const KEY='blutti-frutti-v1';
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});const ctx=await b.newContext({viewport:{width:393,height:852},deviceScaleFactor:2,hasTouch:true});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message+' @ '+String(e.stack).split('\n')[1]));p.on('console',m=>{if(m.type()==='warning'||m.type()==='error')errs.push('console: '+m.text().slice(0,200))});p.on('dialog',d=>d.accept());
await p.addInitScript(()=>{setInterval(()=>{const m=document.getElementById('ckModal');if(m&&!m.hidden){const b=document.getElementById('ckClose');if(b)b.click()}},300)});
fs.writeFileSync(tmp+'tf.html','<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"></head><body style="margin:0">'+fs.readFileSync(dir+'blutti-frutti.html','utf8').replace('<script>\n(function(){','<script>\n(function(){window.__T=function(){return {RPG:RPG,S:S,GL:GL,rpgMove:rpgMove,rpgEnterDung:rpgEnterDung,rpgAttack:rpgAttack}};')+'</body></html>');
await p.goto('file://'+tmp+'tf.html');await p.waitForTimeout(800);
await p.evaluate(({KEY})=>{const S=JSON.parse(localStorage.getItem(KEY));S.settings.incomeExpected=900000;S.settings.wn="2";localStorage.setItem(KEY,JSON.stringify(S))},{KEY});
await p.reload();await p.waitForTimeout(1500);if(await p.$('#vOk:visible'))await p.click('#vOk');
await p.click('[data-tab=jatek]');await p.waitForTimeout(400);await p.click('[data-play=rpg]');await p.waitForTimeout(400);await p.click('#pgGo');await p.waitForTimeout(2500);
console.log('GL ok',await p.evaluate(()=>__T().GL.ok));
await p.evaluate(()=>{const T=__T();T.RPG.p.x=33;T.RPG.p.y=36;T.RPG.mon=[{k:'fustos',x:35,y:36,hp:18,mhp:18,nt:1e15,na:1e15,dir:[-1,0]},{k:'sarkany',x:36,y:38,hp:60,mhp:60,nt:1e15,na:1e15,dir:[-1,0]},{k:'patkany',x:31,y:38,hp:14,mhp:14,nt:1e15,na:1e15,dir:[1,0]},{k:'robot',x:34,y:39,hp:34,mhp:34,nt:1e15,na:1e15,dir:[0,-1]}]});
await p.waitForTimeout(1500);await p.screenshot({path:tmp+'bq1.png'});
await p.evaluate(()=>{const T=__T();T.RPG.p.face=[1,0];T.RPG.mon[0].x=34;T.rpgAttack(false)});await p.waitForTimeout(120);await p.screenshot({path:tmp+'bq2.png'});await p.waitForTimeout(600);
await p.evaluate(()=>{const T=__T();T.S.rpg.unl.d1=1;T.rpgEnterDung('d1')});await p.waitForTimeout(1800);await p.screenshot({path:tmp+'bq3.png'});
await p.evaluate(()=>{const T=__T();T.S.rpg.unl.d3=1;T.rpgEnterDung('d3');T.RPG.p.x=10;T.RPG.p.y=8});await p.waitForTimeout(1800);await p.screenshot({path:tmp+'bq4.png'});
console.log('errs',errs.slice(0,6));await b.close()})();
