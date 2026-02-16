let currentStep = 1;

// ── Open / Close Popup ──

function openOrderPopup() {
  resetForm();
  document.getElementById('popupOverlay').classList.add('open');
}

function closePopup() {
  document.getElementById('popupOverlay').classList.remove('open');
}

function closeOrderPopup(e) {
  if (e.target === e.currentTarget) {
    closePopup();
  }
}

// ── Phone Formatting ──

function formatPhone(input) {
  let digits = input.value.replace(/\D/g, '');
  if (digits.length > 10) digits = digits.slice(0, 10);

  let formatted = '';
  if (digits.length > 0) formatted = '(' + digits.slice(0, 3);
  if (digits.length >= 3) formatted += ') ';
  if (digits.length > 3) formatted += digits.slice(3, 6);
  if (digits.length > 6) formatted += '-' + digits.slice(6);

  input.value = formatted;
}

// ── Validation ──

function clearErrors() {
  document.querySelectorAll('.field-error').forEach(el => el.textContent = '');
  document.querySelectorAll('input.invalid').forEach(el => el.classList.remove('invalid'));
}

function showError(fieldId, message) {
  const input = document.getElementById(fieldId);
  const error = document.getElementById(fieldId + 'Error');
  if (input) input.classList.add('invalid');
  if (error) error.textContent = message;
}

function validateStep1() {
  clearErrors();
  const phone = document.getElementById('phone').value.replace(/\D/g, '');
  if (phone.length < 10) {
    showError('phone', 'Please enter a valid 10-digit phone number.');
    return false;
  }
  return true;
}

function validateStep2() {
  clearErrors();
  let valid = true;

  const fullName = document.getElementById('fullName').value.trim();
  if (!fullName) {
    showError('fullName', 'Full name is required.');
    valid = false;
  }

  const street = document.getElementById('street').value.trim();
  if (!street) {
    showError('street', 'Street address is required.');
    valid = false;
  }

  const city = document.getElementById('city').value.trim();
  if (!city) {
    showError('city', 'City is required.');
    valid = false;
  }

  const zip = document.getElementById('zip').value.trim();
  if (zip.length !== 5) {
    showError('zip', 'Enter a 5-digit zip code.');
    valid = false;
  }

  const email = document.getElementById('email').value.trim();
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailPattern.test(email)) {
    showError('email', 'Please enter a valid email address.');
    valid = false;
  }

  return valid;
}

function validateStep3() {
  clearErrors();
  const selected = document.querySelector('input[name="orderMethod"]:checked');
  if (!selected) {
    document.getElementById('methodError').textContent = 'Please select pickup or delivery.';
    return false;
  }
  return true;
}

// ── Step Navigation ──

function goToStep(step) {
  // Validate current step before advancing
  if (step > currentStep) {
    if (currentStep === 1 && !validateStep1()) return;
    if (currentStep === 2 && !validateStep2()) return;
  }

  clearErrors();
  currentStep = step;

  // Toggle active step panel
  document.querySelectorAll('.popup-step').forEach(el => el.classList.remove('active'));
  document.getElementById('step' + step).classList.add('active');

  // Update progress indicators
  document.querySelectorAll('.progress-step').forEach(el => {
    const s = parseInt(el.dataset.step);
    el.classList.remove('active', 'done');
    if (s === step) el.classList.add('active');
    if (s < step) el.classList.add('done');
  });

  // Update progress lines
  document.getElementById('line1').classList.toggle('filled', step >= 2);
  document.getElementById('line2').classList.toggle('filled', step >= 3);
}

// ── Method Selection ──

function selectMethod(radio) {
  document.querySelectorAll('.method-card').forEach(c => c.classList.remove('selected'));
  radio.closest('.method-card').classList.add('selected');
  document.getElementById('methodError').textContent = '';
}

// ── Submit ──

function submitOrder() {
  if (!validateStep3()) return;

  const method = document.querySelector('input[name="orderMethod"]:checked').value;
  const data = {
    phone: document.getElementById('phone').value,
    fullName: document.getElementById('fullName').value.trim(),
    street: document.getElementById('street').value.trim(),
    city: document.getElementById('city').value.trim(),
    zip: document.getElementById('zip').value.trim(),
    email: document.getElementById('email').value.trim(),
    orderMethod: method,
  };

  console.log('Order submitted:', data);
  alert('Order placed! You chose: ' + method.charAt(0).toUpperCase() + method.slice(1));
  closePopup();
}

// ── Reset ──

function resetForm() {
  currentStep = 1;
  document.querySelectorAll('.popup-step').forEach(el => el.classList.remove('active'));
  document.getElementById('step1').classList.add('active');

  document.querySelectorAll('.progress-step').forEach(el => {
    el.classList.remove('active', 'done');
  });
  document.querySelector('.progress-step[data-step="1"]').classList.add('active');
  document.getElementById('line1').classList.remove('filled');
  document.getElementById('line2').classList.remove('filled');

  document.getElementById('phone').value = '';
  document.getElementById('fullName').value = '';
  document.getElementById('street').value = '';
  document.getElementById('city').value = '';
  document.getElementById('zip').value = '';
  document.getElementById('email').value = '';

  document.querySelectorAll('input[name="orderMethod"]').forEach(r => r.checked = false);
  document.querySelectorAll('.method-card').forEach(c => c.classList.remove('selected'));

  clearErrors();
}

// Close on Escape key
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') closePopup();
});
