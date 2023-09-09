import requests
import json
# from tutor.models import Course

BASE_URL = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232"


res_json=""
page = 1
while((res_json != "[]") and page<2):
    url = BASE_URL+"&page="+str(page)
    print(url)
    res = requests.get(url)
    res_json = res.json()
    print(res_json)
    page+=1
    for course_json in res_json:
        # course = Course(subject=course_json["subject"],catalog_num=course_json["catalog_nbr"],title=course_json["descr"])
        # print(course, course.title)
        print(course_json["subject"],course_json["catalog_nbr"],course_json["descr"])
       
