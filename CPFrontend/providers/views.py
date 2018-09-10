from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from requests.exceptions import ConnectionError

from .services.ProviderCreator import ProviderCreator
from .forms import ProviderForm
from .forms import CommentForm
from .forms import SelectorForm

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
def simple_upload(request):
    instructions = Instructions('providers', 'upload')
    uploaded_file_url = ''
    try:

        if request.method == 'POST' and request.FILES['myfile']:

            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            # ... do here the magic
            creator = ProviderCreator()
            result = creator.createProvidersfromCSV('.' + uploaded_file_url)
            result_json = []

            for provider in result:
                result_json.append(json.dumps(provider))

            backend_host = MachineConfigurator().getBackend()

            r = requests.post(backend_host + '/auth/providers/', json=result)

            backend_message = BackendMessage(json.loads(r.text))

            backend_result = json.loads(backend_message.getValue())

            cleanup(uploaded_file_url)

            return render(request, 'providers/simple_upload.html', {
                'uploaded_providers': backend_result})

        return render(request, 'providers/simple_upload.html', {'instructions_title': instructions.getTitle(),
                                                                'instructions_steps': instructions.getSteps()})

    except MultiValueDictKeyError as exception:
            print("No file selected")
            print(exception)
            return render(request, 'providers/simple_upload.html', {'error_message': 'No file selected',
                                                                    'instructions_title': instructions.getTitle(),
                                                                    'instructions_steps': instructions.getSteps()
                                                                    })
    except UnicodeDecodeError as exception:
        print("There is a problem with the input file - unicode decoding error")
        print(exception)
        cleanup(uploaded_file_url)
        return render(request, 'providers/simple_upload.html', {'error_message': 'Cannot read file correctly',
                                                                'instructions_title': instructions.getTitle(),
                                                                'instructions_steps': instructions.getSteps()
                                                                })

    except ValueError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        cleanup(uploaded_file_url)
        return render(request, 'providers/simple_upload.html', {'error_message': 'Backend problem',
                                                                'instructions_title': instructions.getTitle(),
                                                                'instructions_steps': instructions.getSteps()
                                                                })

    except ConnectionError as exception:
        cleanup(uploaded_file_url)
        print("Backend connection problem")
        print(exception)
        return render(request, 'providers/simple_upload.html', {'error_message': 'Backend connection problem',
                                                                'instructions_title': instructions.getTitle(),
                                                                'instructions_steps': instructions.getSteps()
                                                                })

    except Exception as exception:
        print(exception)
        cleanup(uploaded_file_url)
        return render(request, 'providers/simple_upload.html', {'error_message': 'System error',
                                                                'instructions_title': instructions.getTitle(),
                                                                'instructions_steps': instructions.getSteps()
                                                                })


@login_required(login_url='/auth/login')
def list_all(request):
    try:

        backend_host = MachineConfigurator().getBackend()

        r = requests.get(backend_host + '/auth/providers/')

        backend_message = BackendMessage(json.loads(r.text))

        providers_list = json.loads(backend_message.getValue())

        paginator = Paginator(providers_list, 10)  # Show 25 contacts per page

        page = request.GET.get('page')

        contacts = paginator.get_page(page)

        return render(request, 'providers/list_all.html', {'contacts': contacts})

    except ValueError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'providers/list_all.html', {'error_message': 'Backend problem',
                                                           })

    except ConnectionError as exception:
        print("Backend connection problem")
        print(exception)
        return render(request, 'providers/list_all.html', {'error_message': 'Backend connection problem',
                                                           })

    except Exception as exception:
        print(exception)
        return render(request, 'providers/list_all.html', {'error_message': 'System error',
                                                           })


@login_required(login_url='/auth/login')
def provider_creator(request):
    instructions = Instructions('providers', 'create')

    try:
        if request.method == 'POST':
            form = ProviderForm(request.POST)
            if form.is_valid():

                creator = ProviderCreator()
                result = creator.createProvider(form)
                result_json = []

                print(result)

                for provider in result:
                    result_json.append(json.dumps(provider))

                backend_host = MachineConfigurator().getBackend()

                r = requests.post(backend_host + '/auth/providers/', json=result)

                backend_message = BackendMessage(json.loads(r.text))

                backend_result = json.loads(backend_message.getValue())

                return render(request, 'providers/provider_creator.html', {
                    'uploaded_providers': backend_result})

        else:
            form = ProviderForm()
            return render(request, 'providers/provider_creator.html', {'providerform': form,
                                                                       'instructions_title': instructions.getTitle(),
                                                                       'instructions_steps': instructions.getSteps()})

    except ValueError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'providers/provider_creator.html', {'error_message': 'Backend problem',
                                                                   'instructions_title': instructions.getTitle(),
                                                                   'instructions_steps': instructions.getSteps()
                                                                   })

    except ConnectionError as exception:
        print("Backend connection problem")
        print(exception)
        return render(request, 'providers/provider_creator.html', {'error_message': 'Backend connection problem',
                                                                   'instructions_title': instructions.getTitle(),
                                                                   'instructions_steps': instructions.getSteps()
                                                                   })

    except Exception as exception:
        print(exception)
        return render(request, 'providers/provider_creator.html', {'error_message': 'System error',
                                                                   'instructions_title': instructions.getTitle(),
                                                                   'instructions_steps': instructions.getSteps()
                                                                   })


@login_required(login_url='/auth/login')
def provider_manager(request):
    instructions = Instructions('providers', 'manage')

    try:
        if request.method == 'POST':
            selector_form = SelectorForm(request.POST)

            if selector_form.is_valid():
                code = selector_form.cleaned_data['code']
                action = selector_form.cleaned_data['action']

                if action == '1':
                    return redirect('edit/' + code)
                elif action == '2':
                    return redirect('comment/' + code)

        else:
            selector_form = SelectorForm()
            return render(request, 'providers/provider_selector.html', {'selector_form': selector_form,
                                                                        'instructions_title': instructions.getTitle(),
                                                                        'instructions_steps': instructions.getSteps()})

    except ValueError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'providers/provider_selector.html', {'error_message': 'Backend problem',
                                                                    'instructions_title': instructions.getTitle(),
                                                                    'instructions_steps': instructions.getSteps()
                                                                    })

    except ConnectionError as exception:
        print("Backend connection problem")
        print(exception)
        return render(request, 'providers/provider_selector.html', {'error_message': 'Backend connection problem',
                                                                    'instructions_title': instructions.getTitle(),
                                                                    'instructions_steps': instructions.getSteps()
                                                                    })

    except Exception as exception:
        print(exception)
        return render(request, 'providers/provider_selector.html', {'error_message': 'System error',
                                                                    'instructions_title': instructions.getTitle(),
                                                                    'instructions_steps': instructions.getSteps()
                                                                    })


@login_required(login_url='/auth/login')
def provider_editor(request, code):
    instructions = Instructions('providers', 'edit')

    try:

        backend_host = MachineConfigurator().getBackend()

        r = requests.post(backend_host + '/auth/providers/' + code)

        backend_message = BackendMessage(json.loads(r.text))

        backend_result = json.loads(backend_message.getValue())

        provider_form = ProviderForm(initial=backend_result)

        if request.method == 'POST':

            provider_form = ProviderForm(request.POST)

            if provider_form.is_valid():
                # ... update current provider with the data provided
                print(code)

                creator = ProviderCreator()
                result = creator.createProvider(provider_form)
                result_json = []

                print(result)

                for provider in result:
                    result_json.append(json.dumps(provider))

                r = requests.put(backend_host + '/auth/providers/' + code, json=result)

                backend_message = BackendMessage(json.loads(r.text))

                backend_result = json.loads(backend_message.getValue())

                return render(request, 'providers/provider_editor.html', {'updated_providers': backend_result})

        return render(request, 'providers/provider_editor.html', {'provider_form': provider_form,
                                                                  'instructions_title': instructions.getTitle(),
                                                                  'instructions_steps': instructions.getSteps()})

    except ValueError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'providers/provider_editor.html', {'error_message': 'No such provider exists in the DB: '
                                                                                   + code,
                                                                  'instructions_title': instructions.getTitle(),
                                                                  'instructions_steps': instructions.getSteps()
                                                                  })

    except ConnectionError as exception:
        print("Backend connection problem")
        print(exception)
        return render(request, 'providers/provider_editor.html', {'error_message': 'Backend connection problem',
                                                                  'instructions_title': instructions.getTitle(),
                                                                  'instructions_steps': instructions.getSteps()
                                                                  })

    except Exception as exception:
        print(exception)
        return render(request, 'providers/provider_editor.html', {'error_message': 'System error',
                                                                  'instructions_title': instructions.getTitle(),
                                                                  'instructions_steps': instructions.getSteps()
                                                                  })


@login_required(login_url='/auth/login')
def provider_comment(request, code):
    instructions = Instructions('providers', 'comment')

    try:

        if request.method == 'POST':

            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                # ... update current provider with the data provided

                backend_host = MachineConfigurator().getBackend()

                creator = ProviderCreator()
                result = creator.createComment(comment_form)

                r = requests.post(backend_host + '/auth/providers/comments/' + code, json=result)

                backend_message = BackendMessage(json.loads(r.text))

                backend_result = json.loads(backend_message.getValue())

                return render(request, 'providers/provider_comment.html', {'updated_providers': backend_result})

        form = CommentForm()
        return render(request, 'providers/provider_comment.html', {'comment_form': form,
                                                                   'instructions_title': instructions.getTitle(),
                                                                   'instructions_steps': instructions.getSteps()})

    except ValueError as exception:
        print("There is a problem with the backend return value")
        print(exception)
        return render(request, 'providers/provider_comment.html', {'error_message': 'Backend problem',
                                                                   'instructions_title': instructions.getTitle(),
                                                                   'instructions_steps': instructions.getSteps()
                                                                   })

    except ConnectionError as exception:
        print("Backend connection problem")
        print(exception)
        return render(request, 'providers/provider_comment.html', {'error_message': 'Backend connection problem',
                                                                   'instructions_title': instructions.getTitle(),
                                                                   'instructions_steps': instructions.getSteps()
                                                                   })

    except Exception as exception:
        print(exception)
        return render(request, 'providers/provider_comment.html', {'error_message': 'System error',
                                                                   'instructions_title': instructions.getTitle(),
                                                                   'instructions_steps': instructions.getSteps()
                                                                   })
