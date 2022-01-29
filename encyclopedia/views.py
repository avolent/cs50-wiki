from logging import PlaceHolder
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import random as random2
import markdown2
from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
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
        "html": html,
        })

def search(request):
    if request.method == "POST":
        q = request.POST["q"].lower()
        entries = util.list_entries()
        searchlist = []
        for entry in entries:
            print(entry)
            if q == entry.lower():
                return HttpResponseRedirect(f"wiki/{entry}")
            elif q in entry.lower():
                print("Match, adding to search list")
                searchlist.append(entry)
                print(searchlist)
                continue
        return render(request, "encyclopedia/search.html", {
            "query": q,
            "searchlist": searchlist,
        })
    else:
        # Return to index (Good fail safe)
        return HttpResponseRedirect(reverse("views:index"))

def create(request):
    if request.method == "POST":
        title = util.get_entry(request.POST["title"])
        if title == None:
            title = util.save_entry(request.POST["title"], request.POST["content"])
            return HttpResponseRedirect(f"wiki/{request.POST['title']}")
        else:
            return render(request, "encyclopedia/error.html", {
            "error": "Error!",
            "html": f"Error! Page already exists."
            })          
            
    else:
        return render(request, "encyclopedia/create.html")

def edit(request, entry):
    if request.method == "POST":
        title = util.get_entry(request.POST["title"])
        if title == None:
             return render(request, "encyclopedia/error.html", {
            "error": "Error!",
            "html": f"Error! Page doesn't exist."
            })        
        else:
            title = util.save_entry(request.POST["title"], request.POST["content"])
            return HttpResponseRedirect(f"/wiki/{request.POST['title']}")
    else:
        content = util.get_entry(entry)
        return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "content": content
        })

def random(request):
    entries = util.list_entries()
    return HttpResponseRedirect(f"wiki/{random2.choice(entries)}")