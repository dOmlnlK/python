from django.db import models

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)

# Create your models here.

class UserInfosManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user



class UserInfos(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,

    )
    name = models.CharField(max_length=64, verbose_name="姓名")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    #is_admin = models.BooleanField(default=False)
    role = models.ManyToManyField("Role", blank=True, null=True)

    objects = UserInfosManager()   #变量名必须是objects

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email


    class Meta:
        permissions = (
            ('crm_model_detail', '可以查看bestadmin每张表里所有的数据'),
            ('crm_model_change', '可以对bestadmin表里的每条数据进行修改'),
            ('crm_model_add', '可以对bestadmin每张表进行数据添加'),

        )









class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=32,verbose_name="角色")
    menus = models.ManyToManyField("Menus")

    def __str__(self):
        return self.name



class CustomerInfos(models.Model):
    """客户信息表"""
    name = models.CharField(max_length=32,default=None)
    contact_type_choices = ((0,"qq"),(1,"微信"),(2,"手机"))
    contact_type =models.SmallIntegerField(choices=contact_type_choices,default=0)
    contact = models.CharField(max_length=64,unique=True)
    consult_courses = models.ManyToManyField("Course",verbose_name="咨询课程")
    consult_content = models.TextField(verbose_name="咨询内容")
    consultant = models.ForeignKey("UserInfos",verbose_name="咨询顾问")
    status_choices = ((0,"未报名"),(1,"已报名"),(2,"已退学"))
    status = models.SmallIntegerField(choices=status_choices)
    source_choices = ((0,"QQ群"),(1,"51CTO"),(2,"百度推广"),(3,"知乎"),(4,"转介绍"),(5,"其他"))
    source = models.SmallIntegerField(choices=source_choices)
    referral_from = models.ForeignKey("self",blank=True,null=True)
    id_num = models.CharField(max_length=32,blank=True,null=True)
    sex_choices = ((0,"女"),(1,"男"))
    sex = models.SmallIntegerField(choices=sex_choices,blank=True,null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class CustomerFollowUp(models.Model):
    """客户跟踪记录表"""
    customer = models.ForeignKey("CustomerInfos")
    content = models.TextField(verbose_name="跟进内容")
    user = models.ForeignKey("UserInfos",verbose_name="跟进人")
    status_choices = ((0,"近期无报名计划"),(1,"1个月内报名"),(2,"两周内报名"),(3,"已经报名"))
    status = models.SmallIntegerField(choices=status_choices)
    date = models.DateField(auto_now_add=True)

class Course(models.Model):
    """课程表"""
    name = models.CharField(max_length=32,unique=True,verbose_name="课程名称")
    outline = models.TextField(verbose_name="课程大纲")
    price = models.PositiveSmallIntegerField(verbose_name="课程价格")
    period = models.PositiveSmallIntegerField(verbose_name="课程周期(月)",default=5)

    def __str__(self):
        return self.name


class ClassList(models.Model):
    """班级列表"""
    branch = models.ForeignKey("Branch")
    course = models.ForeignKey("Course")
    semester = models.PositiveSmallIntegerField(verbose_name="学期")
    teachers = models.ManyToManyField("UserInfos",verbose_name="讲师")
    contract_template = models.ForeignKey("ContractTemplate",blank=True,null=True)

    start_date = models.DateField(verbose_name="开学时间")
    graduate_date = models.DateField(verbose_name="毕业时间",blank=True,null=True)
    class_type_choices = ((0,"脱产班"),(1,"周末班"),(2,"网络班"))
    class_type = models.SmallIntegerField(choices=class_type_choices,default=0)

    def __str__(self):
        return "%s(%s)期"%(self.course,self.semester)
    class Meta:
        unique_together = ("course","semester","branch","class_type")


class Branch(models.Model):
    """校区表"""
    name = models.CharField(max_length=32,unique=True)
    addr = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class CourseRecord(models.Model):
    """上课记录"""
    class_grade = models.ForeignKey("ClassList",verbose_name="上课班级")
    day_num = models.PositiveSmallIntegerField(verbose_name="课程节次")
    teacher = models.ForeignKey("UserInfos",verbose_name="本节讲师")
    title = models.CharField(verbose_name="本节主题",max_length=32)
    content = models.TextField(verbose_name="本节内容")
    has_homework = models.BooleanField(verbose_name="本节是否有作业",default=True)
    homework = models.TextField(verbose_name="作业需求",null=True,blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s(%s)节"%(self.class_grade,self.day_num)
    class Meta:
        unique_together = ("class_grade","day_num")



class StudyRecord(models.Model):
    """学习记录表"""
    course_record = models.ForeignKey('CourseRecord')
    student = models.ForeignKey("Student")

    score_choices = (
        (90,"A"),
        (80,"B"),
        (60,"C"),
        (40,"D"),
        (0,"N/A"),
        (-1,"COPY")
    )
    score = models.SmallIntegerField(choices=score_choices)

    show_choices =(
        (0,"缺勤"),
        (1,"已签到"),
        (2,"迟到"),
        (3,"早退")
    )
    show_status = models.SmallIntegerField(choices=show_choices,default=1)

    note = models.TextField(verbose_name="成绩备注",blank=True,null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s %s %s"%(self.course_record,self.student,self.score)



class Student(models.Model):
    """学员表"""
    customer = models.OneToOneField("CustomerInfos")
    class_grades = models.ManyToManyField("ClassList")

    def __str__(self):
        return self.customer.name



class Menus(models.Model):
    """菜单表"""
    name = models.CharField(max_length=32)
    url_type_choices = ((0,"absolute"),(1,"dynamic"))
    url_type = models.SmallIntegerField(choices=url_type_choices,default=0)
    url_name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name","url_name")


class ContractTemplate(models.Model):
    """合同模板表"""
    name = models.CharField(max_length=32)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)


class StudentEnrollment(models.Model):
    """学员报名表"""
    customer = models.ForeignKey("CustomerInfos")
    class_grade = models.ForeignKey("ClassList")
    consultant = models.ForeignKey("UserInfos")

    contract_argeed = models.BooleanField(default=False)
    contract_argeed_date = models.DateField(verbose_name="客户同意时间",blank=True,null=True)

    contract_approved = models.BooleanField(default=False)
    contract_approved_date = models.DateField(verbose_name="审核通过时间",blank=True, null=True)

    class Meta:
        unique_together = ("customer","class_grade")

    def __str__(self):
        return self.customer.name


class PaymentRecoed(models.Model):
    """学员缴费记录表"""
    enrollment = models.ForeignKey("StudentEnrollment")

    payment_type_choices = ((0,"报名费"),(1,"学费"),(2,"退费"))
    payment_type = models.SmallIntegerField(choices=payment_type_choices,default=0)

    amount = models.IntegerField(verbose_name="费用",default=500)
    consultant = models.ForeignKey("UserInfos")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return enumerate







