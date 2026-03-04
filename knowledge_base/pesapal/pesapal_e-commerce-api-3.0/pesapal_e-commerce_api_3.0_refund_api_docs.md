# Refund Request

## Definitions

The refund request endpoint allow you to refund a charge that has previously been processed but not yet refunded. Funds will be refunded to the credit / debit card or mobile money wallet that was originally charged.

The ability to process a refund has the following limitations:

1. A refund has to be approved by the merchant.
2. You can't refund more than what was originally collected.
3. You can only refund payments with the status of **COMPLETED**.
4. You can partially or fully refund a payment card payment.
5. You can only fully refund a payment mobile payment.
6. Refunds are performed in the currency of the original payment.
7. Multiple refunds are not allowed. You can only request one refund against a payment.

The URL to our RequestRefund API is either:

- **Sandbox/Demo URL:** https://cybqa.pesapal.com/pesapalv3/api/Transactions/RefundRequest
- **Production/Live URL:** https://pay.pesapal.com/v3/api/Transactions/RefundRequest

## Authentication

**Bearer Token:** Use token generated during authentication.

## HTTP Request Headers

**Accept:** The response format, which is required for operations with a response body.
**Content-Type:** The request format, which is required for operations with a request body.

| Parameter | Required | Description |
|-----------|----------|-------------|
| Accept | Required | Should be set to `application/json` |
| Content-Type | Required | Should be set to `application/json` |

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| confirmation_code | String | Required | This refers to payment confirmation code that was returned by the processor |
| amount | Float | Required | Amount to be refunded. |
| username | String | Required | Identity of the user who has initiated the refund. |
| remarks | String | Required | A brief description on the reason for the refund. |

## Sample Request

```json
{
    "confirmation_code": "AA11BB22",
    "amount": "100.00",
    "username": "John Doe",
    "remarks": "Service not offered"
}
```

After successfully placing a refund request, a request will be sent to our finance team to start processing the refund.

## Response Parameters

| Name | Type | Description |
|------|------|-------------|
| error | Integer | 200 - Refund received successfully and is being processed. 500 - Refund rejected. |
| message | String | A brief summary of the response received. |

Status **200** mean your request to process the refund has been received successfully. However, please note that this does not mean the refund has been effected. Pesapal has to get the go ahead from the merchant before finalising the refund.

Status **500** mean your request to process the refund was rejected for one reason or another. Refer to the error message for more details.

## Sample Response

```json
{
    "status": "200",
    "message": "Refund request successfully"
}
```

**Important Note:** The refund API uses the confirm code for identification. It's important that you store all payment confirmation codes as returned in the Get Transaction Status Endpoint.