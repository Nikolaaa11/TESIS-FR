/* ===== Tesis USS — gráficos (Chart.js) con datos reales ===== */
const D = window.TESIS_DATA || {};
const C = {
  navy:'#1b2a41', bronze:'#9a6a3a', copper:'#c2703d', blue:'#0071e3',
  green:'#1a8a4a', red:'#c4314b', gray:'#86868b', soft:'#e8e8ed'
};
Chart.defaults.font.family = "'Inter',-apple-system,sans-serif";
Chart.defaults.color = '#6e6e73';
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.boxWidth = 8;

const baseOpts = (yTitle) => ({
  responsive:true, maintainAspectRatio:false,
  plugins:{ legend:{ position:'top' }, tooltip:{ backgroundColor:'#1d1d1f', padding:12, cornerRadius:8 } },
  scales:{
    y:{ title:{display:!!yTitle,text:yTitle}, grid:{color:'#f0f0f2'}, border:{display:false} },
    x:{ grid:{display:false}, border:{display:false} }
  }
});
const ring = a => a.anillo || '';
const round = (x,n=3)=> x==null?null:Math.round(x*Math.pow(10,n))/Math.pow(10,n);

/* ---- 1. Horizonte (hallazgo central) ---- */
function chHorizonte(){
  const h = D.horizonte; if(!h) return;
  new Chart('chHorizonte',{type:'line',
    data:{labels:h.labels,datasets:[
      {label:'Antofagasta (líquido)',data:h.anto,borderColor:C.navy,backgroundColor:C.navy,tension:.35,borderWidth:3,pointRadius:5},
      {label:'Pucobre (ilíquido)',data:h.pucobre,borderColor:C.copper,backgroundColor:C.copper,tension:.35,borderWidth:3,pointRadius:5}
    ]},
    options:{...baseOpts('β-cobre (elasticidad)'),
      plugins:{...baseOpts().plugins,
        subtitle:{display:true,text:'La sensibilidad de Pucobre crece con el horizonte',color:C.gray}}}
  });
}

/* ---- 2. Rezagos día0 vs diferido (doughnuts) ---- */
function chRezagos(){
  const r = D.rezagos; if(!r) return;
  const anto = r.find(x=>x.activo==='ANTO.L'), puco=r.find(x=>x.activo==='PUCOBRE.SN');
  const f = x=> Math.round((x.fraccion_dia0||0)*100);
  new Chart('chRezagos',{type:'bar',
    data:{labels:['Antofagasta','Pucobre'],datasets:[
      {label:'Llega el día 0 (%)',data:[f(anto),f(puco)],backgroundColor:C.blue,borderRadius:6},
      {label:'Diferido a días siguientes (%)',data:[100-f(anto),100-f(puco)],backgroundColor:C.soft,borderRadius:6}
    ]},
    options:{...baseOpts('% del impacto acumulado'),
      scales:{x:{stacked:true,grid:{display:false}},y:{stacked:true,max:100,grid:{color:'#f0f0f2'}}}}
  });
}

/* ---- 3. Beta-cobre por activo (barra horizontal) ---- */
function chBeta(){
  const b = (D.beta_cobre||[]).slice().sort((a,c)=>c.coef-a.coef);
  const cols = b.map(x=> ['ANTO.L','PUCOBRE.SN','CAP.SN','SQM-B.SN'].includes(x.activo)?C.copper:C.navy);
  new Chart('chBeta',{type:'bar',
    data:{labels:b.map(x=>x.activo),datasets:[{label:'β-cobre',data:b.map(x=>x.coef),backgroundColor:cols,borderRadius:6}]},
    options:{...baseOpts('β contemporánea'),indexAxis:'y',plugins:{legend:{display:false},tooltip:{backgroundColor:'#1d1d1f',callbacks:{label:c=>`β = ${c.raw} (R²=${b[c.dataIndex].R2})`}}}}}
  );
}

/* ---- 4. FEVD cobre ---- */
function chFevd(){
  const v = D.var||[];
  new Chart('chFevd',{type:'bar',
    data:{labels:v.map(x=>x.activo),datasets:[
      {label:'1 día',data:v.map(x=>x.fevd_cobre_h1),backgroundColor:C.bronze,borderRadius:6},
      {label:'20 días',data:v.map(x=>x.fevd_cobre_h20),backgroundColor:C.navy,borderRadius:6}
    ]},
    options:baseOpts('% varianza explicada por el cobre')}
  );
}

/* ---- 5. VECM elasticidades largo plazo ---- */
function chVecm(){
  const v = D.vecm||[];
  new Chart('chVecm',{type:'bar',
    data:{labels:v.map(x=>x.activo),datasets:[{label:'Elasticidad-cobre de largo plazo',data:v.map(x=>x.LP_cobre),backgroundColor:C.copper,borderRadius:6}]},
    options:{...baseOpts('elasticidad de cointegración'),plugins:{legend:{display:false},tooltip:{backgroundColor:'#1d1d1f'}}}}
  );
}

/* ---- 6. GARCH persistencia ---- */
function chGarch(){
  const g = (D.garch||[]).filter(x=>x.modelo==='GARCH(1,1)');
  new Chart('chGarch',{type:'bar',
    data:{labels:g.map(x=>x.activo),datasets:[{label:'Persistencia (α+β)',data:g.map(x=>x.persistencia),backgroundColor:g.map(x=>x.persistencia>0.97?C.navy:C.gray),borderRadius:6}]},
    options:{...baseOpts('persistencia de la volatilidad'),scales:{y:{min:0,max:1.02,grid:{color:'#f0f0f2'}},x:{grid:{display:false}}},plugins:{legend:{display:false},tooltip:{backgroundColor:'#1d1d1f'}}}}
  );
}

/* ---- 7. NARDL asimetría ---- */
function chNardl(){
  const n = D.nardl||[];
  new Chart('chNardl',{type:'bar',
    data:{labels:n.map(x=>x.activo),datasets:[
      {label:'Alzas del cobre (|β+|)',data:n.map(x=>Math.abs(x.LP_cobre_pos)),backgroundColor:C.green,borderRadius:6},
      {label:'Caídas del cobre (|β−|)',data:n.map(x=>Math.abs(x.LP_cobre_neg)),backgroundColor:C.red,borderRadius:6}
    ]},
    options:{...baseOpts('|elasticidad| de largo plazo'),
      plugins:{...baseOpts().plugins,tooltip:{backgroundColor:'#1d1d1f',callbacks:{afterBody:items=>{const x=n[items[0].dataIndex];return `Wald simetría p=${x.asim_p} ${x.asim_p!=null&&x.asim_p<0.05?'(ASIMÉTRICO)':''}`;}}}}}}
  );
}

/* ---- 8. Event study CAAR ---- */
function chEvent(){
  const e = D.event_study||[];
  const acts=[...new Set(e.map(x=>x.activo))];
  const alza=acts.map(a=>{const r=e.find(x=>x.activo===a&&x.evento==='alza TPM');return r?r.CAAR:0;});
  const baja=acts.map(a=>{const r=e.find(x=>x.activo===a&&x.evento==='baja TPM');return r?r.CAAR:0;});
  new Chart('chEvent',{type:'bar',
    data:{labels:acts,datasets:[
      {label:'Alza de TPM',data:alza,backgroundColor:C.red,borderRadius:6},
      {label:'Baja de TPM',data:baja,backgroundColor:C.green,borderRadius:6}
    ]},
    options:baseOpts('CAAR (%) ventana [-5,+5]')}
  );
}

/* ---- 9. Scatter iliquidez vs beta ---- */
function chScatter(){
  const il = D.iliquidez||[], be = D.beta_cobre||[];
  const pts = il.map(x=>{const b=be.find(y=>y.activo===x.activo);return b?{x:x.pct_dias_retorno_cero,y:b.coef,t:x.activo}:null;}).filter(Boolean);
  new Chart('chScatter',{type:'scatter',
    data:{datasets:[{label:'Activos',data:pts,backgroundColor:C.copper,pointRadius:7,pointHoverRadius:9}]},
    options:{...baseOpts('β-cobre contemporánea'),
      scales:{x:{title:{display:true,text:'% días de retorno cero (iliquidez)'},grid:{color:'#f0f0f2'}},y:{title:{display:true,text:'β-cobre'},grid:{color:'#f0f0f2'}}},
      plugins:{legend:{display:false},tooltip:{backgroundColor:'#1d1d1f',callbacks:{label:c=>`${c.raw.t}: iliquidez ${c.raw.x}% · β ${c.raw.y}`}}}}}
  );
}

/* ---- Tablas ---- */
function tabla(el, cols, rows){
  const t=document.getElementById(el); if(!t) return;
  let h='<table class="tbl"><thead><tr>'+cols.map(c=>`<th>${c.h}</th>`).join('')+'</tr></thead><tbody>';
  rows.forEach(r=>{h+='<tr>'+cols.map(c=>`<td>${c.f?c.f(r[c.k],r):r[c.k]??''}</td>`).join('')+'</tr>';});
  t.innerHTML=h+'</tbody></table>';
}
const pillCausa = v => /CAUSA/i.test(v)?`<span class="pill ok">${v}</span>`:`<span class="pill no">${v}</span>`;
const sig = p => p!=null&&p<0.05?`<span class="pos">${p}</span>`:`<span class="neg">${p}</span>`;

function tablas(){
  tabla('tblUniverso',
    [{h:'Ticker',k:'ticker'},{h:'Empresa',k:'desc'},{h:'Obs',k:'n'},{h:'Desde',k:'inicio'},{h:'Hasta',k:'fin'},{h:'Moneda',k:'moneda'}],
    (D.universo||[]).filter(x=>x.ok));
  tabla('tblEstac',
    [{h:'Serie',k:'serie'},{h:'Tipo',k:'tipo'},{h:'ADF p',k:'ADF_p'},{h:'KPSS p',k:'KPSS_p'},{h:'Conclusión',k:'conclusion',f:v=>`<span class="pill ${v==='I(0)'?'ok':'mid'}">${v}</span>`}],
    (D.estacionariedad||[]).filter(x=>['lprice_ANTO.L','lprice_PUCOBRE.SN','l_cobre_comex','ret_ANTO.L','ret_PUCOBRE.SN','dl_cobre_comex'].includes(x.serie)));
  tabla('tblTY',
    [{h:'Activo',k:'activo'},{h:'Relación',k:'relacion'},{h:'F',k:'F'},{h:'p',k:'p_valor',f:sig},{h:'',k:'veredicto',f:pillCausa}],
    D.toda_yamamoto||[]);
  tabla('tblMensual',
    [{h:'Activo',k:'activo'},{h:'β-cobre',k:'beta_cobre'},{h:'t',k:'t_cobre'},{h:'R²',k:'R2'},{h:'IMACEC',k:'imacec'}],
    D.mensual||[]);
  tabla('tblDesc',
    [{h:'Activo',k:'serie'},{h:'Media',k:'media'},{h:'SD',k:'sd'},{h:'Asimetría',k:'asimetria'},{h:'Curtosis',k:'curtosis'}],
    D.descriptivos||[]);
}

/* ---- Galería de figuras ---- */
const FIGS = [
  ['precios_normalizados.png','Precios normalizados (base 100) vs cobre'],
  ['irf_ANTO_L.png','IRF — Antofagasta ante shock de cobre'],
  ['irf_PUCOBRE_SN.png','IRF — Pucobre ante shock de cobre (respuesta diferida)'],
  ['heatmap_correlaciones.png','Matriz de correlaciones de retornos'],
  ['iliquidez_vs_beta.png','Iliquidez vs transmisión del cobre'],
  ['vol_condicional_ANTO_L.png','Volatilidad condicional (GJR-GARCH) — Antofagasta'],
  ['acf_ANTO_L.png','ACF de retornos y retornos² — Antofagasta'],
  ['retornos_ANTO_L.png','Log-retornos y volatilidad realizada — Antofagasta'],
  ['vol_condicional_CAP_SN.png','Volatilidad condicional — CAP'],
];
function galeria(){
  const g=document.getElementById('gallery'); if(!g) return;
  g.innerHTML=FIGS.map(([f,c])=>`<figure><img loading="lazy" src="assets/figures/${f}" alt="${c}"><figcaption>${c}</figcaption></figure>`).join('');
}

/* ---- Reveal on scroll ---- */
function reveal(){
  const io=new IntersectionObserver((es)=>{es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target);}});},{threshold:.12});
  document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
}

/* ---- init ---- */
document.addEventListener('DOMContentLoaded',()=>{
  try{ chHorizonte();chRezagos();chBeta();chFevd();chVecm();chGarch();chNardl();chEvent();chScatter(); }
  catch(e){ console.error('charts',e); }
  tablas(); galeria(); reveal();
});
