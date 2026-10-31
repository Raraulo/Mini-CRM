'use strict';
document.documentElement.classList.add('js');
// Referencias compartidas: modales, formularios y filtros.
const dialog = document.querySelector('#client-dialog');
const form = document.querySelector('#client-form');
const deleteDialog = document.querySelector('#delete-dialog');
const filters = document.querySelector('#filters');
const search = document.querySelector('#search');
const statusFilter = document.querySelector('#status-filter');
const saveButton = document.querySelector('#save-client');

// Alta y edición usan el mismo modal; se limpian valores y errores al abrir.
function openNew() {
  form.reset();
  form.action = form.dataset.createUrl;
  for (const field of form.querySelectorAll('input:not([type=hidden]), select')) {
    field.value = field.name === 'status' ? 'prospect' : '';
    field.removeAttribute('aria-invalid');
    field.setCustomValidity('');
  }
  form.querySelectorAll('.field-errors').forEach(el => { el.textContent = ''; });
  form.querySelector('.form-summary')?.remove();
  document.querySelector('#form-title').textContent = 'Nuevo cliente';
  dialog.showModal();
}
document.querySelector('#new-client').addEventListener('click', openNew);
document.querySelector('#empty-new').addEventListener('click', openNew);
// Acciones del listado: delegación para filas actualizadas por la búsqueda.
document.addEventListener('click', event => {
  const close = event.target.closest('.close-dialog');
  if (close) close.closest('dialog').close();
  const edit = event.target.closest('.edit-client');
  if (edit) {
    openNew();
    form.action = edit.dataset.url;
    document.querySelector('#form-title').textContent = 'Editar cliente';
    for (const name of ['name', 'company', 'email', 'phone', 'status']) {
      form.elements.namedItem(name).value = edit.dataset[name];
    }
  }
  const remove = event.target.closest('.delete-client');
  if (remove) {
    document.querySelector('#delete-form').action = remove.dataset.url;
    document.querySelector('#delete-name').textContent = remove.dataset.name;
    deleteDialog.showModal();
  }
});
for (const modal of [dialog, deleteDialog]) {
  modal.addEventListener('click', event => {
    if (event.target === modal) {
      const rect = modal.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) modal.close();
    }
  });
}
// Validación en el navegador antes del envío; Django vuelve a validar al recibir.
const phone = form.elements.namedItem('phone');
const nameField = form.elements.namedItem('name');
function validateName() {
  const value = nameField.value.trim();
  nameField.setCustomValidity(value && /\p{L}/u.test(value) && /^[\p{L}\p{M} '\u2019-]+$/u.test(value)
    ? '' : 'Escribe un nombre con letras, sin números ni símbolos.');
}
function validatePhone() {
  phone.setCustomValidity(!phone.value.trim() || /^\+?[0-9][0-9 ()-]{5,28}[0-9]$/.test(phone.value.trim())
    ? '' : 'Ingresa un teléfono sin letras, de 7 a 30 caracteres.');
}
phone.addEventListener('input', validatePhone);
nameField.addEventListener('input', validateName);
form.addEventListener('submit', event => {
  nameField.value = nameField.value.trim();
  phone.value = phone.value.trim();
  validateName();
  validatePhone();
  if (!form.reportValidity()) { event.preventDefault(); return; }
  saveButton.disabled = true;
  saveButton.textContent = 'Guardando…';
});
document.querySelector('#delete-form').addEventListener('submit', event => {
  const button = event.currentTarget.querySelector('[type=submit]');
  button.disabled = true;
  button.textContent = 'Eliminando…';
});
if (dialog.dataset.reopen) dialog.showModal();

// Búsqueda dinámica: espera breve y cancelación de solicitudes anteriores.
let timer;
let controller;
let requestId = 0;
async function filterClients() {
  const id = ++requestId;
  controller?.abort();
  controller = new AbortController();
  const url = new URL(filters.action || location.href);
  url.pathname = '/clients/';
  url.search = new URLSearchParams(new FormData(filters)).toString();
  document.querySelector('.directory').setAttribute('aria-busy', 'true');
  try {
    const response = await fetch(url, { signal: controller.signal });
    if (response.redirected && new URL(response.url).pathname === '/login/') {
      location.assign(response.url);
      return;
    }
    if (!response.ok) throw new Error('request');
    const page = new DOMParser().parseFromString(await response.text(), 'text/html');
    if (id !== requestId) return;
    document.querySelector('#client-rows').replaceChildren(...page.querySelector('#client-rows').childNodes);
    const incomingEmpty = page.querySelector('#empty-state');
    const empty = document.querySelector('#empty-state');
    empty.hidden = incomingEmpty.hidden;
    empty.querySelector('h3').textContent = incomingEmpty.querySelector('h3').textContent;
    document.querySelector('#results').textContent = page.querySelector('#results').textContent;
    history.replaceState(null, '', url);
  } catch (error) {
    if (error.name !== 'AbortError') showToast('No se pudo actualizar la lista. Intenta buscar de nuevo.', true);
  } finally {
    if (id === requestId) document.querySelector('.directory').removeAttribute('aria-busy');
  }
}
filters.addEventListener('submit', event => { event.preventDefault(); clearTimeout(timer); filterClients(); });
search.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(filterClients, 280); });
statusFilter.addEventListener('change', () => { clearTimeout(timer); filterClients(); });
document.querySelector('#clear-filters').addEventListener('click', () => { search.value = ''; statusFilter.value = ''; clearTimeout(timer); filterClients(); });
document.addEventListener('keydown', event => {
  if (event.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName) && !document.querySelector('dialog[open]')) { event.preventDefault(); search.focus(); }
});
// Notificaciones con Lottie y cierre automático después de cuatro segundos.
function activateToast(toast) {
  const container = toast.querySelector('.toast-lottie');
  const animation = container && window.lottie ? window.lottie.loadAnimation({
    container, renderer: 'svg', loop: false,
    autoplay: !window.matchMedia('(prefers-reduced-motion: reduce)').matches,
    path: container.dataset.animationUrl,
  }) : null;
  animation?.setSpeed(0.75);
  const dismiss = () => { animation?.destroy(); toast.remove(); };
  const timeout = setTimeout(dismiss, 4000);
  toast.querySelector('button').addEventListener('click', () => { clearTimeout(timeout); dismiss(); });
}
function showToast(message, error = false) {
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.setAttribute('role', error ? 'alert' : 'status');
  const icon = document.createElement('span');
  icon.textContent = error ? '!' : '✓';
  const text = document.createTextNode(message);
  const close = document.createElement('button');
  close.type = 'button'; close.textContent = '×'; close.setAttribute('aria-label', 'Cerrar notificación');
  toast.append(icon, text, close);
  document.querySelector('.toasts').append(toast);
  activateToast(toast);
}
document.querySelectorAll('.toast').forEach(activateToast);
// Al volver atrás se comprueba la sesión y se restablecen los botones.
window.addEventListener('pageshow', event => {
  if (event.persisted) {
    location.reload();
    return;
  }
  saveButton.disabled = false; saveButton.textContent = 'Guardar cliente';
  const button = document.querySelector('#delete-form [type=submit]');
  button.disabled = false; button.textContent = 'Sí, eliminar';
});

// Navegacion y metricas comparten la misma animacion al interactuar.
if (window.lottie) {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('.nav-lottie, .metric-lottie').forEach(container => {
    const link = container.closest('a, .metric');
    const animation = window.lottie.loadAnimation({
      container, renderer: 'svg', loop: true, autoplay: false,
      path: container.dataset.animationUrl,
    });
    animation.setSpeed(0.65);
    const play = () => { if (!reducedMotion.matches) animation.play(); };
    const stop = () => {
      if (!link.matches(':hover') && !link.matches(':focus-visible')) animation.goToAndStop(0, true);
    };
    link.addEventListener('pointerenter', play);
    link.addEventListener('pointerleave', stop);
    link.addEventListener('focus', play);
    link.addEventListener('blur', stop);
    reducedMotion.addEventListener('change', event => {
      if (event.matches) animation.goToAndStop(0, true);
    });
  });
}


// Panel desplegable de estadísticas: los gráficos se dibujan al abrirlo.
const insightsToggle = document.querySelector('#toggle-insights');
let chartsRendered = false;
insightsToggle.addEventListener('click', () => {
  const panel = document.querySelector('#insights');
  panel.hidden = !panel.hidden;
  insightsToggle.setAttribute('aria-expanded', String(!panel.hidden));
  insightsToggle.firstChild.textContent = panel.hidden ? 'Ver más ' : 'Ver menos ';
  insightsToggle.querySelector('span').textContent = panel.hidden ? '＋' : '−';
  if (!panel.hidden && !chartsRendered) { renderInsights(); chartsRendered = true; }
});
// Dona de estados y línea de registros construidas con los datos de Django.
function renderInsights() {
  const data = JSON.parse(document.querySelector('#chart-data').textContent);
  const colors = ['#4d3f01', '#d5ad55', '#0b7cf6'];
  const labels = ['Activos', 'Prospectos', 'Inactivos'];
  const total = data.statuses.reduce((sum, value) => sum + value, 0);
  let cursor = 0;
  const segments = data.statuses.map((value, i) => {
    const start = cursor;
    cursor += total ? value / total * 100 : 0;
    return `${colors[i]} ${start}% ${cursor}%`;
  });
  const donut = document.querySelector('#status-donut');
  donut.style.background = total ? `conic-gradient(${segments.join(',')})` : '#e8edeb';
  donut.setAttribute('aria-label', total ? labels.map((label, i) => `${label}: ${data.statuses[i]}`).join(', ') : 'Todavía no hay contactos');
  const legend = document.querySelector('#chart-legend');
  data.statuses.forEach((value, i) => {
    const item = document.createElement('li');
    const dot = document.createElement('i'); dot.style.background = colors[i];
    const name = document.createElement('span'); name.textContent = labels[i];
    const count = document.createElement('strong'); count.textContent = value;
    const percent = document.createElement('small'); percent.textContent = `${total ? Math.round(value / total * 100) : 0}%`;
    item.append(dot, name, count, percent); legend.append(item);
  });
  const days = data.days;
  const maximum = Math.max(1, ...days.map(day => day.count));
  const ceiling = Math.ceil(maximum / 4) * 4;
  const svgNS = 'http://www.w3.org/2000/svg';
  function node(tag, attrs = {}, content) {
    const element = document.createElementNS(svgNS, tag);
    Object.entries(attrs).forEach(([name, value]) => element.setAttribute(name, value));
    if (content !== undefined) element.textContent = content;
    return element;
  }
  const svg = node('svg', { viewBox: '0 0 500 250', role: 'img', 'aria-labelledby': 'line-title line-description' });
  const sum = days.reduce((sum, day) => sum + day.count, 0);
  svg.append(node('title', {id: 'line-title'}, 'Contactos registrados por día'), node('desc', {id: 'line-description'}, `${sum} registros en los últimos 30 días. Incluye solo contactos que siguen guardados.`));
  const x = i => 36 + i / 29 * 450;
  const y = count => 208 - count / ceiling * 180;
  for (let i = 0; i <= 4; i++) {
    const value = ceiling * i / 4;
    svg.append(node('line', {x1:36, x2:486, y1:y(value), y2:y(value), stroke:'#edf0ed', 'stroke-dasharray':'4 5'}));
    svg.append(node('text', {x:24, y:y(value)+4, 'text-anchor':'end', fill:'#8b9690', 'font-size':11}, value));
  }
  const points = days.map((day, i) => `${x(i)},${y(day.count)}`).join(' ');
  svg.append(node('polygon', {points:`36,208 ${points} 486,208`, fill:'#e68e6e', opacity:'.1'}));
  svg.append(node('polyline', {points, fill:'none', stroke:'#cf7758', 'stroke-width':2.5, 'stroke-linejoin':'round'}));
  days.forEach((day, i) => {
    const label = new Date(`${day.date}T12:00:00`).toLocaleDateString('es-EC', {day:'numeric', month:'short'});
    const point = node('circle', {cx:x(i), cy:y(day.count), r:4, fill:'#e68e6e', stroke:'white', 'stroke-width':1.5});
    point.append(node('title', {}, `${label}: ${day.count} contactos`)); svg.append(point);
    if ([0, 7, 14, 21, 29].includes(i)) svg.append(node('text', {x:x(i), y:234, 'text-anchor':i === 29 ? 'end' : 'middle', fill:'#8b9690', 'font-size':10}, label));
  });
  document.querySelector('#registrations-chart').append(svg);
  document.querySelector('#chart-note').textContent = `${sum} registros en este período.`;
}

