from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
from InfScanner import InformationCollector
from ScannerSetupper import *
def menu(request):
    return render(request, "menu/index.html")

def kontur_get_link(request):
    driver = InformationCollector.InformationScanner().driver
    email = request.GET.get("email_field", None)
    if email != None:
        konturGetLink(driver, email)
    return render(request, "menu/index.html")

def kontur_auth(request):
    driver = InformationCollector.InformationScanner().driver
    link = request.GET.get("link_field", None)
    if link != None:
       konturAuth(driver, link)
    return render(request, "menu/index.html")

def sbis_auth(request):
    driver = InformationCollector.InformationScanner().driver
    sbisAuth(driver)
    return render(request, "menu/index.html")