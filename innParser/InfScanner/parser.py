from bs4 import BeautifulSoup as bs
import glob
def parser(soup):
    def find_type(fields):    
        for field in fields:
            if "директор" in field.find("div").text.lower():
                return "company"
            if "лицо" in field.find("div").text.lower():
                return "ip"
    def company_fields_parser(fields):
        leader = ""
        holders = []
        capital = ""
        slaves = ""
        address = ""
        for field in fields:
            fn = field.find("div").text.lower()
            if "директор" in fn:
                leader = " ".join(field.find("div", {"class", "_1jE0i"}).find("span", {"class", "_1Lp34 Ps02p"}).text.split()[::-1][1::][::-1])
            if "учредители" in fn:
                hrs = field.find_all("div", {"class", "_1jE0i"})
                
                for h in hrs:
                    holder = " ".join(h.find("span", {"class", "_1Lp34 Ps02p"}).text.split()[::-1][1::][::-1])
                    holders.append(holder)
        return leader, holders

    companies = soup.find_all("div", {"class":"_30ae9 _1nUgx"})
    for company in companies:
        print("-----------------------------------------")
        header = company.find("div")
        name = header.find("h4", {"class":"_3vWPI _3rH6p"}).text
        inn = header.find("div", {"class":"_2AYPT"}).find_all("span", {"class":"_2KHAQ"})[0].text.replace(" ","").replace("ИНН","").replace(":","")
        ogrn = header.find("div", {"class":"_2AYPT"}).find_all("span", {"class":"_2KHAQ"})[1].text.replace(" ","").replace("ОГРН","").replace(":","")
        print(inn,ogrn)
        print(name)
        fields = company.find_all("div", {"class":"_34Ym4"})
        #print(fields)
        if find_type(fields) == "company":
            print(company_fields_parser(fields))



    pass

for file in glob.glob("dumps\\*.html"):
    with open(file, "r", encoding="utf-8") as f:
        src = f.read()
    soup = bs(src, features = "html.parser")
    parser(soup)
    break
    