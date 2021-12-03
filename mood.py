

class Mood:
    def __init__(self, mood='', timestamp=None):
        self.mood = mood
        self.timestamp = timestamp

    def get_dictionary(self):
        return {
            'mood': self.mood,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_doc(cls, doc):
        mood = doc.get('mood')
        timestamp = doc.get('mood')
        return cls(mood, timestamp)
