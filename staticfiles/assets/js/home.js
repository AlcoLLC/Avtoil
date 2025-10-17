const swiper = new Swiper('.home-header .mySwiper', {
  loop: true,
  effect: 'fade',
  lazy: {
    loadPrevNext: true,
    loadPrevNextAmount: 2
  },
  autoplay: {
    delay: 5000,
    disableOnInteraction: false
  },
  navigation: {
    nextEl: '.home-header .swiper-button-next',
    prevEl: '.home-header .swiper-button-prev'
  },
  pagination: {
    el: '.home-header .swiper-pagination',
    clickable: true
  }
});


document.addEventListener('DOMContentLoaded', function () {
  const playButton = document.getElementById('playButton');
  const textContent = document.getElementById('textContent');
  const videoContainer = document.getElementById('videoContainer');
  const youtubeVideo = document.getElementById('youtubeVideo');

  if (playButton) {
    playButton.addEventListener('click', function () {
      textContent.classList.add('hidden');
      playButton.style.display = 'none';
      videoContainer.style.display = 'block';
      const videoSrc = youtubeVideo.src;
      youtubeVideo.src = videoSrc + '&autoplay=1';
    });
  }

});

document.addEventListener('DOMContentLoaded', function () {
  const seeMoreBtn = document.getElementById('seeMoreBtn');
  const hiddenCards = document.querySelectorAll('.category-card.hidden');

  if (seeMoreBtn) {
    seeMoreBtn.addEventListener('click', function () {
      hiddenCards.forEach((card, index) => {
        card.classList.remove('hidden');
        card.classList.add('fade-in');

        setTimeout(() => {
          card.classList.remove('fade-in');
        }, index * 100);
      });
      seeMoreBtn.style.display = 'none';
    });
  }
});

document.addEventListener('DOMContentLoaded', function () {
  initProductSlider();
});

function initProductSlider() {
  const sliderContainer = document.querySelector('.featured-section .slider-container');
  const productCards = document.querySelectorAll('.featured-section .product-card');
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
    if (allCards[currentIndex]) allCards[currentIndex].classList.add('visible', 'active');
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

document.addEventListener("DOMContentLoaded", function () {
  const playButton = document.getElementById('playButton');
  const videoContainer = document.getElementById('videoContainer');
  const textContent = document.getElementById('textContent');
  const videoId = 'Wx63amCTJqs'; 
  playButton.addEventListener('click', function () {
    textContent.classList.add('hidden');
    playButton.classList.add('hidden');

    videoContainer.style.display = 'block';

    const iframe = document.createElement('iframe');

    iframe.setAttribute('width', '560');
    iframe.setAttribute('height', '315');
    iframe.setAttribute('src', `https://www.youtube-nocookie.com/embed/${videoId}?rel=0&showinfo=0&modestbranding=1&autoplay=1`);
    iframe.setAttribute('title', 'YouTube video player');
    iframe.setAttribute('frameborder', '0');
    iframe.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share');
    iframe.setAttribute('allowfullscreen', 'true');

    videoContainer.innerHTML = ''; 
    videoContainer.appendChild(iframe);
  });
});

document.addEventListener("DOMContentLoaded", function() {
    const mapSection = document.querySelector('.map-section');
    if (mapSection) {
        const scriptUrl = mapSection.dataset.scriptUrl;
        if (scriptUrl) {
            const observerOptions = {
                root: null,
                rootMargin: '0px',
                threshold: 0.1
            };

            const mapObserver = new IntersectionObserver(function(entries, observer) {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const mapScript = document.createElement('script');
                        mapScript.src = scriptUrl;
                        document.body.appendChild(mapScript);
                        observer.unobserve(mapSection);
                    }
                });
            }, observerOptions);
            mapObserver.observe(mapSection);
        } else {
            console.error('Harita script URLsi "data-script-url" attributeunda bulunamadı.');
        }
    }
});