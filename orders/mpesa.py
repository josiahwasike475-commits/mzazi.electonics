import base64
import datetime as dt
import os
from decimal import Decimal

import requests
from django.db import transaction

from .models import Order, PaymentAttempt


class MpesaConfigurationError(Exception):
    pass


def _settings():
    required = ["MPESA_CONSUMER_KEY", "MPESA_CONSUMER_SECRET", "MPESA_SHORTCODE", "MPESA_PASSKEY", "MPESA_CALLBACK_URL"]
    values = {key: os.getenv(key, "").strip() for key in required}
    missing = [key for key, value in values.items() if not value]
    if missing:
        raise MpesaConfigurationError(f"Daraja is not configured. Missing: {', '.join(missing)}")
    return values


def _base_url():
    return "https://api.safaricom.co.ke" if os.getenv("MPESA_ENVIRONMENT", "sandbox").lower() == "production" else "https://sandbox.safaricom.co.ke"


def _timestamp():
    return dt.datetime.now().strftime("%Y%m%d%H%M%S")


def _password(shortcode, passkey, timestamp):
    raw = f"{shortcode}{passkey}{timestamp}".encode()
    return base64.b64encode(raw).decode()


def initiate_stk_push(order: Order, phone: str):
    values = _settings()
    timestamp = _timestamp()
    auth = base64.b64encode(f"{values['MPESA_CONSUMER_KEY']}:{values['MPESA_CONSUMER_SECRET']}".encode()).decode()
    token_response = requests.get(
        f"{_base_url()}/oauth/v1/generate?grant_type=client_credentials",
        headers={"Authorization": f"Basic {auth}"},
        timeout=15,
    )
    token_response.raise_for_status()
    token = token_response.json().get("access_token")
    if not token:
        raise MpesaConfigurationError("Daraja did not return an access token.")

    amount = int(Decimal(order.total).quantize(Decimal("1")))
    payload = {
        "BusinessShortCode": values["MPESA_SHORTCODE"],
        "Password": _password(values["MPESA_SHORTCODE"], values["MPESA_PASSKEY"], timestamp),
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": values["MPESA_SHORTCODE"],
        "PhoneNumber": phone,
        "CallBackURL": values["MPESA_CALLBACK_URL"],
        "AccountReference": order.order_number,
        "TransactionDesc": "Mzazi Electronics order",
    }
    response = requests.post(
        f"{_base_url()}/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
        timeout=20,
    )
    response.raise_for_status()
    result = response.json()
    attempt = PaymentAttempt.objects.create(
        order=order,
        checkout_request_id=result.get("CheckoutRequestID"),
        merchant_request_id=result.get("MerchantRequestID", ""),
        phone=phone,
        amount=order.total,
        status="pending" if result.get("ResponseCode") == "0" else "failed",
        result_description=result.get("CustomerMessage") or result.get("ResponseDescription", ""),
    )
    return attempt, result


def process_callback(payload):
    stk = payload.get("Body", {}).get("stkCallback", {})
    checkout_id = stk.get("CheckoutRequestID")
    if not checkout_id:
        return False
    try:
        attempt = PaymentAttempt.objects.select_related("order").get(checkout_request_id=checkout_id)
    except PaymentAttempt.DoesNotExist:
        return False

    result_code = str(stk.get("ResultCode", "1"))
    with transaction.atomic():
        if attempt.status == "successful":
            return True
        attempt.raw_callback = payload
        attempt.result_description = stk.get("ResultDesc", "")
        if result_code != "0":
            attempt.status = "cancelled"
            attempt.order.payment_status = "cancelled"
        else:
            metadata = {item.get("Name"): item.get("Value") for item in stk.get("CallbackMetadata", {}).get("Item", [])}
            receipt = str(metadata.get("MpesaReceiptNumber", ""))
            amount = Decimal(str(metadata.get("Amount", "0")))
            if amount != attempt.amount:
                attempt.status = "failed"
                attempt.result_description = "Callback amount did not match the order total."
                attempt.order.payment_status = "failed"
            else:
                attempt.status = "successful"
                attempt.mpesa_receipt = receipt
                attempt.order.mpesa_receipt = receipt
                attempt.order.payment_status = "successful"
                attempt.order.status = "confirmed"
        attempt.save()
        attempt.order.save(update_fields=["payment_status", "mpesa_receipt", "status", "updated_at"])
    return True
