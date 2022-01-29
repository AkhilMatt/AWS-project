from flask import Flask, render_template, request, redirect, url_for, app, flash
#from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)

# Configure DB:
db = pymysql.connect(host='database-2.clhatderacte.us-east-2.rds.amazonaws.com', 
user= 'root', 
password= 'root_rishab', 
port=3306, 
database='test', 
cursorclass=pymysql.cursors.DictCursor)

# inserting student data from form to table
@app.route("/add_student", methods = ["POST"])
def insert_student():
    if request.method == "POST":
        f_name = request.form["first_name"]
        l_name = request.form["last_name"]
        roll_no = request.form["roll_no"]
        sub1_marks = float(request.form["sub1_marks"])
        sub2_marks = float(request.form["sub2_marks"])
        sub3_marks = float(request.form["sub3_marks"])
        cur = db.cursor()
        query = "INSERT INTO student VALUES('%s', '%s','%s','%f','%f','%f')"%(f_name, l_name, roll_no, sub1_marks, sub2_marks, sub3_marks)
        try:
            cur.execute(query)
            db.commit()
            cur.close()
            return redirect(url_for("account"))
        except:
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
        return redirect(url_for("login"))

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

# ## DELETE
# @app.route('/flash_')
# def flash_(message = None):
#     cur = db.cursor()
#     valid = cur.execute('SELECT * from teacher;')
#     if(valid > 0):
#         teacherDetails = cur.fetchall()
#         # return str(teacherDetails)
#         return render_template('search_button.html', message = message, teacherDetails = teacherDetails)
#     else:
#         return '<h1>No data</h1>'

# @app.route("/flash_this")
# def flash_this():
#     Flash = 'THIS IS FLASH'
#     return flash_(message = Flash)
# ### DELETE

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
    cur = db.cursor()
    valid = cur.execute('SELECT * from student;')
    if(valid > 0):
        studentDetails = cur.fetchall()
        # return str(teacherDetails)
        return render_template('account_page.html', studentDetails = studentDetails)
    else:
        return '<h1>No data</h1>'

    #return render_template("account_page.html",)# students = all_data)



@app.route("/verify", methods = ["POST"])
def verify():
    """
    Verify login credentials of teacher
    """
    if request.method == "POST":
        password = request.form["password"]
        first_name = request.form['username']
        cur = db.cursor()
        query = "SELECT * FROM teacher WHERE First_Name = '%s' AND password = '%s';"%(first_name, password)
        response = cur.execute(query)
        cur.close()
        if response:
            return redirect(url_for("account"))
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/delete/<string:Roll_no>")
def delete_val(Roll_no):
    cur = db.cursor()
    valid = cur.execute("DELETE FROM student WHERE Roll_no='%s';"%(Roll_no))
    if(valid>0):
        db.commit()
        cur.close()
        #Flash = 'Student record deleted successfully'
        return redirect(url_for("account"))


# @app.route("/update")
# def update():
#     """
#     Updates existing student 
#     """
#     # return redirect(url_for("account"))
#     pass
@app.route("/update/<string:roll_no>", methods=["POST","GET"])
def update(roll_no):
    f_name = request.form["first_name"]
    l_name = request.form["last_name"]
    roll_no_new = request.form["roll_no"]
    sub1_marks = float(request.form["sub1_marks"])
    sub2_marks = float(request.form["sub2_marks"])
    sub3_marks = float(request.form["sub3_marks"])
    f_update = db.cursor()
    update_query = "UPDATE student SET First_Name = '%s', Last_Name ='%s', Roll_no = '%s', Subject_1 ='%f', Subject_2 ='%f', Subject_3 ='%f'  WHERE Roll_no = '%s';"%(f_name,l_name, roll_no_new,sub1_marks, sub2_marks, sub3_marks,roll_no)
    valid = f_update.execute("SELECT * FROM student WHERE Roll_no='%s';"%(roll_no))
    #teacher = f_update.fetchone()
    if(valid > 0 and request.method =="POST"):
        f_update.execute(update_query)
        # teacher["First_Name"] = f_name #request.form['first_name']
        # teacher["Last_Name"] = l_name #request.form['last_name']
        # teacher["email"] = email_new #request.form['email']
        # teacher["password"] = password #request.form['password']
        db.commit()
        f_update.close()
        #Flash = 'Student record updated successfully'
    else:
        return render_template('account_page.html')
    #return flash_(message = Flash)
    return redirect(url_for("account"))
    #, f_update= f_update.email)

if __name__ == "__main__":
    app.run(debug = True)
