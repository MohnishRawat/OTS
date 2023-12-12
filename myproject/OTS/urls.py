from django.urls import path
from OTS.views import *

app_name = "OTS"
urlpatterns = [
    path("new", wellcome),
    path("new-candidate/", CandidateRegistrationForm, name="registrationform"),
    path("store-candidate", CandidateRegistration, name="Registration"),
    path("login", LoginView, name="login"),
    path("home", CandidateHome, name="home"),
    path("test-paper", testPaper, name="testpaper"),
    path("calculate-result", CalculateTestResult, name="calculateTest"),
    path("test-history", testResultHistory, name="testhistory"),
    path("result", showTestResult, name="result"),
    path("logout", logoutView, name="logout"),
]
