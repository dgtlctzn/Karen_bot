from Karen_bot3 import Karen
from pprint import pprint


class KarenLikes(Karen):

    def __init__(self):
        super().__init__()
        users = self._twitter_api.GetSearch(term='Karen gone wild', count=20, include_entities=True, return_json=True)
        ids = []
        for status in users['statuses']:
            ids.append(status['id'])
        self._ids = ids

    @property
    def get_ids(self):
        return self._ids

    def comment_on_posts(self, tweet):
        # for user in self._ids:
        self._twitter_api.PostUpdate(tweet,
                                     in_reply_to_status_id=1315323519857762317,
                                     auto_populate_reply_metadata=True)


if __name__ == '__main__':
    kl = KarenLikes()
    pprint(kl.comment_on_posts("I need to speak to the manager!"))

# dgtlctzn = 1860955230
