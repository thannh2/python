import pygame
import webbrowser

class Video:
	def __init__(self, title, link):
		self.title = title
		self.link = link
	def open_video_in_web(self):
		webbrowser.open(self.link)

class Playlist:
	def __init__(self, name, description, rating, image, videos):
		self.name = name
		self.description = description
		self.rating = rating
		self.image = image
		self.videos = videos

class TextButton:
	def __init__(self, text, position):
		self.text = text
		self.position = position

	def draw_text(self, color):
		font = pygame.font.SysFont('sans', 20)
		text_render = font.render(self.text, True, BLACK)
		self.text_box = text_render.get_rect()

		if self.is_mouse_on_text():
			text_render = font.render(self.text, True, color)
			pygame.draw.line(screen, color, (self.position[0],self.position[1] + self.text_box[3]),(self.position[0]+self.text_box[2],self.position[1]+self.text_box[3]))
		else:
			text_render = font.render(self.text, True, BLACK)

		screen.blit(text_render,self.position)

	def is_mouse_on_text(self):
		mouse_x,mouse_y = pygame.mouse.get_pos()
		if self.position[0] < mouse_x < self.position[0] + self.text_box[2] and self.position[1] < mouse_y < self.position[1] + self.text_box[3]:
			return True
		else:
			return False

#Playlists information function
def read_video_from_txt(file):
	title = file.readline()
	link = file.readline()
	video = Video(title, link)
	return video

def read_videos_from_txt(file):
	videos = []
	total = file.readline()		
	for i in range(int(total)):
		video = read_video_from_txt(file)
		videos.append(video)
	return videos

def read_playlist_from_txt(file):
	playlist_name = file.readline()
	playlist_description = file.readline()
	playlist_rating = file.readline()
	playlist_image = file.readline()
	playlist_videos = read_videos_from_txt(file)
	playlist = Playlist(playlist_name, playlist_description, playlist_rating, playlist_image, playlist_videos)

	return playlist

def read_playlists_from_txt():
	playlists = []

	with open("data.txt", "r") as file:
		total_playlist = file.readline()

		for _ in range(int(total_playlist)):
			playlist_temp = read_playlist_from_txt(file)
			playlists.append(playlist_temp)
			
	return playlists


pygame.init()

screen = pygame.display.set_mode((1000,600))

pygame.display.set_caption('Pygame App')

running = True

#Load data
#Load many playlists
playlists = read_playlists_from_txt()

#Text for print to screen
playlist_name_btn = []
# for i in range(len(playlists)):
for playlist in playlists:
	# playlist_name_btn_temp = TextButton(playlists[i].name.rstrip(), (50,50))
	playlist_name_btn_temp = TextButton(playlist.name.rstrip(), (50, 100))
	playlist_name_btn.append(playlist_name_btn_temp)

video_btn_list = [[] for _ in range(len(playlists))]
video_seen = [[] for _ in range(len(playlists))]

for i in range(len(playlists)):
	# for j in range(len(playlists[i].videos)):
	for (j, video) in enumerate(playlists[i].videos):
		margin = 50
		# video_btn = TextButton(str(j+1) + ". " + playlists[i].videos[j].title.rstrip(),(400,50 + margin * j))
		video_btn = TextButton(str(j+1) + ". " + video.title.rstrip(), (400, 50 + margin * j))
		video_btn_list[i].append(video_btn)
		video_seen[i].append(False)

#Load picture from text
playlist_image = []
for i in range(len(playlists)):
	playlist_temp = pygame.image.load(playlists[i].image.rstrip())
	playlist_image.append(playlist_temp)
background = pygame.image.load('background.jpg')

BLUE = (0,0,255)
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
GREY = (160,160,160)
clock = pygame.time.Clock()

playlist_index = 0
delta_x = 0

while running:
	clock.tick(60)
	screen.fill(WHITE)
	screen.blit(background,(0,0))

	playlist_name_btn[playlist_index].draw_text(BLACK)

	#Thay doi mau sau khi da chon 1 video
	# for j in range(len(video_btn_list[playlist_index])):
	# 	if video_seen[playlist_index][j] == True:
	# 		video_btn_list[playlist_index][j].draw_text()
	# 	else:
	# 		video_btn_list[playlist_index][j].draw_text()
	for (video_btn, current_video_seen) in zip(video_btn_list[playlist_index], video_seen[playlist_index]):
		if current_video_seen == True:
			video_btn.draw_text(BLACK)
		else:
			video_btn.draw_text(BLUE)

	#Check mouse on playlist, show information:
	if playlist_name_btn[playlist_index].is_mouse_on_text():
		x, y = pygame.mouse.get_pos()

		font = pygame.font.SysFont('sans', 20)
		description_background = font.render("  Description: " + playlists[playlist_index].description + "  ", True, BLACK)
		box = description_background.get_rect()
		pygame.draw.rect(screen, GREY, (x,y - 50,box[2],2*box[3]))

		playlist_description_btn = TextButton("  Description: " + playlists[playlist_index].description.rstrip(),(x,y - 30))
		playlist_rating = TextButton("  Rating: " + playlists[playlist_index].rating.rstrip(),(x,y - 50))
		playlist_description_btn.draw_text(BLACK)
		playlist_rating.draw_text(BLACK)

	#Hien mo ta khi dua chuot vao video
	for j in range(len(video_btn_list[playlist_index])):
		if video_btn_list[playlist_index][j].is_mouse_on_text():
			x, y = pygame.mouse.get_pos()

			font = pygame.font.SysFont('sans', 20)
			link_background = font.render("  " + playlists[playlist_index].videos[j].link.rstrip() + "  ", True, BLACK)
			box = link_background.get_rect()
			pygame.draw.rect(screen, GREY, (x,y+20,box[2],box[3]))

			video_show = TextButton("  " + playlists[playlist_index].videos[j].link.rstrip(),(x,y+20))
			video_show.draw_text(BLACK)

	#Tao nut bam chuyen playlist:
	#Tao o bam
	pygame.draw.rect(screen, RED, (50,450,305,50))
	for i in range(4):
		margin = 75
		pygame.draw.rect(screen, WHITE, (55 + margin * i,455,70,40))
	#Ve tam giac
	pygame.draw.polygon(screen, RED, ((90, 457),(70, 474),(90, 493)))
	pygame.draw.polygon(screen, RED, ((105, 457),(105, 493),(78, 475)))
	pygame.draw.polygon(screen, RED, ((303, 457),(302, 493),(323, 475)))
	pygame.draw.polygon(screen, RED, ((315, 457),(316, 493),(336, 475)))
	pygame.draw.polygon(screen, RED, ((178, 457),(178, 493),(149, 475)))
	pygame.draw.polygon(screen, RED, ((228, 457),(229, 493),(256, 475)))
	#Them anh:
	screen.blit(playlist_image[playlist_index],(50,130))
	#Them vach:
	pygame.draw.line(screen, BLACK, (50, 435),(355, 435))
	if delta_x <= 305:
		delta_x += 0.5
		pygame.draw.circle(screen, BLACK, (50 + delta_x,435), 5)
	else:
		delta_x = 0
	#Thao tac voi chuot
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			# if event.button == 3:
			if event.button == 1:
				for j in range(len(video_btn_list[playlist_index])):
					if video_btn_list[playlist_index][j].is_mouse_on_text():
						playlists[playlist_index].videos[j].open_video_in_web()
						video_seen[playlist_index][j] = True
				x,y = pygame.mouse.get_pos()
				if 205 < x < 275 and 455 < y < 495:
					if playlist_index < len(video_btn_list) - 1:
						playlist_index += 1
				if 130 < x < 200 and 455 < y < 495:
					if playlist_index > 0:
						playlist_index -= 1
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				if playlist_index > 0:
					playlist_index -= 1
			if event.key == pygame.K_RIGHT:
				if playlist_index < len(video_btn_list) - 1:
					playlist_index += 1

		if event.type == pygame.QUIT:
			running = False

	pygame.display.flip()

pygame.quit()