from django.shortcuts import render
from django.http import HttpResponse
from InfScanner import InformationCollector
from django.core.files.storage import FileSystemStorage
import os
import pathlib
import threading
import MainScanner
column_name_relations = {
    "inn": "ИНН",
    "authCapital": "Уставной капитал",
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
        "govBuyings": "Гос. закупки",
        "region": "Регион",
        "city": "Город"
        }
def parser(request):
    
    return render(request, 'mainscanner/index.html', context = {"columns": column_name_relations.items(), "loaded" : False})



def upload_file(request):
    
    if request.method == 'POST' and request.FILES.get("file") != None:
        
        myfile = request.FILES["file"]
        loc = os.path.join(pathlib.Path().absolute(), "mainscanner\\forscan")
        print(loc)
        fs = FileSystemStorage(location = loc)
        
        filename = fs.save(myfile.name, myfile)
    
        
        
        out_file = "mainscanner\\scanned\\" + filename
        infile = "mainscanner\\forscan\\" +filename

        #print(request.POST)
        
        services = {
             "inn_parser": False,
            "information_scanner": False,
            "okved_scanner": False,
        }
        for n in services.keys():
            services[n] = n in request.POST
        


        fields = {
            'inn_search_columns': request.POST['inn_search_columns'].split(),
            'inn_search_key_column': request.POST["inn_search_key_column"].strip()
        }
        for c in column_name_relations.keys():
            #print(c, request.POST[c])
            try:
                
                if request.POST[c] == 'on':
                    fields[c] = "auto"
                    continue
                fields[c] = request.POST[c]
            except:
                continue
           
            
        print(fields)
        args = (infile, out_file)
        kwargs = {"fields": fields, "services": services}
        scanT = threading.Thread(target = MainScanner.scan, args = args, kwargs=kwargs)
        
        scanT.start()
        
        return render(request, 'mainscanner/index.html', context = {"columns": column_name_relations.items(), "loaded" : True, "ld_name": filename})

def results(request):
    import glob
    root = pathlib.Path(__file__).resolve().parent.parent
    fls = []
    print(glob.glob("mainscanner\\scanned\\*.xlsx"))
    #for f in glob.glob("inn\\scanned\\*.xlsx"):
    #    fls.append(os.path.join(pathlib.Path(__file__).resolve().parent.parent, f))
    
    return render(request, 'mainscanner/results.html', context = {"files": glob.glob("mainscanner\\scanned\\*.xlsx")})

# Create your views here.
def download(request):
    path = request.GET["file"]
    with open(path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
        return response
