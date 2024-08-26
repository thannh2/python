import pygame
import random
import math
from sklearn.cluster import KMeans

class Point:
	def __init__(self, position, color):
		self.position = position
		self.color = color

	def show_point(self):
		pygame.draw.circle(screen, BLACK, (self.position[0] + 55, self.position[1] + 55),6)
		pygame.draw.circle(screen, self.color, (self.position[0] + 55, self.position[1] + 55),5)

def save_point(points, color):
	x,y = pygame.mouse.get_pos()
	x = x - 55
	y = y - 55
	point_temp = Point((x,y), color)
	points.append(point_temp)
	return points

def random_clusters(k):
	clusters = []
	for i in range(k):
		cluster_apd = [random.randint(9,681),random.randint(9,481)]
		clusters.append(cluster_apd)
	return clusters

def show_clusters(clusters, COLOR):
	for i in range(len(clusters)):
		pygame.draw.circle(screen, COLOR[i], (clusters[i][0] + 55, clusters[i][1] + 55),9)

def distance(p1,p2):
	distance = 0
	for i in range(len(p1)):
		distance += pow(p1[i] - p2[i],2)

	return math.sqrt(distance)

def assign(points, clusters):
	labels = []
	for i in range(len(points)):
		distances = []
		for j in range(len(clusters)):
			distance_temp = distance(points[i].position,clusters[j])
			distances.append(distance_temp)
		labels.append(distances.index(min(distances)))
	for i in range(len(points)):
		points[i].color = COLOR[labels[i]]
	return labels

def update_clusters(clusters, points, labels):
	new_clusters = []

	for i in range(len(clusters)):
		cluster_sum = [0, 0]
		count = 0

		for j in range(len(points)):
			if labels[j] == i:
				cluster_sum[0] += points[j].position[0]
				cluster_sum[1] += points[j].position[1]
				count += 1

		if count != 0:
			new_x = cluster_sum[0] / count
			new_y = cluster_sum[1] / count
			new_clusters.append([new_x, new_y])
		else:
			new_clusters.append(clusters[i])

	return new_clusters

def error_value(points, clusters, labels):
	error_value = 0
	for i in range(len(points)):
		error_value += int(distance(clusters[labels[i]], points[i].position))
	return error_value

pygame.init()

screen = pygame.display.set_mode((1200,700))

pygame.display.set_caption("kmeans visualization")

running = True

clock = pygame.time.Clock()

BACKGROUND = (214, 214, 214)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (147, 153, 35)
PURPLE = (255, 0, 255)
SKY = (0, 255, 255)
ORANGE = (255, 125, 25)
GRAPE = (100, 25, 125)
GRASS = (55, 155, 65)
COLOR = [RED, GREEN, BLUE, YELLOW, PURPLE, SKY, ORANGE, GRAPE, GRASS]

k = 0
error = 0
points = []
clusters = []
labels = []

font = pygame.font.SysFont('sans', 40)
text = [0] * 8
text[0] = font.render("+", True, WHITE)
text[1]= font.render("-", True, WHITE)
text[2] = font.render("Run", True, WHITE)
text[3]= font.render("Random", True, WHITE)
text[4] = font.render("Error = " + str(error), True, BLACK)
text[5]= font.render("Algorithm", True, WHITE)
text[6] = font.render("Reset", True, WHITE)
text[7] = font.render("K = " + str(k), True, BLACK)

while running:
	clock.tick(60)
	screen.fill(BACKGROUND)
	mouse_x, mouse_y = pygame.mouse.get_pos()

	pygame.draw.rect(screen, BLACK, (50,50,700,500))
	pygame.draw.rect(screen, (249, 255, 230), (55,55,690,490))
	pygame.draw.rect(screen, BLACK, (850,50,50,50))
	pygame.draw.rect(screen, BLACK, (950,50,50,50))

	screen.blit(text[0],(865,50))
	screen.blit(text[1],(965,50))
	screen.blit(text[7],(1050,50))

	for i in range(5):
		margin = 100
		pygame.draw.rect(screen, BLACK, (850,150 + margin*i,150,50))
		screen.blit(text[i + 2],(850,150 + margin*i))

	pygame.draw.rect(screen, (214,214,214), (850,350,150,50))
	screen.blit(text[4],(850,350))

	text[4] = font.render("Error = " + str(error), True, BLACK)
	text[7] = font.render("K = " + str(k), True, BLACK)

	if 55 < mouse_x < 745 and 55 < mouse_y < 545:
		font1 = pygame.font.SysFont('sans', 15)
		text_mouse = font1.render("(" + str(mouse_x - 55) + "," + str(mouse_y - 55)+")", True, BLACK)
		screen.blit(text_mouse,(mouse_x + 10,mouse_y + 10))

	for i in range(len(points)):
			points[i].show_point()

	show_clusters(clusters, COLOR)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				# + Button
				if 850 < mouse_x < 900 and 50 < mouse_y < 100:
					if k < 9:
						k += 1
				# - Button
				if 950 < mouse_x < 1000 and 50 < mouse_y < 100:
					if k > 0:
						k -= 1
				#Run
				if 850 < mouse_x < 1000 and 150 < mouse_y < 200:
					try:
						labels = assign(points, clusters)
						clusters = update_clusters(clusters, points, labels)
						error = error_value(points, clusters, labels)
					except:
						print("run error")

				#Random Button
				if 850 < mouse_x < 1000 and 250 < mouse_y < 300:
					if k != 0:
						clusters = random_clusters(k)

				#Algorithm Button
				if 850 < mouse_x < 1000 and 450 < mouse_y < 500:
					try:
						points_position = []
						for i in range(len(points)):
							points_position.append(points[i].position)

						kmeans = KMeans(n_clusters=k).fit(points_position)
						labels = kmeans.predict(points_position)
						clusters = kmeans.cluster_centers_
						assign(points, clusters)
						error = error_value(points, clusters, labels)
					except:
						print("error")

				#Reset Button
				if 850 < mouse_x < 1000 and 550 < mouse_y < 600:
					k = 0
					error = 0
					points = []
					clusters = []
					labels = []

				if 55 < mouse_x < 745 and 55 < mouse_y < 545:
					points = save_point(points, WHITE)

	pygame.display.flip()

pygame.quit()
