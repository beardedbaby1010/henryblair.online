/* Click any figure to see it full size.
   Works for <img> figures and for the inline-SVG derivation diagrams, which
   are drawn at build time and have no file to open. Self-contained: it brings
   its own styles so it can run on every page shell the site uses.
   No dependencies, no network, nothing stored. */
(function () {
  "use strict";
  if (window.__figzoom) return;
  window.__figzoom = 1;

  var CSS =
    '.fz-able{cursor:zoom-in}' +
    '.fz-able:focus-visible{outline:2px solid #1B6FC4;outline-offset:3px}' +
    '.fz-hint{position:absolute;top:8px;right:8px;z-index:2;display:none;' +
      'padding:3px 8px;border-radius:4px;font:600 11px/1.4 ui-sans-serif,-apple-system,' +
      '"Segoe UI",Helvetica,Arial,sans-serif;letter-spacing:.04em;text-transform:uppercase;' +
      'background:rgba(9,30,72,.86);color:#fff;pointer-events:none}' +
    '.fz-wrap{position:relative}' +
    '.fz-wrap:hover .fz-hint,.fz-able:focus-visible+.fz-hint{display:block}' +
    '.fz-ov{position:fixed;inset:0;z-index:9999;display:flex;flex-direction:column;' +
      'align-items:center;justify-content:center;gap:10px;padding:26px 26px 18px;' +
      'background:rgba(9,21,40,.93);opacity:0;transition:opacity .14s ease}' +
    '.fz-ov.on{opacity:1}' +
    '.fz-stage{max-width:100%;max-height:calc(100vh - 118px);overflow:auto;' +
      'background:#fff;border-radius:6px;box-shadow:0 18px 60px rgba(0,0,0,.5)}' +
    '.fz-stage>img{display:block;max-width:100%;height:auto}' +
    '.fz-stage>svg{display:block;width:min(96vw,1700px);height:auto}' +
    '.fz-cap{max-width:min(96vw,1100px);color:#e8eef6;font:400 13px/1.5 ui-sans-serif,' +
      '-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;text-align:center}' +
    '.fz-cap b{color:#fff}' +
    '.fz-x{position:fixed;top:14px;right:18px;width:38px;height:38px;border:0;border-radius:6px;' +
      'background:rgba(255,255,255,.12);color:#fff;font:400 22px/1 system-ui;cursor:pointer}' +
    '.fz-x:hover{background:rgba(255,255,255,.22)}' +
    '.fz-open{overflow:hidden}' +
    '@media(max-width:600px){.fz-stage{max-height:calc(100vh - 150px)}}';

  var st = document.createElement("style");
  st.textContent = CSS;
  document.head.appendChild(st);

  var ov, stage, cap, lastFocus;

  function close() {
    if (!ov) return;
    ov.classList.remove("on");
    document.documentElement.classList.remove("fz-open");
    var o = ov; ov = null;
    setTimeout(function () { if (o && o.parentNode) o.parentNode.removeChild(o); }, 160);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  function open(node, caption) {
    close();
    lastFocus = document.activeElement;
    ov = document.createElement("div");
    ov.className = "fz-ov";
    ov.setAttribute("role", "dialog");
    ov.setAttribute("aria-modal", "true");
    ov.setAttribute("aria-label", "Figure, full size");

    stage = document.createElement("div");
    stage.className = "fz-stage";
    stage.appendChild(node);

    cap = document.createElement("div");
    cap.className = "fz-cap";
    cap.innerHTML = caption || "";

    var x = document.createElement("button");
    x.className = "fz-x";
    x.setAttribute("aria-label", "Close");
    x.innerHTML = "&times;";
    x.addEventListener("click", close);

    ov.appendChild(stage);
    if (caption) ov.appendChild(cap);
    ov.appendChild(x);
    ov.addEventListener("click", function (e) {
      if (e.target === ov) close();
    });
    document.body.appendChild(ov);
    document.documentElement.classList.add("fz-open");
    requestAnimationFrame(function () { ov.classList.add("on"); });
    x.focus();
  }

  document.addEventListener("keydown", function (e) {
    if (ov && (e.key === "Escape" || e.key === "Esc")) { e.preventDefault(); close(); }
  });

  function captionFor(el) {
    var fig = el.closest("figure");
    var fc = fig && fig.querySelector("figcaption");
    if (fc) return fc.innerHTML;
    var sib = el.parentNode && el.parentNode.nextElementSibling;
    if (sib && sib.classList && sib.classList.contains("tblnote")) return sib.innerHTML;
    return el.getAttribute("alt") || "";
  }

  function enable(el, make) {
    if (el.classList.contains("fz-able")) return;
    el.classList.add("fz-able");
    el.setAttribute("tabindex", "0");
    el.setAttribute("role", "button");
    if (!el.getAttribute("aria-label"))
      el.setAttribute("aria-label", "Expand this figure");

    var host = el.parentNode;
    if (host && !host.classList.contains("fz-wrap") &&
        getComputedStyle(host).position === "static") {
      host.classList.add("fz-wrap");
      var hint = document.createElement("span");
      hint.className = "fz-hint";
      hint.textContent = "Click to expand";
      host.appendChild(hint);
    }

    function go(e) { e.preventDefault(); open(make(), captionFor(el)); }
    el.addEventListener("click", go);
    el.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") go(e);
    });
  }

  function scan() {
    document.querySelectorAll('figure img, .figs img, img.zoom, img[src^="figures/"]').forEach(function (im) {
      enable(im, function () {
        var c = document.createElement("img");
        c.src = im.currentSrc || im.src;
        c.alt = im.alt || "";
        return c;
      });
    });
    document.querySelectorAll("figure svg, .diagramwrap svg, svg.pcafig").forEach(function (sv) {
      enable(sv, function () {
        var c = sv.cloneNode(true);
        c.removeAttribute("style");
        c.classList.remove("fz-able");
        c.removeAttribute("tabindex");
        c.removeAttribute("role");
        return c;
      });
    });
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", scan);
  else scan();
  // the live scripts rewrite numbers inside the SVGs after their fetch returns
  window.addEventListener("load", scan);
})();
