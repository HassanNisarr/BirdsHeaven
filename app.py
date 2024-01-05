from flask import Flask,render_template,session,request,json
from flask_restful import Api
from Database import db
from Resources import routes
from Database.model import Birdsdb,ForSale
app = Flask(__name__)
app.secret_key="122344fggdas"
app.config['MONGODB_SETTINGS'] = {'host':'mongodb://localhost:27017/BirdsHeaven'}
db.initialize_db(app)
api = Api(app)
routes.initialize_routes(api)


@app.route("/displaySignUp")
def signup():
    return render_template("SignUp.html")


@app.route("/displayLogin")
def login():
    return render_template("Login.html")

@app.route("/displayAddBird")
def displayAddBird():
    if session["type"] == "Breeder":
        return render_template("AddBirds.html")


@app.route("/displayUpdate")
def updateBird():
    if session["type"] == "Breeder":
        return render_template("UpdateBirds.html")

@app.route("/displayDelete")
def displayDelete():
    if session["type"] == "Breeder":
        return render_template("DeleteBird.html")

@app.route("/displayProduct")
def displayProduct():
    return render_template("displaySale.html")

@app.route("/signout")
def signout():
    session.clear()
    return render_template("Login.html")

@app.route("/display")
def display():
    if session["type"] == "Breeder":
        return render_template("DisplayBird.html")

@app.route("/displayDashboard")
def displayDashboard():
    if session["type"] == "Breeder":
        return render_template("Dashboard.html",user=session["uname"])

@app.route("/displayForSale")
def displayForSale():
    if session["type"] == "Breeder":
        return render_template("ForSale.html")

@app.route("/displayRemoveForSale")
def removeForSale():
    if session["type"] == "Breeder":
        return render_template("RemoveFromSale.html")

@app.route("/deleteBird", methods=["GET","POST"])
def deleteBird():
    try:
        ringno = request.form["ringno"]
        uname = session["uname"]
        bird = Birdsdb.objects.get(ringno=ringno, uname=uname)
        if bird:
            Birdsdb.objects.get(ringno=ringno).delete()
            return render_template("Dashboard.html", message="Successfully Deleted!",user=session["uname"])
        else:
            return render_template("DeleteBird.html", message="Bird Not Found!")
    except Exception as e:
            return render_template("Dashboard.html", message="Bird Not Found",user=session["uname"])

@app.route("/addForSale",methods=["POST"])
def addForSale():
    try:
        ringno = request.form["ringno"]
        price = request.form["price"]
        uname = session["uname"]
        bird = Birdsdb.objects(ringno=ringno, uname=uname).to_json()
        exist = ForSale.objects(ringno = ringno)
        bird = json.loads(bird)
        bird = bird[0]
        if bird:
            if not exist:
                ForSale(ringno = bird["_id"],uname=bird["uname"], specie=bird["specie"], mutation=bird["mutation"], age = bird["age"], gender=bird["gender"],price=price).save()
                return render_template("Dashboard.html",message="Successfully Added to For Sale!",user=session["uname"])
            else:
                return render_template("ForSale.html",message="Bird Already Exist!")
        else:
            return render_template("Dashboard.html", message="Bird Not Found",user=session["uname"])
    except Exception as e:
        return render_template("Dashboard.html", message=str(e),user=session["uname"])

@app.route("/removeFromSale", methods=["GET","POST"])
def removeFromSale():
    try:
        ringno = request.form["ringno"]
        uname = session["uname"]
        bird = ForSale.objects.get(ringno=ringno, uname=uname)
        if bird:
            ForSale.objects.get(ringno=ringno).delete()
            return render_template("Dashboard.html", message="Successfully Deleted!",user=session["uname"])
        else:
            return render_template("DeleteBird.html", message="Bird Not Found!")
    except Exception as e:
            return render_template("Dashboard.html", message="Bird Not Found",user=session["uname"])

if __name__ == '__main__':
    app.run()
