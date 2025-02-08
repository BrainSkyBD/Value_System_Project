from django.db import models
from authenticationApp.models import User
import uuid
from ckeditor.fields import RichTextField
# Create your models here.
from django.db.models import Sum, F, Q 

    
class CompanyDetailsTable(models.Model):
    class Meta:
        verbose_name_plural = "Company Table"
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Subscription_Option = (
        ('Starter', 'Starter'),
        ('Company', 'Company'),
        ('Enterprise', 'Enterprise'),
    )
    Subscription = models.CharField(max_length=255, choices=Subscription_Option, default='Starter')
    Company_Id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False)
    Company_Legal_Name = models.CharField(max_length=255)
    Company_Type_Option = (
        ('Owner', 'Owner'),
        ('Construction Management', 'Construction Management'),
        ('Main Contractor', 'Main Contractor'),
        ('Subcontractor', 'Subcontractor'),
    )
    Company_Type = models.CharField(max_length=255, choices=Company_Type_Option, default='Owner')
    Email = models.CharField(max_length=255, null=True, blank=True)
    Telephone = models.CharField(max_length=255, null=True, blank=True)
    Country = models.CharField(max_length=255, null=True, blank=True)
    Address = models.CharField(max_length=255, null=True, blank=True)
    Company_Website = models.CharField(max_length=255, null=True, blank=True)
    Tax_Identification_Number = models.CharField(max_length=255, null=True, blank=True)
    Primary_Contact_Person = models.CharField(max_length=255, null=True, blank=True)
    Company_Logo = models.ImageField(upload_to='Company_Logo/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





class ProjectTable(models.Model):
    class Meta:
        verbose_name_plural = "Project Table"
    Company_Details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True)
    Project_Id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False)
    Project_Name = models.CharField(max_length=255)
    Project_Start_Date = models.DateField(null=True)
    Short_Description = RichTextField(null=True, blank=True)
    Default_Workflow = models.CharField(max_length=255, null=True, blank=True)
    Note_book = models.CharField(max_length=255, null=True, blank=True)
    Assigned_User = models.ManyToManyField(User, related_name="project_assigned_user", default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Resource_Code_L1_Table(models.Model):
    class Meta:
        verbose_name = "Resource Code Level 1"
        verbose_name_plural = "Resource Codes Level 1"
    Company_Details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True)
    Resource_Code_L1 = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def total_expense_quantity_calculation(self):
        from expenseApp.models import ExpenseTable
        filter_expenses = ExpenseTable.objects.filter(
            Company_Details=self.Company_Details,
            resource_value__Resource_Code_L1=self
        )
        quantity = filter_expenses.aggregate(Sum('quantity'))['quantity__sum'] or 0
        return round(quantity, 2)

    def total_expense_quantity_calculation_price(self):
        from expenseApp.models import ExpenseTable
        filter_expenses = ExpenseTable.objects.filter(
            Company_Details=self.Company_Details,
            resource_value__Resource_Code_L1=self
        )
        total_cost = filter_expenses.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        return round(total_cost, 2)


    def total_stock_in_calculation(self):
        print('level3')
        from storeApp.models import StoreTable
        stock_entries = StoreTable.objects.filter(
            Company_Details=self.Company_Details,
            stock_trasaction_status='Stock-In',
            resource_value__Resource_Code_L1=self
        )
        quantity = stock_entries.aggregate(Sum('quantity'))['quantity__sum'] or 0
        return round(quantity, 2)

    def total_stock_out_calculation(self):
        from storeApp.models import StoreTable
        stock_entries = StoreTable.objects.filter(
            Company_Details=self.Company_Details,
            stock_trasaction_status='Stock-Out',
            resource_value__Resource_Code_L1=self
        )
        quantity = stock_entries.aggregate(Sum('quantity'))['quantity__sum'] or 0
        return round(quantity, 2)

    def calculate_stock_availablity(self):
        total_stock_in = self.total_stock_in_calculation()
        total_stock_out = self.total_stock_out_calculation()
        return total_stock_in - total_stock_out

    def total_stock_in_calculation_price(self):
        from storeApp.models import StoreTable
        stock_entries = StoreTable.objects.filter(
            Company_Details=self.Company_Details,
            stock_trasaction_status='Stock-In',
            resource_value__Resource_Code_L1=self
        )
        total_cost = stock_entries.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        return round(total_cost, 2)

    def total_stock_out_calculation_price(self):
        from storeApp.models import StoreTable
        stock_entries = StoreTable.objects.filter(
            Company_Details=self.Company_Details,
            stock_trasaction_status='Stock-Out',
            resource_value__Resource_Code_L1=self
        )
        total_cost = stock_entries.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        return round(total_cost, 2)

    def filter_resource_level_2_list(self):
        filter_resource_level_2 = Resource_Code_L2_Table.objects.filter(Resource_Code_L1=self)
        return filter_resource_level_2


class Resource_Code_L2_Table(models.Model):
    class Meta:
        verbose_name = "Resource Code Level 2"
        verbose_name_plural = "Resource Codes Level 2"
    Company_Details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True)
    Resource_Code_L1 = models.ForeignKey(Resource_Code_L1_Table, on_delete=models.CASCADE, null=True, blank=True)
    Resource_Code_L2 = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_expense_quantity_calculation(self):
        from expenseApp.models import ExpenseTable
        filter_expenses = ExpenseTable.objects.filter(
            Company_Details=self.Company_Details,
            resource_value__Resource_Code_L2=self
        )
        quantity = filter_expenses.aggregate(Sum('quantity'))['quantity__sum'] or 0
        return round(quantity, 2)

    def total_expense_quantity_calculation_price(self):
        from expenseApp.models import ExpenseTable
        filter_expenses = ExpenseTable.objects.filter(
            Company_Details=self.Company_Details,
            resource_value__Resource_Code_L2=self
        )
        print('expense level2')
        print(filter_expenses)
        total_cost = filter_expenses.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        return round(total_cost, 2)



    def total_stock_in_calculation(self):
        print('level3')
        from storeApp.models import StoreTable
        stock_entries = StoreTable.objects.filter(
            Company_Details=self.Company_Details,
            stock_trasaction_status='Stock-In',
            resource_value__Resource_Code_L2=self
        )
        quantity = stock_entries.aggregate(Sum('quantity'))['quantity__sum'] or 0
        return round(quantity, 2)

    def total_stock_out_calculation(self):
        from storeApp.models import StoreTable
        stock_entries = StoreTable.objects.filter(
            Company_Details=self.Company_Details,
            stock_trasaction_status='Stock-Out',
            resource_value__Resource_Code_L2=self
        )
        quantity = stock_entries.aggregate(Sum('quantity'))['quantity__sum'] or 0
        return round(quantity, 2)

    def calculate_stock_availablity(self):
        total_stock_in = self.total_stock_in_calculation()
        total_stock_out = self.total_stock_out_calculation()
        return total_stock_in - total_stock_out

    def total_stock_in_calculation_price(self):
        from storeApp.models import StoreTable
        stock_entries = StoreTable.objects.filter(
            Company_Details=self.Company_Details,
            stock_trasaction_status='Stock-In',
            resource_value__Resource_Code_L2=self
        )
        total_cost = stock_entries.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        return round(total_cost, 2)

    def total_stock_out_calculation_price(self):
        from storeApp.models import StoreTable
        stock_entries = StoreTable.objects.filter(
            Company_Details=self.Company_Details,
            stock_trasaction_status='Stock-Out',
            resource_value__Resource_Code_L2=self
        )
        total_cost = stock_entries.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        return round(total_cost, 2)
    
    def filter_resource_level_3_list(self):
        filter_resource_level_3 = Resource_Code_L3_Table.objects.filter(Resource_Code_L2=self)
        return filter_resource_level_3


class Resource_Code_L3_Table(models.Model):
    class Meta:
        verbose_name = "Resource Code Level 3"
        verbose_name_plural = "Resource Codes Level 3"
    Company_Details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True)
    Resource_Code_L1 = models.ForeignKey(Resource_Code_L1_Table, on_delete=models.CASCADE, null=True, blank=True)
    Resource_Code_L2 = models.ForeignKey(Resource_Code_L2_Table, on_delete=models.CASCADE, null=True, blank=True)
    Resource_Code_L3 = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def total_expense_quantity_calculation(self):
        from expenseApp.models import ExpenseTable
        filter_expenses = ExpenseTable.objects.filter(
            Company_Details=self.Company_Details,
            resource_value__Resource_Code_L3=self
        )
        quantity = filter_expenses.aggregate(Sum('quantity'))['quantity__sum'] or 0
        return round(quantity, 2)

    def total_expense_quantity_calculation_price(self):
        from expenseApp.models import ExpenseTable
        filter_expenses = ExpenseTable.objects.filter(
            Company_Details=self.Company_Details,
            resource_value__Resource_Code_L3=self
        )
        total_cost = filter_expenses.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        return round(total_cost, 2)

    def total_stock_in_calculation(self):
        print('level3')
        from storeApp.models import StoreTable
        stock_entries = StoreTable.objects.filter(
            Company_Details=self.Company_Details,
            stock_trasaction_status='Stock-In',
            resource_value__Resource_Code_L3=self
        )
        quantity = stock_entries.aggregate(Sum('quantity'))['quantity__sum'] or 0
        return round(quantity, 2)

    def total_stock_out_calculation(self):
        from storeApp.models import StoreTable
        stock_entries = StoreTable.objects.filter(
            Company_Details=self.Company_Details,
            stock_trasaction_status='Stock-Out',
            resource_value__Resource_Code_L3=self
        )
        quantity = stock_entries.aggregate(Sum('quantity'))['quantity__sum'] or 0
        return round(quantity, 2)

    def calculate_stock_availablity(self):
        total_stock_in = self.total_stock_in_calculation()
        total_stock_out = self.total_stock_out_calculation()
        return total_stock_in - total_stock_out

    def total_stock_in_calculation_price(self):
        from storeApp.models import StoreTable
        stock_entries = StoreTable.objects.filter(
            Company_Details=self.Company_Details,
            stock_trasaction_status='Stock-In',
            resource_value__Resource_Code_L3=self
        )
        total_cost = stock_entries.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        return round(total_cost, 2)

    def total_stock_out_calculation_price(self):
        from storeApp.models import StoreTable
        stock_entries = StoreTable.objects.filter(
            Company_Details=self.Company_Details,
            stock_trasaction_status='Stock-Out',
            resource_value__Resource_Code_L3=self
        )
        total_cost = stock_entries.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        return round(total_cost, 2)


class CompanyResourcesTable(models.Model):
    class Meta:
        verbose_name_plural = "Company Resources Table"
    Company_Details = models.ForeignKey(CompanyDetailsTable, on_delete=models.CASCADE, null=True, blank=True)
    Resource_Title = models.CharField(max_length=255, null=True, blank=True, default=None)
    Resource_Name = models.CharField(max_length=255, null=True, blank=True)
    Resource_Code_L1 = models.ForeignKey(Resource_Code_L1_Table, on_delete=models.CASCADE, null=True, blank=True)
    Resource_Code_L2 = models.ForeignKey(Resource_Code_L2_Table, on_delete=models.CASCADE, null=True, blank=True)
    Resource_Code_L3 = models.ForeignKey(Resource_Code_L3_Table, on_delete=models.CASCADE, null=True, blank=True)
    Unit_of_Measure = models.CharField(max_length=255, null=True, blank=True)
    Budget_Unit_Cost = models.CharField(max_length=255, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    
    def total_expense_quantity_calculation(self):
        from expenseApp.models import ExpenseTable
        filter_expenses = ExpenseTable.objects.filter(resource_value=self, Company_Details=self.Company_Details)
        quantity = filter_expenses.aggregate(Sum('quantity'))['quantity__sum'] or 0
        return round(quantity, 2)

    def total_expense_quantity_calculation_price(self):
        from expenseApp.models import ExpenseTable
        filter_expenses = ExpenseTable.objects.filter(resource_value=self, Company_Details=self.Company_Details)
        total_cost = filter_expenses.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        return round(total_cost, 2)


    def total_stock_in_calculation(self):
        from storeApp.models import StoreTable
        company = self.Company_Details
        store_entries = StoreTable.objects.filter(resource_value=self, Company_Details=company, stock_trasaction_status='Stock-In')
        quantity = store_entries.aggregate(Sum('quantity'))['quantity__sum'] or 0
        return round(quantity, 2)

    
    def total_stock_out_calculation(self):
        from storeApp.models import StoreTable
        company = self.Company_Details
        store_entries = StoreTable.objects.filter(resource_value=self, Company_Details=company, stock_trasaction_status='Stock-Out')
        quantity = store_entries.aggregate(Sum('quantity'))['quantity__sum'] or 0
        return round(quantity, 2)

    
    def calculate_stock_availablity(self):
        total_stock_in_calculation = self.total_stock_in_calculation()
        total_stock_out_calculation = self.total_stock_out_calculation()
        stock_availability = total_stock_in_calculation - total_stock_out_calculation
        return stock_availability


    def total_stock_in_calculation_price(self):
        from storeApp.models import StoreTable
        company = self.Company_Details
        store_entries = StoreTable.objects.filter(resource_value=self, Company_Details=company, stock_trasaction_status='Stock-In')
        total_cost = store_entries.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        return round(total_cost, 2)

    
    def total_stock_out_calculation_price(self):
        from storeApp.models import StoreTable
        company = self.Company_Details
        store_entries = StoreTable.objects.filter(resource_value=self, Company_Details=company, stock_trasaction_status='Stock-Out')
        total_cost = store_entries.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
        return round(total_cost, 2)


    