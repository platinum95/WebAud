from flask import Flask, request, render_template
import simpleaudio as sa
import re
import random
import os

app = Flask( __name__ )

@app.route( '/', methods=['GET', 'POST'] )
def hello():
    if request.method == 'POST':
        if request.form['shush'] == 'shush':
            print( "We doin summit" )
            audioFiles = os.listdir( './audio' )
            audioFiles = [ a for a in audioFiles if re.match( r'.*\.wav', a, re.IGNORECASE ) ]
            randL = random.sample( audioFiles, 1 )
            audioPath = randL[ 0 ]
            print( audioPath )
            try:
                wave_obj = sa.WaveObject.from_wave_file( os.path.join( "./audio", audioPath ) )
                play_obj = wave_obj.play()
                play_obj.wait_done()
            except:
                print( "No luck...." )
                

    return render_template('index.html')
