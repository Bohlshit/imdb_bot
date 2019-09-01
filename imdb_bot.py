import bs4
import requests
import json
import os

# Make it possible to mark watched movies
# Make randomized suggestion for movie to watch
# Make filter for movie list
# Make command for % watched
# Add rating to the data

class IMDBBot():
	FILE_DIR = 'C:\\Users\\RasmusBohl\\Desktop\\imdb_bot' # Change
	FILE_NAME = 'imdb_data.json'
	FILE_PATH = os.path.join(FILE_DIR, FILE_NAME)

	def __init__(self):
		self.movie_list = self.get_imdb_data() # TODO: Change this


	# Scrape the data from imdb (currently just 'headlines')
	def get_imdb_data(self):
		data = {}
		imdb_url = 'https://www.imdb.com/chart/top?ref_=nv_mv_250'
		headers = {"Accept-Language": "en-US,en;q=0.5"} # Force English language

		req = requests.get(imdb_url, headers=headers)
		req.raise_for_status() # Probably do try-catch stuff
		soup = bs4.BeautifulSoup(req.text, "html.parser")
		raw_data = soup.findAll("td", {"class":"titleColumn"})
		raw_scores = soup.findAll('strong', {'title': True})
		imdb_data = self.format_data(raw_data, raw_scores)

		return imdb_data


	# Format the scraped data
	def format_data(self, raw_data, raw_scores):
		data = {}

		# Run through each title line and grab stuff
		for index, movie_data in enumerate(raw_data):
			movie_details = {}
			split_data = movie_data.text.split()
			title = ' '.join([word for word in split_data[1:-1]])
			release_year = split_data[-1][1:-1]

			movie_details['release'] = release_year
			movie_details['score'] = raw_scores[index].text
			# Make 'if movie not in all time list' check
			movie_details['seen'] = False

			data[title] = movie_details

		return data


	# Simply print the movie list as presented on the site
	def print_top250_list(self):
		for num, (title, details) in enumerate(self.movie_list.items()):
			movie_seen = details['seen']
			list_item = f"{num + 1}. {title} ({details['release']}) {'✓' if movie_seen else ''}"
			print(list_item)


	# Save the current top 250 list to json file
	def save_movie_list(self):
		list_data = self.get_list_data()

		new_in_top250 = {}
		for movie, details in self.movie_list.items():
			if movie not in list_data:
				new_in_top250[movie] = details

		if len(new_in_top250) != 0:
			with open(self.FILE_PATH, 'w') as file:
				for movie in new_in_top250:
					list_data[movie] = details
				json.dump(list_data, file, indent=4)
			print('Saved top250 list to file...')
		else:
			print('Nothing new to save to list...')

	# Mark a movie as watched - TODO: perhaps do some more error handling (non-existing movie etc.)
	def mark_as_watched(self, movie):
		list_data = self.get_list_data()
		list_data[movie] = True
		with open(self.FILE_PATH, 'w') as file:
			json.dump(list_data, file, indent=4)


	def get_list_data(self):
		with open(self.FILE_PATH, 'r+') as file:
			list_data = json.load(file)
			return list_data


if __name__ == '__main__':
	test = IMDBBot()
	test.print_top250_list()
	test.save_movie_list()