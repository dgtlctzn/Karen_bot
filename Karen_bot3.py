import markovify
from random import randint
import nltk
import pickle
import twitter
import requests
import bs4
from datetime import datetime


class TweetBot:

    def __init__(self):
        Twitter = pickle.load(open('/home/pi/PiPy/karen_secret_twitter_credentials.pkl', 'rb'))
        twitter_api = twitter.api.Api(consumer_key=Twitter['Consumer Key'],
                                      consumer_secret=Twitter['Consumer Secret'],
                                      access_token_key=Twitter['Access Token'],
                                      access_token_secret=Twitter['Access Token Secret'],
                                      tweet_mode='extended'
                                      )
        self._twitter_api = twitter_api

    def post(self, tweet):
        self._twitter_api.PostUpdate(tweet)

    def re_tweet(self, user):
        api = self._twitter_api
        retweet = api.GetUserTimeline(user, count=1)
        retweet_id = retweet[0].AsDict()['id']
        api.PostRetweet(retweet_id)


class MarkovTheWise:

    def __init__(self, file, read_type='rt'):
        self._file = file
        self._read_type = read_type

    def corp_creator(self):
        with open(self._file, self._read_type) as txt_file:
            raw_text = txt_file.read()
            corp = nltk.sent_tokenize(raw_text)
            return corp

    def make_model(self):
        corpora = self.corp_creator()
        text_model = markovify.Text(corpora)
        return text_model


class Karen(TweetBot, MarkovTheWise):

    def __init__(self, file):
        super().__init__(self, file)

    def bad_review(self, review_text, structure_text, chains, weight=(1, 10)):
        hashtags = [' #disappointing', ' #crap', ' #nevercomingback', ' #theworst', ' #livelaughlove...andleave',
                    ' #neveragain', ' #unacceptable', ' #badservice', ' #takemybusinesselsewhere', ' #outrageous']
        hash_num_1 = randint(0, 9)
        hash_one = hashtags[hash_num_1]
        hash_two = hashtags[hash_num_1 - randint(1, 3)]

        km = MarkovTheWise(review_text)
        mm = MarkovTheWise(structure_text)

        my_model = km.make_model()
        my_model_2 = mm.make_model()

        combo_model = markovify.combine([my_model, my_model_2], weight)

        restaurant_sent = combo_model.make_short_sentence(80, min_chars=60, tries=100)
        my_tweet = "I'd like to speak to the manager. " + chains[randint(1, 8)] + ' ' + restaurant_sent + hash_one \
                   + hash_two + ' #karen' + ' #karensgonewild'
        return my_tweet

    def get_recipe(self, url):
        my_url = url

        page = requests.get(my_url)

        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all('div', class_='fixed-recipe-card__info')

        web_dict = {i: str(results[i]).split('href="')[1].split('">')[0] for i in range(0, len(results))}
        return web_dict

    def complain(self):
        number = randint(1, 4)
        if number == 1:
            chains = {1: "@Chilis", 2: "@olivegarden", 3: "@Applebees", 4: '@Cheesecake', 5: "@Carrabbas",
                      6: "@PFChangs", 7: "@Maggianos", 8: "@redlobster"}
            text_1 = '/home/pi/PiPy/Karen_text2.txt'
            text_2 = '/home/pi/PiPy/Karen_rest_structure.txt'
            tb = TweetBot()
            tb.post(bad_review(text_1, text_2, chains))
        elif number == 2:
            chains = {1: "@Sephora", 2: "@Target", 3: "@jcpenney", 4: "@tjmaxx", 5: "@marshalls",
                      6: "@Walmart", 7: "@Bloomingdales", 8: "@Macys"}
            text_1 = '/home/pi/PiPy/Karen_retail2.txt'
            text_2 = '/home/pi/PiPy/Karen_retail_structure.txt'
            tb = TweetBot()
            tb.post(bad_review(text_1, text_2, chains))
        elif number == 3:
            user_list = [31869934, 22650211, 2370627199, 26031542, 22515362]
            user_number = randint(0, 4)
            tb = TweetBot()
            tb.re_tweet(user_list[user_number])
        else:
            recipe_site_num = randint(0, 2)
            recipe_type = ['https://www.allrecipes.com/search/results/?ingIncl=ranch&sort=re',
                           'https://www.allrecipes.com/search/results/?ingIncl=bacon&sort=re',
                           'https://www.allrecipes.com/search/results/?wt=potato%20salad&sort=re']
            current_dict = get_recipe(recipe_type[recipe_site_num])
            recipe_num = randint(0, len(current_dict) - 1)
            share_recipe = current_dict[recipe_num]
            tb = TweetBot()
            tb.post('YUM!' + share_recipe.strip("'"))


try:
    Karen()
    complain()
except twitter.error.TwitterError:
    back_up = {1: 'God bless the troops and the law enforcement keeping us safe! #america',
               2: 'Living, Laughing, and Loving Life #blessed',
               3: '@BarefootWine Time for a glass of that delicious chardonnay :)'}
    tb = TweetBot()
    tb.post(back_up[randint(1, 3)])
except requests.exceptions.ConnectionError as e:
    with open('/home/pi/PiPy/karen_error.csv', 'a') as err_file:
        err_file.write(f'internet outage at {datetime.now()} \n')
except Exception as f:
    with open('/home/pi/PiPy/karen_error.csv', 'a') as err_file:
        err_file.write(str(f) + str(datetime.now()) + '\n')
