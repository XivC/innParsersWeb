from django.shortcuts import render
from django.http import HttpResponse
from .Scanner import *
from django.core.files.storage import FileSystemStorage
import os
import pathlib
import threading
def parser(request):
    n = 'Artem'
    print(111)
    return render(request, 'inn/index.html')


def getInn(request):
    s = Scanner()
    query = request.GET.get("results", "-")
    inn = s.search(query)
    if inn == False:
        return render(request, 'inn/index.html', context = {"inn": "Ничего не найдено", "color": "red"})
    
    return render(request, 'inn/index.html', context = {"inn": inn, "color": "green"})


def upload_file(request):
    
    if request.method == 'POST' and request.FILES.get("file") != None:
        print(request.POST)
        myfile = request.FILES["file"]
        loc = os.path.join(pathlib.Path().absolute(), "inn\\forscan")
        print(loc)
        fs = FileSystemStorage(location = loc)
        
        filename = fs.save(myfile.name, myfile)
        
        s = Scanner()
        key_input = request.POST['key_input'].replace(" ","")
        query_input = request.POST['query_input'].split()
        print(query_input)
        write_input = request.POST['write_input'].replace(" ","")
        out_file = "inn\\scanned\\" + "result_" + filename
        infile = "inn\\forscan\\" + filename
        ignore_input = request.POST['ignore_input'].split()
        number_correction = request.POST['number_correction'].split()
        json_in_path = "inn\\forscan_jsons\\" + filename + ".json"
        json_out_path = "inn\\scanned_jsons\\" + "result_" + filename + ".json"


        args = (infile, key_input, query_input ,write_input ,out_file)
        kwargs = {"ignore": ignore_input, "number_correction": number_correction, "inJson": json_in_path, "outJson": json_out_path}
        scanT = threading.Thread(target = s.scan_xlsx_to_xlsx, args = args, kwargs=kwargs)
        
        scanT.start()

    return render(request, 'inn/index.html', context = {"inn": "загружено", "color": "green"})

def results(request):
    import glob
    root = pathlib.Path(__file__).resolve().parent.parent
    fls = []
    print(glob.glob("inn\\scanned\\*.xlsx"))
    #for f in glob.glob("inn\\scanned\\*.xlsx"):
    #    fls.append(os.path.join(pathlib.Path(__file__).resolve().parent.parent, f))
    
    return render(request, 'inn/results.html', context = {"files": glob.glob("inn\\scanned\\*.xlsx")})

# Create your views here.
def download(request):
    path = request.GET["file"]
    with open(path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
        return response
