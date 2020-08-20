#uci_soc_bot.py

from bs4 import BeautifulSoup
import requests
import urllib.request
import urllib.parse
import csv

URL = "https://www.reg.uci.edu/perl/WebSoc"

def get_departments():
    page = get_html(URL)
    soup = BeautifulSoup(page, 'html.parser')
    
    departments = {}

    for select in soup.find_all(name="select", attrs={"name": "Dept"}):
        for option in select.find_all(name="option"):
            departments[option.get('value')] = option.text
    


    return departments

def get_breadths():
    page = get_html(URL)
    soup = BeautifulSoup(page, 'html.parser')
    

    breadths = {}

    for select in soup.find_all(name="select", attrs={"name": "Breadth"}):
        for option in select.find_all(name="option"):
            breadths[option.get('value')] = option.text
    
    return breadths

def get_quarters():
    page = get_html(URL)
    soup = BeautifulSoup(page, 'html.parser')
    
    quarters = {}
    for select in soup.find_all(name="select", attrs={"name": "YearTerm"}):
        for option in select.find_all(name="option"):
            quarters[option.get('value')] = option.text

    return quarters

def get_classes(params):
    url = get_url(params)
    page = get_html(url)

    soup = BeautifulSoup(page, 'html.parser')

    course_list = soup.find(name="div", attrs={"class": "course-list"})

    if not course_list:
        return None

    classes = {}
    # columns = ['code',
    #     'type',
    #     'section',
    #     'units',
    #     'instructor',
    #     'time',
    #     'place',
    #     'final',
    #     'max',
    #     'enrolled',
    #     'waitlist',
    #     'requests',
    #     'nor',
    #     'restrictions',
    #     'status']
    course_title = ""
    for course_tr in course_list.find_all(name="tr"):
        #fix
        
        if course_tr.find_all(name="td", attrs={'class': 'CourseTitle'}):
            course_title_tr = course_tr.find_all(name="td", attrs={'class': 'CourseTitle'})[0]
            for a in course_title_tr.find_all(name="a"):
                a.decompose()
            course_title = format_entry(course_title_tr).replace("()", "")
            print(course_title)

        course_data = [format_entry(td) for td in course_tr.find_all(name="td")]
        if len(course_data) == 17:
            course = get_course(course_data, course_title)

            classes[course['code']] = course

    return classes
    
    # csv_file = "test.csv"

    # try:
    #     with open(csv_file, 'w') as csvfile:
    #         writer = csv.DictWriter(csvfile, fieldnames=columns)
    #         writer.writeheader()
    #         for data in classes:
    #             writer.writerow(data)
    # except IOError:
    #     print("I/O error")

def format_entry(entry):
    for br in entry.find_all("br"):
        br.replace_with("/")

    return entry.get_text().strip()

def get_course(course_data, course_title):
    code = course_data[0]
    _type = course_data[1]
    section = course_data[2]
    units = course_data[3]
    instructor = course_data[4]
    time = course_data[5]
    place = course_data[6]
    final = course_data[7]
    max_students = course_data[8]
    enrolled = course_data[9]
    waitlist = course_data[10]
    requests = course_data[11]
    nor = course_data[12]
    restrictions = course_data[13]
    status = course_data[15]


    course = {
        'code': code,
        'course': course_title, 
        'type': _type,
        'section': section,
        'units': units,
        'instructor': instructor,
        'time': time,
        'place': place,
        'final': final,
        'max': max_students,
        'enrolled': enrolled,
        'waitlist': waitlist,
        'requests': requests,
        'nor': nor,
        'restrictions': restrictions,
        'status': status
    }


    return course
    

def get_url(params):
    query_params = [(key, value) for key, value in params.items()]

    return URL + "?" + urllib.parse.urlencode(query_params)


def get_html(url):
    with urllib.request.urlopen(url) as response:
        html = response.read().decode()

        return html

if __name__ == "__main__":
    print(get_classes({"YearTerm": "2020-92", "Dept": "EECS", "ShowFinals": "1"}))
    #get_breadths()



