"""PESU URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from smsapp import views
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from smsapp import views, HodViews, StaffViews, StudentViews


urlpatterns = [
    path('', views.loginPage,name="show_login"),
    path('index/', views.showIndexPage),
    path('login', views.doLogin,name="login"),
    path('get_user_details', views.GetUserDetails),
    path('logout', views.doLogout,name="logout"),
    path('admin', admin.site.urls),
    path('admin_home',HodViews.admin_home,name="admin_home"),
    path('add_staff',HodViews.add_staff,name="add_staff"),
    path('add_staff_save',HodViews.add_staff_save,name="add_staff_save"),
    path('add_course', HodViews.add_course,name="add_course"),
    path('add_course_save', HodViews.add_course_save,name="add_course_save"),
    path('add_student', HodViews.add_student,name="add_student"),
    path('add_student_save', HodViews.add_student_save,name="add_student_save"),
    path('add_subject', HodViews.add_subject,name="add_subject"),
    path('add_subject_save', HodViews.add_subject_save,name="add_subject_save"),
    path('manage_staff', HodViews.manage_staff,name="manage_staff"),
    path('manage_student', HodViews.manage_student,name="manage_student"),
    path('manage_course', HodViews.manage_course,name="manage_course"),
    path('manage_subject', HodViews.manage_subject,name="manage_subject"),
    path('edit_staff/<str:staff_id>', HodViews.edit_staff,name="edit_staff"),
    path('edit_staff_save', HodViews.edit_staff_save,name="edit_staff_save"),
    path('edit_student/<str:student_id>', HodViews.edit_student,name="edit_student"),
    path('edit_student_save', HodViews.edit_student_save,name="edit_student_save"),
    path('edit_subject/<str:subject_id>', HodViews.edit_subject,name="edit_subject"),
    path('edit_subject_save', HodViews.edit_subject_save,name="edit_subject_save"),
    path('edit_course/<str:course_id>', HodViews.edit_course,name="edit_course"),
    path('edit_course_save', HodViews.edit_course_save,name="edit_course_save"),
    path('manage_session', HodViews.manage_session,name="manage_session"),
    path('add_session_save', HodViews.add_session_save,name="add_session_save"),
                      #     Staff URL Path
    path('staff_home', StaffViews.staff_home, name="staff_home"),
    path('staff_take_attendance', StaffViews.staff_take_attendance, name="staff_take_attendance"),
    path('staff_update_attendance', StaffViews.staff_update_attendance, name="staff_update_attendance"),
    path('get_students', StaffViews.get_students, name="get_students"),
    path('get_attendance_dates', StaffViews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student', StaffViews.get_attendance_student, name="get_attendance_student"),
    path('save_attendance_data', StaffViews.save_attendance_data, name="save_attendance_data"),
    path('save_updateattendance_data', StaffViews.save_updateattendance_data, name="save_updateattendance_data"),
    # path('staff_apply_leave', StaffViews.staff_apply_leave, name="staff_apply_leave"),
    # path('staff_apply_leave_save', StaffViews.staff_apply_leave_save, name="staff_apply_leave_save"),
    # path('staff_feedback', StaffViews.staff_feedback, name="staff_feedback"),
    # path('staff_feedback_save', StaffViews.staff_feedback_save, name="staff_feedback_save"),
    path('staff_profile', StaffViews.staff_profile, name="staff_profile"),
    path('staff_profile_save', StaffViews.staff_profile_save, name="staff_profile_save"),
    path('staff_fcmtoken_save', StaffViews.staff_fcmtoken_save, name="staff_fcmtoken_save"),
    path('staff_all_notification', StaffViews.staff_all_notification, name="staff_all_notification"),
    # path('staff_add_result', StaffViews.staff_add_result, name="staff_add_result"),
    # path('save_student_result', StaffViews.save_student_result, name="save_student_result"),
    # path('edit_student_result',EditResultViewClass.as_view(), name="edit_student_result"),
    # path('fetch_result_student',StaffViews.fetch_result_student, name="fetch_result_student"),
    # path('start_live_classroom',StaffViews.start_live_classroom, name="start_live_classroom"),
    # path('start_live_classroom_process',StaffViews.start_live_classroom_process, name="start_live_classroom_process"),


    path('student_home', StudentViews.student_home, name="student_home"),
    path('student_view_attendance', StudentViews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    # path('student_apply_leave', StudentViews.student_apply_leave, name="student_apply_leave"),
    # path('student_apply_leave_save', StudentViews.student_apply_leave_save, name="student_apply_leave_save"),
    # path('student_feedback', StudentViews.student_feedback, name="student_feedback"),
    # path('student_feedback_save', StudentViews.student_feedback_save, name="student_feedback_save"),
    path('student_profile', StudentViews.student_profile, name="student_profile"),
    path('student_profile_save', StudentViews.student_profile_save, name="student_profile_save"),
    path('student_fcmtoken_save', StudentViews.student_fcmtoken_save, name="student_fcmtoken_save"),
    # path('firebase-messaging-sw.js',views.showFirebaseJS,name="show_firebase_js"),
    path('student_all_notification',StudentViews.student_all_notification,name="student_all_notification"),
    # path('student_view_result',StudentViews.student_view_result,name="student_view_result"),
    # path('join_class_room/<int:subject_id>/<int:session_year_id>',StudentViews.join_class_room,name="join_class_room"),
    path('node_modules/canvas-designer/widget.html',StaffViews.returnHtmlWidget,name="returnHtmlWidget"),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

# UPDATE(13th Apr 2021): till tutorial 5 done
