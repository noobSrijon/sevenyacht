#simple flask load index.html
from flask import Flask, render_template, request, jsonify,url_for,redirect
from config import DevelopmentConfig
import pymongo
import requests
import certifi
from func import *
import threading

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.secret_key = app.config['SECRET_KEY']

client = pymongo.MongoClient(
    app.config['DATABASE_URI'],
    ,tlsCAFile=certifi.where()
)

db = client['yacht']

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit_form():

    booking_id=get_next_id(db.bookings)
  
    booking = {
        "_id": booking_id,
        "yacht_name": request.form["matrix"],
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "phone": request.form.get("phone"),
        "date": request.form.get("date"),
        "time": request.form.get("time"),
        "charterLength": request.form.get("charter-length")
    }

    channel_id = 344585
    api_token = app.config['API']

    db.bookings.insert_one(booking)

    threading.Thread(target=send_whatsapp_message, args=(booking['phone'], booking['name'], 'en', 'BD', booking, channel_id, api_token)).start()

    return redirect(url_for('bookingsent'))
    

@app.route('/booking-sent')
def bookingsent():
    return render_template('requestsent.html')

if __name__ == '__main__':
    app.run(debug=True)