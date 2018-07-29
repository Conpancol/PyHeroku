from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

from .services.RFQCreator import RFQCreator
from .forms import RFQForm

import requests
import json
import os

from common.BackendMessage import BackendMessage
from common.MachineConfig import MachineConfigurator
from common.Instructions import Instructions


def cleanup(filename):
    try:
        os.remove('.' + filename)
        print("removed file: " + filename)
    except Exception as error:
        print(error)


@login_required(login_url='/auth/login')
def rfq_upload(request):
    try:
        instructions = Instructions('rfqs', 'upload')
        if request.method == 'POST':
            form = RFQForm(request.POST, request.FILES)
            if form.is_valid():

                rfq = RFQCreator()

                internal_code = form.cleaned_data['internalCode']
                external_code = form.cleaned_data['externalCode']
                sender = form.cleaned_data['sender']
                company = form.cleaned_data['company']
                received_date = form.cleaned_data['receivedDate']
                note = form.cleaned_data['note']

                rfq.setRFQInformation(internal_code, external_code, sender, company, received_date)
                rfq.addRFQNote(note)

                myfile = request.FILES['document']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)

                result = rfq.createRFQfromCSV('.' + uploaded_file_url)

                # ... print(json.dumps(result))

                backend_host = MachineConfigurator().getBackend()
                r = requests.post(backend_host + '/auth/rfqs/', json=result)

                backend_message = BackendMessage(json.loads(r.text))

                cleanup(uploaded_file_url)

                return render(request, 'rfqs/rfq_upload.html', {'form': form,
                                                                'error_message': backend_message.getValue()})
        else:
            form = RFQForm()
        return render(request, 'rfqs/rfq_upload.html', {'form': form,
                                                        'instructions_title': instructions.getTitle(),
                                                        'instructions_steps': instructions.getSteps()
                                                        })

    except Exception as exception:
        cleanup(uploaded_file_url)
        print(exception)
        return render(request, 'rfqs/rfq_upload.html', {'form': form,
                                                        'error_message': "Frontend Error",
                                                        'instructions_title': instructions.getTitle(),
                                                        'instructions_steps': instructions.getSteps()
                                                        })

    except ValueError as exception:
        cleanup(uploaded_file_url)
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'rfqs/rfq_upload.html', {'form': form,
                                                        'error_message': 'Backend problem',
                                                        'instructions_title': instructions.getTitle(),
                                                        'instructions_steps': instructions.getSteps()
                                                        })

