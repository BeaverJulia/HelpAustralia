from flask import Flask, render_template, request, redirect, url_for
from bson import ObjectId
from pymongo import MongoClient
import os
from datetime import datetime

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.HelpAustralia
donations = db.donations
goal=70000

@app.route("/")
def main():
    return render_template('index.html')

def percent():
    amount=0
    allDonations = donations.find()
    for i in allDonations:
       amount+=int(i["amount"])

    return amount

def GetAll():
    allDonations = donations.find()
    return (allDonations)

def HowMuchWeHave(howmuchwehave):

    allTogether=howmuchwehave
    p=0
    p = int(allTogether * 100 / goal)
    if p>100:
        return 100
    else:
        return p

@app.route("/donate", methods=["GET", "POST"])
def Donate():
    allamount=percent()
    all=GetAll()
    howMuch=HowMuchWeHave(allamount)
    if request.method == "POST":
        Name = request.form.get("name")
        Amount = request.form.get("Amount")
        Email = request.form.get("email")
        Country = request.form.get("country")
        date = str(datetime.today())
        donations.insert_one({"name": Name, "amount": Amount, "date": date, "email": Email, "country": Country})
        allamount = percent()
        howMuch = HowMuchWeHave(allamount)
        return render_template("donations.html", allamount=allamount, p=howMuch, all=all)
    else:
        return render_template("single-causes.html", allamount=allamount, p=howMuch)

@app.route("/alldonations",  methods=["GET"])
def allDonations():
    allamount = percent()
    all = GetAll()
    howMuch = HowMuchWeHave(allamount)
    return render_template("donations.html", allamount=allamount, p=howMuch, all=all)




