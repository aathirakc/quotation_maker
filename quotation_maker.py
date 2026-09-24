from flask import Flask, render_template, request, redirect, session, jsonify
import datetime
import random
from datetime import date, timedelta
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="MyApp")
from DBConnection import Db
from markupsafe import Markup


app = Flask(__name__)
app.secret_key = "abc"


@app.route('/',methods=['get','post'])
def hello_world():
    if request.method=="POST":
        username=request.form['textfield']
        password=request.form['textfield2']
        db=Db()
        ss=db.selectOne("select * from login where username='"+username+"' and password='"+password+"'")
        if ss is not None:
            if ss['usertype']=='admin':
                session['log'] = "lo"
                return redirect('/admin_home')
            elif ss['usertype']=='user':
                session['lid']=ss['id']
                session['log'] = "lo"
                return redirect('/user_home')
            else:
                return '''<script>alert('incorrect username and password');window.location="/"</script>'''
        else:
            return '''<script>alert('incorrect username and password');window.location="/"</script>'''
    else:
        return render_template('index.html')


#admin


@app.route('/admin_home')
def admin_home():
    if session['log'] == "lo":
        db = Db()
        # ss = db.select("select * from movie")
        return render_template('admin/v_index.html')


#user


@app.route('/user_home')
def user_home():
    if session['log'] == "lo":
        db = Db()
        # ss = db.select("select * from movie")
        return render_template('user/v_index.html')

@app.route('/user_profile')
def user_profile():
        return render_template('user/profile.html')


@app.route('/c_home')
def c_home():
    # if session['log'] == "lo":
    #     db = Db()
    #     ss = db.select("select * from movie")
        return render_template('user/u_index.html')

@app.route('/add_quotation')
def add_quotation():

        return render_template('user/add_q.html')

@app.route('/add_items',methods=['get','post'])
def add_items():
    if session['log'] == "lo":
                if request.method=="POST":

                    name = request.form['textfield1']
                    addr = request.form['textfield2']
                    phno = request.form['textfield3']
                    db=Db()
                    ss=db.insert("insert into add_q values('','"+str(session['lid'])+"','"+name+"','"+addr+"','"+phno+"',curdate())")
                    # a=db.select("select id from add_q")
                    return render_template('user/add_items.html',a=ss)
                return render_template('user/add_items.html')
    return render_template('user/add_items.html')

@app.route('/more_items/<b>',methods=['get','post'])
def more_items(b):
    if session['log'] == "lo":
                if request.method=="POST":

                    name = request.form['textfield1']
                    addr = request.form['textfield2']
                    phno = request.form['textfield3']
                    db=Db()
                    ss=db.insert("insert into add_q values('','"+str(session['lid'])+"','"+name+"','"+addr+"','"+phno+"')")
                    # a=db.select("select id from add_q")
                    return render_template('user/add_items.html',a=ss)
                return render_template('user/add_items.html',a=b)
    return render_template('user/add_items.html')

@app.route('/adding/<b>',methods=['get','post'])
def adding(b):
    if session['log'] == "lo":
        if request.method == "POST":
            q_id=request.form['id']
            item = request.form['textfield1']
            price = float(request.form['textfield2'])
            gst = float(request.form['textfield3'])
            total = price + ((price * gst) / 100)
            total1=str(total)
            print(total1)

            db = Db()
            ss = db.insert("insert into add_items values('','"+str(q_id)+"','" + str(item) + "','" + str(price) + "','" + str(gst) + "','"+str(total1)+"')")
            aa = db.insert("insert into master values('','"+str(session['lid'])+"','"+str(ss)+"',curdate(),'pending')")
            a=db.selectOne("select * from add_q where id='"+q_id+"'")
            # b=db.select("select * from add_items where id='"+str(ss)+"' and q_id='"+q_id+"'")
            ss1 = db.select("select add_q.name AS a,add_q.address AS p,add_q.phonenumber AS s,add_items.price AS h,add_items.item AS b ,add_q.*,add_items.*,master.* from master,add_items,add_q where add_items.id=master.add_item_id and add_items.q_id=add_q.id   and master.status='pending' and master.user_id='" + str(session['lid']) + "' ")
            print(ss1)
            return render_template('user/adding_index.html',data=ss1,data1=a)

        db=Db()
        ss1 = db.select("select add_q.name AS a,add_q.address AS p,add_q.phonenumber AS s,add_items.price AS h,add_items.item AS b ,add_q.*,add_items.*,master.* from master,add_items,add_q where add_items.id=master.add_item_id and add_items.q_id=add_q.id  and master.status='pending' and master.user_id='" + str(session['lid']) + "' and master.date=curdate() ")
        if ss1:
            print("athira",b)
            ab=db.selectOne("select * from add_q where id='"+str(b)+"'")
            return render_template('user/adding_index.html',data=ss1,data1=ab)
        else:
            return render_template('user/no_records.html',data=b)

    return render_template('user/adding_index.html')

@app.route('/no_records')
def no_records():

        return render_template('user/no_records.html')


@app.route('/delete_item/<b>')
def delete_item(b):
    if session['log'] == "lo":
        db=Db()
        ss = db.selectOne("select * from master where id ='" + str(b) + "'")
        print(ss)
        item_id =str( ss['add_item_id'])
        ss2=db.select("select * from add_items where id='"+str(item_id)+"'")
        print(ss2)
        aa = ss2[0]['q_id']

        print("vg",aa)
        safe_aa=str(aa)
        aa1=db.select("select * from add_q where id='"+str(aa)+"'")




        db.delete("delete from add_items where id='"+item_id+"'")
        db.delete("delete  from master where id='"+str(b)+"'")

        # db.delete("delete  from add_items where id='"+str(b)+"'")
        ss1 = db.select("select add_q.name AS a,add_q.address AS p,add_q.phonenumber AS s,add_items.price AS h,add_items.item AS b ,add_q.*,add_items.*,master.* from master,add_items,add_q where add_items.id=master.add_item_id and add_items.q_id=add_q.id  and master.status='pending' and master.user_id='" + str(session['lid']) + "' ")
        return Markup(f"<script>alert('Successfully deleted'); window.location='/adding/{safe_aa}';</script>")

    return render_template('user/view_item.html')


@app.route('/submit/<b>')
def submit(b):
    db=Db()
    item_b=str(b)
    ss=db.select("select add_q.id AS h ,master.id AS p, add_q.*,master.*,add_items.* from add_q,master,add_items where add_items.id=master.add_item_id and add_items.q_id=add_q.id and master.status='pending' and master.user_id='"+str(session['lid'])+"' ")
    ss1=db.selectOne("select * from add_q where id='"+str(b)+"'")
    ss2=db.selectOne("select * from login,add_q where login.id=add_q.user_id and add_q.id='"+str(b)+"'")
    db.update("update master  INNER JOIN add_items  ON add_items.id = master.add_item_id INNER JOIN add_q  ON add_items.q_id = add_q.id SET   master.status='approved' where add_q.id='"+str(b)+"' and master.user_id='"+str(session['lid'])+"'")
    # v = db.select("select sum(add_items.* manage_product.p_price) AS totalsum,book.*,manage_product.* from book,manage_product where book.product_id=manage_product.id")
    return render_template('user/book_radio.html',a=b,data=ss,data1=ss1,data2=ss2)





if __name__ == '__main__':
    app.run(port=4000)