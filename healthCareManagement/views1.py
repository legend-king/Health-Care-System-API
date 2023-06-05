from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import (
    Patient,
    Doctor,
    Nutritionist,
    Specialist,
    PhysicalActivity,
    Chat,
    Prescription,
    PrescribedMedicine,
    PatientReport,
)
from rest_framework.decorators import api_view
from  rest_framework.response import Response
import json

# Create your views here.
@csrf_exempt
def test(request):
    if request.method == 'POST':
        return JsonResponse({})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            ty = int(request.POST.get("type"))
            name = request.POST.get('userName')
            password = request.POST.get('password')

            result = None

            if ty == 0:
                result = Patient.objects.filter(username=name, password=password).first()
            elif ty == 1:
                result = Doctor.objects.filter(username=name, password=password).first()
            elif ty == 3:
                result = Nutritionist.objects.filter(username=name, password=password).first()

            if result:
                response_data = {
                    "message": 1,
                    'name': result.name,
                    'gender': result.gender,
                    'mobile': result.mobile,
                    'email': result.email
                }
            else:
                response_data = {"message": 0}

            return JsonResponse(response_data)

        except Exception as e:
            print(e)
            return JsonResponse({"message": 0})

@csrf_exempt
def doctorRegister(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            password = request.POST.get('password')
            userName = request.POST.get("userName")
            gender = request.POST.get("gender")
            mobile = request.POST.get("mobile")
            specialist_id = request.POST.get("specialist")
            email = request.POST.get("email")
            consultation_charge = request.POST.get("consultationCharge")

            if Doctor.objects.filter(username=userName).exists():
                return JsonResponse({"message": 2})

            specialist = Specialist.objects.get(id=specialist_id)

            Doctor.objects.create(
                name=name,
                gender=gender,
                mobile=mobile,
                email=email,
                password=password,
                username=userName,
                specialist=specialist,
                consultation_charge=consultation_charge
            )

            return JsonResponse({"message": 1})

        except Exception as e:
            print(e)
            return JsonResponse({"message": 0})

@csrf_exempt
def doctorSpecialist(request):
    if request.method == 'GET':
        specialists = Specialist.objects.all().values()
        return JsonResponse(list(specialists), safe=False)

@csrf_exempt
def doctorProfile(request, id):
    if request.method == 'GET':
        doctor = Doctor.objects.select_related('specialist').filter(username=id).values(
            'username', 'name', 'specialist__name as specialist', 'gender', 'mobile', 'email'
        ).first()
        return JsonResponse(doctor, safe=False)

@csrf_exempt
def nutritionistProfile(request):
    if request.method == 'GET':
        id = request.GET.get("userName")
        nutritionist = Nutritionist.objects.filter(username=id).values().first()
        return JsonResponse(nutritionist, safe=False)

@csrf_exempt
def nutritionistRegister(request):
    if request.method == 'POST':
        try:
            data = request.POST
            name = data['name']
            password = data['password']
            userName = data["userName"]
            gender = data["gender"]
            mobile = data["mobile"]
            email = data["email"]
            consultation_charge = data['consultationCharge']

            if Nutritionist.objects.filter(username=userName).exists():
                return JsonResponse({"message": 2})

            Nutritionist.objects.create(
                name=name,
                gender=gender,
                mobile=mobile,
                email=email,
                password=password,
                username=userName,
                consultation_charge=consultation_charge
            )

            return JsonResponse({"message": 1})

        except Exception as e:
            print(e)
            return JsonResponse({"message": 0})

@csrf_exempt
def physicalActivityList(request):
    if request.method == 'GET':
        activities = PhysicalActivity.objects.all().values()
        return JsonResponse(list(activities), safe=False)

@csrf_exempt
def physicalActivityAdd(request):
    if request.method == 'POST':
        try:
            data = request.POST
            name = data['name']
            description = data['description']
            calories_burned = data['caloriesBurned']

            PhysicalActivity.objects.create(
                name=name,
                description=description,
                calories_burned=calories_burned
            )

            return JsonResponse({"message": 1})

        except Exception as e:
            print(e)
            return JsonResponse({"message": 0})

@csrf_exempt
def chatAdd(request):
    if request.method == 'POST':
        try:
            data = request.POST
            sender = data['sender']
            receiver = data['receiver']
            message = data['message'].strip()

            Chat.objects.create(
                sender=sender,
                receiver=receiver,
                message=message
            )

            return JsonResponse({"message": 1})

        except Exception as e:
            print(e)
            return JsonResponse({"message": 0})

@csrf_exempt
def prescriptionAdd(request):
    if request.method == 'POST':
        try:
            data = request.POST
            doctor_id = data['doctorId']
            patient_id = data['patientId']
            symptoms = data['symptoms']
            diagnosis = data['diagnosis']

            doctor = Doctor.objects.get(username=doctor_id)
            patient = Patient.objects.get(username=patient_id)

            prescription = Prescription.objects.create(
                doctor=doctor,
                patient=patient,
                symptoms=symptoms,
                diagnosis=diagnosis
            )

            medicines = data.getlist('medicines[]')
            for medicine in medicines:
                PrescribedMedicine.objects.create(
                    prescription=prescription,
                    medicine=medicine
                )

            return JsonResponse({"message": 1})

        except Exception as e:
            print(e)
            return JsonResponse({"message": 0})
        
@api_view(['POST'])
def prescribeMedicine(request):
    try:
        data = json.loads(request.body)
        diagnosis = request.data.get("diagnosis")
        advice = request.data.get("advice")
        prescribedTo = request.data.get("prescribedTo")
        prescribedBy = request.data.get("prescribedBy")

        prescription = Prescription.objects.create(prescribed_by=prescribedBy, prescribed_to=prescribedTo, diagnosis=diagnosis, advice=advice)

        for item in data:
            PrescribedMedicine.objects.create(
                prescription=prescription,
                medicine_name=item["medicineName"],
                medicine_type=item["medicineType"],
                before_breakfast=item["beforeBreakFastQuantity"],
                after_breakfast=item["afterBreakFastQuantity"],
                before_lunch=item["beforeLunchQuantity"],
                after_lunch=item["afterLunchQuantity"],
                before_dinner=item["beforeDinnerQuantity"],
                evening=item["eveningQuantity"],
                after_dinner=item["afterDinnerQuantity"],
                tablets=item["medicineQuantity"],
                duration=item["duration"]
            )

        return Response({"message": "Success"})
    except Exception as e:
        print(e)
        return Response({"message": "Failure"})

@csrf_exempt
def patientReports(request):
    if request.method == 'POST':
        try:
            data = request.POST
            patient_id = data['patientId']
            date = data['date']
            report_type = data['reportType']
            file = request.FILES.get('file')

            patient = Patient.objects.get(username=patient_id)

            report = PatientReport.objects.create(
                patient=patient,
                date=date,
                report_type=report_type,
                file=file
            )

            return JsonResponse({"message": 1})

        except Exception as e:
            print(e)
            return JsonResponse({"message": 0})
