import os
import time
import sqlite3
from flask import Flask, render_template, request, send_file, session, redirect, url_for
from rembg import remove
from PIL import Image
from PyPDF2 import PdfMerger
import io

app = Flask(__name__)
app.secret_key="mysecretkey"

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()


@app.route('/')
def home():
    return render_template('index.html', active='home')

@app.route('/merge-pdf', methods=['GET', 'POST'])
def merge_pdf():
    if request.method == "POST":
        files = request.files.getlist("pdfs")

        merger = PdfMerger()

        for file in files:
            merger.append(file)

        output = io.BytesIO()
        merger.write(output)
        merger.close()
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="merged.pdf",
            mimetype="application/pdf"
        )

    return render_template("merge.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=? AND password=?", 
                  (username, password))

        user = c.fetchone()

        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid Login"


    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))


        conn.commit()
        conn.close()

        return render_template('login.html')

    return render_template('register.html')
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/remove', methods=['POST'])
def remove_bg():

    file = request.files['image']
    filename = str(int(time.time()))

    input_path = f"static/input_{filename}.png"
    output_path = f"static/output_{filename}.png"

    file.save(input_path)

    inp = Image.open(input_path)

    output = remove(inp)

    output.save(output_path)
    return render_template("index.html",
                       input_image=f"input_{filename}.png",
                       output_image=f"output_{filename}.png",
                       username=session.get("username"))
@app.route('/dashboard')
def dashboard():
    username = session.get('username')   # 👈 yaha fix

    return render_template(
        'dashboard.html',
        username=username , active='dashboard'
    )
@app.route('/pdf')
def pdf():
    return render_template('pdf.html', active='pdf')

if __name__ == '__main__':
    app.run(debug=True)
