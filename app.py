from flask import Flask, render_template, request , redirect ,url_for, flash
import mysql.connector

app = Flask(__name__)
my_db = mysql.connector.connect(host='localhost',user='root',password='Admin@123', database='todo')
my_cursor = my_db.cursor(dictionary=True)


@app.route('/')
def index():
    my_cursor.execute("select * from taskmanager")
    tasks = my_cursor.fetchall()
    return render_template('index.html', tasks=tasks)


@app.route('/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'GET':
        return render_template('create_task.html')
    task = request.form['task']
    status = request.form['status']
    remarks = request.form['remarks']
    sql = '''insert into taskmanager(task_name,status,remarks)
         values(%s,%s,%s)'''
    val = (task, status, remarks)
    my_cursor.execute(sql, val)
    my_db.commit()
    return redirect(url_for('index'))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    ID = int(id)
    if request.method == 'GET':
        return display_data(ID)
    task = request.form['task']
    status = request.form['status']
    remarks = request.form['remarks']
    sql = '''update taskmanager set
       task_name=%s,
       status=%s,
       remarks=%s where id=%s '''
    val = (task, status, remarks, id)
    my_cursor.execute(sql, val)
    my_db.commit()
    return redirect(url_for('index'))


@app.route('/update/<int:id>', methods=['GET'])
def display_data(ID):
    sql = '''select * from 
      taskmanager where id=%s'''
    val = (ID,)
    my_cursor.execute(sql, val)
    my_result = my_cursor.fetchone()
    return render_template('update_task.html',my_result=my_result)


@app.route('/delete/<int:id>',methods=['GET'])
def delete_task(id):
    ID = int(id)
    sql = '''delete from taskmanager
    where id=%s'''
    val=(ID,)
    my_cursor.execute(sql,val)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

