from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from requests.exceptions import ConnectionError

from .services.MaterialCreator import MaterialCreator

import requests
import json
import os

from common.BackendMessage import BackendMessage
from common.MachineConfig import MachineConfigurator
from common.Instructions import Instructions
from common.FrontendTexts import FrontendTexts

from .forms import xcheckForm
from .forms import SelectorForm
from .forms import MaterialForm
from .forms import WeightCalculatorForm
from .choices import *


view_texts = FrontendTexts('materials')


def cleanup(filename):
    try:
        os.remove('.' + filename)
        print("removed file: " + filename)
    except Exception as error:
        print(error)


@login_required(login_url='/auth/login')
def simple_upload(request):
    menu_texts = FrontendTexts('menu')
    instructions = Instructions('materials', 'upload')
    uploaded_file_url = ''
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

            backend_result = json.loads(backend_message.getValue())

            cleanup(uploaded_file_url)

            return render(request, 'materials/simple_upload.html', {'menu_text': menu_texts.getComponent(),
                                                                    'view_texts': view_texts.getComponent(),
                                                                    'uploaded_materials': backend_result } )

        return render(request, 'materials/simple_upload.html', {'menu_text': menu_texts.getComponent(),
                                                                'view_texts': view_texts.getComponent(),
                                                                'instructions_title': instructions.getTitle(),
                                                                'instructions_steps': instructions.getSteps()})

    except MultiValueDictKeyError as exception:
            print("No file selected")
            print(exception)
            return render(request, 'materials/simple_upload.html', {'menu_text': menu_texts.getComponent(),
                                                                    'view_texts': view_texts.getComponent(),
                                                                    'error_message': 'No file selected',
                                                                    'instructions_title': instructions.getTitle(),
                                                                    'instructions_steps': instructions.getSteps()
                                                                    })
    except UnicodeDecodeError as exception:
        print("There is a problem with the input file - unicode decoding error")
        print(exception)
        cleanup(uploaded_file_url)
        return render(request, 'materials/simple_upload.html', {'menu_text': menu_texts.getComponent(),
                                                                'view_texts': view_texts.getComponent(),
                                                                'error_message': 'Cannot read file correctly',
                                                                'instructions_title': instructions.getTitle(),
                                                                'instructions_steps': instructions.getSteps()
                                                                })

    except ValueError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        cleanup(uploaded_file_url)
        return render(request, 'materials/simple_upload.html', {'menu_text': menu_texts.getComponent(),
                                                                'view_texts': view_texts.getComponent(),
                                                                'error_message': 'Backend problem',
                                                                'instructions_title': instructions.getTitle(),
                                                                'instructions_steps': instructions.getSteps()
                                                                })

    except ConnectionError as exception:
        cleanup(uploaded_file_url)
        print("Backend connection problem")
        print(exception)
        return render(request, 'materials/simple_upload.html', {'menu_text': menu_texts.getComponent(),
                                                                'view_texts': view_texts.getComponent(),
                                                                'error_message': 'Backend connection problem',
                                                                'instructions_title': instructions.getTitle(),
                                                                'instructions_steps': instructions.getSteps()
                                                                })

    except Exception as exception:
        print(exception)
        cleanup(uploaded_file_url)
        return render(request, 'materials/simple_upload.html', {'menu_text': menu_texts.getComponent(),
                                                                'view_texts': view_texts.getComponent(),
                                                                'error_message': 'System error',
                                                                'instructions_title': instructions.getTitle(),
                                                                'instructions_steps': instructions.getSteps()
                                                                })


@login_required(login_url='/auth/login')
def singlexcheck(request):
    menu_texts = FrontendTexts('menu')
    instructions = Instructions('materials', 'singlexcheck')
    try:
        if request.method == 'POST':
            form = xcheckForm(request.POST)
            if form.is_valid():

                itemcode = form.cleaned_data['itemcode']

                backend_host = MachineConfigurator().getBackend()

                r = requests.post(backend_host + '/auth/materials/xcheck/' + itemcode)

                backend_message = BackendMessage(json.loads(r.text))
                backend_result = json.loads(backend_message.getValue())

                return render(request, 'materials/singlexcheck.html', {'menu_text': menu_texts.getComponent(),
                                                                       'view_texts': view_texts.getComponent(),
                                                                       'xform': form,
                                                                       'uploaded_materials': backend_result})

        else:
            form = xcheckForm()

        return render(request, 'materials/singlexcheck.html', {'menu_text': menu_texts.getComponent(),
                                                               'view_texts': view_texts.getComponent(),
                                                               'xform': form,
                                                               'instructions_title': instructions.getTitle(),
                                                               'instructions_steps': instructions.getSteps()})

    except ValueError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'materials/singlexcheck.html', {'menu_text': menu_texts.getComponent(),
                                                               'view_texts': view_texts.getComponent(),
                                                               'error_message': 'Backend problem',
                                                               'instructions_title': instructions.getTitle(),
                                                               'instructions_steps': instructions.getSteps()
                                                               })

    except ConnectionError as exception:
        print("Backend connection problem")
        print(exception)
        return render(request, 'materials/singlexcheck.html', {'menu_text': menu_texts.getComponent(),
                                                               'view_texts': view_texts.getComponent(),
                                                               'error_message': 'Backend connection problem',
                                                               'instructions_title': instructions.getTitle(),
                                                               'instructions_steps': instructions.getSteps()
                                                               })

    except Exception as exception:
        print(exception)
        return render(request, 'materials/singlexcheck.html', {'menu_text': menu_texts.getComponent(),
                                                               'view_texts': view_texts.getComponent(),
                                                               'error_message': 'System error',
                                                               'instructions_title': instructions.getTitle(),
                                                               'instructions_steps': instructions.getSteps()
                                                               })


@login_required(login_url='/auth/login')
def multiplexcheck(request):
    menu_texts = FrontendTexts('menu')
    instructions = Instructions('materials', 'multiplexcheck')
    uploaded_file_url = ''
    try:
        if request.method == 'POST' and request.FILES['myfile']:

            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            creator = MaterialCreator()
            result = creator.createMaterial('.' + uploaded_file_url)
            result_json = []

            for material in result:
                result_json.append(json.dumps(material))

            backend_host = MachineConfigurator().getBackend()

            r = requests.post(backend_host + '/auth/materials/xcheck', json=result)

            backend_message = BackendMessage(json.loads(r.text))
            backend_result = json.loads(backend_message.getValue())

            cleanup(uploaded_file_url)

            return render(request, 'materials/multiplexcheck.html', {'menu_text': menu_texts.getComponent(),
                                                                     'view_texts': view_texts.getComponent(),
                                                                     'uploaded_materials': backend_result})

        return render(request, 'materials/multiplexcheck.html', {'menu_text': menu_texts.getComponent(),
                                                                 'view_texts': view_texts.getComponent(),
                                                                 'instructions_title': instructions.getTitle(),
                                                                 'instructions_steps': instructions.getSteps()})

    except MultiValueDictKeyError as exception:
            print("No file selected")
            print(exception)
            return render(request, 'materials/multiplexcheck.html', {'menu_text': menu_texts.getComponent(),
                                                                     'view_texts': view_texts.getComponent(),
                                                                     'error_message': 'No file selected',
                                                                     'instructions_title': instructions.getTitle(),
                                                                     'instructions_steps': instructions.getSteps()
                                                                     })

    except ValueError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        cleanup(uploaded_file_url)
        return render(request, 'materials/multiplexcheck.html', {'menu_text': menu_texts.getComponent(),
                                                                 'view_texts': view_texts.getComponent(),
                                                                 'error_message': 'Backend problem',
                                                                 'instructions_title': instructions.getTitle(),
                                                                 'instructions_steps': instructions.getSteps()
                                                                 })

    except ConnectionError as exception:
        cleanup(uploaded_file_url)
        print("Backend connection problem")
        print(exception)
        return render(request, 'materials/multiplexcheck.html', {'menu_text': menu_texts.getComponent(),
                                                                 'view_texts': view_texts.getComponent(),
                                                                 'error_message': 'Backend connection problem',
                                                                 'instructions_title': instructions.getTitle(),
                                                                 'instructions_steps': instructions.getSteps()
                                                                 })

    except Exception as exception:
        print(exception)
        cleanup(uploaded_file_url)
        return render(request, 'materials/multiplexcheck.html', {'menu_text': menu_texts.getComponent(),
                                                                 'view_texts': view_texts.getComponent(),
                                                                 'error_message': 'System error',
                                                                 'instructions_title': instructions.getTitle(),
                                                                 'instructions_steps': instructions.getSteps()
                                                                 })


@login_required(login_url='/auth/login')
def material_manager(request):
    menu_texts = FrontendTexts('menu')
    instructions = Instructions('materials', 'manage')
    try:
        if request.method == 'POST':
            selector_form = SelectorForm(request.POST)

            if selector_form.is_valid():
                code = selector_form.cleaned_data['code']
                action = selector_form.cleaned_data['action']

                if action == '1':
                    return redirect('edit/' + code)
                elif action == '2':
                    return redirect('weight/' + code)

        else:
            selector_form = SelectorForm()
            return render(request, 'materials/material_selector.html', {'menu_text': menu_texts.getComponent(),
                                                                        'view_texts': view_texts.getComponent(),
                                                                        'selector_form': selector_form,
                                                                        'instructions_title': instructions.getTitle(),
                                                                        'instructions_steps': instructions.getSteps()})

    except ValueError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'materials/material_selector.html', {'menu_text': menu_texts.getComponent(),
                                                                    'view_texts': view_texts.getComponent(),
                                                                    'error_message': 'Backend problem',
                                                                    'instructions_title': instructions.getTitle(),
                                                                    'instructions_steps': instructions.getSteps()
                                                                    })

    except ConnectionError as exception:
        print("Backend connection problem")
        print(exception)
        return render(request, 'materials/material_selector.html', {'menu_text': menu_texts.getComponent(),
                                                                    'view_texts': view_texts.getComponent(),
                                                                    'error_message': 'Backend connection problem',
                                                                    'instructions_title': instructions.getTitle(),
                                                                    'instructions_steps': instructions.getSteps()
                                                                    })

    except Exception as exception:
        print(exception)
        return render(request, 'materials/material_selector.html', {'menu_text': menu_texts.getComponent(),
                                                                    'view_texts': view_texts.getComponent(),
                                                                    'error_message': 'System error',
                                                                    'instructions_title': instructions.getTitle(),
                                                                    'instructions_steps': instructions.getSteps()
                                                                    })


@login_required(login_url='/auth/login')
def material_editor(request, code):
    menu_texts = FrontendTexts('menu')
    instructions = Instructions('materials', 'edit')
    try:

        backend_host = MachineConfigurator().getBackend()

        r = requests.post(backend_host + '/auth/materials/' + code)

        backend_message = BackendMessage(json.loads(r.text))

        backend_result = json.loads(backend_message.getValue())

        print(backend_result)

        material_form = MaterialForm(initial=backend_result)

        if request.method == 'POST':

            material_form = MaterialForm(request.POST)

            if material_form.is_valid():
                # ... update current material with the data provided
                print(code)

                creator = MaterialCreator()
                result = creator.editMaterial(material_form)
                result_json = []

                print(result)

                for material in result:
                    result_json.append(json.dumps(material))

                r = requests.put(backend_host + '/auth/materials/' + code, json=result)

                backend_message = BackendMessage(json.loads(r.text))

                backend_result = json.loads(backend_message.getValue())

                return render(request, 'materials/material_editor.html', {'menu_text': menu_texts.getComponent(),
                                                                          'view_texts': view_texts.getComponent(),
                                                                          'updated_materials': backend_result})

        return render(request, 'materials/material_editor.html', {'menu_text': menu_texts.getComponent(),
                                                                  'view_texts': view_texts.getComponent(),
                                                                  'material_form': material_form,
                                                                  'instructions_title': instructions.getTitle(),
                                                                  'instructions_steps': instructions.getSteps()})

    except ValueError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'materials/material_editor.html', {'menu_text': menu_texts.getComponent(),
                                                                  'view_texts': view_texts.getComponent(),
                                                                  'error_message': 'No such material exists in the DB: '
                                                                                   + code,
                                                                  'instructions_title': instructions.getTitle(),
                                                                  'instructions_steps': instructions.getSteps()
                                                                  })

    except ConnectionError as exception:
        print("Backend connection problem")
        print(exception)
        return render(request, 'materials/material_editor.html', {'menu_text': menu_texts.getComponent(),
                                                                  'view_texts': view_texts.getComponent(),
                                                                  'error_message': 'Backend connection problem',
                                                                  'instructions_title': instructions.getTitle(),
                                                                  'instructions_steps': instructions.getSteps()
                                                                  })

    except Exception as exception:
        print(exception)
        return render(request, 'materials/material_editor.html', {'menu_text': menu_texts.getComponent(),
                                                                  'view_texts': view_texts.getComponent(),
                                                                  'error_message': 'System error',
                                                                  'instructions_title': instructions.getTitle(),
                                                                  'instructions_steps': instructions.getSteps()
                                                                  })


@login_required(login_url='/auth/login')
def material_weight(request, code):
    menu_texts = FrontendTexts('menu')
    instructions = Instructions('materials', 'weightcalc')
    try:

        backend_host = MachineConfigurator().getBackend()

        quantity_form = WeightCalculatorForm(request.POST)

        if request.method == 'POST':

            if quantity_form.is_valid():
                # ... update current material with the data provided

                value = quantity_form.cleaned_data['value']
                units = UNIT_CHOICES[int(quantity_form.cleaned_data['units'])-1][1]

                result = {'quantity': value, 'units': units}

                r = requests.post(backend_host + '/auth/materials/weights/' + code, json=result)

                backend_message = BackendMessage(json.loads(r.text))

                backend_result = json.loads(backend_message.getValue())

                return render(request, 'materials/material_weight.html', {'menu_text': menu_texts.getComponent(),
                                                                          'weight_materials': backend_result})

        return render(request, 'materials/material_weight.html', {'menu_text': menu_texts.getComponent(),
                                                                  'view_texts': view_texts.getComponent(),
                                                                  'quantity_form': quantity_form,
                                                                  'instructions_title': instructions.getTitle(),
                                                                  'instructions_steps': instructions.getSteps()})

    except ConnectionError as exception:
        print("Backend connection problem")
        print(exception)
        return render(request, 'materials/material_weight.html', {'menu_text': menu_texts.getComponent(),
                                                                  'view_texts': view_texts.getComponent(),
                                                                  'error_message': 'Backend connection problem',
                                                                  'instructions_title': instructions.getTitle(),
                                                                  'instructions_steps': instructions.getSteps()
                                                                  })

    except Exception as exception:
        print(exception)
        return render(request, 'materials/material_weight.html', {'menu_text': menu_texts.getComponent(),
                                                                  'view_texts': view_texts.getComponent(),
                                                                  'error_message': 'System error',
                                                                  'instructions_title': instructions.getTitle(),
                                                                  'instructions_steps': instructions.getSteps()
                                                                  })
