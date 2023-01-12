from PyQt5 import QtCore, QtGui, QtWidgets
from flask_mysqldb import MySQL
from flask import Flask,render_template,request,redirect,url_for,session,flash
import pymysql
import MySQLdb.cursors
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dimas123'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pelayanan'
mysql = MySQL(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        if '@' not in email:
            flash('Invalid Email', 'Cek Kembali Email Anda')
            return email
        else:
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM akun WHERE EMAIL = %s AND PASSWORD = %s", ([(email), (password)]))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['nama'] = account['nama']
                session['nik'] = account['nik']
                return redirect(url_for('home'))
            else:
                flash("Email/password! salah", "danger")
    return render_template('auth/login.html',title="Login")

@app.route('/daftar', methods=['GET','POST'])
def daftar():
    if request.method == 'POST' and 'nik' in request.form and 'password' in request.form and 'email' in request.form:
        nik = request.form['nik']
        nama = request.form['nama']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute( "SELECT * FROM akun WHERE nik LIKE %s", [nik] )
        account = cursor.fetchone()
        if account:
            flash("Akun telah tersedia!", "danger")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Alamat email invalid!", "danger")
        elif not re.match(r'[0-9]+', nik):
            flash("Nik hanya boleh angka!", "danger")
        #elif password or not email:
        #   flash("Incorrect nik/password!", "danger")
        else:
            password = request.form['password']
            confirmPass = request.form['confirmPass']
            if password != confirmPass:
                flash('password Error', 'Password tidak cocok')
                return password and confirmPass
            elif len(password) != len(confirmPass):
                flash('password Error', 'Password tidak cocok')
                return password and confirmPass
            else:
                phone = request.form['phone']
                sex = request.form['sex']
                address = request.form['address']
                cursor.execute('INSERT INTO akun VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', (nik,nama,email,password,confirmPass,phone,sex,address))
                mysql.connection.commit()
                flash("Registrasi Berhasil!", "Success")
                return redirect(url_for('login'))
    elif request.method == 'POST':
        flash("Mohon isi form!", "danger")
    return render_template('auth/daftar.html',title="Daftar")

@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('home/home.html',nama=session['nama'],title="Home")
    return redirect(url_for('login'))    

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        return render_template('auth/profile.html',nama = session['nama'] ,title="Profile")
    return redirect(url_for('login'))  

@app.route('/pengajuan', methods=['GET','POST'])
def pengajuan():
    if 'loggedin' in session:
        if request.method == 'POST':
            text = request.form['teks']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("insert into pengaduan values(%s)", (text,))
            mysql.connection.commit()
            cursor.execute("SELECT teks FROM pengaduan")
            value = cursor.fetchall()
        return render_template('auth/pengaduan.html',title="Forum")
    return redirect(url_for('pengajuan'))

@app.route('/ktp', methods=['GET','POST'])
def formktp():
    if 'loggedin' in session:
        if request.method == 'POST':
            req = request.form
            nik = req['nik']
            nokk = req['nokk']
            nama = req['nama']
            tempat = req['tempat']
            tanggal = req['tanggal']
            alamat = req['alamat']
            status = req['status']
            pekerjaan = req['pekerjaan']
            kewarganegaraan = req['kewarganegaraan']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("insert into ktp_baru values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(nik,nokk,nama,tempat,tanggal,alamat,status,pekerjaan,kewarganegaraan))
        return render_template('auth/form.html',title="Form")  
    return redirect(url_for('ktp'))

@app.route('/saran', methods=['GET','POST'])
def saran():
    if 'loggedin' in session:
        if request.method == 'POST':
            text = request.form['teks']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("insert into pengaduan values(%s)", (text,))
            mysql.connection.commit()
            cursor.execute("SELECT teks FROM pengaduan")
            value = cursor.fetchall()
        return render_template('auth/pengaduan.html',title="Forum")
    return redirect(url_for('pengajuan'))
if __name__ == "__main__" :
    app.run(debug=True)