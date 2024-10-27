from flask import Flask, render_template, send_file
import random

app = Flask(__name__)

# Generate random leaderboard data


def generate_leaderboard_data():
    applications = ['App1', 'App2', 'App3', 'App4', 'App5']
    data = []
    for app in applications:
        data.append({
            'application': app,
            'average': round(random.uniform(70, 100), 2),
            'ifeval': round(random.uniform(70, 100), 2),
            'bbh': round(random.uniform(70, 100), 2),
            'math_lvl_5': round(random.uniform(70, 100), 2),
            'gpqa': round(random.uniform(70, 100), 2),
            'musr': round(random.uniform(70, 100), 2),
            'mmlu_pro': round(random.uniform(70, 100), 2)
        })
    return data

# Route for the index page


@app.route('/')
def index():
    return render_template('index.html')

# Route for the downloads page


@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

# Route for the leaderboard page


@app.route('/leaderboard')
def leaderboard():
    data = generate_leaderboard_data()
    return render_template('leaderboard.html', data=data)

# Route to handle file downloads


@app.route('/download-file/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

# Route for the login page


@app.route('/login')
def login():
    return render_template('login.html')

# Route for the register page


@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
