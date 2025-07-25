const swiper = new Swiper(".home-header .mySwiper", {
  loop: true,
  effect: "fade",
  lazy: {
    loadPrevNext: true,
    loadPrevNextAmount: 2,
  },
  autoplay: {
    delay: 5000,
    disableOnInteraction: false,
  },
  navigation: {
    nextEl: ".home-header .swiper-button-next",
    prevEl: ".home-header .swiper-button-prev",
  },
  pagination: {
    el: ".home-header .swiper-pagination",
    clickable: true,
  },
});

window.addEventListener("scroll", function () {
  const fixedWhatsapp = document.querySelector(".fixed-whatsapp");
  const scrollPosition = window.scrollY;

  if (scrollPosition > 100) {
    fixedWhatsapp.style.opacity = "1";
    fixedWhatsapp.style.visibility = "visible";

    if (headerWhatsapp) {
      headerWhatsapp.style.opacity = "0";
      headerWhatsapp.style.visibility = "hidden";
    }
  } else {
    fixedWhatsapp.style.opacity = "0";
    fixedWhatsapp.style.visibility = "hidden";

    if (headerWhatsapp) {
      headerWhatsapp.style.opacity = "1";
      headerWhatsapp.style.visibility = "visible";
    }
  }
});

document.getElementById("scrollToTop").addEventListener("click", function () {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const playButton = document.getElementById("playButton");
  const textContent = document.getElementById("textContent");
  const videoContainer = document.getElementById("videoContainer");
  const youtubeVideo = document.getElementById("youtubeVideo");

  if (playButton) {
    playButton.addEventListener("click", function () {
      textContent.classList.add("hidden");
      playButton.style.display = "none";
      videoContainer.style.display = "block";
      const videoSrc = youtubeVideo.src;
      youtubeVideo.src = videoSrc + "&autoplay=1";
    });
  }

  checkScroll();
  window.addEventListener("scroll", checkScroll);

  function checkScroll() {
    const sections = document.querySelectorAll(".section");
    sections.forEach((section) => {
      const sectionTop = section.getBoundingClientRect().top;
      const windowHeight = window.innerHeight;
      if (sectionTop < windowHeight * 0.85) {
        section.classList.add("active");
      } else {
        section.classList.remove("active");
      }
    });
  }

  const swiperGallery = new Swiper(".gallery-section .labSwiper", {
    slidesPerView: 2.5,
    centeredSlides: true,
    spaceBetween: 20,
    loop: true,
    speed: 800,
    navigation: {
      nextEl: ".gallery-section .swiper-button-next",
      prevEl: ".gallery-section .swiper-button-prev",
    },
    breakpoints: {
      320: {
        slidesPerView: 1.3,
        spaceBetween: 15,
      },
      640: {
        slidesPerView: 1.8,
        spaceBetween: 15,
      },
      1024: {
        slidesPerView: 2.2,
        spaceBetween: 20,
      },
    },
    on: {
      init: function () {
        updateSlideScaling();
      },
      slideChange: function () {
        updateSlideScaling();
      },
    },
  });

  function updateSlideScaling() {
    const slides = document.querySelectorAll(".gallery-section .swiper-slide");

    slides.forEach((slide) => {
      slide.classList.remove("active-slide");
    });

    setTimeout(() => {
      const activeSlide = document.querySelector(
        ".gallery-section .swiper-slide-active"
      );
      if (activeSlide) {
        activeSlide.classList.add("active-slide");
      }
    }, 50);
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const seeMoreBtn = document.getElementById("seeMoreBtn");
  const hiddenCards = document.querySelectorAll(".category-card.hidden");

  if (seeMoreBtn) {
    seeMoreBtn.addEventListener("click", function () {
      hiddenCards.forEach((card, index) => {
        card.classList.remove("hidden");
        card.classList.add("fade-in");

        setTimeout(() => {
          card.classList.remove("fade-in");
        }, index * 100);
      });
      seeMoreBtn.style.display = "none";
    });
  }
});

document.addEventListener('DOMContentLoaded', function () {
  initProductSlider();
});

function initProductSlider() {
  const sliderContainer = document.querySelector(
    '.featured-section .slider-container'
  );
  const productCards = document.querySelectorAll(
    '.featured-section .product-card'
  );
  const prevBtn = document.querySelector('.featured-section .prev-btn');
  const nextBtn = document.querySelector('.featured-section .next-btn');

  const originalProductCount = productCards.length;
  let autoplayInterval;

  // Orijinal elementləri kopyalayıb əvvələ və sona əlavə et
  function createInfiniteLoop() {
    // Sonuncu elementləri əvvələ əlavə et
    for (let i = originalProductCount - 1; i >= 0; i--) {
      const clone = productCards[i].cloneNode(true);
      sliderContainer.insertBefore(clone, sliderContainer.firstChild);
    }

    // İlk elementləri sona əlavə et
    for (let i = 0; i < originalProductCount; i++) {
      const clone = productCards[i].cloneNode(true);
      sliderContainer.appendChild(clone);
    }
  }

  createInfiniteLoop();

  // Yenilənmiş card listini al
  const allCards = document.querySelectorAll('.featured-section .product-card');
  const totalCards = allCards.length;

  // Başlanğıc pozisiyası - orijinal ilk element (ortadakı grup)
  let currentIndex = originalProductCount + 1; // İkinci qrupdan başla (orijinal mərkəz)

  function updateSlider() {
    allCards.forEach((card) => {
      card.classList.remove('visible', 'active');
    });

    const prevIndex = currentIndex - 1;
    const nextIndex = currentIndex + 1;

    if (allCards[prevIndex]) allCards[prevIndex].classList.add('visible');
    if (allCards[currentIndex])
      allCards[currentIndex].classList.add('visible', 'active');
    if (allCards[nextIndex]) allCards[nextIndex].classList.add('visible');
  }

  function nextSlide() {
    currentIndex++;

    // Sona çatdıqda başa qayıt
    if (currentIndex >= totalCards - originalProductCount) {
      currentIndex = originalProductCount;
    }

    updateSlider();
  }

  function prevSlide() {
    currentIndex--;

    // Başa çatdıqda sona qayıt
    if (currentIndex < originalProductCount) {
      currentIndex = totalCards - originalProductCount - 1;
    }

    updateSlider();
  }

  function startAutoplay() {
    autoplayInterval = setInterval(() => {
      nextSlide();
    }, 3000);
  }

  function stopAutoplay() {
    clearInterval(autoplayInterval);
  }

  function restartAutoplay() {
    stopAutoplay();
    startAutoplay();
  }

  prevBtn.addEventListener('click', () => {
    prevSlide();
    restartAutoplay();
  });

  nextBtn.addEventListener('click', () => {
    nextSlide();
    restartAutoplay();
  });

  updateSlider();
  startAutoplay();

  let touchStartX = 0;
  let touchEndX = 0;

  sliderContainer.addEventListener(
    'touchstart',
    (e) => {
      touchStartX = e.changedTouches[0].screenX;
      stopAutoplay();
    },
    false
  );

  sliderContainer.addEventListener(
    'touchend',
    (e) => {
      touchEndX = e.changedTouches[0].screenX;
      handleSwipe();
      restartAutoplay();
    },
    false
  );

  function handleSwipe() {
    if (touchEndX < touchStartX - 50) {
      nextSlide();
    }

    if (touchEndX > touchStartX + 50) {
      prevSlide();
    }
  }

  sliderContainer.addEventListener('mouseenter', stopAutoplay);
  sliderContainer.addEventListener('mouseleave', startAutoplay);
}

