document.addEventListener('DOMContentLoaded', function () {
  // =================
  // MOBILE MENU FUNCTIONALITY
  // =================
  let isMobileMenuInitialized = false;

  function initializeMobileMenu() {
    if (isMobileMenuInitialized) {
      console.warn('initializeMobileMenu() zaten çalıştırıldı. Tekrar çalıştırılması engellendi.');
      return;
    }

    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobile-menu');

    if (!hamburger || !mobileMenu) {
      console.error('HATA: Hamburger veya Mobil Menü elementi bulunamadı!');
      return;
    }

    const hamburgerIcon = hamburger.querySelector('i');
    let isProcessingClick = false;

    hamburger.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();

      if (isProcessingClick) {
        return;
      }
      isProcessingClick = true;

      console.log('Hamburger clicked');

      const isActive = mobileMenu.classList.toggle('active');
      hamburger.classList.toggle('active');
      document.body.style.overflow = isActive ? 'hidden' : '';

      // Icon değiştirme
      if (hamburgerIcon) {
        hamburgerIcon.className = isActive ? 'fas fa-xmark' : 'fas fa-bars';
      }

      console.log('Menü durumu değiştirildi. Yeni durum:', isActive ? 'Açık' : 'Kapalı');

      setTimeout(() => {
        isProcessingClick = false;
      }, 200);
    });

    // Menü dışına tıklandığında kapatma
    document.addEventListener('click', function (e) {
      if (
        mobileMenu.classList.contains('active') &&
        !mobileMenu.contains(e.target) &&
        !hamburger.contains(e.target)
      ) {
        mobileMenu.classList.remove('active');
        hamburger.classList.remove('active');
        document.body.style.overflow = '';

        if (hamburgerIcon) {
          hamburgerIcon.className = 'fas fa-bars';
        }
      }
    });

    isMobileMenuInitialized = true;
    console.log('✅ Mobile Menu başarıyla yüklendi ve olay dinleyicileri eklendi.');
  }

  // =================
  // MOBILE DROPDOWN FUNCTIONALITY
  // =================
  const mobileDropdowns = document.querySelectorAll('.mobile-dropdown');

  mobileDropdowns.forEach((dropdown) => {
    const dropdownHead = dropdown.querySelector('.mobile-dropdown-head');
    const dropdownIcon = dropdown.querySelector('i');

    if (dropdownHead) {
      dropdownHead.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();

        const isAlreadyActive = dropdown.classList.contains('active');

        // Önce tüm dropdown'ları kapat
        mobileDropdowns.forEach((d) => {
          d.classList.remove('active');
          const otherIcon = d.querySelector('i');
          if (otherIcon) {
            otherIcon.className = 'fa-solid fa-chevron-down';
          }
        });

        // Eğer tıklanan dropdown zaten aktif değilse, onu aktif yap
        if (!isAlreadyActive) {
          dropdown.classList.add('active');
          if (dropdownIcon) {
            dropdownIcon.className = 'fa-solid fa-chevron-up';
          }
        }
      });
    }
  });

  // =================
  // DESKTOP DROPDOWN FUNCTIONALITY
  // =================
  const dropdowns = document.querySelectorAll('.dropdown');
  const dropdownBackground = document.querySelector('.dropdown-background');

  if (dropdownBackground) {
    dropdowns.forEach((dropdown) => {
      dropdown.addEventListener('mouseenter', function () {
        dropdownBackground.style.display = 'block';
        dropdownBackground.style.visibility = 'visible';
        dropdownBackground.style.opacity = '1';
      });

      dropdown.addEventListener('mouseleave', function (e) {
        const relatedTarget = e.relatedTarget;
        if (
          !dropdown.contains(relatedTarget) &&
          relatedTarget !== dropdownBackground &&
          !dropdownBackground.contains(relatedTarget)
        ) {
          hideDropdownBackground();
        }
      });
    });

    dropdownBackground.addEventListener('mouseleave', function (e) {
      const relatedTarget = e.relatedTarget;
      let isInDropdown = false;

      dropdowns.forEach((dropdown) => {
        if (dropdown.contains(relatedTarget)) {
          isInDropdown = true;
        }
      });

      if (!isInDropdown) {
        hideDropdownBackground();
      }
    });
  }

  // Click based dropdown functionality for cases where hover doesn't work
  dropdowns.forEach((dropdown) => {
    const dropdownHead = dropdown.querySelector('.dropdown-head');
    const dropdownContent = dropdown.querySelector('.dropdown-content');

    if (dropdownHead && dropdownContent) {
      dropdownHead.addEventListener('click', function (e) {
        e.preventDefault();

        // Close other dropdowns
        dropdowns.forEach((otherDropdown) => {
          if (otherDropdown !== dropdown) {
            otherDropdown.classList.remove('active');
          }
        });

        // Toggle current dropdown
        dropdown.classList.toggle('active');
      });
    }
  });

  function hideDropdownBackground() {
    if (dropdownBackground) {
      dropdownBackground.style.visibility = 'hidden';
      dropdownBackground.style.opacity = '0';
      setTimeout(() => {
        if (dropdownBackground.style.opacity === '0') {
          dropdownBackground.style.display = 'none';
        }
      }, 100);
    }
  }

  // =================
  // LANGUAGE DROPDOWN FUNCTIONALITY
  // =================
  // Desktop language dropdown elements
  const langDropdownBtn = document.querySelector('.language-dropdown .lang-dropdown-btn');
  const languageDropdown = document.getElementById('languageDropdown');
  const desktopLangOptions = document.querySelectorAll('#languageDropdown .lang-option');

  // Mobile language dropdown elements
  const mobileLangDropdownBtn = document.querySelector(
    '.mobile-language-dropdown .lang-dropdown-btn'
  );
  const mobileLanguageDropdown = document.getElementById('mobileLanguageDropdown');
  const mobileLangOptions = document.querySelectorAll('#mobileLanguageDropdown .lang-option');

  // Desktop dropdown functionality
  if (langDropdownBtn && languageDropdown) {
    langDropdownBtn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      languageDropdown.classList.toggle('show');
      // Close mobile dropdown if open
      if (mobileLanguageDropdown) {
        mobileLanguageDropdown.classList.remove('show');
      }
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function (e) {
      if (!langDropdownBtn.contains(e.target) && !languageDropdown.contains(e.target)) {
        languageDropdown.classList.remove('show');
      }
    });
  }

  // Mobile language dropdown functionality
  if (mobileLangDropdownBtn && mobileLanguageDropdown) {
    mobileLangDropdownBtn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      mobileLanguageDropdown.classList.toggle('show');
      // Close desktop dropdown if open
      if (languageDropdown) {
        languageDropdown.classList.remove('show');
      }
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function (e) {
      if (!mobileLangDropdownBtn.contains(e.target) && !mobileLanguageDropdown.contains(e.target)) {
        mobileLanguageDropdown.classList.remove('show');
      }
    });
  }

  // Desktop language option click handlers
  desktopLangOptions.forEach((option) => {
    option.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();

      const selectedLang = this.getAttribute('data-lang');

      if (languageDropdown) {
        languageDropdown.classList.remove('show');
      }

      switchLanguage(selectedLang);
    });
  });

  // Mobile language option click handlers
  mobileLangOptions.forEach((option) => {
    option.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();

      const selectedLang = this.getAttribute('data-lang');

      if (mobileLanguageDropdown) {
        mobileLanguageDropdown.classList.remove('show');
      }

      switchLanguage(selectedLang);
    });
  });

  // =================
  // LANGUAGE SWITCHING FUNCTIONS
  // =================
  function switchLanguage(langCode) {
    let csrfValue = getCsrfToken();
    const newPath = calculateNewPath(langCode);

    if (csrfValue) {
      submitLanguageForm(langCode, newPath, csrfValue);
    } else {
      window.location.href = newPath;
    }
  }

  function getCsrfToken() {
    // First try meta tag
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    if (csrfMeta) {
      return csrfMeta.getAttribute('content');
    }

    // Try input field
    const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (csrfInput) {
      return csrfInput.value;
    }

    // Try cookie
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split('=');
      if (name === 'csrftoken') {
        return value;
      }
    }

    return null;
  }

  function calculateNewPath(langCode) {
    const currentPath = window.location.pathname;
    const supportedLangs = ['de', 'es', 'fr', 'it', 'zh-hans'];

    let pathWithoutLang = currentPath;
    let currentLang = 'en';

    // Check if current path starts with a language code
    for (let lang of supportedLangs) {
      if (currentPath.startsWith(`/${lang}/`)) {
        currentLang = lang;
        pathWithoutLang = currentPath.substring(lang.length + 1);
        break;
      } else if (currentPath === `/${lang}`) {
        currentLang = lang;
        pathWithoutLang = '/';
        break;
      }
    }

    // Build new path
    if (langCode === 'en') {
      return pathWithoutLang;
    } else {
      if (pathWithoutLang === '/') {
        return `/${langCode}/`;
      } else if (pathWithoutLang.startsWith('/')) {
        return `/${langCode}${pathWithoutLang}`;
      } else {
        return `/${langCode}/${pathWithoutLang}`;
      }
    }
  }

  function submitLanguageForm(langCode, nextUrl, csrfToken) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/i18n/setlang/';
    form.style.display = 'none';

    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;
    form.appendChild(csrfInput);

    const langInput = document.createElement('input');
    langInput.type = 'hidden';
    langInput.name = 'language';
    langInput.value = langCode;
    form.appendChild(langInput);

    const nextInput = document.createElement('input');
    nextInput.type = 'hidden';
    nextInput.name = 'next';
    nextInput.value = nextUrl;
    form.appendChild(nextInput);

    document.body.appendChild(form);
    form.submit();
  }

  function setActiveLanguageButton() {
    const currentPath = window.location.pathname;
    let currentLang = 'en';

    // Determine current language from URL
    const supportedLangs = ['de', 'es', 'fr', 'it', 'zh-hans'];
    for (let lang of supportedLangs) {
      if (currentPath.startsWith(`/${lang}/`) || currentPath === `/${lang}`) {
        currentLang = lang;
        break;
      }
    }

    // Remove active class from all language options
    document.querySelectorAll('.lang-option').forEach((btn) => {
      btn.classList.remove('active');
    });

    // Add active class to current language
    document.querySelectorAll(`.lang-option[data-lang="${currentLang}"]`).forEach((btn) => {
      btn.classList.add('active');
    });

    // Update dropdown button text
    const langTexts = {
      en: 'EN',
      de: 'DE',
      es: 'ES',
      fr: 'FR',
      it: 'IT',
      'zh-hans': '汉语'
    };

    const currentLangText = langTexts[currentLang] || 'EN';

    // Update desktop dropdown button
    if (langDropdownBtn) {
      langDropdownBtn.innerHTML = `${currentLangText} <i class="fa-solid fa-angle-down"></i>`;
    }

    // Update mobile dropdown button
    if (mobileLangDropdownBtn) {
      mobileLangDropdownBtn.innerHTML = `${currentLangText} <i class="fa-solid fa-angle-down"></i>`;
    }
  }

  // =================
  // ACTIVE LINKS FUNCTIONALITY
  // =================
  function setActiveLinks() {
    const currentPath = window.location.pathname;
    const allNavLinks = document.querySelectorAll('.navbar a[href], .mobile-menu a[href]');

    // Bütün linklərdən active class-ı sil
    allNavLinks.forEach((link) => {
      link.classList.remove('active');
    });

    const dropdownParents = document.querySelectorAll(
      '.dropdown > a, .mobile-dropdown > .mobile-dropdown-head'
    );
    dropdownParents.forEach((parent) => {
      parent.classList.remove('active');
    });

    // Dropdown linklərini yoxla
    const dropdownLinks = document.querySelectorAll(
      '.dropdown-content a[href], .mobile-dropdown-content a[href]'
    );
    let activeDropdownFound = false;

    dropdownLinks.forEach((dropdownLink) => {
      const linkPath = dropdownLink.getAttribute('href');

      if (
        linkPath === currentPath ||
        (linkPath && linkPath !== '/' && currentPath.startsWith(linkPath))
      ) {
        dropdownLink.classList.add('active');

        const parentDropdown = dropdownLink.closest('.dropdown');
        if (parentDropdown) {
          const parentLink = parentDropdown.querySelector('> a');
          if (parentLink) {
            parentLink.classList.add('active');
            activeDropdownFound = true;
          }
        }

        const parentMobileDropdown = dropdownLink.closest('.mobile-dropdown');
        if (parentMobileDropdown) {
          const parentMobileLink = parentMobileDropdown.querySelector('.mobile-dropdown-head');
          if (parentMobileLink) {
            parentMobileLink.classList.add('active');
            activeDropdownFound = true;
          }
        }
      }
    });

    if (!activeDropdownFound) {
      const regularNavLinks = document.querySelectorAll(
        '.navbar a[href]:not(.dropdown-content a), .mobile-menu a[href]:not(.mobile-dropdown-content a)'
      );

      regularNavLinks.forEach((link) => {
        const linkPath = link.getAttribute('href');

        if (linkPath === currentPath) {
          link.classList.add('active');
        } else if (
          linkPath &&
          linkPath !== '/' &&
          linkPath !== '' &&
          currentPath.startsWith(linkPath)
        ) {
          link.classList.add('active');
        }
      });
    }
  }

  initializeMobileMenu();
  setActiveLanguageButton();
  setActiveLinks();

  window.addEventListener('popstate', setActiveLinks);
  window.updateActiveLinks = setActiveLinks;

  window.testLanguageSwitch = function (lang) {
    switchLanguage(lang);
  };

  console.log('Navbar initialized for path:', window.location.pathname);
});
document.addEventListener('DOMContentLoaded', function () {
  let e = !1,
    t = document.querySelectorAll('.mobile-dropdown');
  t.forEach((e) => {
    let a = e.querySelector('.mobile-dropdown-head'),
      n = e.querySelector('i');
    a &&
      a.addEventListener('click', function (a) {
        a.preventDefault(), a.stopPropagation();
        let o = e.classList.contains('active');
        t.forEach((e) => {
          e.classList.remove('active');
          let t = e.querySelector('i');
          t && (t.className = 'fa-solid fa-chevron-down');
        }),
          !o && (e.classList.add('active'), n && (n.className = 'fa-solid fa-chevron-up'));
      });
  });
  let a = document.querySelectorAll('.dropdown'),
    n = document.querySelector('.dropdown-background');
  function o() {
    n &&
      ((n.style.visibility = 'hidden'),
      (n.style.opacity = '0'),
      setTimeout(() => {
        '0' === n.style.opacity && (n.style.display = 'none');
      }, 100));
  }
  n &&
    (a.forEach((e) => {
      e.addEventListener('mouseenter', function () {
        (n.style.display = 'block'), (n.style.visibility = 'visible'), (n.style.opacity = '1');
      }),
        e.addEventListener('mouseleave', function (t) {
          let a = t.relatedTarget;
          e.contains(a) || a === n || n.contains(a) || o();
        });
    }),
    n.addEventListener('mouseleave', function (e) {
      let t = e.relatedTarget,
        n = !1;
      a.forEach((e) => {
        e.contains(t) && (n = !0);
      }),
        n || o();
    })),
    a.forEach((e) => {
      let t = e.querySelector('.dropdown-head'),
        n = e.querySelector('.dropdown-content');
      t &&
        n &&
        t.addEventListener('click', function (t) {
          t.preventDefault(),
            a.forEach((t) => {
              t !== e && t.classList.remove('active');
            }),
            e.classList.toggle('active');
        });
    });
  let l = document.querySelector('.language-dropdown .lang-dropdown-btn'),
    i = document.getElementById('languageDropdown'),
    r = document.querySelectorAll('#languageDropdown .lang-option'),
    s = document.querySelector('.mobile-language-dropdown .lang-dropdown-btn'),
    c = document.getElementById('mobileLanguageDropdown'),
    d = document.querySelectorAll('#mobileLanguageDropdown .lang-option');
  function u(e) {
    let t = (function e() {
        let t = document.querySelector('meta[name="csrf-token"]');
        if (t) return t.getAttribute('content');
        let a = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (a) return a.value;
        let n = document.cookie.split(';');
        for (let o of n) {
          let [l, i] = o.trim().split('=');
          if ('csrftoken' === l) return i;
        }
        return null;
      })(),
      a = (function e(t) {
        let a = window.location.pathname,
          n = a,
          o = 'en';
        for (let l of ['de', 'es', 'fr', 'it', 'zh-hans']) {
          if (a.startsWith(`/${l}/`)) {
            (o = l), (n = a.substring(l.length + 1));
            break;
          }
          if (a === `/${l}`) {
            (o = l), (n = '/');
            break;
          }
        }
        return 'en' === t
          ? n
          : '/' === n
          ? `/${t}/`
          : n.startsWith('/')
          ? `/${t}${n}`
          : `/${t}/${n}`;
      })(e);
    t
      ? (function e(t, a, n) {
          let o = document.createElement('form');
          (o.method = 'POST'), (o.action = '/i18n/setlang/'), (o.style.display = 'none');
          let l = document.createElement('input');
          (l.type = 'hidden'), (l.name = 'csrfmiddlewaretoken'), (l.value = n), o.appendChild(l);
          let i = document.createElement('input');
          (i.type = 'hidden'), (i.name = 'language'), (i.value = t), o.appendChild(i);
          let r = document.createElement('input');
          (r.type = 'hidden'),
            (r.name = 'next'),
            (r.value = a),
            o.appendChild(r),
            document.body.appendChild(o),
            o.submit();
        })(e, a, t)
      : (window.location.href = a);
  }
  function f() {
    let e = window.location.pathname,
      t = document.querySelectorAll('.navbar a[href], .mobile-menu a[href]');
    t.forEach((e) => {
      e.classList.remove('active');
    });
    let a = document.querySelectorAll('.dropdown > a, .mobile-dropdown > .mobile-dropdown-head');
    a.forEach((e) => {
      e.classList.remove('active');
    });
    let n = document.querySelectorAll(
        '.dropdown-content a[href], .mobile-dropdown-content a[href]'
      ),
      o = !1;
    if (
      (n.forEach((t) => {
        let a = t.getAttribute('href');
        if (a === e || (a && '/' !== a && e.startsWith(a))) {
          t.classList.add('active');
          let n = t.closest('.dropdown');
          if (n) {
            let l = n.querySelector('> a');
            l && (l.classList.add('active'), (o = !0));
          }
          let i = t.closest('.mobile-dropdown');
          if (i) {
            let r = i.querySelector('.mobile-dropdown-head');
            r && (r.classList.add('active'), (o = !0));
          }
        }
      }),
      !o)
    ) {
      let l = document.querySelectorAll(
        '.navbar a[href]:not(.dropdown-content a), .mobile-menu a[href]:not(.mobile-dropdown-content a)'
      );
      l.forEach((t) => {
        let a = t.getAttribute('href');
        a === e
          ? t.classList.add('active')
          : a && '/' !== a && '' !== a && e.startsWith(a) && t.classList.add('active');
      });
    }
    !(function e(t) {
      if (['/markets/automotive', '/markets/industrial', '/markets/shipping'].includes(t)) {
        let a = Array.from(document.querySelectorAll('.dropdown > a')).find((e) =>
          e.textContent.trim().toLowerCase().includes('market')
        );
        a && a.classList.add('active');
        let n = Array.from(document.querySelectorAll('.mobile-dropdown-head')).find((e) =>
          e.textContent.trim().toLowerCase().includes('market')
        );
        n && n.classList.add('active');
        let o = document.querySelector(
          `.dropdown-content a[href="${t}"], .mobile-dropdown-content a[href="${t}"]`
        );
        o && o.classList.add('active');
      }
      if (['/services/dealer', '/services/laboratory', '/services/logistics'].includes(t)) {
        let l = Array.from(document.querySelectorAll('.dropdown > a')).find((e) =>
          e.textContent.trim().toLowerCase().includes('service')
        );
        l && l.classList.add('active');
        let i = Array.from(document.querySelectorAll('.mobile-dropdown-head')).find((e) =>
          e.textContent.trim().toLowerCase().includes('service')
        );
        i && i.classList.add('active');
        let r = document.querySelector(
          `.dropdown-content a[href="${t}"], .mobile-dropdown-content a[href="${t}"]`
        );
        r && r.classList.add('active');
      }
    })(e);
  }
  l &&
    i &&
    (l.addEventListener('click', function (e) {
      e.preventDefault(),
        e.stopPropagation(),
        i.classList.toggle('show'),
        c && c.classList.remove('show');
    }),
    document.addEventListener('click', function (e) {
      l.contains(e.target) || i.contains(e.target) || i.classList.remove('show');
    })),
    s &&
      c &&
      (s.addEventListener('click', function (e) {
        e.preventDefault(),
          e.stopPropagation(),
          c.classList.toggle('show'),
          i && i.classList.remove('show');
      }),
      document.addEventListener('click', function (e) {
        s.contains(e.target) || c.contains(e.target) || c.classList.remove('show');
      })),
    r.forEach((e) => {
      e.addEventListener('click', function (e) {
        e.preventDefault(), e.stopPropagation();
        let t = this.getAttribute('data-lang');
        i && i.classList.remove('show'), u(t);
      });
    }),
    d.forEach((e) => {
      e.addEventListener('click', function (e) {
        e.preventDefault(), e.stopPropagation();
        let t = this.getAttribute('data-lang');
        c && c.classList.remove('show'), u(t);
      });
    }),
    !(function t() {
      if (e) {
        console.warn(
          'initializeMobileMenu() zaten \xe7alıştırıldı. Tekrar \xe7alıştırılması engellendi.'
        );
        return;
      }
      let a = document.getElementById('hamburger'),
        n = document.getElementById('mobile-menu');
      if (!a || !n) {
        console.error('HATA: Hamburger veya Mobil Men\xfc elementi bulunamadı!');
        return;
      }
      let o = a.querySelector('i'),
        l = !1;
      a.addEventListener('click', function (e) {
        if ((e.preventDefault(), e.stopPropagation(), l)) return;
        (l = !0), console.log('Hamburger clicked');
        let t = n.classList.toggle('active');
        a.classList.toggle('active'),
          (document.body.style.overflow = t ? 'hidden' : ''),
          o && (o.className = t ? 'fas fa-xmark' : 'fas fa-bars'),
          console.log('Men\xfc durumu değiştirildi. Yeni durum:', t ? 'A\xe7ık' : 'Kapalı'),
          setTimeout(() => {
            l = !1;
          }, 200);
      }),
        document.addEventListener('click', function (e) {
          n.classList.contains('active') &&
            !n.contains(e.target) &&
            !a.contains(e.target) &&
            (n.classList.remove('active'),
            a.classList.remove('active'),
            (document.body.style.overflow = ''),
            o && (o.className = 'fas fa-bars'));
        }),
        (e = !0),
        console.log('✅ Mobile Menu başarıyla y\xfcklendi ve olay dinleyicileri eklendi.');
    })(),
    (function e() {
      let t = window.location.pathname,
        a = 'en';
      for (let n of ['de', 'es', 'fr', 'it', 'zh-hans'])
        if (t.startsWith(`/${n}/`) || t === `/${n}`) {
          a = n;
          break;
        }
      document.querySelectorAll('.lang-option').forEach((e) => {
        e.classList.remove('active');
      }),
        document.querySelectorAll(`.lang-option[data-lang="${a}"]`).forEach((e) => {
          e.classList.add('active');
        });
      let o =
        {
          en: 'EN',
          de: 'DE',
          es: 'ES',
          fr: 'FR',
          it: 'IT',
          'zh-hans': '汉语'
        }[a] || 'EN';
      l && (l.innerHTML = `${o} <i class="fa-solid fa-angle-down"></i>`),
        s && (s.innerHTML = `${o} <i class="fa-solid fa-angle-down"></i>`);
    })(),
    f(),
    window.addEventListener('popstate', f),
    (window.updateActiveLinks = f),
    (window.testLanguageSwitch = function (e) {
      u(e);
    }),
    console.log('Navbar initialized for path:', window.location.pathname);
});
