document.addEventListener('DOMContentLoaded', function () {
    // Element kontrolü ile başla
    const customSelect = document.querySelector('.custom-select');
    const customOptions = document.querySelector('.custom-options');
    const hiddenInput = document.querySelector('#helpType');
    const contactForm = document.querySelector('form[action*="contact"]');
   
    // Ana custom select elementleri yoksa, bu sayfa için script'i çalıştırma
    if (!customSelect || !customOptions) {
        console.log("Custom select elements not found - this script may not be needed on this page");
        return;
    }

    const optionItems = document.querySelectorAll('.custom-option');
   
    // Eğer template'den option'lar gelmemişse (fallback için)
    if (optionItems.length === 0) {
        console.warn("No options found from template, creating fallback options");
        
        const helpChoices = [
            ['buy', 'I would like to buy Aminol products.'],
            ['become_dealer', 'I am interested in becoming a distributor.'],
            ['technical', 'I need technical support.'],
            ['other', 'Other']
        ];
       
        helpChoices.forEach(choice => {
            const option = document.createElement('div');
            option.className = 'custom-option';
            option.setAttribute('data-value', choice[0]);
            option.textContent = choice[1];
            customOptions.appendChild(option);
           
            option.addEventListener('click', function(e) {
                selectOption(this);
            });
        });
    } else {
        // Template'den gelen option'lara click event'i ekle
        optionItems.forEach(option => {
            option.addEventListener('click', function(e) {
                selectOption(this);
            });
        });
    }
   
    function selectOption(option) {
        const selectedText = option.textContent.trim();
        const selectedValue = option.getAttribute('data-value') || selectedText;
       
        customSelect.textContent = selectedText;
        if (hiddenInput) {
            hiddenInput.value = selectedValue;
        }
       
        document.querySelectorAll('.custom-option').forEach(opt =>
            opt.classList.remove('selected'));
        option.classList.add('selected');
       
        customOptions.classList.remove('active');
        customSelect.classList.remove('open');
    }
   
    customSelect.addEventListener('click', function (e) {
        e.stopPropagation();
        this.classList.toggle('open');
        customOptions.classList.toggle('active');
    });
   
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('custom-option')) {
            e.stopPropagation();
            selectOption(e.target);
        }
    });
   
    document.addEventListener('click', function () {
        customOptions.classList.remove('active');
        customSelect.classList.remove('open');
    });
   
    // İlk option'ı default olarak seç
    const firstOption = document.querySelector('.custom-option[data-value="buy"]') || 
                       document.querySelector('.custom-option');
    if (firstOption) {
        firstOption.classList.add('selected');
        customSelect.textContent = firstOption.textContent.trim();
        if (hiddenInput) {
            hiddenInput.value = firstOption.getAttribute('data-value');
        }
    }

    // reCAPTCHA validation functions
    function showRecaptchaError(message) {
        // Remove existing error message
        const existingError = document.querySelector('.recaptcha-error');
        if (existingError) {
            existingError.remove();
        }

        // Create new error message
        const recaptchaContainer = document.querySelector('.g-recaptcha');
        if (recaptchaContainer) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'recaptcha-error alert alert-danger';
            errorDiv.style.cssText = 'color: #d32f2f; font-size: 14px; margin-top: 5px; padding: 8px; background: #ffebee; border: 1px solid #ffcdd2; border-radius: 4px;';
            errorDiv.textContent = message;
            recaptchaContainer.parentNode.insertBefore(errorDiv, recaptchaContainer.nextSibling);
        }
    }

    function clearRecaptchaError() {
        const existingError = document.querySelector('.recaptcha-error');
        if (existingError) {
            existingError.remove();
        }
    }

    function validateRecaptcha() {
        // reCAPTCHA yüklü değilse, validasyonu atla
        if (typeof grecaptcha === 'undefined') {
            console.warn('reCAPTCHA not loaded');
            return true; // Bu durumda server-side validasyon yapılmalı
        }
        
        const recaptchaResponse = grecaptcha.getResponse();
        
        if (!recaptchaResponse) {
            showRecaptchaError('Please complete the reCAPTCHA verification.');
            return false;
        }
        
        clearRecaptchaError();
        return true;
    }

    // Form submission handler with reCAPTCHA validation
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            // reCAPTCHA kontrolü - sadece yüklüyse
            if (typeof grecaptcha !== 'undefined') {
                if (!validateRecaptcha()) {
                    e.preventDefault();
                    return false;
                }
            }

            // Required field validations
            const requiredFields = contactForm.querySelectorAll('[required]');
            let hasEmptyFields = false;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    hasEmptyFields = true;
                    field.style.borderColor = '#d32f2f';
                } else {
                    field.style.borderColor = '';
                }
            });

            if (hasEmptyFields) {
                e.preventDefault();
                showRecaptchaError('Please fill in all required fields.');
                return false;
            }

            // Show loading state
            const submitButton = contactForm.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = 'Sending... <i class="fa-solid fa-spinner fa-spin"></i>';
                
                // Store original text for potential reset
                submitButton.setAttribute('data-original-text', originalText);
            }
        });
    }

    // reCAPTCHA callback functions (global scope) - sadece reCAPTCHA varsa
    if (typeof window !== 'undefined') {
        window.onRecaptchaSuccess = function() {
            clearRecaptchaError();
            console.log('reCAPTCHA verified successfully');
        };

        window.onRecaptchaExpired = function() {
            showRecaptchaError('reCAPTCHA has expired. Please verify again.');
            console.log('reCAPTCHA expired');
        };

        window.onRecaptchaError = function() {
            showRecaptchaError('reCAPTCHA verification failed. Please try again.');
            console.log('reCAPTCHA error occurred');
        };

        // Reset form state
        window.resetContactForm = function() {
            if (contactForm) {
                const submitButton = contactForm.querySelector('button[type="submit"]');
                if (submitButton) {
                    submitButton.disabled = false;
                    const originalText = submitButton.getAttribute('data-original-text') || 
                                       'Send <i class="fa-solid fa-paper-plane"></i>';
                    submitButton.innerHTML = originalText;
                }
            }
            
            if (typeof grecaptcha !== 'undefined') { 
                try {
                    grecaptcha.reset();
                } catch (error) {
                    console.log('reCAPTCHA reset failed:', error);
                }
            }
            
            clearRecaptchaError();
        };
    }

    // Handle form reset on page navigation back
    window.addEventListener('pageshow', function(event) {
        if (event.persisted && typeof window.resetContactForm === 'function') {
            window.resetContactForm();
        }
    });
});