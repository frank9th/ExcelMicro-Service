from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import xlrd
from django.shortcuts import  get_object_or_404
from django.core.files.storage import FileSystemStorage 
from .forms import FileForm 
from .models import File
import pandas as pd 
import json
# Create your views here.
"""
import requests
from rest_framework import viewsets 
from .serializers import FileSerializer
from rest_framework.decorators import action


class FileView(viewsets.ModelViewSet): 
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

"""

def index(request):
    name = " index"
    return render(request, 'index.html', {'name':name})


def upload_file(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['excel']

        #this line of code saves the uploaded file to the media file 
        fs = FileSystemStorage()
        # assigning name and context is to get the uploaded 
        # file name and url and display it to the user
        name = fs.save(uploaded_file.name, uploaded_file, max_length=None)
        context['url'] = fs.url(name)
       
        #print(uploaded_file.name)
        #print(uploaded_file.size)
    return render(request, 'upload_file.html', context)

def file_list(request):
	files = File.objects.all()
	return render(request, 'file_list.html', {'files' : files})


def file_upload(request):
	if request.method == 'POST':
		form = FileForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			# this is where we can now do somthing with the form 
			return redirect('file_list')
	else:
		form = FileForm()
		return render(request, 'file_upload.html', {'form' : form})


# ------- TO READ FROM A FILE PATH PASSED IN FROM THE BE-----

def budget(request):

    try:
       
        # reading the excel file
        df = pd.read_excel('./media/APRIL.xlsx', usecols = "B:G",encoding='utf-8' )
        # Dropping the unneccessary columns
        data = df.dropna(axis = 0, how= "any")
        data.columns = data.iloc[0]
        data2 = data.iloc[1:,].reindex()    
        # data3 = df.book.nrows
        nrows = 10
     
        # here is month, the variable in which the month is stored in
        #month = data2.columns[2]
     
        data2.columns = data2.columns.map(lambda x: x.replace('\n', ''))
        data2.columns = ["sector", "budget", "allocation","total_allocation","balance","percentage"]
        # we dont need percentage... dropping it
        data2.drop(["percentage"], axis = 1, inplace = True)
     
     
        final_data = data2.to_dict(orient = "records")
        return render(request, 'budget.html', {'final_data': final_data})
       
        print(final_data)
    except KeyError:
        print("failed")

    
def excel_upload(request):
    name = " index"
    return render(request, 'index.html', {'name':name})

# to acces the upload file and read excel
"""
def budget(request):
    try:
    
        file = File.objects.all()
       
        # reading the excel file
        df = pd.read_excel('(file)', usecols = "B:G",encoding='utf-8' )
        # Dropping the unneccessary columns
        data = df.dropna(axis = 0, how= "any")
        data.columns = data.iloc[0]
        data2 = data.iloc[1:,].reindex()    
        # data3 = df.book.nrows
        nrows = 10
     
        # here is month, the variable in which the month is stored in
        #month = data2.columns[2]
     
        data2.columns = data2.columns.map(lambda x: x.replace('\n', ''))
        data2.columns = ["sector", "budget", "allocation","total_allocation","balance","percentage"]
        # we dont need percentage... dropping it
        data2.drop(["percentage"], axis = 1, inplace = True)
     
     
        final_data = data2.to_dict(orient = "records")
        return render(request, 'budget.html', {'final_data': final_data})

      
       
        print(final_data)
    except KeyError:
        print("failed")

"""
'''
'''
'''
# ---- To read only FG excel whit specific colums ---

def excel_files(request,pk):
    #get an instance of the file here... so i can access any of it's fields...
    file = get_object_or_404(File,pk=pk)
    
    #where name_of_file is the name of the field on ur model
    #file_path = file.name
    file_path = file.xlsx 

    try:
       
        # reading the excel file
        df = pd.read_excel(file_path, usecols = "B:G",encoding='utf-8' )
        # Dropping the unneccessary columns
        data = df.dropna(axis = 0, how= "any")
        data.columns = data.iloc[0]
        data2 = data.iloc[1:,].reindex()    
        # data3 = df.book.nrows
        nrows = 10
     
        # here is month, the variable in which the month is stored in
        #month = data2.columns[2]
     
        data2.columns = data2.columns.map(lambda x: x.replace('\n', ''))
        data2.columns = ["sector", "budget", "allocation","total_allocation","balance","percentage"]
        # we dont need percentage... dropping it
        data2.drop(["percentage"], axis = 1, inplace = True)
     
     
        final_data = data2.to_dict(orient = "records")
        return render(request, 'excel_files.html', {'final_data': final_data})
       
        print(final_data)
    except KeyError:
        print("failed")
'''


def excel_files(request,pk):
    #get an instance of the file here... so i can access any of it's fields...
    file = get_object_or_404(File,pk=pk)
    
    #where name_of_file is the name of the field on ur model
    #file_path = file.name
    file_path = file.xlsx 

    try:
       
        # reading the excel file
        excel_data_df = pd.read_excel(file_path, usecols = "B:G",encoding='utf-8' )


        final_data = excel_data_df.to_json(orient = "table", index=None)
        #final_data = data2.to_dict(orient = "records")
        return render(request, 'excel_files.html', {'final_data': final_data})

    except KeyError:
        print("failed")
