from django.shortcuts import render
from django.http import HttpResponse
from InfScanner import InformationCollector
from django.core.files.storage import FileSystemStorage
import os
import pathlib
import threading
column_name_relations = {"main": "Основной код деятильности",
        "additional": "Дополнительные коды деятельность",
        "all_start": "Таблицу кодов записывать с колонки",
       }
def parser(request):
    
    return render(request, 'okved/index.html', context = {"columns": column_name_relations.items(), "loaded" : False})



def upload_file(request):
    
    if request.method == 'POST' and request.FILES.get("file") != None:
        print(request.POST)
        myfile = request.FILES["file"]
        loc = os.path.join(pathlib.Path().absolute(), "okved\\forscan")
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
        
        out_file = "okved\\scanned\\" + filename
        infile = "okved\\forscan\\" +filename

        print(request.POST)
        fields = {
            "main": request.POST["main"],
            "additional": request.POST["additional"],
            "all_start": request.POST["all_start"]
        }
        
        print(fields)
        og_in = request.POST["ogrn_input"]
        og_out = request.POST["ogrn_input"]
        args = (infile, out_file, og_in, og_out)
        kwargs = {"output_file_fields": fields}
        scanT = threading.Thread(target = s.scanOkveds, args = args, kwargs=kwargs)
        
        scanT.start()
        return render(request, 'okved/index.html', context = {"columns": column_name_relations.items(), "loaded" : True, "ld_name": filename})

def results(request):
    import glob
    root = pathlib.Path(__file__).resolve().parent.parent
    fls = []
    print(glob.glob("okved\\scanned\\*.xlsx"))
    #for f in glob.glob("inn\\scanned\\*.xlsx"):
    #    fls.append(os.path.join(pathlib.Path(__file__).resolve().parent.parent, f))
    
    return render(request, 'okved/results.html', context = {"files": glob.glob("okved\\scanned\\*.xlsx")})

# Create your views here.
def download(request):
    path = request.GET["file"]
    with open(path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
        return response
