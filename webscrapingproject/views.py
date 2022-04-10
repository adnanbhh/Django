from django.shortcuts import render
from django.http import HttpResponse
from webscrapingproject.script import script

def index(request):
    template_path = "webscrapingproject/home.html"


    context = {
        "img":
            "images/nada/logosearch.png"

    }

    return render(request, template_path, context)


def search(request):
    template_path = "webscrapingproject/search.html"
    context = {
        "img":
            "images/nada/logosearch.png",
    }
    if request.GET['sear']:
        keyword = request.GET['sear']
        Base = ['Base0', 'Base1', 'Base2', 'Base3', 'Base4', 'Base5', 'Base6']
        a = [keyword]
        # data retrieved
        context = { "img":
                "images/nada/logosearch.png",}
        for i in Base:
            try:
                strh = request.GET[i]
                a.append(strh)
                del strh
            except Exception as e:
                print(e)
        for i in a:
            if i == "pubmed":
                b = getKey("pubmed", keyword)
                thegood = {"DONNEE": b}
                context.update(thegood)
            if i == "espacenet":
                c = getKey("espacenet", keyword)
                thegood = {"DONNEE1": c}
                context.update(thegood)
            if i == "scopus":
                d = getKey("scopus", keyword)
                thegood = {"DONNEE2": d}
                context.update(thegood)
            if i == "UPTDO":
                e = getKey("UPTDO", keyword)
            if i == "IEEE":
                f = getKey("IEEE", keyword)
            if i == "wikipedia":
                g = getKey("wikipedia", keyword)
            if i == "google":
                h = getKey("google", keyword)

        cont = {

            "keyword": keyword,
            "BASE": a,
        }

        context.update(cont)

    else:
        context = {
            "img":
                "images/nada/logosearch.png",
            "keyword": "Data Not Found: No keyword"
        }


    return render(request, template_path, context)


def retrieveData(BD, key):
    import pymongo

    client = pymongo.MongoClient("mongodb://localhost:27017/")

    # Database Name
    db = client[BD]

    # Collection Name
    mycol = db[key]

    # Fields with values as 1 will
    # only appear in the result
    #chhhhehehehhehecker
    if BD == "pubmed":
        x = mycol.find({}, {'title': key, 'authors': 1, 'journal': 1, 'PMID': 1, 'title': 1})
        b = []
        for y in x:
            a = []
            for i in y.items():
                #print(i[1])
                if type(i[1]) == dict:
                    a.append(list(i[1].values()))
            b.append(a)
            del a
        return b
    if BD == "espacenet":

        x = mycol.find({}, {'title': key,'link': 1, 'inventor': 1, 'applicant': 1, 'CPC': 1, 'IPC': 1, 'publication info': 1,'priority date': 1, 'title': 1})
        b = []
        for y in x:
            a = []
            for i in y.items():
                #print(i[1])
                if type(i[1]) == dict:
                    a.append(list(i[1].values()))
            b.append(a)
            del a
        return b
    if BD == "scopus":

        x = mycol.find({}, {'title': key,'authors': 1, 'link':1, 'year': 1, 'source': 1, 'title': 1})
        b = []
        for y in x:
            a = []
            for i in y.items():
                #print(i[1])
                if type(i[1]) == dict:
                    a.append(list(i[1].values()))
            b.append(a)
            del a
        return b

def checkExistKeyInDB(DB, Key):
    from pymongo import MongoClient

    connection = MongoClient('localhost', 27017)
    db = connection[DB]
    if Key in db.list_collection_names():
        return True
    else:
        return False

#i is db
def getKey(i, keyword):
    b = []
    if checkExistKeyInDB(i, keyword):
        b.extend(retrieveData(i, keyword))
        return b
    else:
        if i == "pubmed":
            script.pubmed(keyword)
            b.extend(retrieveData(i, keyword))
            return b
        if i == "espacenet":
            script.espacenet(keyword)
            b.extend(retrieveData(i, keyword))
            return b
        if i == "scopus":
            script.scopus(keyword)
            b.extend(retrieveData(i, keyword))
            return b
        if i == "UPTDO":
            script.UPTDO(keyword)
            b.extend(retrieveData(i, keyword))
            return b
        if i == "IEEE":
            script.IEEE(keyword)
            b.extend(retrieveData(i, keyword))
            return b
        if i == "wikipedia":
            script.wikipedia(keyword)
            b.extend(retrieveData(i, keyword))
            return b
        if i == "google":
            script.google(keyword)
            b.extend(retrieveData(i, keyword))
            return b

