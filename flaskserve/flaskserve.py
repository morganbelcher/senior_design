from flask import Flask, Response, render_template
import pandas as pd
import os

# To initialize flask
# export FLASK_APP=flaskserve
# export FLASK_ENV=development
# flask run --host=0.0.0.0

app = Flask(__name__)
abspath = os.path.dirname(os.path.abspath(__file__)) + "/"


@app.route("/")

def hello_world():
    
    c = pd.read_csv(abspath + "FaceReqData.csv")
    table = c.to_html(index=False)

    return render_template('base.html', table=table)
    
# This can probably be deleted


@app.route("/download")
def download():
    c = pd.read_csv(abspath + "FaceReqData.csv")
    return Response(c.to_csv(), mimetype="text/csv", headers = {"Content-disposition": "attachment; filename=FaceReqData.csv"})
