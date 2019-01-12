import os
from flask import Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
from multiprocessing import Value
import time
import re
import random 
import simpleaudio as sa
from flask_bootstrap import Bootstrap

AUDIO_PATH="~/audio"

bp = Blueprint('index', __name__, url_prefix='/')

counter = Value('i', 0)

# Main page route, if POST then play audio
@bp.route( '/', methods=['GET', 'POST'] )
def index():
    if request.method == 'POST':
        # Make sure the button was pushed...
        if request.form[ 'shush' ] == 'shush':
            # Make sure we don't play audio from 2 separate threads
            curTime = time.time()
            # Mutex lock
            with counter.get_lock():
                timeSince = curTime - counter.value
                print("has been %d and last %d" %(timeSince, counter.value  ))
                # If 5 seconds have passed, reset the counter and continue
                if curTime - counter.value > 5.0:
                    print( "Setting to 0..." )
                    counter.value = 0
                if counter.value == 0:
                    # Find viable audio files from the data folder
                    audioFiles = os.listdir( AUDIO_PATH )
                    audioFiles = [ a for a in audioFiles if re.match( r'.*\.wav', a, re.IGNORECASE ) ]
                    # Take a random file
                    randL = random.sample( audioFiles, 1 )
                    audioPath = randL[ 0 ]
                    try:
                        # Play the file
                        wavePath = os.path.join( AUDIO_PATH, audioPath )
                        wave_obj = sa.WaveObject.from_wave_file(wavePath )
                        play_obj = wave_obj.play()
                        counter.value = int( curTime )
                    except Exception as e:
                        print( "No luck.... %s" % str( e ) )
                else:
                    print( "Already running..." )
                
    # Always render the same template
    return render_template('index.html')



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='ThisIsAWebAudPassword',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #from . import db
    #db.init_app(app)

    app.register_blueprint( bp )
    bootstrap = Bootstrap( app )

    return app

