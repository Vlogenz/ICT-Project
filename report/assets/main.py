from turtle import Turtle, Screen
from random import randint,choice

tim = Turtle()
tim.shape("turtle")
tim.color("green")
tim.pendown()
def drawShapes():
    """Really nice Docstring"""
    for shape in range(3,11):
        tim.pencolor(randint(0,255)/255,randint(0,255)/255,randint(0,255)/255)
        turn = ((shape-2)*180)/shape
        print(turn)
        print(shape)
        for j in range(shape):
            tim.forward(100)
            tim.left(180-turn)


def randomWalk(num):
    tim.speed(0)
    tim.pensize(10)
    for i in range(num):
        tim.pencolor(randint(0,255)/255,randint(0,255)/255,randint(0,255)/255)
        tim.setheading(choice([0,90,180,270]))
        tim.forward(30)


def circles():
    tim.speed(0)
    for i in range(150):
        tim.pencolor(randint(0,255)/255,randint(0,255)/255,randint(0,255)/255)
        tim.circle(300)
        tim.setheading(tim.heading()+360/150)



circles()





screen = Screen()
screen.exitonclick()
