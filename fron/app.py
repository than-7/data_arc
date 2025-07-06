from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form-schema')
def form_schema():
    schema = {
        "title": "User Info",
        "fields": [
            { "label": "Name", "type": "text", "name": "name" },
            { "label": "Email", "type": "email", "name": "email" },
            { "label": "Age", "type": "number", "name": "age" },
            { "label": "Subscribe", "type": "checkbox", "name": "subscribe" }
        ]
    }
    return jsonify(schema)

if __name__ == '__main__':
    app.run(debug=True)
