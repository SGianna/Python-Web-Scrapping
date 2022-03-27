from flask import Flask, render_template, request,redirect, send_file
from indeed import get_jobs as get_indeed_jobs
from stackoverflow import get_jobs as get_stackoverflow_jobs
from save import save_to_file

app = Flask("JobScrapper")

db = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        existing_jobs = db.get(word)
        if existing_jobs:
            jobs = existing_jobs
        else:
            so_jobs = get_stackoverflow_jobs(word)
            indeed_jobs = get_indeed_jobs(word)
            jobs = so_jobs + indeed_jobs
            db[word] = jobs
    else:
        return redirect("/")
    return render_template(
        "report.html",searchingBy = word, 
        resultsNumber = len(jobs), 
        jobs = jobs)

@app.route("/export")
def export():
    try:
        word = request.args.get('word')    
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(word, jobs)
        return send_file(f"{word}_jobs.csv")
    except:
        return redirect("/")
app.run(host="0.0.0.0")