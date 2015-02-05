# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime, date

from appl.models import Employee, CompanyDetail, PreCompany

c_lst = CompanyDetail.objects.all().only('c_name')

def home(request):
    return render_to_response('appl/home.html', context_instance=RequestContext(request))

@csrf_exempt
def log_in(request):
    if request.method == "POST":
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        user = authenticate(username = user_name, password = pass_word)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('appl.views.company_list')
            else:
                return render_to_response('appl/home.html', {'flag': 'Account Disabled'}, context_instance=RequestContext(request))
        else:
            return render_to_response('appl/home.html', {'flag': 'invalid username or password'}, context_instance=RequestContext(request))
         
def log_out(request):
    logout(request)
    return redirect('appl.views.home')
             
def sign_up(request):
    field = {'lst': c_lst}
    return render_to_response('appl/sign_up.html', {'field': field}, context_instance=RequestContext(request))

def signup(request):
    field = {}
    if request.method=="POST":
        user_name = request.POST.get('username')
        email = request.POST.get('email-id')
        name = request.POST.get('name')
        age = request.POST.get('age')
        curr_company_name = request.POST.get('current-company')
        desination = request.POST.get('desination')
        pass_word = request.POST.get('password')
        conferm_password = request.POST.get('c_password')

        field = {'u_name': user_name, 'e_mail': email, 'p_word': pass_word, 'c_pass': conferm_password, 'p_name': name,
         'p_age': age, 'p_c_company': curr_company_name, 'p_desination': desination, 'lst': c_lst, 'flag': 'flag'} 

        if all((user_name, email, pass_word, conferm_password, name, age, curr_company_name, desination)):
            newemployee = Employee()
            usrname = User.objects.filter(username = user_name)
            if usrname:
                return render_to_response('appl/sign_up.html', {'flag': 'User Already Exist', 'field': field}, 
context_instance=RequestContext(request))

            if (pass_word != conferm_password):
               return render_to_response('appl/sign_up.html', {'flag': 'Password Mismatch', 'field': field}, 
context_instance=RequestContext(request))
            else:
               user = User()
               user.username = user_name
               user.first_name = name
               user.email = email
               user.set_password(pass_word)
               user.is_staff = True
               user.save()
            
               curr_company = get_object_or_404(CompanyDetail, c_name=curr_company_name)
               
               newemployee.name = name
               newemployee.age = age
               newemployee.desination = desination
               newemployee.confermPassword = conferm_password
               newemployee.user = user
               newemployee.current_Company = curr_company
               newemployee.save()
               return render_to_response('appl/sucess.html', {'field': field}, context_instance=RequestContext(request))
        else:
            return render_to_response('appl/sign_up.html', {'field': field}, context_instance=RequestContext(request))

def change_detail(request):
    u = request.user
    objct = get_object_or_404(Employee, user__username = u)
    field = {'uname': u, 'objct': objct, 'lst': c_lst}
    return render_to_response('appl/change_detail.html', {'field': field}, context_instance=RequestContext(request))

def changed(request):
    u = request.user
    field = {}
    c_lst = CompanyDetail.objects.all().only('c_name')
    objct = get_object_or_404(Employee, user__username=u)
    if request.method=="POST": 
        updat = get_object_or_404(Employee, user__username=u)
        email = request.POST.get('email-id')
        name = request.POST.get('name')
        age = request.POST.get('age')
        curr_company_name = request.POST.get('current-company')
        desination = request.POST.get('desination')
        pass_word = request.POST.get('password')
        conferm_password = request.POST.get('c_password')

        field = {'uname': u, 'objct': objct, 'e_mail': email, 'p_word': pass_word, 'c_pass': conferm_password,
 'p_name': name, 'p_age': age, 'p_c_company': curr_company_name, 'p_desination': desination,
 'lst': c_lst, 'flag1': 'flag1', 'flag2': 'password missmatch'} 
        
        if all((email, pass_word, conferm_password, name, age, curr_company_name, desination)):
            if (pass_word != conferm_password):
                return render_to_response('appl/change_detail.html', {'field': field}, context_instance=RequestContext(request))
            updat.name = name
            updat.age = age
            updat.desination = desination
            updat.confermPassword = pass_word
            updat.user.set_password(pass_word)
            updat.user.email = email
            updat.user.first_name = name
            updat.user.is_staff = True
            updat.user.save()

            curr_company = get_object_or_404(CompanyDetail, c_name = curr_company_name)

            updat.current_Company = curr_company
            updat.save()

            if(str(objct.current_Company) != str(curr_company_name)):
                precompanydetail = get_object_or_404(CompanyDetail, c_name = objct.current_Company)

                pre_company = PreCompany()
                pre_company.company_name = precompanydetail
                pre_company.pre_desination = objct.desination
                pre_company.save()
                updat.preCompany.add(pre_company)
            if(str(objct.desination) != str(desination) and str(objct.current_Company) == str(curr_company_name)):
                precompanydetail = get_object_or_404(CompanyDetail, c_name = curr_company_name)
                pre_company = PreCompany()
                pre_company.company_name = precompanydetail
                pre_company.pre_desination = objct.desination
                pre_company.save()
                updat.preCompany.add(pre_company)
            return redirect('appl.views.emp_detail', u)
        return render_to_response('appl/change_detail.html', {'field': field}, context_instance=RequestContext(request))

def company_list(request):
    return render_to_response('appl/company_list.html', {'lst': c_lst}, context_instance=RequestContext(request))

def company_detail(request, companyname):
    c_detail = get_object_or_404(CompanyDetail, c_name=companyname) 
    # we can use, p = CompanyDetail.objects.get(c_name=companyname) and then e = p.employee_set.all()
    employee_list = Employee.objects.filter(current_Company__c_name = c_detail.c_name)
    ctx = { 'employee': employee_list, 'cmpdet': c_detail}
    return render_to_response('appl/company_detail.html', ctx, context_instance=RequestContext(request))

def emp_detail(request, usrname):
     new = request.user
     detail = get_object_or_404(Employee, user__username=usrname)
     new1 = detail.user.username
     if (str(new)==str(new1)):
         ctx = {'detail': detail, 'page': 'Have all permission'}
         return render_to_response('appl/emp_detail.html', ctx, context_instance=RequestContext(request))
     else:
         return render_to_response('appl/emp_detail.html', {'detail': detail}, context_instance=RequestContext(request))

@csrf_exempt
def search(request):
    search_name = request.POST.get('namee')
    search_desination = request.POST.get('desination')
    search_company = request.POST.get('companyname') 
    p = Employee.objects.filter(name__istartswith=search_name).filter(desination__istartswith=search_desination).filter(current_Company__c_name__istartswith=search_company)
    ctx = {'lst': p, 'rslt': 'Hello'}
    return render_to_response('appl/result.html', ctx, context_instance=RequestContext(request))
             
