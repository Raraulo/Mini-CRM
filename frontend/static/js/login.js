'use strict';
// Bloqueo temporal del botón para evitar envíos repetidos.
const loginForm = document.querySelector('#login-form');
loginForm.addEventListener('submit', () => {
  const button = loginForm.querySelector('[type=submit]');
  button.disabled = true;
  button.textContent = 'Iniciando sesión…';
});
window.addEventListener('pageshow', () => {
  const button = loginForm.querySelector('[type=submit]');
  button.disabled = false;
  button.textContent = 'Entrar a mi espacio';
});

// Ilustración del login: autoplay lento y respeto a movimiento reducido.
const sunflower = document.querySelector('#sunflower-animation');
if (sunflower && window.lottie) {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const animation = window.lottie.loadAnimation({
    container: sunflower,
    renderer: 'svg',
    loop: true,
    autoplay: !reducedMotion.matches,
    path: sunflower.dataset.animationUrl,
    rendererSettings: { preserveAspectRatio: 'xMidYMid meet' },
  });
  animation.setSpeed(0.5);
  reducedMotion.addEventListener('change', event => {
    if (event.matches) animation.pause();
    else animation.play();
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden || reducedMotion.matches) animation.pause();
    else animation.play();
  });
}

// Alterna la visibilidad de la contraseña y actualiza su etiqueta accesible.
const passwordInput = document.querySelector('#id_password');
const passwordToggle = document.querySelector('.password-toggle');
passwordToggle.addEventListener('click', () => {
  const visible = passwordInput.type === 'password';
  passwordInput.type = visible ? 'text' : 'password';
  passwordToggle.setAttribute('aria-label', visible ? 'Ocultar contraseña' : 'Mostrar contraseña');
  passwordToggle.setAttribute('aria-pressed', String(visible));
  passwordToggle.querySelector('.eye-open').hidden = visible;
  passwordToggle.querySelector('.eye-closed').hidden = !visible;
});

