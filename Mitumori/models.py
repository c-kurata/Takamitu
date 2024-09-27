from django.db import models

class Department(models.Model):
    department_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department_name

class Employee(models.Model):
    employee_name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employee_name

class Estimate(models.Model):
    estimate_name = models.CharField(max_length=255)
    submit_to_name = models.CharField(max_length=255)
    estimate_amount = models.DecimalField(max_digits=10, decimal_places=2)
    summary = models.TextField()
    created_by = models.ForeignKey(Employee, related_name='created_estimates', on_delete=models.CASCADE)
    last_updated_by = models.ForeignKey(Employee, related_name='updated_estimates', on_delete=models.CASCADE)
    admin_approval_status = models.CharField(max_length=50, choices=[('', '選択してください'), ('承認', '承認'), ('未承認', '未承認')])
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    submission_date = models.DateField()
    attachment = models.FileField(upload_to='attachments/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.estimate_name
