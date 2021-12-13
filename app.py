import datetime
import utilities

from flask import Flask, request
from pymongo import ReturnDocument
from mood import Mood
from user import User

app = Flask(__name__)


@app.route('/api/new-user', methods=['POST'])
def add_new_user():
    name = request.form.get('name')
    email = request.form.get('email')
    if name and email:
        possible_user = utilities.find_user_doc(email=email)

        if not possible_user:
            user = User(name=name, email=email)
            utilities.get_user_collection().insert_one(user.get_dictionary())
            return 'Success'
        return 'Duplicate User - Not creating new user'
    return 'Must provide a name and email for the new user'


@app.route('/api/add-contact', methods=['POST'])
def add_new_contact():
    user_uuid = request.form.get('user_uuid')
    contact_email = request.form.get('contact_email')  # TODO Encrypt this
    contact_doc = utilities.find_user_doc(email=contact_email)
    contact_uuid = contact_doc.get('uuid')

    if user_uuid and contact_uuid and user_uuid != contact_uuid:
        updated_user = utilities.get_user_collection().find_one_and_update(
            {'uuid': user_uuid},
            {'$addToSet': {'contacts': contact_uuid}},
            return_document=ReturnDocument.AFTER
        )
        utilities.get_user_collection().find_one_and_update(
            {'uuid': contact_uuid},
            {'$addToSet': {'feed': user_uuid}},
            return_document=ReturnDocument.AFTER
        )
        return str(updated_user)
    return 'Error'


@app.route('/api/add-mood', methods=['POST'])
def add_new_mood():
    user_uuid = request.form.get('user_uuid')
    mood_text = request.form.get('mood')
    timestamp = datetime.datetime.utcnow().timestamp()
    if user_uuid and mood_text:
        mood = Mood(mood_text, timestamp)
        user = utilities.get_user_collection().find_one_and_update(
            {'uuid': user_uuid},
            {'$push': {'moods': {'$each': [mood.get_dictionary()], '$position': 0}}}
        )
        return str(user)
    # TODO Trigger updates here.
    return 'Error'


@app.route('/api/get-feed/<user_uuid>', methods=['GET'])
def get_feed(user_uuid):
    feed_users = utilities.get_user_collection().find({'contacts': user_uuid})
    feed_items = []
    for user in feed_users:
        name = user.get('name')
        items = [dict(item, **{'name': name}) for item in user.get('moods')]
        feed_items.append(items)
    feed_items = [item for sublist in feed_items for item in sublist]
    sorted_feed = sorted(feed_items, key=lambda d: float(d['timestamp']), reverse=True)
    return {'feed': str(sorted_feed)}


if __name__ == '__main__':
    app.run()
