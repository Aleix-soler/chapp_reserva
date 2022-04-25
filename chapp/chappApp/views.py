from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf.urls.static import static
from django.conf import settings
import json
import xlwt

from .models import *
from .forms import *

class Date: 
    def __init__(self, d:int, m:int, y:int):
        self.d = int(d)
        self.m = int(m)
        self.y = int(y)

def book_list(request):
    
    books = Book.objects.filter().order_by('-date_entry')
    books_count = books.count()
    print(static(settings.STATIC_URL))
    context = {'books': books, 'books_count': books_count}
    return render(request, './book/list.html', context)


def firstForm(request):
    form = FirstForm(request.POST or None)
    context = {'form': form}
    request.session['firstForm'] = '0'
    if request.POST:
        print(request.POST)
        if form.is_valid():
            print("IS VALID", form.cleaned_data)
            request.session['firstForm'] = json.dumps(form.cleaned_data, sort_keys=True, default=str)
            print("REQUEST SESSION->", request.session['firstForm'])
            return redirect('/book/form/2')
        else:
            print("ITS NOT VALID")

    return render(request, './book/form/firstForm.html', context)

def secondForm(request):
    #Check session to avoid mistakes
    if request.session['firstForm'] == '0':
        return redirect('/book/form/1')
    
    form = SecondForm(request.POST or None)
    if request.POST:
        print("POST REQUEST",request.POST)
        firstFormData = json.loads(request.session['firstForm'])
        if form.is_valid():
            print("FORM IS VALID",form.cleaned_data)
            #request.session['firstForm'] = '0'
            #request.session['book'] = json.dumps(finalBook, sort_keys=True, indent=4, default=vars(Book))
            request.session['secondForm'] = json.dumps(form.cleaned_data, sort_keys=True, default=str)
            return redirect('/book/form/3')
        else: 
            print("FORM NOT VALID")
            print(form.errors.as_data())


    firstFormData = json.loads(request.session['firstForm'])
    
    available = [['SINGLE', 10], ['DOUBLE', 5], ['TRIPLE', 4], ['QUADRUPLE', 6]]
    books_query = Book.objects.raw("SELECT localizador, type_room, count(*) as quantity from chappapp_book WHERE ((date_entry>=%s and date_entry<%s) or (date_exit > %s and date_exit <= %s) or (date_entry < %s and date_exit > %s)) group by type_room",
        [firstFormData['date_entry'], firstFormData['date_exit'], firstFormData['date_entry'], firstFormData['date_exit'], firstFormData['date_entry'], firstFormData['date_exit']])

    #Checks Availability
    for p in books_query:
        for i in available:
            if i[0] == p.type_room:
                i[1]-=p.quantity
                
    context = {'rooms_available': available, 'form': form, 'guests': firstFormData['number_guests'], 'entry_data': firstFormData['date_entry'], 'exit_data': firstFormData['date_exit']}
    
    return render(request, './book/form/secondForm.html', context)

def thirdForm(request):
    form = ThirdForm(request.POST or None)
    if request.POST:
        
        firstForm = json.loads(request.session['firstForm'])
        secondForm = json.loads(request.session['secondForm'])
        if form.is_valid():
            print("FORM IS VALID->", form.cleaned_data)
            newBook = Book(date_entry=firstForm['date_entry'], date_exit=firstForm['date_exit'], type_room=secondForm['type_room'], price=secondForm['price'], name=form.cleaned_data['name'], email=form.cleaned_data['email'], phone=form.cleaned_data['phone'])
            newBook.save()
            return redirect('/')
        else:
            print("FORM NOT VALID->", form.errors.as_data())
            
    context = {'form': form}
    print("FIRST FORM->", request.session['firstForm'])
    print("SECOND FORM->",  request.session['secondForm'])
    return render(request, './book/form/thirdForm.html', context)

def deleteBook(request, id):
    print("REQUEST->", request)
    print("ID->", id)
    Book.objects.filter(localizador=id).delete()
    return redirect('/')

def export_books_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reservation.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Reservations')


    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    

    columns = ['localizador', 'date_entry', 'date_exit', 'type_room', 'price', 'name', 'email', 'phone']

    ws.col(0).width  = 256*50
    ws.col(1).width  = 256*15
    ws.col(2).width  = 256*15
    ws.col(3).width  = 256*20
    ws.col(4).width  = 256*20
    ws.col(5).width  = 256*50
    ws.col(6).width  = 256*100
    ws.col(7).width  = 256*20  

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    date_style = xlwt.easyxf(num_format_str='YYYY-MM-DD')
    
    rows = Book.objects.all().values_list('localizador', 'date_entry', 'date_exit', 'type_room', 'price', 'name', 'email', 'phone')
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
    
            if col_num==0:
                ws.write(row_num, col_num, str(row[col_num]), font_style)
            elif col_num==1 or col_num==2:
                ws.write(row_num, col_num, row[col_num], date_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

def view_book(request, id):
    book = Book.objects.filter(localizador=id)
    context={'id':id, 'book': book}
    
    return render(request, './book/view_book.html', context)