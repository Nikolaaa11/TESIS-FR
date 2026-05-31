/* ===== Tesis USS — interacción y gráficos (Chart.js) con datos reales ===== */
const D = window.TESIS_DATA || {};
const PAL = { navy:'#1b2a41', bronze:'#9a6a3a', copper:'#c2703d', blue:'#0071e3',
  green:'#1a8a4a', red:'#c4314b', gray:'#86868b' };
let CHARTS = [];

function themeColors(){
  const dark = document.documentElement.getAttribute('data-theme') === 'dark';
  return {
    ink: dark ? '#f5f5f7' : '#1d1d1f',
    ink2: dark ? '#a1a1a6' : '#6e6e73',
    grid: dark ? '#2a2a2c' : '#f0f0f2',
    navy: dark ? '#dfe6f2' : '#1b2a41',
    soft: dark ? '#2c2c2e' : '#e8e8ed',
    tip: dark ? '#2c2c2e' : '#1d1d1f'
  };
}

/* ---------- THEME ---------- */
function initTheme(){
  const saved = localStorage.getItem('tesis-theme');
  if(saved) document.documentElement.setAttribute('data-theme', saved);
  else if(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)
    document.documentElement.setAttribute('data-theme','dark'); // respeta el SO en 1ª visita
  const btn = document.getElementById('themeBtn');
  const setIcon = ()=> btn.textContent = document.documentElement.getAttribute('data-theme')==='dark' ? '☀' : '◐';
  setIcon();
  btn.addEventListener('click', ()=>{
    const now = document.documentElement.getAttribute('data-theme')==='dark' ? 'light':'dark';
    document.documentElement.setAttribute('data-theme', now);
    localStorage.setItem('tesis-theme', now); setIcon();
    CHARTS.forEach(c=>c.destroy()); CHARTS=[]; buildCharts();
  });
}

/* ---------- PROGRESS + SCROLL-SPY ---------- */
function initScroll(){
  const bar = document.getElementById('progress');
  const links = [...document.querySelectorAll('.nav-links a[href^="#"]')];
  const secs = links.map(a=>document.querySelector(a.getAttribute('href'))).filter(Boolean);
  const onScroll = ()=>{
    const h = document.documentElement;
    bar.style.width = (h.scrollTop/(h.scrollHeight-h.clientHeight)*100)+'%';
    let cur = secs[0];
    secs.forEach(s=>{ if(s.getBoundingClientRect().top <= 120) cur = s; });
    links.forEach(a=>a.classList.toggle('active', a.getAttribute('href')==='#'+(cur&&cur.id)));
  };
  document.addEventListener('scroll', onScroll, {passive:true}); onScroll();
}

/* ---------- COUNTERS ---------- */
function initCounters(){
  const els = document.querySelectorAll('[data-count]');
  const io = new IntersectionObserver(es=>es.forEach(e=>{
    if(!e.isIntersecting) return; io.unobserve(e.target);
    const el=e.target, end=+el.dataset.count, suf=el.dataset.suffix||'', dur=1100, t0=performance.now();
    const fmt=n=> n>=1000 ? n.toLocaleString('es-CL') : n;
    (function tick(t){ const p=Math.min((t-t0)/dur,1); const v=Math.round((1-Math.pow(1-p,3))*end);
      el.textContent=fmt(v)+suf; if(p<1) requestAnimationFrame(tick); })(t0);
  }),{threshold:.5});
  els.forEach(el=>io.observe(el));
}

/* ---------- helpers ---------- */
const round=(x,n=3)=>x==null?null:Math.round(x*10**n)/10**n;
function baseOpts(yT){ const c=themeColors(); return {
  responsive:true, maintainAspectRatio:false,
  plugins:{ legend:{position:'top',labels:{usePointStyle:true,boxWidth:8,color:c.ink2}},
    tooltip:{backgroundColor:c.tip,padding:12,cornerRadius:8} },
  scales:{ y:{title:{display:!!yT,text:yT,color:c.ink2},grid:{color:c.grid},border:{display:false},ticks:{color:c.ink2}},
    x:{grid:{display:false},border:{display:false},ticks:{color:c.ink2}} } };
}

/* ---------- CHARTS ---------- */
function buildCharts(){
  const c = themeColors();
  Chart.defaults.font.family="'Inter',-apple-system,sans-serif";
  Chart.defaults.color=c.ink2;
  const mk=(id,cfg)=>{ const el=document.getElementById(id); if(el){ CHARTS.push(new Chart(el,cfg)); } };

  // Horizonte
  const h=D.horizonte;
  if(h) mk('chHorizonte',{type:'line',data:{labels:h.labels,datasets:[
    {label:'Antofagasta (líquido)',data:h.anto,borderColor:c.navy,backgroundColor:c.navy,tension:.35,borderWidth:3,pointRadius:5},
    {label:'Pucobre (ilíquido)',data:h.pucobre,borderColor:PAL.copper,backgroundColor:PAL.copper,tension:.35,borderWidth:3,pointRadius:5}]},
    options:baseOpts('β-cobre (elasticidad)')});

  // Rezagos
  const r=D.rezagos;
  if(r){ const a=r.find(x=>x.activo==='ANTO.L'),p=r.find(x=>x.activo==='PUCOBRE.SN'); const f=x=>Math.round((x.fraccion_dia0||0)*100);
    mk('chRezagos',{type:'bar',data:{labels:['Antofagasta','Pucobre'],datasets:[
      {label:'Llega el día 0 (%)',data:[f(a),f(p)],backgroundColor:PAL.blue,borderRadius:6},
      {label:'Diferido (%)',data:[100-f(a),100-f(p)],backgroundColor:c.soft,borderRadius:6}]},
      options:{...baseOpts('% del impacto acumulado'),scales:{x:{stacked:true,grid:{display:false},ticks:{color:c.ink2}},y:{stacked:true,max:100,grid:{color:c.grid},ticks:{color:c.ink2}}}}}); }

  // Series precios
  const s=D.series;
  if(s) mk('chSeries',{type:'line',data:{labels:s.fechas,datasets:[
    {label:'Antofagasta',data:s.anto,borderColor:PAL.navy,borderWidth:2.2,pointRadius:0,tension:.25,fill:true,
      backgroundColor:ctx=>vgrad(ctx.chart.ctx,ctx.chart.chartArea,PAL.navy,0.16)},
    {label:'Pucobre',data:s.pucobre,borderColor:PAL.copper,borderWidth:2.2,pointRadius:0,tension:.25,fill:true,
      backgroundColor:ctx=>vgrad(ctx.chart.ctx,ctx.chart.chartArea,PAL.copper,0.14)},
    {label:'Cobre (HG=F)',data:s.cobre,borderColor:PAL.bronze,borderWidth:2,borderDash:[5,4],pointRadius:0,tension:.25}]},
    options:{...baseOpts('base 100'),scales:{...baseOpts().scales,x:{grid:{display:false},ticks:{color:c.ink2,maxTicksLimit:8}}}}});

  // Cobre con eventos anotados
  if(s && typeof window!=='undefined'){
    const eventos=[
      {x:"2008-09",txt:"Crisis financiera 2008",col:PAL.red},
      {x:"2011-02",txt:"Pico superciclo",col:PAL.bronze},
      {x:"2020-03",txt:"Shock COVID-19",col:PAL.blue},
      {x:"2021-05",txt:"Boom pospandemia",col:PAL.green},
    ];
    const has=fch=>s.fechas.includes(fch);
    const ann={};
    eventos.filter(e=>has(e.x)).forEach((e,i)=>{ann["l"+i]={type:'line',xMin:e.x,xMax:e.x,
      borderColor:e.col,borderWidth:1.6,borderDash:[4,3],
      label:{display:true,content:e.txt,position:(i%2?'start':'end'),backgroundColor:e.col,
        color:'#fff',font:{size:9,weight:'600'},padding:4,borderRadius:5}}});
    mk('chCobreEventos',{type:'line',data:{labels:s.fechas,datasets:[
      {label:'Precio del cobre (base 100)',data:s.cobre,borderColor:PAL.copper,borderWidth:2.4,pointRadius:0,tension:.25,fill:true,
        backgroundColor:ctx=>vgrad(ctx.chart.ctx,ctx.chart.chartArea,PAL.copper,0.20)}]},
      options:{...baseOpts('base 100'),
        plugins:{legend:{display:false},tooltip:{backgroundColor:c.tip},annotation:{annotations:ann}},
        scales:{...baseOpts().scales,x:{grid:{display:false},ticks:{color:c.ink2,maxTicksLimit:9}}}}});
  }

  // Beta
  const b=(D.beta_cobre||[]).slice().sort((x,y)=>y.coef-x.coef);
  if(b.length){ const cols=b.map(x=>['ANTO.L','PUCOBRE.SN','CAP.SN','SQM-B.SN'].includes(x.activo)?PAL.copper:PAL.navy);
    mk('chBeta',{type:'bar',data:{labels:b.map(x=>x.activo),datasets:[{label:'β-cobre',data:b.map(x=>x.coef),backgroundColor:cols,borderRadius:6}]},
      options:{...baseOpts('β contemporánea'),indexAxis:'y',plugins:{legend:{display:false},tooltip:{backgroundColor:c.tip,callbacks:{label:ctx=>`β = ${ctx.raw} (R²=${b[ctx.dataIndex].R2})`}}}}}); }

  // FEVD
  const v=D.var||[];
  if(v.length) mk('chFevd',{type:'bar',data:{labels:v.map(x=>x.activo),datasets:[
    {label:'1 día',data:v.map(x=>x.fevd_cobre_h1),backgroundColor:PAL.bronze,borderRadius:6},
    {label:'20 días',data:v.map(x=>x.fevd_cobre_h20),backgroundColor:PAL.navy,borderRadius:6}]},
    options:baseOpts('% varianza explicada por cobre')});

  // IRF
  const irf=D.irf;
  if(irf) mk('chIrf',{type:'line',data:{labels:irf.dias,datasets:[
    {label:'Antofagasta',data:irf.anto,borderColor:PAL.navy,backgroundColor:PAL.navy,borderWidth:2.5,pointRadius:0,tension:.3},
    {label:'Pucobre',data:irf.pucobre,borderColor:PAL.copper,backgroundColor:PAL.copper,borderWidth:2.5,pointRadius:0,tension:.3}]},
    options:{...baseOpts('respuesta (%)'),scales:{...baseOpts().scales,x:{title:{display:true,text:'días tras el shock',color:c.ink2},grid:{display:false},ticks:{color:c.ink2}}}}});

  // VECM
  const vm=D.vecm||[];
  if(vm.length) mk('chVecm',{type:'bar',data:{labels:vm.map(x=>x.activo),datasets:[{label:'Elasticidad-cobre de largo plazo',data:vm.map(x=>x.LP_cobre),backgroundColor:PAL.copper,borderRadius:6}]},
    options:{...baseOpts('elasticidad de cointegración'),plugins:{legend:{display:false},tooltip:{backgroundColor:c.tip}}}});

  // GARCH
  const g=(D.garch||[]).filter(x=>x.modelo==='GARCH(1,1)');
  if(g.length) mk('chGarch',{type:'bar',data:{labels:g.map(x=>x.activo),datasets:[{label:'Persistencia (α+β)',data:g.map(x=>x.persistencia),backgroundColor:g.map(x=>x.persistencia>0.97?PAL.navy:PAL.gray),borderRadius:6}]},
    options:{...baseOpts('persistencia de la volatilidad'),scales:{y:{min:0,max:1.02,grid:{color:c.grid},ticks:{color:c.ink2}},x:{grid:{display:false},ticks:{color:c.ink2}}},plugins:{legend:{display:false},tooltip:{backgroundColor:c.tip}}}});

  // NARDL
  const n=D.nardl||[];
  if(n.length) mk('chNardl',{type:'bar',data:{labels:n.map(x=>x.activo),datasets:[
    {label:'Alzas del cobre (|β+|)',data:n.map(x=>Math.abs(x.LP_cobre_pos)),backgroundColor:PAL.green,borderRadius:6},
    {label:'Caídas del cobre (|β−|)',data:n.map(x=>Math.abs(x.LP_cobre_neg)),backgroundColor:PAL.red,borderRadius:6}]},
    options:{...baseOpts('|elasticidad| largo plazo'),plugins:{legend:{position:'top',labels:{usePointStyle:true,boxWidth:8,color:c.ink2}},tooltip:{backgroundColor:c.tip,callbacks:{afterBody:it=>{const x=n[it[0].dataIndex];return `Wald simetría p=${x.asim_p} ${x.asim_p!=null&&x.asim_p<0.05?'(ASIMÉTRICO)':''}`;}}}}}});

  // Event study
  const e=D.event_study||[]; const acts=[...new Set(e.map(x=>x.activo))];
  if(acts.length) mk('chEvent',{type:'bar',data:{labels:acts,datasets:[
    {label:'Alza de TPM',data:acts.map(a=>{const x=e.find(y=>y.activo===a&&y.evento==='alza TPM');return x?x.CAAR:0;}),backgroundColor:PAL.red,borderRadius:6},
    {label:'Baja de TPM',data:acts.map(a=>{const x=e.find(y=>y.activo===a&&y.evento==='baja TPM');return x?x.CAAR:0;}),backgroundColor:PAL.green,borderRadius:6}]},
    options:baseOpts('CAAR (%) ventana [-5,+5]')});

  // Out-of-sample (Clark-West t por activo; placebo SQM en gris)
  const oos=D.out_of_sample||[];
  if(oos.length) mk('chOOS',{type:'bar',data:{labels:oos.map(x=>x.activo),datasets:[{
      label:'Clark-West t (cobre rezagado predice)',data:oos.map(x=>x.ClarkWest_t),
      backgroundColor:oos.map(x=>x.activo.includes('SQM')?PAL.gray:(x.CW_pvalor<0.05?PAL.green:PAL.gray)),borderRadius:6}]},
    options:{...baseOpts('estadístico Clark-West'),plugins:{legend:{display:false},
      tooltip:{backgroundColor:c.tip,callbacks:{label:ctx=>{const x=oos[ctx.dataIndex];return `t=${x.ClarkWest_t} (p=${x.CW_pvalor}) · R²oos=${x.R2_oos_pct}%`;}}},
      annotation:{annotations:{cv:{type:'line',yMin:1.645,yMax:1.645,borderColor:PAL.copper,borderWidth:1.4,borderDash:[5,4],
        label:{display:true,content:'5% (1.65)',position:'end',backgroundColor:PAL.copper,color:'#fff',font:{size:9}}}}}}}});

  // Quiebre estructural (beta pre vs post)
  const qb=D.quiebres||[];
  if(qb.length) mk('chQuiebre',{type:'bar',data:{labels:qb.map(x=>x.activo),datasets:[
      {label:'β-cobre antes del quiebre',data:qb.map(x=>x.beta_cobre_pre),backgroundColor:PAL.gray,borderRadius:6},
      {label:'β-cobre después',data:qb.map(x=>x.beta_cobre_post),backgroundColor:PAL.copper,borderRadius:6}]},
    options:{...baseOpts('β-cobre'),plugins:{legend:{position:'top',labels:{usePointStyle:true,boxWidth:8,color:c.ink2}},
      tooltip:{backgroundColor:c.tip,callbacks:{afterBody:it=>{const x=qb[it[0].dataIndex];return `supF=${x.supF} · quiebre ${x.quiebre} · ${x.hay_quiebre}`;}}}}}});

  // Scatter
  const il=D.iliquidez||[],be=D.beta_cobre||[];
  const pts=il.map(x=>{const z=be.find(y=>y.activo===x.activo);return z?{x:x.pct_dias_retorno_cero,y:z.coef,t:x.activo}:null;}).filter(Boolean);
  if(pts.length) mk('chScatter',{type:'scatter',data:{datasets:[{label:'Activos',data:pts,backgroundColor:PAL.copper,pointRadius:7,pointHoverRadius:9}]},
    options:{...baseOpts(),scales:{x:{title:{display:true,text:'% días de retorno cero (iliquidez)',color:c.ink2},grid:{color:c.grid},ticks:{color:c.ink2}},y:{title:{display:true,text:'β-cobre',color:c.ink2},grid:{color:c.grid},ticks:{color:c.ink2}}},plugins:{legend:{display:false},tooltip:{backgroundColor:c.tip,callbacks:{label:ctx=>`${ctx.raw.t}: iliquidez ${ctx.raw.x}% · β ${ctx.raw.y}`}}}}});
}

/* ---------- HEATMAP (CSS grid) ---------- */
function heatmap(){
  const el=document.getElementById('heat'); const C=D.correlacion; if(!el||!C) return;
  const n=C.labels.length;
  const color=v=>{ // azul(-) blanco(0) cobre(+)
    if(v>=0){const t=v; return `rgb(${Math.round(255-(255-194)*t)},${Math.round(255-(255-112)*t)},${Math.round(255-(255-61)*t)})`;}
    const t=-v; return `rgb(${Math.round(255-(255-27)*t)},${Math.round(255-(255-42)*t)},${Math.round(255-(255-65)*t)})`;
  };
  let html=`<div class="heat" style="grid-template-columns:80px repeat(${n},1fr)">`;
  html+=`<div></div>`;
  C.labels.forEach(l=>html+=`<div class="hh" title="${l}">${l.slice(0,5)}</div>`);
  C.matriz.forEach((fila,i)=>{ html+=`<div class="hr" title="${C.labels[i]}">${C.labels[i].slice(0,7)}</div>`;
    fila.forEach(val=>{ const tx=Math.abs(val)>0.55?'#fff':(document.documentElement.getAttribute('data-theme')==='dark'?'#111':'#333');
      html+=`<div class="hc" style="background:${color(val)};color:${tx}" title="${val}">${val.toFixed(1)}</div>`; }); });
  html+='</div>'; el.innerHTML=html;
}

/* ---------- TABLES ---------- */
function tabla(el,cols,rows){ const t=document.getElementById(el); if(!t) return;
  let h='<table class="tbl"><thead><tr>'+cols.map(c=>`<th>${c.h}</th>`).join('')+'</tr></thead><tbody>';
  rows.forEach(r=>{h+='<tr>'+cols.map(c=>`<td>${c.f?c.f(r[c.k],r):(r[c.k]??'')}</td>`).join('')+'</tr>';});
  t.innerHTML=h+'</tbody></table>';
}
const pillCausa=v=>/CAUSA/i.test(v)?`<span class="pill ok">${v}</span>`:`<span class="pill no">${v}</span>`;
const sig=p=>p!=null&&p<0.05?`<span class="pos">${p}</span>`:`<span class="neg">${p}</span>`;
function tablas(){
  tabla('tblUniverso',[{h:'Ticker',k:'ticker'},{h:'Empresa',k:'desc'},{h:'Obs',k:'n'},{h:'Desde',k:'inicio'},{h:'Moneda',k:'moneda'}],(D.universo||[]).filter(x=>x.ok));
  tabla('tblEstac',[{h:'Serie',k:'serie'},{h:'Tipo',k:'tipo'},{h:'ADF p',k:'ADF_p'},{h:'KPSS p',k:'KPSS_p'},{h:'',k:'conclusion',f:v=>`<span class="pill ${v==='I(0)'?'ok':'mid'}">${v}</span>`}],
    (D.estacionariedad||[]).filter(x=>['lprice_ANTO.L','lprice_PUCOBRE.SN','l_cobre_comex','ret_ANTO.L','ret_PUCOBRE.SN','dl_cobre_comex'].includes(x.serie)));
  tabla('tblTY',[{h:'Activo',k:'activo'},{h:'Relación',k:'relacion'},{h:'F',k:'F'},{h:'p',k:'p_valor',f:sig},{h:'',k:'veredicto',f:pillCausa}],D.toda_yamamoto||[]);
  tabla('tblMensual',[{h:'Activo',k:'activo'},{h:'β-cobre',k:'beta_cobre'},{h:'t',k:'t_cobre'},{h:'R²',k:'R2'},{h:'IMACEC',k:'imacec'}],D.mensual||[]);
  tabla('tblDesc',[{h:'Activo',k:'serie'},{h:'Media',k:'media'},{h:'SD',k:'sd'},{h:'Asim.',k:'asimetria'},{h:'Curtosis',k:'curtosis'}],D.descriptivos||[]);
  const nombreMedida={amihud:'Amihud',pct_ceros:'% días retorno cero',roll_spread_pct:'Spread de Roll',vol_medio_usd:'Volumen medio (USD)'};
  tabla('tblIlRobust',[{h:'Medida de iliquidez',k:'medida',f:v=>nombreMedida[v]||v},{h:'Signo esp.',k:'signo_esperado'},{h:'Spearman ρ',k:'spearman_rho'},{h:'p',k:'p_valor'}],D.iliquidez_robustez_corr||[]);
}

/* ---------- GALLERY + LIGHTBOX ---------- */
const FIGS=[
  ['precios_normalizados.png','Precios normalizados (base 100) vs cobre'],
  ['irf_ANTO_L.png','IRF — Antofagasta ante shock de cobre'],
  ['irf_PUCOBRE_SN.png','IRF — Pucobre (respuesta diferida)'],
  ['heatmap_correlaciones.png','Matriz de correlaciones de retornos'],
  ['iliquidez_vs_beta.png','Iliquidez vs transmisión del cobre'],
  ['vol_condicional_ANTO_L.png','Volatilidad condicional (GJR) — Antofagasta'],
  ['acf_ANTO_L.png','ACF de retornos y retornos² — Antofagasta'],
  ['retornos_ANTO_L.png','Log-retornos y volatilidad — Antofagasta'],
  ['vol_condicional_CAP_SN.png','Volatilidad condicional — CAP'],
];
function galeria(){ const g=document.getElementById('gallery'); if(!g) return;
  g.innerHTML=FIGS.map(([f,c])=>`<figure data-src="assets/figures/${f}"><img loading="lazy" src="assets/figures/${f}" alt="${c}"><figcaption>${c}</figcaption></figure>`).join('');
  const lb=document.getElementById('lightbox'), lbImg=lb.querySelector('img');
  g.querySelectorAll('figure').forEach(f=>f.addEventListener('click',()=>{lbImg.src=f.dataset.src;lb.classList.add('open');}));
  lb.addEventListener('click',()=>lb.classList.remove('open'));
}

function reveal(){ const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target);}}),{threshold:.1});
  document.querySelectorAll('.reveal,.stagger').forEach(el=>io.observe(el)); }

/* ---------- MOBILE DRAWER ---------- */
function initMenu(){
  const btn=document.getElementById('menuBtn'), dr=document.getElementById('drawer'), cl=document.getElementById('drawerClose');
  if(!btn||!dr) return;
  const open=()=>{dr.classList.add('open');dr.setAttribute('aria-hidden','false');};
  const close=()=>{dr.classList.remove('open');dr.setAttribute('aria-hidden','true');};
  btn.addEventListener('click',open); cl&&cl.addEventListener('click',close);
  dr.querySelectorAll('a').forEach(a=>a.addEventListener('click',close));
  document.addEventListener('keydown',e=>{if(e.key==='Escape')close();});
}

/* gradiente vertical para áreas */
function vgrad(ctx,area,hex,a1=0.22,a2=0.0){
  if(!area) return hex;
  const g=ctx.createLinearGradient(0,area.top,0,area.bottom);
  const h=hex.replace('#',''); const r=parseInt(h.substr(0,2),16),gg=parseInt(h.substr(2,2),16),b=parseInt(h.substr(4,2),16);
  g.addColorStop(0,`rgba(${r},${gg},${b},${a1})`); g.addColorStop(1,`rgba(${r},${gg},${b},${a2})`);
  return g;
}

document.addEventListener('DOMContentLoaded',()=>{
  initTheme(); initScroll(); initCounters(); initMenu();
  try{ buildCharts(); }catch(e){ console.error('charts',e); }
  heatmap(); tablas(); galeria(); reveal();
});
