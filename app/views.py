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

	twitterText = twitterSearch(url)
	yttext+=" "
	yttext+= twitterText
	
	#newfile = codecs.open('youtubetext.txt','r')
	#inputtext = newfile.read()
	alchemy = AlchemyAPI()

	entities = alchemy.entities('text', yttext, {'sentiment': 1, 'outputMode': 'json'})		#finds entities and keywords using alchemy API
	keywords = alchemy.keywords('text', yttext, {'sentiment': 1, 'outputMode': 'json'})
	#newfile.close()
	
	IMPORTANCE_BOUNDARY = .8

	entitylist = ''
	keywordlist = ''
	words_to_search = ''
	try:
		all_entities = entities['entities']
	except KeyError:
		print ("empty entities")
	for entity in all_entities:																	#creates a list of all entities and keywords for reference
		if float(entity['relevance']) > IMPORTANCE_BOUNDARY:													#filters out any entities/keywords with relevance less than 9 (out of 10)
			words_to_search += entity['text']+' '
		entitylist += smart_str(entity['text'])+'('+smart_str(entity['relevance'])+')'+' '
	allkeywords = keywords['keywords']
	for keyword in allkeywords:
		if float(keyword['relevance']) > IMPORTANCE_BOUNDARY:
			words_to_search += keyword['text']+' '
		keywordlist += smart_str(keyword['text'])+'('+smart_str(keyword['relevance'])+')'+' '

	keyword_videos = youtube_search(words_to_search)

	if entitylist == '':
		entitylist = "None Detected"
	if keywordlist == '':
		keywordlist = "None Detected"
	
	'''
	###################
	SIMPLE TITLE SEARCH
	###################
	'''

	videotitle = video.title
	uploaddate = datetime.datetime.strptime(video.published, '%Y-%m-%d %H:%M:%S')


	titlesearch_videos = youtube_search(video.title)			#search title 

	keywordvideo_prev = []
	for video in keyword_videos:
		if video.get('time') < uploaddate:
			keyword_videos.remove(video)
			keywordvideo_prev.append(video)

	titlevideo_prev = []
	for video in titlesearch_videos:
		if video.get('time') < uploaddate:
			titlesearch_videos.remove(video)
			titlevideo_prev.append(video)


	return render_template('search_results.html',
							query=query,
							entitylist = entitylist,
							keywordlist = keywordlist,
							text = yttext,
							words_to_search = words_to_search,
							keyword_videos = keyword_videos,
							keywordvideo_prev = keywordvideo_prev,
							videotitle = videotitle,
							titlesearch_videos = titlesearch_videos,
							titlevideo_prev = titlevideo_prev,
							uploaddate = uploaddate)






