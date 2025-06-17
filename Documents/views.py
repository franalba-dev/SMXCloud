from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from Documents.forms import DocumentForm, SubjectForm
from Documents.models import Document, Subject
from Users.views import user_is_not_alumno
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required()
def home(request):
    documents = Document.objects.filter(owner=request.user).order_by('-upload_date')
    subject_choices = Subject.objects.all().order_by('name')

    search = request.GET.get('search', '').strip()
    subject_pk   = request.GET.get('subject', '').strip()
    date_str     = request.GET.get('upload_date', '').strip()

    if search:
        documents = documents.filter(
            Q(title__icontains=search)
    )
        
    if subject_pk:
        if subject_pk == 'null':
            documents = documents.filter(subject__isnull=True)
        else:
            documents = documents.filter(subject_id=subject_pk)

    if date_str:
        documents = documents.filter(upload_date__date=date_str)

    paginator = Paginator(documents, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    total = paginator.num_pages
    current = page_obj.number

    start = max(current - 2, 1)
    end = min(start + 4, total)

    if end - start < 4:
        start = max(end - 4, 1)
    
    page_range = range(start, end + 1)
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1) 
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request,
        'home.html',
        {
            'page_range': page_range,
            'page_obj': page_obj,
            'documents': documents,
            'search': search,
            'subject_choices': subject_choices,
            'selected_subject': subject_pk,
            'selected_date': date_str,
            },
    )

@login_required()
def list_documents(request):
    documents = Document.objects.exclude(owner=request.user).order_by('-upload_date')
    subject_choices = Subject.objects.all().order_by('name')

    search = request.GET.get('search', '').strip()
    subject_pk   = request.GET.get('subject', '').strip()
    date_str     = request.GET.get('upload_date', '').strip()

    if search:
        documents = documents.filter(
            Q(title__icontains=search) |
            Q(owner__first_name__icontains=search) |
            Q(owner__last_names__icontains=search) |
            Q(owner__email__icontains=search)
    )
        
    if subject_pk:
        if subject_pk == 'null':
            documents = documents.filter(subject__isnull=True)
        else:
            documents = documents.filter(subject_id=subject_pk)

    if date_str:
        documents = documents.filter(upload_date__date=date_str)

    paginator = Paginator(documents, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    total = paginator.num_pages
    current = page_obj.number

    start = max(current - 2, 1)
    end = min(start + 4, total)

    if end - start < 4:
        start = max(end - 4, 1)
    
    page_range = range(start, end + 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1) 
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
        
    return render(
        request,
        'documents/list_documents.html',
        {
            'page_range': page_range,
            'page_obj': page_obj,
            'documents': documents,
            'search': search,
            'subject_choices': subject_choices,
            'selected_subject': subject_pk,
            'selected_date': date_str,
            },
    )

@login_required()
def upload_document(request):
     if request.method == 'GET':
             return render(
                 request,
                 'documents/upload_document.html',
                 {'document_form': DocumentForm()}
             )
     if request.method == 'POST':
         form = DocumentForm(request.POST, request.FILES)
         if form.is_valid():
            document = form.save(commit=False)  
            document.owner = request.user       
            document.save()
            messages.success(request, ("Se ha subido el documento."))
            return redirect('/')
         else:
             messages.success(request, ("No se ha podido subir el documento. Verifique que el título no exista e inténtelo nuevamente."))
             return render(
                 request,
                 'documents/upload_document.html',
                 {'document_form': form}
             )

@login_required()
def update_document(request, pk=None):
    document = Document.objects.get(pk=pk)
    if request.user == document.owner:
        if request.method == 'GET':
            document_form = DocumentForm(instance=document)
            return render(
                request,
                'documents/update_document.html',
                {
                    'document': document,
                    'document_form': document_form,
                },
            )
        
        if request.method == 'POST':
            document_form = DocumentForm(
                request.POST, request.FILES,
                instance=document,
            )
            if document_form.is_valid():
                document_form.save()
                messages.success(request, ("Se ha editado el documento."))
                return redirect('/')
            else:
                messages.success(request, ("No se ha podido editar el documento. Verifique que el título no exista e inténtelo nuevamente."))
                return render(
                    request,
                    'documents/update_document.html',
                    {'document_form': document_form}
                )
    else:
        return redirect('/no-autorizado/')

@login_required()
def delete_document(request, pk=None):
    document = Document.objects.get(pk=pk)
    if request.user == document.owner or user_is_not_alumno:
        document.delete()
        messages.success(request, ("Se ha eliminado el documento."))
        if request.user == document.owner:
            return redirect('/')
        else:
            return redirect('/lista-de-documentos/')
    else:
        return redirect('/no-autorizado/')

@login_required()
def list_subjects(request):
    subjects = Subject.objects.all()
    search = request.GET.get('search', '').strip()

    if search:
        subjects = subjects.filter(
            Q(name__icontains=search)
    )
        
    paginator = Paginator(subjects, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    total = paginator.num_pages
    current = page_obj.number

    start = max(current - 2, 1)
    end = min(start + 4, total)

    if end - start < 4:
        start = max(end - 4, 1)
    
    page_range = range(start, end + 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1) 
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)       

    return render(
        request,
        'subjects/list_subjects.html',
        {
            'page_range': page_range,
            'page_obj': page_obj,
            'subjects': subjects,
            'search': search,
        }
    )


@login_required()
@user_passes_test(user_is_not_alumno, login_url='/no-autorizado/')
def create_subject(request):
    if request.method == 'GET':
             return render(
                 request,
                 'subjects/create_subject.html',
                 {'subject_form': SubjectForm()}
             )
    if request.method == 'POST':
         form = SubjectForm(request.POST)
         if form.is_valid():    
            form.save()
            messages.success(request, ("Se ha creado la asignatura."))
            return redirect('lista-asignaturas')
         else:
            messages.success(request, ("No se ha podido crear la asignatura. Verifique que el nombre no exista e inténtelo nuevamente."))
            return render(
                 request,
                 'subjects/create_subject.html',
                 {'subject_form': form}
             )
         
@user_passes_test(user_is_not_alumno, login_url='/no-autorizado/')
@login_required()
def update_subject(request, pk=None):
    subject = Subject.objects.get(pk=pk)
    if request.method == 'GET':
        subject_form = SubjectForm(instance=subject)
        return render(
            request,
            'subjects/update_subject.html',
            {
                'subject': subject,
                'subject_form': subject_form,
            },
        )
    
    if request.method == 'POST':
        subject_form = SubjectForm(
            request.POST,
            instance=subject,
        )
        if subject_form.is_valid():
            subject_form.save()
            messages.success(request, ("Se ha editado la asignatura."))
            return redirect('lista-asignaturas')
        else:
            form = SubjectForm(data=request.POST, instance=subject)
            messages.success(request, ("No se ha podido editar la asignatura. Verifique que el nombre no exista e inténtelo nuevamente."))
            return render(
                request,
                'subjects/update_subject.html',
                {'subject_form': form},
            )
         
@user_passes_test(user_is_not_alumno, login_url='/no-autorizado/')
@login_required()
def delete_subject(request, pk=None):
    Subject.objects.get(pk=pk).delete()
    messages.success(request, ("Se ha eliminado la asignatura."))
    return redirect('lista-asignaturas')