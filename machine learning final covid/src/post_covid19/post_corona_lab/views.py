from django.shortcuts import render
from django.http import HttpResponse

def index(request):

    total_cases = {'China' : 0.2, 'Asia' : 2.1, 'Europe' : 3.4, 'America' : 2.0, 'Africa' : 0.1, 'Oceania' : 0.0}

    daily_cases = {'China' : '1.2', 'Asia' : '7.2', 'Europe' : '20.3', 'America' : '17.6', 'Africa' : '0.7', 'Oceania' : '0.2'}

    keyword = ['disease', 'virus', 'pandemic', 'china', 'epidemic', 'italy']


    return render(request,'index.html',{'total_cases'  : total_cases, 'daily_cases' : daily_cases, 'keyword': keyword})

def popup(request):
    continent = request.GET['Continent']
    print(continent)

    if ( continent == 'China' ) :
        bar = 'bar-chart-horizontal-China'
        line = 'morris-line-chart-China'
        chartjs = "/static/dist/js/pages/chartjs/chartjs.init.china.js"
        morris = "/static/dist/js/pages/morris/morris-data.china.js"
        image = ''
        return render(request,'popup.html', {'bar':bar, 'line':line, 'image':image, 'chartjs' : chartjs, 'morris' : morris})

    elif ( continent == 'Asia' ) :
        bar = 'bar-chart-horizontal-Asia'
        line = 'morris-line-chart-Asia'
        chartjs = "/static/dist/js/pages/chartjs/chartjs.init.asia.js"
        morris = "/static/dist/js/pages/morris/morris-data.asia.js"
        image = ''
        return render(request,'popup.html', {'bar':bar, 'line':line, 'image':image, 'chartjs' : chartjs, 'morris' : morris})
    
    elif ( continent == 'Europe' ) :
        bar = 'bar-chart-horizontal-Europe'
        line = 'morris-line-chart-Europe'
        chartjs = "/static/dist/js/pages/chartjs/chartjs.init.europe.js"
        morris = "/static/dist/js/pages/morris/morris-data.europe.js"
        image = ''
        return render(request,'popup.html', {'bar':bar, 'line':line, 'image':image, 'chartjs' : chartjs, 'morris' : morris})
    
    elif ( continent == 'America' ) :
        bar = 'bar-chart-horizontal-America'
        line = 'morris-line-chart-America'
        chartjs = "/static/dist/js/pages/chartjs/chartjs.init.america.js"
        morris = "/static/dist/js/pages/morris/morris-data.america.js"
        image = ''
        return render(request,'popup.html', {'bar':bar, 'line':line, 'image':image, 'chartjs' : chartjs, 'morris' : morris})
    
    elif ( continent == 'Africa' ) :
        bar = 'bar-chart-horizontal-Africa'
        line = 'morris-line-chart-Africa'
        chartjs = "/static/dist/js/pages/chartjs/chartjs.init.africa.js"
        morris = "/static/dist/js/pages/morris/morris-data.africa.js"
        image = ''
        return render(request,'popup.html', {'bar':bar, 'line':line, 'image':image, 'chartjs' : chartjs, 'morris' : morris})
    
    elif ( continent == 'Oceania' ) :
        bar = 'bar-chart-horizontal-Oceania'
        line = 'morris-line-chart-Oceania'
        chartjs = "/static/dist/js/pages/chartjs/chartjs.init.oceania.js"
        morris = "/static/dist/js/pages/morris/morris-data.oceania.js"
        image = ''
        return render(request,'popup.html', {'bar':bar, 'line':line, 'image':image, 'chartjs' : chartjs, 'morris' : morris})