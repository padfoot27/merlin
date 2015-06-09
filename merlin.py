import click
import tmdbsimple as tmdb
import time

tmdb.API_KEY = 'deb5d2f55e284931baf4f7e7020cfe44'

genreDict = {u'Action': 28,
 u'Adventure': 12,
 u'Animation': 16,
 u'Comedy': 35,
 u'Crime': 80,
 u'Documentary': 99,
 u'Drama': 18,
 u'Family': 10751,
 u'Fantasy': 14,
 u'Foreign': 10769,
 u'History': 36,
 u'Horror': 27,
 u'Music': 10402,
 u'Mystery': 9648,
 u'Romance': 10749,
 u'Science Fiction': 878,
 u'TV Movie': 10770,
 u'Thriller': 53,
 u'War': 10752,
 u'Western': 37}

numToGenre = {1: u'Action',
 2: u'Adventure',
 3: u'Animation',
 4: u'Comedy',
 5: u'Crime',
 6: u'Documentary',
 7: u'Drama',
 8: u'Family',
 9: u'Fantasy',
 10: u'Foreign',
 11: u'History',
 12: u'Horror',
 13: u'Music',
 14: u'Mystery',
 15: u'Romance',
 16: u'Science Fiction',
 17: u'TV Movie',
 18: u'Thriller',
 19: u'War',
 20: u'Western'}

# Movie class

class Movie:

    def __init__(self,title,ID,lan,genres,overview,rating,release_date):
        self.title = title
        self.ID = ID
        self.lan = lan
        self.genres = genres
        self.overview = overview
        self.rating = rating
        self.release_date = release_date

    def get_title(self):
        return self.title

    def get_id(self):
        return self.ID

    def get_lan(self):
        return self.lan

    def get_genres(self):
        return self.genres

    def get_overview(self):
        return self.overview

    def get_rating(self):
        return self.rating 
    
    def get_release_date(self):
        return self.release_date
    
    def findTrailer(self):
        movie = tmdb.Movies(self.get_id())
        tries = 0
        trailer = []
        while tries < 3:
            tries += 1
            try:
                trailer = movie.videos()
                trailer = trailer['results']
                break
            except:
                continue 
        result = []

        for i in xrange(len(trailer)):
             result.append('https://www.youtube.com/watch?v=' + trailer[i]['key'].encode('ascii','ignore'))
        return result 

    def findCastAndCrew(self):
        movie = tmdb.Movies(self.get_id())
        tries = 0
        cast = []
        crew = []
        while tries < 3:
            tries += 1
            try:
                credits = movie.credits()
                cast = credits['cast']
                crew = credits['crew']
                break 
            except:
                continue 
        ca = []
        cr = []

        for i in xrange(len(cast)):
            ca.append(cast[i]['name'].encode('ascii','ignore') + ' As ' + cast[i]['character'].encode('ascii','ignore'))

        for i in xrange(len(crew)):
            cr.append((crew[i]['name'].encode('ascii','ignore'),crew[i]['job'].encode('ascii','ignore')))
        return ca,cr

    def findKeywords(self):
        movie = tmdb.Movies(self.get_id())
        keywords = []
        tries = 0

        while tries < 3:
            tries += 1
            try:
                keywords = movie.keywords()
                keywords = keywords['keywords']
                break
            except:
                continue 

        result = ''
        for i in xrange(len(keywords)):
            result += keywords[i]['name'].encode('ascii','ignore') + ','
        
        return result[:-1]
            
    def __repr__(self):
        return self.title

# Helper Function

def findPerson(name):
    search = tmdb.Search()
    nID = {}
    tries = 0
    while tries < 3:
        tries += 1
        try:    
            response = search.person(query=name)
            for i in xrange(3):
                nID[(i + 1,response['results'][i]['name'])] = response['results'][i]['id'] 
            break
        except:
            continue
    return nID

# Find movies based on the given data

def discoverMovie(genre,cast,crew,language):
    
    discover = tmdb.Discover()
    tries = 0
    response = None
    kwargs = {'with_cast':cast,'with_crew':crew,'with_genres':genre,'language':language,'primary_release_date.gte':'2000-01-01'}
    while tries < 3:
        tries += 1
        try:
            response = discover.movie(**kwargs)
            break
        except:
            continue 
    r = None
    if response:    
        r = response['results']
    result = {}

    if response:
        for i in xrange(len(r)):
            m = Movie(r[i]['title'],r[i]['id'],r[i]['original_language'],r[i]['genre_ids'],r[i]['overview'],r[i]['vote_average'],r[i]['release_date'])
            result[i + 1] = m

    return result 


# Starts from here

@click.command()
def discover():
    '''Merlin's here'''
    click.echo("Hi, I am Merlin, google's dumb cousin, your personal movie recommender\n")
    time.sleep(1)
    click.echo("So,let's find you a Movie\n")
    time.sleep(0.5)

    # Get the Language
    language = 'en'
    wantLanguage = click.confirm('Do you want to pick the language,default is english')
    click.echo('\n')
    if wantLanguage:
        justEN = click.confirm('All languages')
        click.echo('\n')
        if justEN:
           language = '' 

    # Get the Genre
    genre = ''
    wantGenre = click.confirm('Do you want to a pick a genre ')
    click.echo('\n')
    if wantGenre:
        for key in sorted(numToGenre.iterkeys()):
            click.echo(str(key) + '. ' + numToGenre[key].encode('ascii','ignore'))
        g = click.prompt('\nPick a Genre(comma separated)')
        click.echo('\n')
        gList = g.split(',')
        for i in xrange(len(gList)):
            genre += str(genreDict[numToGenre[int(gList[i])]])
            genre += ','
        genre = genre[:-1]

    # Get the Cast
    cast = ''
    wantCast = click.confirm('Do you want to specify the cast ')
    click.echo('\n')
    if wantCast:
        click.echo('Pick the cast, Be as specific as you can and avoid spelling mistakes\n')
        while True:
            search = tmdb.Search()
            name = click.prompt('Give me a name')
            click.echo('\n')
            result = findPerson(name)
            if (result):
                for key in sorted(result.iterkeys()):
                    add = click.confirm('Are you looking for ' + key[1].encode('ascii','ignore'))
                    click.echo('\n')
                    if add:
                        cast += str(result[key])
                        cast += ','
                        break;
            else:
                print 'Sorry, try again'
                click.echo('\n')
             
            confirm = click.confirm('You want to add more people')
            click.echo('\n')
            if (confirm == False):
                break
        cast = cast[:-1]

    
    # Get the crew
    crew = ''
    wantCrew = click.confirm('Do you want to specify the crew ')
    click.echo('\n')
    if wantCrew:
        click.echo('Pick the crew, Be as specific as you can and avoid spelling mistakes\n')
        while True:
            search = tmdb.Search()
            name = click.prompt('Give me a name')
            click.echo('\n')

            result = findPerson(name)
            if (result):
                for key in sorted(result.iterkeys()):
                    add = click.confirm('Are you looking for ' + key[1].encode('ascii','ignore'))
                    click.echo('\n')
                    if add:
                        crew += str(result[key])
                        crew += ','
                        break;
            else:
                print 'Sorry, try again'
                click.echo('\n')
             
            confirm = click.confirm('You want to add more people')
            click.echo('\n')
            if (confirm == False):
                break
        crew = crew[:-1]

    # Get results
    click.echo('Sit back and Relax\n')
    movies = discoverMovie(genre,cast,crew,language)
    found = False

    if movies:
        found = True 
        for key in sorted(movies.iterkeys()):
            print movies[key].get_title(),
            print movies[key].get_rating()
            print movies[key].get_release_date()
            print movies[key].get_overview()
            print '\n'

            wantDetails = click.confirm('Do you want more details regarding this movie ')
            click.echo('\n')
            if wantDetails:
                click.echo('Wait up\n')
                cast,crew = movies[key].findCastAndCrew()
    
                click.echo('Full Cast')
                for i in xrange(min(len(cast),12)):
                    click.echo(cast[i])

                click.echo('\n')

                click.echo('Full Crew')
                for i in xrange(len(crew)):
                    if (crew[i][1] in ['Director','Screenplay','Editor','Producer','Writer','Original Music Composer']):
                        click.echo(crew[i][0] + ' ... ' + crew[i][1])

                click.echo('\n')
                
                click.echo('Getting the keywords for the movie\n') 
                keywords = movies[key].findKeywords()
                if keywords:
                    click.echo(keywords)
                else:
                    click.echo('Nothing Found')
                click.echo('\n')


            wantTrailer = click.confirm('Would you like to see the trailer')
            click.echo('\n')
            if wantTrailer:
                trailer = movies[key].findTrailer() 
                if trailer:
                    for i in xrange(len(trailer)):
                        click.echo(trailer[i])
                else:
                    click.echo('Nothing Found')
            click.echo('\n')

            wantQuit = click.confirm('Do you want to look at more movies')
            click.echo('\n')
            if wantQuit == False:
                break
    else:
        click.echo('Sorry, try again')

    if found:
        click.echo("That's all Folks,Merlin says goodbye\n")
