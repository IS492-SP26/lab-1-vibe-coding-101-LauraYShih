import turtle
import os

# Set up the screen
wn = turtle.Screen()
wn.title("Pong by @GitHub_Copilot")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)  # Stops the window from updating, speeds up the game

# Score
score_a = 0
score_b = 0

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0) # Animation speed, not movement speed
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 2  # Change in x (speed)
ball.dy = 2  # Change in y (speed)

# Pen (Scoreboard)
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

# Function to move Paddle A up
def paddle_a_up():
    y = paddle_a.ycor()
    if y < 250: # boundary check
        y += 20
        paddle_a.sety(y)

# Function to move Paddle A down
def paddle_a_down():
    y = paddle_a.ycor()
    if y > -240: # boundary check
        y -= 20
        paddle_a.sety(y)

# Function to move Paddle B up
def paddle_b_up():
    y = paddle_b.ycor()
    if y < 250:
        y += 20
        paddle_b.sety(y)

# Function to move Paddle B down
def paddle_b_down():
    y = paddle_b.ycor()
    if y > -240:
        y -= 20
        paddle_b.sety(y)

# Keyboard binding
wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")

# Main game loop
while True:
    wn.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border checking

    # Top boundary
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
        # Optional: Sound effect
        # os.system("afplay bounce.wav&")

    # Bottom boundary
    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    # Right boundary (scoring for Player A)
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

    # Left boundary (scoring for Player B)
    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

    # Paddle and Ball Collisions
    # Collision with Paddle B
    if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddle_b.ycor() + 40 and ball.ycor() > paddle_b.ycor() - 40):
        ball.setx(340)
        ball.dx *= -1

    # Collision with Paddle A
    if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddle_a.ycor() + 40 and ball.ycor() > paddle_a.ycor() - 40):
        ball.setx(-340)
        ball.dx *= -1