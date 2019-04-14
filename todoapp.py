from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
import pickle
import re
import os

app = Flask(__name__)
error_flg = 'f'  # error flag for show error message on html
dic_no = 0
todo_list = []

@app.before_first_request
def function_to_run_only_once():
    global dic_no
    global todo_list
    exists = os.path.isfile('todolist.bin')
    if exists:
        with open('todolist.bin', 'rb') as f:
            while True:
                try:
                    data = pickle.load(f)
                except EOFError:
                    break
                dic_no = len(data)
                todo_list = data
    else:
        todo_list = []

@app.route('/')
def view_list():
    global error_flg

    return render_template('index.html', todo_list = todo_list, error_flg = error_flg)

@app.route('/hello')
def hello():
    return 'hello world'

@app.route('/submit', methods = ['post'])
def submit():
    global error_flg
    global dic_no
    oktoprc = 'f'
    #  read post form values
    id = dic_no
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']

    #  check validation for correct email format and priority value
    if re.search('@', email) and re.search('Low|Medium|High', priority):
        oktoprc = 't'

    if oktoprc == 't':
        # Append a new key value pair in dictionary
        #todo_list.update({dic_no: [task, email, priority]})
        todo_list.append({'id': id, 'task': task, 'email': email, 'priority': priority})
        dic_no += 1
        error_flg = 'f'

        return redirect('/')
    else:
        error_flg = 't'
        return redirect('/')

#  clear form and redirct to controller
@app.route('/clear', methods = ['post'])
def clear():
    global error_flg
    global dic_no
    del todo_list[:]
    if len(todo_list) == 0:
        error_flg = 'f'
        dic_no = 0
        return redirect('/')
    else:
        error_flg = 'c'
        return redirect('/')

@app.route('/delete', methods = ['post'])
def delete():
    global error_flg
    global dic_no
    # get hidden id from html form
    todoid = request.form['todoid']
    # get list index and value
    for i, v in enumerate(todo_list):
        delete_id = v['id']
        if int(delete_id) == int(todoid):
            del todo_list[i]

    return redirect('/')

@app.route('/save', methods = ['post'])
def save():
    global error_flg
    error_flg = 's' # save success message flag
    with open('todolist.bin','wb') as f:
        pickle.dump(todo_list, f)
    return redirect('/')

if __name__ == '__main__':
    app.run()