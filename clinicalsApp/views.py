from django.shortcuts import render,redirect
from clinicalsApp.models import Patient,ClinicalData
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from clinicalsApp.forms import ClinicalDataForm
# Create your views here.

class PatientListView(ListView):
    model=Patient

class PatientCreateView(CreateView):
    model=Patient
    success_url=reverse_lazy('index')
    fields=('firstName','lastName','age')

class PatientUpdateView(UpdateView):
    model=Patient
    success_url=reverse_lazy('index')
    fields=('firstName','lastName','age')

class PatientDeleteView(DeleteView):
    model=Patient
    success_url=reverse_lazy('index')

def addData(request,**kwargs):
    form=ClinicalDataForm()
    patient=Patient.objects.get(id=kwargs['pk'])
    if request.method=='POST':
        form=ClinicalDataForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    return render(request,'clinicalsApp/clinicaldata_form.html',{'form':form,'patient':patient})

def analyze(request,**kwargs):
    data=ClinicalData.objects.filter(patient_id=kwargs['pk'])
    responseData=[]
    for eachEntry in data: 
        if eachEntry.componentName == 'hw':
            heightandweight = eachEntry.componentValue.split('/')
            if len(heightandweight) > 1:
                feettometers=float(heightandweight[0])*0.4536
                ans = float(heightandweight[1])/(feettometers*feettometers)
                bmiEntry=ClinicalData()
                bmiEntry.componentName='BMI'
                bmiEntry.componentValue=ans
                responseData.append(bmiEntry)
        responseData.append(eachEntry)


    return render(request,'clinicalsApp/generalReport.html',{'data':responseData})
    
