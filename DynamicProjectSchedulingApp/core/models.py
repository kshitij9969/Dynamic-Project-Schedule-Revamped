from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,
                                        PermissionsMixin)


# class ProjectMetaData(models.Model):
#     """
#     Model for project meta data
#     """
#
#     project_name = models.CharField(max_length=255, unique=True, null=False)
#     project_description = models.TextField(null=False)
#
#     def __str__(self):
#         return f"Project name: {self.project_name}" \
#                f"Project description: {self.project_description}."
#
#
# class ProjectScheduleDetail(models.Model):
#     """
#     Model for project details
#     1. first field is boolean store wheather action
#     was taken on a particular date or not. For eg:
#     analysis: True means that analysis was done
#     for that particular date.
#
#     2. _text is a textfield to store any note for
#     that activity
#
#     """
#
#     assoc_project = models.ForeignKey(ProjectMetaData, on_delete=models.CASCADE)
#
#     date = models.DateField()
#
#     analysis = models.BooleanField(default=False)
#     analysis_text = models.TextField(default='')
#
#     cut = models.BooleanField(default=False)
#     cut_text = models.TextField(default='')
#
#     code_merge = models.BooleanField(default=False)
#     code_merge_text = models.TextField(default='')
#
#     ST = models.BooleanField(default=False)
#     ST_text = models.TextField(default='')
#
#     UAT = models.BooleanField(default=False)
#     UAT_text = models.TextField(default='')
#
#     implementation = models.BooleanField(default=False)
#     implementation_text = models.TextField(default='')
#
#     PIS = models.BooleanField(default=False)
#     PIS_text = models.TextField(default='')
#
#     def __str__(self):
#         """
#         String function to return string representation of
#         the object.
#         :return: String
#         """
#         return f"Date: {self.date}\n" \
#                f"Analysis: {self.analysis}\n" \
#                f"CUT: {self.cut}\n" \
#                f"Code Merger: {self.code_merge}\n" \
#                f"ST: {self.ST}\n" \
#                f"UAT: {self.UAT}\n" \
#                f"implementation: {self.implementation}\n" \
#                f"PIS: {self.PIS}\n"
#

def rename_profile_picture(instance, filename):
    """
    Rename the file on upload
    :param instance: User instance
    :param filename: the filename as uploaded by user
    :return: filepath + filename as String object
    """
    file_ext = filename.split('.')[1]
    return f"{instance.full_name}_{instance.nick_name}.{file_ext}"


class Organization(models.Model):
    """
    Model for organization details
    """
    pass


class UserManager(BaseUserManager):
    """
    Manager model for user
    """
    def create_user(self, full_name, nick_name,
                         email, password, dob, *args, profile_picture=None, **kwargs):
        """
        function to create user
        :param profile_picture: Profile picture of the user
        :param first_name: First name of user
        :param last_name: Last name of user
        :param employee_id: employee id of user
        :param email: email address of user
        :param password: password(hashed)
        :return: User object
        """
        if all([full_name, nick_name, email, dob]):
            email = self.normalize_email(email)
            user = self.model(profile_picture=profile_picture, full_name=full_name,
                              nick_name=nick_name, email=email,
                              dob=dob, *args, **kwargs)
            user.set_password(password)
            user.save(using=self._db)

            return user
        else:
            raise ValueError("Fields missing!")

    def create_superuser(self, full_name, nick_name,
                         email, password, dob, *args, profile_picture=None, **kwargs):
        """
        Function to create superuser
        :param profile_picture: Profile picture of the user
        :param first_name: First name of user
        :param last_name: Last name of user
        :param employee_id: employee id of user
        :param email: email address of user
        :param password: password(hashed)
        :return: User object
        """
        email = self.normalize_email(email)
        user = self.create_user(profile_picture=profile_picture,
                                full_name=full_name, nick_name=nick_name, email=email,
                                password=password, dob=dob, *args, **kwargs)
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model for user objects
    """
    """
    Basic information
    """
    profile_picture = models.ImageField(upload_to=rename_profile_picture,
                                        null=True, blank=True, default='')
    email = models.EmailField(max_length=200, unique=True, null=False)
    full_name = models.CharField(max_length=100, unique=False, null=False)
    nick_name = models.CharField(max_length=50, unique=False, null=True)
    dob = models.DateField(null=False, blank=False)

    """
    Permission information
    """
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    """
    Organization information
    """

    objects = UserManager()

    USERNAME_FIELD = 'email'


class OrganizationAccount(models.Model):
    """
    Model for handling Organization Account
    """
    """
    Link the User model(for authentication)
    """
    user_account = models.OneToOneField(User, on_delete=models.CASCADE)
    """
    Basic information
    """
    industry = models.CharField(max_length=50, null=False, blank=False)  # choices in a drop down
    country_code = models.CharField(max_length=5, null=False, blank=False)
    contact_no = models.CharField(max_length=30, null=False, blank=False)
    address_line_one = models.CharField(max_length=30, null=False, blank=False)
    address_line_two = models.CharField(max_length=30, null=True, blank=True)
    address_line_three = models.CharField(max_length=40, null=True, blank=True)
    country = models.CharField(max_length=50, null=False, blank=False)
    province_state = models.CharField(max_length=50, null=False, blank=False)
    city = models.CharField(max_length=30, null=False, blank=False)
    """
    Verification information
    """
    account_verified = models.BooleanField(default=True)  # Change this is to default=False


class ManagerAccount(User):
    """
    Model for handling Manager Account
    """
    """
    Link the User model(for authentication)
    """
    user_account = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)

    employee_id = models.CharField(max_length=10, unique=True, null=False)
    belongs_to = models.ForeignKey(OrganizationAccount,
                                   on_delete=models.DO_NOTHING, null=False)


class AssociateAccount(User):
    """
    Model for handling Associate Account
    """
    """
    Link the User model(for authentication)
    """
    user_account = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)

    employee_id = models.CharField(max_length=10, unique=True, null=False)
    reports_to = models.ForeignKey(ManagerAccount, on_delete=models.DO_NOTHING)
    belongs_to = models.ForeignKey(OrganizationAccount,
                                   on_delete=models.DO_NOTHING, null=False)

