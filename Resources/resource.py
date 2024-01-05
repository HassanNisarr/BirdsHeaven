from flask import Response,request,render_template,session,json
from flask_restful import Resource
from Database.model import Credentials,Birdsdb, ForSale


class RegisterApi(Resource):
    def post(self):
        try:
            uname = request.form["uname"]
            password = request.form["password"]
            user_type = request.form["type"]
            Credentials(type=user_type,uname=uname, password=password).save()
            return Response(render_template("Login.html", message="Successfully Registered!"),200)
        except Exception as e:
            return Response(render_template("SignUp.html", message="Not Registered!"))


class LoginApi(Resource):
    def post(self):
        try:
            uname = request.form["uname"]
            password = request.form["password"]
            user_type = request.form["type"]
            user = Credentials.objects(type= user_type,uname=uname,password=password)
            if user and user_type == "Breeder":
                session["uname"] = uname
                session["type"] = user_type
                return Response(render_template("Dashboard.html", user=uname),200)
            elif user and user_type == "Buyer":
                session["type"] = user_type
                return Response(render_template("home.html", uname=uname),200)
            else:
                return Response(render_template("Login.html", message="Invalid Credentials!"))
        except Exception as e:
            return Response(render_template("Login.html", message="Error!"))


class BirdsAPI(Resource):
    def get(self):
        uname = session["uname"]
        bird = Birdsdb.objects(uname=uname).to_json()
        return Response(bird, mimetype="application/json", status=200)

    def post(self):
        try:
            ringno = request.form["ringno"]
            specie = request.form["specie"]
            mutation = request.form["mutation"]
            age = request.form["age"]
            gender = request.form["gender"]
            uname = session.get("uname")

            Birdsdb(ringno=ringno,uname=uname, specie=specie, mutation=mutation, age=age, gender=gender).save()

            return Response(render_template("Dashboard.html", message="Successfully Entered!"), 200)

        except Exception as e:
            return Response(render_template("AddBirds.html", message=" Insertion Failed"),400)


class BirdCRUDAPI(Resource):
    def post(self):
        try:
            ringno = request.form["ringno"]
            uname = session.get("uname")
            bird = Birdsdb.objects.get(ringno = ringno,uname = uname)
            if bird:
                specie = request.form["specie"]
                mutation=request.form["mutation"]
                age = request.form["age"]
                gender = request.form["gender"]
                Birdsdb.objects.get(ringno=ringno).update(specie=specie,mutation=mutation,age = age,gender=gender)
                return Response(render_template("Dashboard.html",message="Successfully Updated"),200)
            else:
                return Response(render_template("UpdateBirds.html",message="Bird Not Found!"))
        except Exception as e:
            return Response(render_template("UpdateBirds.html",message="Bird Not Found!"))


class BirdsShop(Resource):
    def get(self):
        bird = ForSale.objects().to_json()
        return Response(bird, mimetype="application/json", status = 200)
