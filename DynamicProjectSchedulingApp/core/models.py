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
                         email, password, *args, profile_picture=None, **kwargs):
        """
        function to create user
        :param dob:
        :param profile_picture: Profile picture of the user
        :param first_name: First name of user
        :param last_name: Last name of user
        :param employee_id: employee id of user
        :param email: email address of user
        :param password: password(hashed)
        :return: User object
        """
        if not all([full_name, nick_name, email]):
            raise ValueError("Fields missing!")

        email = self.normalize_email(email)
        user = self.model(profile_picture=profile_picture, full_name=full_name,
                          nick_name=nick_name, email=email, *args, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, full_name, nick_name,
                         email, password, *args, profile_picture=None, **kwargs):
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
                                password=password, *args, **kwargs)
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
    creation_date = models.DateField(auto_now_add=True, null=True, blank=False)
    account_update_date = models.DateField(auto_now=True, null=True, blank=True)
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


class OrganisationAccountManager(models.Manager):
    """
    Manager class for OrganisationAccount
    """
    def create_org_account(self, user_account, industry, country_code,
                           contact_no, country, province_state, city,
                           address_line_one, address_line_two=None,
                           address_line_three=None,
                           *args, **kwargs):
        """
        Creates and returns OrganisationAccount object
        :param user_account: user account to which
                             organisation account is linked
        :param industry: industry
        :param country_code: country code(+91, +1, etc.)
        :param contact_no: contact number
        :param address_line_one: address line one
        :param address_line_two: address line two
        :param address_line_three: address line three
        :param country: country
        :param province_state: State/Province(Maharashtra, M.P. etc.)
        :param city: City (Mumbai, N.Y. etc.)
        :param args: extra args
        :param kwargs: extra kwargs
        :return: OrganisationAccount object
        """
        if user_account is None:
            raise ValueError('User account must be created before '
                             'creating an organisation account!')
        if not all([industry, country, contact_no, country, province_state,
                   city, address_line_one]):
            raise ValueError("Mandatory fields missing!")

        org_acc = self.model(user_account=user_account,
                                      industry=industry,
                                      country_code=country_code,
                                      contact_no=contact_no,
                                      address_line_one=address_line_one,
                                      address_line_two=address_line_two,
                                      address_line_three=address_line_three,
                                      country=country, province_state=province_state,
                                      city=city,
                                    *args, **kwargs)
        org_acc.save(using=self._db)

        return org_acc


class OrganisationAccount(models.Model):
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
    country_code = models.CharField(max_length=10, null=False, blank=False)
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

    """
    Assign a manager
    """
    objects = OrganisationAccountManager()


class ManagerAccountManager(models.Manager):
    """
    Manager for ManagerAccount model
    """
    def create_manager_account(self, user_account, employee_id, belongs_to):
        """
        Creates and returns ManagerAccount object
        :param user_account: user account to which manager account is linked
        :param employee_id: employee_id of manager
        :param belongs_to: organisation to which the ManagerAccount belongs
        :return: ManagerAccount object
        """
        if not all([user_account, belongs_to, employee_id]):
            raise ValueError('Create user account, organisation account and'
                             ' provide employee id to create manager account')
        manager_acc = self.model(user_account=user_account,
                                     employee_id=employee_id,
                                     belongs_to=belongs_to)

        manager_acc.save(using=self._db)

        return manager_acc


class ManagerAccount(models.Model):
    """
    Model for handling Manager Account
    """
    """
    Link the User model(for authentication)
    """
    user_account = models.OneToOneField(User, on_delete=models.CASCADE)

    employee_id = models.CharField(max_length=10, unique=True, null=False)
    belongs_to = models.ForeignKey(OrganisationAccount,
                                   on_delete=models.DO_NOTHING, null=False)

    objects = ManagerAccountManager()


class AssociateAccountManager(models.Manager):
    """
    Manager for managing AssociateAccount model
    """
    def create_associate_account(self, user_account, employee_id,
                                 reports_to, belongs_to):
        """
        Creates and returns AssociateAccount object
        :param user_account: user account to which AssociateAccount will be linked
        :param employee_id: employee id of the user
        :param reports_to: manager to whom the associate reports(can be null)
        :param belongs_to: organisation to which the associate belongs(cannot be null)
        :return: AssociateAccount object
        """
        if not all([user_account, employee_id, reports_to, belongs_to]):
            raise ValueError('Make sure a user account, an employee id, and '
                             'organisation is created before creating associate account')

        assoc_acc = AssociateAccount(user_account=user_account, employee_id=employee_id,
                                     reports_to=reports_to, belongs_to=belongs_to)
        assoc_acc.save(using=self._db)

        return assoc_acc


class AssociateAccount(models.Model):
    """
    Model for handling Associate Account
    """
    """
    Link the User model(for authentication)
    """
    user_account = models.OneToOneField(User, on_delete=models.CASCADE)

    employee_id = models.CharField(max_length=10, unique=True, null=False)
    reports_to = models.ForeignKey(ManagerAccount, on_delete=models.DO_NOTHING)
    belongs_to = models.ForeignKey(OrganisationAccount,
                                   on_delete=models.DO_NOTHING, null=False)

    objects = AssociateAccountManager()

