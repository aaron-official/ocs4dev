# MoMo API

## Use Cases

Select the product of interest and the use case

Follow the APIs as shown. Execute in sequential order.

**Product Set:** Select a Product  
**Use Case:** Please select a product first

## Request To Pay

Request to Pay service is used for requesting a payment from a customer (Payer). This can be used by e.g. an online web shop to request a payment for a customer. The customer is requested to approve the transaction on the customer client.

### Flow:

1. Customer (Payer) have selected product(s) in the merchant web shop and decided to check out. Customer select to pay with Mobile Money.

2. The provider system collects the account information for the customer e.g. mobile number and calculate the total amount of the products.

3. The provider system sends a request to pay (`POST /requesttopay`) operation to Wallet Platform. This request includes the amount and customer (Payer) account holder number.

4. Wallet Platform will respond with HTTP 202 Accepted to the provider system

5. Provider shall inform the customer that a payment needs to be approved, by giving information on the merchant web page. For example, the merchant could show information that payment is being processed and that customer needs to approve using the own client, e.g. USSD, mobile app.

6. Wallet Platform will process the request so that the customer can approve the payment. The request to pay will be in PENDING state until the customer have approved/Rejected the payment.

7. The Customer (Payer) will use his/her own client to review the payment. Customer can approve or reject the payment.

8. Wallet platform will transfer the funds if the customer approves the payment. Status of the payment is updated to SUCCESSFUL or FAILED.

9. If a callback URL was provided in the `POST /requesttopay` then a callback will be sent once the request to pay have reached a final state (SUCCESSFUL, FAILED). Note the callback will only be sent once. There is no retry.

10. GET request can be used for validating the status of the transaction. GET is used if the partner system has not requested a callback by providing a callback URL or if the callback was not received.

## Pre-Approval

Pre-approval is used to setup an auto debit towards a customer. The Partner can request a pre-approval from the customer. Once the customer has approved then the partner can debit the customer account without authorization from the customer.

The call flow for setting up a pre-approval is like the request to pay use case. The following picture describes the sequence for pre-approval.

### Flow:

1. The Provider sends a `POST /preapproval` request to Wallet platform.

2. Provider shall inform the customer that pre-approval needs to be approved.

3. Customer (Payer) will use the own client to view the pre-approval request. Customer can approve or reject the request.

4. Callback will be sent if a callback URL was provided in the POST request. The callback is sent when the request has reach a final state (Successful, Failed).

5. The Provider can use the GET request to validate the status of the pre-approval.

## Transfer

Transfer is used for transferring money from the provider account to a customer.

The below sequence gives an overview of the flow of the transfer use case.

### Flow:

1. The Provider sends a `POST /transfer` request to Wallet platform.

2. Wallet platform will directly respond to indicate that the request is received and will be processed.

3. Wallet platform will authorize the request to ensure that the transfer is allowed. The funds will be transferred from the provider account to the Payee account provided in the transfer request.

4. Callback will be sent if a callback URL was provided in the POST request. The callback is sent when the request has reach a final state (SUCCESSFUL, FAILED).

5. The Provider can use the GET request to validate the status of the transfer.

## Validate Account Holder

Validate account holder can be used to do a validation if a customer is active and able to receive funds. The use case will only validate that the customer is available and active. It does not validate that a specific amount can be received.

The sequence for the validate account holder is described below.

### Flow:

1. The Partner can send a `GET /accountholder` request to validate is a customer is active. The Partner provides the id of that customer as part of the URL

2. Wallet platform will respond with HTTP 200 if the account holder is active.

## Get Balance

Get balance request is used to check the balance on the default account connected to the API User. The following is the sequence flow for get balance use case.

## Delivery Notification

This service is intended to provide an additional notification to a customer after the completion of a successful financial transaction, by SMS or by email.

Merchants and Service Providers using **PGW** (Partner gateway is an application responsible for connecting API manager to different Wallet instances across all the Opcos) to interact with the Wallet Platform have the capability to send a notification to their customers after completed transaction.

Additional information is sent via SMS and is free text that may contain information that a partner wants to communicate for example, delivery notification reference number, a lottery number, a booking number, ticket id etc.

The channel used to send the notification will be determined based on what identity was used to initiate original transaction/payment.

The time window during which partner can use additional notification is configured in Partner Gateway.

## Validate Consumer Identity

The Validate Consumer Identity use case (**KYC as a service**) enables a partner to retrieve (limited) customer KYC information with their consent. Upon request by the service provider, the customer will authorize, authenticate and provide consent to get detailed information.

The Partner will receive a short-lived token to fetch detailed information of the customer from the wallet platform.

The basic information that can be retrieved by default is Profile: Name, Gender, Date of birth, locale etc.

API: **GetBasicUserinfo** can be used to either validate for example, Consumer's age or name.

The use case will return limited information about the Consumer that can be used to pre-populate fields, validate the Consumer's age or use it for remittance or sanctions screening purposes.

## Get Consumer Information with Consent

This use case (**Authentication as a Service**) is used to validate/authenticate customer information, by way of a service provider sending a request to the wallet platform, with or without customer consent. The consumer will authenticate via authorization service, and if required, the consumer will be required to provide consent. The scope is to validate or retrieve customer information.

This use case will also enable a partner to obtain consent, or digitally accept terms and conditions. This can be seen as a "digital signature" (where a partner requires this).

A partner may also be able to fetch limited user info without requiring customer consent. This will also enable partners to record and review that a customer has accepted the terms of a contract (amongst other use cases).

This will be used as a base when any token based "as a service" is required.

API: **bc-authorize**.

It provides the Partner with the ability to fetch detailed information about a Consumer, after the Consumer has given the Partner consent for the retrieval of said information:

## Token Based API Authorization

Token based API authorization is required to support consent management for different services. The Partner will request consent from the consumer for certain financial and non-financial transactions, and this will remain valid until the account holder revokes the consent.

The functionalities that can be enhanced by using consent will be:

1. Transfer
2. Payment
3. Merchant payment
4. Transfer to any bank account

For partners, this will enable them to view the status of the transactions for which consent was given using the related parameters. For account holders, they can revoke the consent from any service at their will.

Business benefit of consent can be improved customer experience. Consent can be configured for a specific time and there will be no need to get consent for each transaction. Providing better control on what services are being allowed by the account holder for consent etc.

## Transfer with Consumer Consent

Gives the partner the ability to transfer money on behalf of a consumer, after the consumer has given the partner consent to do so.

## Merchant Payment with Consumer Consent

Gives the Merchant System (partner) the possibility to perform a merchant payment on behalf of a consumer to any receiver. This will only be possible after the Consumer has given the Merchant System (partner) a consent for doing so.

## Payment with Consumer Consent

Gives the Merchant System (partner) the possibility to perform a payment on behalf of a consumer to any receiver. This will only be possible after the Consumer has given the Merchant System (partner) a consent for doing so.

Payment with consent will be similar to Merchant Payment. For more details, Please refer above section- "Merchant Payment with Consumer Consent".

## Bank Transfer with Consumer Consent

Gives the Merchant System (partner) the possibility to perform a Bank Transfer on behalf of a consumer to any receiver. This will only be possible after the Consumer has given the Merchant System (partner) a consent for doing so.

Bank transfer with consent will be similar to Transfer with Consent. For more details, Please refer above section- "Transfer with Consumer Consent".