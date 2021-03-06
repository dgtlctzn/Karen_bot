from markovify import Text, combine
from random import randint
from nltk import sent_tokenize
import pickle
import twitter
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


class Karen:

    def __init__(self):
        twitter_keys = pickle.load(open('karen_secret_twitter_credentials.pkl', 'rb'))
        twitter_api = twitter.api.Api(consumer_key=twitter_keys['Consumer Key'],
                                      consumer_secret=twitter_keys['Consumer Secret'],
                                      access_token_key=twitter_keys['Access Token'],
                                      access_token_secret=twitter_keys['Access Token Secret'],
                                      tweet_mode='extended')
        self._twitter_api = twitter_api

    def post(self, tweet):
        self._twitter_api.PostUpdate(tweet)

    def re_tweet(self, user):
        api = self._twitter_api
        retweet = api.GetUserTimeline(user, count=1)
        retweet_id = retweet[0].AsDict()['id']
        api.PostRetweet(retweet_id)

    @staticmethod
    def make_model(file, read_type='rt'):
        with open(file, read_type) as txt_file:
            raw_text = txt_file.read()
            corpora = sent_tokenize(raw_text)
            text_model = Text(corpora)
        return text_model

    @staticmethod
    def add_reviews(one_start_url, file_nm):
        page = requests.get(one_start_url)

        soup = BeautifulSoup(page.content, 'html.parser')
        tags = soup.find_all('span', class_='lemon--span__373c0__3997G raw__373c0__3rKqk')

        with open(file_nm, 'a') as karen_txt:
            for tag in tags:
                karen_txt.write(tag.text + '\n')

    def bad_review(self, review_text, structure_text, chains, weight=(1, 10)):
        hashtags = [' #disappointing', ' #crap', ' #nevercomingback', ' #theworst', ' #livelaughlove...andleave',
                    ' #neveragain', ' #unacceptable', ' #badservice', ' #takemybusinesselsewhere', ' #outrageous']
        hash_num_1 = randint(0, 9)
        hash_one = hashtags[hash_num_1]
        hash_two = hashtags[hash_num_1 - randint(1, 3)]

        model_1 = self.make_model(review_text)
        model_2 = self.make_model(structure_text)

        combo_model = combine([model_1, model_2], weight)

        restaurant_sent = combo_model.make_short_sentence(80, min_chars=60, tries=100)
        my_tweet = "I'd like to speak to the manager. " + chains[randint(1, 8)] + ' ' + restaurant_sent + hash_one \
                   + hash_two + ' #karen' + ' #karensgonewild'
        return my_tweet

    @staticmethod
    def get_recipe(url):
        my_url = url
        page = requests.get(my_url)

        soup = BeautifulSoup(page.content, 'html.parser')
        tags = soup.find_all('div', class_='fixed-recipe-card__info')

        return [re.search(r'https(.*)/', str(tag)).group() for tag in tags]

    def complain(self):
        number = randint(1, 4)
        if number == 1:
            chains = {1: "@Chilis", 2: "@olivegarden", 3: "@Applebees", 4: '@Cheesecake', 5: "@Carrabbas",
                      6: "@PFChangs", 7: "@Maggianos", 8: "@redlobster"}
            text_1 = './text/Karen_text2.txt'
            text_2 = './text/Karen_rest_structure.txt'
            self.post(self.bad_review(text_1, text_2, chains))
        elif number == 2:
            chains = {1: "@Sephora", 2: "@Target", 3: "@jcpenney", 4: "@tjmaxx", 5: "@marshalls",
                      6: "@Walmart", 7: "@Bloomingdales", 8: "@Macys"}
            text_1 = './text/Karen_retail2.txt'
            text_2 = './text/Karen_retail_structure.txt'
            self.post(self.bad_review(text_1, text_2, chains))
        elif number == 3:
            user_list = [31869934, 22650211, 2370627199, 26031542, 22515362]
            user_number = randint(0, 4)
            self.re_tweet(user_list[user_number])
        else:
            recipe_site_num = randint(0, 2)
            recipe_type = ['https://www.allrecipes.com/search/results/?ingIncl=ranch&sort=re',
                           'https://www.allrecipes.com/search/results/?ingIncl=bacon&sort=re',
                           'https://www.allrecipes.com/search/results/?wt=potato%20salad&sort=re']
            current_list = self.get_recipe(recipe_type[recipe_site_num])
            recipe_num = randint(0, len(current_list) - 1)
            share_recipe = current_list[recipe_num]
            self.post('YUM!' + share_recipe)


if __name__ == '__main__':
    try:
        karen = Karen()
        karen.complain()
    except twitter.error.TwitterError:
        back_up = {1: 'God bless the troops and the law enforcement keeping us safe! #america',
                   2: 'Living, Laughing, and Loving Life #blessed',
                   3: '@BarefootWine Time for a glass of that delicious chardonnay :)'}
        ken = Karen()
        ken.post(back_up[randint(1, 3)])
    except requests.exceptions.ConnectionError as e:
        with open('karen_error.txt', 'a') as err_file:
            err_file.write(f'internet outage at {datetime.now()} \n')
    except Exception as f:
        with open('karen_error.txt', 'a') as err_file:
            err_file.write(str(f) + str(datetime.now()) + '\n')
