import os
import subprocess
from flask import Flask, render_template, request
from flask import Flask,render_template,request,redirect,url_for,flash
from flask import Flask,request,jsonify,render_template
import sqlite3 as sql
import subprocess
import getData
from sqlalchemy import true
app = Flask(__name__, template_folder="templtes")
path = os.path.dirname(os.path.abspath(__file__))


class Id:
    name = ""
    email = ""
    pin = ""

    def __init__(self, nameR, emailR, pinR):
        self.name = nameR
        self.email = emailR
        self.pin = pinR

id_list = []
worker_List = []
sms_List = []
ownerEmail = ""
ownerName = ""
ownerPin = ""

# Save Data of Owner


def saveDataOwner():
    global ownerEmail
    global ownerName
    global ownerPin
    file_path = path+'/data/dataOwner.txt'
    myfile = open(file_path, 'w')
    myfile.close()
    record = ownerName+","+ownerEmail+","+ownerPin
    myfile = open(file_path, 'a')
    print(record, file=myfile, sep="\n")
    myfile.close()

# Load Data of Owner


def loaddataOwner():
    global ownerName
    global ownerEmail
    global ownerPin
    file_path = path+'/data/dataOwner.txt'
    myfile = open(file_path, 'r')
    records = myfile.read().splitlines()
    name = ""
    email = ""
    password = ""
    i = 0
    for record in records:
        while(record[i] != ","):
            name = name + record[i]
            i = i+1
        i = i+1
        while(record[i] != ","):
            email = email + record[i]
            i = i+1
        i = i+1
        for x in range(i, len(record)):
            password = password + record[x]
    ownerName = name
    ownerEmail = email
    ownerPin = password

# Save Messages


def saveSms():
    global sms_List
    file_path = path+'/data/messages.txt'
    myfile = open(file_path, 'w')
    myfile.close()
    for sms in sms_List:
        record = sms
        myfile = open(file_path, 'a')
        print(record, file=myfile, sep="\n")
    myfile.close()


def loadSms():
    file_path = path+'/data/messages.txt'
    myfile = open(file_path, 'r')
    records = myfile.read().splitlines()
    for record in records:
        if record != "":
            sms_List.append(record)


@app.route("/")
def Page():
    return render_template("mainLoginPage.html")

# Banque Pages

@app.route("/login")
def login1():
    return render_template("Banque/login.html")




@app.route("/Banque")
def owner():
    return render_template("Banque/banque_populaire.html", variable=ownerEmail, residents=len(id_list), workers=len(worker_List))


@app.route("/Physiques")
def get():
    ObjectData=getData.getDatas()
    aData=ObjectData.getAllData()
    if len(aData):
        response=jsonify({
            "result":aData,
            "status":200,
        })
    else:
        response=jsonify({
            "result":[],
            "status":400,
        })
    return render_template('Banque/personnes_physiques.html',resp=aData)

@app.route("/espace/<id>")
def get_info_id(id):
    ObjectData=getData.getDatas()
    aData=ObjectData.getOne(id)
    aData2=ObjectData.get_doc_user(id)
    return render_template("espaces.html",info=aData,info_docs=aData2)
    
@app.route("/sendMessage")
def sendMessageManager():
    global ownerEmail
    return render_template("Banque/sendMessageToManager.html", variable=ownerEmail)


@app.route("/recieveMessage")
def recieveMessageManager():
    global sms_List
    return render_template("Banque/recieveMessageOwner.html", variable=ownerEmail, smsList=sms_List)


@app.route("/Profession")
def ResidentsDetail():
    con=sql.connect("db_web.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from Files where Type !='Commerçant'")
    data=cur.fetchall()
    return render_template("Banque/Prof_lib.html", datas=data)


@app.route("/Files")
def Workers():
    con=sql.connect("db_web.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from Files where check1=1")
    data=cur.fetchall()
    return render_template("Banque/Files.html", datas=data)


@app.route("/Commerçant")
def MyownerRooms():
    con=sql.connect("db_web.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from files where Type='Commerçant'")
    data=cur.fetchall()
    return render_template("Banque/Commerçants.html", datas=data)

@app.route("/sendMessageByOwner", methods=['POST', 'GET'])
def smsSend():
    global ownerEmail
    if request.method == "POST":
        sms = request.form['sms']+",owner"
        sms_List.append(sms)
        saveSms()
    return render_template("Banque/sendMessageToManager.html", variable=ownerEmail)


@app.route("/Banque", methods=['POST', 'GET'])
def ownerVerfiy():
    password = request.form['pin']
    global MyEmail
    MyEmail = request.form['myemail']
    if verifyowner(MyEmail, password):
        return render_template("Banque/banque_populaire.html", variable=ownerEmail, residents=len(id_list), workers=len(worker_List))
    else:
        return render_template("Banque/login.html")


def verifyowner(email, password):
    global ownerEmail
    global ownerPin
    if email == ownerEmail and password == ownerPin:
        return True
    return False


@app.route("/profile")
def profile1():
    return render_template("Banque/profile.html", email=ownerEmail, name=ownerName, pin=ownerPin)

@app.route("/register")
def register():
    return render_template("Banque/register.html")

@app.route("/myregisterOwner", methods=['POST', 'GET'])
def createAcoount23():
    global ownerEmail
    global ownerName
    global ownerPin
    name = request.form['name1']+" "+request.form['name2']
    email = request.form['email']
    pin = request.form['password']
    ownerName=name
    ownerEmail=email
    ownerPin=pin
    saveDataOwner()
    return render_template("Banque/login.html")

@app.route("/forgotpinowner")
def Pin():
    return render_template("Banque/forgotpinowner.html")


@app.route("/changepasswordowner")
def loadchangepagepassword():
    global ownerEmail
    return render_template("Banque/changeownerpin.html", variable=ownerEmail)


@app.route("/changePinMyOwner", methods=['POST', 'GET'])
def changeownerMypin():
    global ownerEmail
    email = request.form['owneremail']
    pin = request.form['ownerpin']
    if(verifyemail(email, pin)):
        saveDataOwner()
        return render_template("Banque/banque_populaire.html", variable=ownerEmail, residents=len(id_list), workers=len(worker_List))
    else:
        return render_template("Banque/changeownerpin.html", variable=ownerEmail)


@app.route("/frogotPinOwner", methods=['POST', 'GET'])
def changeMyOwnerPassword():
    email = request.form['myemail']
    password = request.form['pin']
    if verifyemail(email, password):
        saveDataOwner()
        return render_template("Banque/login.html")
    else:
        return render_template("Banque/forgotpinowner.html")


def verifyemail(email, password):
    global ownerEmail
    global ownerPin
    if email == ownerEmail:
        ownerPin = password
        return True
    return False


if __name__ == "__main__":
    loaddataOwner()
    loadSms()
    app.run(debug=True,host="0.0.0.0")
