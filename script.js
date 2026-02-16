let currentStep = 1;

/* ── Open / Close ── */

function openOrderPopup() {
  resetForm();
  document.getElementById('popupOverlay').classList.add('open');
  // Focus the first input after transition
  setTimeout(() => document.getElementById('phone').focus(), 350);
}

function closePopup() {
  document.getElementById('popupOverlay').classList.remove('open');
}

function closeOrderPopup(e) {
  if (e.target === e.currentTarget) closePopup();
}

/* ── Phone Formatting ── */

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

/* ── Validation ── */

function clearErrors() {
  document.querySelectorAll('.field-error').forEach(el => el.textContent = '');
  document.querySelectorAll('input.invalid').forEach(el => el.classList.remove('invalid'));
}

function showError(fieldId, msg) {
  const input = document.getElementById(fieldId);
  const error = document.getElementById(fieldId + 'Error');
  if (input) input.classList.add('invalid');
  if (error) error.textContent = msg;
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

  if (!document.getElementById('fullName').value.trim()) {
    showError('fullName', 'Full name is required.');
    valid = false;
  }
  if (!document.getElementById('street').value.trim()) {
    showError('street', 'Street address is required.');
    valid = false;
  }
  if (!document.getElementById('city').value.trim()) {
    showError('city', 'City is required.');
    valid = false;
  }
  if (document.getElementById('zip').value.trim().length !== 5) {
    showError('zip', 'Enter a 5-digit zip code.');
    valid = false;
  }

  const email = document.getElementById('email').value.trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    showError('email', 'Please enter a valid email address.');
    valid = false;
  }

  return valid;
}

function validateStep3() {
  clearErrors();
  if (!document.querySelector('input[name="orderMethod"]:checked')) {
    document.getElementById('methodError').textContent = 'Please select pickup or delivery.';
    return false;
  }
  return true;
}

/* ── Stepper ── */

function updateStepper(step) {
  // Fill bar: step 1 = 0%, step 2 = 50%, step 3 = 100%
  const pct = ((step - 1) / 2) * 100;
  document.getElementById('stepperFill').style.width = pct + '%';

  // Labels
  document.querySelectorAll('.stepper-label').forEach(el => {
    const s = parseInt(el.dataset.step);
    el.classList.remove('active', 'done');
    if (s === step) el.classList.add('active');
    if (s < step) el.classList.add('done');
  });
}

/* ── Step Navigation ── */

function goToStep(step) {
  if (step > currentStep) {
    if (currentStep === 1 && !validateStep1()) return;
    if (currentStep === 2 && !validateStep2()) return;
  }

  clearErrors();
  currentStep = step;

  // Swap visible panels
  document.querySelectorAll('.popup-step').forEach(el => el.classList.remove('active'));
  document.getElementById('step' + step).classList.add('active');

  updateStepper(step);

  // Auto-focus first input on new step
  const firstInput = document.querySelector('#step' + step + ' input:not([type="radio"])');
  if (firstInput) setTimeout(() => firstInput.focus(), 100);
}

/* ── Method Selection ── */

function selectMethod(radio) {
  document.querySelectorAll('.method-card').forEach(c => c.classList.remove('selected'));
  radio.closest('.method-card').classList.add('selected');
  document.getElementById('methodError').textContent = '';
}

/* ── Submit ── */

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

/* ── Reset ── */

function resetForm() {
  currentStep = 1;

  document.querySelectorAll('.popup-step').forEach(el => el.classList.remove('active'));
  document.getElementById('step1').classList.add('active');
  updateStepper(1);

  ['phone', 'fullName', 'street', 'city', 'zip', 'email'].forEach(id => {
    document.getElementById(id).value = '';
  });

  document.querySelectorAll('input[name="orderMethod"]').forEach(r => r.checked = false);
  document.querySelectorAll('.method-card').forEach(c => c.classList.remove('selected'));

  clearErrors();
}

/* ── Keyboard ── */

document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') closePopup();
});
