from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
import markdown
import random

from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(label="title")
    entry = forms.CharField(label="entry", widget=forms.Textarea())


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    name = util.get_entry(entry)
    if name:
        return render(request, "encyclopedia/entry.html", {
            "name": markdown.markdown(name),
            "title": entry,
        })
    else:
        return render(request, "encyclopedia/error.html")


def search(request):
    query = request.GET['q']
    name = util.get_entry(query)

    if name:
        return render(request, "encyclopedia/entry.html", {
            "name": markdown.markdown(name),
            "title": query,
        })
    elif name == None:
        entries = util.list_entries()
        matches = []
        for entry in entries:
            if query.lower() in entry.lower():
                matches.append(entry)
        if len(matches) == 0:
            return render(request, "encyclopedia/error.html")
        return render(request, "encyclopedia/results.html", {
            "matches": matches,
            "query": query,
        })

def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title in util.list_entries():
                return render(request, "encyclopedia/new.html", {
                    "form": NewEntryForm(),
                    "invalid": True,
                    "title": title,
                })
            entry = form.cleaned_data["entry"]
            util.save_entry(title, entry)
            return redirect("entry", entry=title)
    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm(),
    })


def random_entry(request):
    random_entry = random.choice(util.list_entries())
    return entry(request, random_entry)


def edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })


def save(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        converted = markdown.markdown(content)
        return entry(request, title)