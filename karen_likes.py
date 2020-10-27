from Karen_bot3 import Karen
import sys
from datetime import date
from random import randint


class SuperKaren(Karen):

    def __init__(self, search_term, count_num):
        super().__init__()
        users = self._twitter_api.GetSearch(term=search_term, count=count_num, since=date.today(),
                                            include_entities=True, return_json=True)
        ids = {}
        for status in users['statuses']:
            if status['user']['id'] not in ids:
                ids[status['user']['name']] = status['id']
        self._ids = ids

    @property
    def get_ids(self):
        return self._ids

    def like_posts(self):
        for user, status in self._ids.items():
            # can't like your own posts...
            if user != 'Karen Bot 💁🏼':
                self._twitter_api.CreateFavorite(status_id=status)

    def comment_on_posts(self, tweet):
        for user, status in self._ids.items():
            # can't like your own posts...
            if user != 'Karen Bot 💁🏼':
                self._twitter_api.PostUpdate(tweet,
                                             in_reply_to_status_id=status,
                                             auto_populate_reply_metadata=True)

    @classmethod
    def comment_message(cls):
        messages = ["Reported!!!",
                    "I'll be speaking to the manager about this!",
                    "I have the right and freedom to complain as a proud American!"]
        random_num = randint(0, 2)
        return cls('Karensgonewild', 10).comment_on_posts(messages[random_num])


if __name__ == '__main__':
    try:
        action = sys.argv[1]
        if action == 'comment':
            SuperKaren.comment_message()
        elif action == 'like':
            kl = SuperKaren('Karensgonewild', 20)
            kl.like_posts()
    except Exception as f:
        with open('karen_error.txt', 'a') as err_file:
            err_file.write(str(f) + " " + str(date.today()) + '\n')
