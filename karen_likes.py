from Karen_bot3 import Karen
import sys
from datetime import datetime


class KarenLikes(Karen):

    def __init__(self, search_term, count_num):
        super().__init__()
        users = self._twitter_api.GetSearch(term=search_term, count=count_num, include_entities=True, return_json=True)
        ids = {}
        for status in users['statuses']:
            if status['user']['id'] not in ids:
                ids[status['user']['id']] = status['id']
        self._ids = ids

    @property
    def get_ids(self):
        return self._ids

    def like_posts(self):
        liked = self.check_likes()
        for user, status in self._ids.items():
            if status not in liked:
                self._twitter_api.CreateFavorite(status_id=status)

    def comment_on_posts(self, tweet):
        commented_users = self.check_comments()
        for user_id, status in self._ids.items():
            if user_id not in commented_users:
                self._twitter_api.PostUpdate(tweet,
                                             in_reply_to_status_id=status,
                                             auto_populate_reply_metadata=True)

    def check_likes(self):
        check_likes = self._twitter_api.GetFavorites(screen_name='KarenVsManager', return_json=True)
        liked = []
        for status in check_likes:
            liked.append(status['id'])
        return liked

    def check_comments(self):
        check_comments = self._twitter_api.GetReplies()
        commented_users = []
        for status in check_comments:
            if 'in_reply_to_user_id' in status.AsDict():
                commented_users.append(status.AsDict()['in_reply_to_user_id'])
        return commented_users


if __name__ == '__main__':
    try:
        action = sys.argv[1]
        if action == 'comment':
            kc = KarenLikes('Karens gone wild', 2)
            kc.comment_on_posts("I'll be speaking to the manager!")
        elif action == 'like':
            kl = KarenLikes('Karens gone wild', 10)
            kl.like_posts()
    except Exception as f:
        with open('karen_error.txt', 'a') as err_file:
            err_file.write(str(f) + str(datetime.now()) + '\n')

