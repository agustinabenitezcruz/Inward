(function(){
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Textos que arma el JavaScript (formulario, opiniones). El HTML se traduce
     con build.py; esto no pasa por ahi, asi que lleva su propio diccionario
     segun el idioma de la pagina. */
  var LANG = (document.documentElement.lang || "fr").slice(0, 2);
  var TXT = {
    fr: { invalid: "Adresse email invalide.", pro: "Merci d'utiliser une adresse professionnelle.",
          empty: "Merci d'indiquer une adresse email.", reviews: [" avis Google", " avis Google"], of5: " sur 5",
          demo: "Aperçu : avis fictifs, pour visualiser la mise en page",
          doneH: "Merci, votre demande a bien été envoyée.",
          doneP: "La personne qui suivra votre dossier vous recontactera très prochainement.",
          fail: "L'envoi n'a pas abouti. Réessayez dans un instant ou écrivez-nous à ",
          ytAsk: "Cette vidéo est hébergée par YouTube, qui peut déposer des cookies. Acceptez-vous de la charger\u00a0?",
          ytOk: "Accepter et lire la vidéo", ytMore: "Gérer mes cookies" },
    en: { invalid: "Invalid email address.", pro: "Please use a business email address.",
          empty: "Please enter an email address.", reviews: [" Google review", " Google reviews"], of5: " out of 5",
          demo: "Preview: sample reviews, to show the layout",
          doneH: "Thank you, your request has been sent.",
          doneP: "The person who will handle your case will get back to you shortly.",
          fail: "Your message could not be sent. Please try again in a moment or write to us at ",
          ytAsk: "This video is hosted by YouTube, which may set cookies. Do you agree to load it?",
          ytOk: "Accept and play the video", ytMore: "Manage my cookies" },
    es: { invalid: "Dirección de email no válida.", pro: "Utilice una dirección de email profesional.",
          empty: "Indique una dirección de email.", reviews: [" opinión en Google", " opiniones en Google"], of5: " de 5",
          demo: "Vista previa: opiniones de ejemplo, para ver el diseño",
          doneH: "Gracias, su solicitud fue enviada.",
          doneP: "La persona que llevará su expediente se pondrá en contacto con usted muy pronto.",
          fail: "No se pudo enviar. Vuelva a intentarlo en un momento o escríbanos a ",
          ytAsk: "Este video está alojado en YouTube, que puede instalar cookies. ¿Acepta cargarlo?",
          ytOk: "Aceptar y ver el video", ytMore: "Gestionar mis cookies" }
  };
  var T = TXT[LANG] || TXT.fr;

  /* ---------- Invitacion a bajar ----------
     El hero ocupa toda la pantalla y de la seccion siguiente solo asoma el
     borde redondeado. Si el visitante no baja, ese borde da dos saltitos
     (.nudge en el CSS): a los 1,6 s y despues cada 5 s, tres veces como
     maximo. Al primer scroll se corta. */
  (function () {
    var hero = document.querySelector(".hero");
    if (!hero || reduce) return;
    var sig = hero.nextElementSibling;
    while (sig && sig.tagName !== "SECTION") sig = sig.nextElementSibling;
    if (!sig || !sig.classList.contains("band-top")) return;
    var veces = 0, reloj = null;
    function salta() {
      if (window.scrollY > 20 || veces >= 3) return;
      veces++;
      sig.classList.remove("nudge");
      void sig.offsetWidth;
      sig.classList.add("nudge");
      reloj = setTimeout(salta, 5000);
    }
    sig.addEventListener("animationend", function (e) {
      if (e.target === sig) sig.classList.remove("nudge");
    });
    addEventListener("scroll", function () {
      if (window.scrollY > 20) { clearTimeout(reloj); veces = 3; }
    }, { passive: true });
    if (window.scrollY <= 20) reloj = setTimeout(salta, 1600);
  })();

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
      /* La primera marca de la lista (Chubb, la mas importante para la
         clienta) arranca en el centro de la pantalla, no en el borde
         izquierdo donde el fundido la borraba: el carril empieza la vuelta
         ya avanzada con un retardo negativo. */
      function vel() {
        var dur = Math.max(ul.offsetWidth / 38, 12);
        track.style.setProperty("--marq-dur", dur + "s");
        var li = ul.querySelector("li");
        if (!li) return;
        var ciclo = ul.offsetWidth;
        var r = li.getBoundingClientRect(), u = ul.getBoundingClientRect();
        var d = marq.offsetWidth / 2 - (r.left - u.left + r.width / 2);
        var avance = ((ciclo - d) % ciclo + ciclo) % ciclo;
        track.style.animationDelay = (-dur * avance / ciclo) + "s";
      }
      vel();
      addEventListener("load", vel);
      /* Pausada mientras no se ve: la animacion infinita sigue costando
         cuadros aunque este fuera de pantalla. */
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (e) {
          marq.classList.toggle("is-off", !e[0].isIntersecting);
        }).observe(marq);
      }
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
      /* Sobre el hero el rail no se muestra: no hay secciones que recorrer
         todavia y competia con el titular. Aparece cuando la primera seccion
         llega al centro de la ventana. */
      var enHero = sobreHero || overDark.some(function (d) { return d.classList.contains("lp-hero"); });
      railNav.setAttribute("data-hero", enHero ? "true" : "false");
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
        var tg = it.querySelector(".nav-tog");
        if (tg) tg.setAttribute("aria-expanded", "false");
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

    /* Telefono y tablet: el nombre del grupo (Entreprises, Particuliers,
       Ressources) es un enlace normal y lleva a su pagina. El submenu se abre
       SOLO con la flecha de al lado (.nav-tog). Un grupo por vez: dos
       abiertos en una pantalla chica obligan a buscar el segundo titulo. */
    menu.querySelectorAll(".nav-tog").forEach(function (tog) {
      tog.addEventListener("click", function () {
        var item = tog.closest(".nav-item"), open = item.getAttribute("data-open") === "true";
        closeGroups();
        if (!open) {
          item.setAttribute("data-open", "true");
          tog.setAttribute("aria-expanded", "true");
        }
      });
    });

    /* Al elegir cualquier destino el menu se cierra: si no, el ancla salta
       detras del panel. */
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) setMenu(false);
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
      if (foco) tabs[idx].focus({ preventScroll: true });
      /* En tablet y celular la fila de titulos se desplaza de costado: la
         pestana activa se centra en la tira, asi el titulo del texto que se
         esta leyendo siempre esta a la vista. Se mueve solo la tira, nunca la
         pagina. */
      var lista = tabs[idx].parentNode;
      if (lista.scrollWidth > lista.clientWidth + 2) {
        var t = tabs[idx];
        lista.scrollTo({ left: t.offsetLeft - (lista.clientWidth - t.offsetWidth) / 2,
                         behavior: reduce ? "auto" : "smooth" });
      }
    }
    /* Bordes desvanecidos solo del lado donde hay mas titulos. */
    var engList = eng.querySelector(".eng-list");
    function bordes() {
      var max = engList.scrollWidth - engList.clientWidth;
      engList.setAttribute("data-l", engList.scrollLeft > 4 ? "1" : "0");
      engList.setAttribute("data-r", engList.scrollLeft < max - 4 ? "1" : "0");
    }
    engList.addEventListener("scroll", bordes, { passive: true });
    window.addEventListener("resize", bordes);
    bordes();
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
        ind.style.setProperty("--ind-p", p.toFixed(3));
      } else {
        /* Fuera de pantalla el bucle se detiene: no se gasta un cuadro por
           segundo en algo que nadie ve. Lo reanuda el observer. */
        raf = 0;
        return;
      }
      raf = requestAnimationFrame(late);
    }

    tabs.forEach(function (t, k) {
      t.addEventListener("click", function () {
        muestra(k); corrido = 0;
        ind.style.setProperty("--ind-p", 0);
      });
      t.addEventListener("keydown", function (e) {
        var d = e.key === "ArrowDown" || e.key === "ArrowRight" ? 1
              : e.key === "ArrowUp"   || e.key === "ArrowLeft"  ? -1 : 0;
        if (!d) return;
        e.preventDefault(); muestra(k + d, true); corrido = 0;
        ind.style.setProperty("--ind-p", 0);
      });
    });
    eng.addEventListener("pointerenter", function (e) { if (e.pointerType === "mouse") para(); });
    eng.addEventListener("pointerleave", function (e) { if (e.pointerType === "mouse") sigue(); });
    eng.addEventListener("focusin", function () { if (eng.querySelector(":focus-visible")) para(); });
    eng.addEventListener("focusout", function (e) { if (!eng.contains(e.relatedTarget)) sigue(); });

    muestra(0);
    eng.setAttribute("data-auto", auto ? "on" : "off");
    if (!auto) ind.style.setProperty("--ind-p", 1);
    addEventListener("resize", colocaInd);

    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (e) {
        visible = e[0].isIntersecting;
        if (visible && auto && !raf) { t0 = performance.now() - corrido; raf = requestAnimationFrame(late); }
        if (!visible) corrido = 0;
      },
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

    /* Alto fijo en escritorio. Los textos de las columnas cerradas son
       invisibles pero siguen ocupando lugar: al abrir una, las otras se
       angostan, esos textos se parten en mas lineas y la seccion crecia de
       golpe (285 -> 386px a 1440px, con solo pasar el mouse). Se mide una
       copia oculta en los cinco estados —todo cerrado y cada columna abierta—
       y la rejilla toma el alto del mayor, asi abrir o cambiar de columna ya
       no mueve nada. En telefono es una lista que se despliega hacia abajo y
       ahi si tiene que crecer; lo hace con la transicion del CSS. */
    var haccCols = hacc.querySelector(".hacc-cols");
    var ancho = window.matchMedia("(min-width:861px)");
    function fijaAlto() {
      haccCols.style.removeProperty("--hacc-h");
      if (!ancho.matches) return;
      var copia = hacc.cloneNode(true);
      copia.removeAttribute("id");
      [].slice.call(copia.querySelectorAll("[id]")).forEach(function (el) { el.removeAttribute("id"); });
      copia.style.cssText = "position:absolute;left:-9999px;top:0;visibility:hidden;pointer-events:none;animation:none;width:" + hacc.offsetWidth + "px";
      var cc = copia.querySelector(".hacc-cols");
      cc.style.transition = "none";
      /* La copia hereda el alto fijo del CSS (height:var(--hacc-h, piso)) y
         con eso siempre median el piso: el boton de la columna abierta
         quedaba cortado. Se mide con alto libre. */
      cc.style.height = "auto";
      var cs = [].slice.call(copia.querySelectorAll(".hcol"));
      hacc.parentNode.appendChild(copia);
      var max = 0;
      for (var i = 0; i <= cs.length; i++) {
        copia.setAttribute("data-open", String(i));
        cs.forEach(function (c, k) { c.toggleAttribute("data-on", k === i - 1); });
        max = Math.max(max, cc.offsetHeight);
      }
      copia.remove();
      haccCols.style.setProperty("--hacc-h", Math.ceil(max) + "px");
    }
    fijaAlto();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fijaAlto);
    addEventListener("load", fijaAlto);
    var relojAlto = null;
    addEventListener("resize", function () { clearTimeout(relojAlto); relojAlto = setTimeout(fijaAlto, 150); });
  }

  /* ---------- Avis Google ----------
     Los datos vienen de api/avis.php, que habla con la Places API del lado del
     servidor: la clave nunca llega al navegador y no se carga ningun script de
     terceros, que en Francia es ademas lo que evita el problema de RGPD.
     Si el endpoint no esta configurado, la seccion se queda con el aviso de
     pendiente. Nunca se inventa una opinion. */
  var avis = document.getElementById("avis");
  function fotosAvis() {
    if (!avis || !window.inwardConsent || !inwardConsent("inwardavis")) return;
    [].slice.call(avis.querySelectorAll(".avis-ini[data-photo]")).forEach(function (sp) {
      var im = document.createElement("img");
      im.className = "avis-av"; im.alt = ""; im.width = 32; im.height = 32;
      im.loading = "lazy"; im.referrerPolicy = "no-referrer";
      im.src = sp.getAttribute("data-photo");
      sp.replaceWith(im);
    });
  }
  document.addEventListener("inward:consent", function (e) {
    if (e.detail && e.detail.servicio === "inwardavis" && e.detail.ok) fotosAvis();
  });
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
    /* Vista previa para la clienta: con ?avis=demo en la URL se pinta la
       franja con contenido de RELLENO (lorem ipsum y cifras "X"), para ver el
       espaciado antes de conectar la cuenta de Google. No hay nombres ni
       opiniones inventadas que puedan pasar por reales, y nunca aparece sin
       el parametro. */
    var demo = /(?:^|[?&])avis=demo(?:&|$)/.test(location.search.slice(1));
    var DEMO = {
      rating: "X,X", stars: 5, countText: "X", mapsUri: "https://www.google.com/maps?cid=1377371409426816352",
      reviews: [
        { author: "Lorem I.", when: "Lorem ipsum", rating: 5, text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna." },
        { author: "Dolor S.", when: "Lorem ipsum", rating: 5, text: "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo." },
        { author: "Amet C.", when: "Lorem ipsum", rating: 5, text: "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur, excepteur sint occaecat." },
        { author: "Elit S.", when: "Lorem ipsum", rating: 5, text: "Sunt in culpa qui officia deserunt mollit anim id est laborum." },
        { author: "Tempor I.", when: "Lorem ipsum", rating: 5, text: "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores." }
      ]
    };
    (demo ? Promise.resolve(DEMO) : fetch(api, { headers: { Accept: "application/json" } })
      .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); }))
      .then(function (d) {
        if (!d || !d.reviews || !d.reviews.length) return;

        var n = avis.querySelector('[data-avis="rating"]');
        if (d.rating != null) n.textContent = String(d.rating).replace(".", ",");
        avis.querySelector('[data-avis="stars"]').innerHTML = stars(d.stars || d.rating || 0);
        if (d.countText) {
          avis.querySelector('[data-avis="count"]').textContent = d.countText + T.reviews[1];
        } else if (d.count != null) {
          avis.querySelector('[data-avis="count"]').textContent =
            d.count + T.reviews[d.count > 1 ? 1 : 0];
        }
        var src = avis.querySelector('[data-avis="src"]');
        if (d.mapsUri) src.setAttribute("href", d.mapsUri);

        rail.innerHTML = d.reviews.map(function (r) {
          /* Atribucion obligatoria de Google: nombre del autor, foto, fecha
             relativa y acceso directo a la opinion original. */
          /* La foto viene de Google: se pide recien con el consentimiento
             (consent.js, servicio "inwardavis"). Mientras, la inicial. */
          var ini = esc(String(r.author || "").trim().charAt(0).toUpperCase());
          var av = '<span class="avis-av avis-ini" aria-hidden="true"'
            + (r.photo ? ' data-photo="' + esc(r.photo) + '"' : '') + '>' + ini + '</span>';
          return '<a class="avis-card" role="listitem" href="' + esc(r.uri || d.mapsUri || "#")
            + '" target="_blank" rel="noopener nofollow">'
            + '<span class="avis-head">' + av
            + '<span class="avis-who"><span class="avis-nm">' + esc(r.author) + '</span>'
            + '<span class="avis-when">' + esc(r.when) + '</span></span></span>'
            + '<span class="stars" aria-label="' + (r.rating || "") + T.of5 + '">' + stars(r.rating || 0) + '</span>'
            + '<span class="avis-txt">' + esc(r.text) + '</span></a>';
        }).join("");

        avis.setAttribute("data-state", "ok");
        fotosAvis();
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
      if (!d) return T.invalid;
      if (form.dataset.profil === "entreprise" && PERSO.indexOf(d) !== -1) {
        /* Corto a proposito: el aviso tiene un renglon reservado debajo del
           campo y si ocupa dos, empuja el resto del formulario al aparecer. */
        return T.pro;
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
      if (!mail.value.trim()) { err = T.empty; }
      showErr(err);
      if (err) first = mail;

      form.querySelectorAll("[required]").forEach(function (f) {
        if (f.disabled || (f.type === "checkbox" ? f.checked : f.value.trim())) return;
        f.classList.add("is-bad");
        if (!first) first = f;
      });
      form.querySelectorAll("[required]").forEach(function (f) {
        f.addEventListener(f.type === "checkbox" ? "change" : "input", function () { f.classList.remove("is-bad"); }, { once: true });
      });

      e.preventDefault();
      if (first) { first.focus(); return; }
      envia();
    });

    /* Envio: api/contact.php manda la consulta por mail al equipo. Sin
       Calendly en el formulario (pedido de la clienta): la reserva de llamada
       va aparte, como enlace debajo del mail en la columna de contacto. La
       ruta al endpoint sale de donde esta main.js, asi funciona igual en la
       home, en las landings y en /en/ y /es/. */
    var abierto = Date.now();
    var base = (document.querySelector('script[src*="assets/js/main.js"]') || {}).src || "";
    base = base.split("assets/js/main.js")[0];
    var msgBox = form.querySelector(".ct-msg");
    var boton = form.querySelector('button[type="submit"]');
    function val(id) { var el = form.querySelector("#" + id); return el && !el.disabled ? el.value.trim() : ""; }
    function envia() {
      boton.disabled = true;
      msgBox.hidden = true;
      var datos = {
        nom: val("nom"), mail: val("mail"), societe: val("societe"),
        dem: val("dem"), canal: val("canal"), msg: val("msg"),
        rgpd: !!(form.querySelector("#rgpd") || {}).checked, news: !!(form.querySelector("#news") || {}).checked,
        profil: form.dataset.profil, site: (form.querySelector("#site") || {}).value || "",
        t: Date.now() - abierto, page: location.pathname
      };
      fetch(base + "api/contact.php", {
        method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(datos)
      })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (d) {
          if (!d || !d.ok) throw new Error("envio");
          form.innerHTML = '<div class="ct-done" role="status">'
            + '<h3>' + T.doneH + '</h3>'
            + '<p>' + T.doneP + '</p>'
            + '</div>';
        })
        .catch(function () {
          boton.disabled = false;
          msgBox.hidden = false;
          msgBox.innerHTML = T.fail
            + '<a href="mailto:info@inwardpro.com">info@inwardpro.com</a>.';
        });
    }

    if (canal) canal.addEventListener("change", function () { canal.classList.remove("is-bad"); });
  }

  /* ---------- Enlaces del menu a una prestacion concreta ----------
     El menu apunta a filas y acordeones (#gestion-visa, #changement-de-statut,
     #audit...). Llegar a una fila cerrada obliga a buscarla y abrirla a mano:
     aca se abre sola, en el modo que corresponda si vive en el selector de
     particuliers, y se vuelve a centrar porque al abrirse cambia el alto. */
  /* ---------- Servicios de empresas: pestanas verticales ----------
     Clic, flechas arriba/abajo, Inicio y Fin. Solo cambia que panel se ve:
     los cinco estan en el HTML. En telefono el CSS muestra los cinco seguidos
     y esconde la lista, asi que esto no interviene. */
  var stabs = document.querySelector(".stabs");
  var eligeServicio = null, abrePanel = null;
  if (stabs) {
    var sBtns = [].slice.call(stabs.querySelectorAll(".stb"));
    var sPanes = sBtns.map(function (b) { return document.getElementById(b.getAttribute("aria-controls")); });
    stabs.classList.add("is-js");
    eligeServicio = function (i, foco) {
      sBtns.forEach(function (b, k) {
        var on = k === i;
        b.setAttribute("aria-selected", on ? "true" : "false");
        b.tabIndex = on ? 0 : -1;
        sPanes[k].hidden = !on;
      });
      if (foco) sBtns[i].focus();
    };
    /* En escritorio alcanza con pasar el mouse por el servicio. Retardo
       corto para que cruzar la lista hacia el panel no vaya cambiando de
       servicio por el camino. */
    var sHover = window.matchMedia("(hover:hover) and (pointer:fine)"), sReloj = null;
    sBtns.forEach(function (b, k) {
      b.addEventListener("click", function () { clearTimeout(sReloj); eligeServicio(k); });
      b.addEventListener("mouseenter", function () {
        if (!sHover.matches || b.getAttribute("aria-selected") === "true") return;
        clearTimeout(sReloj);
        sReloj = setTimeout(function () { eligeServicio(k); }, 110);
      });
      b.addEventListener("mouseleave", function () { clearTimeout(sReloj); });
      b.addEventListener("keydown", function (e) {
        var i = null, n = sBtns.length;
        if (e.key === "ArrowDown" || e.key === "ArrowRight") i = (k + 1) % n;
        else if (e.key === "ArrowUp" || e.key === "ArrowLeft") i = (k - 1 + n) % n;
        else if (e.key === "Home") i = 0;
        else if (e.key === "End") i = n - 1;
        if (i === null) return;
        e.preventDefault();
        eligeServicio(i, true);
      });
    });
    eligeServicio(0);
    stabs.__panes = sPanes;

    /* Tablet y celular: las cinco cajas se ven juntas y la flecha de cada
       una la despliega. Una abierta por vez. En escritorio el boton del
       titulo no hace nada y queda fuera del tabulador. */
    var sMovil = window.matchMedia("(max-width:860px)");
    var sTogs = sPanes.map(function (pn) { return pn.querySelector(".stp-tog"); });
    abrePanel = function (pn, abrir) {
      sPanes.forEach(function (o, k) {
        var on = abrir && o === pn;
        o.toggleAttribute("data-open", on);
        sTogs[k].setAttribute("aria-expanded", on ? "true" : "false");
      });
    };
    sTogs.forEach(function (tg, k) {
      tg.addEventListener("click", function () {
        if (!sMovil.matches) return;
        abrePanel(sPanes[k], !sPanes[k].hasAttribute("data-open"));
      });
    });
    function modoServicios() {
      sTogs.forEach(function (tg) { tg.tabIndex = sMovil.matches ? 0 : -1; });
    }
    sMovil.addEventListener("change", modoServicios);
    modoServicios();
  }

  /* Una prestacion sola en su lista: queda siempre abierta, no se pliega. */
  [].slice.call(document.querySelectorAll("details.mode-solo")).forEach(function (d) {
    d.open = true;
    d.querySelector("summary").addEventListener("click", function (e) { e.preventDefault(); });
  });

  function abreDestino() {
    var id = decodeURIComponent(location.hash.slice(1));
    var el = id && document.getElementById(id);
    if (!el) return;
    if (stabs && el.classList.contains("stp") && eligeServicio) {
      eligeServicio(stabs.__panes.indexOf(el));
      if (abrePanel && window.matchMedia("(max-width:860px)").matches) abrePanel(el, true);
      setTimeout(function () {
        stabs.scrollIntoView({ block: "start", behavior: reduce ? "auto" : "smooth" });
      }, 80);
      return;
    }
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
  /* ---------- Entradas por reloj, no por scroll ----------
     Las entradas estaban atadas al scroll (animation-timeline:view()): avanzaban
     solo mientras el usuario movia la rueda, y si algo quedaba abajo de todo
     de la pantalla se quedaba a medio aparecer. Pedido de la clienta: que cada
     animacion termine sola una vez que el elemento entro en pantalla.
     Se buscan los elementos cuya animacion usa view() (asi no hay que mantener
     una lista a mano: el CSS sigue diciendo que gesto hace cada uno), se
     marcan con data-rev y el CSS los pasa al reloj, en pausa. Al entrar en la
     ventana, el observer los pone en marcha; los que entran juntos se
     escalonan 70 ms, con tope de 420 ms. No toca el rail ni el hero, que son
     efectos ligados al scroll a proposito (timeline con nombre o scroll()). */
  if (!reduce && scrollTimeline && "IntersectionObserver" in window) {
    var revs = [].filter.call(document.querySelectorAll("body *"), function (el) {
      if (el.hasAttribute("data-onload")) return false;
      var t = getComputedStyle(el).animationTimeline || "";
      return t.indexOf("view(") > -1;
    });
    /* Los logos del carrusel se mueven en horizontal y muchos estan fuera de
       la franja visible: para el observer nunca "entran". Por eso lo que se
       observa es el carrusel entero (.marq) y al entrar se encienden todos. */
    var grupos = new Map();
    revs.forEach(function (el) {
      el.setAttribute("data-rev", "");
      var t = el.closest(".marq") || el;
      if (!grupos.has(t)) grupos.set(t, []);
      grupos.get(t).push(el);
    });
    var ioRev = new IntersectionObserver(function (entries) {
      var n = 0;
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        (grupos.get(e.target) || []).forEach(function (el) {
          el.style.setProperty("--rd", Math.min(n++ * 70, 420) + "ms");
          el.setAttribute("data-rev", "in");
        });
        ioRev.unobserve(e.target);
      });
    }, { rootMargin: "0px 0px -6% 0px" });
    grupos.forEach(function (_, t) { ioRev.observe(t); });
  }

  abreDestino();
  addEventListener("hashchange", abreDestino);


  /* ---------- Landing de visa: linea de tiempo del hexagono ----------
     Corre una sola vez al entrar en pantalla y termina sola. En reposo el
     hexagono ya esta completo, asi que sin JS o con movimiento reducido se lee
     igual. */
  (function () {
    var tls = [].slice.call(document.querySelectorAll(".vl-tl"));
    if (!tls.length || !("IntersectionObserver" in window)) return;
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    /* Se observa la seccion entera, no el panel: asi el hexagono arranca en
       el mismo momento en que aparecen el rotulo y el titulo. */
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        var t = e.target.querySelector(".vl-sw-p:not([hidden]) .vl-tl") || e.target.querySelector(".vl-tl");
        if (t) t.classList.add("is-play");
      });
    }, { threshold: 0.2 });
    var secs = [];
    tls.forEach(function (t) { var s = t.closest("section") || t; if (secs.indexOf(s) < 0) { secs.push(s); io.observe(s); } });
  })();


  /* ---------- Landing de visa: lista de ventajas ----------
     Al entrar en pantalla las filas aparecen una tras otra y cada tilde se
     enciende. Una sola vez; termina sola. */
  (function () {
    var ls = [].slice.call(document.querySelectorAll(".vl-hc"));
    if (!ls.length || !("IntersectionObserver" in window)) return;
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        e.target.classList.add("is-play");
      });
    }, { threshold: 0.25 });
    ls.forEach(function (l) { io.observe(l); });
  })();


  /* ---------- Landing de visa: propuestas de ventajas ---------- */
  (function () {
    var reduceM = matchMedia("(prefers-reduced-motion: reduce)").matches;
    /* A: selector + foto, con recorrido automatico */
    [].slice.call(document.querySelectorAll("[data-vla]")).forEach(function (box) {
      var tabs = [].slice.call(box.querySelectorAll(".vla-tab"));
      var imgs = [].slice.call(box.querySelectorAll(".vla-img"));
      var caps = [].slice.call(box.querySelectorAll(".vla-cap"));
      var cur = 0, timer = null, vis = false, user = false;
      function show(i) {
        cur = i;
        tabs.forEach(function (t, k) { t.setAttribute("aria-selected", k === i ? "true" : "false"); t.tabIndex = k === i ? 0 : -1; });
        imgs.forEach(function (m, k) { m.classList.toggle("is-on", k === i); });
        caps.forEach(function (c, k) { c.classList.toggle("is-on", k === i); c.setAttribute("aria-hidden", k === i ? "false" : "true"); });
        if (box.classList.contains("is-auto")) {
          var a = tabs[i]; a.classList.remove("rs"); void a.offsetWidth;
        }
      }
      function stop() { clearInterval(timer); timer = null; box.classList.remove("is-auto"); }
      function start() {
        if (user || reduceM || timer || !vis) return;
        box.classList.add("is-auto"); show(cur);
        timer = setInterval(function () { show((cur + 1) % tabs.length); }, 4000);
      }
      tabs.forEach(function (t, k) {
        t.addEventListener("click", function () { user = true; stop(); show(k); });
        t.addEventListener("mouseenter", function () { if (matchMedia("(hover:hover)").matches) { user = true; stop(); show(k); } });
        t.addEventListener("keydown", function (e) {
          var d = e.key === "ArrowDown" || e.key === "ArrowRight" ? 1 : e.key === "ArrowUp" || e.key === "ArrowLeft" ? -1 : 0;
          if (!d) return; e.preventDefault(); user = true; stop();
          var n = (cur + d + tabs.length) % tabs.length; show(n); tabs[n].focus();
        });
      });
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (es) {
          vis = es[0].isIntersecting; if (vis) start(); else stop();
        }, { threshold: 0.35 }).observe(box);
      }
    });
    /* B: carrusel con flechas, arrastre y barra de avance */
    [].slice.call(document.querySelectorAll(".vlb-track")).forEach(function (tr) {
      var sec = tr.closest("section");
      var prev = sec.querySelector('.vlb-arw[data-dir="-1"]'), next = sec.querySelector('.vlb-arw[data-dir="1"]');
      var bar = sec.querySelector(".vlb-bar span");
      function step() { var c = tr.querySelector(".vlb-c"); return c ? c.getBoundingClientRect().width + 16 : 300; }
      function upd() {
        var max = tr.scrollWidth - tr.clientWidth;
        prev.disabled = tr.scrollLeft <= 2; next.disabled = tr.scrollLeft >= max - 2;
        if (bar) { var w = tr.clientWidth / tr.scrollWidth; bar.style.width = (w * 100) + "%"; bar.style.translate = (max > 0 ? (tr.scrollLeft / max) * ((1 - w) / w) * 100 : 0) + "% 0"; }
      }
      [prev, next].forEach(function (b) { b.addEventListener("click", function () { tr.scrollBy({ left: step() * +b.dataset.dir, behavior: reduceM ? "auto" : "smooth" }); }); });
      tr.addEventListener("scroll", upd, { passive: true }); addEventListener("resize", upd); upd();
      var down = false, x0 = 0, s0 = 0, moved = false;
      tr.addEventListener("pointerdown", function (e) { if (e.pointerType !== "mouse") return; down = true; moved = false; x0 = e.clientX; s0 = tr.scrollLeft; });
      addEventListener("pointermove", function (e) { if (!down) return; var dx = e.clientX - x0; if (Math.abs(dx) > 4) { moved = true; tr.classList.add("is-drag"); } tr.scrollLeft = s0 - dx; });
      addEventListener("pointerup", function () { if (!down) return; down = false; tr.classList.remove("is-drag");
        if (moved) { var st = step(); tr.scrollTo({ left: Math.round(tr.scrollLeft / st) * st, behavior: "smooth" }); } });
      /* Avance automatico cada 3,5 s; al llegar al final vuelve al principio.
         Se pausa con el mouse encima, con foco adentro, mientras se arrastra
         y fuera de pantalla. Con movimiento reducido no corre. */
      if (!reduceM && "IntersectionObserver" in window) {
        var auto = null, hover = false, focus = false, vis = false;
        function tick() {
          if (hover || focus || down) return;
          var max = tr.scrollWidth - tr.clientWidth;
          if (tr.scrollLeft >= max - 2) tr.scrollTo({ left: 0, behavior: "smooth" });
          else tr.scrollBy({ left: step(), behavior: "smooth" });
        }
        function run() { if (!auto && vis) auto = setInterval(tick, 3500); }
        function halt() { clearInterval(auto); auto = null; }
        tr.addEventListener("mouseenter", function () { hover = true; });
        tr.addEventListener("mouseleave", function () { hover = false; });
        sec.addEventListener("focusin", function () { focus = true; });
        sec.addEventListener("focusout", function () { focus = false; });
        [prev, next].forEach(function (b) { b.addEventListener("click", function () { halt(); run(); }); });
        new IntersectionObserver(function (es) { vis = es[0].isIntersecting; if (vis) run(); else halt(); }, { threshold: 0.3 }).observe(tr);
      }
    });
    /* D: contador 0 -> 7 al entrar en pantalla */
    [].slice.call(document.querySelectorAll("[data-vld-count]")).forEach(function (el) {
      if (reduceM || !("IntersectionObserver" in window)) return;
      var end = parseInt(el.textContent, 10) || 0;
      var io = new IntersectionObserver(function (es) {
        if (!es[0].isIntersecting) return; io.disconnect();
        var t0 = null;
        function f(t) { if (!t0) t0 = t; var k = Math.min(1, (t - t0) / 1400); el.textContent = Math.round(end * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(f); }
        el.textContent = "0"; requestAnimationFrame(f);
      }, { threshold: 0.5 });
      io.observe(el);
    });
  })();


  /* ---------- Fondos animados de hero: pausa fuera de pantalla ---------- */
  (function () {
    var hs = [].slice.call(document.querySelectorAll(".hero"));
    if (!hs.length || !("IntersectionObserver" in window)) return;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { e.target.classList.toggle("is-off", !e.isIntersecting); });
    }, { threshold: 0 });
    hs.forEach(function (h) { io.observe(h); });
  })();


  /* ---------- Landings de visa: selector de dos opciones ----------
     Pestanas accesibles (flechas, Inicio/Fin). Al cambiar a un panel con
     linea de tiempo, la animacion corre de nuevo desde cero. */
  [].slice.call(document.querySelectorAll("[data-vl-sw]")).forEach(function (sw) {
    var bs = [].slice.call(sw.querySelectorAll(".vl-sw-b"));
    var ps = [].slice.call(sw.querySelectorAll(".vl-sw-p"));
    var reduceM = matchMedia("(prefers-reduced-motion: reduce)").matches;
    function go(i, focus) {
      bs.forEach(function (b, k) { b.setAttribute("aria-selected", k === i ? "true" : "false"); b.tabIndex = k === i ? 0 : -1; });
      ps.forEach(function (p, k) { p.hidden = k !== i; });
      sw.style.setProperty("--sw-i", i);
      var tl = ps[i].querySelector(".vl-tl");
      if (tl && !reduceM) { tl.classList.remove("is-play"); void tl.offsetWidth; tl.classList.add("is-play"); }
      if (focus) bs[i].focus();
    }
    bs.forEach(function (b, k) {
      b.addEventListener("click", function () { go(k); });
      b.addEventListener("keydown", function (e) {
        var n = e.key === "ArrowRight" ? k + 1 : e.key === "ArrowLeft" ? k - 1 : e.key === "Home" ? 0 : e.key === "End" ? bs.length - 1 : null;
        if (n === null) return; e.preventDefault(); go((n + bs.length) % bs.length, true);
      });
    });
    sw.setAttribute("data-ready", "");
  });


  /* ---------- Menu: marca la pagina en la que esta la persona ----------
     Un enlace es "actual" si apunta a esta misma pagina (sin ancla, o con
     #top, que es como sync_shell escribe el enlace a uno mismo). Se subraya
     el item y el boton de su grupo. Si la pagina no esta en el menu (un
     articulo del blog, un video), se marca el grupo cuya ruta la contiene. */
  (function () {
    var norm = function (u) { return u.replace(/index\.html$/, "").replace(/\/?$/, "/"); };
    var here = norm(location.pathname);
    function isHere(a) {
      var u = new URL(a.getAttribute("href"), location.href);
      return norm(u.pathname) === here && (!u.hash || u.hash === "#top");
    }
    var marked = false;
    [].slice.call(document.querySelectorAll(".nav-item")).forEach(function (it) {
      var hit = [].slice.call(it.querySelectorAll(".mega li a")).filter(isHere);
      hit.forEach(function (a) { a.setAttribute("aria-current", "page"); });
      var btn = it.querySelector(".nav-btn");
      if (btn && (isHere(btn) || (hit.length && !marked))) { btn.setAttribute("data-current", ""); marked = true; }
    });
    if (!marked) {
      [].slice.call(document.querySelectorAll(".nav-item")).forEach(function (it) {
        if (marked) return;
        [].slice.call(it.querySelectorAll(".nav-btn, .mega li a")).some(function (a) {
          var u = new URL(a.getAttribute("href"), location.href);
          if (u.hash) return false;
          var p = norm(u.pathname);
          if (p !== here && here.indexOf(p) === 0) {
            it.querySelector(".nav-btn").setAttribute("data-current", "");
            if (a.closest(".mega")) a.setAttribute("aria-current", "page");
            marked = true; return true;
          }
          return false;
        });
      });
    }
  })();

  /* Video con fachada: al tocar la miniatura se cambia por el reproductor
     de YouTube (youtube-nocookie) y arranca solo. */
  /* Sin consentimiento para YouTube (consent.js) no se crea el iframe: se
     muestra un aviso encima de la miniatura con "Accepter et lire". Si la
     pagina no tiene CMP (vista previa sin consent.js), se reproduce igual. */
  function pideYoutube(caja, lanza) {
    if (!window.inwardConsent || inwardConsent("inwardyoutube")) { lanza(); return; }
    var viejo = caja.querySelector(".yt-gate");
    if (viejo) viejo.remove();
    var g = document.createElement("div");
    g.className = "yt-gate";
    g.setAttribute("role", "group");
    g.innerHTML = '<p>' + T.ytAsk + '</p><div class="yt-gate-act">'
      + '<button type="button" class="btn btn-primary yt-ok">' + T.ytOk + ' <span class="arw">&rsaquo;</span></button>'
      + '<button type="button" class="yt-more">' + T.ytMore + '</button></div>';
    caja.appendChild(g);
    g.querySelector(".yt-ok").addEventListener("click", function () {
      window.inwardAllow("inwardyoutube");
      g.remove();
      lanza();
    });
    g.querySelector(".yt-more").addEventListener("click", function () { window.inwardPanel(); });
    g.querySelector(".yt-ok").focus();
  }
  document.querySelectorAll(".vid-facade[data-yt]").forEach(function (b) {
    b.addEventListener("click", function () {
      pideYoutube(b.parentNode, function () {
      var f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + b.getAttribute("data-yt") + "?autoplay=1&rel=0";
      f.title = b.getAttribute("aria-label") || "";
      f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
      f.allowFullscreen = true;
      b.replaceWith(f);
      f.focus();
      });
    });
  });

  /* Video en modal: [data-video] abre el <dialog> indicado en aria-controls */
  (function () {
    document.querySelectorAll('[data-video]').forEach(function (btn) {
      var dlg = document.getElementById(btn.getAttribute('aria-controls'));
      if (!dlg || typeof dlg.showModal !== 'function') return;
      var box = dlg.querySelector('.vid-frame');
      btn.addEventListener('click', function () {
        dlg.showModal();
        pideYoutube(box, function () {
          var f = document.createElement('iframe');
          f.src = 'https://www.youtube-nocookie.com/embed/' + btn.getAttribute('data-video') + '?autoplay=1&rel=0';
          f.title = dlg.getAttribute('aria-label') || '';
          f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
          f.allowFullscreen = true;
          box.appendChild(f);
        });
      });
      dlg.querySelector('.vid-close').addEventListener('click', function () { dlg.close(); });
      dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
      dlg.addEventListener('close', function () { box.innerHTML = ''; btn.focus(); });
    });
  })();

})();
