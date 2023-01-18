from rest_framework.decorators import api_view
from  rest_framework.response import Response

import mysql.connector
import json
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="must",
  database="health_care_system"
)

mycursor = mydb.cursor(dictionary=True)



# Create your views here.
@api_view(['POST'])
def test(request):
   # mycursor.execute("SELECT * from physical_activity")
   # result=mycursor.fetchall()
   # return Response(result)
   print(request)
   print(request.body)
   print(request.POST)
   return Response()

@api_view(['POST'])
def login(request):
   try:
      ty = int(request.POST.get("type"))
      name=request.POST.get('userName')
      password = request.POST.get('password')

      # data = json.loads(request.body)
      # ty=data['type']
      # name = data['userName']
      # password= data['password']
      if ty==0:
         mycursor.execute("select * from patient where username='{}' and password='{}'".format(name, password))
      elif ty==1:
         mycursor.execute("select * from doctor where username='{0}' and password='{1}'".format(name, password))
      result = mycursor.fetchone()
      print(result)
      if result:
         return Response({"message":1, 'name':result['name'], 'gender':result['gender'], 'mobile':result['mobile'], 'email':result['email']})
      return Response({"message":0})
   except Exception as e:
      print(e)
      return Response({"message":0})

@api_view(['POST'])
def doctorRegister(request):
   try:
      name=request.POST.get('name')
      password = request.POST.get('password')
      userName = request.POST.get("userName")
      gender = request.POST.get("gender")
      mobile = request.POST.get("mobile")
      specialist = request.POST.get("specialist")
      email = request.POST.get("email")

      mycursor.execute("select * from doctor where username='{0}'".format(userName))
      result = mycursor.fetchall()
      if len(result)==1:
         return Response({"message":2})
      mycursor.execute("insert into doctor(name, gender, mobile, email, password, username, specialist) values('{}','{}', '{}', '{}','{}','{}',{})".format(name, gender, mobile, email, password, userName, specialist))
      x=mycursor.rowcount

      mydb.commit()
      if x==1:
         return Response({"message":1})
      return Response({"message":0})
   except Exception as e:
      print(e)
      return Response({"message":0})

@api_view(['GET'])
def doctorSpecialist(request):
   try:
      mycursor.execute("select * from specialist")
      result = mycursor.fetchall()
      return Response(result)
   except Exception as e:
      print(e)
      return Response()


@api_view(['GET'])
def doctorProfile(request, id):
   try:
      mycursor.execute("select *, s.name as specialist,d.name as name, d.id as id from doctor d, specialist s where username='{}' and s.id=d.specialist".format(id))
      result=mycursor.fetchone()
      return Response(result)
   except Exception as e:
      print(e)
      return Response()


@api_view(['POST'])
def patientRegister(request):
   try:
      name=request.POST.get('name')
      password = request.POST.get('password')
      userName = request.POST.get("userName")
      gender = request.POST.get("gender")
      mobile = request.POST.get("mobile")
      dob = request.POST.get("dob")
      email = request.POST.get("email")
      height = request.POST.get("height")
      weight = request.POST.get("weight")

      mycursor.execute("select * from patient where username='{0}'".format(userName))
      result = mycursor.fetchall()
      if len(result)==1:
         return Response({"message":2})
      mycursor.execute("insert into patient(name, gender, mobile, email, password, username, height, weight, dob) values('{}','{}', '{}', '{}','{}','{}',{},{},'{}')".format(name, gender, mobile, email, password, userName, height, weight, dob))
      x=mycursor.rowcount

      mydb.commit()
      if x==1:
         return Response({"message":1})
      return Response({"message":0})
   except Exception as e:
      print(e)
      return Response()


@api_view(['GET'])
def patientProfile(request, id):
   try:
      mycursor.execute("select *,floor(datediff(current_date, dob)/365) as age from patient where username='{}'".format(id))
      result=mycursor.fetchone()
      return Response(result)
   except Exception as e:
      print(e)
      return Response()


@api_view(['GET'])
def physicalActivity(request):
   try:
      mycursor.execute("SELECT * from physical_activity")
      result=mycursor.fetchall()
      return Response(result)
   except Exception as e:
      print(e)
      return Response()


@api_view(['GET'])
def patientSearchDoctor(request, id):
   try:
      mycursor.execute("SELECT username,name from doctor where specialist={}".format(id))
      result=mycursor.fetchall()
      return Response(result)
   except Exception as e:
      print(e)
      return Response()

@api_view(['POST'])
def patDocChat(request):
   try:
      sender = request.POST.get('sender')
      receiver = request.POST.get("receiver")
      message = request.POST.get("message")
      mycursor.execute("insert into chats(sender, receiver, message) values('{}','{}', '{}')".format(sender, receiver, message))
      x=mycursor.rowcount

      mydb.commit()
      if x==1:
         return Response({"message":1})
      return Response({"message":0})
   except Exception as e:
      print(e)
      return Response({"message":-1})


@api_view(['POST'])
def patDocGetChat(request):
   try:
      sender = request.POST.get('sender')
      receiver = request.POST.get("receiver")
      # print("SELECT * from chats where (sender='{0}' and recevier='{1}') or (sender='{1}' and receiver='{0}')".format(sender, receiver))
      mycursor.execute("SELECT sender, receiver, message from chats where (sender='{0}' and receiver='{1}') or (sender='{1}' and receiver='{0}')".format(sender, receiver))
      result=mycursor.fetchall()
      return Response(result)
   except Exception as e:
      print(e)
      return Response()

@api_view(['GET'])
def patChats(request, id):
   try:
      mycursor.execute("Select distinct receiver from chats where (sender='{}')".format(id))
      result = mycursor.fetchall()
      res = []
      for i in result:
         mycursor.execute("select d.username, d.name, s.name as sname from doctor d, specialist s where d.username='{}' and d.specialist=s.id".format(i['receiver']))
         data = mycursor.fetchone()
         res.append(data)
      return Response(res)
   except Exception as e:
      print(e)
      return Response()

@api_view(['GET'])
def docChats(request,id):
   try:
      mycursor.execute("Select distinct sender from chats where (receiver='{}')".format(id))
      result = mycursor.fetchall()
      res = []
      for i in result:
         mycursor.execute("select name,username from patient where username='{}'".format(i["sender"]))
         data = mycursor.fetchone()
         res.append(data)
      return Response(res)
   except Exception as e:
      print(e)
      return Response()


@api_view(['POST'])
def prescribeMedicine(request):
   try:
      print(request.body)
      data = json.loads(request.body)
      print(request.query_params)
      diagnosis = request.query_params["diagnosis"]
      advice = request.query_params["advice"]
      prescribedTo = request.query_params["prescribedTo"]
      prescribedBy = request.query_params["prescribedBy"]
      return Response()
   except Exception as e:
      print(e)
      return Response()