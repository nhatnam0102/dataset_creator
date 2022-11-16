# import module turtle
import turtle

# tạo màn hình
sc = turtle.Screen()
sc.title("Pong game")
sc.bgcolor("white")
sc.setup(width=1000, height=600)

# tạo cây vợt bên trái
left_pad = turtle.Turtle()
left_pad.speed(0)
left_pad.shape("square")
left_pad.color("black")
left_pad.shapesize(stretch_wid=6, stretch_len=2)
left_pad.penup()
left_pad.goto(-400, 0)

# tạo cây vợt bên phải
right_pad = turtle.Turtle()
right_pad.speed(0)
right_pad.shape("square")
right_pad.color("black")
right_pad.shapesize(stretch_wid=6, stretch_len=2)
right_pad.penup()
right_pad.goto(400, 0)

# tạo quả bóng tròn màu xanh
hit_ball = turtle.Turtle()
hit_ball.speed(100)
hit_ball.shape("circle")
hit_ball.color("blue")
hit_ball.penup()
hit_ball.goto(0, 0)
hit_ball.dx = 5
hit_ball.dy = -5

# khởi tạo điểm =0 cho 2 người chơi
left_player = 0
right_player = 0

# hiển thị điểm và V1Study
sketch = turtle.Turtle()
# hiển thị điểm
sketch.speed(0)
sketch.color("blue")
sketch.penup()
sketch.hideturtle()
sketch.goto(0, 260)
sketch.write("Left_player : 0    Right_player: 0",
             align="center", font=("Courier", 24, "normal"))

# hiển thị V1Study
sketch.color("#568000")
sketch.penup()
sketch.hideturtle()
sketch.goto(0, 200)
sketch.write("UPC",
             align="center", font=("Courier", 30, "bold"))


# các hàm di chuyển cây vợt theo chiều dọc
def paddleaup():
    y = left_pad.ycor()
    y += 20
    left_pad.sety(y)


def paddleadown():
    y = left_pad.ycor()
    y -= 20
    left_pad.sety(y)


def paddlebup():
    y = right_pad.ycor()
    y += 20
    right_pad.sety(y)


def paddlebdown():
    y = right_pad.ycor()
    y -= 20
    right_pad.sety(y)


# bắt các phím
sc.listen()
sc.onkeypress(paddleaup, "w")
sc.onkeypress(paddleadown, "s")
sc.onkeypress(paddlebup, "Up")
sc.onkeypress(paddlebdown, "Down")

# vòng lặp trò chơi
while True:
    sc.update()

    hit_ball.setx(hit_ball.xcor() + hit_ball.dx)
    hit_ball.sety(hit_ball.ycor() + hit_ball.dy)

    # kiểm tra va chạm bóng với đường biên
    if hit_ball.ycor() > 280:
        hit_ball.sety(280)
        hit_ball.dy *= -1

    if hit_ball.ycor() < -280:
        hit_ball.sety(-280)
        hit_ball.dy *= -1

    if hit_ball.xcor() > 500:
        hit_ball.goto(0, 0)
        hit_ball.dy *= -1
        left_player += 1
        sketch.clear()
        sketch.goto(0, 260)
        sketch.write("Left_player : {}    Right_player: {}".format(
            left_player, right_player), align="center",
            font=("Courier", 24, "normal"))
        # hiển thị V1Study
        sketch.color("#568000")
        sketch.penup()
        sketch.hideturtle()
        sketch.goto(0, 200)
        sketch.write("UPC",
                     align="center", font=("Courier", 30, "bold"))

    if hit_ball.xcor() < -500:
        hit_ball.goto(0, 0)
        hit_ball.dy *= -1
        right_player += 1
        sketch.clear()
        sketch.goto(0, 260)
        sketch.write("Left_player : {}    Right_player: {}".format(
            left_player, right_player), align="center",
            font=("Courier", 24, "normal"))
        # hiển thị V1Study
        sketch.color("#568000")
        sketch.penup()
        sketch.hideturtle()
        sketch.goto(0, 200)
        sketch.write("UPC",
                     align="center", font=("Courier", 30, "bold"))

    # kiểm tra va cham bóng với cây vợt
    if (360 < hit_ball.xcor() < 370) and \
            (right_pad.ycor() + 40 > hit_ball.ycor() > right_pad.ycor() - 40):
        hit_ball.setx(360)
        hit_ball.dx *= -1

    if (-360 > hit_ball.xcor() > -370) and \
            (left_pad.ycor() + 40 > hit_ball.ycor() > left_pad.ycor() - 40):
        hit_ball.setx(-360)
        hit_ball.dx *= -1
