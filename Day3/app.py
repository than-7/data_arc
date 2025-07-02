from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

@app.route('/', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Normally, you'd save to DB here
        print(f"Feedback received from {name} ({email}): {message}")
        flash("✅ Thank you for your feedback!")

        return redirect('/')
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(debug=True)
