import json
import redis
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.management.base import BaseCommand
from analytics.models import Transaction
from ml_engine.predict import evaluate_transaction

class Command(BaseCommand):
    help = 'Consumes transactions from Redis Stream, runs ML inference, saves & broadcasts.'

    def handle(self, *args, **kwargs):
        r = redis.Redis(host='localhost', port=6379, db=0)
        channel_layer = get_channel_layer()
        last_id = '$'

        self.stdout.write(self.style.SUCCESS('[RUNNING] Stream Inference Consumer Active...'))

        while True:
            response = r.xread({"transaction_stream": last_id}, count=1, block=0)
            for stream_name, messages in response:
                for msg_id, data in messages:
                    last_id = msg_id
                    raw_data = json.loads(data[b'data'].decode('utf-8'))
                    
                    # Run Hybrid ML Engine
                    ml_result = evaluate_transaction(
                        amount=raw_data['amount'],
                        device_risk=raw_data['device_risk'],
                        location_risk=raw_data['location_risk']
                    )

                    # Persist record in DB
                    tx_obj = Transaction.objects.create(
                        transaction_id=raw_data['transaction_id'],
                        sender_account=raw_data['sender_account'],
                        receiver_account=raw_data['receiver_account'],
                        amount=raw_data['amount'],
                        location=raw_data['location'],
                        device_info=raw_data['device_info'],
                        fraud_risk_score=ml_result['fraud_risk_score'],
                        is_fraud=ml_result['is_fraud']
                    )

                    broadcast_payload = {
                        "id": tx_obj.id,
                        "transaction_id": tx_obj.transaction_id,
                        "sender_account": tx_obj.sender_account,
                        "receiver_account": tx_obj.receiver_account,
                        "amount": tx_obj.amount,
                        "location": tx_obj.location,
                        "device_info": tx_obj.device_info,
                        "fraud_risk_score": tx_obj.fraud_risk_score,
                        "is_fraud": tx_obj.is_fraud,
                        "timestamp": tx_obj.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    }

                    # Broadcast through Django Channels WebSocket
                    async_to_sync(channel_layer.group_send)(
                        "fraud_alerts",
                        {
                            "type": "send_fraud_alert",
                            "data": broadcast_payload
                        }
                    )
                    
                    print(f"[PROCESSED] Tx: {tx_obj.transaction_id} | Score: {tx_obj.fraud_risk_score} | Fraud: {tx_obj.is_fraud}")