"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
from app import app
from flask import render_template, request, redirect, url_for, flash, session, abort
from werkzeug.utils import secure_filename
from .forms import RegForm, LoginForm, ModAboutForm, gen, AdminForm, CPostForm, UppForm, Addcom_PostForm, SearchForm, AddFriendForm, CGroupForm, GroupForm
from werkzeug.security import generate_password_hash, check_password_hash
import re
import pymsgbox

import datetime
import time
from wtforms.fields.html5 import DateField
from datetime import datetime

from flask_mysqldb import MySQL
from app import app
import ctypes

# Configure db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'COMP3161';
app.config['MYSQL_PASSWORD'] = '';  
app.config['MYSQL_DB'] = 'socialmedia'

mysql = MySQL(app)

@app.route('/')
def index():
    """Render website's home page."""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegForm()
        return render_template('reg.html', form = form)

    form = RegForm()
    if request.method == 'POST'and form.validate_on_submit():
        
        first = request.form['firstname']
        pattern = "/^[a-zA-Z\-]+$/" 
        if (re.search(pattern,first)):
            pymsgbox.alert('','Invalid First Name!')

        last = request.form['lastname']
        pattern = "/^[a-zA-Z\-]+$/" 
        if (re.search(pattern,last)):
            pymsgbox.alert('','Invalid Last Name!')

        email_add = request.form['email']
        pattern = "/^a-zA-Z0-9.-_+]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/" 
        if (re.search(pattern,email_add)):
            pymsgbox.alert('','Invalid Email!')

        telephone = request.form['telephone_no']
        pattern = "/^\d{7}$/" 
        if (re.search(pattern,telephone)):
            pymsgbox.alert('','Invalid Telephone Number!')

        street = request.form['street_name']
        city_name = request.form['city']
        coun = request.form['country']

        area = request.form['area_code']
        pattern = "/^\d{3}$/" 
        if (re.search(pattern,area)):
            print("")
        else:
            flash('Invalid Area Code!','success')

        passw = request.form['password']
        pattern = "/^a-zA-Z0-9.-_+]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]" 
        if (re.search(pattern,passw)):
            pymsgbox.alert('','Invalid Email!')
        cpass = request.form['con_pass']

        if passw!=cpass:
            flash('Non-matching Passwords', 'success')
            form = RegForm()
            return render_template('reg.html', form = form)

        cur = mysql.connection.cursor()
        cur.execute("SELECT count(email) FROM User WHERE email='{}'".format(email_add))
        result=cur.fetchall()
        emailcount = int(result[0][0])

        if emailcount > 0:
            flash('Email being used', 'success')
            form = RegForm()
            return render_template('reg.html', form = form)
        passwo = generate_password_hash(passw, method='pbkdf2:sha256')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO User(firstName, lastName, email, password_digest) VALUES (%s, %s, %s, %s)", (first, last, email_add, passwo))
        cur.execute("SELECT user_id FROM User WHERE email='{}'".format(email_add))
        result=cur.fetchall()
        use_r = result[0][0]
       
        
        cur.execute("INSERT INTO Phone(user_id, telephone_no, area_code) VALUES (%s ,%s, %s)", (use_r, telephone, area))
        cur.execute("INSERT INTO Address(user_id, street_name, city, country) VALUES (%s ,%s, %s, %s)", (use_r, street, city_name, coun))
        cur.execute("INSERT INTO Profile(user_id) VALUES ({})".format(use_r))

        mysql.connection.commit()
        return render_template('index.html')
    return render_template('reg.html',form=form)

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM User")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', form = form)

    form = LoginForm()
    if request.method == 'POST':
        # Fetch form data
        email_add = request.form['e_mail']
        passw = request.form['password']
        passwo = generate_password_hash(passw, method='pbkdf2:sha256')
        cur = mysql.connection.cursor()

        cur.execute("SELECT password_digest FROM User WHERE email='{}'".format(email_add))
        re_sult=cur.fetchall()

        if len(re_sult)==0:
            flash('Invalid Info', 'success')
            return render_template('login.html', form = form)

        pass_hash = re_sult[0][0]

        if check_password_hash(pass_hash,passw):
            cur.execute("SELECT user_id FROM User WHERE email='{}'".format(email_add))
            result=cur.fetchall()
            userid = result[0][0]

            cur.close()
            return redirect(url_for('profileuserid', userid = userid))
        else:
            flash('Invalid Info', 'success')
            return render_template('login.html', form = form)

@app.route('/profileuserid/<int:userid>', methods=['GET', 'POST'])
def profileuserid(userid):

    if request.method == 'GET':
        
        cur = mysql.connection.cursor()
        #Search db for firstname
        cur.execute("SELECT firstname FROM User WHERE user_id='{}'".format(userid))
        result=cur.fetchall()
        firstname = result[0][0]

        #Search db for lastname
        cur.execute("SELECT lastname FROM User WHERE user_id='{}'".format(userid))
        result=cur.fetchall()
        lastname = result[0][0]

        #Search db for email
        cur.execute("SELECT email FROM User WHERE user_id='{}'".format(userid))
        result=cur.fetchall()
        email = result[0][0]

        cur.execute("SELECT profile_id FROM Profile WHERE user_id='{}'".format(userid))
        result=cur.fetchall()

        dire=""
        if len(result)>0:
            profile1id = result[0][0]

            cur.execute("SELECT image_id FROM Profile_pic WHERE profile_id='{}'".format(profile1id))
            result=cur.fetchall()

            if len(result)>0:
                image1id = result[0][0]

                cur.execute("SELECT directory FROM Image WHERE image_id='{}'".format(image1id))
                if len(result)>0:
                    result=cur.fetchall()
                    dire = result[0][0]

        form = SearchForm()

        return render_template('profileuserid.html',userid=userid,firstname=firstname,lastname=lastname,email=email,dire=dire, form=form)

    form = SearchForm()

    if request.method == 'POST' and form.validate_on_submit():
        searchbar = request.form['searchbar']
        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id,firstname,lastname FROM User WHERE firstname LIKE '%{}%' OR lastname LIKE '%{}%'".format(searchbar, searchbar))
        result=cur.fetchall()

        profiles = []
        for r in result:
            uid, first, last = r
            cur.execute("SELECT directory FROM Image where image_id in (SELECT image_id FROM Profile_pic where profile_id in (SELECT profile_id FROM Profile where user_id = {}))".format(uid))
            p = cur.fetchall()
            photo = ""
            if len(p)>0:
                photo = p[0][0]
            if userid != uid:
                profiles.append((uid, first, last, photo))
        profiles.sort(key=lambda x:x[2])
        profiles.sort(key=lambda x:x[1])

        mysql.connection.commit()
        form = AddFriendForm()
        return render_template('sfriend.html',form=form,userid=userid,fren_info=profiles)
    return redirect(url_for('profileuserid', userid = userid))  


@app.route('/addfriend/<int:userid>',methods=['GET', 'POST'])                
def addfriend(userid):
    groups1 = {'Relative':'1','School':'2','Work':'3'}
    if request.method =='POST':
        f_id = request.form.get('Encrypt')
        _groupname = request.form['group']
        _groupid = groups1[_groupname]
        cur = mysql.connection.cursor()

        cur.execute("SELECT count(user_id) FROM friends_with where user_id = {} and friend_id = {} and group_id = {}".format(userid, f_id, _groupid))
        ch = cur.fetchall()
        ch = ch[0][0]
        if ch < 1:
            cur.execute("INSERT INTO friends_with(user_id, friend_id, group_id) VALUES (%s ,%s, %s)", (userid, f_id, _groupid))
        
        mysql.connection.commit()
        return redirect(url_for('profileuserid', userid = userid))  

    elif request.method =='GET':
        print(" ")
    return redirect(url_for('profileuserid', userid = userid)) 


@app.route('/vfriend/<int:userid>')               
def vfriend(userid):
    cur = mysql.connection.cursor()

    cur.execute("SELECT friend_id FROM friends_with WHERE user_id='{}'".format(userid))
    fren_ids=cur.fetchall()

    info = []
    for fren in fren_ids:
        
        fid=fren[0]
        cur.execute("SELECT directory FROM Image WHERE image_id in (Select image_id FROM profile_pic WHERE  profile_id in (SELECT profile_id FROM Profile WHERE user_id={}))".format(fid))
        images = cur.fetchall()
        pic = images[0][0]

        cur.execute("SELECT user_id,firstname,lastname FROM User WHERE user_id = {}".format(fid))
        fren_info = cur.fetchall()
        uid,first,last = fren_info[0]
        
        #dont insert duplicates
        if (uid, first, last, pic) not in info:
            info.append((uid,first, last, pic))
        mysql.connection.commit()
    
    info.sort(key=lambda x:x[2])
    info.sort(key=lambda x:x[1])
    print(userid)
    return render_template('vfriend.html',fren_stuff=info,userid=userid)
 
@app.route('/groups/<int:userid>', methods=['GET', 'POST'])
def groups(userid): 
    if request.method == 'GET':
        form = GroupForm() 
        return render_template('groups.html',form=form,userid=userid) 
    form = GroupForm() 
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        group_search = request.form['groupsearch']
        cur.execute("SELECT group_id,group_name FROM Group1 WHERE group_name LIKE '%{}%'".format(group_search))
        gr_result=cur.fetchall()

        info=[]
        print(gr_result)
        for g in gr_result:
            gid,gname = g
            cur = mysql.connection.cursor()
            cur.execute("SELECT user_id,create_date FROM creates WHERE group_id={}".format(gid))
            gr=cur.fetchall()
            #if empty skip
            if len(gr) == 0:
                continue

            uid,cdate=gr[0]

            cur.execute("SELECT firstname,lastname FROM User WHERE user_id={}".format(uid))
            u_result=cur.fetchall()
            fname,lname=u_result[0]

            if gid not in [1,2,3]:
                info.append((gid,gname,fname,lname,cdate))

        mysql.connection.commit()

        info.sort(key=lambda x:x[1])
        return render_template('sgroup.html',userid=userid,info=info,form=form)
    return redirect(url_for('groups',userid=udserid))   

@app.route('/joingroup/<int:userid>',methods=['GET', 'POST'])                
def joingroup(userid):
    if request.method =='POST':
        g_id = request.form.get('Encrypt')
        joindate = datetime.today().strftime('%Y-%m-%d')

        cur = mysql.connection.cursor()
        cur.execute("SELECT count(group_id) FROM joins where user_id = {} and group_id = {}".format(userid,g_id))
        gh = cur.fetchall()
        gh = gh[0][0]
        if gh < 1:
            cur.execute("INSERT INTO joins(user_id, group_id, join_date) VALUES (%s ,%s, %s)", (userid, g_id,joindate))
        mysql.connection.commit()
        return redirect(url_for('groups', userid = userid))  

    elif request.method =='GET':
        print(" ")
    return redirect(url_for('groups', userid = userid)) 


@app.route('/dgroupcom/<int:userid>',methods=['GET', 'POST'])                
def dgroupcom(userid):
    if request.method =='POST':

        comdate = datetime.today().strftime('%Y-%m-%d')
        comtime = datetime.now().strftime("%H:%M:%S")

        comm = request.form['usr_text']
        g_id = request.form.get('Encrypt')
        p_id = request.form.get('Postid')


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Comment(post_id,usr_text,com_date,com_time) VALUES ({},'{}','{}','{}')".format(p_id,comm,comdate,comtime))
        cur.execute("SELECT com_id FROM Comment WHERE com_date='{}' AND com_time='{}' AND usr_text='{}'".format(comdate,comtime,comm))
        co_result=cur.fetchall()
        comid = co_result[0][0]
        cur.execute("INSERT INTO Commented(user_id,com_id,post_id) VALUES (%s,%s,%s)", (userid,comid,p_id)) 
        mysql.connection.commit()

        cur = mysql.connection.cursor()

        cur.execute("SELECT post_id FROM belongs WHERE group_id={}".format(g_id))
        result=cur.fetchall()
        post_ids=result
        cur.execute("SELECT post_id,description,post_date,post_time FROM Post WHERE post_id in (SELECT post_id FROM belongs WHERE group_id={}) ORDER BY post_date DESC, post_time DESC".format(g_id))
        posts=cur.fetchall()

        info = []
        for post in posts:
            doc =[]
            pid, des, date, time = post
            cur.execute("SELECT directory FROM Image WHERE image_id in (Select image_id FROM post_image where  post_id = {})".format(pid))
            images = cur.fetchall()
            pics = []
            for image in images:
                dr = image[0]
                pics.append(dr)


            cur.execute("SELECT usr_text, com_date, com_time FROM Comment WHERE com_id in (Select com_id FROM Commented where  post_id = {})".format(pid))
            comments = cur.fetchall()
            words = []
            for comment in comments:
                cr = comment
                words.append(cr)    

            doc = [pid, des, date, time, pics, words]       
            info.append(doc)

        cur.execute("SELECT group_name FROM Group1 WHERE group_id={}".format(g_id))
        gname = cur.fetchall()
        gname = gname[0][0]
        info.append(g_id)
        info.append(gname)

        mysql.connection.commit()
        form = Addcom_PostForm()
        #joindate = datetime.today().strftime('%Y-%m-%d')

        #cur = mysql.connection.cursor()
        #cur.execute("INSERT INTO joins(user_id, group_id, join_date) VALUES (%s ,%s, %s)", (userid, g_id,joindate))
        #mysql.connection.commit()
        return render_template('dgroup.html', form = form, pos_t=info,userid=userid)  

    elif request.method =='GET':
        print(" ")
    return redirect(url_for('groups', userid = userid))



@app.route('/dgroup/<int:userid>',methods=['GET', 'POST'])                
def dgroup(userid):
    if request.method =='POST':
        g_id = request.form.get('Encrypt')

        cur = mysql.connection.cursor()

        cur.execute("SELECT post_id FROM belongs WHERE group_id={}".format(g_id))
        result=cur.fetchall()
        post_ids=result
        cur.execute("SELECT post_id,description,post_date,post_time FROM Post WHERE post_id in (SELECT post_id FROM belongs WHERE group_id={}) ORDER BY post_date DESC, post_time DESC".format(g_id))
        posts=cur.fetchall()

        info = []
        for post in posts:
            doc =[]
            pid, des, date, time = post
            cur.execute("SELECT directory FROM Image WHERE image_id in (Select image_id FROM post_image where  post_id = {})".format(pid))
            images = cur.fetchall()
            pics = []
            for image in images:
                dr = image[0]
                pics.append(dr)


            cur.execute("SELECT usr_text, com_date, com_time FROM Comment WHERE com_id in (Select com_id FROM Commented where  post_id = {})".format(pid))
            comments = cur.fetchall()
            words = []
            for comment in comments:
                cr = comment
                words.append(cr)    

            doc = [pid, des, date, time, pics, words]       
            info.append(doc)

        cur.execute("SELECT group_name FROM Group1 WHERE group_id={}".format(g_id))
        gname = cur.fetchall()
        gname = gname[0][0]
        info.append(g_id)
        info.append(gname)

        mysql.connection.commit()
        form = Addcom_PostForm()
        #joindate = datetime.today().strftime('%Y-%m-%d')

        #cur = mysql.connection.cursor()
        #cur.execute("INSERT INTO joins(user_id, group_id, join_date) VALUES (%s ,%s, %s)", (userid, g_id,joindate))
        #mysql.connection.commit()
        return render_template('dgroup.html', form = form, pos_t=info,userid=userid)  

    elif request.method =='GET':
        print(" ")
    return redirect(url_for('groups', userid = userid)) 


@app.route('/cgroup/<int:userid>', methods=['GET', 'POST'])
def cgroup(userid):
    if request.method == 'GET':
        form = CGroupForm()
        return render_template('cgroup.html', form = form,userid=userid)

    form = CGroupForm()
    if request.method == 'POST':
        g_roupname = request.form['groupname']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Group1(group_name) VALUES ('{}')".format(g_roupname))
        cur.execute("SELECT LAST_INSERT_ID()") 
        g_result=cur.fetchall()
        g_id=g_result[0][0]
        c_d=  datetime.today().strftime('%Y-%m-%d')
        print('GID: '+str(g_id))
        cur.execute("INSERT INTO creates(editor_id,group_id,user_id,create_date) VALUES (%s,%s,%s,%s)", (userid,g_id,userid,c_d))
        cur.execute("INSERT INTO joins(user_id,group_id,join_date) VALUES (%s,%s,%s)", (userid,g_id,c_d))
        
        mysql.connection.commit()
        flash('Group successfully created!','success')
        return redirect(url_for('mygroups', userid = userid))
    return redirect(url_for('profileuserid', userid = userid))

@app.route('/mygroups/<int:userid>')
def mygroups(userid):
    cur = mysql.connection.cursor()
    cur.execute("SELECT group_id,join_date FROM joins WHERE user_id='{}'".format(userid))
    myg_result=cur.fetchall()

    info=[]
    for myg in myg_result:
        gid, gdate = myg
        cur.execute("SELECT group_name FROM Group1 WHERE group_id ={}".format(gid))
        my_result=cur.fetchall()
        g_name=my_result[0][0]
        cur.execute("SELECT user_id, firstname,lastname FROM User WHERE user_id in (SELECT user_id FROM creates WHERE group_id ={})".format(gid))
        my_result=cur.fetchall()
        gowner_id,fn_ame, ln_ame=my_result[0]
        info.append((gid,g_name,gdate,fn_ame,ln_ame,))
    mysql.connection.commit()
    info.sort(key=lambda x:x[1])
    form = GroupForm() 
    return render_template('mygroups.html', userid = userid,info=info,form=form)

@app.route('/aboutuserid/<int:userid>')
def aboutuserid(userid):
    cur = mysql.connection.cursor()
    #Search db for country
    cur.execute("SELECT country FROM Address WHERE user_id='{}'".format(userid))
    c_result=cur.fetchall()

    #Search db for dob
    cur.execute("SELECT dob FROM Profile WHERE user_id='{}'".format(userid))
    d_result=cur.fetchall()

    #Search db for gender
    cur.execute("SELECT gender FROM Profile WHERE user_id='{}'".format(userid))
    g_result=cur.fetchall()

    #Search db for nickname
    cur.execute("SELECT nickname FROM Profile WHERE user_id='{}'".format(userid))
    n_result=cur.fetchall()

    if len(d_result)==0:
        flash('Modify About First','error')
        return redirect(url_for('modaboutuserid',userid=userid))
    else:
        country = c_result[0][0]
        dob = d_result[0][0]
        gender = g_result[0][0]
        nickname = n_result[0][0]
        return render_template('aboutuserid.html',userid=userid,country=country,dob=dob,gender=gender,nickname=nickname)

@app.route('/modaboutuserid/<int:userid>',methods=['GET', 'POST'])
def modaboutuserid(userid):
    if request.method == 'GET':
        form = ModAboutForm()
        return render_template('modaboutuserid.html', form = form, userid=userid)

    form = ModAboutForm()
    if request.method == 'POST' and form.validate_on_submit():
        nickname = request.form['nickname']
        # dob = request.form['dob']
        # dob = datetime.today().strftime('%Y-%m-%d')
        d_ob = form.dob.data.strftime('%Y-%m-%d')
        gen_der = dict(gen).get(form.gender.data)
        cur = mysql.connection.cursor()

        cur.execute("SELECT profile_id FROM Profile WHERE user_id='{}'".format(userid))
        pr_result=cur.fetchall()
        if len(pr_result)==0:
            cur.execute("INSERT INTO Profile(user_id, dob, gender,nickname) VALUES (%s ,%s, %s, %s)", (userid,d_ob,gen_der,nickname)) 
        else:
            profileid = pr_result[0][0]
            cur.execute("UPDATE Profile SET dob=%s, gender=%s,nickname=%s WHERE profile_id=%s", (d_ob,gen_der,nickname,profileid)) 
    
        mysql.connection.commit()
        return redirect(url_for('profileuserid', userid = userid))
    return redirect(url_for('index'))

@app.route('/cpost/<int:userid>',methods=['GET', 'POST'])
def cpost(userid):
    if request.method == 'GET':

        cur = mysql.connection.cursor()
        cur.execute("SELECT group_id, group_name FROM Group1 WHERE group_id in (1,2,3) or group_id in (SELECT group_id FROM creates WHERE editor_id= {})".format(userid))
        groups=cur.fetchall()
        mysql.connection.commit()


        form = CPostForm()
        return render_template('cpost.html', form = form, userid=userid, groups = groups)

    form = CPostForm()
    if request.method == 'POST':
        des_cription = request.form['description']
        file = request.files['photo'] 
        _groupid = request.form['autocomplete_group']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        dir_ectory="uploads/"+filename

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO Image(image_name,directory) VALUES (%s,%s)", (filename,dir_ectory)) 
        cur.execute("SELECT LAST_INSERT_ID()") 
        im_result=cur.fetchall()
        imageid = im_result[0][0]


        cur.execute("INSERT INTO Adds(image_id,user_id) VALUES (%s,%s)", (imageid,userid)) 

        post_date = datetime.today().strftime('%Y-%m-%d')
        post_time = datetime.now().strftime("%H:%M:%S")

        cur.execute("INSERT INTO Post(description,post_date,post_time) VALUES (%s,%s,%s)", (des_cription,post_date,post_time)) 
        cur.execute("SELECT post_id FROM Post WHERE post_date='{}' AND post_time='{}' AND description='{}'".format(post_date, post_time, des_cription))
        po_result=cur.fetchall()
        postid = po_result[0][0]

        cur.execute("INSERT INTO Post_image(post_id,image_id) VALUES (%s,%s)", (postid,imageid))

        cur.execute("INSERT INTO Submits(post_id,user_id) VALUES (%s,%s)", (postid,userid))

        cur.execute("INSERT INTO belongs(post_id,group_id) VALUES (%s,%s)", (postid, _groupid))

        mysql.connection.commit()

        return redirect(url_for('vpost', userid = userid))
    return redirect(url_for('index'))

@app.route('/vfrenprofile/<int:userid>',methods=['GET','POST'])
def vfrenprofile(userid):
    if request.method == 'POST':
        #frenid = request.form.get("Frendid")
        frenid = request.form["Friendid"]
        cur = mysql.connection.cursor()

        cur.execute("SELECT post_id FROM Submits WHERE user_id={}".format(frenid))
        result=cur.fetchall()
        post_ids=result
        print((frenid,post_ids))
        cur.execute("SELECT post_id,description,post_date,post_time FROM Post WHERE post_id in (SELECT post_id FROM Submits WHERE user_id={}) ORDER BY post_date DESC, post_time DESC".format(frenid))
        posts=cur.fetchall()

        info = []
        for post in posts:
            doc =[]
            pid, des, date, time = post
            cur.execute("SELECT directory FROM Image WHERE image_id in (Select image_id FROM post_image where  post_id = {})".format(pid))
            images = cur.fetchall()
            pics = []
            for image in images:
                dr = image[0]
                pics.append(dr)


            cur.execute("SELECT usr_text, com_date, com_time FROM Comment WHERE com_id in (Select com_id FROM Commented where  post_id = {})".format(pid))
            comments = cur.fetchall()
            words = []
            for comment in comments:
                cr = comment
                words.append(cr)    


            doc = [pid, des, date, time, pics, words]       
            info.append(doc)
        mysql.connection.commit()
        form = Addcom_PostForm()
        #return render_template('vpost.html', form = form,pos_t=info,userid=userid)

        return render_template('vpost.html', userid=userid, pos_t=info, form=form, fid = frenid)
    return redirect(url_for('vfrenprofile', userid = userid))

@app.route('/vpost/<int:userid>', methods=['GET', 'POST'])
def vpost(userid):
    if request.method == 'GET':
    
        cur = mysql.connection.cursor()

        cur.execute("SELECT post_id FROM Submits WHERE user_id={}".format(userid))
        result=cur.fetchall()
        post_ids=result

        cur.execute("SELECT post_id,description,post_date,post_time FROM Post WHERE post_id in (SELECT post_id FROM Submits WHERE user_id={}) ORDER BY post_date DESC, post_time DESC".format(userid))
        posts=cur.fetchall()

        info = []
        for post in posts:
            doc =[]
            pid, des, date, time = post
            cur.execute("SELECT directory FROM Image WHERE image_id in (Select image_id FROM post_image where  post_id = {})".format(pid))
            images = cur.fetchall()
            pics = []
            for image in images:
                dr = image[0]
                pics.append(dr)


            cur.execute("SELECT usr_text, com_date, com_time FROM Comment WHERE com_id in (Select com_id FROM Commented where  post_id = {})".format(pid))
            comments = cur.fetchall()
            words = []
            for comment in comments:
                cr = comment
                words.append(cr)    


            doc = [pid, des, date, time, pics, words]       
            info.append(doc)
        mysql.connection.commit()
        form = Addcom_PostForm()
        return render_template('vpost.html', form = form,pos_t=info, userid=userid, fid = userid)

    form = Addcom_PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        cur = mysql.connection.cursor()
        us_rtext = request.form['usr_text']
        p_id = request.form['pi_d']
        comdate = datetime.today().strftime('%Y-%m-%d')
        comtime = datetime.now().strftime("%H:%M:%S")

        #cur.execute("INSERT INTO Comment(post_id,usr_text,com_date,com_time) VALUES (%s,%s,%s,%s)", (p_id,us_rtext,comdate,comtime)) 
        cur.execute("INSERT INTO Comment(post_id,usr_text,com_date,com_time) VALUES ({},'{}','{}','{}')".format(p_id,us_rtext,comdate,comtime))
        #print("INSERT INTO Comment(post_id,usr_text,com_date,com_time) VALUES ({},'{}','{}','{}')".format(p_id,us_rtext,comdate,comtime))
        mysql.connection.commit()
        cur = mysql.connection.cursor()
        cur.execute("SELECT com_id FROM Comment WHERE com_date='{}' AND com_time='{}' AND usr_text='{}'".format(comdate,comtime,us_rtext))
        co_result=cur.fetchall()
        comid = co_result[0][0]
        cur.execute("INSERT INTO Commented(user_id,com_id,post_id) VALUES (%s,%s,%s)", (userid,comid,p_id)) 
        mysql.connection.commit()

        return redirect(url_for('vpost',userid=userid))
    return redirect(url_for('profileuserid', userid = userid))

import os
def get_uploaded_images():
    a=[]
    rootdir = os.getcwd()
    print (rootdir)
    for subdir, dirs, files in os.walk(rootdir + app.config['UPLOAD_FOLDER']):
        for file in files:
            a.append(file)
    return a

@app.route('/upp/<int:userid>', methods=['GET', 'POST'])
def upp(userid):
    if request.method == 'GET':
        form = UppForm()
        return render_template('upp.html', form = form, userid=userid)

    form = UppForm()
    if request.method == 'POST'and form.validate_on_submit():
        file = request.files['photo'] 
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #dir_ectory=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        dir_ectory="uploads/"+filename
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Image(image_name,directory) VALUES (%s,%s)", (filename,dir_ectory)) 
        mysql.connection.commit()
        cur.execute("SELECT LAST_INSERT_ID()") 
        im_result=cur.fetchall()
        imageid = im_result[0][0]
       

        cur.execute("SELECT profile_id FROM Profile WHERE user_id='{}'".format(userid))
        pro_result=cur.fetchall()
        profileid = pro_result[0][0]

        cur.execute("SELECT image_id FROM Profile_pic WHERE profile_id='{}'".format(profileid))
        prom_result=cur.fetchall()
        #cur_imageid = prom_result[0][0]

        if len(prom_result)==0:
            cur.execute("INSERT INTO Profile_pic(profile_id,image_id) VALUES (%s,%s)", (profileid,imageid))
        else:
            cur.execute("UPDATE Profile_pic SET image_id=%s WHERE profile_id=%s", (imageid,profileid)) 
        cur.execute("INSERT INTO Adds(image_id,user_id) VALUES (%s,%s)", (imageid,userid)) 
        mysql.connection.commit()

        flash('Profile Picture Saved!', 'success')
        return redirect(url_for('profileuserid', userid = userid))
    return render_template('upp.html', form = form, userid=userid)

@app.route('/addcom_post/<int:userid>', methods=['GET', 'POST'])
def addcom_post():
    if request.method == 'GET':

        cur = mysql.connection.cursor()
        cur.execute("SELECT group_id, group_name FROM Group1 WHERE group_id in (1,2,3) or group_id in (SELECT group_id FROM creates WHERE editor_id= {})".format(userid))
        groups=cur.fetchall()
        mysql.connection.commit()

        form = CPostForm()
        return render_template('cpost.html', form = form)

    form = CPostForm()
    if request.method == 'POST' and form.validate_on_submit():
        cur = mysql.connection.cursor()
        us_rtext = request.form['usr_text']
        p_id = request.form['pi_d']
        comdate = datetime.today().strftime('%Y-%m-%d')
        comtime = datetime.now().strftime("%H:%M:%S")

        #cur.execute("INSERT INTO Comment(post_id,usr_text,com_date,com_time) VALUES (%s,%s,%s,%s)", (p_id,us_rtext,comdate,comtime)) 
        cur.execute("INSERT INTO Comment(post_id,usr_text,com_date,com_time) VALUES ({},'{}','{}','{}')".format(p_id,us_rtext,comdate,comtime))
        #print("INSERT INTO Comment(post_id,usr_text,com_date,com_time) VALUES ({},'{}','{}','{}')".format(p_id,us_rtext,comdate,comtime))
        mysql.connection.commit()
        cur = mysql.connection.cursor()
        cur.execute("SELECT com_id FROM Comment WHERE com_date='{}' AND com_time='{}' AND usr_text='{}'".format(comdate,comtime,us_rtext))
        co_result=cur.fetchall()
        comid = co_result[0][0]
        cur.execute("INSERT INTO Commented(user_id,com_id,post_id) VALUES (%s,%s,%s)", (userid,comid,p_id)) 
        mysql.connection.commit()
        
        return redirect(url_for('profileuserid', userid = userid))
    return redirect(url_for('addcom_post', userid = userid))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        form = AdminForm()
        return render_template('admin.html', form = form)

    form = AdminForm()
    if request.method == 'POST' and form.validate_on_submit():
        user_name = request.form['username']
        pass_word = request.form['password']
        if user_name=="Database" and pass_word=="Database":
            return render_template('adminpage.html', form = form)
    flash('Unauthorized', 'success')
    return render_template('admin.html', form = form)

###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
