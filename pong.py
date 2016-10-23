import pygame, sys, random
import math
from datetime import datetime
from operator import add
from operator import mul

def disp_title_screen(screen, width, height):
	white = (255, 255, 255)
	black = (0, 0, 0)
	t_font = pygame.font.SysFont(pygame.font.get_default_font(), 50)
	st_font = pygame.font.SysFont(pygame.font.get_default_font(), 36)
	play = 0
	quit = 0
	
	#Title
	title = t_font.render("Welcome to a pong game", 1, white)
	title_rect = title.get_rect()
	title_rect.center = [width/2, 2*height/5]
	
	#Play
	pl_po = st_font.render("PLAY", 1, white)
	pl_po_rect = pl_po.get_rect()
	pl_po_rect.center = [width/2, 3*height/5]
	
	#Quit
	qu_po = st_font.render("QUIT", 1, white)
	qu_po_rect = qu_po.get_rect()
	qu_po_rect.center = [width/2, 4*height/5]
	
	screen.fill(black)
	screen.blit(title, title_rect)
	screen.blit(pl_po, pl_po_rect)
	screen.blit(qu_po, qu_po_rect)
	pygame.display.flip()
	
	while 1:
		for event in pygame.event.get():
			if event.type is pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if pl_po_rect.collidepoint(event.pos):
					play = 1
				elif qu_po_rect.collidepoint(event.pos):
					quit = 1
		if play:
			return 1
		elif quit:
			return 0

#Bug when renormalizing vectors
def bounce(player, ball, speed):
	o = (player.centerx - ball.centerx)/player.h
	print(o)
	a = math.cos(math.asin(o))
	speed = list(map(add, speed, (a, o)))
	return speed

def calc_traj(angle):
	x = 4*math.cos(math.radians(angle))
	y = 4*math.sin(math.radians(angle))
	return [x, y]

def calc_new_traj(random, range):
	x = 0
	y = 0
	while int(x) is 0 or int(y) is 0 or math.fabs(int(x)/4) is 1 or math.fabs(int(y)/4) is 1:
		z = random.randrange(range[0], range[1], 1)
		x = 4*math.cos(math.radians(z))
		y = 4*math.sin(math.radians(z))
	
	return [x, y]
	
def driver(basepath, screen, width, height):
	#General vars used more than once
	black = 0, 0, 0
	white = 255, 255, 255
	speed = [3, 3]
	player = [31, 160]
	ball_init_pos = []
	p1_u = 0
	p1_d = 0
	p2_u = 0
	p2_d = 0
	
	#Initialize players
	pl_img = pygame.image.load(basepath+"player.png").convert()
	p1 = pl_img.get_rect()
	p1_init_pos = p1.x, p1.y = [p1.w, height/2 - p1.h/2]
	p1_score = 0
	p2 = pl_img.get_rect()
	p2_init_pos = p2.x, p2.y =  [width - 2*p2.w, height/2 - p2.h/2]
	p2_score = 0
	
	#Initialize ball
	ball = pygame.image.load(basepath+"new_ball.bmp").convert()
	ballrect = ball.get_rect()
	ball_init_pos = [width / 2 - ballrect.w / 2, height /2 + ballrect.h /2]
	ballrect.left = ball_init_pos[0]
	ballrect.top = ball_init_pos[1]
	
	#Initialize ball trajector
	random.seed(datetime.now())
	speed = calc_new_traj(random, (0, 359))
	
	#Initialize context
	font = pygame.font.SysFont(pygame.font.get_default_font(), 36)
	p1_show = font.render("Player 1", 1, white)
	p1_inst = font.render("[w|s] = [up|down]", 1, white)
	
	p2_show = font.render("Player 2", 1, white)
	p2_inst = font.render("up down arrow keys", 1, white)
	
	p1_s_text_pos = p1_show.get_rect()
	p2_s_text_pos = p2_show.get_rect()
	
	p1_inst_rect = p1_inst.get_rect()
	p2_inst_rect = p2_inst.get_rect()
	
	p1_s_text_pos.centerx = width / 4
	p1_inst_rect.centerx = p1_s_text_pos.centerx
	p1_s_text_pos.top = 240
	p1_inst_rect.top = 300
	
	p2_s_text_pos.left = 3 * width / 4
	p2_inst_rect.centerx = p2_s_text_pos.centerx
	p2_s_text_pos.top = 240
	p2_inst_rect.top = 300
	
	#Initialize scoreboard
	p1_score_pos = [100, 50]
	p2_score_pos = [width/2+100, 50]
	score0 = font.render("0", 1, white)
	score1 = font.render("1", 1, white)
	score2 = font.render("2", 1, white)
	score3 = font.render("3", 1, white)
	score4 = font.render("4", 1, white)
	score5 = font.render("5", 1, white)
	scores = [score0, score1, score2, score3, score4, score5]
	
	iter = 0
	#Go for 5 score
	while p1_score < 5 and p2_score < 5:
		#Let player read
		if iter == 1:
			pygame.time.delay(5000)
		
		#Check for movement command
		for event in pygame.event.get():
				#Exit if quit
				if event.type is pygame.QUIT:
					sys.exit()
				
				#If player let go of a key, set bool change_pos to 0
				if event.type is pygame.KEYUP:
					a = pygame.key.name(event.key)
					if a == "w":
						p1_u = 0
					if a == "s":
						p1_d = 0
					if a == "up":
						p2_u = 0
					if a == "down":
						p2_d = 0
				
				#If player pushed a key, set bool change_pos to 1
				if event.type is pygame.KEYDOWN:
					a = pygame.key.name(event.key)
					if a == "w" and p1.top -5 >= 0:
						p1_u = 1
					if a == "s" and p1.bottom +5 <= height:
						p1_d = 1
					if a == "up" and p2.top -5 >= 0:
						p2_u = 1
					if a == "down" and p2.bottom +5 <= height:
						p2_d = 1
		
		#Check if either player needs to move
		#If player has not let up on the key and they can still move
		if p1_u and p1.top -5 >= 0:
			p1 = p1.move([0, -5])
		if p1_d and p1.bottom +5 <= height:
			p1 = p1.move([0, 5])
		if p2_u and p2.top -5 >= 0:
			p2 = p2.move([0, -5])
		if p2_d and p2.bottom +5 <= height:
			p2 = p2.move([0, 5])
		
		#Check the ball
		if ballrect.left < 0:
			p2_score += 1
			pygame.time.delay(300)
			ballrect.left = ball_init_pos[0]
			ballrect.top = ball_init_pos[1]
			speed = calc_new_traj(random, (0, 359))
		if ballrect.right > width:
			p1_score += 1
			pygame.time.delay(300)
			ballrect.left = ball_init_pos[0]
			ballrect.top = ball_init_pos[1]
			speed = calc_new_traj(random, (0, 359))
		if ballrect.top < 0 or ballrect.bottom > height:
			speed[1] = -speed[1]
		
		#Simple collision detection is not enough, we must define explicitly
		if p1.right > ballrect.x or p2.left < ballrect.x+ballrect.width:
			if p1.collidepoint(ballrect.topleft) or p1.collidepoint(ballrect.bottomleft):
				speed = bounce(p1, ballrect, speed)
			if p2.collidepoint(ballrect.topright) or p2.collidepoint(ballrect.bottomright):
				temp = bounce(p2, ballrect, speed)
				speed = [-1*temp[0], temp[1]]
			if ballrect.top == p1.bottom or ballrect.top == p2.bottom:
				speed[1] = -speed[1]
			if ballrect.bottom == p1.top or ballrect.bottom == p2.top:
				speed[1] = -speed[1]
		
		#Move
		if iter is not 0:
			ballrect = ballrect.move(speed)
		
		#Write changes
		screen.fill(black)
		pygame.draw.rect(screen, white, [width/2 - 15, 0, 30,height])
		screen.blit(ball, ballrect)
		screen.blit(pl_img, p1)
		screen.blit(pl_img, p2)
		screen.blit(scores[p1_score], p1_score_pos)
		screen.blit(scores[p2_score], p2_score_pos)
		if iter == 0:
			screen.blit(p1_show, p1_s_text_pos)
			screen.blit(p2_show, p2_s_text_pos)
			screen.blit(p1_inst, p1_inst_rect)
			screen.blit(p2_inst, p2_inst_rect)
		pygame.display.flip()
		
		iter += 1
	
	#Declare winner
	if p1_score > p2_score:
		print('Player 1 wins')
	else:
		print('Player 2 wins')