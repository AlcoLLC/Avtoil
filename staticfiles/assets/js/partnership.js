document.addEventListener('DOMContentLoaded', function () {
  const commentSwiper = new Swiper('.partner-review-section .commentSwiper', {
    cssMode: true,
    slidesPerView: 2,
    spaceBetween: 20,
    navigation: {
      nextEl: '.partner-review-section .swiper-button-next',
      prevEl: '.partner-review-section .swiper-button-prev'
    },
    pagination: {
      el: '.partner-review-section .swiper-pagination'
    },
    mousewheel: true,
    keyboard: true
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const coorperationSelect = document.querySelector('.coorperation-select');
  const coorperationOptions = document.querySelector('.coorperation-options');
  const hiddenInput = document.querySelector('#typeOfBusiness');

  if (!coorperationSelect || !coorperationOptions) {
    console.log(
      'coorperation select elements not found - this script may not be needed on this page'
    );
    return;
  }

  function selectOption(option) {
    const selectedText = option.textContent.trim();
    const selectedValue = option.getAttribute('data-value') || selectedText;

    coorperationSelect.textContent = selectedText;
    if (hiddenInput) {
      hiddenInput.value = selectedValue;
    }

    document
      .querySelectorAll('.coorperation-option')
      .forEach((opt) => opt.classList.remove('selected'));
    option.classList.add('selected');

    coorperationOptions.classList.remove('active');
    coorperationSelect.classList.remove('open');
  }

  coorperationSelect.addEventListener('click', function (e) {
    e.stopPropagation();
    this.classList.toggle('open');
    coorperationOptions.classList.toggle('active');
  });

  document.addEventListener('click', function (e) {
    if (e.target.classList.contains('coorperation-option')) {
      e.stopPropagation();
      selectOption(e.target);
    }
  });

  document.addEventListener('click', function () {
    coorperationOptions.classList.remove('active');
    coorperationSelect.classList.remove('open');
  });

  const firstOption =
    document.querySelector('.coorperation-option[data-value="buy"]') ||
    document.querySelector('.coorperation-option');
  if (firstOption) {
    firstOption.classList.add('selected');
    coorperationSelect.textContent = firstOption.textContent.trim();
    if (hiddenInput) {
      hiddenInput.value = firstOption.getAttribute('data-value');
    }
  }
});

// Form submit handling
const form = document.querySelector('.coorperation-form form');
if (form) {
  form.addEventListener('submit', function (e) {
    const requiredFields = form.querySelectorAll('input[required], select[required]');
    let isValid = true;

    requiredFields.forEach((field) => {
      if (!field.value.trim()) {
        isValid = false;
        field.style.borderColor = '#dc3545';
      } else {
        field.style.borderColor = '#b4b7d425';
      }
    });

    // Check hidden input (business type)
    const hiddenInput = document.querySelector('#typeOfBusiness');
    if (!hiddenInput || !hiddenInput.value) {
      isValid = false;
      const selectWrapper = document.querySelector('.coorperation-select');
      if (selectWrapper) {
        selectWrapper.style.borderColor = '#dc3545';
      }
    }

    if (!isValid) {
      e.preventDefault();
      // Show error message if needed
    }
  });
}

// Auto hide messages after 5 seconds
document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.style.display = 'none';
    }, 5000);
  });
});
