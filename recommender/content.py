from google_images_search import GoogleImagesSearch
from youtubesearchpython import VideosSearch
import config

class ContentGetter(object):
    def __init__(self):
        self.gis = GoogleImagesSearch(config.GCS_DEVELOPER_KEY, config.GCS_CX)

    def get_images(self,query):
        query = query.replace('\n','')
        _search_params = {
        'q': query,
        'num': 1,
        'fileType': 'jpg',
        # 'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived',
        'imgType': 'photo',
        'safe': 'medium',
        'imgSize': 'MEDIUM',
        # "tbm": "isch",
        # "tbs": "itp:photos,isz:s"
        }
        self.gis.search(search_params=_search_params)
        image_urls = []
        for image in self.gis.results():
            image_urls.append(image.url)
        return image_urls
        
    def get_yt_link(self, query):
        query = query.replace('\n','')
        videosSearch = VideosSearch(query, limit = 1)
        return (videosSearch.result()['result'][0]['title'], 
                videosSearch.result()['result'][0]['link'])

