from flask import Flask, render_template, request, redirect, url_for, app
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)

# Configure DB:
db = pymysql.connect(host='database-2.clhatderacte.us-east-2.rds.amazonaws.com', 
user= 'root', 
password= 'root_rishab', 
port=3306, 
database='test', 
cursorclass=pymysql.cursors.DictCursor)
#app.secret_key = "Secret Key" # can be anything
# CONNECTING TO DB
# mysql:// user : password @localhost / databaseName
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:''@localhost/db"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# SQLAlc obejct
#db = SQLAlchemy(app)

# Table
# class StudentData(db.Model): # db.table_name ? 
#     f_name = db.Column(db.String(100)) # make Varcahr
#     l_name = db.Column(db.String(100)) # make Varcahr
#     roll_no = db.Column(db.String(20), primary_key = True) # make Varcahr
#     sub1_marks = db.Column(db.Integer) # make float
#     sub2_marks = db.Column(db.Integer) # make float
#     sub3_marks = db.Column(db.Integer) # make float

#     def __init__(self, f_name,l_name, roll_no, sub1_marks,sub2_marks,sub3_marks):
#         self.f_name = f_name
#         self.l_name = l_name
#         self.roll_no = roll_no
#         self.sub1_marks = sub1_marks
#         self.sub2_marks = sub2_marks
#         self.sub3_marks = sub3_marks

# class TeacherData(db.Model):
#     t_f_name = db.Column(db.String(100)) # make Varcahr
#     #m_name = db.Column(db.String(100))
#     t_l_name = db.Column(db.String(100)) # make Varcahr
#     email = db.Column(db.String(100)) # make Varcahr
#     #gender = db.Column(db.String(100))
#     username = db.Column(db.String(100), primary_key = True) # make Varcahr
#     password = db.Column(db.String(100)) # make Varcahr

#     def __init__(self, t_f_name, t_l_name, email, username, password):
#         self.t_f_name = t_f_name
#         #self.m_name = m_name
#         self.t_l_name = t_l_name
#         self.email = email
#         #self.gender = gender
#         self.username = username
#         self.password = password

# inserting student data from form to table
@app.route("/add_student", methods = ["POST"])
def insert_student():
    if request.method == "POST":
        f_name = request.form["first_name"]
        l_name = request.form["last_name"]
        email = request.form['email']
        password = request.form['password']
        # roll_no = request.form["roll_no"]
        # sub1_marks = request.form["sub1_marks"]
        # sub2_marks = request.form["sub2_marks"]
        # sub3_marks = request.form["sub3_marks"]
        # my_data = StudentData(f_name, l_name, roll_no, sub1_marks, sub2_marks,sub3_marks)
        # db.session.add(my_data)
        # db.session.commit()
        cur = db.cursor()
        cur.execute("INSERT INTO teacher VALUES('%s', '%s','%s','%s')"%(f_name, l_name, email, password))
        db.commit()
        cur.close()
        return redirect(url_for("account"))

# registering teachers
@app.route("/register_teacher", methods = ["POST", "GET"])
def register_teacher():
    if(request.method == 'POST'):
        # fetch data
        f_name=request.form["first_name"]
        l_name=request.form["last_name"]
        email=request.form["email"]
        password=request.form["password"]
        cur = db.cursor()
        cur.execute("INSERT INTO teacher VALUES('%s','%s','%s','%s')" % (f_name, l_name, email, password))
        db.commit()
        cur.close()
        return 'Successfully inserted data...'

    # # if request.method == "POST":
    # #     t_f_name = request.form["first_name"]
    # #     #m_name = request.form["middle_name"]
    # #     t_l_name = request.form["last_name"]
    # #     email = request.form["email"]
    # #     #gender = request.form["gender"]
    # #     username = request.form["username"]
    # #     password = request.form["password"]
    # #     # my_data = TeacherData(t_f_name,t_l_name,email,username,password)
    # #     # db.session.add(my_data)
    # #     # db.session.commit()
    #     return redirect(url_for("login"))


@app.route("/")
def index():
    """
    Presentation page
    """
    return render_template("index.html")

@app.route("/login")
def login():
    """
    Login page
    """
    return render_template("login.html")

@app.route("/register")
def register():
    """
    Teacher Registeration Page
    """
    return render_template("register.html")

@app.route("/account_page")
def account():
    """
    Teachers' account page to manage students
    """
    #all_data = StudentData.query.all()
    cur = db.cursor()
    valid = cur.execute('SELECT * from teacher;')
    if(valid > 0):
        teacherDetails = cur.fetchall()
        # return str(teacherDetails)
        return render_template('account_page.html', teacherDetails = teacherDetails)
    else:
        return '<h1>No data</h1>'

    #return render_template("account_page.html",)# students = all_data)



@app.route("/verify", methods = ["POST"])
def verify():
    """
    Verify login credentials of teacher
    """
    if request.method == "POST":
        username = request.form["username"]
        return redirect(url_for("account"))
    else:
        return render_template("login.html")
    # if account == exists:
        # return redirect(url_for("account"))
    # elif account != exists:
        # flash_a_message("Account doesn't exist. Ensure correct username and password is entered")
        # return redirect(url_for("login"))


@app.route("/delete/<string:email>")
def delete_val(email):
    cur = db.cursor()
    valid = cur.execute("DELETE FROM teacher WHERE email='%s';"%(email))
    if(valid>0):
        db.commit()
        cur.close()
        return redirect('/account_page')


# @app.route("/update")
# def update():
#     """
#     Updates existing student 
#     """
#     # return redirect(url_for("account"))
#     pass
@app.route("/update/<string:email>", methods=["POST","GET"])
def update(email):
    f_name=request.form["first_name"]
    l_name=request.form["last_name"]
    email_new=request.form["email"]
    password=request.form["password"]
    f_update = db.cursor()
    update_query = "UPDATE teacher SET First_Name = '%s', Last_Name ='%s', email = '%s', password ='%s'  WHERE email = '%s';"%(f_name,l_name, email_new,password,email)
    valid = f_update.execute("SELECT * FROM teacher WHERE email='%s';"%(email))
    #teacher = f_update.fetchone()
    if(valid > 0 and request.method =="POST"):
        f_update.execute(update_query)
        # teacher["First_Name"] = f_name #request.form['first_name']
        # teacher["Last_Name"] = l_name #request.form['last_name']
        # teacher["email"] = email_new #request.form['email']
        # teacher["password"] = password #request.form['password']
        db.commit()
        f_update.close()
    else:
        return render_template('account_page.html')
    return redirect('/account_page')#, f_update= f_update.email)



if __name__ == "__main__":
    app.run(debug = True)