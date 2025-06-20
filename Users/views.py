from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from Users.forms import CreateUserForm, UpdateUserForm
from Users.models import User
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def unauthorized(request):
    return render(request, 'authentication/unauthorized.html')

def user_is_not_alumno(user):
    return not user.groups.filter(name='Alumnos').exists()

@login_required()
@user_passes_test(user_is_not_alumno, login_url='/unauthorized/')
def list_users(request):
    alumnos_group = Group.objects.get(name='Alumnos')
    users = User.objects.filter(groups=alumnos_group)

    search      = request.GET.get('search', '').strip()
    gender_pk   = request.GET.get('gender', '').strip() 
    date_str    = request.GET.get('birthday', '').strip()

    if search:
        users = users.filter(
            Q(first_name__icontains=search) |
            Q(last_names__icontains=search) |
            Q(email__icontains=search)
        )
    
    if gender_pk:
        if gender_pk == 'null':
            users = users.filter(gender__isnull=True)
        else:
            users = users.filter(gender=gender_pk)

    gender_choices = (
        User.objects
            .values_list('gender', flat=True)
            .distinct()
    )

    if date_str:
        users = users.filter(birthday=date_str)

    paginator = Paginator(users, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    total = paginator.num_pages
    current = page_obj.number

    start = max(current - 2, 1)
    end = min(start + 4, total)

    if end - start < 4:
        start = max(end - 4, 1)
    
    page_range = range(start, end + 1)

    return render(
        request,
        'users/list_users.html',
        {
            'page_obj': page_obj,
            'page_range': page_range,
            'users': users,
            'search': search,
            'gender_pk': gender_pk,
            'selected_date': date_str,
            'gender_choices': gender_choices,
        },
    )

@login_required()
@user_passes_test(user_is_not_alumno, login_url='/unauthorized/')
def create_user(request):
    if request.method == 'GET':
             return render(
                 request,
                 'users/create_user.html',
                 {'user_form': CreateUserForm()}
             )
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            alumnos_group = Group.objects.get(name='Alumnos')
            user.groups.add(alumnos_group)
            messages.success(request, ("Se ha creado el usuario."))
            return redirect('/lista-de-usuarios/')
        else:
            messages.success(request, ("No se ha podido crear el usuario. Verifique que el nombre no exista e inténtelo nuevamente."))
            return render(
                request,
                'users/create_user.html',
                {'user_form': form}
            )

@user_passes_test(user_is_not_alumno, login_url='/unauthorized/')
@login_required()
def update_user(request, pk=None):
    user = User.objects.get(pk=pk)
    if request.method == 'GET':
        user_form = UpdateUserForm(instance=user)
        return render(
            request,
            'users/update_user.html',
            {
                'user': user,
                'user_form': user_form,
            },
        )
    
    if request.method == 'POST':
        user_form = UpdateUserForm(
            request.POST,
            instance=user,
        )
        if user_form.is_valid():
            user_form.save()
            messages.success(request, ("Se ha editado el usuario."))
            return redirect('/lista-de-usuarios/')
        else:
            form = UpdateUserForm(data=request.POST, instance=user)
            messages.success(request, ("No se ha podido editar el usuario. Verifique que el nombre no exista e inténtelo nuevamente."))
            return render(
                request,
                'users/update_user.html',
                {'user_form': form}
            )

@user_passes_test(user_is_not_alumno, login_url='/unauthorized/')
@login_required()
def delete_user(request, pk=None):
    User.objects.get(pk=pk).delete()
    messages.success(request, ("Se ha eliminado el usuario."))
    return redirect('/lista-de-usuarios/')

def login_user(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Has iniciado sesión correctamente."))
            return redirect('/')   
        else:
            messages.success(request, ("Inicio de sesión fallido, inténtalo de nuevo."))
            return redirect('login')
    else:
        return render(request, 'authentication/login.html', {})

@login_required()
def logout_user(request):
    logout(request)
    messages.success(request, ("Has cerrado la sesión."))
    return redirect('login')