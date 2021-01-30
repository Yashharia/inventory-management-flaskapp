from flask import Flask, render_template, flash, redirect, url_for,request, session, logging
from flask_mysqldb import MySQL
from wtforms import Form,StringField,PasswordField,validators 
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="inventorymanagement"
app.config['MYSQL_CURSORCLASS']="DictCursor"
#intialize mysql
mysql = MySQL(app)

@app.route('/')
def index():
    # create cursor
    cur=mysql.connection.cursor()

    result=cur.execute("SELECT * from product")
    products = cur.fetchall()

    result=cur.execute("SELECT * from location")
    locations = cur.fetchall()

    #get productmovement
    result=cur.execute("SELECT * from productmovement")
    productmovements = cur.fetchall()

    result=cur.execute("SELECT product_id,to_location, SUM(qty) totalstock from productmovement WHERE to_location!='' GROUP BY product_id,to_location")
    values=cur.fetchall()

    result=cur.execute("SELECT product_id,from_location, SUM(qty) totalstock from productmovement WHERE to_location ='' GROUP BY product_id,from_location")
    outvalues=cur.fetchall()

    count = 0
    for value in values:
        for outvalue in outvalues:
            if(value['product_id'] == outvalue['product_id'] and value['to_location'] == outvalue['from_location'] ):
                values[count]['totalstock']=value['totalstock'] - outvalue['totalstock']
                # print("totalstock : %s",value['totalstock'])
                # print("id= %s fromlocation=%s outstock : %s",(outvalue['product_id'],outvalue['from_location'] ,outvalue['totalstock']))
        count+=1
        # print(count)
    


    return render_template('home.html',products=products,productmovements=productmovements,locations=locations,values=values)

#dashboard
@app.route('/dashboard')
def dashboard():

    # create cursor
    cur=mysql.connection.cursor()

    #get articles
    result=cur.execute("SELECT * from articles")

    articles = cur.fetchall()

    if result>0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg="No articles found"
        return render_template('dashboard.html',msg=msg)

    #connection close
    cur.close() 

    return render_template('dashboard.html')

############################ PRODUCT ###################################################
############################ PRODUCT ###################################################

#add product
class ProductForm(Form):
    product_id = StringField('Product ID',[validators.Length(min=1, max=200)])
    product_name = StringField('Product Name',[validators.Length(min=5)])

#products
@app.route('/products')
def products():
     # create cursor
    cur=mysql.connection.cursor()
    #get products
    result=cur.execute("SELECT * from product")
    products = cur.fetchall()

    if result>0:
        return render_template('/products/products.html', products=products)
    else:
        msg="No products found"
        return render_template('/products/products.html',msg=msg)

    #connection close
    cur.close() 

#add products
@app.route('/add_product',methods=["GET","POST"])
def add_product():
    form = ProductForm(request.form)
    if(request.method == "POST" and form.validate()):
        product_id = form.product_id.data
        product_name= form.product_name.data

        #Create cursor
        cur = mysql.connection.cursor()

        result = cur.execute('SELECT * FROM product where product_id=%s',[product_id])
        if result>0:
            flash("Product with this ID already exist","danger")
            return redirect(url_for("add_product"))
        else:   
            #excute query
            cur.execute("INSERT INTO product(product_id,product_name) VALUES(%s,%s)",(product_id,product_name))

            #commit to db
            mysql.connection.commit()

            #close cursor
            cur.close()
            flash("Product created","success")
            return redirect(url_for("products"))

    return render_template('/products/add_product.html',form=form)

#edit products
@app.route('/edit_product/<string:id>/',methods=["GET","POST"])
def edit_product(id):
    #create cursor
    cur = mysql.connection.cursor()

    #get product values
    result= cur.execute("SELECT * from product WHERE product_id=%s",[id])

    product=cur.fetchone()

    form = ProductForm(request.form)

    #populate the form 
    form.product_id.data=product['product_id']
    form.product_name.data=product['product_name']

    if(request.method == "POST" and form.validate()):
        product_id = request.form['product_id']
        product_name= request.form['product_name']
        cur = mysql.connection.cursor()
        
        try:
            cur.execute("UPDATE product SET product_id=%s, product_name=%s WHERE product_id=%s",(product_id,product_name,id))
            flash("Product Updated","success")
        except:
            flash("ID already exist","danger")

        mysql.connection.commit()
        cur.close()
        return redirect(url_for("products"))

    return render_template('/products/edit_product.html',form=form)

#delete product
@app.route('/delete_product/<string:id>/',methods=["POST"])
def delete_product(id):
   cur=mysql.connection.cursor()
   cur.execute("DELETE from product WHERE product_id=%s",[id])
   mysql.connection.commit()
   cur.close()
   flash("Product deleted","success")
   return redirect(url_for('products'))


############################ LOCATION ###################################################
############################ LOCATION ###################################################

class locationForm(Form):
    location_id = StringField('Location ID',[validators.Length(min=1, max=200)])
    location_name = StringField('Location Name',[validators.Length(min=1, max=200)])

#location
@app.route('/locations')
def locations():
    cur=mysql.connection.cursor()
    result=cur.execute("SELECT * from location")
    locations = cur.fetchall()

    if result>0:
        return render_template('/locations/locations.html', locations=locations)
    else:
        msg="No locations found"
        return render_template('/locations/locations.html',msg=msg)

    cur.close() 

#add product
@app.route('/add_location',methods=["GET","POST"])
def add_location():
    form = locationForm(request.form)
    if(request.method == "POST" and form.validate()):
        location_id = form.location_id.data
        location_name = form.location_name.data

        cur = mysql.connection.cursor()
        result = cur.execute('SELECT * FROM location where location_id=%s',[location_id])

        if result>0:
            flash("location with this ID already exist","danger")
            return redirect(url_for("add_location"))
        else:   
            cur.execute("INSERT INTO location(location_id,location_name) VALUES(%s,%s)",(location_id,location_name))
            mysql.connection.commit()
            cur.close()
            flash("location created","success")
            return redirect(url_for("locations"))

    return render_template('/locations/add_location.html',form=form)

#edit product
@app.route('/edit_location/<string:id>/',methods=["GET","POST"])
def edit_location(id):
    cur = mysql.connection.cursor()
    result= cur.execute("SELECT * from location WHERE location_id=%s",[id])

    location=cur.fetchone()
    form = locationForm(request.form)
    form.location_id.data=location['location_id']
    form.location_name.data=location['location_name']

    if(request.method == "POST" and form.validate()):
        location_id = request.form['location_id']
        location_name= request.form['location_name']
        cur = mysql.connection.cursor()
        
        try:
            cur.execute("UPDATE location SET location_id=%s,location_name=%s WHERE location_id=%s",(location_id,location_name,id))
            flash("Location Updated","success")
        except:
            flash("ID already exist","danger")
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("locations"))

    return render_template('/locations/edit_location.html',form=form)

#delete location
@app.route('/delete_location/<string:id>/',methods=["POST"])
def delete_location(id):
   cur=mysql.connection.cursor()
   cur.execute("DELETE from location WHERE location_id=%s",[id])
   mysql.connection.commit()
   cur.close()
   flash("location deleted","success")
   return redirect(url_for('locations'))

############################ PRODUCT MOVEMENT ###################################################
############################ PRODUCT MOVEMENT ###################################################

#product movement
@app.route('/productmovements')
def productmovements():
    cur=mysql.connection.cursor()
    #get productmovement
    result=cur.execute("SELECT * from productmovement")
    productmovement = cur.fetchall()

    if result>0:
        return render_template('/productmovement/productmovements.html', productmovements=productmovement)
    else:
        msg="No product movement found"
        return render_template('/productmovement/productmovements.html',msg=msg)

    cur.close() 

#add productmovement
@app.route('/add_productmovement',methods=["GET","POST"])
def add_productmovement():
    # form = productmovementForm(request.form)
    cur = mysql.connection.cursor()

    productresult=cur.execute("SELECT * from product")
    productlist = cur.fetchall()

    locationresult=cur.execute("SELECT * from location")
    locationlist = cur.fetchall()

    if request.method == "POST" :
        product_id = request.form['product_id']
        from_location = request.form['from_location']
        to_location = request.form['to_location']
        qty = request.form['quantity']

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO productmovement(product_id,from_location,to_location,qty) VALUES(%s,%s,%s,%s)",(product_id,from_location,to_location,qty))
        mysql.connection.commit()
        cur.close()
        flash("Product movement created","success")
        return redirect(url_for("productmovements"))

    return render_template('/productmovement/add_productmovement.html',productlist=productlist,locationlist=locationlist)


@app.route('/edit_productmovement/<string:id>/',methods=["GET","POST"])
def edit_productmovement(id):
    cur = mysql.connection.cursor()

    productresult=cur.execute("SELECT * from product")
    productlist = cur.fetchall()

    locationresult=cur.execute("SELECT * from location")
    locationlist = cur.fetchall()

    result= cur.execute("SELECT * from productmovement WHERE movement_id=%s",[id])

    productmovement=cur.fetchone()
    form={}
    form['product_id']=productmovement['product_id']
    form['from_location']=productmovement['from_location']
    form['to_location']=productmovement['to_location']
    form['qty']=productmovement['qty']

    if request.method == "POST" :
        product_id= request.form['product_id']
        from_location= request.form['from_location']
        to_location= request.form['to_location']
        qty= request.form['quantity']
        cur = mysql.connection.cursor()
        
        try:
            cur.execute("UPDATE productmovement SET product_id=%s,from_location=%s,to_location=%s,qty=%s WHERE movement_id=%s",(product_id,from_location,to_location,qty,id))
            flash("Product Movement Updated","success")
        except:
            flash("ID already exist","danger")
        
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("productmovements"))

    return render_template('/productmovement/edit_productmovement.html',form=form,productlist=productlist,locationlist=locationlist)



#delete productmovement
@app.route('/delete_productmovement/<string:id>/',methods=["POST"])
def delete_productmovement(id):
   cur=mysql.connection.cursor()
   cur.execute("DELETE from productmovement WHERE movement_id=%s",[id])
   mysql.connection.commit()
   cur.close()
   flash("Product movement deleted","success")
   return redirect(url_for('productmovements'))


if __name__ == "__main__":
    app.secret_key='secret123'
    app.run(debug=True)