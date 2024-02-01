import pygame
import sys
pygame.init()


WHITE = (255,255,255)
WIDTH, HEIGHT = 700,500
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
right_paddle_x = WIDTH - 20
left_paddle_x = 10
right_paddle_y = HEIGHT// 2 - 10
left_paddle_y = HEIGHT// 2 - 10
left_paddle_width = 10
right_paddle_width = 10
left_paddle_height = 100
right_paddle_height = 100
original_ball_x = WIDTH//2 
original_ball_y = HEIGHT//2
ball_radius = 7


WINNING_FONT = pygame.font.SysFont('arial.ttf', 35)
winning_score = 10

class Paddle:
    VEL = 5



    
    def __init__(self,x,y,width,height,color):
        self.x = self.original_x = x
        self.y = self.original_y =  y
        self.width = width
        self.height = height
        self.color = color



    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y




class Ball:
    MAX_VEL = 5

    
    def __init__(self,x,y,radius,color):
        self.x = self.original_x =  x
        self.y = self.original_y = y
        self.radius = radius
        self.color = color
        self.x_vel = self.MAX_VEL
        self.y_vel = 0


    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x,self.y),self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= 1



def draw(win, paddles, ball, left_score, right_score):
    
        win.fill((0,0,0))
        left_score_text = WINNING_FONT.render(f"{left_score}", 1, WHITE)
        right_score_text = WINNING_FONT.render(f"{right_score}", 1, WHITE)
        win.blit(left_score_text, (WIDTH // 4 , 10))
        win.blit(right_score_text, (WIDTH * 3//4, 10))
        


        pygame.draw.rect(win, WHITE, (WIDTH/2 - 15,0, 15, HEIGHT))

        for paddle in paddles:
            paddle.draw(win)

        ball.draw(win)
        pygame.display.update()


def handle_events(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.height + left_paddle.VEL <= HEIGHT:
        left_paddle.move(up=False)


    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle_height <= HEIGHT:
        right_paddle.move(up=False)


def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y 
                reduction_factor = (left_paddle.height / 2)  / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y =  middle_y - ball.y 
                reduction_factor = (right_paddle.height / 2)  / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
               



def main():
    running = True
    right_paddle = Paddle(right_paddle_x,right_paddle_y,right_paddle_width,right_paddle_height,WHITE)
    left_paddle = Paddle(left_paddle_x,left_paddle_y,left_paddle_width,left_paddle_height,WHITE)
    

    paddles = [left_paddle,right_paddle]

    ball = Ball(WIDTH // 2,HEIGHT // 2,ball_radius,WHITE)
    left_score = 0
    right_score = 0

    while running:
        draw(win, paddles, ball, left_score, right_score)

       
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break


        keys = pygame.key.get_pressed()
        handle_events(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)


        if ball.x < 0:
            right_score += 1
            ball.reset()
        if ball.x > WIDTH:
            left_score += 1
            ball.reset()


        won = False
        if left_score >= winning_score:
            won = True
            win_text = "LEFT WINS"
        if right_score >= winning_score:
            won = True
            win_text = "RIGHT WINS"


        if won:
            won_text = WINNING_FONT.render(win_text, 1, WHITE)
            win.blit(won_text, (WIDTH // 2 - won_text.get_width() // 2, HEIGHT // 2 - won_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

        pygame.display.update()

        clock.tick(60)


        




    pygame.quit()

def main_menu():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            main()

        win.fill((0,0,0))
        begin_text = "Enter Space To Begin"

        begin = WINNING_FONT.render(begin_text, 1, WHITE)
        win.blit(begin, (WIDTH // 2 - begin.get_width() // 2,HEIGHT // 2 - begin.get_height() // 2))

        pygame.display.update()

        clock.tick(60)

    pygame.quit()



main_menu()
