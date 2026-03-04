# Ssentezo Wallet Version 2.x 🤩 API Documentation

**Ssentezo Wallet** is a platform which enables businesses and developers to collect or deliver payments to the last mile through digital platforms like mobile money.

Our simple APIs make it easy to collect your payments in a few minutes. Add our web links to your website to collect payments with zero code.

## Ssentezo Wallet Environment/MODE

The Wallet has two types of environments in which it operates:

- **LIVE**: In this environment, actual money is credited and debited from the MSISDN/phone numbers that you specify during Deposit and Withdraw operations. Real money is moved around, so be sure to have tested your application well from SANDBOX before moving into this mode.

- **SANDBOX**: This is a testing environment where no actual money is collected and disbursed. You can perform transactions just like in LIVE mode, but all these are theoretical. The MSISDN/phone numbers that you specify during Deposit and Withdraw operations will neither be credited nor debited.

In order to access **LIVE** mode, register at https://wallet.ssentezo.com/merchants/register.

In order to access **SANDBOX** mode, register at https://devwallet.ssentezo.com/merchants/register.

**NOTE**: Functionality in LIVE and SANDBOX modes is exactly the same. All that changes is the endpoint being called: `https://wallet.ssentezo.com/api` for LIVE mode and `https://devwallet.ssentezo.com/api` for SANDBOX mode.

## Authorization

The API utilizes **Auth Basic** authorization method. This requires you to possess valid API credentials which can be generated from the API Access menu in your Wallet Account.

## Limits

- API does not support entry of negative figures, exponential figures (e.g., e100), or characters while entering the amount to be transacted.
- Only transactions between **UGX 500 to UGX 7,000,000** are allowed, provided the current wallet balance can meet your charges as defined in your Ssentezo agreement.
- Charges are applicable to all transactions as specified in your contract for use of this service.

## Supported Currencies

The wallet currently supports only Uganda Shillings (UGX) for transactions.

| ISO Code | Currency Name | Status |
|----------|---------------|--------|
| UGX | Uganda Shillings | Supported |

## Setting up Authorization

Using your generated **API USER** and **API KEY**. The wallet follows a standard basic auth to secure the API where the Authorization header is sent encoded to base64.

**NOTE**: All requests must contain the authorization header.

**NOTE**: All responses are JSON-encoded strings.

**Example - How to encode the string using PHP**

```php
// Your API user
$apiUser = '';

// Your API key
$apiKey = '';

$encodedString = base64_encode($apiUser . ':' . $apiKey);

$header = ['Authorization' => 'Basic '. $encodedString];
$header = ['Content-Type' => "application/form-data"];
```

For other programming languages, follow the permitted syntax respectively.

## Expected HTTP Response Codes

These are the possible response codes that can be received in the course of the transaction.

| Status Code | Interpretation |
|-------------|----------------|
| 202 | Succeeded Transaction |
| 400 | Failed Transaction |
| 401 | No Authorization Header |
| 403 | Invalid Credentials |
| 500 | An error occurred to check the message |
| 422 | Unprocessable Entity check the request body |

## Transaction Statuses

These are the available transaction statuses that a transaction can have.

| Status | Description |
|--------|-------------|
| PENDING | Transaction still pending. All transactions begin from this state. |
| SUCCEEDED | Succeeded transaction |
| FAILED | Failed Transaction |
| INDETERMINATE | Status not yet determined. This can take up to 48hrs. |

## API Request Responses

### Successful Responses

For successful requests, a JSON object response is sent back containing two keys:

- **response**: This has a value of OK, indicating that the request was processed successfully.
- **data**: This is an object that holds any relevant data that should be returned as per the endpoint called.

**Example:**

```json
{
    "response": "OK",
    "data": {
        "amount": 1834665,
        "formatted": "1,834,665",
        "currency": "UGX"
    }
}
```

### Erroneous Responses

For erroneous responses, a JSON object response is sent back containing two keys:

- **response**: This has a value of ERROR, indicating that there was an error during the course of the request.
- **error**: This is an object that holds any relevant data to the error that just occurred. It always contains a message property that describes the error and may also have other properties relevant to that error.

**Example:**

```json
{
    "response": "ERROR",
    "error": {
        "message": "The currency field is required."
    }
}
```

## Checking the Account Balance

**Endpoint**: `https://wallet.ssentezo.com/api/acc_balance`

**Method**: `POST`

The endpoint above is accessed via the POST method. It does not require a request body, but a valid authorization header is mandatory.

### Form Data Parameters

- `currency`

**Example Request**

```json
{
    "currency": "UGX"
}
```

**Example success response**

```json
{
    "response": "OK",
    "data": {
        "amount": 1834665,
        "formatted": "1,834,665",
        "currency": "UGX"
    }
}
```

**Example error response**

```json
{
    "response": "ERROR",
    "error": {
        "message": "The currency field is required."
    }
}
```

## MSISDN/Phone Number Verification

**Endpoint**: `https://wallet.ssentezo.com/api/msisdn-verification`

**Method**: `POST`

The endpoint above is accessed via the POST method.

### Form Data Parameters

- `msisdn`

**Sample Request Body**

```json
{
    "msisdn": "256709920188"
}
```

**Sample success response**

```json
{
    "response": "OK",
    "data": {
        "msisdn": "256712345678",
        "FirstName": "John",
        "Surname": "Doe"
    }
}
```

**Sample error response**

```json
{
    "response": "ERROR",
    "error": {
        "message": "The msisdn field format is invalid."
    }
}
```

```json
{
    "response": "ERROR",
    "error": {
        "message": "Failed to verify the name of the holder of the MSISDN"
    }
}
```

## Withdrawing Funds from Your Wallet Account

**Endpoint**: `https://wallet.ssentezo.com/api/withdraw`

**Method**: `POST`

### Form Data Parameters

- `externalReference`
- `msisdn`
- `amount`
- `currency`
- `reason`
- `name` (Optional)
- `success_callback` (Optional)
- `failure_callback` (Optional)

**Example request body**

```php
// Example request body

$requestBody => [
    'externalReference' => '{your external reference}', // This should always be unique. Duplicate references will cause an error
    'msisdn' => 256770691484,
    'amount' => 2000,
    'currency' => 'UGX', // should be a valid ISO code and this currency should be supported by your wallet
    'reason' => 'Your reason for the transaction',
    'name' => '{Optional Field, You may send  the name of the recipient}',
    'success_callback' => 'https://yourapp.com/my-success-callback (Optional)', // A POST endpoint the wallet will call when a transaction is successful
    'failure_callback' => 'https://yourapp.com/my-failure-callback (Optional)', // A POST endpoint the wallet will call when a transaction has failed
];

// With PHP you can use curl, Http Request 2, or Guzzle Http to perform this request.
```

### Description

- **externalReference**: This is the string or number or reference that you use to refer to your transaction in your own application. It supports (250) characters. This should always be UNIQUE
- **msisdn**: This is a phone number formatted to international standard
- **amount**: The amount of money being transacted. It should not be formatted or contain any non-numeric characters. Amount should be between UGX 500 to UGX 7000000
- **currency**: Valid ISO format of the currency. Currently UGX is the only currency supported for transactions
- **reason**: Your reason for the transaction
- **name**: Name of the recipient
- **success_callback**: A POST endpoint the wallet will call when a transaction is successful
- **failure_callback**: A POST endpoint the wallet will call when a transaction has failed

**Example success response**

```json
{
    "response": "OK",
    "data": {
        "transactionStatus": "PENDING",
        "ssentezoWalletReference": "f245ddac-1622-4dad-9a94-4e289bb6b8a4",
        "financialTransactionId": "b997c60c6f445185fcd9a3a595533734b997c60c6f445185fcd9a3a595533734"
    }
}
```

### Description

- **transactionStatus**: Status of the transaction in our system. All transactions begin from the PENDING status
- **ssentezoWalletReference**: A unique id that we use to identify the transaction in our system
- **financialTransactionId**: A unique id that identifies your transaction at the network provider eg MTN/Airtel

**NOTE**: The financialTransactionId is the transaction reference from the Network service provider

**Example error response**

```json
{
    "response": "ERROR",
    "error": {
        "code": "UPPER_CEILING_BREACH", // Brief overview of what the error is about
        "message": "Maximum transaction amount is UGX 7,000,000" // A description of the error that occurred
    }
}
```

**Example error response (Validation)**

```json
{
    "response": "ERROR",
    "error": {
        "message": "The given data was invalid.",
        "errors": {
            "amount": ["The amount field must be at least 500."],
            "msisdn": ["The msisdn field is required."],
            "externalReference": [
                "The external reference has already been taken."
            ]
        }
    }
}
```

## Collecting Money into the Wallet (Deposit)

**Endpoint**: `https://wallet.ssentezo.com/api/deposit`

**Method**: `POST`

### Form Data Parameters

- `externalReference`
- `msisdn`
- `amount`
- `currency`
- `reason`
- `name` (Optional)
- `success_callback` (Optional)
- `failure_callback` (Optional)

**Example - Setting up a collection request**

```php
// Example request body

$requestBody => [
    'amount' => 1000,
    'msisdn' => 256770691484,
    'reason' => 'Your reason for the transaction',
    'currency' => 'UGX', // should be a valid ISO code and this currency should be supported by your wallet
    'name' => 'John Doe (Optional)', // A person's name you are collecting from
    'success_callback' => 'https://yourapp.com/my-success-callback (Optional)', // A POST endpoint the wallet will call when a transaction is successful
    'failure_callback' => 'https://yourapp.com/my-failure-callback (Optional)', // A POST endpoint the wallet will call when a transaction has failed
];

// With PHP you can use curl, Http Request 2, or Guzzle Http to perform this request.
```

**Example success response**

```json
{
    "response": "OK",
    "data": {
        "transactionStatus": "PENDING",
        "ssentezoWalletReference": "f245ddac-1622-4dad-9a94-4e289bb6b8a4",
        "financialTransactionId": "b997c60c6f445185fcd9a3a595533734b997c60c6f445185fcd9a3a595533734"
    }
}
```

**Example error response**

```json
{
    "response": "ERROR",
    "error": {
        "code": "UPPER_CEILING_BREACH", // Brief overview of what the error is about
        "message": "Maximum transaction amount is UGX 7,000,000" // A description of the error that occurred
    }
}
```

**Example error response (Validation)**

```json
{
    "response": "ERROR",
    "error": {
        "message": "The given data was invalid.",
        "errors": {
            "amount": ["The amount field must be at least 500."],
            "msisdn": ["The msisdn field is required."],
            "externalReference": [
                "The external reference has already been taken."
            ]
        }
    }
}
```

**NOTE**: A PENDING status with an HTTP status code of 202 means the transaction has been initiated and the benefactor must enter their Mobile Money Pin. Once the transaction has succeeded, the callback endpoint is then hit using a POST request to notify you.

## Checking for a Transaction Status

**Endpoint**: `https://wallet.ssentezo.com/api/get_status/{externalReference}`

**Method**: `POST`

### URL Parameters

- `externalReference`

**Sample success response**

```json
{
    "response": "OK",
    "data": {
        "transactionStatus": "SUCCEEDED",
        "ssentezoWalletReference": "3181ead4-eff9-4b9b-b926-53b41e632ca5",
        "externalReference": "rfg54rj59033w4672326hi45h6j6456",
        "financialTransactionId": "QkK0UVtkMlCZN1ZEuKVv4NU5l2sFA1uO82fb7ef5f6a2530bc5c2118b34620b5a",
        "amount": 3000,
        "reason": "Sending money to someone",
        "currency": "UGX",
        "msisdn": "256770691484",
        "transactionTime": "2024-04-24T16:24:58.000000Z"
    }
}
```

## Receiving a Transaction Status Notification

If you would like your system to be notified immediately after a transaction status changes from the PENDING status into either SUCCEEDED or FAILED statuses, you can specify callback URLs that we shall hit to notify your system.

When making a deposit or withdraw request, as part of your request data, you can pass two parameters:

- `success_callback`
- `failure_callback`

These should contain valid URLs that will be called using a POST request to your system when a transaction either succeeds or fails. Check the documentation section for DEPOSIT or WITHDRAW for an example.

**Sample of POST data sent using the success callback**

```json
{
    "response": "OK", // Indicates a successful response
    "data": {
        "transactionStatus": "SUCCEEDED", // Indicates the status of the transaction (SUCCEEDED/FAILED)
        "ssentezoWalletReference": "f245ddac-1622-4dad-9a94-4e289bb6b8a4",
        "externalReference": "16011650463271",
        "financialTransactionId": "f245ddac-1622-4dad-9a94-4e289bb6b8a4-f245ddac-1622-4dad-9a94-4e289bb6b8a4"
    }
}
```

**NOTE 1**: Please ensure that you provide valid and resolvable URLs to your system. If our system is to resolve your endpoint within 5 seconds, the request will timeout. In such cases, you will need to check the transaction status as described above.

**NOTE 2**: Please ensure that this endpoint is publicly accessible and does not require any authentication or authorization. This is because our system is decoupled from your implementation, and we rely on unrestricted callback requests to function correctly.

## Request Bank Transfer (Push Money to the Bank)

Two Endpoints: In order to Push money to the bank, two endpoints are required.

1. **Get list of banks** - This returns a list of all banks the we currently support. The bank id will be required in when making the actual request to transfer money to the bank.

2. **Request bank transfer** - After you have a list of the banks, select the bank you would like to send money to, along side with other required parameters.

### 1) Get Supported Banks

**Endpoint**: `https://wallet.ssentezo.com/api/push-to-bank/get-banks`

**Method**: `POST`

#### Form Data Parameters

Not required

**Example success response**

```json
{
    "response": "OK",
    "data": {
        "banks": [
            {
                "id": 3,
                "bank_name": "Equity",
                "address": "Church House",
                "swift_code": "QW2456"
            },
            {
                "id": 4,
                "bank_name": "Stanbic Bank",
                "address": "Church House",
                "swift_code": "QW2456"
            },
            {
                "id": 5,
                "bank_name": "Housing Finance Bank",
                "address": "Ntinda",
                "swift_code": "QWE34E"
            }
        ]
    }
}
```

### 2) Request Bank Transfer

**Endpoint**: `https://wallet.ssentezo.com/api/push-to-bank/request-bank-transfer`

**Method**: `POST`

#### Form Data Parameters

- `external_reference`
- `bank_id`
- `account_name`
- `account_number`
- `amount`
- `reason`

```php
// Example request body

$requestBody => [
    'external_reference' => c734d323-8c1c-4160-8649-4df22443aa57, // A unique identifier that you provide to our system that will be used to identify your transaction
    'bank_id' => 3, // The id of one of the banks that we support. It's obtained from the get-banks endpoint
    'account_name' => 'John Doe', // The name of the bank account you would like the funds to be transfered to
    'account_number' => '044653389534563', // The bank account number you would like the funds to be transfered to
    'amount' => '50000', // The amount of money you would like to transfer. Minimum amount is UGX 50,000
    'reason' => 'Pushing my money to the bank', // A narration about the transaction.
];

// With PHP you can use curl, Http Request 2, or Guzzle Http to perform this request.
```

**Example success response**

```json
{
    "response": "OK",
    "data": {
        "transactionStatus": "PENDING",
        "ssentezoWalletReference": "21537d54-bcd1-44a5-8614-717e093483ac",
        "externalReference": "82c7d1d6-850b-4e14-a0b7-5379058b17be"
    }
}
```

**Example error response**

```json
{
    "response": "ERROR",
    "error": {
        "message": "Minimum transaction amount is UGX 50,000"
    }
}
```

**Example error response (Validation)**

```json
{
    "response": "ERROR",
    "error": {
        "message": "The given data was invalid.",
        "errors": {
            "bank_id": [
                "The bank id field is required."
            ],
            "account_name": [
                "The account name field is required."
            ],
            "account_number": [
                "The account number field is required."
            ],
            "amount": [
                "The amount field is required."
            ]
        }
    }
}
```

### 3) Check Bank Transfer Status

**Endpoint**: `https://wallet.ssentezo.com/api/push-to-bank/check-bank-transfer-status`

**Method**: `POST`

#### Form Data Parameters

- `external_reference`

```php
// Example request body

$requestBody => [
    'external_reference' => c734d323-8c1c-4160-8649-4df22443aa57, // A unique identifier that you provide to our system that will be used to identify your transaction
];
```

**Example success response**

```json
{
    "response": "OK",
    "data": {
        "transactionStatus": "SUCCEEDED",
        "ssentezoWalletReference": "51c3d7b3-e70a-4016-8839-fe27a5c610fd",
        "externalReference": "c734d323-8c1c-4160-8649-4df22443aa57",
        "amount": 85000,
        "transactionTime": "2024-09-30T12:40:48.000000Z"
    }
}
```

**Example error response (Validation)**

```json
{
    "response": "ERROR",
    "error": {
        "message": "The given data was invalid.",
        "errors": {
            "external_reference": [
                "The selected external reference is invalid."
            ]
        }
    }
}
```

---

That's it. Go build something great 💪🏼