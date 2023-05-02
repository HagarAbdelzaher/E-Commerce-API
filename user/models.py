from django.db import models
from django.contrib.auth import models as auth_models
# Create your models here.
class UserManager(auth_models.BaseUserManager):
    def create_user(
            self,
            firstName:str,
            lastName:str,
            email:str,
            phoneNumber:str,
            address:str,
            city:str,
            state:str,
            postalCode:str,
            username:str,
            password: str = None,
            is_staff=False,
            is_superuser=False,

            

    )->"User":
        if not email:
            raise ValueError ("User must have an Email")
        if not firstName:
            raise ValueError("User must have first name")
        if not lastName:
            raise ValueError("User must have last name")
        
        user = self.model(email=self.normalize_email(email))
        user.firstName = firstName
        user.lastName = lastName
        user.username = username
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.address = address
        user.city=city
        user.state=state
        user.postalCode = postalCode
        user.phoneNumber = phoneNumber
        user.set_password(password)
        user.save()
        
        return user
    
    
    def create_superuser(
        self,
        username:str,
        firstName: str,
        lastName: str,
        password: str ,
        email: str = "admin@gmail.com", 
        address :str="", 
        phoneNumber:str="",
        city:str="",
        state:str="",
        postalCode:str="",
        
    ) -> "User":
        user = self.create_user(
            firstName=firstName,
            lastName=lastName,
            email=email,
            password=password,
            address = address,
            phoneNumber= phoneNumber,
            city=city,
            state=state,
            postalCode=postalCode,
            username = username,
            is_staff=True,
            is_superuser=True,
        )
        user.save()

        return user
    
class User (auth_models.AbstractUser):
    email = models.EmailField(verbose_name = "Email" , unique=True)
    password = models.CharField(verbose_name = "Password" ,max_length=30 )
    username = models.CharField(verbose_name="username" , max_length=50 , unique=True,)
    firstName = models.CharField(verbose_name = "First Name ",max_length=50)
    lastName = models.CharField(verbose_name = "Last Name ",max_length=50)
    address  = models.TextField(verbose_name = "Address" ,null = True)
    city = models.CharField(verbose_name = "City",max_length=20,null = True)
    state = models.CharField(verbose_name = "State",max_length=50,null = True)
    postalCode = models.CharField(verbose_name = "Postal Code ",max_length=20, null=  True)
    country = models.CharField(verbose_name = "Country",max_length=50,null = True)
    phoneNumber = models.CharField(verbose_name = "Phone",max_length=20, null=  True)
    

    objects = UserManager()
    REQUIRED_FIELDS = ["firstName", "lastName"]

