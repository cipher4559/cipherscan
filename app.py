from flask import Flask, render_template, request, redirect, url_for, flash, abort, send_from_directory
from concurrent.futures import ThreadPoolExecutor
from config import FLASK_SECRET_KEY, MAX_CONCURRENT_SCANS
from db import init_db, insert_scan, get_all_scans, get_scan_with_findings, is_domain_running
from modules.utils import validate_domain
from modules.ratelimit import is_rate_limited, record_scan
from cipherscan import main

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

init_db()

executor = ThreadPoolExecutor(max_workers=MAX_CONCURRENT_SCANS)


@app.route("/")
def index():
    scans = get_all_scans()
    return render_template("index.html", scans=scans)


@app.route("/scan", methods=["POST"])
def scan():
    domain     = request.form.get("domain", "").strip().lower()
    authorized = request.form.get("authorized") == "on"

    if not validate_domain(domain):
        flash("Invalid domain. Please enter a valid hostname (e.g. example.com).", "error")
        return redirect(url_for("index"))

    if not authorized:
        flash("You must confirm you are authorized to scan this target.", "error")
        return redirect(url_for("index"))

    if is_domain_running(domain):
        flash(f"A scan for {domain} is already running.", "warning")
        return redirect(url_for("index"))

    limited, remaining = is_rate_limited(domain)
    if limited:
        flash(f"{domain} was scanned recently. Try again in {remaining}s.", "warning")
        return redirect(url_for("index"))

    scan_id = insert_scan(domain)
    record_scan(domain)
    executor.submit(main, domain, scan_id, authorized)

    flash(f"Scan started for {domain}.", "success")
    return redirect(url_for("index"))


@app.route("/results/<int:scan_id>")
def results(scan_id):
    scan, findings = get_scan_with_findings(scan_id)
    if not scan:
        abort(404)
    return render_template("results.html", scan=scan, findings=findings)


@app.route("/download/<path:filename>")
def download(filename):
    """Serve files from the output/ directory (PDF, JSON, CSV reports)."""
    import os
    # Security: only allow files inside the output/ folder
    safe_root = os.path.abspath("output")
    target    = os.path.abspath(os.path.join("output", filename))
    if not target.startswith(safe_root):
        abort(403)
    directory = os.path.dirname(target)
    fname     = os.path.basename(target)
    return send_from_directory(directory, fname, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
