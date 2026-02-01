const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const scoreLeftEl = document.getElementById("score-left");
const scoreRightEl = document.getElementById("score-right");
const statusEl = document.getElementById("status");
const startButton = document.getElementById("start");

const keysPressed = new Set();

const game = {
  width: canvas.width,
  height: canvas.height,
  running: false,
  serving: true,
  serveTimer: 0,
  serveDelay: 1.2,
  winningScore: 11,
};

const paddleConfig = {
  width: 14,
  height: 90,
  padding: 24,
  speed: 360,
};

const leftPaddle = {
  x: paddleConfig.padding,
  y: game.height / 2 - paddleConfig.height / 2,
  width: paddleConfig.width,
  height: paddleConfig.height,
  speed: paddleConfig.speed,
  dy: 0,
};

const rightPaddle = {
  x: game.width - paddleConfig.padding - paddleConfig.width,
  y: game.height / 2 - paddleConfig.height / 2,
  width: paddleConfig.width,
  height: paddleConfig.height,
  speed: paddleConfig.speed,
  dy: 0,
};

const ball = {
  x: game.width / 2,
  y: game.height / 2,
  radius: 9,
  speed: 320,
  maxSpeed: 520,
  vx: 0,
  vy: 0,
};

const score = {
  left: 0,
  right: 0,
};

const maxBounceAngle = Math.PI / 3;

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function resetPaddles() {
  leftPaddle.y = game.height / 2 - leftPaddle.height / 2;
  rightPaddle.y = game.height / 2 - rightPaddle.height / 2;
}

function resetBall(randomServe = true) {
  ball.x = game.width / 2;
  ball.y = game.height / 2;
  ball.speed = 320;

  const direction = randomServe ? (Math.random() > 0.5 ? 1 : -1) : 1;
  const angle = (Math.random() * 0.5 - 0.25) * Math.PI;
  ball.vx = direction * ball.speed * Math.cos(angle);
  ball.vy = ball.speed * Math.sin(angle);
}

function setStatus(message) {
  statusEl.textContent = message;
}

function updateScore() {
  scoreLeftEl.textContent = score.left;
  scoreRightEl.textContent = score.right;
}

function startGame() {
  if (score.left >= game.winningScore || score.right >= game.winningScore) {
    score.left = 0;
    score.right = 0;
    updateScore();
  }

  game.running = true;
  game.serving = true;
  game.serveTimer = 0;
  resetPaddles();
  resetBall();
  setStatus("Serve incoming...");
}

function stopGame(message) {
  game.running = false;
  game.serving = true;
  setStatus(message);
}

function handleInput() {
  const leftUp = keysPressed.has("w") || keysPressed.has("W");
  const leftDown = keysPressed.has("s") || keysPressed.has("S");
  const rightUp = keysPressed.has("ArrowUp");
  const rightDown = keysPressed.has("ArrowDown");

  leftPaddle.dy = (leftDown ? 1 : 0) + (leftUp ? -1 : 0);
  rightPaddle.dy = (rightDown ? 1 : 0) + (rightUp ? -1 : 0);
}

function updatePaddles(dt) {
  leftPaddle.y += leftPaddle.dy * leftPaddle.speed * dt;
  rightPaddle.y += rightPaddle.dy * rightPaddle.speed * dt;

  leftPaddle.y = clamp(leftPaddle.y, 0, game.height - leftPaddle.height);
  rightPaddle.y = clamp(rightPaddle.y, 0, game.height - rightPaddle.height);
}

function paddleCollision(paddle, direction) {
  const relativeIntersect =
    (ball.y - (paddle.y + paddle.height / 2)) / (paddle.height / 2);
  const clampedIntersect = clamp(relativeIntersect, -1, 1);
  const bounceAngle = clampedIntersect * maxBounceAngle;

  ball.speed = Math.min(ball.speed + 10, ball.maxSpeed);
  ball.vx = direction * ball.speed * Math.cos(bounceAngle);
  ball.vy = ball.speed * Math.sin(bounceAngle);
}

function updateBall(dt) {
  if (game.serving) {
    game.serveTimer += dt;
    if (game.serveTimer >= game.serveDelay) {
      game.serving = false;
      setStatus("");
    }
    return;
  }

  ball.x += ball.vx * dt;
  ball.y += ball.vy * dt;

  if (ball.y - ball.radius <= 0) {
    ball.y = ball.radius;
    ball.vy *= -1;
  }

  if (ball.y + ball.radius >= game.height) {
    ball.y = game.height - ball.radius;
    ball.vy *= -1;
  }

  const hitLeft =
    ball.x - ball.radius <= leftPaddle.x + leftPaddle.width &&
    ball.x + ball.radius >= leftPaddle.x &&
    ball.y + ball.radius >= leftPaddle.y &&
    ball.y - ball.radius <= leftPaddle.y + leftPaddle.height;

  if (hitLeft && ball.vx < 0) {
    ball.x = leftPaddle.x + leftPaddle.width + ball.radius;
    paddleCollision(leftPaddle, 1);
  }

  const hitRight =
    ball.x + ball.radius >= rightPaddle.x &&
    ball.x - ball.radius <= rightPaddle.x + rightPaddle.width &&
    ball.y + ball.radius >= rightPaddle.y &&
    ball.y - ball.radius <= rightPaddle.y + rightPaddle.height;

  if (hitRight && ball.vx > 0) {
    ball.x = rightPaddle.x - ball.radius;
    paddleCollision(rightPaddle, -1);
  }

  if (ball.x + ball.radius < 0) {
    score.right += 1;
    updateScore();
    game.serving = true;
    game.serveTimer = 0;
    resetBall();
    setStatus("Point for Right Player!");
  }

  if (ball.x - ball.radius > game.width) {
    score.left += 1;
    updateScore();
    game.serving = true;
    game.serveTimer = 0;
    resetBall();
    setStatus("Point for Left Player!");
  }
}

function checkWin() {
  if (score.left >= game.winningScore) {
    stopGame("Left Player wins! Press Start or Space to play again.");
  }

  if (score.right >= game.winningScore) {
    stopGame("Right Player wins! Press Start or Space to play again.");
  }
}

function drawCenterLine() {
  ctx.strokeStyle = "#1f2a44";
  ctx.setLineDash([10, 16]);
  ctx.beginPath();
  ctx.moveTo(game.width / 2, 0);
  ctx.lineTo(game.width / 2, game.height);
  ctx.stroke();
  ctx.setLineDash([]);
}

function draw() {
  ctx.clearRect(0, 0, game.width, game.height);

  drawCenterLine();

  ctx.fillStyle = "#f5f7ff";
  ctx.fillRect(
    leftPaddle.x,
    leftPaddle.y,
    leftPaddle.width,
    leftPaddle.height
  );
  ctx.fillRect(
    rightPaddle.x,
    rightPaddle.y,
    rightPaddle.width,
    rightPaddle.height
  );

  ctx.beginPath();
  ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
  ctx.fill();
}

let lastTime = 0;

function gameLoop(timestamp) {
  if (!lastTime) lastTime = timestamp;
  const dt = (timestamp - lastTime) / 1000;
  lastTime = timestamp;

  if (game.running) {
    handleInput();
    updatePaddles(dt);
    updateBall(dt);
    checkWin();
  }

  draw();
  requestAnimationFrame(gameLoop);
}

document.addEventListener("keydown", (event) => {
  keysPressed.add(event.key);

  if (event.key === " " || event.code === "Space") {
    if (!game.running) {
      startGame();
    }
  }
});

document.addEventListener("keyup", (event) => {
  keysPressed.delete(event.key);
});

startButton.addEventListener("click", () => {
  if (!game.running) {
    startGame();
  }
});

resetBall();
setStatus("Press Start or Space to begin.");
requestAnimationFrame(gameLoop);
