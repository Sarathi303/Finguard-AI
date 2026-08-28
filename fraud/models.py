from django.db import models

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=64, unique=True)
    sender_account = models.CharField(max_length=32)
    receiver_account = models.CharField(max_length=32)
    amount = models.FloatField()
    location = models.CharField(max_length=64)
    device_info = models.CharField(max_length=64)
    fraud_risk_score = models.FloatField()
    is_fraud = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_id} - Score: {self.fraud_risk_score}"