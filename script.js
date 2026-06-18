(function () {
  "use strict";

  /* Header shadow on scroll */
  var header = document.getElementById("header");
  function onScroll() {
    if (window.scrollY > 10) header.classList.add("is-scrolled");
    else header.classList.remove("is-scrolled");
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* Mobile menu */
  var burger = document.getElementById("burger");
  var nav = document.getElementById("nav");
  function closeMenu() {
    nav.classList.remove("is-open");
    burger.classList.remove("is-open");
    burger.setAttribute("aria-expanded", "false");
  }
  burger.addEventListener("click", function () {
    var open = nav.classList.toggle("is-open");
    burger.classList.toggle("is-open", open);
    burger.setAttribute("aria-expanded", String(open));
  });
  nav.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", closeMenu);
  });

  /* Reveal on scroll */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* Current year */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* Form validation (demo — no backend) */
  var form = document.getElementById("signupForm");
  if (form) {
    var status = document.getElementById("formStatus");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      status.className = "form__status";
      status.textContent = "";

      var name = form.elements.name;
      var contact = form.elements.contact;
      var valid = true;

      [name, contact].forEach(function (field) {
        if (!field.value.trim()) {
          field.classList.add("invalid");
          valid = false;
        } else {
          field.classList.remove("invalid");
        }
      });

      if (!valid) {
        status.classList.add("err");
        status.textContent = "Пожалуйста, заполните имя и контакт для связи.";
        return;
      }

      status.classList.add("ok");
      status.textContent = "Спасибо! Заявка принята — я свяжусь с вами в ближайшее время.";
      form.reset();
    });

    form.querySelectorAll("input, textarea").forEach(function (field) {
      field.addEventListener("input", function () { field.classList.remove("invalid"); });
    });
  }
})();
