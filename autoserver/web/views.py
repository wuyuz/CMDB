from django.shortcuts import render, redirect
from repository import models
from web.form import ServerForm


# Create your views here.
def index(request):
    return render(request, 'index.html')


def server_list(request):
    servers = models.Server.objects.all()

    return render(request, 'server_list.html', {'servers': servers})


def server_change(request, pk=None):
    obj = models.Server.objects.filter(pk=pk).first()
    form_obj = ServerForm(instance=obj)
    if request.method == 'POST':
        form_obj = ServerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('web:server_list')
    return render(request, 'form.html', {'form_obj': form_obj})


def server_detail(request,pk):
    obj = models.Server.objects.filter(pk=pk).first()
    disks = obj.disk_list.order_by('slot')
    return render(request,'server_detail.html',{'obj':obj,'disks':disks})


def server_record(request,pk):
    obj = models.Server.objects.filter(pk=pk).first()
    return render(request,'server_record.html',{'obj':obj})

