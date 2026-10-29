

\# Campus Assignment Portal



A Flask-based web application for submitting and validating student assignments.



\## Features



\- Student name, registration number, assignment title, and submission URL.

\- Required-field validation.

\- Basic HTTP/HTTPS URL validation.

\- Display of valid submissions.

\- Automated tests using pytest.

\- GitHub Actions CI pipeline (to be configured).



\## Requirements



\- Python 3

\- Git

\- pip



\## Setup Instructions



Clone the repository:



```powershell

git clone https://github.com/MahreenMalik05/campus-assign-portal

cd YOUR\_REPOSITORY\_FOLDER

```



Create and activate a virtual environment:



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

```



Install dependencies:



```powershell

python -m pip install -r requirements.txt

```



\## Run the Application



```powershell

python app.py

```



Open http://127.0.0.1:5000 in your browser.



\## Run Automated Tests



```powershell

python -m pytest -v

```



\## Project Structure



\- `app.py` — Flask application.

\- `tests/test\_portal.py` — automated tests.

\- `receiver/report\_receiver.py` — local report receiver.

\- `.github/workflows/ci-pipeline.yml` — CI workflow.

\- `requirements.txt` — Python dependencies.



