# 89memes - A Very Meme Phone Tree

Explore an index of historically popular memes by calling 1-833-89MEMES 

This project was spawned from a desire to build something with the [Flask](http://flask.pocoo.org/) microframework for Python. It uses the sqlite3 interface to store and access the app's data, and JSON to hold an index of initial data objects.

89memes uses the [Twilio API](https://twilio.com). It takes advantage of incoming phone call web hooks, text-to-speech, SMS, and DTMF input tones. 

The memes are indexed in [`memedex.json`](https://github.com/e-ht/89memes/blob/master/memedex.json), please feel free to PR additional objects and Twilio interactions.

### JSON format

`memeobject`'s are options for Twilio actions. A random list item will be chosen from each object type.

```
{
  "Meme Name": {
    "intro": "Text that is read to introduce the meme.",
    "memeobjects": {
      "text2speech": [
        "wow, so scare. many memes.",
        "such phone call. Many fren."
      ],
      "sms": [
          "SMS text that will be sent"
      ],
      "mms": [
          "Only use MMS if your Twilio Phone number supports it."
      ],
      "audio": ["URL_to_mp3_file.mp3"]
    }
  }
```


### Build

Use [pipenv](https://github.com/pypa/pipenv) to manage this projects VM and dependencies. The `requirements.txt` is only there for deploying to AWS with ease.

* Build the sqlite schema with `python build_schema.py`. This will also parse `memedex.json` and insert the meme data into the new database.
* Start the Flask app and start accepting incoming phone calls with `python application.py`.

For local testing with the Twilio API I recommend using [https://ngrok.com/](https://ngrok.com/)


## Deployment

Deployment to AWS Elastic Beanstalk is as easy as:

```
fizz@buzz~/89memes$ eb init
fizz@buzz~/89memes$ eb create 89memes
fizz@buzz~/89memes$ eb open
```
If you insist on using the localized sqlite database you will need to SSH into your instance and manually build your schema for each deployment.


## Built With

* [Python](https://www.python.org/)
* [Flask](http://flask.pocoo.org/)
* [SQLite](http://www.sqlite.org)
* [JSON](http://json.org/)
* [Twilio](https://twilio.com/)
* [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/)

