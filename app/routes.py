from flask import Blueprint, render_template, redirect, url_for, flash, request
import os

from config import Config
from .services.pandas_service import DatasetAnalyzer
from .services.gemini_service import generate_ai_insight

# Defines the main blueprint that groups application routes.
main = Blueprint("main", __name__)


# Renders the homepage with upload form and list of uploaded files.
@main.route("/")
def index():
    upload_folder = Config.UPLOAD_FOLDER
    os.makedirs(upload_folder, exist_ok=True)
    files = os.listdir(upload_folder)

    return render_template("index.html", files=files)


# Handles file upload and redirects to the dataset detail page.
@main.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")

    if not file:
        flash("No file selected!", "error")
        return redirect(url_for("main.index"))

    filename = file.filename

    if not filename.lower().endswith(".csv"):
        flash("Only CSV files allowed!", "error")
        return redirect(url_for("main.index"))

    upload_path = os.path.join(Config.UPLOAD_FOLDER, filename)

    # Ensure upload directory exists
    os.makedirs(os.path.dirname(upload_path), exist_ok=True)

    # Save file to disk
    file.save(upload_path)

    flash(f"{filename} uploaded successfully!", "success")
    return redirect(url_for("main.dataset_detail", filename=filename))


# Displays analysis details and AI insights for a specific uploaded dataset.
@main.route("/datasets/<filename>")
def dataset_detail(filename):
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        flash("File not found!", "error")
        return redirect(url_for("main.index"))

    analyzer = DatasetAnalyzer(filepath)

    shape = analyzer.shape()
    preview = analyzer.preview()
    summary = analyzer.summary()
    missing = analyzer.missing_values()
    correlations = analyzer.correlations()
    column_types = analyzer.column_types()

    # Default AI insight to None in case Gemini fails.
    ai_insight = None
    try:
        ai_insight = generate_ai_insight(
            filename=filename,
            rows=shape["rows"],
            columns=shape["columns"],
            column_types=column_types,
            missing=missing,
            summary=summary,
            correlations=correlations,
        )
    except Exception as e:
        # Avoid crashing the page if AI fails; just show a small note.
        ai_insight = f"AI insight could not be generated: {e}"

    return render_template(
        "dataset_detail.html",
        filename=filename,
        rows=shape["rows"],
        columns=shape["columns"],
        preview=preview,
        summary=summary,
        missing=missing,
        correlations=correlations,
        column_types=column_types,
        ai_insight=ai_insight,
    )
