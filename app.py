import os
import sqlite3

from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.voice_response import Gather, VoiceResponse

# Twilio rest credentials
account_sid = os.environ['twilio_account_sid']
auth_token = os.environ['twilio_auth_token']

application = app = Flask(__name__)


@app.route('/answer', methods=['GET', 'POST'])
def answer_call():
    conn = sqlite3.connect('meme.db')
    c = conn.cursor()
    # Create Gather and VoiceResponse objects
    resp = VoiceResponse()
    gather = Gather()
    # Check if we have any digits posted from user interaction
    if 'Digits' in request.values:
        digits = int(request.values['Digits'])
        # Select a meme at random
        gather.say('One tasty meme coming right up!')
        if digits == 0:
            memeselect = c.execute(
                'SELECT * FROM memes WHERE id IN (SELECT id FROM memes ORDER BY RANDOM() LIMIT 1)')
        else:
            # Grab meme by meme id
            memeselect = c.execute(
                'SELECT * FROM memes WHERE id = ?', [digits])
        memedata = memeselect.fetchall()
        if memedata:
            for row in memedata:
                memeid = row[0]
                memename = row[1]
                memeintro = row[2]
                # Play meme intro
                gather.say("Meme extension number {}, {}. {}.".format(
                    memeid, memename, memeintro))
                # Play a text2speech object
                c.execute('SELECT text  FROM memeobjects WHERE memeid = ? AND type = ? ORDER BY RANDOM() LIMIT 1', [
                          memeid, 'text2speech'])
                speechobject = c.fetchall()
                if speechobject:
                    gather.say("Consider the following mee mee: {}".format(
                        speechobject[0][0]))
                # Check if there is an sms or MMS to send
                c.execute('SELECT text FROM memeobjects WHERE memeid = ? AND type = ? ORDER BY RANDOM() LIMIT 1', [
                          memeid, 'sms'])
                smsobject = c.fetchall()
                if smsobject:
                    send_to = request.values['From']
                    send_from = request.values['To']
                    sms_client = Client(account_sid, auth_token)
                    sms_client.api.account.messages.create(
                        to=send_to,
                        from_=send_from,
                        body=smsobject[0][0])
                # Check if there is an audio file to play
                c.execute('SELECT text FROM memeobjects WHERE memeid = ? AND type = ? ORDER BY RANDOM() LIMIT 1', [
                          memeid, 'audio'])
                audioobject = c.fetchall()
                if audioobject:
                    resp.play(audioobject[0][0], loop=10)

        else:
            gather.say(
                "We have not caught this may may yet. Please stand by while we 'gotta catch them all!")
        # Post loop
        gather.pause(length=2)
        gather.say(
            "To enjoy another random me me, press cero, followed by the pound sign.", voice='woman')
        gather.say(
            "If you already know your me mes extension, you may dial it at any time followed by the pound sign.")
        gather.pause(length=5)
    # Play intro
    gather.say(
        "Thank you for calling 89 memes. I am your host, Louie Louie. ...And here we go a' memeing!")
    gather.say(
        "If you already know your me mes extension, you may dial it at any time followed by the pound sign.")
    gather.say(
        "To enjoy a random mee mee, press cero, followed by the pound sign.", voice='woman')
    resp.append(gather)

    return str(resp)


if __name__ == '__main__':
    app.run(debug=True)
