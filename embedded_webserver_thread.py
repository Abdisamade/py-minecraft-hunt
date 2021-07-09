from flask import Flask, request, render_template
from threading import Thread
from new_hunt import NewHunt
from models import Item, Elem, Block, Mob

app = Flask(__name__)
FLASK_PORT = 5245
FLASK_HOME_URL = "http://127.0.0.1:"+str(FLASK_PORT)
FLASK_SHUTDOWN_ENDPOINT = FLASK_HOME_URL+"/shutdown"

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


@app.route('/')
def hello_world():
    return render_template('index.html', user="Abdisamade")


@app.route('/generate/<level>')
def generates(level):

    level = int(level)
    new_hunt = NewHunt()

    new_hunt.connect()
    mobs = new_hunt.getList(Mob, 5, level)
    items = new_hunt.getList(Item, 5, level)
    blocks = new_hunt.getList(Block, 5, level)

    difficulty = 0
    for mob in mobs:
        difficulty += mob.level
    for item in items:
        difficulty += item.level
    for block in blocks:
        difficulty += block.level

    difficulty /= (len(mobs)+len(items)+len(blocks))

    return render_template('generate.html', items= items, blocks= blocks, mobs = mobs, difficulty=difficulty)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

class FlaskThread(Thread):
    def __init__(self):      # jusqua = donnée supplémentaire
        Thread.__init__(self)  # ne pas oublier cette ligne

    def run(self):
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        app.run(port=FLASK_PORT, host='0.0.0.0')
