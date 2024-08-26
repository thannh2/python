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

#function read videos from user
def read_video():
	title = input("Enter title: ") + "\n"
	link = input("Enter link: ") + "\n"
	video = Video(title, link)
	return video

def read_videos():
	videos = []
	total_video = int(input("Enter how many videos: "))
	for i in range(total_video):
		print("Enter video ", i + 1)
		vid = read_video()
		videos.append(vid)
	return videos

#function print videos from list
def print_video(video):
	print("Video title: " + video.title, end = "")
	print("Video link: " + video.link, end = "")

def print_videos(videos):
	for i in range(len(videos)):
		print("Video " + str(i + 1) + ": ")
		print_video(videos[i])
#-------------------------------------------------------------------------------------------------

#function write videos to text
def write_video_txt(video, file):
	file.write(video.title)
	file.write(video.link)

def write_videos_txt(videos, file):
	total = len(videos)
	file.write(str(total) + "\n")
	for i in range(total):
		write_video_txt(videos[i], file)

#function read videos from text
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

#function for playlist
def read_playlist():
	playlist_name = input("Enter playlist name: ") + "\n"
	playlist_description = input("Enter playlist description: ") +"\n"
	playlist_rating = input("Enter rating (1-5): ") + "\n"
	playlist_image = input("Enter image(image.jpg/png/...): ") + "\n"
	playlist_videos = read_videos()
	playlist = Playlist(playlist_name, playlist_description, playlist_rating, playlist_image ,playlist_videos)
	return playlist

def write_playlist_txt(playlist, file):
	file.write(playlist.name)
	file.write(playlist.description)
	file.write(playlist.rating)
	file.write(playlist.image)
	write_videos_txt(playlist.videos, file)

def write_playlists_txt(playlists):
	total_playlist = len(playlists)
	with open("data.txt", "w") as file:
		file.write(str(total_playlist)+ "\n")
		for i in range(total_playlist):
			write_playlist_txt(playlists[i], file)

def print_playlist(playlist):
	print("Playlist name: " +  playlist.name, end = "")
	print("Playlist description: " +  playlist.description, end = "")
	print("Playlist rating: " +  playlist.rating, end = "")
	print("Playlist image: "+ playlist.image, end = "")
	print_videos(playlist.videos)
	print("") 

#Load data

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

def select_in_range(prompt, min, max):
	user_input = input(prompt)
	while not user_input.isdigit() or int(user_input) < min or int(user_input) > max:
		print("Not valid, try again ")
		user_input = input(prompt)

	return int(user_input)

#-------------------------------------------------------------------------------------------------

#function for menu
def show_menu_playlist():
	print("Menu Option: ")
	print(" -------------------------------------")
	print("|  Option 1: Show and play playlists  |")
	print("|  Option 2: Add a playlist           |")
	print("|  Option 3: Remove a playlist        |")
	print("|  Option 4: Save and Exit            |")
	print(" -------------------------------------")

def menu_option_playlist1(playlists):
	for i in range(len(playlists)):
		print(str(1+i) + ". " + playlists[i].name, end = "")
		print("Description: " + playlists[i].description, end = "")
		print("Rating: " + playlists[i].rating, end = "")
		print("--------")

	select_playlist = select_in_range("Select a playlist(1-"+  str(len(playlists)) +"): ", 1, len(playlists))
	print_playlist(playlists[select_playlist - 1])
	video_option(playlists[select_playlist - 1])

def menu_option_playlist2(playlists):
	add_playlist = read_playlist() 
	playlists.append(add_playlist)
	return playlists

def menu_option_playlist3(playlists):
	for i in range(len(playlists)):
		print(str(1+i) + ". " + playlists[i].name, end = "")
		print("Description: " + playlists[i].description, end = "")
		print("Rating: " + playlists[i].rating, end = "")
		print("--------")
	remove_playlist = select_in_range("Remove a playlist(1-"+  str(len(playlists)) +"): ", 1, len(playlists))
	del playlists[remove_playlist - 1]
	return playlists
#-------------------------------------------------------------------------------------------------

def show_menu_video():
	print(" ------------------------------")
	print("|  Option 1: Play a video      |")
	print("|  Option 2: Add a video       |")
	print("|  Option 3: Update a playlist |")
	print("|  Option 4: Remove a video    |")
	print("|  Option 5: Exit              |")
	print(" ------------------------------")

def video_option(playlist):
	while True:
		show_menu_video()
		user_option_video = select_in_range("Select an option(1-5): ", 1, 5)
		if user_option_video == 1:
			menu_option_video1(playlist)
			input("Press Enter to continue.")

		elif user_option_video == 2:
			playlist = menu_option_video2(playlist)
			print("Add a video successfully!")
			input("Press Enter to continue.")

		elif user_option_video == 3:
			playlist = menu_option_video3(playlist)
			print("Update successfully!")
			input("Press Enter to continue.")

		elif user_option_video == 4:
			playlist = menu_option_video4(playlist)
			print("Remove a video successfully")
			input("Press Enter to continue.")

		elif user_option_video == 5:
			break

#Open a video which user select on web
def menu_option_video1(playlist):
	print_videos(playlist.videos)
	play_video = select_in_range("\nSelect a video (1," + str(len(playlist.videos)) + "): ", 1, len(playlist.videos))
	print_video(playlist.videos[play_video - 1])
	playlist.videos[play_video - 1].open_video_in_web()

#Add a video to playlist
def menu_option_video2(playlist):
	print("New video information: ")
	title = input("New video title: ") + "\n"
	link = input("New video link: ") + "\n"
	add_video = Video(title, link)
	playlist.videos.append(add_video)
	return playlist

#Update playlist (name, description, rating)
def menu_option_video3(playlist):
	print("what do you want to update: ")
	print("1. Name playlist")
	print("2. Description")
	print("3. Rating")
	update = select_in_range("Enter what you want to update (1-3):", 1, 3)
	if update == 1:
		playlist.name = input("Enter new name: ") + "\n"
	elif update == 2:
		playlist.description = input("Enter new description: ") + "\n"
	else:
		playlist.rating = input("Enter rating (1-5): ") + "\n"

	return playlist

#Remove a video from playlist
def menu_option_video4(playlist):
	print_videos(playlist.videos)
	video_remove = select_in_range("Remove video(1," + str(len(playlist.videos)) +"): ", 1, len(playlist.videos))
	del playlist.videos[video_remove - 1] #you can use for loop to save to a new list except the video you want to remove.
	return playlist
#-------------------------------------------------------------------------------------------------

def main():
	try:
		playlists = read_playlists_from_txt()
	except:
		playlist = []
		print("Let's create your playlist:")
		print("Create playlist:")
		playlist = read_playlist()
		write_playlist_txt(playlist)
		playlists.append(playlist)

	while True:
		show_menu_playlist()
		user_option_playlist = select_in_range("Select an option(1-4): ", 1, 4)
		if user_option_playlist == 1:
			menu_option_playlist1(playlists)

		elif user_option_playlist == 2:
			playlists = menu_option_playlist2(playlists)
			print("Add a playlist successfully")
			input("Press Enter to continue.")

		elif user_option_playlist == 3:
			playlists = menu_option_playlist3(playlists)
			print("Remove a playlist successfully")
			input("Press Enter to continue.")

		elif user_option_playlist == 4:
			write_playlists_txt(playlists)
			print("Save and Exit")
			break
main()
