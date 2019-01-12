from flask import Flask, request, render_template
import simpleaudio as sa



app = Flask( __name__ )

@app.route( '/', methods=['GET', 'POST'] )
def hello():
    if request.method == 'POST':
        if request.form['shush'] == 'shush':
            print( "We doin summit" )
            wave_obj = sa.WaveObject.from_wave_file("test.wav")
            play_obj = wave_obj.play()
            play_obj.wait_done()

    return render_template('index.html')
