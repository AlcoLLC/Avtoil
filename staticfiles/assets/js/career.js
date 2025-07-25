let currentStep = 1;
let formData = {};

// Modal elementlerini al - null check ile
const customAlertModal = document.getElementById('customAlertModal');
const customAlertModalMessage = document.getElementById('customAlertModalMessage');
const customAlertModalTitle = document.getElementById('customAlertModalTitle');

// File upload handler - element kontrolü ile
const cvFileInput = document.getElementById('cvFile');
const fileNameElement = document.getElementById('file-name');

if (cvFileInput && fileNameElement) {
    cvFileInput.addEventListener('change', function(e) {
        const fileName = e.target.files[0] ? e.target.files[0].name : 'Click to upload file';
        fileNameElement.textContent = fileName;
    });
}

// Yeni Modal Fonksiyonları
function showCustomAlertModal(message, title = 'Notification') {
    if (!customAlertModal || !customAlertModalMessage || !customAlertModalTitle) {
        console.error('Modal elements not found, falling back to alert');
        alert(title + ': ' + message);
        return;
    }
    
    customAlertModalTitle.textContent = title;
    customAlertModalMessage.textContent = message;
    customAlertModal.style.display = 'flex';
    setTimeout(() => {
        customAlertModal.classList.add('show');
    }, 10);
}

function hideCustomAlertModal() {
    if (!customAlertModal) return;
    
    customAlertModal.classList.remove('show');
    setTimeout(() => {
        customAlertModal.style.display = 'none';
    }, 300);
}

// Modalın dışına tıklandığında kapatma - element kontrolü ile
if (customAlertModal) {
    customAlertModal.addEventListener('click', function(event) {
        if (event.target === customAlertModal) {
            hideCustomAlertModal();
        }
    });
}

function nextStep(step) {
    if (validateStep(step)) {
        saveStepData(step);
        showStep(step + 1);
    }
}

function previousStep(step) {
    showStep(step - 1);
}

function showStep(stepNumber) {
    document.querySelectorAll('.step-container').forEach(container => {
        container.style.display = 'none';
    });
    
    const targetStepId = stepNumber <= 3 ? `step-${stepNumber}` : (stepNumber === 4 ? 'confirmation' : 'success');
    const targetStepElement = document.getElementById(targetStepId);
    if (targetStepElement) {
        targetStepElement.style.display = 'block';
    }
    currentStep = stepNumber;
}

function validateStep(step) {
    let isValid = true;
    let errorMessage = '';
    let errorTitle = 'Validation Error';
    
    if (step === 1) {
        const firstName = document.getElementById('firstName');
        const lastName = document.getElementById('lastName');
        const email = document.getElementById('email');
        const phone = document.getElementById('phone');
        
        // Element kontrolü
        if (!firstName || !lastName || !email || !phone) {
            isValid = false;
            errorMessage = 'Required form elements are missing. Please refresh the page.';
        } else {
            const firstNameValue = firstName.value.trim();
            const lastNameValue = lastName.value.trim();
            const emailValue = email.value.trim();
            const phoneValue = phone.value.trim();
            
            if (!firstNameValue || !lastNameValue || !emailValue || !phoneValue) {
                isValid = false;
                errorMessage = 'Please fill in all required personal information fields.';
            } else if (!/^\S+@\S+\.\S+$/.test(emailValue)) {
                isValid = false;
                errorMessage = 'Please enter a valid email address.';
            }
        }
    } else if (step === 2) {
        const cvFileInput = document.getElementById('cvFile');
        if (!cvFileInput) {
            isValid = false;
            errorMessage = 'CV upload field is missing. Please refresh the page.';
        } else if (!cvFileInput.files[0]) {
            isValid = false;
            errorMessage = 'Please upload your CV file.';
        }
    } else if (step === 3) {
        const motivationLetter = document.getElementById('motivationLetter');
        if (!motivationLetter) {
            isValid = false;
            errorMessage = 'Motivation letter field is missing. Please refresh the page.';
        } else if (!motivationLetter.value.trim()) {
            isValid = false;
            errorMessage = 'Please write your motivation letter.';
        }
    }
    
    if (!isValid) {
        showCustomAlertModal(errorMessage, errorTitle);
    }
    
    return isValid;
}

function saveStepData(step) {
    if (step === 1) {
        const firstName = document.getElementById('firstName');
        const lastName = document.getElementById('lastName');
        const email = document.getElementById('email');
        const phone = document.getElementById('phone');
        
        if (firstName && lastName && email && phone) {
            formData.first_name = firstName.value.trim();
            formData.last_name = lastName.value.trim();
            formData.email = email.value.trim();
            formData.phone = phone.value.trim();
        }
    } else if (step === 2) {
        const cvFileInput = document.getElementById('cvFile');
        if (cvFileInput && cvFileInput.files[0]) {
            formData.cv_file = cvFileInput.files[0];
        }
    } else if (step === 3) {
        const motivationLetter = document.getElementById('motivationLetter');
        if (motivationLetter) {
            formData.motivation_letter = motivationLetter.value.trim();
        }
    }
}

function showConfirmation() {
    if (validateStep(3)) {
        saveStepData(3);
        
        // Confirmation elementlerini kontrol et
        const confirmElements = {
            firstName: document.getElementById('confirm-firstName'),
            lastName: document.getElementById('confirm-lastName'),
            email: document.getElementById('confirm-email'),
            phone: document.getElementById('confirm-phone'),
            cvFile: document.getElementById('confirm-cvFile')
        };
        
        // Sadece mevcut elementleri güncelle
        if (confirmElements.firstName) confirmElements.firstName.textContent = formData.first_name || '';
        if (confirmElements.lastName) confirmElements.lastName.textContent = formData.last_name || '';
        if (confirmElements.email) confirmElements.email.textContent = formData.email || '';
        if (confirmElements.phone) confirmElements.phone.textContent = formData.phone || '';
        if (confirmElements.cvFile) confirmElements.cvFile.textContent = formData.cv_file ? formData.cv_file.name : 'Not uploaded';
        
        showStep(4);
    }
}

function submitApplication() {
    const submitFormData = new FormData();
    
    // CSRF token'ını bul
    const csrfTokenInput = document.querySelector('#step1-form [name=csrfmiddlewaretoken]') || 
                           document.querySelector('#step2-form [name=csrfmiddlewaretoken]') ||
                           document.querySelector('#step3-form [name=csrfmiddlewaretoken]') ||
                           document.querySelector('[name=csrfmiddlewaretoken]'); // Genel arama

    if (csrfTokenInput) {
        submitFormData.append('csrfmiddlewaretoken', csrfTokenInput.value);
    } else {
        console.error('CSRF token not found!');
        showCustomAlertModal('A security token is missing. Please refresh the page and try again.', 'Error');
        return;
    }
    
    // Form verilerini ekle
    if (formData.first_name) submitFormData.append('first_name', formData.first_name);
    if (formData.last_name) submitFormData.append('last_name', formData.last_name);
    if (formData.email) submitFormData.append('email', formData.email);
    if (formData.phone) submitFormData.append('phone', formData.phone);
    if (formData.cv_file) submitFormData.append('cv_file', formData.cv_file);
    if (formData.motivation_letter) submitFormData.append('motivation_letter', formData.motivation_letter);
    
    // Butonu güncelle
    const confirmButton = document.querySelector('.btn-confirm');
    if (confirmButton) {
        const originalButtonText = confirmButton.innerHTML;
        confirmButton.disabled = true;
        confirmButton.innerHTML = 'Sending...';

        fetch(window.location.href, {
            method: 'POST',
            body: submitFormData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showStep(5);
            } else {
                showCustomAlertModal(data.message || 'An unknown error occurred. Please check your input.', 'Application Error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showCustomAlertModal('An error occurred while submitting your application. Please try again later.', 'Submission Failed');
        })
        .finally(() => {
            confirmButton.disabled = false;
            confirmButton.innerHTML = originalButtonText;
        });
    } else {
        console.error('Confirm button not found');
        showCustomAlertModal('Submit button not found. Please refresh the page.', 'Error');
    }
}

// Sayfa yüklendiğinde çalışacak kod
document.addEventListener('DOMContentLoaded', function() {
    // İlk adımı göster - sadece step container'ları varsa
    const stepContainers = document.querySelectorAll('.step-container');
    if (stepContainers.length > 0) {
        showStep(1);
    } else {
        console.warn('No step containers found on this page');
    }
});