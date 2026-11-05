import re, json, sys
sys.path.insert(0,'tools')
from newpage import write
T=open('visas/talent/index.html',encoding='utf-8').read()
def grab(a,b):
    i=T.index(a); j=T.index(b,i); return T[i:j].rstrip()
AVIS=grab('<section class="band band-top sec vl-avis" id="avis"','<!-- ============================ INTRO')
ENG=grab('<section class="band sec" id="about">','<!-- ============================ FAQ')
P='../../assets/img/'
CH='<svg class="qa-mk" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M3 5.25L7 9.25l4-4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
HEXP='M100 14 L174.5 57 L174.5 143 L100 186 L25.5 143 L25.5 57 Z'
def btn(t): return f'<a class="btn btn-primary" href="#contact">{t} <span class="arw">&rsaquo;</span></a>'
def nb(t): return t.replace(' ?','&nbsp;?').replace(' :','&nbsp;:').replace('« ','«&nbsp;').replace(' »','&nbsp;»')
def head(label,h2,cls='vl-head'):
    return f'''    <div class="sec-head {cls} rv">
      <p class="label">{label}</p>
      <h2>{nb(h2)}</h2>
    </div>'''
def tick(items,ind='          '):
    return "\n".join(f'{ind}<li><span class="vld-tk" aria-hidden="true"></span>{nb(t)}</li>' for t in items)
def timeline(mid,unit,steps):
    n=len(steps)
    li="\n".join(f'          <li style="animation-delay:{3.2*(i+1)/n:.2f}s"><span class="vl-n">{i+1:02d}</span><span><span class="vl-st">{nb(t)}</span></span></li>' for i,t in enumerate(steps))
    return f'''    <div class="vl-tl">
      <div class="vl-hex">
        <svg viewBox="0 0 200 200" aria-hidden="true">
          <path class="vl-hb" d="{HEXP}"/>
          <path class="vl-hd" pathLength="100" d="{HEXP}"/>
        </svg>
        <div class="vl-mid"><strong>{mid}</strong><span>{unit}</span></div>
      </div>
      <ol class="vl-steps">
{li}
      </ol>
    </div>'''
def switch(uid,tabs,panes,label):
    bt="\n".join(f'''        <button class="vl-sw-b" type="button" role="tab" id="{uid}-t{i}" aria-controls="{uid}-p{i}" aria-selected="{'true' if i==0 else 'false'}" tabindex="{0 if i==0 else -1}"><span class="vl-sw-k">{nb(k)}</span><span class="vl-sw-s">{nb(s)}</span></button>''' for i,(k,s) in enumerate(tabs))
    pn="\n".join(f'''      <div class="vl-sw-p" role="tabpanel" id="{uid}-p{i}" aria-labelledby="{uid}-t{i}"{'' if i==0 else ' hidden'}>
{p}
      </div>''' for i,p in enumerate(panes))
    return f'''    <div class="vl-sw rv" data-vl-sw>
      <div class="vl-sw-bar" role="tablist" aria-label="{label}">
{bt}
      </div>
{pn}
    </div>'''
def faq(items):
    out=[]
    for i,(q,a) in enumerate(items):
        out.append(f'''        <details class="qa" name="faq">
          <summary>
            <span class="qa-n">{i+1:02d}</span>
            <span class="qa-q">{nb(q)}</span>
            {CH}
          </summary>
          <div class="qa-a">{a}</div>
        </details>''')
    return "\n".join(out)
def page(c):
    b=[]
    b.append(f'''<!-- ============================ HERO ============================ -->
<section class="hero hero-v{' vl-hero-long' if len(c['h1'])>50 else ''}">
  <div class="hero-bg" aria-hidden="true">
    <span class="hero-glow hero-glow-1"></span>
    <span class="hero-glow hero-glow-2"></span>
    <span class="hero-glow hero-glow-3"></span>
  </div>
  <div class="wrap hero-in">
    <h1>{nb(c['h1'])}</h1>
    <p class="lead hero-sub">{nb(c['sub'])}</p>
    <div class="hero-ctas">
      {btn("Parler à une experte")}
    </div>
  </div>
</section>
<div id="hdrSentinel" aria-hidden="true" style="position:absolute;top:50vh;height:1px;width:1px"></div>

<!-- ============================ AVIS GOOGLE ============================ -->
{AVIS}

<!-- ============================ INTRO ============================ -->
<section class="band sec vl-intro" id="{c['intro_id']}">
  <div class="wrap vl-split">
    <div class="vl-split-txt rv">
      <div class="sec-head">
        <p class="label">{c['intro_label']}</p>
        <h2>{nb(c['intro_h2'])}</h2>
        <p class="lead">{nb(c['intro_lead'])}</p>{''.join(f'<p class="vl-more">{nb(x)}</p>' for x in c.get('intro_more',[]))}
      </div>
      {btn(c.get("intro_cta","Vérifier mon éligibilité"))}
    </div>
    <figure class="vl-split-ph rv">
      <img src="{P}{c['intro_ph'][0]}" width="{c['intro_ph'][1]}" height="{c['intro_ph'][2]}" alt="{c['intro_ph'][3]}" loading="lazy" decoding="async">
    </figure>
  </div>
</section>
''')
    # tipos (opcional, como en Talent)
    if c.get('types'):
        tl="\n".join(f'      <li class="vl-type"><span class="vl-num">{i+1:02d}</span><h3>{nb(t)}</h3></li>' for i,t in enumerate(c['types']))
        b.append(f'''<!-- ============================ TYPES ============================ -->
<section class="band tinted sec" id="types">
  <div class="wrap">
{head(c.get('types_label',"Types de visa"),c['types_h2'])}
    <ul class="vl-types rv">
{tl}
    </ul>
    <div class="vl-act rv">{btn(c.get('types_cta',"Trouver ma procédure"))}</div>
  </div>
</section>
''')
    # ventajas
    if not c.get('adv_mode'):
        pass
    elif c['adv_mode']=='single':
        adv=c['adv']; ph=c['adv_ph']
        tabs="\n".join(f'''        <button class="vla-tab" type="button" role="tab" id="vla-t{i}" aria-controls="vla-p" aria-selected="{'true' if i==0 else 'false'}" tabindex="{0 if i==0 else -1}" data-i="{i}"><span class="vla-n">{i+1:02d}</span><span class="vla-l">{nb(t)}{'<span class="vla-dot" aria-hidden="true"></span>' if i in c.get('adv_wink',{}) else ''}{f'<span class="vla-hint">{c["adv_hint"][i]}</span>' if i in c.get('adv_hint',{}) else ''}</span></button>''' for i,t in enumerate(adv))
        imgs="\n".join(f'''        <img class="vla-img{' is-on' if i==0 else ''}" src="{P}{f}" width="{w}" height="{h}" alt="{a}" loading="lazy" decoding="async">''' for i,(f,w,h,a) in enumerate(ph))
        wink=c.get('adv_wink',{})
        def cap(i,t):
            w=wink.get(i)
            extra=f'<span class="vla-wink"><span class="vla-wink-k">Entre nous</span> {w}</span>' if w else ''
            mo=c.get('adv_more',{}).get(i)
            if mo: extra+=f'<span class="vla-more">{mo}</span>'
            return f'''        <p class="vla-cap{' is-on' if i==0 else ''}" data-i="{i}" aria-hidden="{'false' if i==0 else 'true'}">{nb(t)}{extra}</p>'''
        caps="\n".join(cap(i,t) for i,t in enumerate(adv))
        inner=f'''    <div class="vla" data-vla>
      <div class="vla-list" role="tablist" aria-label="{c['adv_h2']}">
{tabs}
      </div>
      <div class="vla-ph" id="vla-p" role="tabpanel">
{imgs}
        <div class="vla-caps">
{caps}
        </div>
      </div>
    </div>'''
    else:
        panes=[f'''        <div class="vl-ck">
          <div class="vl-ck-h"><span class="vl-ck-k">{nb(k)}</span><h3>{nb(h)}</h3></div>
          <ul class="vld-list">
{tick(items,'            ')}
          </ul>
        </div>''' for (k,h,items) in c['adv_dual']]
        inner=switch('adv',c['adv_tabs'],panes,c['adv_h2'])
    if c.get('adv_mode'): b.append(f'''<!-- ============================ CARACTERISTIQUES ============================ -->
<section class="band tinted sec" id="avantages">
  <div class="wrap">
{head("Caractéristiques du visa",c['adv_h2'])}
{inner}
    <div class="vl-act rv">{btn("Prendre rendez-vous")}</div>
  </div>
</section>
''')
    # delais
    if len(c['delais'])==1:
        d=c['delais'][0]; inner=timeline(d['mid'],d['unit'],d['steps'])
    else:
        inner=switch('dl',[(d['tab'],d['tabs']) for d in c['delais']],[timeline(d['mid'],d['unit'],d['steps']) for d in c['delais']],"Délais estimatifs")
    b.append(f'''<!-- ============================ DELAIS ============================ -->
<!-- Linea de tiempo: el hexagono se dibuja de 0 al final y cada etapa se
     enciende a su turno. Corre una vez y termina sola. -->
<section class="band sec" id="delais">
  <div class="wrap">
{head("Délais estimatifs","Les étapes de la procédure")}
{inner}
    <div class="vl-act rv">{btn("Lancer ma démarche")}</div>
  </div>
</section>

<!-- ============================ SERVICES ============================ -->
<section class="band tinted sec" id="services">
  <div class="wrap">
{head("Nos services","Ce que nous prenons en charge")}
    <div class="vld vld-solo rv">
      <ul class="vld-list">
{tick(c['svc'])}
      </ul>
    </div>
    <div class="vl-act rv">{btn("Demander un devis")}</div>
  </div>
</section>

<!-- ============================ ENGAGEMENTS ============================ -->
{ENG}

<!-- ============================ FAQ ============================ -->
<section class="band tinted faq sec" id="faq">
  <div class="wrap">
    <div class="sec-head rv">
      <p class="label">Questions fréquentes</p>
      <h2>Ce qu'on nous demande le plus souvent</h2>
    </div>
    <div class="qas qn-lilac rv">
{faq(c['faq'])}
    </div>

    <div class="faq-act rv">
      {btn("Contactez une experte")}
    </div>
  </div>
</section>''')
    body="\n".join(b)
    D="https://inwardpro.com"; U=f"{D}/{c['dir']}/"
    jsonld=json.dumps({"@context":"https://schema.org","@graph":[
     {"@type":"WebPage","@id":U+"#webpage","url":U,"name":c['h1'],"isPartOf":{"@id":D+"/#website"},"about":{"@id":D+"/#organization"},"inLanguage":"fr","breadcrumb":{"@id":U+"#breadcrumb"}},
     {"@type":"Service","@id":U+"#service","name":"Accompagnement "+c['short'],"serviceType":c['short'],"provider":{"@id":D+"/#organization"},"areaServed":{"@type":"Country","name":"France"},
      "hasOfferCatalog":{"@type":"OfferCatalog","name":"Nos services","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s}} for s in c['svc']]}},
     {"@type":"BreadcrumbList","@id":U+"#breadcrumb","itemListElement":[{"@type":"ListItem","position":1,"name":"Accueil","item":D+"/"},{"@type":"ListItem","position":2,"name":c['short'],"item":U}]}]},ensure_ascii=False,indent=2)
    rail="\n".join(f'  <a href="#{a}" aria-label="{l}"><span></span></a>' for a,l in [("top","Haut de page"),("avis","Avis"),(c['intro_id'],c['intro_label'])]+([("types","Types de visa")] if c.get('types') else [])+([("avantages","Caractéristiques")] if c.get('adv_mode') else [])+[("delais","Délais"),("services","Nos services"),("about","Nos engagements"),("faq","Questions fréquentes"),("contact","Contact")])
    write(c['dir'],c['title'],c['desc'],jsonld,body,rail)
