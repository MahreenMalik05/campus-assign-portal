
from flask import Flask, request, render_template_string
from urllib.parse import urlparse

app = Flask(__name__)

submissions = []

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campus Assignment Portal</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 850px;
            margin: 35px auto;
            padding: 20px;
            background: #f2f5f9;
        }
        h1, h2 { color: #203864; }
        form, .submission {
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
        }
        label { display: block; margin-top: 12px; }
        input {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            box-sizing: border-box;
        }
        button {
            margin-top: 18px;
            padding: 11px 20px;
            background: #203864;
            color: white;
            border: none;
            cursor: pointer;
        }
        .success { color: green; }
        .error { color: #b00020; }
    </style>
</head>
<body>
    <h1>Campus Assignment Portal</h1>
    <p>Submit your assignment details below.</p>

    {% if message %}
        <p class="{{ category }}">{{ message }}</p>
    {% endif %}

    <form method="POST" action="/">
        <label for="student_name">Student Name</label>
        <input id="student_name" name="student_name"
               value="{{ form_data.get('student_name', '') }}">

        <label for="registration_number">Registration Number</label>
        <input id="registration_number" name="registration_number"
               value="{{ form_data.get('registration_number', '') }}">

        <label for="assignment_title">Assignment Title</label>
        <input id="assignment_title" name="assignment_title"
               value="{{ form_data.get('assignment_title', '') }}">

        <label for="submission_url">Submission URL</label>
        <input id="submission_url" name="submission_url"
               value="{{ form_data.get('submission_url', '') }}">

        <button type="submit">Submit Assignment</button>
    </form>

    <h2>Saved Submissions</h2>

    {% if submissions %}
        {% for item in submissions %}
            <div class="submission">
                <p><strong>Name:</strong> {{ item.student_name }}</p>
                <p><strong>Registration:</strong>
                   {{ item.registration_number }}</p>
                <p><strong>Assignment:</strong> {{ item.assignment_title }}</p>
                <p><strong>URL:</strong>
                   <a href="{{ item.submission_url }}" target="_blank"
                      rel="noopener noreferrer">
                      {{ item.submission_url }}
                   </a>
                </p>
            </div>
        {% endfor %}
    {% else %}
        <p>No submissions yet.</p>
    {% endif %}
</body>
</html>
"""

def valid_submission_url(value):
    return True


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    category = ""
    form_data = {}

    if request.method == "POST":
        form_data = {
            "student_name": request.form.get("student_name", "").strip(),
            "registration_number": request.form.get(
                "registration_number", ""
            ).strip(),
            "assignment_title": request.form.get(
                "assignment_title", ""
            ).strip(),
            "submission_url": request.form.get(
                "submission_url", ""
            ).strip(),
        }

        if not all(form_data.values()):
            message = "Error: All fields are required."
            category = "error"

        elif not valid_submission_url(form_data["submission_url"]):
            message = "Error: Please enter a valid HTTP or HTTPS URL."
            category = "error"

        else:
            submissions.append(form_data.copy())
            message = "Assignment submitted successfully!"
            category = "success"
            form_data = {}

    return render_template_string(
        HTML_PAGE,
        submissions=submissions,
        message=message,
        category=category,
        form_data=form_data,
    )


if __name__ == "__main__":
    app.run(debug=True)
