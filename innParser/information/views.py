from django.shortcuts import render
from django.http import HttpResponse
from InfScanner import InformationCollector
from django.core.files.storage import FileSystemStorage
import os
import pathlib
import threading
column_name_relations = {"authCapital": "Уставной капитал",
        "phones": "Номера телефонов",
        "address": "Адрес",
        "workers": "Число сотрудников",
        "shortName": "Сокращ. имя",
        "fullName": "Полное имя",
        "ogrn": "ОГРН",
        "status": "Статус",
        "regDate": "Дата регистрации",
        "directors": "Управляющие",
        "holders": "Владельцы",
        "reportYear": "Год отчётности",
        "earnings": "Выручка",
        "govContracts": "Гос. контракты",
        "govBuyings": "Гос. закупки"}
def parser(request):
    
    return render(request, 'information/index.html', context = {"columns": column_name_relations.items(), "loaded" : False})



def upload_file(request):
    
    if request.method == 'POST' and request.FILES.get("file") != None:
        print(request.POST)
        myfile = request.FILES["file"]
        loc = os.path.join(pathlib.Path().absolute(), "information\\forscan")
        print(loc)
        fs = FileSystemStorage(location = loc)
        
        filename = fs.save(myfile.name, myfile)
        print(filename)
        print(filename)
        print(filename)
        print(filename)
        print(filename)
        print(filename)
        s = InformationCollector.InformationScanner()
        
        out_file = "information\\scanned\\" + filename
        infile = "information\\forscan\\" +filename

        print(request.POST)
        fields = {
            "inn": request.POST["inn_output"]
        }
        for c in dict(request.POST).keys():
            if c not in ['inn_input', 'inn_output', "csrfmiddlewaretoken"]:
                fields[c] = request.POST[c]
        print(fields)
        args = (infile, out_file, request.POST["inn_input"])
        kwargs = {"output_file_fields": fields}
        scanT = threading.Thread(target = s.scan, args = args, kwargs=kwargs)
        
        scanT.start()
        return render(request, 'information/index.html', context = {"columns": column_name_relations.items(), "loaded" : True, "ld_name": filename})

def results(request):
    import glob
    root = pathlib.Path(__file__).resolve().parent.parent
    fls = []
    print(glob.glob("information\\scanned\\*.xlsx"))
    #for f in glob.glob("inn\\scanned\\*.xlsx"):
    #    fls.append(os.path.join(pathlib.Path(__file__).resolve().parent.parent, f))
    
    return render(request, 'information/results.html', context = {"files": glob.glob("information\\scanned\\*.xlsx")})

# Create your views here.
def download(request):
    path = request.GET["file"]
    with open(path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
        return response
