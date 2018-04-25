import json
import sqlite3

# Create a database and connect to it.
conn = sqlite3.connect('meme.db')
c = conn.cursor()

## Create tables
c.execute('''
    CREATE TABLE memes(
        id INTEGER PRIMARY KEY, name TEXT, intro TEXT, score INTEGER
    )
''')

c.execute('''
    CREATE TABLE memeobjects(
        id INTEGER PRIMARY KEY, memeid INTEGER, text TEXT, type TEXT, play_count INTEGER,
        FOREIGN KEY(memeid) REFERENCES memes89(id)
    )
''')
# Open the JSON structure containing our glorious memes
with open('memedex.json') as json_data:
    meme_struct = json.load(json_data)
    # Insert memes and memes data
    for meme, memeindex in meme_struct.items():
        print("Meme: {}".format(meme))
        c.execute('''
            INSERT INTO memes (
                name,
                intro,
                score
            )
            VALUES (
                ?,
                ?,
                ?
            )
        ''', [meme, memeindex['intro'], 0])
        insert_id = c.lastrowid
        conn.commit()

        # # Insert objects for meme
        for memetype, typeindex in memeindex['memeobjects'].items():
            # print("Meme type: {}".format(memetype))
            # print("Type index: {}".format(typeindex))
            for memeobject in typeindex:
                c.execute('''
                    INSERT INTO memeobjects (
                        memeid,
                        text,
                        type,
                        play_count
                    )
                    VALUES (
                        ?,
                        ?,
                        ?,
                        ?
                    )
                ''', [insert_id, memeobject, memetype, 0])
                conn.commit()
