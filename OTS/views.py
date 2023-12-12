from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from OTS.models import *
import random


def wellcome(request):
    template = loader.get_template("wellcome.html")
    return HttpResponse(template.render({}, request))


def CandidateRegistrationForm(request):
    res = render(request, "registration.html")
    return res


def CandidateRegistration(request):
    if request.method == "POST":
        username = request.POST["username"]
        # Check if user already exist
        if len(Candidate.objects.filter(username=username)):
            userStatus = 1
        else:
            candidate = Candidate()
            candidate.username = username
            candidate.name = request.POST["fname"]
            candidate.password = request.POST["fpass"]
            candidate.save()
            userStatus = 2
    else:
        userStatus = 3  # request method in not POST

    context = {"userStatus": userStatus}

    res = render(request, "Checkregistration.html", context)
    return res


def LoginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        candidate = Candidate.objects.filter(username=username, password=password)
        if len(candidate) == 0:
            loginError = "Invalid Username or Password"
            res = render(request, "login.html", {"loginError": loginError})
        else:
            # login success
            request.session["username"] = candidate[0].username
            request.session["name"] = candidate[0].name
            res = HttpResponseRedirect("home")
    else:
        res = render(request, "login.html")
    return res


def CandidateHome(request):
    if "name" not in request.session.keys():
        res = HttpResponseRedirect("login")
    else:
        res = render(request, "home.html")
    return res


def testPaper(request):
    if "name" not in request.session.keys():
        res = HttpResponseRedirect("login")
    # fetch questions from database table
    n = int(request.GET["n"])
    question_pool = list(Question.objects.all())
    random.shuffle(question_pool)
    question_list = question_pool[:n]
    context = {"questions": question_list}
    res = render(request, "testpaper.html", context)
    return res


def CalculateTestResult(request):
    if "name" not in request.session.keys():
        res = HttpResponseRedirect("login")
    total_attempt = 0
    total_right = 0
    total_wrong = 0
    qid_list = []
    for k in request.POST:
        if k.startswith("qno"):
            qid_list.append(int(request.POST[k]))

    for n in qid_list:
        question = Question.objects.get(qid=n)
        try:
            if question.ans == request.POST["q" + str(n)]:
                total_right += 1
            else:
                total_wrong += 1
            total_attempt += 1
        except:
            pass
    points = (total_right - total_wrong) / len(qid_list) * 10
    # store result in result table
    result = Result()
    result.username = Candidate.objects.get(username=request.session["username"])
    result.attempts = total_attempt
    result.right = total_right
    result.wrong = total_wrong
    result.points = points
    result.save()

    # Update Candidate table
    candidate = Candidate.objects.get(username=request.session["username"])
    candidate.test_attempted += 1
    candidate.points = (
        candidate.points * (candidate.test_attempted - 1) + points
    ) / candidate.test_attempted
    candidate.save()
    return HttpResponseRedirect("result")


def testResultHistory(request):
    if "name" not in request.session.keys():
        res = HttpResponseRedirect("login")
    candidate = Candidate.objects.filter(username=request.session["username"])
    results = Result.objects.filter(username_id=candidate[0].username)
    context = {"candidate": candidate[0], "results": results}
    res = render(request, "candidate_history.html", context)
    return res


def showTestResult(request):
    if "name" not in request.session.keys():
        res = HttpResponseRedirect("login")
    # fetch latest result from Result table
    result = Result.objects.filter(
        result_id=Result.objects.latest("result_id").result_id,
        username_id=request.session["username"],
    )
    context = {"result": result}
    res = render(request, "show_result.html", context)
    return res


def logoutView(request):
    if "name" in request.session.keys():
        del request.session["username"]
        del request.session["name"]
    return HttpResponseRedirect("login")
