from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def hello_admins():
    return 'WElcome to the danger zone'

@app.route('/hello/<name>')
def hello_name(name):
    if name == 'admin':
        return redirect(url_for('hello_admins'))
    else:
        return 'Oh hai %s' % name


@app.route('/loginPage')
def loadLogin():
    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('login_success', name=user))
    else:
        return redirect(url_for('loadLogin'))        
        
@app.route('/success/<name>')
def login_success(name):
    return render_template('hello.html', user=name)

if __name__ == '__main__':
    app.debug = True
    app.run()