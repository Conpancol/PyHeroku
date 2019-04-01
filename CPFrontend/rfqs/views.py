from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import Http404
from django.forms import formset_factory

from requests.exceptions import ConnectionError

from .services.RFQCreator import RFQCreator
from .forms import RFQForm
from .forms import ExtMaterialForm
from .forms import RFQFormOnlyinfo
from .forms import RFQInternalCode
from .forms import SelectorForm

# from .choices import ACTION_CHOICES

import requests
import json
import os

from common.BackendMessage import BackendMessage
from common.MachineConfig import MachineConfigurator
from common.Instructions import Instructions
from common.FrontendTexts import FrontendTexts


view_texts = FrontendTexts('rfqs')


def cleanup(filename):
    try:
        os.remove('.' + filename)
        print("removed file: " + filename)
    except Exception as error:
        print(error)


@login_required(login_url='/auth/login')
def rfq_upload(request):
    menu_texts = FrontendTexts('menu')
    instructions = Instructions('rfqs', 'upload')
    uploaded_file_url = ''
    try:

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

                return render(request, 'rfqs/rfq_upload.html', {'menu_text': menu_texts.getComponent(),
                                                                'view_texts': view_texts.getComponent(),
                                                                'form': form,
                                                                'error_message': backend_message.getValue()})
        else:
            form = RFQForm()
        return render(request, 'rfqs/rfq_upload.html', {'menu_text': menu_texts.getComponent(),
                                                        'view_texts': view_texts.getComponent(),
                                                        'form': form,
                                                        'instructions_title': instructions.getTitle(),
                                                        'instructions_steps': instructions.getSteps()
                                                        })

    except ValueError as exception:
        cleanup(uploaded_file_url)
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'rfqs/rfq_upload.html', {'menu_text': menu_texts.getComponent(),
                                                        'view_texts': view_texts.getComponent(),
                                                        'form': form,
                                                        'error_message': 'Backend problem',
                                                        'instructions_title': instructions.getTitle(),
                                                        'instructions_steps': instructions.getSteps()
                                                        })

    except ConnectionError as exception:
        cleanup(uploaded_file_url)
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'rfqs/rfq_upload.html', {'menu_text': menu_texts.getComponent(),
                                                        'view_texts': view_texts.getComponent(),
                                                        'form': form,
                                                        'error_message': 'Backend connection problem',
                                                        'instructions_title': instructions.getTitle(),
                                                        'instructions_steps': instructions.getSteps()
                                                        })

    except Exception as exception:
        cleanup(uploaded_file_url)
        print(exception)
        return render(request, 'rfqs/rfq_upload.html', {'menu_text': menu_texts.getComponent(),
                                                        'view_texts': view_texts.getComponent(),
                                                        'form': form,
                                                        'error_message': "Frontend Error",
                                                        'instructions_title': instructions.getTitle(),
                                                        'instructions_steps': instructions.getSteps()
                                                        })


@login_required(login_url='/auth/login')
def rfq_export(request):
    menu_texts = FrontendTexts('menu')
    instructions = Instructions('rfqs', 'export')
    output_file = ''
    try:
        if request.method == 'POST':
            form = RFQInternalCode(request.POST)
            if form.is_valid():

                internal_code = form.cleaned_data['internalcode']

                incoterms = form.cleaned_data['incoterms']

                port = form.cleaned_data['port']

                backend_host = MachineConfigurator().getBackend()

                r = requests.get(backend_host + '/auth/rfqs/' + internal_code)

                backend_message = BackendMessage(json.loads(r.text))

                if not backend_message.getErrorInd():

                    rfq = json.loads(backend_message.getValue())
                    rfq_service = RFQCreator()
                    output_file = rfq_service.exportRFQtoCSV(rfq, incoterms, port)

                    if os.path.exists(output_file):
                        with open(output_file, 'rb') as fh:
                            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                        cleanup('/' + output_file)
                        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(output_file)
                        return response
                    raise Http404

                else:
                    print("There is a backend error message")
                    return render(request, 'rfqs/rfq_export.html', {'menu_text': menu_texts.getComponent(),
                                                                    'view_texts': view_texts.getComponent(),
                                                                    'rfqform': form,
                                                                    'error_message': backend_message.getValue(),
                                                                    'instructions_title': instructions.getTitle(),
                                                                    'instructions_steps': instructions.getSteps()
                                                                    })

        else:
            form = RFQInternalCode()

        return render(request, 'rfqs/rfq_export.html', {'menu_text': menu_texts.getComponent(),
                                                        'view_texts': view_texts.getComponent(),
                                                        'rfqform': form,
                                                        'instructions_title': instructions.getTitle(),
                                                        'instructions_steps': instructions.getSteps()
                                                        })

    except ValueError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'rfqs/rfq_export.html', {'menu_text': menu_texts.getComponent(),
                                                        'view_texts': view_texts.getComponent(),
                                                        'rfqform': form,
                                                        'error_message': 'Backend problem',
                                                        'instructions_title': instructions.getTitle(),
                                                        'instructions_steps': instructions.getSteps()
                                                        })

    except ConnectionError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'rfqs/rfq_upload.html', {'menu_text': menu_texts.getComponent(),
                                                        'view_texts': view_texts.getComponent(),
                                                        'form': form,
                                                        'error_message': 'Backend connection problem',
                                                        'instructions_title': instructions.getTitle(),
                                                        'instructions_steps': instructions.getSteps()
                                                        })

    except Exception as exception:
        cleanup(output_file)
        print(exception)
        return render(request, 'rfqs/rfq_upload.html', {'menu_text': menu_texts.getComponent(),
                                                        'view_texts': view_texts.getComponent(),
                                                        'form': form,
                                                        'error_message': "Frontend Error",
                                                        'instructions_title': instructions.getTitle(),
                                                        'instructions_steps': instructions.getSteps()
                                                        })


@login_required(login_url='/auth/login')
def rfq_qfinder(request):
    menu_texts = FrontendTexts('menu')
    instructions = Instructions('rfqs', 'qfinder')
    uploaded_file_url = ''
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            rfq = RFQCreator()
            result = rfq.findQuotesFromCSV('.' + uploaded_file_url)

            # ... print(json.dumps(result))

            backend_host = MachineConfigurator().getBackend()
            r = requests.post(backend_host + '/auth/rfqs/quotes', json=result)

            backend_message = BackendMessage(json.loads(r.text))

            if not backend_message.getErrorInd():

                quoted_materials = json.loads(backend_message.getValue())
                cleanup(uploaded_file_url)

                return render(request, 'rfqs/rfq_qfinder.html', {'menu_text': menu_texts.getComponent(),
                                                                 'view_texts': view_texts.getComponent(),
                                                                 'quoted_materials': quoted_materials,
                                                                 'instructions_title': instructions.getTitle(),
                                                                 'instructions_steps': instructions.getSteps()
                                                                 })
            else:
                print(backend_message.getValue())
                cleanup(uploaded_file_url)
                return render(request, 'rfqs/rfq_qfinder.html', {'menu_text': menu_texts.getComponent(),
                                                                 'view_texts': view_texts.getComponent(),
                                                                 'error_message': backend_message.getValue(),
                                                                 'instructions_title': instructions.getTitle(),
                                                                 'instructions_steps': instructions.getSteps()
                                                                 })

        return render(request, 'rfqs/rfq_qfinder.html', {'menu_text': menu_texts.getComponent(),
                                                         'view_texts': view_texts.getComponent(),
                                                         'instructions_title': instructions.getTitle(),
                                                         'instructions_steps': instructions.getSteps()
                                                         })

    except ConnectionError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'rfqs/rfq_qfinder.html', {'menu_text': menu_texts.getComponent(),
                                                         'view_texts': view_texts.getComponent(),
                                                         'error_message': 'Backend connection problem',
                                                         'instructions_title': instructions.getTitle(),
                                                         'instructions_steps': instructions.getSteps()
                                                         })

    except Exception as exception:
        cleanup(uploaded_file_url)
        print(exception)
        return render(request, 'rfqs/rfq_qfinder.html', {'menu_text': menu_texts.getComponent(),
                                                         'view_texts': view_texts.getComponent(),
                                                         'error_message': "Frontend Error",
                                                         'instructions_title': instructions.getTitle(),
                                                         'instructions_steps': instructions.getSteps()
                                                         })


@login_required(login_url='/auth/login')
def rfq_manager(request):
    menu_texts = FrontendTexts('menu')
    instructions = Instructions('rfqs', 'manage')
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
            return render(request, 'rfqs/rfq_selector.html', {'menu_text': menu_texts.getComponent(),
                                                              'view_texts': view_texts.getComponent(),
                                                              'selector_form': selector_form,
                                                              'instructions_title': instructions.getTitle(),
                                                              'instructions_steps': instructions.getSteps()})

    except ValueError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'rfqs/rfq_selector.html', {'menu_text': menu_texts.getComponent(),
                                                          'view_texts': view_texts.getComponent(),
                                                          'error_message': 'Backend problem',
                                                          'instructions_title': instructions.getTitle(),
                                                          'instructions_steps': instructions.getSteps()
                                                          })

    except ConnectionError as exception:
        print("Backend connection problem")
        print(exception)
        return render(request, 'rfqs/rfq_selector.html', {'menu_text': menu_texts.getComponent(),
                                                                    'view_texts': view_texts.getComponent(),
                                                                    'error_message': 'Backend connection problem',
                                                                    'instructions_title': instructions.getTitle(),
                                                                    'instructions_steps': instructions.getSteps()
                                                                    })

    except Exception as exception:
        print(exception)
        return render(request, 'rfqs/rfq_selector.html', {'menu_text': menu_texts.getComponent(),
                                                          'view_texts': view_texts.getComponent(),
                                                          'error_message': 'System error',
                                                          'instructions_title': instructions.getTitle(),
                                                          'instructions_steps': instructions.getSteps()
                                                          })


@login_required(login_url='/auth/login')
def rfq_editor(request, code):
    menu_texts = FrontendTexts('menu')
    instructions = Instructions('rfqs', 'edit')
    try:

        backend_host = MachineConfigurator().getBackend()

        r = requests.post(backend_host + '/auth/rfqs/' + code)

        backend_message = BackendMessage(json.loads(r.text))

        backend_result = json.loads(backend_message.getValue())

        rfq_form = RFQFormOnlyinfo(initial=backend_result)

        if request.method == 'POST':

            rfq_form = RFQFormOnlyinfo(request.POST)

            if rfq_form.is_valid():
                # ... update current material with the data provided

                creator = RFQCreator()
                result = creator.editRFQ(rfq_form)
                result_json = []

                for rfq in result:
                    result_json.append(json.dumps(rfq))

                r = requests.put(backend_host + '/auth/rfqs/' + code, json=result)

                backend_message = BackendMessage(json.loads(r.text))

                backend_result = json.loads(backend_message.getValue())

                return render(request, 'rfqs/rfq_editor.html', {'menu_text': menu_texts.getComponent(),
                                                                'view_texts': view_texts.getComponent(),
                                                                'updated_materials': backend_result})

        return render(request, 'rfqs/rfq_editor.html', {'menu_text': menu_texts.getComponent(),
                                                        'view_texts': view_texts.getComponent(),
                                                        'rfq_form': rfq_form,
                                                        'instructions_title': instructions.getTitle(),
                                                        'instructions_steps': instructions.getSteps()})

    except ValueError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'rfqs/rfq_editor.html', {'menu_text': menu_texts.getComponent(),
                                                        'view_texts': view_texts.getComponent(),
                                                        'error_message': 'No such RFQ exists in the DB: '+ code,
                                                        'instructions_title': instructions.getTitle(),
                                                        'instructions_steps': instructions.getSteps() })

    except ConnectionError as exception:
        print("Backend connection problem")
        print(exception)
        return render(request, 'rfqs/rfq_editor.html', {'menu_text': menu_texts.getComponent(),
                                                        'view_texts': view_texts.getComponent(),
                                                        'error_message': 'Backend connection problem',
                                                        'instructions_title': instructions.getTitle(),
                                                        'instructions_steps': instructions.getSteps()})

    except Exception as exception:
        print(exception)
        return render(request, 'rfqs/rfq_editor.html', {'menu_text': menu_texts.getComponent(),
                                                        'view_texts': view_texts.getComponent(),
                                                        'error_message': 'System error',
                                                        'instructions_title': instructions.getTitle(),
                                                        'instructions_steps': instructions.getSteps()})


@login_required(login_url='/auth/login')
def rfq_material_editor_test(request, code):
    menu_texts = FrontendTexts('menu')
    instructions = Instructions('rfqs', 'edit')
    try:

        backend_host = MachineConfigurator().getBackend()

        r = requests.post(backend_host + '/auth/rfqs/' + code)

        backend_message = BackendMessage(json.loads(r.text))

        backend_result = json.loads(backend_message.getValue())

        material_data = backend_result['materialList']

        rfq_form = RFQFormOnlyinfo(initial=backend_result)

        MaterialFormSet = formset_factory(ExtMaterialForm, extra=0)
        materials_formset = MaterialFormSet(initial=material_data)

        if request.method == 'POST':

            rfq_form = RFQFormOnlyinfo(request.POST)

            materials_formset = MaterialFormSet(request.POST)

            if rfq_form.is_valid() and materials_formset.is_valid():
                # ... update current material with the data provided
                # ... send data to backend

                creator = RFQCreator()
                result = creator.editRFQwithMaterials(rfq_form, materials_formset)
                result_json = []

                for rfq in result:
                    result_json.append(json.dumps(rfq))

                r = requests.put(backend_host + '/auth/rfqs/' + code, json=result)

                backend_message = BackendMessage(json.loads(r.text))

                backend_result = json.loads(backend_message.getValue())

                return render(request, 'rfqs/rfq_material_editor.html', {'menu_text': menu_texts.getComponent(),
                                                                         'view_texts': view_texts.getComponent(),
                                                                         'updated_materials': backend_result})

        return render(request, 'rfqs/rfq_material_editor.html', {'menu_text': menu_texts.getComponent(),
                                                                 'view_texts': view_texts.getComponent(),
                                                                 'rfq_form': rfq_form,
                                                                 'materials_formset': materials_formset,
                                                                 'instructions_title': instructions.getTitle(),
                                                                 'instructions_steps': instructions.getSteps()})

    except ValueError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'rfqs/rfq_material_editor.html', {'menu_text': menu_texts.getComponent(),
                                                                 'view_texts': view_texts.getComponent(),
                                                                 'error_message': 'No such RFQ exists in the DB: ' + code,
                                                                 'instructions_title': instructions.getTitle(),
                                                                 'instructions_steps': instructions.getSteps()})

    except ConnectionError as exception:
        print("Backend connection problem")
        print(exception)
        return render(request, 'rfqs/rfq_material_editor.html', {'menu_text': menu_texts.getComponent(),
                                                                 'view_texts': view_texts.getComponent(),
                                                                 'error_message': 'Backend connection problem',
                                                                 'instructions_title': instructions.getTitle(),
                                                                 'instructions_steps': instructions.getSteps()})

    except Exception as exception:
        print(exception)
        return render(request, 'rfqs/rfq_material_editor.html', {'menu_text': menu_texts.getComponent(),
                                                                 'view_texts': view_texts.getComponent(),
                                                                 'error_message': 'System error',
                                                                 'instructions_title': instructions.getTitle(),
                                                                 'instructions_steps': instructions.getSteps()})

