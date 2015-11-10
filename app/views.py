from flask import render_template, flash, redirect, url_for
from app import app
from .forms import SearchForm
from .keyword_search import *
from .youtube_search import *


@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
	form = SearchForm()
	return render_template('index.html',
							title = 'home',
							form=form)

@app.route('/search', methods=['POST'])
def search():
	search = SearchForm()
	return redirect(url_for('search_results', query=search.videoid.data.split('=')[-1]))

@app.route('/search_results/<query>')
def search_results(query):
	
	'''
	#################################
	KEYWORD/ENTITY ALCHEMY API SEARCH
	#################################
	'''
	url = query
	video = pafy.new(url)									#new pafy video object
	#yttext = codecs.open('youtubetext.txt','w+','utf-8')
	description = video.description
	description_noURL = removeURLs(description)		#removes links from descriptions
	#yttext.write(description_noURL+' ')			#writes file with description and title of video
	yttext = description_noURL
	yttext+=" "
	yttext+=video.title

	twitter_text = twitter_search(url)
	yttext+=" "
	yttext+= twitter_text
	
	#newfile = codecs.open('youtubetext.txt','r')
	#inputtext = newfile.read()
	alchemy = AlchemyAPI()

	entities = alchemy.entities('text', yttext, {'sentiment': 1, 'outputMode': 'json'})		#finds entities and keywords using alchemy API
	keywords = alchemy.keywords('text', yttext, {'sentiment': 1, 'outputMode': 'json'})
	#newfile.close()
	
	IMPORTANCE_BOUNDARY = .8

	entity_list = ''
	keyword_list = ''
	words_to_search = ''
	try:
		all_entities = entities['entities']
		for entity in all_entities:	
			if float(entity['relevance']) > IMPORTANCE_BOUNDARY: #filters out any entities/keywords with relevance less than importance boundary
				words_to_search += entity['text']+' '
			entity_list += entity['text']+'('+entity['relevance']+')'+' '
	except KeyError:
		print ("empty entities")
	
	all_keywords = keywords['keywords']
	for keyword in all_keywords:
		if float(keyword['relevance']) > IMPORTANCE_BOUNDARY:
			words_to_search += keyword['text']+' '
		keyword_list += keyword['text']+'('+keyword['relevance']+')'+' '

	keyword_videos = youtube_search(words_to_search)

	if entity_list == '':
		entity_list = "None Detected"
	if keyword_list == '':
		keyword_list = "None Detected"
	
	'''
	###################
	SIMPLE TITLE SEARCH
	###################
	'''

	videotitle = video.title
	uploaddate = datetime.datetime.strptime(video.published, '%Y-%m-%d %H:%M:%S')


	titlesearch_videos = youtube_search(video.title)	#search title 

	keyword_video_earlier = [video for video in keyword_videos if video.get('time') < uploaddate]
	keyword_video_later = [video for video in keyword_videos if video.get('time') >= uploaddate]

	title_video_earlier = [video for video in titlesearch_videos if video.get('time') < uploaddate]
	title_video_later = [video for video in titlesearch_videos if video.get('time') >= uploaddate]

	return render_template('search_results.html',
							query=query,
							entity_list = entity_list,
							keyword_list = keyword_list,
							text = yttext,
							words_to_search = words_to_search,
							keyword_video_later = keyword_video_later,
							keyword_video_earlier = keyword_video_earlier,
							videotitle = videotitle,
							title_video_later = title_video_later,
							title_video_earlier = title_video_earlier,
							uploaddate = uploaddate)






