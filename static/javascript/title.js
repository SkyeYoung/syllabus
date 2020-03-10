let leon, canvas, ctx;

const sw = 400;
const sh = 150;
const pixelRatio = 2;

function init() {
  canvas = document.querySelector('canvas');
  ctx = canvas.getContext("2d");
  
  canvas.width = sw * pixelRatio;
  canvas.height = sh * pixelRatio;
  canvas.style.width = sw + 'px';
  canvas.style.height = sh + 'px';
  ctx.scale(pixelRatio, pixelRatio);
  
  leon = new LeonSans({
    text: 'JUST\nSyllabus',
    color: ['#000000'],
    size: 80,
    weight: 100
  });
  
  requestAnimationFrame(animate);
}

function animate(t) {
  requestAnimationFrame(animate);
  
  ctx.clearRect(0, 0, sw, sh);
  
  const x = (sw - leon.rect.w) / 2;
  const y = (sh - leon.rect.h) / 2;
  leon.position(x, y);
  
  leon.draw(ctx);
}

window.onload = () => {
  init();
};