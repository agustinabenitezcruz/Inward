(function(){
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Logos clientes en carrusel ----------
     Va primero: la copia tiene que existir antes de que el bloque "lo que ya
     se ve al cargar" recorra los .logos li, o la mitad del carril se quedaria
     sin su fundido de entrada. La copia es decorativa: aria-hidden y alt
     vacio, para que un lector de pantalla no lea cada marca dos veces. */
  if (!reduce) {
    [].slice.call(document.querySelectorAll("ul.logos")).forEach(function (ul) {
      var marq = document.createElement("div");
      var track = document.createElement("div");
      marq.className = "marq";
      track.className = "marq-track";
      ul.parentNode.insertBefore(marq, ul);
      marq.appendChild(track);
      track.appendChild(ul);
      var copy = ul.cloneNode(true);
      copy.classList.remove("rv");
      copy.setAttribute("aria-hidden", "true");
      [].slice.call(copy.querySelectorAll("img")).forEach(function (im) { im.alt = ""; });
      track.appendChild(copy);
      /* Velocidad constante en px/s, no duracion fija: con mas marcas el
         carril se alarga y una duracion fija lo haria correr mas rapido. */
      function vel() { track.style.setProperty("--marq-dur", Math.max(ul.offsetWidth / 38, 12) + "s"); }
      vel();
      addEventListener("load", vel);
    });
  }

  /* ---------- Acordeones <details> animados ----------
     Chrome anima la apertura solo con CSS (::details-content). Safari y
     Firefox todavia no, y ahi el panel abria y cerraba de golpe. En esos
     navegadores se anima la altura con la Web Animations API.
     El atributo name (uno abierto por grupo) se gestiona aca: si lo hiciera
     el navegador, cerraria la fila anterior de golpe mientras la nueva baja. */
  var cssDetails = window.CSS && CSS.supports &&
    CSS.supports("interpolate-size: allow-keywords") && CSS.supports("selector(::details-content)");
  if (!reduce && !cssDetails && Element.prototype.animate) {
    var acc = [].slice.call(document.querySelectorAll("details.qa,details.svc,details.mode-it"));
    acc.forEach(function (d) {
      d.setAttribute("data-group", d.getAttribute("name") || "");
      d.removeAttribute("name");
      d.querySelector("summary").addEventListener("click", function (e) {
        e.preventDefault();
        mueve(d, !(d.open && !d._cierra));
      });
    });
    function mueve(d, abrir) {
      var sum = d.querySelector("summary");
      var desde = d.offsetHeight;
      if (d._anim) d._anim.cancel();
      if (abrir) {
        var g = d.getAttribute("data-group");
        if (g) acc.forEach(function (o) {
          if (o !== d && o.open && o.getAttribute("data-group") === g) mueve(o, false);
        });
        d.open = true;
      }
      var hasta = abrir ? d.offsetHeight : sum.offsetHeight + (d.offsetHeight - d.clientHeight);
      d._cierra = !abrir;
      d.style.overflow = "hidden";
      var a = d.animate({ height: [desde + "px", hasta + "px"] },
        { duration: 480, easing: "cubic-bezier(.77,0,.175,1)" });
      (d._fades || []).forEach(function (x) { x.cancel(); });
      d._fades = [].slice.call(d.children).filter(function (c) { return c !== sum; })
        .map(function (c) {
          return c.animate({ opacity: abrir ? [0, 1] : [1, 0] },
            { duration: abrir ? 420 : 260, easing: "ease", fill: "both" });
        });
      d._anim = a;
      a.onfinish = function () {
        if (!abrir) d.open = false;
        d._cierra = false;
        d.style.overflow = "";
        d._anim = null;
        d._fades.forEach(function (x) { x.cancel(); });
        d._fades = [];
      };
    }
  }

  /* Rail : section active.
     #top est un div de hauteur nulle tout en haut : il ne tombe jamais dans la
     bande centrale du rootMargin. C'est la sentinelle du header qui le pilote. */
  var links = {};
  [].slice.call(document.querySelectorAll(".rail a")).forEach(function (a) {
    links[a.getAttribute("href")] = a;
  });
  var atTop = true, lastSection = "#top";

  /* Quien esta detras del rail se deduce de la seccion activa, no de observar
     el hero: el hero es sticky, se queda pegado arriba tapado por las
     secciones siguientes, y para un IntersectionObserver esta SIEMPRE a la
     vista. Ademas, observar el cruce de un borde falla con los saltos de
     ancla: el elemento cruza la banda entre dos fotogramas y no hay
     notificacion. La seccion activa ya la mantienen los observers de arriba y
     si se actualiza al saltar. */
  var alCambiarSeccion = null;
  function setCurrent(href) {
    for (var k in links) links[k].removeAttribute("aria-current");
    if (links[href]) links[href].setAttribute("aria-current", "true");
    if (alCambiarSeccion) alCambiarSeccion(href);
  }
  setCurrent("#top");

  if ("IntersectionObserver" in window) {
    /* Las secciones que se observan salen del PROPIO rail, no de una lista fija
       de ids. Antes estaba escrita a mano con los ids de la home, asi que en
       las landings —#agilite, #services, #types-de-visa— no se observaba nada
       y el indicador no se movia nunca. Ahora el rail es la fuente: si tiene
       un enlace, su seccion se observa, y una pagina nueva funciona sola. */
    var secs = Object.keys(links)
      .filter(function (h) { return h !== "#top"; })
      .map(function (h) { return document.querySelector(h); })
      .filter(Boolean);
    var io2 = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          lastSection = "#" + e.target.id;
          if (!atTop) setCurrent(lastSection);
        }
      });
    }, { rootMargin: "-45% 0px -45% 0px" });
    secs.forEach(function (s) { io2.observe(s); });
  }

  /* Barre du haut : transparente au-dessus de la video, pleine ensuite.
     Une sentinelle observee, pas de listener de scroll. */
  var hdr = document.querySelector(".hdr"), sentinel = document.getElementById("hdrSentinel");
  /* Una pagina sin centinela es una pagina sin hero oscuro (blog, articulo,
     video): ahi la barra tiene que nacer solida. Si no, se queda en modo
     "sobre el video" —logo y enlaces en blanco— encima de un fondo blanco y
     no se ve nada. */
  if (hdr && !sentinel) hdr.classList.add("is-solid");
  if (hdr && sentinel && "IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      var top = entries[0].isIntersecting;
      hdr.classList.toggle("is-solid", !top);
      atTop = top;
      setCurrent(top ? "#top" : lastSection);
    }, { threshold: 0 }).observe(sentinel);
  }

  /* Rail : se aclara cuando el centro de la ventana cae sobre una banda
     oscura (el hero y el pie). El rootMargin -50%/-50% reduce la zona de
     observacion a la linea media exacta de la ventana, que es donde vive el
     rail: el observer dispara justo cuando esa linea entra o sale de la banda.
     Sin listener de scroll y sin medir posiciones a mano. */
  /* railNav y no rail: mas abajo hay otro 'var rail' (el carril de las
     opiniones). Como var no tiene ambito de bloque, los dos serian la MISMA
     variable y el observer terminaba escribiendo el atributo en el elemento
     equivocado. */
  var railNav = document.querySelector(".rail");
  if (railNav && "IntersectionObserver" in window) {
    /* El hero de la home es sticky: se queda pegado arriba y tapado por las
       secciones siguientes, asi que para un IntersectionObserver esta SIEMPRE
       a la vista y el rail se quedaba en blanco toda la pagina. Se observa en
       su lugar la seccion que viene justo despues: mientras su borde superior
       este por debajo de la linea media, lo que hay ahi es el hero. */
    var heroSticky = document.querySelector(".hero");
    var darks = [].slice.call(document.querySelectorAll(".lp-hero,.ft"));
    /* Se guarda QUE bandas estan cruzando la linea media, no un contador de
       mas/menos: la primera notificacion llega con una entrada por cada
       elemento observado, y sumar +1 a las que entran y -1 a las que no
       daba cero justo cuando el hero SI estaba cubriendo el centro. */
    var overDark = [];
    var ioDark = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var i = overDark.indexOf(e.target);
        if (e.isIntersecting && i < 0) overDark.push(e.target);
        if (!e.isIntersecting && i >= 0) overDark.splice(i, 1);
      });
      pinta();
      /* -49.9% y no -50%: con -50% exacto la zona de observacion queda de
         alto cero, y una zona vacia no interseca con nada, asi que el observer
         no dispara nunca. Dejando dos pixeles de banda funciona igual y
         dispara. */
    }, { rootMargin: "-49.9% 0px -49.9% 0px" });
    darks.forEach(function (d) { ioDark.observe(d); });

    var sobreHero = !!heroSticky;
    function pinta() {
      railNav.setAttribute("data-dark", (overDark.length || sobreHero) ? "true" : "false");
    }
    if (heroSticky) {
      alCambiarSeccion = function (href) {
        sobreHero = href === "#top";
        pinta();
      };
    }
    pinta();

    /* Reserva para navegadores sin animation-timeline: el rail se retira
       cuando el pie asoma. Donde hay soporte, lo hace el CSS atado al scroll
       y este observer no se instala. */
    var tl = window.CSS && CSS.supports && CSS.supports("animation-timeline: view()");
    var ft = document.querySelector(".ft");
    if (!tl && ft) {
      new IntersectionObserver(function (es) {
        railNav.setAttribute("data-lift", es[0].isIntersecting ? "true" : "false");
      }, { threshold: 0 }).observe(ft);
    }
  }

  /* Video du hero : coupee si l'utilisateur demande moins d'animation.
     Le poster reste affiche, la page ne perd rien. */
  var hv = document.getElementById("heroVideo");
  if (hv && reduce) { hv.removeAttribute("autoplay"); hv.pause(); }

  /* ---------- Lo que ya se ve al cargar ----------
     Las animaciones de entrada van atadas al scroll. Para lo que ya esta en
     la primera pantalla eso no funciona: el progreso depende de cuanto
     scrolleaste, asi que arrancan a medio camino y se quedan ahi. Se marcan
     esos elementos con data-onload y el CSS los pasa al reloj, con un
     escalonado corto para que el ultimo termine alrededor del segundo. */
  if (!reduce) {
    var SEL = ".rv,.logos li,.cell,.art,.svc,.qa summary,.row-btn,.b2c-media," +
              ".avis-card,.eng-pane,.about-band";
    var arriba = [].slice.call(document.querySelectorAll(SEL)).filter(function (el) {
      var r = el.getBoundingClientRect();
      return r.top < window.innerHeight * 0.95 && r.bottom > 0;
    });
    arriba.forEach(function (el, i) {
      /* El escalonado se corta a 60 ms por elemento y 420 ms en total: con
         muchos elementos arriba, un retardo proporcional dejaria al ultimo
         entrando varios segundos despues de que la pagina ya esta quieta. */
      el.style.setProperty("--dl", Math.min(i * 60, 420) + "ms");
      el.setAttribute("data-onload", "");
    });
    /* Dos fotogramas: uno para que el navegador registre el estado inicial
       (opacidad 0) y otro para disparar la transicion. Con uno solo, los dos
       valores caen en el mismo recalculo y no hay transicion que animar. */
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        arriba.forEach(function (el) { el.setAttribute("data-in", ""); });
      });
    });
  }

  /* Reveal : visible par defaut, masque seulement si hors ecran au chargement */
  var scrollTimeline = window.CSS && CSS.supports && CSS.supports("animation-timeline: view()");
  if (!reduce && !scrollTimeline && "IntersectionObserver" in window) {
    var els = [].slice.call(document.querySelectorAll(".rv"));
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting) { e.target.setAttribute("data-hidden","false"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.08 });
    els.forEach(function(el, i){
      var r = el.getBoundingClientRect();
      if (r.top > window.innerHeight * 0.92) {
        el.setAttribute("data-hidden","true");
        el.style.transitionDelay = ((i % 4) * 55) + "ms";
        io.observe(el);
      }
    });
  }

  /* Lignes B2C : accordeon. Un clic ouvre, un autre ferme.
     Pas d'ouverture au survol : elle rouvrirait la ligne qu'on vient de fermer. */
  var rows = [].slice.call(document.querySelectorAll(".row"));
  var shots = [].slice.call(document.querySelectorAll(".b2c-media img"));

  function setRow(row, open) {
    row.setAttribute("data-open", open ? "true" : "false");
    var btn = row.querySelector(".row-btn");
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    btn.setAttribute("aria-label", (open ? "Replier " : "Deplier ") + btn.textContent.trim());
  }

  function showShot(key) {
    shots.forEach(function (s) { s.classList.toggle("is-on", s.getAttribute("data-key") === key); });
  }

  rows.forEach(function (row) {
    setRow(row, row.getAttribute("data-open") === "true");
    row.querySelector(".row-btn").addEventListener("click", function () {
      var wasOpen = row.getAttribute("data-open") === "true";
      /* Se cierran las hermanas del MISMO panel, no todas las de la pagina.
         En la home habia un solo .rows y daba igual; la landing de
         particulares tiene dos (tipos de visa y soutien) y con el criterio
         viejo abrir una fila cerraba la que estuviera abierta en la otra
         seccion, que no tienen nada que ver entre si. */
      var panel = row.closest(".rows") || document;
      [].slice.call(panel.querySelectorAll(".row")).forEach(function (r) { setRow(r, false); });
      if (!wasOpen) {
        setRow(row, true);
        /* Solo las filas de la home llevan foto asociada. */
        if (row.hasAttribute("data-img")) showShot(row.getAttribute("data-img"));
      }
      /* Si on ferme, l'apercu reste sur la derniere image : le bloc ne se vide pas. */
    });
  });

  /* ---------- Menu desplegable (tablet y telefono) ----------
     El mismo <nav> de escritorio hace de panel. En escritorio los grupos se
     abren con :hover y este bloque no interviene: la consulta media es la
     unica fuente de verdad, asi no hay dos criterios de ancho que discrepen. */
  var burger = document.getElementById("burger"), menu = document.getElementById("navMenu");
  if (burger && menu) {
    var mobile = matchMedia("(max-width:1080px)");

    function closeGroups() {
      menu.querySelectorAll('.nav-item[data-open="true"]').forEach(function (it) {
        it.setAttribute("data-open", "false");
        var b = it.querySelector(".nav-btn");
        /* aria-expanded solo en los que son boton: los nombres de grupo que
           llevan a una landing son enlaces, y en un enlace ese atributo no
           significa nada. */
        if (b.tagName === "BUTTON") b.setAttribute("aria-expanded", "false");
      });
    }

    function setMenu(open) {
      menu.setAttribute("data-open", open ? "true" : "false");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      burger.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
      /* Bloquear el scroll del fondo: sin esto el dedo arrastra la pagina
         detras del panel y al cerrar aparecemos en otra parte del sitio.
         Firefox vuelve el documento arriba de todo al quitar el overflow de
         <html>, asi que se guarda la posicion al abrir y se repone al cerrar,
         sin animar (el html tiene scroll-behavior:smooth). */
      var root = document.documentElement;
      if (open && root.style.overflow !== "hidden") menuY = scrollY;
      var estaba = root.style.overflow === "hidden";
      root.style.overflow = open ? "hidden" : "";
      if (!open && estaba && Math.abs(scrollY - menuY) > 1) scrollTo({ top: menuY, behavior: "instant" });
      if (!open) closeGroups();
    }
    var menuY = 0;

    burger.addEventListener("click", function () {
      setMenu(menu.getAttribute("data-open") !== "true");
    });

    /* Un grupo por vez: dos mega menus abiertos en una pantalla de telefono
       obligan a desplazarse para encontrar el segundo titulo. */
    menu.querySelectorAll(".nav-btn").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        if (!mobile.matches) return;
        /* En telefono no hay hover: el primer toque despliega el grupo en vez
           de irse a la landing. El enlace sigue estando ahi —dentro del panel
           hay un acceso directo— pero el toque sobre el nombre no puede
           sacarte de la pagina sin haber visto el menu. */
        e.preventDefault();
        var item = btn.closest(".nav-item"), open = item.getAttribute("data-open") === "true";
        closeGroups();
        if (!open) {
          item.setAttribute("data-open", "true");
          if (btn.tagName === "BUTTON") btn.setAttribute("aria-expanded", "true");
        }
      });
    });

    /* Al elegir un destino el menu se va: si no, el ancla salta detras del
       panel. Los nombres de grupo quedan fuera: ahora tambien son enlaces, y
       en telefono su primer toque despliega el grupo —cerrar el panel entero
       ahi deshace justo lo que el usuario acaba de pedir. */
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a") && !e.target.closest(".nav-btn")) setMenu(false);
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.getAttribute("data-open") === "true") {
        setMenu(false);
        burger.focus();
      }
    });

    /* Al pasar a escritorio el panel deja de existir como panel: si quedara
       marcado abierto, el scroll del documento seguiria bloqueado. */
    mobile.addEventListener("change", function (e) { if (!e.matches) setMenu(false); });
  }

  /* ---------- Cifras clave : cuenta de cero al valor final ----------
     El numero se lee del propio texto, asi sirve igual en FR, EN y ES: lo que
     va antes ("+") y despues (" %") se conserva tal cual. Arranca al entrar
     en pantalla, una sola vez, y la barra de abajo avanza al mismo ritmo. */
  var kpis = [].slice.call(document.querySelectorAll("[data-count]"));
  if (kpis.length && !reduce && "IntersectionObserver" in window) {
    kpis.forEach(function (el) {
      var txt = el.textContent.trim();
      var m = txt.match(/\d+(?:[\s., ]\d{3})*/);
      if (!m) return;
      var fin = parseInt(m[0].replace(/\D/g, ""), 10);
      var pre = txt.slice(0, m.index), post = txt.slice(m.index + m[0].length);
      var kpi = el.closest(".kpi") || el;
      var DUR = 1800;
      function pinta(p) {
        el.textContent = pre + Math.round(fin * p) + post;
        kpi.style.setProperty("--p", p.toFixed(3));
      }
      pinta(0);
      var io = new IntersectionObserver(function (e) {
        if (!e[0].isIntersecting) return;
        io.disconnect();
        var t0 = performance.now();
        (function paso(now) {
          var t = Math.min((now - t0) / DUR, 1);
          /* Sale rapido y frena al llegar: la cifra se asienta, no choca. */
          pinta(1 - Math.pow(1 - t, 3));
          if (t < 1) requestAnimationFrame(paso);
          else el.textContent = txt;
        })(t0);
      }, { threshold: 0.6 });
      io.observe(el);
    });
  }

  /* ---------- Engagements : pestanas con avance automatico ----------
     Las etapas pasan solas. Pasar el mouse por encima o enfocar con el
     teclado solo PAUSA (para poder leer con calma) y al salir sigue desde la
     misma etapa. Elegir una pestana a mano la muestra y el avance continua
     desde ahi. Tambien se detiene si la seccion no esta a la vista, para no
     gastar bateria animando algo que nadie ve. */
  var eng = document.querySelector(".eng");
  if (eng) {
    var tabs = [].slice.call(eng.querySelectorAll(".eng-tab"));
    var panes = [].slice.call(eng.querySelectorAll(".eng-pane"));
    var ind = eng.querySelector(".eng-ind");
    var idx = 0, auto = !reduce, visible = false, t0 = 0, raf = 0;
    var DUR = 5200;

    /* La regla es horizontal: el indicador toma el ancho y la posicion
       izquierda de la pestana activa. */
    function colocaInd() {
      var t = tabs[idx];
      eng.style.setProperty("--ind-x", t.offsetLeft + "px");
      eng.style.setProperty("--ind-w", t.offsetWidth + "px");
    }
    function muestra(i, foco) {
      idx = (i + tabs.length) % tabs.length;
      tabs.forEach(function (t, k) {
        var on = k === idx;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        panes[k].hidden = !on;
      });
      colocaInd();
      t0 = performance.now();
      if (foco) tabs[idx].focus();
    }
    /* Pausa: el tiempo ya corrido se guarda y al reanudar se descuenta,
       asi la barra sigue desde donde quedo y no vuelve a cero. */
    var pausa = false, corrido = 0;
    function para() {
      if (!auto || pausa) return;
      pausa = true;
      corrido = performance.now() - t0;
    }
    function sigue() {
      if (!auto || !pausa) return;
      pausa = false;
      t0 = performance.now() - corrido;
    }
    function late(now) {
      if (!auto) return;
      if (pausa) {
        /* quieto */
      } else if (visible) {
        var p = (now - t0) / DUR;
        if (p >= 1) { muestra(idx + 1); p = 0; }
        eng.style.setProperty("--ind-p", p.toFixed(3));
      } else {
        t0 = now;
      }
      raf = requestAnimationFrame(late);
    }

    tabs.forEach(function (t, k) {
      t.addEventListener("click", function () {
        muestra(k); corrido = 0;
        eng.style.setProperty("--ind-p", 0);
      });
      t.addEventListener("keydown", function (e) {
        var d = e.key === "ArrowDown" || e.key === "ArrowRight" ? 1
              : e.key === "ArrowUp"   || e.key === "ArrowLeft"  ? -1 : 0;
        if (!d) return;
        e.preventDefault(); muestra(k + d, true); corrido = 0;
        eng.style.setProperty("--ind-p", 0);
      });
    });
    eng.addEventListener("pointerenter", function (e) { if (e.pointerType === "mouse") para(); });
    eng.addEventListener("pointerleave", function (e) { if (e.pointerType === "mouse") sigue(); });
    eng.addEventListener("focusin", function () { if (eng.querySelector(":focus-visible")) para(); });
    eng.addEventListener("focusout", function (e) { if (!eng.contains(e.relatedTarget)) sigue(); });

    muestra(0);
    eng.setAttribute("data-auto", auto ? "on" : "off");
    if (!auto) eng.style.setProperty("--ind-p", 1);
    addEventListener("resize", colocaInd);

    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (e) { visible = e[0].isIntersecting; },
        { threshold: 0.35 }).observe(eng);
    } else { visible = true; }
    if (auto) raf = requestAnimationFrame(late);
  }

  /* ---------- Particuliers : selector de modo ----------
     Sin JavaScript los dos modos se ven lado a lado. Con JavaScript aparece
     el selector y se muestra uno por vez. Pestanas ARIA de libro: flechas
     para moverse, y solo la activa entra en el orden de tabulacion. */
  var ways = document.querySelector(".ways");
  if (ways) {
    var wTabs = [].slice.call(ways.querySelectorAll(".ways-tab"));
    var wPanes = wTabs.map(function (t) { return document.getElementById(t.getAttribute("aria-controls")); });
    function elige(i, foco) {
      wTabs.forEach(function (t, k) {
        var on = k === i;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        /* No se usa hidden: los dos paneles comparten celda y el inactivo se
           funde. aria-hidden + inert lo sacan del lector y del tabulador. */
        wPanes[k].setAttribute("aria-hidden", on ? "false" : "true");
        wPanes[k].inert = !on;
        wPanes[k].setAttribute("role", "tabpanel");
      });
      ways.setAttribute("data-sel", String(i + 1));
      if (foco) wTabs[i].focus();
    }
    wTabs.forEach(function (t, k) {
      t.addEventListener("click", function () { elige(k); });
      t.addEventListener("keydown", function (e) {
        var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        elige((k + d + wTabs.length) % wTabs.length, true);
      });
    });
    ways.querySelector(".ways-sw").hidden = false;
    ways.setAttribute("data-on", "");
    elige(Math.max(0, (parseInt(ways.getAttribute("data-ways"), 10) || 1) - 1));
    /* La pastilla nace ya en su sitio: sin esto se veria deslizarse al cargar. */
    requestAnimationFrame(function () { ways.setAttribute("data-ready", ""); });
  }

  /* ---------- Acordeon horizontal (soutien au nouvel arrivant) ----------
     Una columna abierta por vez. El ancho lo reparte el CSS a partir de
     data-open en el contenedor: aca solo se escribe que numero esta abierto,
     asi la animacion vive entera en la hoja de estilos y el JavaScript no
     toca ni un pixel.
     El cuerpo de una columna cerrada sigue en el DOM —el buscador lo ve— pero
     se saca del tabulador con inert: si no, se tabula a un texto invisible. */
  var hacc = document.querySelector(".hacc");
  if (hacc) {
    var hcols = [].slice.call(hacc.querySelectorAll(".hcol"));
    function abreCol(i) {
      hacc.setAttribute("data-open", i === null ? "0" : String(i + 1));
      hcols.forEach(function (c, k) {
        var on = k === i;
        c.toggleAttribute("data-on", on);
        c.querySelector(".hcol-btn").setAttribute("aria-expanded", on ? "true" : "false");
        var cuerpo = c.querySelector(".hcol-body");
        cuerpo.inert = !on;
      });
    }
    /* En escritorio basta pasar el mouse: la columna se abre sola. El retardo
       corto evita que se abran y cierren todas mientras el cursor cruza la
       fila para llegar a la que de verdad interesa. Al salir no se cierra
       nada: dejar el panel vacio de golpe se lee como un parpadeo. */
    var finoHover = window.matchMedia("(hover:hover) and (pointer:fine)");
    var reloj = null;
    hcols.forEach(function (c, k) {
      c.querySelector(".hcol-btn").addEventListener("click", function () {
        clearTimeout(reloj);
        abreCol(c.hasAttribute("data-on") ? null : k);
      });
      c.addEventListener("mouseenter", function () {
        if (!finoHover.matches || c.hasAttribute("data-on")) return;
        clearTimeout(reloj);
        reloj = setTimeout(function () { abreCol(k); }, 90);
      });
      c.addEventListener("mouseleave", function () { clearTimeout(reloj); });
    });
    abreCol(null);
  }

  /* ---------- Avis Google ----------
     Los datos vienen de api/avis.php, que habla con la Places API del lado del
     servidor: la clave nunca llega al navegador y no se carga ningun script de
     terceros, que en Francia es ademas lo que evita el problema de RGPD.
     Si el endpoint no esta configurado, la seccion se queda con el aviso de
     pendiente. Nunca se inventa una opinion. */
  var avis = document.getElementById("avis");
  if (avis) {
    var rail = avis.querySelector('[data-avis="rail"]');

    function star(on) {
      return '<svg viewBox="0 0 20 19" aria-hidden="true"><path d="M10 0l2.6 6.3 6.8.5-5.2 4.4 1.6 6.6L10 14.2 4.2 17.8l1.6-6.6L.6 6.8l6.8-.5z" fill="'
        + (on ? "#f5a623" : "rgba(16,16,16,.16)") + '"/></svg>';
    }
    function stars(n) {
      var out = "";
      for (var i = 1; i <= 5; i++) out += star(i <= Math.round(n));
      return out;
    }
    function esc(t) {
      return String(t).replace(/[&<>"']/g, function (c) {
        return { "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[c];
      });
    }

    /* /en/ y /es/ viven un nivel mas abajo pero comparten el endpoint con la
       raiz: se sube ese nivel en vez de escribir una ruta absoluta, que
       rompe al abrir el archivo en local. */
    /* La ruta al endpoint la declara la seccion en data-api, porque depende de
       cuan hondo esta la pagina y eso no se puede deducir de la URL sin saber
       cuales son carpetas de idioma y cuales de pagina. */
    var api = avis.getAttribute("data-api") || "api/avis.php";
    fetch(api, { headers: { Accept: "application/json" } })
      .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
      .then(function (d) {
        if (!d || !d.reviews || !d.reviews.length) return;

        var n = avis.querySelector('[data-avis="rating"]');
        if (d.rating != null) n.textContent = String(d.rating).replace(".", ",");
        avis.querySelector('[data-avis="stars"]').innerHTML = stars(d.rating || 0);
        if (d.count != null) {
          avis.querySelector('[data-avis="count"]').textContent =
            d.count + (d.count > 1 ? " avis vérifiés" : " avis vérifié");
        }
        var src = avis.querySelector('[data-avis="src"]');
        if (d.mapsUri) src.setAttribute("href", d.mapsUri);

        rail.innerHTML = d.reviews.map(function (r) {
          /* Atribucion obligatoria de Google: nombre del autor, foto, fecha
             relativa y acceso directo a la opinion original. */
          var av = r.photo
            ? '<img class="avis-av" src="' + esc(r.photo) + '" alt="" width="32" height="32" loading="lazy" referrerpolicy="no-referrer">'
            : '<span class="avis-av"></span>';
          return '<a class="avis-card" role="listitem" href="' + esc(r.uri || d.mapsUri || "#")
            + '" target="_blank" rel="noopener nofollow">'
            + '<span class="avis-head">' + av
            + '<span class="avis-who"><span class="avis-nm">' + esc(r.author) + '</span>'
            + '<span class="avis-when">' + esc(r.when) + '</span></span></span>'
            + '<span class="stars" aria-label="' + (r.rating || "") + ' sur 5">' + stars(r.rating || 0) + '</span>'
            + '<span class="avis-txt">' + esc(r.text) + '</span></a>';
        }).join("");

        avis.setAttribute("data-state", "ok");
      })
      .catch(function () { /* Sin datos, queda el aviso de pendiente. */ });
  }

  /* ---------- Formulaire de contact ----------
     Dos perfiles en un mismo formulario. Empresa pide razon social y solo
     acepta un correo profesional; particular no. */
  var form = document.getElementById("ctForm");
  if (form) {
    var mail   = form.querySelector("#mail");
    var mailEr = form.querySelector("#mail-err");
    var canal  = form.querySelector("#canal");

    /* Dominios de correo personal y desechable. No se valida "que tenga
       dominio propio" al reves, listando lo permitido, porque eso dejaria
       afuera a cualquier empresa con un dominio que no conocemos. */
    var PERSO = [
      "gmail.com","googlemail.com","hotmail.com","hotmail.fr","outlook.com","outlook.fr",
      "live.com","live.fr","msn.com","yahoo.com","yahoo.fr","ymail.com","aol.com",
      "icloud.com","me.com","mac.com","protonmail.com","proton.me","gmx.com","gmx.fr",
      "free.fr","orange.fr","wanadoo.fr","sfr.fr","neuf.fr","laposte.net","bbox.fr",
      "numericable.fr","club-internet.fr","yandex.com","mail.ru","zoho.com",
      "mailinator.com","yopmail.com","jetable.org","guerrillamail.com","10minutemail.com"
    ];

    function domainOf(v) {
      var m = String(v).trim().toLowerCase().match(/^[^\s@]+@([^\s@]+\.[a-z]{2,})$/);
      return m ? m[1] : null;
    }

    function showErr(msg) {
      mailEr.textContent = msg;
      mailEr.hidden = !msg;
      mail.setAttribute("aria-invalid", msg ? "true" : "false");
      mail.classList.toggle("is-bad", !!msg);
    }

    /* Devuelve el mensaje de error, o "" si esta bien. */
    function checkMail() {
      var v = mail.value.trim();
      if (!v) return "";                       // el campo vacio lo avisa el submit
      var d = domainOf(v);
      if (!d) return "Adresse email invalide.";
      if (form.dataset.profil === "entreprise" && PERSO.indexOf(d) !== -1) {
        /* Corto a proposito: el aviso tiene un renglon reservado debajo del
           campo y si ocupa dos, empuja el resto del formulario al aparecer. */
        return "Merci d'utiliser une adresse professionnelle.";
      }
      return "";
    }

    function setProfil(p) {
      form.dataset.profil = p;
      form.querySelectorAll('[data-only]').forEach(function (el) {
        var on = el.getAttribute("data-only") === p;
        el.hidden = !on;
        var f = el.querySelector("input,select,textarea");
        if (f) { f.disabled = !on; f.required = on; }
      });
      showErr(checkMail());   // el mismo correo puede ser valido en un perfil y no en el otro
    }

    form.querySelectorAll('input[name="profil"]').forEach(function (r) {
      r.addEventListener("change", function () { if (r.checked) setProfil(r.value); });
    });
    setProfil(form.dataset.profil);

    mail.addEventListener("blur", function () { showErr(checkMail()); });
    mail.addEventListener("input", function () { if (mailEr.hidden === false) showErr(checkMail()); });

    form.addEventListener("submit", function (e) {
      var err = checkMail();
      var first = null;
      if (!mail.value.trim()) { err = "Merci d'indiquer une adresse email."; }
      showErr(err);
      if (err) first = mail;

      form.querySelectorAll("[required]").forEach(function (f) {
        if (f.disabled || f.value.trim()) return;
        f.classList.add("is-bad");
        if (!first) first = f;
      });
      form.querySelectorAll("[required]").forEach(function (f) {
        f.addEventListener("input", function () { f.classList.remove("is-bad"); }, { once: true });
      });

      if (first) { e.preventDefault(); first.focus(); return; }
      /* TODO produccion: aca se conecta Calendly o Typeform. */
      e.preventDefault();
    });

    if (canal) canal.addEventListener("change", function () { canal.classList.remove("is-bad"); });
  }

  /* ---------- Enlaces del menu a una prestacion concreta ----------
     El menu apunta a filas y acordeones (#gestion-visa, #changement-de-statut,
     #audit...). Llegar a una fila cerrada obliga a buscarla y abrirla a mano:
     aca se abre sola, en el modo que corresponda si vive en el selector de
     particuliers, y se vuelve a centrar porque al abrirse cambia el alto. */
  function abreDestino() {
    var id = decodeURIComponent(location.hash.slice(1));
    var el = id && document.getElementById(id);
    if (!el) return;
    var pane = el.closest(".mode");
    if (pane && ways && wPanes.indexOf(pane) >= 0) elige(wPanes.indexOf(pane));
    if (el.tagName === "DETAILS" && !el.open) el.open = true;
    if (el.classList.contains("row") && el.getAttribute("data-open") !== "true") {
      el.querySelector(".row-btn").click();
    }
    if (el.tagName === "DETAILS" || el.classList.contains("row")) {
      setTimeout(function () {
        el.scrollIntoView({ block: "center", behavior: reduce ? "auto" : "smooth" });
      }, 80);
    }
  }
  abreDestino();
  addEventListener("hashchange", abreDestino);

})();
