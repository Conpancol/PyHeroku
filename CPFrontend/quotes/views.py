from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from requests.exceptions import ConnectionError

from .services.QuoteCreator import QuoteCreator
from .services.ExtQuotedMaterialCreator import ExtQuotedMaterialCreator
from .forms import QuotesForm, QuotedMaterialsForm

import requests
import json
import os

from common.BackendMessage import BackendMessage
from common.MachineConfig import MachineConfigurator
from common.Instructions import Instructions
from common.FrontendTexts import FrontendTexts


view_texts = FrontendTexts('quotes')


def cleanup(filename):
    try:
        os.remove('.' + filename)
        print("removed file: " + filename)
    except Exception as error:
        print(error)


@login_required(login_url='/auth/login')
def quotes_upload(request):
    menu_texts = FrontendTexts('menu')
    instructions = Instructions('quotes', 'upload')
    uploaded_file_url = ''
    try:
        form = QuotesForm()
        if request.method == 'POST':
            form = QuotesForm(request.POST, request.FILES)
            if form.is_valid():

                quote = QuoteCreator()

                internal_code = form.cleaned_data['internalCode']
                external_code = form.cleaned_data['externalCode']
                provider_code = form.cleaned_data['providerCode']
                received_date = form.cleaned_data['receivedDate']
                sent_date = form.cleaned_data['sentDate']
                user = form.cleaned_data['user']
                provider_id = form.cleaned_data['providerId']
                provider_name = form.cleaned_data['providerName']
                contact_name = form.cleaned_data['contactName']
                incoterms = form.cleaned_data['incoterms']
                note = form.cleaned_data['note']

                quote.setQuoteInformation(internal_code, external_code, provider_code, provider_id, provider_name,
                                          contact_name, received_date, sent_date, user)
                quote.setQuoteIncoterms(incoterms)
                quote.setQuoteNote(note)

                myfile = request.FILES['document']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)

                result = quote.createQuotefromCSV('.' + uploaded_file_url)

                # ...  print(json.dumps(result))
                backend_host = MachineConfigurator().getBackend()

                r = requests.post(backend_host + '/auth/quotes/', json=result)

                backend_message = BackendMessage(json.loads(r.text))

                cleanup(uploaded_file_url)

                return render(request, 'quotes/quote_upload.html', {'menu_text': menu_texts.getComponent(),
                                                                    'view_texts': view_texts.getComponent(),
                                                                    'form': form,
                                                                    'error_message': backend_message.getValue()})

        return render(request, 'quotes/quote_upload.html', {'menu_text': menu_texts.getComponent(),
                                                            'view_texts': view_texts.getComponent(),
                                                            'form': form,
                                                            'instructions_title': instructions.getTitle(),
                                                            'instructions_steps': instructions.getSteps()})

    except ValueError as exception:
        cleanup(uploaded_file_url)
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'quotes/quote_upload.html', {'menu_text': menu_texts.getComponent(),
                                                            'view_texts': view_texts.getComponent(),
                                                            'error_message': 'Backend problem',
                                                            'instructions_title': instructions.getTitle(),
                                                            'instructions_steps': instructions.getSteps()
                                                            })

    except ConnectionError as exception:
        cleanup(uploaded_file_url)
        print("Backend connection problem")
        print(exception)
        return render(request, 'quotes/quote_upload.html', {'menu_text': menu_texts.getComponent(),
                                                            'view_texts': view_texts.getComponent(),
                                                            'error_message': 'Backend connection problem',
                                                            'instructions_title': instructions.getTitle(),
                                                            'instructions_steps': instructions.getSteps()
                                                            })

    except Exception as exception:
        cleanup(uploaded_file_url)
        print(exception)
        return render(request, 'quotes/quote_upload.html', {'menu_text': menu_texts.getComponent(),
                                                            'view_texts': view_texts.getComponent(),
                                                            'error_message': 'General problem',
                                                            'instructions_title': instructions.getTitle(),
                                                            'instructions_steps': instructions.getSteps()
                                                            })


@login_required(login_url='/auth/login')
def quoted_materials_upload(request):
    menu_texts = FrontendTexts('menu')
    instructions = Instructions('quotes', 'materials_upload')
    uploaded_file_url = ''
    try:
        if request.method == 'POST':
            form = QuotedMaterialsForm(request.POST, request.FILES)
            if form.is_valid():

                data = ExtQuotedMaterialCreator()

                providerId = form.cleaned_data['providerId']
                providerName = form.cleaned_data['providerName']
                revision = form.cleaned_data['revision']

                data.setExtendedInformation(providerId, providerName, revision)

                my_file = request.FILES['document']
                fs = FileSystemStorage()
                filename = fs.save(my_file.name, my_file)
                uploaded_file_url = fs.url(filename)

                result = data.createExtQuotedMaterialsfromCSV('.' + uploaded_file_url)

                # print(json.dumps(result))

                backend_host = MachineConfigurator().getBackend()
                r = requests.post(backend_host + '/auth/quotes/materials', json=result)

                backend_message = BackendMessage(json.loads(r.text))

                cleanup(uploaded_file_url)

                backend_result = []

                if backend_message.errorInd:
                    display_message = {}
                    display_message['itemcode'] = "-"
                    display_message['revision'] = "-"
                    display_message['status'] = "-"
                    backend_result.append(display_message)
                else:
                    backend_result = json.loads(backend_message.getValue())

                return render(request, 'quotes/materials_upload.html', {'menu_text': menu_texts.getComponent(),
                                                                        'view_texts': view_texts.getComponent(),
                                                                        'upload_result': backend_result})
        else:
            form = QuotedMaterialsForm()

        return render(request, 'quotes/materials_upload.html', {'menu_text': menu_texts.getComponent(),
                                                                'view_texts': view_texts.getComponent(),
                                                                'form': form,
                                                                'instructions_title': instructions.getTitle(),
                                                                'instructions_steps': instructions.getSteps()
                                                                })

    except ValueError as exception:
        cleanup(uploaded_file_url)
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'quotes/materials_upload.html', {'menu_text': menu_texts.getComponent(),
                                                                'view_texts': view_texts.getComponent(),
                                                                'error_message': 'Backend problem',
                                                                'instructions_title': instructions.getTitle(),
                                                                'instructions_steps': instructions.getSteps()
                                                                })

    except ConnectionError as exception:
        cleanup(uploaded_file_url)
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'quotes/materials_upload.html', {'menu_text': menu_texts.getComponent(),
                                                                'view_texts': view_texts.getComponent(),
                                                                'error_message': 'Backend connection problem',
                                                                'instructions_title': instructions.getTitle(),
                                                                'instructions_steps': instructions.getSteps()
                                                                })

    except Exception as exception:
        cleanup(uploaded_file_url)
        print(exception)
        return render(request, 'quotes/materials_upload.html', {'menu_text': menu_texts.getComponent(),
                                                                'view_texts': view_texts.getComponent(),
                                                                'error_message': "Frontend Error",
                                                                'instructions_title': instructions.getTitle(),
                                                                'instructions_steps': instructions.getSteps()
                                                                })
