/* Innovahub — sitio web (beta)
   Interacciones descritas en las anotaciones del wireframe:
   header compacto, menú móvil, contadores, timeline, acordeones,
   filtros del portafolio, formulario de contacto y ciclo orbital. */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduceMotion) document.documentElement.classList.add("js");

  /* ------------------------------------------------------------------
     Íconos sólidos (manual de marca: formas rellenas, sin trazos)
     ------------------------------------------------------------------ */
  var ICONS = {
    formacion: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1h-6l1 2h2v1H7v-1h2l1-2H4a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm6 3v6l5-3-5-3z"/></svg>',
    diagnostico: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 4a6 6 0 1 1 0 12 6 6 0 0 1 0-12zm0 3.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5z"/></svg>',
    sistematizacion: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 2 8l10 5 10-5-10-5zm-8 8.5-2 1 10 5 10-5-2-1-8 4-8-4zm0 4-2 1 10 5 10-5-2-1-8 4-8-4z"/></svg>',
    produccion: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h11a2 2 0 0 1 2 2v1.5l4-2.5v10l-4-2.5V16a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2zm2 3a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z"/></svg>',
    plataformas: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4h18a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1h-7v2h3v2H7v-2h3v-2H3a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1zm3 3v2h12V7H6zm0 4v2h8v-2H6z"/></svg>',
    escala: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a5 5 0 1 1 0 10 5 5 0 0 1 0-10zm-7 9a3 3 0 1 1 0 6 3 3 0 0 1 0-6zm14 0a3 3 0 1 1 0 6 3 3 0 0 1 0-6zM12 13c3.3 0 6 1.6 6 4v3H6v-3c0-2.4 2.7-4 6-4z"/></svg>',
    orden: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4h8v7H3V4zm10 0h8v4h-8V4zm0 6h8v10h-8V10zM3 13h8v7H3v-7z"/></svg>',
    medir: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 20h18v2H3v-2zM4 18V10h4v8H4zm6 0V4h4v14h-4zm6 0v-6h4v6h-4z"/></svg>',
    personas: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a4 4 0 1 1 0 8 4 4 0 0 1 0-8zm0 10c4.4 0 8 2.2 8 5v3H4v-3c0-2.8 3.6-5 8-5z"/></svg>',
    evidencia: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3h10l4 4v14H5V3zm2 8v2h10v-2H7zm0 4v2h7v-2H7z"/></svg>',
    acceso: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 3.5a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3zM9 9h6v2h-2v7h-2v-7H9V9z"/></svg>',
    abierto: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2 4 6v6c0 5 3.4 9 8 10 4.6-1 8-5 8-10V6l-8-4zm-1 13-3-3 1.4-1.4L11 12.2l4.6-4.6L17 9l-6 6z"/></svg>',
    retorno: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm1 5v1.3c1.7.3 3 1.3 3 3h-2c0-.8-.8-1.3-2-1.3s-2 .4-2 1c0 .7.9 1 2.3 1.3C14.6 12.7 16 13.4 16 15.2c0 1.6-1.2 2.6-3 2.9V19h-2v-1c-1.8-.3-3-1.4-3-3.2h2c0 .9.9 1.4 2 1.4 1.3 0 2-.5 2-1.1 0-.8-.9-1.1-2.4-1.5C9.6 13.2 8 12.6 8 10.8 8 9.3 9.2 8.4 11 8.1V7h2z"/></svg>',
    productividad: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 17l6-6 4 4 8-8v4h2V4h-7v2h4l-7 7-4-4-7 7 1 1z"/></svg>',
    costos: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4h16v12H4V4zm2 2v8h12V6H6zm4 2h4v4h-4V8zM2 18h20v2H2v-2z"/></svg>',
    efectividad: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 4a6 6 0 1 1 0 12 6 6 0 0 1 0-12zm0 3a3 3 0 1 0 0 6 3 3 0 0 0 0-6z"/></svg>',
    flexibilidad: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm-1 5h2v5.6l3.5 2-1 1.7L11 13.4V7z"/></svg>',
    repositorio: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5a2 2 0 0 1 2-2h5l2 2h7a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5zm4 6v2h10v-2H7z"/></svg>',
    campus: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 1 8l11 5 9-4.1V15h2V8L12 3zM5 12.6V16c0 1.8 3.1 3.5 7 3.5s7-1.7 7-3.5v-3.4l-7 3.2-7-3.2z"/></svg>',
    brochure: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 2h9l5 5v15H6V2zm7 1.5V8h4.5L13 3.5zM8 11v2h8v-2H8zm0 4v2h8v-2H8z"/></svg>',
    linkedin: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.98 3.5A2.5 2.5 0 1 1 5 8.5a2.5 2.5 0 0 1-.02-5zM3 9h4v12H3V9zm7 0h3.8v1.7h.1c.5-1 1.8-2 3.7-2 4 0 4.7 2.6 4.7 6V21h-4v-5.5c0-1.3 0-3-1.8-3s-2.1 1.4-2.1 2.9V21h-4V9z"/></svg>',
    youtube: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M23 7.2c-.3-1-1-1.8-2-2C19.2 4.7 12 4.7 12 4.7s-7.2 0-9 .5c-1 .2-1.7 1-2 2C.5 9 .5 12 .5 12s0 3 .5 4.8c.3 1 1 1.8 2 2 1.8.5 9 .5 9 .5s7.2 0 9-.5c1-.2 1.7-1 2-2 .5-1.8.5-4.8.5-4.8s0-3-.5-4.8zM9.8 15.1V8.9L15.7 12l-5.9 3.1z"/></svg>',
    instagram: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7.5 2h9A5.5 5.5 0 0 1 22 7.5v9a5.5 5.5 0 0 1-5.5 5.5h-9A5.5 5.5 0 0 1 2 16.5v-9A5.5 5.5 0 0 1 7.5 2zm0 2A3.5 3.5 0 0 0 4 7.5v9A3.5 3.5 0 0 0 7.5 20h9a3.5 3.5 0 0 0 3.5-3.5v-9A3.5 3.5 0 0 0 16.5 4h-9zM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10zm0 2a3 3 0 1 0 0 6 3 3 0 0 0 0-6zm5.3-3.3a1.2 1.2 0 1 1 0 2.4 1.2 1.2 0 0 1 0-2.4z"/></svg>',
    whatsapp: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5.1-1.3A10 10 0 1 0 12 2zm0 2a8 8 0 1 1-4.1 14.9l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 0 1 12 4zm-3.3 4.2c-.2 0-.5 0-.7.3-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 4.9 4.3 2.4.9 2.9.8 3.4.7.5 0 1.7-.7 1.9-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3l-2-.9c-.3-.1-.5-.2-.7.1l-.9 1.1c-.2.2-.3.2-.6.1-.3-.2-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.5-.5.3-.5c.1-.2 0-.4 0-.5L9.5 8.6c-.2-.4-.4-.4-.5-.4h-.3z"/></svg>'
  };

  document.querySelectorAll("[data-icon]").forEach(function (el) {
    var name = el.getAttribute("data-icon");
    if (ICONS[name]) el.innerHTML = ICONS[name];
  });

  /* ------------------------------------------------------------------
     Header: compactar al scroll, menú desplegable y menú móvil
     ------------------------------------------------------------------ */
  var header = document.querySelector(".header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 24);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  document.querySelectorAll(".nav__item--menu").forEach(function (item) {
    var trigger = item.querySelector(".nav__link");
    var timer = null;
    var open = function () { clearTimeout(timer); item.classList.add("is-open"); trigger.setAttribute("aria-expanded", "true"); };
    var close = function () { clearTimeout(timer); item.classList.remove("is-open"); trigger.setAttribute("aria-expanded", "false"); };
    trigger.addEventListener("click", function (e) {
      e.preventDefault();
      if (item.classList.contains("is-open")) close(); else open();
    });
    item.addEventListener("mouseenter", open);
    /* Pequeño retardo: si el puntero vuelve al ítem antes de 200 ms, el menú sigue abierto */
    item.addEventListener("mouseleave", function () { timer = setTimeout(close, 200); });
    item.addEventListener("focusout", function (e) { if (!item.contains(e.relatedTarget)) close(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
    document.addEventListener("click", function (e) { if (!item.contains(e.target)) close(); });
  });

  var burger = document.querySelector(".burger");
  var navMovil = document.querySelector(".nav-movil");
  if (burger && navMovil) {
    burger.addEventListener("click", function () {
      var open = navMovil.classList.toggle("is-open");
      burger.setAttribute("aria-expanded", String(open));
      burger.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
    });
  }

  /* ------------------------------------------------------------------
     Revelado al entrar en viewport
     ------------------------------------------------------------------ */
  var io = ("IntersectionObserver" in window) ? new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      el.classList.add("is-visible");
      if (el.hasAttribute("data-count")) animateCount(el);
      if (el.classList.contains("pasos")) activateSteps(el);
      io.unobserve(el);
    });
  }, { threshold: 0.25 }) : null;

  function observe(sel) {
    document.querySelectorAll(sel).forEach(function (el) {
      if (io) io.observe(el); else { el.classList.add("is-visible"); if (el.hasAttribute("data-count")) animateCount(el); if (el.classList.contains("pasos")) activateSteps(el); }
    });
  }

  /* Contadores de cifras */
  function formatNum(n) {
    return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  }
  function animateCount(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var prefix = el.getAttribute("data-prefix") || "";
    var suffix = el.getAttribute("data-suffix") || "";
    if (reduceMotion || isNaN(target)) { el.textContent = prefix + formatNum(target) + suffix; return; }
    var dur = 1400, start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = prefix + formatNum(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* Timeline: se ilumina paso a paso */
  function activateSteps(container) {
    var steps = container.querySelectorAll(".paso");
    steps.forEach(function (s, i) {
      setTimeout(function () { s.classList.add("is-active"); }, reduceMotion ? 0 : 220 * i);
    });
  }

  observe(".reveal, [data-count], .pasos");

  /* Red de seguridad: si el observador no dispara (impresión, navegadores
     antiguos, capturas), todo queda visible a los 2,5 s. */
  setTimeout(function () {
    document.querySelectorAll(".reveal:not(.is-visible)").forEach(function (el) { el.classList.add("is-visible"); });
  }, 2500);

  /* ------------------------------------------------------------------
     Acordeones
     ------------------------------------------------------------------ */
  document.querySelectorAll(".acordeon").forEach(function (acc) {
    var items = acc.querySelectorAll(".acordeon__item");
    items.forEach(function (item, i) {
      var btn = item.querySelector(".acordeon__boton");
      var panel = item.querySelector(".acordeon__panel");
      var icon = item.querySelector(".acordeon__icono");
      if (!btn || !panel) return;
      var id = panel.id || ("acc-" + Math.random().toString(36).slice(2, 8));
      panel.id = id;
      btn.setAttribute("aria-controls", id);
      var set = function (open) {
        item.classList.toggle("is-open", open);
        btn.setAttribute("aria-expanded", String(open));
        panel.hidden = !open;
        if (icon) icon.textContent = open ? "−" : "+";
      };
      set(item.classList.contains("is-open") || (i === 0 && acc.hasAttribute("data-open-first")));
      btn.addEventListener("click", function () { set(panel.hidden); });
    });
  });

  /* ------------------------------------------------------------------
     Carrusel móvil de casos (puntos)
     ------------------------------------------------------------------ */
  document.querySelectorAll(".casos-carrusel").forEach(function (car) {
    var track = car.querySelector(".casos-carrusel__pista");
    var dots = car.querySelectorAll(".puntos button");
    if (!track || !dots.length) return;
    var cards = track.querySelectorAll(".caso-card");
    dots.forEach(function (d, i) {
      d.addEventListener("click", function () {
        if (cards[i]) track.scrollTo({ left: cards[i].offsetLeft - track.offsetLeft, behavior: reduceMotion ? "auto" : "smooth" });
      });
    });
    track.addEventListener("scroll", function () {
      var idx = Math.round(track.scrollLeft / (cards[0].offsetWidth + 16));
      dots.forEach(function (d, i) { d.classList.toggle("is-active", i === idx); });
    }, { passive: true });
  });

  /* Testimonios: puntos que alternan citas */
  document.querySelectorAll("[data-testimonios]").forEach(function (box) {
    var citas = JSON.parse(box.getAttribute("data-testimonios"));
    var cita = box.querySelector(".testimonio__cita");
    var nombre = box.querySelector(".testimonio__autor strong");
    var cargo = box.querySelector(".testimonio__autor span");
    var dots = box.querySelectorAll(".puntos button");
    dots.forEach(function (d, i) {
      d.addEventListener("click", function () {
        cita.textContent = citas[i].cita; nombre.textContent = citas[i].nombre; cargo.textContent = citas[i].cargo;
        dots.forEach(function (x, j) { x.classList.toggle("is-active", i === j); });
      });
    });
  });

  /* ------------------------------------------------------------------
     Portafolio filtrable
     ------------------------------------------------------------------ */
  var portafolio = document.querySelector("[data-portafolio]");
  if (portafolio) {
    var grid = portafolio.querySelector(".casos-grid");
    var cards = Array.prototype.slice.call(grid.querySelectorAll(".caso-card"));
    var vacio = portafolio.querySelector(".estado-vacio");
    var contador = portafolio.querySelector("[data-contador]");
    var chipsLinea = portafolio.querySelectorAll('[data-filtro="linea"] .chip--filtro');
    var chipsSector = portafolio.querySelectorAll('[data-filtro="sector"] .chip--filtro');
    var selectsPais = portafolio.querySelectorAll('[data-filtro="pais"]');
    var buscador = portafolio.querySelector("[data-buscador]");
    var chipsActivos = portafolio.querySelector(".chips-activos");
    var contadorMovil = portafolio.querySelector("[data-contador-movil]");
    var btnFiltrar = portafolio.querySelector("[data-abrir-filtros]");
    var hoja = portafolio.querySelector(".hoja");
    var estado = { linea: "todas", sector: "todos", pais: "todos", q: "" };
    var LABELS = { linea: {}, sector: {} };
    chipsLinea.forEach(function (c) { LABELS.linea[c.getAttribute("data-valor")] = c.textContent.trim(); });
    chipsSector.forEach(function (c) { LABELS.sector[c.getAttribute("data-valor")] = c.textContent.trim(); });

    function aplicar() {
      grid.classList.add("is-loading");
      var q = estado.q.trim().toLowerCase();
      var visibles = 0;
      cards.forEach(function (card) {
        var lineas = (card.getAttribute("data-lineas") || "").split(" ");
        var sector = card.getAttribute("data-sector");
        var pais = card.getAttribute("data-pais");
        var texto = card.textContent.toLowerCase();
        var ok = (estado.linea === "todas" || lineas.indexOf(estado.linea) !== -1) &&
                 (estado.sector === "todos" || sector === estado.sector) &&
                 (estado.pais === "todos" || pais === estado.pais) &&
                 (!q || texto.indexOf(q) !== -1);
        card.hidden = !ok;
        if (ok) visibles++;
      });
      var txt = visibles === 1 ? "1 proyecto" : visibles + " proyectos";
      if (contador) contador.textContent = txt;
      if (contadorMovil) contadorMovil.textContent = txt;
      if (vacio) vacio.hidden = visibles !== 0;
      grid.hidden = visibles === 0;
      chipsLinea.forEach(function (c) { c.setAttribute("aria-pressed", String(c.getAttribute("data-valor") === estado.linea)); });
      chipsSector.forEach(function (c) { c.setAttribute("aria-pressed", String(c.getAttribute("data-valor") === estado.sector)); });
      renderActivos();
      var n = (estado.linea !== "todas") + (estado.sector !== "todos") + (estado.pais !== "todos");
      if (btnFiltrar) btnFiltrar.textContent = n ? "Filtrar (" + n + ")" : "Filtrar";
      setTimeout(function () { grid.classList.remove("is-loading"); }, reduceMotion ? 0 : 180);
    }

    function renderActivos() {
      if (!chipsActivos) return;
      chipsActivos.innerHTML = "";
      var items = [];
      if (estado.linea !== "todas") items.push({ k: "linea", v: "todas", t: LABELS.linea[estado.linea], cls: "chip--" + estado.linea });
      if (estado.sector !== "todos") items.push({ k: "sector", v: "todos", t: LABELS.sector[estado.sector] });
      if (estado.pais !== "todos") items.push({ k: "pais", v: "todos", t: estado.pais });
      items.forEach(function (it) {
        var b = document.createElement("button");
        b.type = "button"; b.className = "chip " + (it.cls || "");
        b.textContent = it.t + " ×"; b.setAttribute("aria-label", "Quitar filtro " + it.t);
        b.addEventListener("click", function () { estado[it.k] = it.v; if (it.k === "pais") selectsPais.forEach(function (s) { s.value = "todos"; }); aplicar(); });
        chipsActivos.appendChild(b);
      });
    }

    chipsLinea.forEach(function (c) { c.addEventListener("click", function () { estado.linea = c.getAttribute("data-valor"); aplicar(); }); });
    chipsSector.forEach(function (c) { c.addEventListener("click", function () { estado.sector = c.getAttribute("data-valor"); aplicar(); }); });
    selectsPais.forEach(function (s) {
      s.addEventListener("change", function () {
        estado.pais = s.value;
        selectsPais.forEach(function (o) { o.value = s.value; });
        aplicar();
      });
    });
    if (buscador) buscador.addEventListener("input", function () { estado.q = buscador.value; aplicar(); });

    portafolio.querySelectorAll("[data-limpiar]").forEach(function (b) {
      b.addEventListener("click", function () {
        estado = { linea: "todas", sector: "todos", pais: "todos", q: "" };
        selectsPais.forEach(function (s) { s.value = "todos"; });
        if (buscador) buscador.value = "";
        aplicar();
      });
    });

    /* Hoja inferior en móvil */
    if (btnFiltrar && hoja) {
      var abrir = function () { hoja.classList.add("is-open"); document.body.style.overflow = "hidden"; hoja.querySelector(".hoja__cerrar").focus(); };
      var cerrar = function () { hoja.classList.remove("is-open"); document.body.style.overflow = ""; btnFiltrar.focus(); };
      btnFiltrar.addEventListener("click", abrir);
      hoja.querySelectorAll("[data-cerrar-hoja]").forEach(function (b) { b.addEventListener("click", cerrar); });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape" && hoja.classList.contains("is-open")) cerrar(); });
    }

    /* Entrada por audiencia desde el home: ?sector=... */
    var params = new URLSearchParams(window.location.search);
    if (params.get("sector")) estado.sector = params.get("sector");
    if (params.get("linea")) estado.linea = params.get("linea");
    aplicar();
  }

  /* ------------------------------------------------------------------
     Formulario de contacto (validación en cliente; sin backend aún)
     ------------------------------------------------------------------ */
  var form = document.querySelector("[data-form-contacto]");
  if (form) {
    var ok = form.parentNode.querySelector(".aviso--ok");
    var err = form.parentNode.querySelector(".aviso--error");
    var campos = form.querySelectorAll("[required]");
    var etiquetas = { nombre: "el nombre", organizacion: "la organización", correo: "el correo", pais: "el país", linea: "la línea de servicio", mensaje: "el mensaje", datos: "la autorización de datos" };

    function validar(campo) {
      var wrap = campo.closest(".campo");
      var valido = campo.type === "checkbox" ? campo.checked : campo.value.trim() !== "";
      if (valido && campo.type === "email") valido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(campo.value.trim());
      if (wrap) wrap.classList.toggle("is-error", !valido);
      campo.setAttribute("aria-invalid", String(!valido));
      return valido;
    }
    campos.forEach(function (c) {
      c.addEventListener("blur", function () { validar(c); });
      c.addEventListener("input", function () { if (c.closest(".campo").classList.contains("is-error")) validar(c); });
    });
    var sel = form.querySelector("select");
    if (sel) { var syncSel = function () { sel.classList.toggle("is-placeholder", sel.value === ""); }; sel.addEventListener("change", syncSel); syncSel(); }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var faltan = [];
      campos.forEach(function (c) { if (!validar(c)) faltan.push(etiquetas[c.name] || c.name); });
      if (faltan.length) {
        ok.hidden = true; err.hidden = false;
        err.querySelector("span").textContent = faltan.length === 1 ? "Falta " + faltan[0] + "." : "Faltan " + faltan.slice(0, -1).join(", ") + " y " + faltan[faltan.length - 1] + ".";
        form.querySelector(".is-error input, .is-error select, .is-error textarea").focus();
        return;
      }
      err.hidden = true; ok.hidden = false;
      form.reset(); if (sel) sel.classList.add("is-placeholder");
      ok.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "nearest" });
    });
  }

  /* ------------------------------------------------------------------
     Ciclo orbital: hover en nodo resalta la fila de la tabla
     ------------------------------------------------------------------ */
  var orbital = document.querySelector(".orbital");
  if (orbital) {
    var nodos = orbital.querySelectorAll(".orbital__nodo");
    var filas = document.querySelectorAll(".tabla-pasos__fila");
    var setActivo = function (n) {
      nodos.forEach(function (x) { x.classList.toggle("is-active", x.getAttribute("data-paso") === n); });
      filas.forEach(function (f) { f.classList.toggle("is-active", f.getAttribute("data-paso") === n); });
    };
    nodos.forEach(function (nodo) {
      var n = nodo.getAttribute("data-paso");
      nodo.addEventListener("mouseenter", function () { setActivo(n); });
      nodo.addEventListener("focus", function () { setActivo(n); });
      nodo.addEventListener("mouseleave", function () { setActivo(null); });
      nodo.addEventListener("blur", function () { setActivo(null); });
      nodo.addEventListener("click", function () {
        var fila = document.querySelector('.tabla-pasos__fila[data-paso="' + n + '"]');
        if (fila) fila.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
        setActivo(n);
      });
    });
  }

  /* Año en el pie */
  document.querySelectorAll("[data-anio]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
