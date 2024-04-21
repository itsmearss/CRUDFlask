from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask import jsonify

class Base(DeclarativeBase): 
    pass #Blank body class, but "Base" class inherits "DeclarativeBase" class

app = Flask(__name__) # Instantiate Flask
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@127.0.0.1/webservices2"  #"mysql://username:password@localhost/databasename"  
db = SQLAlchemy(model_class=Base) # Instantiate SQLALchemy
db.init_app(app)

class User(db.Model): #User class inherit Model class
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    password: Mapped[str]

@app.route("/user", methods=['GET','POST','PUT','DELETE'])
def user():
    if request.method == 'POST':
        dataDict = request.get_json() #It return dictionary.
        email = dataDict["email"]
        name = dataDict["name"]
        password = dataDict["password"]
        
        user = User(
            email= email,
            name = name,
            password = password
        )
        
        db.session.add(user)
        db.session.commit()
        
        return {
            "message": "Successfull, data telah ditambahkan",
        }, 200 
        
        
    elif request.method == 'PUT':
        dataDict = request.get_json() #It return dictionary.
        id = dataDict["id"]
        email = dataDict["email"]
        name = dataDict["name"]
        password = dataDict["password"]
        
        if not id:
            return {
                "message": "ID required"
            },400
        
        row = db.session.execute(
            db.select(User) #Select from user model
            .filter_by(id=id) #where ID=1  by id
            ).scalar_one() # Return a list of rows.
        
        if "email" in dataDict : 
            row.email = dataDict["email"]
            
        if "name" in dataDict :
            row.name = dataDict["name"]
            
        if "password" in dataDict :
            row.password = dataDict["password"]
            
        db.session.commit()
        return {
            "message": "Successfull!"
        }, 200
        
    elif request.method == 'DELETE':
        dataDict = request.get_json() #It return dictionary.
        id = dataDict["id"]
        
        if not id:
            return {
                "message": "ID required"
            },400
        
        row = db.session.execute(
            db.select(User) #Select from user model
            .filter_by(id=id) #where ID=1  by id
            ).scalar_one() # Return a list of rows.
        
        db.session.delete(row)
        db.session.commit()
        return {
            "message": "Successfull!"
        }, 200
        
    else : #GET
        rows = db.session.execute(
            db.select(User).order_by(User.id)
            ).scalars()
        
        print(rows)
        
        users =[]
        for row in rows:
            users.append({
                "id" : row.id,
                "email" : row.email,
                "name" : row.name,
            })
            
        print(users)
        return users, 200

if __name__ == '__main__':
    app.run(debug=True)