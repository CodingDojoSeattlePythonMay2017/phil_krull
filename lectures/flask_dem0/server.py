from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    print 'in index method'
    return 'Message from server'


app.run(debug=True)
