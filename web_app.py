# web_app.py
import threading
import webbrowser
from pathlib import Path

from flask import Flask, render_template, request

from downloader import download_images, DownloadError

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static"),
)


@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    error = None
    details = None
    form_values = {
        "url": "",
        "folder": str(BASE_DIR / "downloads"),
        "naming_scheme": "original",
    }

    if request.method == "POST":
        form_values["url"] = request.form.get("url", "").strip()
        form_values["folder"] = request.form.get("folder", form_values["folder"]).strip()
        form_values["naming_scheme"] = request.form.get("naming_scheme", "original")

        try:
            result = download_images(
                page_url=form_values["url"],
                target_folder=form_values["folder"],
                naming_scheme=form_values["naming_scheme"],
            )

            if result["count"] == 0:
                message = "Keine Bilder gefunden oder heruntergeladen."
            else:
                message = (
                    f"{result['count']} Bilder wurden nach "
                    f"„{result['folder']}“ heruntergeladen."
                )

            if result["errors"]:
                error = f"{len(result['errors'])} Bilder konnten nicht geladen werden."
                details = result["errors"]

        except DownloadError as e:
            error = str(e)
        except Exception as e:
            error = f"Unerwarteter Fehler: {e!r}"

    return render_template(
        "index.html",
        message=message,
        error=error,
        details=details,
        form_values=form_values,
    )


def open_browser():
    webbrowser.open("http://127.0.0.1:5000", new=1)


if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=False)
