import time
import json
import uuid
import random
import redis
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Simulates high-frequency banking transactions pushing into Redis Stream'

    def handle(self, *args, **kwargs):
        r = redis.Redis(host='localhost', port=6379, db=0)
        locations = ['Chennai, IN', 'Mumbai, IN', 'New York, US', 'London, UK', 'Tokyo, JP']
        devices = ['iOS-App', 'Android-App', 'Web-Browser', 'ATM-Terminal']

        self.stdout.write(self.style.SUCCESS('[RUNNING] Transaction Generator Started...'))
        
        while True:
            # 10% chance to generate high risk values
            is_suspicious = random.random() < 0.10
            
            payload = {
                "transaction_id": str(uuid.uuid4())[:12],
                "sender_account": f"ACC{random.randint(1000, 9999)}",
                "receiver_account": f"ACC{random.randint(1000, 9999)}",
                "amount": round(random.uniform(1500, 5000) if is_suspicious else random.uniform(10, 300), 2),
                "location_risk": 1 if is_suspicious else random.choice([0, 1]),
                "device_risk": 1 if is_suspicious else random.choice([0, 1]),
                "location": random.choice(locations),
                "device_info": random.choice(devices)
            }

            r.xadd("transaction_stream", {"data": json.dumps(payload)})
            self.stdout.write(f"Pushed: {payload['transaction_id']} | Amount: ${payload['amount']}")
            time.sleep(1.5)