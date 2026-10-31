'use strict';
// Lottie de error: reproducción lenta y pausa si la pestaña está oculta.
const container = document.querySelector('#error-animation');
if (container && window.lottie) {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const animation = window.lottie.loadAnimation({
    container, renderer: 'svg', loop: true, autoplay: !reducedMotion.matches,
    path: container.dataset.animationUrl,
  });
  animation.setSpeed(0.5);
  function updatePlayback() {
    if (document.hidden || reducedMotion.matches) animation.pause();
    else animation.play();
  }
  reducedMotion.addEventListener('change', updatePlayback);
  document.addEventListener('visibilitychange', updatePlayback);
}
