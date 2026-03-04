# Wireless Connectivity

Achieving seamless integration with your Point of Sale (POS) is possible through wireless transmission of payment details to your designated endpoint.

The initiation of this request will originate from the pqd devices, and upon a successful transaction, the relevant information will be transmitted to your specified endpoint, allowing you to efficiently settle the bill on your end.

This guide explains the process through which merchants can obtain transactional data after customers make payments on the Sabi terminal.

To facilitate the reception of payments within their external systems, merchants are required to furnish us with a secure URL featuring SSL encryption. Pesapal, in turn, will initiate an HTTP POST request to the merchant system, posting the transaction details with the specified parameters.

## Request Parameters

| Parameter | Data Type | Description | Example |
|-----------|-----------|-------------|---------|
| first_name | String | Represent the first name of the customer | John |
| last_name | String | Represents the last name of the customer | Doe |
| phone | String | Represents the phone number of the customer if provided | 0712345678 |
| amount | Decimal | Represents the amount paid by the customer | 1.00 |
| payment_option | String | Represent the payment option used by the customer eg. Visa, MasterCard, Mpesa | Visa |
| transaction_date | datetime | Represents date and time when the transaction was done | 2019-08-14T14:41:21.4612553Z |
| currency | String | Represents the currency used during the transaction | KES, USD |
| merchant_reference | String | Represents the merchant reference in case it was entered by the merchant | 1234 |
| id | int | Represents Pesapal unique ID | 12 |
| confirmation_code | String | Represents either confirmation of payment code for mpesa and cards | QWE1234 |

## Sample Request

```json
{
  "id": 10463,
  "first_name": "joe",
  "last_name": "doe",
  "phone": "+254712345678",
  "amount": 1.0,
  "payment_option": "Visa",
  "transaction_date": "2022-02-04T14:19:05.0210431Z",
  "currency": "KES",
  "merchant_reference": "TEST",
  "confirmation_code": "test10"
}
```

## Sample Response

```json
{
  "status": "200",
  "message": "Ok"
}
```

**NB:** For a tailored solution corresponding to the above payload, please reach out to developer@pesapal.com. Our dedicated team is ready to provide assistance and support.