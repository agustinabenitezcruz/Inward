/* Consentimiento de cookies (CMP): tarteaucitron.js, autoalojado en
   assets/vendor/tarteaucitron/ (v1.37.0, licencia MIT). Nada de terceros se
   carga antes de que la persona acepte:

     YouTube        el reproductor (youtube-nocookie) se crea recien al tocar
                    play Y con el servicio aceptado. Sin consentimiento, la
                    miniatura propia pide permiso ahi mismo (main.js).
     Avis Google    las opiniones salen de nuestro servidor (api/avis.php);
                    lo unico de Google son las fotos de los autores, que se
                    muestran solo con el servicio aceptado. Si no, iniciales.
     GA4 / GTM      no instalados todavia. Para activarlos basta escribir el
                    ID abajo: tarteaucitron los carga solo despues de "Accepter".

   Orden de carga (todos con defer, se ejecutan en este orden):
   consent.js -> tarteaucitron.min.js -> main.js. Por eso aca se fijan las
   variables globales que tarteaucitron lee al cargar (duracion del
   consentimiento) y el init se hace en DOMContentLoaded, cuando ya cargo. */

/* Consentimiento guardado 6 meses (recomendacion CNIL: 6 a 13). */
var tarteaucitronForceExpire = 183;
var tarteaucitronExpireInDay = true;

(function () {
  "use strict";

  /* ---- Medicion de audiencia: completar para activar ---- */
  var GA4_ID = "";   /* ej. "G-XXXXXXXXXX" */
  var GTM_ID = "";   /* ej. "GTM-XXXXXXX"  (usar uno u otro, no los dos) */

  var me = document.currentScript;
  var raiz = me ? new URL("../../", me.src).href : "/";
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var politica = raiz + (lang === "fr" ? "" : lang + "/") + "cookies/";

  /* Avisa a main.js cuando cambia un permiso, sin que main.js tenga que
     saber nada de tarteaucitron. */
  function avisa(nombre, ok) {
    document.dispatchEvent(new CustomEvent("inward:consent", { detail: { servicio: nombre, ok: ok } }));
  }
  window.inwardConsent = function (nombre) {
    return !!(window.tarteaucitron && tarteaucitron.state && tarteaucitron.state[nombre] === true);
  };
  window.inwardAllow = function (nombre) {
    if (window.tarteaucitron && tarteaucitron.setConsent) tarteaucitron.setConsent(nombre, true);
  };
  window.inwardPanel = function () {
    if (window.tarteaucitron && tarteaucitron.userInterface) tarteaucitron.userInterface.openPanel();
  };

  document.addEventListener("DOMContentLoaded", function () {
    if (!window.tarteaucitron) return;

    tarteaucitron.services.inwardyoutube = {
      key: "inwardyoutube",
      type: "video",
      name: "YouTube",
      uri: "https://policies.google.com/privacy",
      needConsent: true,
      cookies: ["VISITOR_INFO1_LIVE", "YSC", "PREF", "GPS"],
      js: function () { avisa("inwardyoutube", true); },
      fallback: function () { avisa("inwardyoutube", false); }
    };
    tarteaucitron.services.inwardavis = {
      key: "inwardavis",
      type: "other",
      name: "Google Business Profile (avis)",
      uri: "https://policies.google.com/privacy",
      needConsent: true,
      cookies: [],
      js: function () { avisa("inwardavis", true); },
      fallback: function () { avisa("inwardavis", false); }
    };

    var google = !!(GA4_ID || GTM_ID);
    tarteaucitron.init({
      privacyUrl: politica,
      readmoreLink: politica,
      bodyPosition: "top",
      hashtag: "#cookies",
      cookieName: "tarteaucitron",
      orientation: "bottom",
      groupServices: false,
      showDetailsOnClick: true,
      serviceDefaultState: "wait",
      showAlertSmall: false,
      cookieslist: true,
      cookieslistEmbed: false,
      closePopup: true,
      showIcon: false,
      adblocker: false,
      DenyAllCta: true,
      AcceptAllCta: true,
      highPrivacy: true,
      alwaysNeedConsent: false,
      handleBrowserDNTRequest: false,
      removeCredit: true,
      moreInfoLink: true,
      useExternalCss: false,
      useExternalJs: false,
      mandatory: true,
      mandatoryCta: false,
      googleConsentMode: google,
      bingConsentMode: false,
      pianoConsentMode: false,
      piwikConsentMode: false,
      partnersList: false
    });

    tarteaucitron.job = tarteaucitron.job || [];
    tarteaucitron.job.push("inwardyoutube", "inwardavis");
    if (GA4_ID) {
      tarteaucitron.user.gtagUa = GA4_ID;
      tarteaucitron.user.gtagMore = function () {};
      tarteaucitron.job.push("gtag");
    } else if (GTM_ID) {
      tarteaucitron.user.googletagmanagerId = GTM_ID;
      tarteaucitron.job.push("googletagmanager");
    }

    /* Enlace "Gestion des cookies" del pie (y cualquier [data-cookies]). */
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("[data-cookies]");
      if (!a) return;
      e.preventDefault();
      window.inwardPanel();
    });
  });
})();
