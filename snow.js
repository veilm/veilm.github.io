/*
1751763776 sucralose: right now the fade-in logic was originally meant to just
be for the snowflakes spawning at the top, but  I ese it's being applied to all
at once when you first load the page. but actually this looks quite good so I
think we'll keep it as intended behaviour
*/

const canvas = document.getElementById("snow");

const ctx = canvas.getContext("2d");
let lastTime = 0;
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
    const maxOpacity = Math.random() * 0.5 + 0.5; // 0.5–1 opacity for depth effect
    flakes.push({
      x: Math.random() * width,
      y: Math.random() * height,
      r: Math.random() * 3 + 1,       // radius 1–4 px
      speedY: Math.random() * 1 + 0.5, // fall speed
      drift: Math.random() * 0.5 - 0.25, // horizontal drift
      opacity: maxOpacity,
      maxOpacity: maxOpacity,
      isResting: false,
      restStartTime: 0,

      meltTimeout: Math.random() * 3000 + 2000, // 2-5 seconds
      groundLevel: height - (Math.random() * 20 + 5),
      spawnTime: Date.now(),
    });
  }
}
initFlakes();

function update() {

  for (const f of flakes) {
    if (f.isResting) {
      const elapsed = Date.now() - f.restStartTime;
      if (elapsed > f.meltTimeout) {

        // Flake has melted, respawn it at the top
        f.x = Math.random() * width;
        f.y = -f.r;
        f.isResting = false;
        f.spawnTime = Date.now();
      } else {
        // Fade out as it melts
        f.opacity = f.maxOpacity * (1 - elapsed / f.meltTimeout);
      }

    } else {
      const timeSinceSpawn = Date.now() - f.spawnTime;
      const fadeInDuration = 1000; // 1 second
      if (timeSinceSpawn < fadeInDuration) {
          f.opacity = f.maxOpacity * (timeSinceSpawn / fadeInDuration);
      } else {
          f.opacity = f.maxOpacity;
      }
      // Flake is falling
      f.y += f.speedY;
      f.x += f.drift;
      // gentle sway effect
      f.drift += Math.sin(Date.now() / 10000 + f.y) * 0.001;


      // Check for landing on the ground
      if (f.y > f.groundLevel) {
        f.isResting = true;
        f.restStartTime = Date.now();
      }

      // Wrap horizontally
      if (f.x > width) f.x = 0;
      if (f.x < 0) f.x = width;
    }
  }
}


function draw() {
  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = "#fff";
  for (const f of flakes) {
    ctx.beginPath();
    ctx.globalAlpha = f.opacity;
    ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.globalAlpha = 1;
}


function loop(currentTime = 0) {
  if (!lastTime) {
    lastTime = currentTime;
  }
  const deltaTime = currentTime - lastTime;

  // If the tab was inactive for a while, reset the snowflakes
  if (deltaTime > 1000) {
    initFlakes();
  }

  update();
  draw();

  lastTime = currentTime;
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop); // Start the animation
