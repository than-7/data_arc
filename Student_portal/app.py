from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Connect to DB
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Add new student
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        department = request.form['department']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO students (name, age, department) VALUES (?, ?, ?)', (name, age, department))
        conn.commit()
        conn.close()
        
        return redirect('/view')
    return render_template('add.html')

# View all students
@app.route('/view')
def view():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('view.html', students=students)

# Edit student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        department = request.form['department']

        conn.execute('UPDATE students SET name = ?, age = ?, department = ? WHERE id = ?',
                     (name, age, department, id))
        conn.commit()
        conn.close()
        return redirect('/view')

    conn.close()
    return render_template('edit.html', student=student)

# Delete student
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/view')

if __name__ == '__main__':
    app.run(debug=True)
