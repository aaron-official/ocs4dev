# IPN URL Registration

## IPN URL Registration Endpoint - Post Request

**IPN** stands for **Instant Payment Notification**. When a payment is made against a transaction, Pesapal will trigger an IPN call to the notification URL related to this transaction. This notification URL is usually located on your servers. These notifications allows you to be alerted in real time whenever there is a status change for any transaction.

An IPN is particular important as it allows you to be notified incase the following happens:

- Your client gets disconnected after payment due to internet issues
- Your client experiences server errors hence Pesapal and your application gets disconnected before callback URL is loaded
- Your client exits your application / closes the browser during payment
- The transaction is rejected

As such, it's mandatory to have IPN configured to allow Pesapal to notify your servers when a status changes. It's also important to note that this **IPN URL must be publicly available**. In cases where you have strict server rules preventing external systems reaching your end, you must then whitelist all calls from our domain (pesapal.com). Please be informed that IP whitelisting is not feasible as our IP may change without notice.

Before sending Submit Order Requests to Pesapal API 3.0, you are expected to register your IPN URL. Upon registration, you receive an **IPN ID** which is a mandatory field (**notification_id**) when submitting an order request to Pesapal API 3.0. This **notification_id** uniquely identifies the endpoint Pesapal will send alerts to whenever a payment status changes for each transaction processed via API 3.0

The URL to our IPN registration API is either:

- **Sandbox/Demo URL:** https://cybqa.pesapal.com/pesapalv3/api/URLSetup/RegisterIPN
- **Production/Live URL:** https://pay.pesapal.com/v3/api/URLSetup/RegisterIPN

## Authentication

**Bearer Token:** Use token generated during authentication.

## HTTP Request Headers

**Accept:** The response format, which is required for operations with a response body.
**Content-Type:** The request format, which is required for operations with a request body.

| Parameter | Required | Description |
|-----------|----------|-------------|
| Accept | Required | Should be set to application/json |
| Content-Type | Required | Should be set to application/json |

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| url | String | Required | The notification url Pesapal with send a status alert to. |
| ipn_notification_type | String | Required | GET or POST. This is the http request method Pesapal will use when triggering the IPN alert. |

## Sample Request

```json
{
    "url": "https://www.myapplication.com/ipn",
    "ipn_notification_type": "GET"
}
```

## Response Parameters

| Name | Description |
|------|-------------|
| url | The notification url Pesapal will send a status alert to. |
| created_date | Date and time the IPN URL was registered UTC |
| ipn_id | A unique identifier that's linked to the IPN endpoint URL. GUID |
| notification_type | 1 or 0 |
| ipn_notification_type_description | The http request method you registered your IPN url as |
| ipn_status | 1 or 0 ie Active or Inactive |
| ipn_status_decription | Status description ie Active or Inactive |
| error | An error object containing error_type, code and message if any. Null to signify no error. |
| status | Response code. |

## Sample Response

```json
{
    "url": "https://myapplication.com/ipn",
    "created_date": "2024-06-14T07:50:22.2825997Z",
    "ipn_id": "84740ab4-3cd9-47da-8a4f-dd1db53494b5",
    "notification_type": 0,
    "ipn_notification_type_description": "GET",
    "ipn_status": 1,
    "ipn_status_description": "Active",
    "error": null,
    "status": "200"
}
```

## Alternative Registration Methods

You can also use our online forms below to register your IPN URLs:

- **Sandbox/Demo IPN Registration Form**
- **Production/Live IPN Registration Form**