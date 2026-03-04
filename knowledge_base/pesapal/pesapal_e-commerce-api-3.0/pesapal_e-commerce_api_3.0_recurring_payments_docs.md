# Pesapal Recurring / Subscription Based Payments

## Definitions

**Recurring payment** is a payment model where customers authorize the business to pull funds from their accounts automatically at regular intervals for the goods and services provided to them on an ongoing basis.

With Pesapal's subscription based payments, customers can set automated card payments on their account where they can be debited automatically at a different set times. Examples of services one can enroll to include cable bills, cell phone bills, gym membership fees, utility bills and magazine subscriptions. These payments can be set to run an various intervals such as daily, weekly, monthly or yearly.

## How can recurring payments benefit your business?

- **Saves customers time**: Customers no longer have to go through the payment process every time they need to make a payment.
- **Ensures prompt payment**: Businesses no longer need to worry about getting paid on time. Since the payments are automated, they no longer need to send out overdue payment reminders.
- **Boosts customer loyalty**: With a subscription model, businesses can form closer relationships with their customers.
- **Cash flow prediction**: Businesses can easily predict their cash flow, which helps with business strategy.
- **Lowers billing and collection costs**: Businesses no longer need to chase after missed payments, freeing up their time to concentrate on other elements of the business.

## How do I enable recurring payment for my customers?

Enable our subscription based payments by passing an additional **account_number** field when sending data to our **SubmitOrderRequest** endpoint. This account_number should relate to an account number / invoice number that helps you identify the payment.

**Note**: It's critical that you get to understand all other Pesapal API 3.0 endpoints before implementing the recurring feature.

In addition to the **SubmitOrderRequest** parameters, include one more param as shown below.

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| account_number | Optional | Customer's identification number known to your system. This can be an invoice number or an account number. |

### Sample Request

```json
{
    "id": "AA1122-3344ZZ",
    "currency": "KES",
    "amount": 100.00,
    "description": "Payment description goes here",
    "callback_url": "https://www.myapplication.com/response-page",
    "notification_id": "fe078e53-78da-4a83-aa89-e7ded5c456e6",
    "billing_address": {
        "email_address": "john.doe@example.com",
        "phone_number": "0723xxxxxx",
        "country_code": "KE",
        "first_name": "John",
        "middle_name": "",
        "last_name": "Doe",
        "line_1": "Pesapal Limited",
        "line_2": "",
        "city": "",
        "state": "",
        "postal_code": "",
        "zip_code": ""
    },
    "account_number": "555-678"
}
```

After successfully processing your request using the **SubmitOrderRequest** endpoint, the customer will be shown an option to opt into the recurring model on the Pesapal iframe during payment. The customer will then configure the frequency (Daily, weekly, monthly, quarterly or yearly), set a start and enddate, and finally enter an amount to be automatically deducted from their card on each payment cycle.

Once the customer has made a successful payment, Pesapal will automatically create a scheduled subscription on their behalf and an email alert will be sent to the provided card billing email that was used during the payment process, notifying them of the newly created subscription together with a link they can access a dashboard to manage their subscription.

**Pesapal will NOT store the customer's card details.** Instead, Pesapal has implemented the **card tokenization technology**.

**Credit card tokenization** is the process of de-identifying sensitive cardholder data by converting it to a string of randomly generated numbers called a "token." Similar to encryption, tokenization obfuscates the original data to render it unreadable to a user. Unlike encryption, however, credit card tokenization is irreversible.

## Is it possible to send the extra subscription parameters (Frequency, amount, period) via the API?

Yes, in cases where your application already handles the process where the customer opts into a subscription based model from your application, Pesapal allows you to send these extra parameters via the API. This ensures that the user does not have to fill in the same details again (on your application and on the Pesapal Iframe).

However, it's important to note that the customer **MUST accept to enroll to your subscription on the iframe**. They will however not be able to edit the subscription details on the iframe.

In addition to the **account_number** parameter included in the **SubmitOrderRequest**, you are required to send the following parameter.

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| subscription_details | Optional | Customer Subscription Object You can pass subscription data to Pesapal allowing a user to setup recurring payment. |

### Subscription Object

| Name | Type | Required | Description |
|------|------|----------|-------------|
| start_date | String | Mandatory | Your subscription's start date in the format dd-MM-yyyy e.g 24-01-2023 representing 24th Jan 2023 |
| end_date | String | Mandatory | Your subscription's end date in the format dd-MM-yyyy e.g 31-12-2023 representing 31st Dec 2023 |
| frequency | String | Mandatory | The period billed to the account is set out in the user contract. For instance, if users subscribe to a monthly service. Accepted values include DAILY, WEEKLY, MONTHLY or YEARLY |

### Sample Request

```json
{
    "id": "AA1122-3344ZZ",
    "currency": "KES",
    "amount": 100.00,
    "description": "Payment description goes here",
    "callback_url": "https://www.myapplication.com/response-page",
    "notification_id": "fe078e53-78da-4a83-aa89-e7ded5c456e6",
    "billing_address": {
        "email_address": "john.doe@example.com",
        "phone_number": "0723xxxxxx",
        "country_code": "KE",
        "first_name": "John",
        "middle_name": "",
        "last_name": "Doe",
        "line_1": "Pesapal Limited",
        "line_2": "",
        "city": "",
        "state": "",
        "postal_code": "",
        "zip_code": ""
    },
    "account_number": "555-678",
    "subscription_details": {
        "start_date": "24-01-2023",
        "end_date": "31-12-2023",
        "frequency": "DAILY"
    }
}
```

After successfully processing your request using the **SubmitOrderRequest** endpoint, the customer will be shown an option to opt into the recurring model on the Pesapal iframe during payment. The iframe will this time load without the options to re-select the Frequency, period and dates.

## Can a customer opt out of recurring payments before the end date?

Yes, customers have the right to cancel their subscription at anytime. Pesapal will send them email alerts a day or two prior to charging their cards. This ensures customers are always aware of all upcoming charges giving them the freedom to opt out or pausing their subscriptions.

## Which cards are currently supported?

We currently support **Visa** and **MasterCard** for recurring payments. More card options will be enabled in the near future.

## How will Pesapal alert my business about successful recurring payments?

Once a schedule is created and executed successfully, Pesapal will trigger an **IPN (Instant Payment Notification)** to the IPN endpoint you provided when calling the **SubmitOrderRequest** endpoint. This IPN call will have the **OrderNotificationType** set as **RECURRING**.

**Sample IPN URL**: 
```
https://www.myapplication.com/response-page?OrderTrackingId=b945e4af-80a5-4ec1-8706-e03f8332fb04&OrderMerchantReference=555-678&OrderNotificationType=RECURRING
```

### Recurring IPN Details

The IPN alert will either be a **GET** or **POST** request, depending on which HTTP method you selected when registering the IPN URL.

The IPN call will have the following parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| OrderTrackingId | String | Unique order id generated by Pesapal. |
| OrderNotificationType | String | Value set as RECURRING to represent a Recurring IPN call. |
| OrderMerchantReference | String | Your account number received as part of the SUBMIT ORDER REQUEST. |

The IPN call will **NOT** have all details of the payment for security reasons. As such, you will be required to fetch the payment using the **GetTransactionStatus API** once the IPN URL is triggered.

In addition to the normal payment status details received from the **GetTransactionStatus** endpoint, Pesapal will append an object **subscription_transaction_info** containing some additional recurring payment data.

### Recurring Payments Extra Data (subscription_transaction_info)

| Name | Description |
|------|-------------|
| account_reference | Customer's identification number known to your system. This can be an invoice number or an account number. |
| amount | Amount paid by the customer. |
| first_name | Customer's first name. |
| last_name | Customer's last name. |
| correlation_id | Pesapal's unique recurring payment identifier / id. |

### Sample Response

```json
{
    "payment_method": "Visa",
    "amount": 100,
    "created_date": "2022-04-30T07:41:09.763",
    "confirmation_code": "6513008693186320103009",
    "payment_status_description": "Failed",
    "description": "Unable to Authorize Transaction.Kindly contact your bank for assistance",
    "message": "Request processed successfully",
    "payment_account": "476173**0010",
    "call_back_url": "https://test.com/?OrderTrackingId=7e6b62d9-883e-440f-a63e-e1105bbfadc3&OrderMerchantReference=555-678",
    "status_code": 2,
    "merchant_reference": "1515111111",
    "payment_status_code": "",
    "currency": "KES",
    "subscription_transaction_info": {
        "account_reference": "555-678",
        "amount": 100,
        "first_name": "John",
        "last_name": "Doe",
        "correlation_id": 111222
    },
    "error": {
        "error_type": null,
        "code": null,
        "message": null,
        "call_back_url": null
    },
    "status": "200"
}
```

## What Next?

Once you've fetched the recurring data, you are then required to store the same in your system and provide services / goods as subscribed.

Your IPN endpoint should then respond to Pesapal with a json string confirming service delivery. Part of the json string contains a **status** parameter that should be set as **200** (meaning request was received and processed) or **500** (meaning request was received but there was an issue providing the services).

**Sample JSON Response String**: 
```json
{
    "orderNotificationType": "RECURRING",
    "orderTrackingId": "d0fa69d6-f3cd-433b-858e-df86555b86c8",
    "orderMerchantReference": "555-678",
    "status": 200
}
```

**NB**: Constant complaints from your customers about service / goods not delivered which were paid using recurring / subscription based payment mode will lead to the subscriptions being terminated and your profile banned from using the feature.