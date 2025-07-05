const canvas = document.getElementById("snow");
const ctx = canvas.getContext("2d");
let width, height;

function resize() {
  width = canvas.width = window.innerWidth;
  height = canvas.height = window.innerHeight;
}
window.addEventListener("resize", resize);
resize();

// Particle setup
const flakes = [];
const maxParticles = Math.floor((width * height) / 8000); // adaptive density

function initFlakes() {
  flakes.length = 0;
  for (let i = 0; i < maxParticles; i++) {
    flakes.push({
      x: Math.random() * width,
      y: Math.random() * height,
      r: Math.random() * 3 + 1,       // radius 1–4 px
      speedY: Math.random() * 1 + 0.5, // fall speed
      drift: Math.random() * 0.5 - 0.25, // horizontal drift
      opacity: Math.random() * 0.5 + 0.5 // 0.5–1 opacity for depth effect
    });
  }
}
initFlakes();

function update() {
  for (const f of flakes) {
    f.y += f.speedY;
    f.x += f.drift;
    // gentle sway effect
    f.drift += Math.sin(Date.now() / 10000 + f.y) * 0.001;

    // respawn at top when out of view
    if (f.y > height) {
      f.y = -f.r;
      f.x = Math.random() * width;
    }
    if (f.x > width) f.x = 0;
    if (f.x < 0) f.x = width;
  }
}

function draw() {
  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = "#fff";
  ctx.beginPath();
  for (const f of flakes) {
    ctx.globalAlpha = f.opacity;
    ctx.moveTo(f.x, f.y);
    ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2);
  }
  ctx.fill();
  ctx.globalAlpha = 1;
}

function loop() {
  update();
  draw();
  requestAnimationFrame(loop);
}
loop();
