import requests
import arrow

class TVMazeAPI:
    
    def __init__(self):
        self.base_url = 'http://api.tvmaze.com'
        self.api_key = ''
        
    def _get(self, url, headers={}):
        response = requests.get(url, headers=headers)
        return response
    
    def _post(self, url):
        response = requests.post(url)
        return response
    
    def _create_show_obj(self, info):
        show_id = info['id']
        title = info['name']
        img = info['image']['medium'] if info['image'] else None
        summary = info['summary']
        network = info['network']['name'] if info['network'] else None
        show = TVShow(show_id, title, img, summary, network)
        return show
    
    def search_shows(self, query):
        url = self.base_url + f'/search/shows?q={query}'
        res = self._get(url)
        if res.status_code == 200:
            searched_shows = res.json()
            return [self._create_show_obj(show['show']) for show in searched_shows]
        return res
    
    def get_show_info(self, show_id):
        url = self.base_url + f'/shows/{show_id}'
        res = self._get(url)
        if res.status_code == 200:
            info = res.json()
            show = self._create_show_obj(info)
            show.cast = show.get_cast()
            return show
        return res
    
    def get_episode_list(self, show_id):
        url = self.base_url + f'/shows/{show_id}/episodes'
        res = self._get(url)
        if res.status_code == 200:
            return res.json()
        return res

    def get_cast_list(self, show_id):
        url = self.base_url + f'/shows/{show_id}/cast'
        res = self._get(url)
        if res.status_code == 200:
            return res.json()
        return res


class TVShow:
    def __init__(self, show_id, title, img, summary, network):
        self.id = show_id
        self.title = title
        self.image = img
        self.summary = summary
        self.network = network
        self.episodes = self.get_episodes()
        
    def __repr__(self):
        return f'<TV Show | {self.title} >'
    
    def __str__(self):
        return f'{self.id} - {self.title}'
    
    def get_episodes(self):
        api = TVMazeAPI()
        episodes = api.get_episode_list(self.id)
        all_eps = []
        for episode in episodes:
            episode_id = episode['id']
            title = episode['name']
            season = episode['season']
            number = episode['number']
            airdate = episode['airdate']
            summary = episode['summary']
            all_eps.append(Episode(episode_id, title, season, number, airdate, summary))
        return all_eps

    def get_cast(self):
        api = TVMazeAPI()
        cast_list = api.get_cast_list(self.id)
        cast = []
        for person in cast_list:
            person_id = person['person']['id']
            name = person['person']['name']
            image = person['person']['image']['medium']
            char_image = person['character']['image']['medium']
            birthday = person['person']['birthday']
            char_name = person['character']['name']
            cast.append(Person(person_id, name, image, char_name, char_image, birthday))
        return cast
        

class Episode:
    def __init__(self, episode_id, title, season, number, airdate, summary):
        self.id = episode_id
        self.title = title
        self.season = season
        self.number = number
        self.airdate = airdate
        self.summary = summary
        
    def __repr__(self):
        return f'<Episode | {self.title}>'
    
    def __str__(self):
        return f'{self.id} - {self.title}'


class Person:

    def __init__(self, person_id, actor_name, actor_image, character_name, character_image, birthday):
        self.id = person_id
        self.actor_name = actor_name
        self.actor_image = actor_image
        self.character_name = character_name
        self.character_image = character_image
        if birthday:
            self.age = arrow.get(birthday).humanize().replace('ago', 'old')
        else:
            self.age = birthday

    def __repr__(self):
        return f'<Person | {self.name}>'

    def __str__(self):
        return f'{self.id} - {self.name}'