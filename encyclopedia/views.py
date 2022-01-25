from django.http import HttpResponse
from django.shortcuts import render
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()

    })

def entry(request, entry):
    if util.get_entry(entry) == None:
        return render(request, "encyclopedia/error.html", {
        "error": "Error!",
        "html": f"Error! The page '{entry}' does not exist on this wiki."
        })
    else:
        html = markdown2.markdown_path(f"entries/{entry}.md")
        return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "html": html
        })

def search(request):
    print(request)
    return HttpResponse("test")