import os
from flask import Flask, render_template, request
from uiskill_agent import get_response_for_user

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    profile = skills = error_msg = user_name = None

    if request.method == 'POST':
        user_name = request.form.get('username')
        if not user_name:
            error_msg = "Please enter a user name."
        else:
            try:
                profile, skills = get_response_for_user(user_name)
            except Exception as e:
                error_msg = f"⚠️ Error: {str(e)}"

    return render_template('index1.html',
                           profile=profile, 
                           skills=skills,
                           user_name=user_name,
                           error_msg=error_msg)

if __name__ == '__main__':
    # Use the port provided by Render or default to 5000 for local testing
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
