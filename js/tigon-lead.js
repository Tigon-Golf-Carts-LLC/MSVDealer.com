/*
 * TIGON Webhook Flows lead forms for MSV DEALER (https://msvdealer.com).
 *
 * Loaded on every page. It:
 *   - renders the lead form into any <div data-tigon-form="..."> placeholder (the Contact page),
 *   - adds a "Get a Quote" pop-up (modal) with the same form, plus floating Call Now / Get a Quote buttons,
 *   - adds Call Now / Request a Quote buttons to dealer pages,
 *   - pre-fills brand / model / VIN / SKU when the page lists a specific cart (see LISTING PRE-FILL below),
 *   - validates, fills tracking fields and POSTs to this website's TIGON IOT webhook.
 *
 * This is a static site (GitHub Pages) with no server, so leads are posted straight from the browser.
 * The webhook only accepts browser posts from https://msvdealer.com. No signing secret belongs in this file.
 */
(function () {
  "use strict";

  var ENDPOINT = "https://tigoniot.com/hooks/hCVBsSRWnJYSXMUHJHatCSa8M7uyN6Qa";
  var FORM_NAME = "Contact form";
  var SITE_PHONE = "1-844-844-6638";
  var SITE_TEL = "+18448446638";
  var HONEYPOT = "website";
  var SUCCESS_TEXT = "Thank you! We received your message and will contact you shortly.";
  var ERROR_TEXT = "Sorry, something went wrong. Please try again or call us at " + SITE_PHONE + ".";
  var RATE_LIMIT_TEXT = "Too many tries. Please wait a minute and try again.";
  var MAX_FILE_MB = 10;
  var IMAGE_EXT = /\.(jpe?g|png|gif|webp|heic|heif)$/i;
  var TRACK = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "fbclid"];
  var HIDDEN = ["url", "referrer"].concat(TRACK, ["ga_client_id"]);
  var STORE_KEY = "tigon_first_touch";
  var MAX_AGE_MS = 30 * 24 * 60 * 60 * 1000;
  var BRANDS = ["TIGON", "Evolution", "ICON", "Club Car", "E-Z-GO", "Yamaha", "Other"];

  // ---------- tracking ----------

  // First-touch attribution: the first utm_*/gclid/fbclid seen are kept for 30 days.
  function firstTouch() {
    var current = {}, found = false, q = null;
    try { q = new URLSearchParams(window.location.search); } catch (e) { q = null; }
    TRACK.forEach(function (k) { var v = q && q.get(k); if (v) { current[k] = v; found = true; } });
    var saved = null;
    try { saved = JSON.parse(window.localStorage.getItem(STORE_KEY) || "null"); } catch (e) { saved = null; }
    if (saved && (!saved.ts || Date.now() - saved.ts > MAX_AGE_MS)) {
      saved = null;
      try { window.localStorage.removeItem(STORE_KEY); } catch (e) { /* storage blocked */ }
    }
    if (!saved && found) {
      saved = { ts: Date.now(), v: current };
      try { window.localStorage.setItem(STORE_KEY, JSON.stringify(saved)); } catch (e) { /* private mode */ }
    }
    var out = {};
    TRACK.forEach(function (k) { out[k] = (saved && saved.v && saved.v[k]) || current[k] || ""; });
    return out;
  }

  // Google Analytics client id from the _ga cookie: GA1.1.123456.789012 -> 123456.789012
  function gaClientId() {
    var m = document.cookie.match(/(?:^|;\s*)_ga=([^;]+)/);
    if (!m) return "";
    var parts = decodeURIComponent(m[1]).split(".");
    return parts.length >= 4 ? parts.slice(-2).join(".") : "";
  }

  function tracking() {
    var t = firstTouch();
    t.url = window.location.href;
    t.referrer = document.referrer || "";
    t.ga_client_id = gaClientId();
    return t;
  }

  function fillHidden(form) {
    var t = tracking();
    HIDDEN.forEach(function (k) {
      var el = form.querySelector('input[type="hidden"][name="' + k + '"]');
      if (el) el.value = t[k] || "";
    });
  }

  // ---------- page context ----------

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // LISTING PRE-FILL: a page that shows one specific cart marks it like
  //   <div data-tigon-listing data-brand="TIGON" data-model="Blaze 4" data-vin="1TGN..." data-sku="BLZ4-RED"></div>
  // Those values are pre-filled read-only in every form on the page.
  function listing() {
    var el = document.querySelector("[data-tigon-listing]");
    if (!el) return null;
    return {
      brand: el.getAttribute("data-brand") || "",
      model: el.getAttribute("data-model") || "",
      vin_number: el.getAttribute("data-vin") || "",
      sku_number: el.getAttribute("data-sku") || ""
    };
  }

  // Dealer pages: send which dealer page the lead came from as an extra field.
  function dealerName() {
    var h = document.querySelector(".dealer-header h1");
    return h ? h.textContent.trim() : "";
  }

  // ---------- form markup ----------

  function field(p, o) {
    var id = p + "-" + o.name;
    var req = o.required ? ' <span class="tgn-req" aria-hidden="true">*</span>' : "";
    var hint = o.hint ? ' <span class="tgn-hint">' + o.hint + "</span>" : "";
    var attrs = ' name="' + o.name + '" id="' + id + '" aria-describedby="' + id + '-err"' +
      (o.required ? " required" : "") + (o.auto ? ' autocomplete="' + o.auto + '"' : "") +
      (o.inputmode ? ' inputmode="' + o.inputmode + '"' : "") + (o.extra || "");
    var control;
    if (o.type === "textarea") control = '<textarea rows="4"' + attrs + (o.placeholder ? ' placeholder="' + o.placeholder + '"' : "") + "></textarea>";
    else if (o.type === "file") control = '<input type="file" accept="image/*,.heic,.heif"' + attrs + ">";
    else control = '<input type="' + o.type + '"' + attrs + ">";
    return '<div class="tgn-field' + (o.half ? " tgn-half" : "") + '">' +
      '<label for="' + id + '">' + o.label + req + hint + "</label>" + control +
      '<span class="tgn-err" id="' + id + '-err"></span></div>';
  }

  function formHTML(p, location) {
    var brandList = p + "-brands";
    var html = '<form class="tgn-form" id="' + p + '" data-tigon-lead method="post" action="' + ENDPOINT + '" enctype="multipart/form-data" novalidate>' +
      '<div class="tgn-grid">' +
      field(p, { name: "first_name", label: "First name", type: "text", auto: "given-name", required: true, half: true }) +
      field(p, { name: "last_name", label: "Last name", type: "text", auto: "family-name", required: true, half: true }) +
      field(p, { name: "email", label: "Email", type: "email", auto: "email", required: true, half: true }) +
      field(p, { name: "phone1", label: "Phone", type: "tel", auto: "tel", required: true, half: true }) +
      field(p, { name: "phone2", label: "Alternate phone", type: "tel", auto: "off", half: true, hint: "(optional)" }) +
      field(p, { name: "zip_code", label: "ZIP code", type: "text", auto: "postal-code", inputmode: "numeric", half: true }) +
      field(p, { name: "address", label: "Address", type: "text", auto: "street-address" }) +
      '<p class="tgn-legend">Vehicle you are interested in</p>' +
      field(p, { name: "brand", label: "Brand", type: "text", half: true, extra: ' list="' + brandList + '"' }) +
      field(p, { name: "model", label: "Model", type: "text", half: true }) +
      field(p, { name: "vin_number", label: "VIN", type: "text", half: true, hint: "(optional)" }) +
      field(p, { name: "sku_number", label: "Stock # / SKU", type: "text", half: true, hint: "(optional)" }) +
      field(p, { name: "comments", label: "Message", type: "textarea", placeholder: "How can we help?" }) +
      '<p class="tgn-legend">Photos <span class="tgn-hint">(optional, up to ' + MAX_FILE_MB + ' MB each: jpg, png, gif, webp or heic)</span></p>' +
      field(p, { name: "image_1", label: "Photo 1", type: "file" }) +
      field(p, { name: "image_2", label: "Photo 2", type: "file" }) +
      field(p, { name: "image_3", label: "Photo 3", type: "file" }) +
      "</div>" +
      '<datalist id="' + brandList + '">' + BRANDS.map(function (b) { return '<option value="' + esc(b) + '">'; }).join("") + "</datalist>" +
      '<div class="tgn-hp" aria-hidden="true"><label for="' + p + '-hp">Leave this field empty</label>' +
      '<input type="text" name="' + HONEYPOT + '" id="' + p + '-hp" tabindex="-1" autocomplete="off" value=""></div>' +
      '<input type="hidden" name="form_name" value="' + esc(FORM_NAME) + '">' +
      '<input type="hidden" name="form_location" value="' + esc(location) + '">' +
      HIDDEN.map(function (k) { return '<input type="hidden" name="' + k + '" value="">'; }).join("");
    var dealer = dealerName();
    if (dealer) html += '<input type="hidden" name="dealer" value="' + esc(dealer) + '">';
    html += '<button type="submit" class="tgn-submit">Send Message</button>' +
      '<p class="tigon-msg" role="status" aria-live="polite"></p></form>';
    return html;
  }

  function prefill(form) {
    var l = listing();
    if (!l) return;
    Object.keys(l).forEach(function (k) {
      var el = form.elements[k];
      if (el && l[k]) { el.value = l[k]; el.readOnly = true; }
    });
  }

  function setupForm(form) {
    fillHidden(form);
    prefill(form);
  }

  // ---------- validation ----------

  function setErr(form, name, text) {
    var el = form.elements[name];
    if (!el) return;
    var box = document.getElementById(el.id + "-err");
    if (box) box.textContent = text || "";
    el.classList.toggle("tgn-invalid", !!text);
    if (text) el.setAttribute("aria-invalid", "true"); else el.removeAttribute("aria-invalid");
  }

  function validate(form) {
    var first = null;
    function check(name, text) {
      setErr(form, name, text);
      if (text && !first) first = form.elements[name];
    }
    var v = function (n) { return (form.elements[n] && form.elements[n].value || "").trim(); };
    check("first_name", v("first_name") ? "" : "Please enter your first name.");
    check("last_name", v("last_name") ? "" : "Please enter your last name.");
    var email = v("email");
    check("email", !email ? "Please enter your email." :
      (/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) ? "" : "Please enter a valid email address, like name@example.com."));
    var phone = v("phone1");
    check("phone1", !phone ? "Please enter your phone number." :
      (phone.replace(/\D/g, "").length >= 10 ? "" : "Please enter a phone number with at least 10 digits."));
    var phone2 = v("phone2");
    check("phone2", !phone2 || phone2.replace(/\D/g, "").length >= 10 ? "" : "Please enter at least 10 digits, or leave this blank.");
    ["image_1", "image_2", "image_3"].forEach(function (n) {
      var input = form.elements[n], f = input && input.files && input.files[0], msg = "";
      if (f) {
        if (f.size > MAX_FILE_MB * 1024 * 1024) msg = "This photo is larger than " + MAX_FILE_MB + " MB. Please choose a smaller one.";
        else if (!/^image\//.test(f.type) && !IMAGE_EXT.test(f.name)) msg = "Please choose a jpg, png, gif, webp or heic photo.";
      }
      check(n, msg);
    });
    return first;
  }

  // ---------- sending ----------

  function show(form, text, ok) {
    var el = form.querySelector(".tigon-msg");
    el.textContent = text;
    el.className = "tigon-msg " + (ok ? "tgn-ok" : "tgn-bad");
  }

  function buildData(form) {
    fillHidden(form);
    var fd = new FormData(form);
    // Leave out empty file inputs so no blank images are sent.
    ["image_1", "image_2", "image_3"].forEach(function (n) {
      var input = form.elements[n];
      if (!input || !input.files || !input.files.length) fd.delete(n);
    });
    fd.set("form_name", FORM_NAME);
    fd.set(HONEYPOT, form.elements[HONEYPOT] ? form.elements[HONEYPOT].value : "");
    return fd;
  }

  function send(form) {
    var button = form.querySelector(".tgn-submit");
    var label = button.textContent;
    var bad = validate(form);
    if (bad) {
      show(form, "Please fix the highlighted fields.", false);
      bad.focus();
      return;
    }
    var fd = buildData(form);
    button.disabled = true;
    button.textContent = "Sending…";
    show(form, "Sending…", true);
    fetch(ENDPOINT, { method: "POST", body: fd, mode: "cors" })
      .then(function (res) {
        return res.text().then(function (body) {
          var data = null;
          try { data = JSON.parse(body); } catch (e) { data = null; }
          if (res.status === 429) throw new Error(RATE_LIMIT_TEXT);
          if (!res.ok || !data || data.ok !== true) throw new Error((data && (data.error || data.message)) || ERROR_TEXT);
        });
      })
      .then(function () {
        form.reset();
        setupForm(form);
        show(form, SUCCESS_TEXT, true);
        if (typeof window.gtag === "function") window.gtag("event", "generate_lead", { form_name: FORM_NAME });
      })
      .catch(function (err) {
        show(form, (err && err.message && err.message !== "Failed to fetch") ? err.message : ERROR_TEXT, false);
      })
      .then(function () {
        button.disabled = false;
        button.textContent = label;
      });
  }

  // ---------- Call Now / Get a Quote buttons and modal ----------

  function callLink(cls) {
    return '<a class="tgn-btn tgn-btn-call' + (cls ? " " + cls : "") + '" href="tel:' + SITE_TEL + '" aria-label="Call now ' + SITE_PHONE + '">&#9742; Call Now</a>';
  }

  var modal = null, lastFocus = null;

  function buildModal() {
    modal = document.createElement("div");
    modal.className = "tgn-modal";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-labelledby", "tgn-modal-title");
    modal.innerHTML = '<div class="tgn-modal-box">' +
      '<button type="button" class="tgn-modal-close" aria-label="Close">&times;</button>' +
      '<h2 id="tgn-modal-title">Get a Quote</h2>' +
      "<p>Tell us what you are looking for and an MSV specialist will contact you shortly. Prefer to talk? Call " +
      '<a href="tel:' + SITE_TEL + '">' + SITE_PHONE + "</a>.</p>" +
      formHTML("tigon-form-modal", "Pop-up form") + "</div>";
    document.body.appendChild(modal);
    setupForm(modal.querySelector("form"));
    modal.querySelector(".tgn-modal-close").addEventListener("click", closeModal);
    modal.addEventListener("click", function (e) { if (e.target === modal) closeModal(); });
  }

  function openLead(e) {
    if (e) e.preventDefault();
    var inline = document.querySelector("[data-tigon-form] form");
    if (inline) {
      inline.scrollIntoView({ behavior: "smooth", block: "start" });
      inline.elements.first_name.focus({ preventScroll: true });
      return;
    }
    if (!modal) buildModal();
    lastFocus = document.activeElement;
    fillHidden(modal.querySelector("form"));
    modal.classList.add("tgn-open");
    document.body.classList.add("tgn-lock");
    modal.querySelector('[name="first_name"]').focus();
  }

  function closeModal() {
    if (!modal) return;
    modal.classList.remove("tgn-open");
    document.body.classList.remove("tgn-lock");
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  document.addEventListener("keydown", function (e) {
    if (!modal || !modal.classList.contains("tgn-open")) return;
    if (e.key === "Escape") { closeModal(); return; }
    if (e.key !== "Tab") return;
    // Keep keyboard focus inside the open pop-up.
    var items = modal.querySelectorAll('button, [href], input:not([type="hidden"]):not([tabindex="-1"]), select, textarea');
    var firstEl = items[0], lastEl = items[items.length - 1];
    if (e.shiftKey && document.activeElement === firstEl) { e.preventDefault(); lastEl.focus(); }
    else if (!e.shiftKey && document.activeElement === lastEl) { e.preventDefault(); firstEl.focus(); }
  });

  // Any element with data-tigon-open (or a link to #quote) opens the form.
  document.addEventListener("click", function (e) {
    var t = e.target.closest && e.target.closest('[data-tigon-open], a[href="#quote"]');
    if (t) openLead(e);
  });

  // Capture phase: runs before any other submit handlers.
  document.addEventListener("submit", function (e) {
    var form = e.target;
    if (!form || !form.hasAttribute("data-tigon-lead")) return;
    e.preventDefault();
    e.stopImmediatePropagation();
    send(form);
  }, true);

  function init() {
    // Inline forms (Contact page).
    var slots = document.querySelectorAll("[data-tigon-form]");
    for (var i = 0; i < slots.length; i++) {
      slots[i].innerHTML = formHTML("tigon-form-" + (i ? "inline-" + i : "contact"), slots[i].getAttribute("data-tigon-form") || "Contact page");
      setupForm(slots[i].querySelector("form"));
    }

    // Dealer pages: Call Now + Request a Quote under the dealer name.
    var header = document.querySelector(".dealer-header");
    if (header && !header.querySelector(".tgn-cta-row")) {
      var row = document.createElement("div");
      row.className = "tgn-cta-row";
      row.innerHTML = callLink() + '<button type="button" class="tgn-btn tgn-btn-quote" data-tigon-open>Request a Quote</button>';
      header.appendChild(row);
    }

    // Floating Call Now / Get a Quote on every page.
    if (!document.querySelector(".tgn-float")) {
      var fl = document.createElement("div");
      fl.className = "tgn-float";
      fl.innerHTML = '<button type="button" class="tgn-btn tgn-btn-quote" data-tigon-open>Get a Quote</button>' + callLink();
      document.body.appendChild(fl);
    }

    if (/(?:^|[#&])quote(?:$|&)/.test(window.location.hash.slice(1))) openLead();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
