import json
from datetime import datetime
from uuid import uuid4

from django.contrib import messages
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from smsapp.models import Subjects, SessionYearModel, Students, Attendance, AttendanceReport, \
    Staffs, CustomUser, Courses, NotificationStaffs


def staff_home(request):
    #For Fetch All Student Under Staff
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    course_id_list=[]
    for subject in subjects:
        course=Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)

    final_course=[]
    #removing Duplicate Course ID
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    students_count=Students.objects.filter(course_id__in=final_course).count()

    #Fetch All Attendance Count
    attendance_count=Attendance.objects.filter(subject_id__in=subjects).count()

    #Fetch All Approve Leave
    staff=Staffs.objects.get(admin=request.user.id)
    # leave_count=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
    subject_count=subjects.count()

    #Fetch Attendance Data by Subject
    subject_list=[]
    attendance_list=[]
    for subject in subjects:
        attendance_count1=Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    students_attendance=Students.objects.filter(course_id__in=final_course)
    student_list=[]
    student_list_attendance_present=[]
    student_list_attendance_absent=[]
    for student in students_attendance:
        attendance_present_count=AttendanceReport.objects.filter(status=True,student_id=student.id).count()
        attendance_absent_count=AttendanceReport.objects.filter(status=False,student_id=student.id).count()
        student_list.append(student.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    return render(request,"staff_template/staff_home_template.html",{"students_count":students_count,"attendance_count":attendance_count,"subject_count":subject_count,"subject_list":subject_list,"attendance_list":attendance_list,"student_list":student_list,"present_list":student_list_attendance_present,"absent_list":student_list_attendance_absent})

def staff_take_attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_years=SessionYearModel.object.all()
    return render(request,"staff_template/staff_take_attendance.html",{"subjects":subjects,"session_years":session_years})

@csrf_exempt
def get_students(request):
    subject_id=request.POST.get("subject")
    session_year=request.POST.get("session_year")

    subject=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.object.get(id=session_year)
    students=Students.objects.filter(course_id=subject.course_id,session_year_id=session_model)
    list_data=[]

    for student in students:
        data_small={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_attendance_data(request):
    student_ids=request.POST.get("student_ids")
    subject_id=request.POST.get("subject_id")
    attendance_date=request.POST.get("attendance_date")
    session_year_id=request.POST.get("session_year_id")

    subject_model=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.object.get(id=session_year_id)
    json_sstudent=json.loads(student_ids)
    #print(data[0]['id'])


    try:
        attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date,session_year_id=session_model)
        attendance.save()

        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'])
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

def staff_update_attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_year_id=SessionYearModel.object.all()
    return render(request,"staff_template/staff_update_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})

@csrf_exempt
def get_attendance_dates(request):
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_updateattendance_data(request):
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    json_sstudent=json.loads(student_ids)


    try:
        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport.objects.get(student_id=student,attendance_id=attendance)
             attendance_report.status=stud['status']
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def staff_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    staff=Staffs.objects.get(admin=user)
    return render(request,"staff_template/staff_profile.html",{"user":user,"staff":staff})

def staff_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            staff=Staffs.objects.get(admin=customuser.id)
            staff.address=address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))

@csrf_exempt
def staff_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        staff=Staffs.objects.get(admin=request.user.id)
        staff.fcm_token=token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def staff_all_notification(request):
    staff=Staffs.objects.get(admin=request.user.id)
    notifications=NotificationStaffs.objects.filter(staff_id=staff.id)
    return render(request,"staff_template/all_notification.html",{"notifications":notifications})

@csrf_exempt
# def fetch_result_student(request):
#     subject_id=request.POST.get('subject_id')
#     student_id=request.POST.get('student_id')
#     student_obj=Students.objects.get(admin=student_id)
#     result=StudentResult.objects.filter(student_id=student_obj.id,subject_id=subject_id).exists()
#     if result:
#         result=StudentResult.objects.get(student_id=student_obj.id,subject_id=subject_id)
#         result_data={"exam_marks":result.subject_exam_marks,"assign_marks":result.subject_assignment_marks}
#         return HttpResponse(json.dumps(result_data))
#     else:
#         return HttpResponse("False")

# def start_live_classroom(request):
#     subjects=Subjects.objects.filter(staff_id=request.user.id)
#     session_years=SessionYearModel.object.all()
#     return render(request,"staff_template/start_live_classroom.html",{"subjects":subjects,"session_years":session_years})

# def start_live_classroom_process(request):
#     session_year=request.POST.get("session_year")
#     subject=request.POST.get("subject")

#     subject_obj=Subjects.objects.get(id=subject)
#     session_obj=SessionYearModel.object.get(id=session_year)
#     checks=OnlineClassRoom.objects.filter(subject=subject_obj,session_years=session_obj,is_active=True).exists()
#     if checks:
#         data=OnlineClassRoom.objects.get(subject=subject_obj,session_years=session_obj,is_active=True)
#         room_pwd=data.room_pwd
#         roomname=data.room_name
#     else:
#         room_pwd=datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
#         roomname=datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
#         staff_obj=Staffs.objects.get(admin=request.user.id)
#         onlineClass=OnlineClassRoom(room_name=roomname,room_pwd=room_pwd,subject=subject_obj,session_years=session_obj,started_by=staff_obj,is_active=True)
#         onlineClass.save()

#     return render(request,"staff_template/live_class_room_start.html",{"username":request.user.username,"password":room_pwd,"roomid":roomname,"subject":subject_obj.subject_name,"session_year":session_obj})


def returnHtmlWidget(request):
    return render(request,"widget.html")