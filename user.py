import uuid

from mood import Mood


class User:
    def __init__(self, user_uuid=uuid.uuid4, name='', email='', moods=None, contacts=None, feed=None):
        moods = [] if not moods else moods
        contacts = [] if not contacts else contacts
        feed = [] if not feed else feed
        self.uuid = str(user_uuid())
        self.name = name
        self.email = email
        self.moods = moods
        self.contacts = contacts
        self.feed = feed

    def get_dictionary(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'email': self.email,
            'moods': self.moods,
            'contacts': self.contacts,
            'feed': self.feed
        }

    @classmethod
    def from_document(cls, doc):
        user_uuid = doc.get('uuid')
        name = doc.get('name')
        email = doc.get('email')
        moods = []
        for mood in doc.get('moods'):
            moods.append([Mood.from_doc(mood)])
        contacts = doc.get('contacts')
        feed = doc.get('feed')
        return cls(user_uuid, name, email, moods, contacts, feed)
