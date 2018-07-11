from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required

from .services.MaterialCreator import MaterialCreator

import requests
import json
import os

from common.BackendMessage import BackendMessage
from common.MachineConfig import MachineConfigurator


def cleanup(filename):
    try:
        os.remove('.' + filename)
        print("removed file: " + filename)
    except Exception as error:
        print(error)


@login_required(login_url='/auth/login')
def simple_upload(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:

            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            # ... do here the magic
            creator = MaterialCreator()
            result = creator.createMaterialfromCSV('.' + uploaded_file_url)
            result_json = []

            for material in result:
                result_json.append(json.dumps(material))

            backend_host = MachineConfigurator().getBackend()

            r = requests.post(backend_host + '/auth/materials/', json=result)

            backend_message = BackendMessage(json.loads(r.text))
            print(backend_message)

            cleanup(uploaded_file_url)

            return render(request, 'materials/simple_upload.html', {
                'uploaded_materials': result_json})

    except MultiValueDictKeyError as exception:
            print("No file selected")
            return render(request, 'materials/simple_upload.html', {'error_message': 'No file selected'})

    except ValueError as exception:
        print("There is a problem with the backend return value")
        return render(request, 'materials/simple_upload.html', {'error_message': 'Backend problem'})

    return render(request, 'materials/simple_upload.html')

