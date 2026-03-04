# MoMo Open APIs SandBox Documentation

MTN MoMo Open APIs are a set of APIs that allow third-party developers to create innovative digital financial services using MTN Mobile Money platform.

These APIs facilitate all key use cases including consumer to business payments (C2B), business to business payments (B2B), collections, and disbursements, Cash In, Cash Out, Refund, Notification and more.

MoMo APIs are completely RESTful and all our responses are returned in JSON.

## Generate Subscription Keys

1. Sign up at https://momodeveloper.mtn.com
2. Navigate to the products page Product-descriptions
3. Select drop down on product that suits the business case and subscribe
4. After completion, you can locate the Subscription Keys in your profile

**Configure the Environment variables as shown below**

| Subscription name | Key Type | Variable |
|------------------|----------|----------|
| Disbursements | Primary | {{Disbursement_Subscription-Key}} |
| Collections | Primary | {{Collection_Subscription-Key}} |

## Fork the MoMo Open API Postman Collection

Ensure the Environment is set to sandbox before running the collection.

The Collections and Folders have been configured with basic testing scripts to help narrow down the error scope.

## Generate API User and Key SandBox

Run the below request to generate API user and Key. These will be auto saved within the environment leveraging on scripting.

## Test MSISDN Numbers

In the Sandbox, adjust the Test Numbers(MSISDN) within the sandbox environment as follows.

Each numeric string yields a distinct response status within the Sandbox.

For Production, Number begins with the country code.

| Number - {{MSISDN}} | Expected Status Response |
|---------------------|-------------------------|
| 46733123450 | Failed |
| 46733123451 | Rejected |
| 46733123452 | Timeout |
| 56733123453 | Success |
| 46733123454 | Pending |

## Authorization

Consists of Bearer Access Token API, This is also saved within the environment, will refresh once its time has expired, 60 minutes.

### Generate access_token

**Endpoint:** `POST {{base_url}}/collection/token/`

The POST /collection/token/ endpoint is used to obtain a token.

**Request Body**
No request body parameters required for this request.

**Response**
Upon a successful request, the response will be a JSON object with the following properties:

- **access_token** (string): The access token obtained
- **token_type** (string): The type of token obtained
- **expires_in** (integer): The duration in seconds for which the token is valid

**Headers**
No specific headers are required for this request.

**Example response:**

```json
{
  "access_token": "",
  "token_type": "",
  "expires_in": 0
}
```

**Authorization**
- Basic Auth
- Username: `{{api_user}}`
- Password: `{{api_key}}`

**Example Request**

```bash
curl --location --globoff --request POST '{{base_url}}/collection/token/' \
--header 'Ocp-Apim-Subscription-Key: {{Collection_Subscription-Key}}' \
--data ''
```

**Example Response**

```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSMjU2In0.eyJjbGllbnRJZCI6IjA0ZGIwYjk5LTkyNmYtNGQ0Ni04YzI3LTQ2OWIwMmMxZWUxMyIsImV4cGlyZXMiOiIyMDI0LTEwLTA4VDIxOjI1OjI3LjgwNyIsInNlc3Npb25JZCI6IjVhODkwODJlLTk3NmQtNGYwMy04OTNjLTJlNTEwNWI1YWM5NiJ9.hAmAJFZkdyhuEEWGgdZZUtO5hYzIcigV-Sjrhv_zsmTBRu8X8Dhs5Zssr-mulwSaDjITcKRlCna1Eej5kJNQUYeLDDB5pKK5Xx3T3eFxNLrTNvGABMENfoWZgmlLnBgg_ux9bmm4XcncNL5pb_cpEgCZKVpv-SJh2dTtY8Q-QutUDNDG34m-ifMcwicK59RiGsF8fNPKy44wX_BJhqwrg80FYEhOhrqJhzVqSSLb807yIQkx5fNFy8ekzrR2toGusQBsAVwz06g3xaDVMGXBz7mmB35gCP_NQscIGSjtFXTNeItM-HJzTU7TDBzbMDMuRaI2DU1mb7Dt30z8D2NNrw",
    "token_type": "access_token",
    "expires_in": 3600
}
```

## Get Paid

MoMo get paid APIs enable businesses to collect payments from consumers and businesses in different ways.
Partners initiate instant payment within any digital platform (website, mobile application) through MoMo channels.
Folder also includes a set of capabilities that enhance value and offer an excellent customer experience. These include: Refund, Notification.

### Request To Pay

**Endpoint:** `POST {{base_url}}/collection/v1_0/requesttopay`

Create Request To Pay - This endpoint allows the client to initiate a request to pay.

**Request Body**
- **amount** (string): The amount to be requested
- **currency** (string): The currency in which the amount is requested
- **externalId** (string): The unique identifier for the request
- **payer** (object):
  - **partyIdType** (string): The type of party ID for the payer (MSISDN/ALIAS/EMAIL)
  - **partyId** (string): The ID of the payer
- **payerMessage** (string): Message from the payer
- **payeeNote** (string): Note for the payee

**Request Body Example**

```json
{
  "amount": "600",
  "currency": "EUR",
  "externalId": "00004335",
  "payer": {
    "partyIdType": "MSISDN",
    "partyId": "{{MSISDN}}"
  },
  "payerMessage": "MoMo Market Payment",
  "payeeNote": "MoMo Market Payment"
}
```

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Example Request**

```bash
curl --location 'https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay' \
--header 'X-Reference-Id: 2f209631-07d4-4254-8d6a-bd0f1ef78538' \
--header 'X-Target-Environment: sandbox' \
--header 'Content-Type: application/json' \
--header 'Ocp-Apim-Subscription-Key: bca0c92d326a46cd885f443d51b859f1' \
--header 'X-Callback-Url: https://webhook.site/mywebhooksandbox' \
--data '{
  "amount": "600",
  "currency": "EUR",
  "externalId": "00004335",
  "payer": {
    "partyIdType": "MSISDN",
    "partyId": "56733123450"
  },
  "payerMessage": "MoMo Market Payment",
  "payeeNote": "MoMo Market Payment"
}'
```

### Status Request To Pay

**Endpoint:** `GET {{base_url}}/collection/v1_0/requesttopay/:Request_ID_Debit`

Retrieve Request To Pay Response - This endpoint retrieves the response for a specific request to pay, identified by the unique Request_ID_Debit.

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Path Variables**
- **Request_ID_Debit**: `{{Request_ID_Debit}}` - Request Id of the debit request Posted

**Example Request**

```bash
curl --location 'https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay/2f209631-07d4-4254-8d6a-bd0f1ef78538' \
--header 'X-Target-Environment: sandbox' \
--header 'Ocp-Apim-Subscription-Key: bca0c92d326a46cd885f443d51b859f1'
```

### Notification

**Endpoint:** `POST {{base_url}}/collection/v1_0/requesttopay/{{Request_ID_Debit}}/deliverynotification`

This endpoint is used to send a delivery notification for a specific request to pay.

**Request Body**
- **notificationMessage**: (string) The message for the delivery notification

**Request Body Example**

```json
{
  "notificationMessage": "Thank You for using MoMo"
}
```

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Example Request**

```bash
curl --location 'https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay/2f209631-07d4-4254-8d6a-bd0f1ef78538/deliverynotification' \
--header 'X-Target-Environment: sandbox' \
--header 'Content-Type: application/json' \
--header 'Ocp-Apim-Subscription-Key: bca0c92d326a46cd885f443d51b859f1' \
--data '{
  "notificationMessage": "Thank You for using MoMo"
}'
```

### Refund

**Endpoint:** `POST {{base_url}}/disbursement/v1_0/refund`

Refund Disbursement - This endpoint allows the user to initiate a refund for a previous disbursement.

**Request Body**
- **amount** (string): The amount to be refunded
- **currency** (string): The currency in which the refund amount is specified
- **externalId** (string): The external identifier for the refund transaction
- **payerMessage** (string): Message to be displayed to the payer (optional)
- **payeeNote** (string): Note to be displayed to the payee (optional)
- **referenceIdToRefund** (string): The reference ID of the disbursement to be refunded

**Request Body Example**

```json
{
  "amount": "300",
  "currency": "EUR",
  "externalId": "Refund_uibi",
  "payerMessage": "Refund for MoMo Market Payment",
  "payeeNote": "Refund for MoMo Market Payment",
  "referenceIdToRefund": "{{Request_ID_Debit}}"
}
```

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Example Request**

```bash
curl --location 'https://sandbox.momodeveloper.mtn.com/disbursement/v1_0/refund' \
--header 'X-Callback-Url: https://webhook.site/mywebhooksandbox' \
--header 'X-Reference-Id: 85c66b88-abb8-4523-a81d-2d5566816c70' \
--header 'X-Target-Environment: sandbox' \
--header 'Content-Type: application/json' \
--header 'Ocp-Apim-Subscription-Key: 0fd9826a39aa468fb311d23fc08a55fc' \
--data '{
  "amount": "300",
  "currency": "EUR",
  "externalId": "Refund_uibi",
  "payerMessage": "Refund for MoMo Market Payment",
  "payeeNote": "Refund for MoMo Market Payment",
  "referenceIdToRefund": "2f209631-07d4-4254-8d6a-bd0f1ef78538"
}'
```

### Refund Status

**Endpoint:** `GET {{base_url}}/disbursement/v1_0/refund/:Request_ID_Refund`

This endpoint is used to check the status of a refund by providing the Request_ID_Refund, which is also mapped as the X-Reference-Id in the Refund Request.

**Headers**
- **X-Target-Environment** (string, required): The identifier specifying the country the request is meant for
- **Ocp-Apim-Subscription-Key** (string, required): Subscription key providing access to this API

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Path Variables**
- **Request_ID_Refund**: `{{Request_ID_Refund}}`

**Example Request**

```bash
curl --location 'https://sandbox.momodeveloper.mtn.com/disbursement/v1_0/refund/85c66b88-abb8-4523-a81d-2d5566816c70' \
--header 'X-Target-Environment: sandbox' \
--header 'Ocp-Apim-Subscription-Key: 0fd9826a39aa468fb311d23fc08a55fc'
```

## Payment

Payment API enables a Business to streamline utility payments and initiate services like airtime and bundle activation through MoMo.

### Create Payment

**Endpoint:** `POST https://sandbox.momodeveloper.mtn.com/collection/v2_0/payment`

This API endpoint is used to initiate a payment collection.

**Request Body**
- **externalTransactionId** (text): The ID of the external transaction
- **money.amount** (text): The amount of the payment
- **money.currency** (text): The currency of the payment
- **customerReference** (text): Reference to the customer initiating the payment
- **serviceProviderUserName** (text): Username of the service provider
- **couponId** (text): ID of the coupon, if applicable
- **productId** (text): ID of the product
- **productOfferingId** (text): ID of the product offering
- **receiverMessage** (text): Message for the receiver of the payment
- **senderNote** (text): Note from the sender of the payment
- **maxNumberOfRetries** (text): Maximum number of retries for the payment
- **includeSenderCharges** (text): Indicator whether to include sender charges

**Request Body Example**

```json
{
  "externalTransactionId": "457373",
  "money": {
    "amount": "2000",
    "currency": "EUR"
  },
  "customerReference": "561551442",
  "serviceProviderUserName": "WaterProvider",
  "couponId": "203",
  "productId": "Monthly Payments",
  "productOfferingId": "788",
  "receiverMessage": "Thank You ",
  "senderNote": "Thank You",
  "maxNumberOfRetries": "2",
  "includeSenderCharges": "1"
}
```

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Example Request**

```bash
curl --location 'https://sandbox.momodeveloper.mtn.com/collection/v2_0/payment' \
--header 'X-Callback-Url: https://webhook.site/mywebhooksandbox' \
--header 'X-Reference-Id;' \
--header 'X-Target-Environment: sandbox' \
--header 'Content-Type: application/json' \
--header 'Ocp-Apim-Subscription-Key: bca0c92d326a46cd885f443d51b859f1' \
--data '{
  "externalTransactionId": "457373",
  "money": {
    "amount": "2000",
    "currency": "EUR"
  },
  "customerReference": "561551442",
  "serviceProviderUserName": "WaterProvider",
  "couponId": "203",
  "productId": "Monthly Payments",
  "productOfferingId": "788",
  "receiverMessage": "Thank You ",
  "senderNote": "Thank You",
  "maxNumberOfRetries": "2",
  "includeSenderCharges": "1"
}'
```

### Get Payment Status

**Endpoint:** `GET https://sandbox.momodeveloper.mtn.com/collection/v2_0/payment/:Request_ID_Payment`

Retrieve Payment Response - This endpoint retrieves the response for a specific payment request identified by the provided Request ID.

**Response**

```json
{
    "referenceId":"",
    "status":"",
    "reason":""
}
```

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Path Variables**
- **Request_ID_Payment**: `{{Request_ID_Payment}}`

**Example Request**

```bash
curl --location 'https://sandbox.momodeveloper.mtn.com/collection/v2_0/payment/:Request_ID_Payment' \
--header 'X-Target-Environment: sandbox' \
--header 'Ocp-Apim-Subscription-Key: bca0c92d326a46cd885f443d51b859f1'
```

## Pay

MoMo PAY APIs enable businesses to disburse payments to other consumers or businesses. This can be used in the context of salary payment, benefits disbursements and any other pay out. It can also be used to pay other business (suppliers).

PAY APIs utilize the Disbursement Subscription Keys.

### Transfer

Make MoMo Transfer from Your Business to Other Business, Customers, Employees in the context of salary, bet winnings, Service Payments.

The MoMo Transfer API accommodates one MSISDN/ALIAS per request, and not bulk.

**Business to Business Payments** by using their Merchant ID:

```json
{
  "amount": "5900",
  "currency": "EUR",
  "externalId": "890695",
  "payee": {
    "partyIdType": "ALIAS",
    "partyId": "678997678"
  },
  "payerMessage": "Salary Payment April 2023",
  "payeeNote": "Salary Payment April 2023"
}
```

**Business to Customer/Employee Payments** by using their MSISDN with country code:

```json
{
  "amount": "5900",
  "currency": "EUR",
  "externalId": "890695",
  "payee": {
    "partyIdType": "MSISDN",
    "partyId": "2567524561"
  },
  "payerMessage": "Salary Payment April 2023",
  "payeeNote": "Salary Payment April 2023"
}
```

**Endpoint:** `POST {{base_url}}/disbursement/v1_0/transfer`

**Request Body**
- **amount** (string): The amount to be transferred
- **currency** (string): The currency in which the amount is specified
- **externalId** (string): An ID to uniquely identify the transfer
- **payee** (object): Information about the payee
  - **partyIdType** (string): Type of ID for the payee
  - **partyId** (string): ID of the payee
- **payerMessage** (string): Message from the payer
- **payeeNote** (string): Note for the payee

**Request Body Example**

```json
{
  "amount": "5900",
  "currency": "EUR",
  "externalId": "890695",
  "payee": {
    "partyIdType": "MSISDN",
    "partyId": "{{MSISDN}}"
  },
  "payerMessage": "Salary Payment April 2023",
  "payeeNote": "Salary Payment April 2023"
}
```

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Example Request**

```bash
curl --location 'https://sandbox.momodeveloper.mtn.com/disbursement/v1_0/transfer' \
--header 'X-Callback-Url: https://webhook.site/mywebhooksandbox' \
--header 'X-Reference-Id: 1077fbc2-9253-437f-883c-30e248bc635d' \
--header 'X-Target-Environment: sandbox' \
--header 'Content-Type: application/json' \
--header 'Ocp-Apim-Subscription-Key: 0fd9826a39aa468fb311d23fc08a55fc' \
--data '{
  "amount": "5900",
  "currency": "EUR",
  "externalId": "890695",
  "payee": {
    "partyIdType": "MSISDN",
    "partyId": "56733123455"
  },
  "payerMessage": "Salary Payment April 2023",
  "payeeNote": "Salary Payment April 2023"
}'
```

### Transfer Status

**Endpoint:** `GET https://sandbox.momodeveloper.mtn.com/disbursement/v1_0/transfer/:Request_ID_Transfer`

This endpoint makes an HTTP GET request to retrieve information about a specific transfer identified by the provided Request ID.

**Response Body**
The response includes the following fields in JSON format:
- **amount**: The amount of the transfer
- **currency**: The currency used for the transfer
- **financialTransactionId**: The financial transaction ID associated with the transfer
- **externalId**: The external ID associated with the transfer
- **payee**: An object containing information about the payee, including party ID type and party ID
- **payerMessage**: The message from the payer associated with the transfer
- **payeeNote**: The note from the payee associated with the transfer
- **status**: The status of the transfer

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Path Variables**
- **Request_ID_Transfer**: `{{Request_ID_Transfer}}`

**Example Request**

```bash
curl --location 'https://sandbox.momodeveloper.mtn.com/disbursement/v1_0/transfer/1077fbc2-9253-437f-883c-30e248bc635d' \
--header 'X-Target-Environment: sandbox' \
--header 'Ocp-Apim-Subscription-Key: 0fd9826a39aa468fb311d23fc08a55fc'
```

## Account Validation

To avoid Debiting Or Transferring invalid / Wrong MoMo Accounts, good practice to validate them and confirm ownership. Get Names and KYC and Account Status (Active- True, Inactive-False).

### Validation No Consent

API Folder containing APIs that can be validated without requiring customer consent.

#### Check Account Holder

Check Account Holder API - This API provides information on whether an account has a MoMo wallet or not. It returns either true or false.

**Endpoint:** `GET {{base_url}}/disbursement/v1_0/accountholder/msisdn/:MSISDN/active`

Retrieve Active Account Holder by MSISDN - This endpoint makes an HTTP GET request to retrieve the active account holder by MSISDN.

**URL Parameters**
- **MSISDN** (required, string): The mobile number for which the active account holder information is to be retrieved

**Response**
The response will be in JSON format and will contain the following key:
- **result** (boolean): Indicates whether the account holder is active or not

**Example response:**

```json
{
    "result": true
}
```

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Path Variables**
- **MSISDN**: `{{MSISDN}}`

#### Get Basic Info (MSISDN)

Get Basic Info (MSISDN) API - This API retrieves the first and last names of the MoMo wallet owner. If the wallet does not exist, it returns an error message stating "Not Found".

**Endpoint:** `GET {{base_url}}/remittance/v1_0/accountholder/msisdn/:MSISDN/basicuserinfo`

This endpoint retrieves basic user information for the account holder associated with the provided MSISDN (Mobile Station International Subscriber Directory Number).

**Headers**
- **Authorization** (Bearer Token): The request is authenticated using a Bearer Token
- **X-Target-Environment**: The identifier on the API Request specifying which country the request is to be processed for production
- **Ocp-Apim-Subscription-Key**: Subscription key which provides access to the APIM

**Path Parameter**
- **MSISDN**: The Mobile Station International Subscriber Directory Number for which the basic user information is to be retrieved

**Response**
Upon successful execution, the response will have a status code of 200 and a JSON object with the following fields:

```json
{
  "sub": "",
  "name": "",
  "given_name": "",
  "family_name": "",
  "birthdate": "",
  "locale": "",
  "gender": "",
  "updated_at": 0
}
```

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Path Variables**
- **MSISDN**: `{{MSISDN}}`

#### Get Basic Info (Alias)

Get Basic Info (Alias) API - This API retrieves the first and last names of the MoMo wallet owner using an Alias (Business Merchant ID). If the wallet does not exist, it returns an error message stating "Not Found".

**Endpoint:** `GET {{base_url}}/disbursement/v1_0/accountholder/Alias/:MSISDN/basicuserinfo`

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Path Variables**
- **MSISDN**: `{{MSISDN}}`

### Detailed KYC - With Consent

KYC With Consent APIs, Used to obtain Consent from the Customer to access their KYC information, like National ID, Date of Birth.

#### bc-authorize

**Endpoint:** `POST {{base_url}}/disbursement/v1_0/bc-authorize`

This endpoint allows you to make an HTTP POST request to authorize a disbursement.

**Request Body**
The request should include the following parameters in x-www-form-urlencoded format:
- **scope**: all_info
- **login_hint**: ID:563667/MSISDN
- **access_type**: offline

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Example Request**

```bash
curl --location 'https://sandbox.momodeveloper.mtn.com/disbursement/v1_0/bc-authorize' \
--header 'X-Target-Environment: sandbox' \
--header 'X-Callback-Url: https://webhook.site/mywebhooksandbox' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--header 'Ocp-Apim-Subscription-Key: 0fd9826a39aa468fb311d23fc08a55fc' \
--data-urlencode 'scope=all_info' \
--data-urlencode 'login_hint=ID:563667/MSISDN' \
--data-urlencode 'access_type=offline'
```

#### Generate Oauth2 Token

**Endpoint:** `POST {{base_url}}/disbursement/oauth2/token/`

This endpoint allows the client to obtain an OAuth2 token for disbursement.

**Response JSON Schema**

```json
{
  "type": "object",
  "properties": {
    "access_token": {
      "type": "string"
    },
    "token_type": {
      "type": "string"
    },
    "expires_in": {
      "type": "integer"
    },
    "scope": {
      "type": "string"
    }
  }
}
```

**Authorization**
- Basic Auth
- Username: `{{api_user}}`
- Password: `{{api_key}}`

**Request Body**
- **grant_type**: urn:openid:params:grant-type:ciba
- **auth_req_id**: `{{Consent_Req_Id}}`

**Example Request**

```bash
curl --location 'https://sandbox.momodeveloper.mtn.com/disbursement/oauth2/token/' \
--header 'X-Target-Environment: sandbox' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--header 'Ocp-Apim-Subscription-Key: 0fd9826a39aa468fb311d23fc08a55fc' \
--data-urlencode 'grant_type=urn:openid:params:grant-type:ciba' \
--data-urlencode 'auth_req_id=010001b2-5c84-4dd1-9eaf-56d5668dabd3'
```

#### Get UserInfo

**Endpoint:** `GET {{base_url}}/disbursement/oauth2/v1_0/userinfo`

This endpoint is used to retrieve user information via an HTTP GET request.

**Authorization**
- Bearer Token: `{{Oauth2_Token}}`

**Example Request**

```bash
curl --location --globoff '{{base_url}}/disbursement/oauth2/v1_0/userinfo' \
--header 'X-Target-Environment: {{Target_Environment}}' \
--header 'Ocp-Apim-Subscription-Key: {{Disbursement_Subscription-Key}}'
```

## Distribute

MoMo Open APIs enable business to distribute MTN and MoMo service and facilitate Cash In, Cash out and Airtime sale and get commission from MTN and MoMo.

Folder contains Cash In APIs and Cash Out.

### Cash IN

#### Deposit Request

**Endpoint:** `POST https://sandbox.momodeveloper.mtn.com/disbursement/v1_0/deposit`

Deposit Disbursement - This endpoint allows you to initiate a deposit disbursement.

**Request Body**
- **amount** (string): The amount to be deposited
- **currency** (string): The currency of the amount
- **externalId** (string): Your unique identifier for this transaction
- **payee.partyIdType** (string): The type of the party ID
- **payee.partyId** (string): The ID of the party to receive the deposit
- **payerMessage** (string): Message from the payer
- **payeeNote** (string): Note to the payee

**Request Body Example**

```json
{
  "amount": "2679",
  "currency": "EUR",
  "externalId": "004504",
  "payee": {
    "partyIdType": "MSISDN",
    "partyId": "{{MSISDN}}"
  },
  "payerMessage": "MoMo CASH IN Thank You",
  "payeeNote": "MoMo CASH IN Thank You"
}
```

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Example Request**

```bash
curl --location 'https://sandbox.momodeveloper.mtn.com/disbursement/v1_0/deposit' \
--header 'X-Callback-Url: https://webhook.site/mywebhooksandbox' \
--header 'X-Reference-Id;' \
--header 'X-Target-Environment: sandbox' \
--header 'Content-Type: application/json' \
--header 'Ocp-Apim-Subscription-Key: 0fd9826a39aa468fb311d23fc08a55fc' \
--data '{
  "amount": "2679",
  "currency": "EUR",
  "externalId": "004504",
  "payee": {
    "partyIdType": "MSISDN",
    "partyId": "56733123455"
  },
  "payerMessage": "MoMo CASH IN Thank You",
  "payeeNote": "MoMo CASH IN Thank You"
}'
```

#### Deposit Request Status

**Endpoint:** `GET {{base_url}}/disbursement/v1_0/deposit/:Request_ID_CashIn`

This API endpoint makes an HTTP GET request to retrieve the details of a specific deposit identified by the Request_ID_CashIn in the URL.

**Response**

```json
{
    "externalId":"",
    "amount":"",
    "currency":"",
    "payee":{
        "partyIdType":"",
        "partyId":""
    },
    "payerMessage":"",
    "payeeNote":"",
    "status":""
}
```

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Path Variables**
- **Request_ID_CashIn**: `{{Request_ID_CashIn}}`

**Example Request**

```bash
curl --location 'https://sandbox.momodeveloper.mtn.com/disbursement/v1_0/deposit/:Request_ID_CashIn' \
--header 'X-Target-Environment: sandbox' \
--header 'Ocp-Apim-Subscription-Key: 0fd9826a39aa468fb311d23fc08a55fc'
```

### Cash OUT

#### Request To Withdraw

**Endpoint:** `POST {{base_url}}/collection/v1_0/requesttowithdraw`

This endpoint allows the user to initiate a request to withdraw funds.

**Request Body**
- **amount** (string, required): The amount to be withdrawn
- **currency** (string, required): The currency in which the withdrawal is to be made
- **externalId** (string, required): The unique identifier for the withdrawal request
- **payer** (object, required):
  - **partyIdType** (string, required): The type of party ID for the payer
  - **partyId** (string, required): The ID of the payer
- **payerMessage** (string, optional): A message from the payer
- **payeeNote** (string, optional): A note for the payee

**Request Body Example**

```json
{
  "amount": "3536636",
  "currency": "EUR",
  "externalId": "45757757",
  "payer": {
    "partyIdType": "MSISDN",
    "partyId": "{{MSISDN}}"
  },
  "payerMessage": "MoMo Cash Out Thank You",
  "payeeNote": "MoMo Cash Out Thank You "
}
```

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Example Request**

```bash
curl --location 'https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttowithdraw' \
--header 'X-Callback-Url: https://webhook.site/mywebhooksandbox' \
--header 'X-Reference-Id;' \
--header 'X-Target-Environment: sandbox' \
--header 'Content-Type: application/json' \
--header 'Ocp-Apim-Subscription-Key: bca0c92d326a46cd885f443d51b859f1' \
--data '{
  "amount": "3536636",
  "currency": "EUR",
  "externalId": "45757757",
  "payer": {
    "partyIdType": "MSISDN",
    "partyId": "56733123455"
  },
  "payerMessage": "MoMo Cash Out Thank You",
  "payeeNote": "MoMo Cash Out Thank You "
}'
```

#### Request To Withdraw Status

**Endpoint:** `GET {{base_url}}/collection/v1_0/requesttowithdraw/:Request_ID_CashOut`

This endpoint makes an HTTP GET request to retrieve information about a specific cash withdrawal request identified by the provided Request_ID_CashOut.

**Response**
Upon a successful execution, the endpoint returns a JSON object with the following fields:
- **financialTransactionId** (string): The ID of the financial transaction
- **externalId** (string): The external ID associated with the transaction
- **amount** (string): The amount of the withdrawal
- **currency** (string): The currency in which the withdrawal is made
- **payer** (object): An object containing information about the payer, including partyIdType and partyId
- **payerMessage** (string): A message from the payer
- **payeeNote** (string): A note from the payee
- **status** (string): The status of the withdrawal request

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Path Variables**
- **Request_ID_CashOut**: `{{Request_ID_CashOut}}`

**Example Request**

```bash
curl --location 'https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttowithdraw/:Request_ID_CashOut' \
--header 'X-Target-Environment: sandbox' \
--header 'Ocp-Apim-Subscription-Key: bca0c92d326a46cd885f443d51b859f1'
```

## Invoice

A Business may use this in order to create an invoice that can be paid by an intended payer via any channel at a later stage.

### Create Invoice

**Endpoint:** `POST {{base_url}}collection/v2_0/invoice`

This endpoint allows you to create a new invoice. The customer will receive an SMS with the Invoice ID.

The Payments can be made via MoMo USSD or MoMo APP.

**Request Body**
- **externalId** (string): The external identifier for the invoice
- **amount** (string): The amount of the invoice
- **currency** (string): The currency in which the invoice amount is specified
- **validityDuration** (string): The duration for which the invoice is valid
- **intendedPayer** (object): An object containing the party ID type and party ID of the intended payer
  - **partyIdType** ("MSISDN/ALIAS"): The type of party ID for the intended payer
  - **partyId** (MSISDN ID): The party ID of the intended payer
- **payee** (object): An object containing the party ID type and party ID of the payee
  - **partyIdType** (MSISDN): The type of party ID for the payee
  - **partyId** (string): The party ID of the payee
- **description** (string): Description of the invoice

**Request Body Example**

```json
{
    "externalId": "005060",
    "amount": "5000",
    "currency": "EUR",
    "validityDuration": "360",
    "intendedPayer": {
        "partyIdType": "MSISDN",
        "partyId": "56784939"
    },
    "payee": {
        "partyIdType": "MSISDN",
        "partyId": "46733123450"
    },
    "description": "Invoice SandBox"
}
```

**Authorization**
- Bearer Token: `{{Access_Token}}`

### Invoice Status

**Endpoint:** `GET {{base_url}}/collection/v2_0/invoice/:Request_ID_Invoice`

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Path Variables**
- **Request_ID_Invoice**: `{{Request_ID_Invoice}}`

### Delete Invoice

**Endpoint:** `DELETE {{base_url}}/collection/v2_0/invoice/:Request_ID_Invoice`

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Path Variables**
- **Request_ID_Invoice**: `{{Request_ID_Invoice}}`

**Request Body Example**

```json
{
    "externalId": "57r75677"
}
```

## Pre Approval

Pre Approval API is used to get consent from the customer to be Debited for a specified period of time. The Consent is approved by the customer providing the correct PIN. The Consent can be cancelled anytime by the customer.

### Request Preapproval

**Endpoint:** `POST {{base_url}}/collection/v2_0/preapproval`

Create Preapproval - This endpoint allows you to create a preapproval for a collection.

**Request Body**
- **payer** (object, required): Information about the payer including partyIdType and partyId
- **payerCurrency** (string, required): The currency of the payer
- **payerMessage** (string, required): A message from the payer
- **validityTime** (string, required): The validity time of the preapproval

**Request Body Example**

```json
{
  "payer": {
    "partyIdType": "MSISDN",
    "partyId": "{{MSISDN}}"
  },
  "payerCurrency": "EUR",
  "payerMessage": "HI MoMo API",
  "validityTime": "300"
}
```

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Example Request**

```bash
curl --location --globoff '{{base_url}}/collection/v2_0/preapproval' \
--header 'X-Callback-Url: {{CallbackURL}}' \
--header 'X-Reference-Id: {{Request_ID_Preapproval}}' \
--header 'X-Target-Environment: {{Target_Environment}}' \
--header 'Content-Type: application/json' \
--header 'Ocp-Apim-Subscription-Key: {{Collection_Subscription-Key}}' \
--data '{
  "payer": {
    "partyIdType": "MSISDN",
    "partyId": "{{MSISDN}}"
  },
  "payerCurrency": "EUR",
  "payerMessage": "HI MoMo API",
  "validityTime": "300"
}'
```

### Get PreApproval Status

**Endpoint:** `GET {{base_url}}/collection/v2_0/preapproval/:Request_ID_Preapproval`

This API endpoint retrieves the details of a specific preapproval by providing the preapproval request ID in the URL.

**Response**
Upon a successful execution (Status: 200), the response will be in JSON format with the following fields:
- **payer**
  - **partyIdType**
  - **partyId**
- **payerCurrency**
- **payerMessage**
- **expirationDateTime**
- **status**

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Path Variables**
- **Request_ID_Preapproval**: `{{Request_ID_Preapproval}}`

**Example Request**

```bash
curl --location --globoff '{{base_url}}/collection/v2_0/preapproval/{{Request_ID_Preapproval}}' \
--header 'X-Target-Environment: {{Target_Environment}}' \
--header 'Ocp-Apim-Subscription-Key: {{Collection_Subscription-Key}}'
```

## Remittance

The Remittance API empowers businesses by enabling users to transmit or receive funds from overseas straight into their Mobile Money accounts, all in local currency.

### Transfer

**Endpoint:** `POST {{base_url}}/remittance/v1_0/transfer`

**Headers**
- **X-Reference-Id**: The UUID Version 4 Format String, labeled as Request_ID_Transfer, is used to uniquely identify a transaction and retrieve the status
- **Authorization**: Bearer Token, the Access_token, is automatically generated in the pre-request script of the collection
- **X-Target-Environment**: Specifies the country the request is to be processed for production, using sandbox during testing
- **Content-Type**: application/json
- **Ocp-Apim-Subscription-Key**: Subscription key providing access to the APIM
- **X-Callback-Url**: Secure HTTPS URL for receiving responses

**Request Body**
- **Amount** (string): Amount to be transferred to the MoMo Subscriber
- **Currency** (string): Varies depending on the country, with Sandbox using EUR
- **ExternalId** (string): String used for reconciliation between Partner Platform and MoMo Platform
- **PartyIdType** (string): Supported types are MSISDN and ALIAS
- **PartyId** (string): Value of the MSISDN Number or Merchant ID
- **PayerMessage** (string): Notification sent to the Sender
- **PayeeNote** (string): Notification sent to the receiver

**Request Body Example**

```json
{
  "amount": "980000",
  "currency": "EUR",
  "externalId": "9087699",
  "payee": {
    "partyIdType": "MSISDN",
    "partyId": "{{MSISDN}}"
  },
  "payerMessage": "remittance amount",
  "payeeNote": "remittance amount"
}
```

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Example Request**

```bash
curl --location --globoff '{{base_url}}/remittance/v1_0/transfer' \
--header 'X-Callback-Url: {{CallbackURL}}' \
--header 'X-Reference-Id: {{Request_ID_Remit_Transfer}}' \
--header 'X-Target-Environment: {{Target_Environment}}' \
--header 'Content-Type: application/json' \
--header 'Ocp-Apim-Subscription-Key: {{Remittance_Subscription-Key}}' \
--data '{
  "amount": "980000",
  "currency": "EUR",
  "externalId": "9087699",
  "payee": {
    "partyIdType": "MSISDN",
    "partyId": "{{MSISDN}}"
  },
  "payerMessage": "remittance amount",
  "payeeNote": "remittance amount"
}'
```

### Transfer Status

**Endpoint:** `GET https://sandbox.momodeveloper.mtn.com/remittance/v1_0/transfer/:Request_ID_Remit_Transfer`

This HTTP GET request is used to retrieve information about a specific remittance transfer identified by the Request ID.

**Response**
Upon a successful execution, the API returns a JSON response with the following fields:
- **amount**: The amount of the remittance transfer
- **currency**: The currency of the remittance transfer
- **financialTransactionId**: The financial transaction ID associated with the transfer
- **externalId**: The external ID associated with the transfer
- **payee**: An object containing information about the payee, including party ID type and party ID
- **payerMessage**: The message from the payer associated with the transfer
- **payeeNote**: The note from the payee associated with the transfer
- **status**: The status of the remittance transfer

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Path Variables**
- **Request_ID_Remit_Transfer**: `{{Request_ID_Remit_Transfer}}`

**Example Request**

```bash
curl --location --globoff 'https://sandbox.momodeveloper.mtn.com/remittance/v1_0/transfer/{{Request_ID_Remit_Transfer}}' \
--header 'X-Target-Environment: {{Target_Environment}}' \
--header 'Ocp-Apim-Subscription-Key: {{Remittance_Subscription-Key}}'
```

## CashTransfer

CashTransfer API is the enriched Remittance API, designed to facilitate the efficient capture of Know Your Customer (KYC) details for both the payer and payee involved in fund transfers.

### Field Descriptions:

- **amount**: This is the sum that the recipient will receive following currency conversion
- **currency**: Specifies the type of currency in which the recipient will receive the amount (ISO 4217 Currency Codes)
- **payee**: Contains information about the beneficiary
- **partyId**: A unique identifier for the recipient, which could be a phone number, email, or a designated party code
- **partyIdType**: The kind of identifier being used, such as MSISDN, EMAIL, or PARTY_CODE
- **externalId**: This is the transaction ID used for business applications and is useful for reconciliation purposes
- **originatingCountry**: The country from which the funds are being sent
- **originalAmount**: The initial sum to be received before any currency conversion takes place
- **originalCurrency**: The currency in which the original sum is denominated (ISO 4217 Currency Codes)
- **payerMessage**: A message that will be delivered to the sender
- **payeeNote**: A note that will be delivered to the beneficiary
- **payerIdentificationType**: The type of identification used for the sender

### Payer Identification Types:
- **CPFA**: CPF account number
- **SRSA**: SRS account number
- **NRIN**: National registration identification number
- **OTHR**: Other
- **DRLC**: Drivers license number
- **PASS**: Passport number
- **SOCS**: Social security number
- **AREG**: Alien registration number
- **IDCD**: Identity card number
- **EMID**: Employer identification number

- **payerIdentificationNumber**: The identification number that corresponds to the specified identification type
- **payerIdentity**: The MSISDN utilized by the sender in the country where the remittance originates. Format: (ID:6873248686/MSISDN)
- **payerFirstName** / **payerSurName**: The given name and surname of the sender
- **payerLanguageCode**: The linguistic code corresponding to the sender's nation (ISO_639-1)
- **payerEmail**: The sender's electronic mail address (Validated)
- **payerMsisdn**: The phone number of the sender
- **payerGender**: The sex of the sender (MALE, FEMALE, OTHER)

### cashtransfer

**Endpoint:** `POST {{base_url}}/remittance/v2_0/cashtransfer`

**Request Headers**
- **X-Reference-Id**: `{{Request_ID_Cash_Transfer}}`
- **X-Target-Environment**: `{{Target_Environment}}`
- **Content-Type**: application/json
- **Ocp-Apim-Subscription-Key**: `{{Remittance_Subscription-Key}}`

**Request Body Example**

```json
{
    "amount": "208",
    "currency": "EUR",
    "payee": {
        "partyIdType": "MSISDN",
        "partyId": "{{MSISDN}}"
    },
    "externalId": "XTR1718714047",
    "orginatingCountry": "SO",
    "originalAmount": "1",
    "originalCurrency": "USD",
    "payerMessage": "From SO to MTN UG Payer",
    "payeeNote": "Test",
    "payerIdentificationType": "PASS",
    "payerIdentificationNumber": "UG0002",
    "payerIdentity": "ID:256701081899/MSISDN",
    "payerFirstName": "Abdirazak",
    "payerSurName": "Ibrahim",
    "payerLanguageCode": "en",
    "payerEmail": "abdirazak.ibrahim@tt.com",
    "payerMsisdn": "252654249184",
    "payerGender": "MALE"
}
```

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Example Request**

```bash
curl --location --globoff '{{base_url}}/remittance/v2_0/cashtransfer' \
--header 'X-Reference-Id: {{Request_ID_Cash_Transfer}}' \
--header 'X-Target-Environment: {{Target_Environment}}' \
--header 'Content-Type: application/json' \
--header 'Ocp-Apim-Subscription-Key: {{Remittance_Subscription-Key}}' \
--data-raw '{
    "amount": "208",
    "currency": "EUR",
    "payee": {
        "partyIdType": "MSISDN",
        "partyId": "{{MSISDN}}"
    },
    "externalId": "XTR1718714047",
    "orginatingCountry": "SO",
    "originalAmount": "1",
    "originalCurrency": "USD",
    "payerMessage": "From SO to MTN UG Payer",
    "payeeNote": "Test",
    "payerIdentificationType": "PASS",
    "payerIdentificationNumber": "UG0002",
    "payerIdentity": "ID:256701081899/MSISDN",
    "payerFirstName": "Abdirazak",
    "payerSurName": "Ibrahim",
    "payerLanguageCode": "en",
    "payerEmail": "abdirazak.ibrahim@tt.com",
    "payerMsisdn": "252654249184",
    "payerGender": "MALE"
}'
```

### cashtransfer status

**Endpoint:** `GET {{base_url}}/remittance/v2_0/cashtransfer/:Request_ID_Cash_Transfer`

**Request Headers**
- **X-Target-Environment**: `{{Target_Environment}}`
- **Ocp-Apim-Subscription-Key**: `{{Remittance_Subscription-Key}}`

**Path Variables**
- **Request_ID_Cash_Transfer**: `{{Request_ID_Cash_Transfer}}`

**Response Example**

```json
{
    "financialTransactionId": "179403634",
    "externalId": "XTR1718714047",
    "payee": {
        "partyIdType": "MSISDN",
        "partyId": "56733123453"
    },
    "amount": "208",
    "currency": "EUR",
    "originalAmount": "1",
    "originalCurrency": "USD",
    "payerMessage": "From SO to MTN UG Payer",
    "payeeNote": "Test",
    "status": "SUCCESSFUL",
    "payerIdentificationType": "PASS",
    "payerIdentificationNumber": "UG0002",
    "payerIdentity": "ID:256701081899/MSISDN",
    "payerFirstName": "Abdirazak",
    "payerSurName": "Ibrahim",
    "payerLanguageCode": "en",
    "payerEmail": "abdirazak.ibrahim@tt.com",
    "payerMsisdn": "252654249184",
    "payerGender": "MALE"
}
```

**Authorization**
- Bearer Token: `{{Access_Token}}`

**Example Request**

```bash
curl --location --globoff '{{base_url}}/remittance/v2_0/cashtransfer/{{Request_ID_Cash_Transfer}}' \
--header 'X-Target-Environment: {{Target_Environment}}' \
--header 'Ocp-Apim-Subscription-Key: {{Remittance_Subscription-Key}}'
```

## Account Balance

MoMo API for Account Balance to check your personal account standings. Remember, this balance isn't for the client, but specifically for the Merchant Account - the Account Owner.

### Get Account Balance

**Endpoint:** `GET {{base_url}}/collection/v1_0/account/balance`

This endpoint makes an HTTP GET request to retrieve the account balance from the specified collection.

**Authorization**
- Bearer Token: `{{Access_Token}}`

## Get API User and API Key

**Endpoint:** `POST {{base_url}}/v1_0/apiuser`

This endpoint makes an HTTP POST request to create an API user at the specified URL.

**Request Body**

```json
{
    "providerCallbackHost": "{{CallbackHost}}"
}
```

**Example Request**

```bash
curl --location --globoff '{{base_url}}/v1_0/apiuser' \
--header 'X-Reference-Id: {{api_user}}' \
--header 'Content-Type: application/json' \
--header 'Ocp-Apim-Subscription-Key: {{Collection_Subscription-Key}}' \
--data '{
    "providerCallbackHost": {{CallbackHost}}
}'
```