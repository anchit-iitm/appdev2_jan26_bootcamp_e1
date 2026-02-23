from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/hello')
def hello():
    return render_template('hello.html')

@app.route('/hello/<name>')
def hello_name(name):
    return render_template('hello1.html', html_name=name)

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method=="GET":
        return render_template('form.html')
    elif request.method=="POST":
        name = request.form.get('name')
        age = request.form.get('age')
        print(f"name: {name}, age: {age}")
        return redirect(url_for('hello_name', name=name))


if __name__ == '__main__':
    app.run()