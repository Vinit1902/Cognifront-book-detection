from flask import Flask, render_template ,Response
from cami import Video
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(cami):
    while True:
        frame=cami.get_frame()
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')

@app.route('/video')

def video():
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/ans')
def ans():
    return render_template('final.html',Result=Video.Answer1)


app.run(debug=True)