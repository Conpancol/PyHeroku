from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory

from requests.exceptions import ConnectionError

from .services.QuoteCreator import QuoteCreator
from .services.ExtQuotedMaterialCreator import ExtQuotedMaterialCreator
from .forms import QuotesForm, QuotedMaterialsForm, SelectorForm, QuotesFormOnlyinfo, QuotedMaterialForm

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
                edt = form.cleaned_data['edt']

                quote.setQuoteInformation(internal_code, external_code, provider_code, provider_id, provider_name,
                                          contact_name, received_date, sent_date, user, edt)
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

                backend_result = []

                if backend_message.errorInd:
                    display_message = {}
                    display_message['internalCode'] = internal_code
                    display_message['externalCode'] = external_code
                    display_message['status'] = backend_message.getValue()
                    backend_result.append(display_message)
                else:
                    backend_result = json.loads(backend_message.getValue())

                return render(request, 'quotes/quote_upload.html', {'menu_text': menu_texts.getComponent(),
                                                                    'view_texts': view_texts.getComponent(),
                                                                    'upload_result': backend_result})

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


@login_required(login_url='/auth/login')
def quotes_manager(request):
    menu_texts = FrontendTexts('menu')
    instructions = Instructions('quotes', 'manage')
    print("quotes manager")
    try:
        if request.method == 'POST':
            selector_form = SelectorForm(request.POST)

            if selector_form.is_valid():
                code = selector_form.cleaned_data['code']
                action = selector_form.cleaned_data['action']

                if action == '1':
                    return redirect('edit/' + code)

        else:
            selector_form = SelectorForm()
            return render(request, 'quotes/quote_selector.html', {'menu_text': menu_texts.getComponent(),
                                                                  'view_texts': view_texts.getComponent(),
                                                                  'selector_form': selector_form,
                                                                  'instructions_title': instructions.getTitle(),
                                                                  'instructions_steps': instructions.getSteps()})

    except ValueError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'quotes/quote_selector.html', {'menu_text': menu_texts.getComponent(),
                                                              'view_texts': view_texts.getComponent(),
                                                              'error_message': 'Backend problem',
                                                              'instructions_title': instructions.getTitle(),
                                                              'instructions_steps': instructions.getSteps()
                                                              })

    except ConnectionError as exception:
        print("Backend connection problem")
        print(exception)
        return render(request, 'quotes/quote_selector.html', {'menu_text': menu_texts.getComponent(),
                                                              'view_texts': view_texts.getComponent(),
                                                              'error_message': 'Backend connection problem',
                                                              'instructions_title': instructions.getTitle(),
                                                              'instructions_steps': instructions.getSteps()
                                                              })

    except Exception as exception:
        print(exception)
        return render(request, 'quotes/quote_selector.html', {'menu_text': menu_texts.getComponent(),
                                                              'view_texts': view_texts.getComponent(),
                                                              'error_message': 'System error',
                                                              'instructions_title': instructions.getTitle(),
                                                              'instructions_steps': instructions.getSteps()
                                                              })


@login_required(login_url='/auth/login')
def quotes_material_editor(request, code):
    menu_texts = FrontendTexts('menu')
    instructions = Instructions('quotes', 'edit')
    try:

        backend_host = MachineConfigurator().getBackend()

        r = requests.post(backend_host + '/auth/quotes/' + code)

        backend_message = BackendMessage(json.loads(r.text))

        backend_result = json.loads(backend_message.getValue())

        material_data = backend_result['materialList']

        quote_form = QuotesFormOnlyinfo(initial=backend_result)

        MaterialFormSet = formset_factory(QuotedMaterialForm, extra=0)
        materials_formset = MaterialFormSet(initial=material_data)

        if request.method == 'POST':

            quote_form = QuotesFormOnlyinfo(request.POST)

            materials_formset = MaterialFormSet(request.POST)

            if quote_form.is_valid() and materials_formset.is_valid():
                # ... update current material with the data provided
                # ... send data to backend

                creator = QuoteCreator()
                result = creator.editQuotewithMaterials(quote_form, materials_formset, material_data)

                print(result)
                result_json = []

                for quote in result:
                    result_json.append(json.dumps(quote))

                r = requests.put(backend_host + '/auth/quotes/' + code, json=result)

                backend_message = BackendMessage(json.loads(r.text))

                backend_result = json.loads(backend_message.getValue())

                return render(request, 'quotes/quote_editor.html', {'menu_text': menu_texts.getComponent(),
                                                                    'view_texts': view_texts.getComponent(),
                                                                    'updated_materials': backend_result})
            else:
                print("Invalid form")

        return render(request, 'quotes/quote_editor.html', {'menu_text': menu_texts.getComponent(),
                                                            'view_texts': view_texts.getComponent(),
                                                            'quote_form': quote_form,
                                                            'materials_formset': materials_formset,
                                                            'instructions_title': instructions.getTitle(),
                                                            'instructions_steps': instructions.getSteps()})

    except ValueError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'quotes/quote_editor.html', {'menu_text': menu_texts.getComponent(),
                                                            'view_texts': view_texts.getComponent(),
                                                            'error_message': 'No such RFQ exists in the DB: ' + code,
                                                            'instructions_title': instructions.getTitle(),
                                                            'instructions_steps': instructions.getSteps()})

    except ConnectionError as exception:
        print("Backend connection problem")
        print(exception)
        return render(request, 'quotes/quote_editor.html', {'menu_text': menu_texts.getComponent(),
                                                            'view_texts': view_texts.getComponent(),
                                                            'error_message': 'Backend connection problem',
                                                            'instructions_title': instructions.getTitle(),
                                                            'instructions_steps': instructions.getSteps()})

    except Exception as exception:
        print(exception)
        return render(request, 'quotes/quote_editor.html', {'menu_text': menu_texts.getComponent(),
                                                            'view_texts': view_texts.getComponent(),
                                                            'error_message': 'System error',
                                                            'instructions_title': instructions.getTitle(),
                                                            'instructions_steps': instructions.getSteps()})

