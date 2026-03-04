# MoMo API FAQ

## Authentication

### 1. What credentials do I need once I have subscribed to a product?

- **Subscription Key** - received upon subscription to a product. It is used for authenticating the number of API calls. For information about subscription keys, refer to point 2
- **API User and API Key** for bearer Oauth 2.0 token. In the sandbox they are self-generated from the APIs. In production these are generated from the partner portal (part of onboarding)

### 2. What is a subscription Key?

- This Key is used to authenticate and limit the number of calls that can be made
- The subscription key is assigned to the **Ocp-Apim-Subscription-Key** parameter of the header
- The Subscription Key can be found in your user profile
- Developers - can use either the Primary Key or Secondary Key for every product they subscribe to allow access to the API
- A developer cannot access or utilize any of the respective APIs without a Subscription Key
- Different subscription keys can be used for different product APIs; please check in your user profile

### 3. What is the API User and API Key for Oauth 2.0?

- The API User and API Key are used together with your subscription key to grant access to the -wallet system and is applicable to a specific country
- The API User and API Key are generated using respective APIs in the sandbox
- API user and Key are wholly managed by the merchant through Partner Portal for PRODUCTION setups
- Merchants can generate/revoke/refresh API Keys through the Partner Portal
- For Sandbox API User and Key is generated using an API

### 4. How do I generate an Oauth 2.0 token?

- You require an API User and API Key in format **APIUSER: APIKey** `e16510xx-7282-4a39-xx8b-da054889a33a:xx1894d23a8d4xxdadaf62f39dae99xx`
- Convert the concatenation of APIUser: APIKey into Base64 format
- Use the Base64 format to generate the authorization token, the result will look similar to this string `ZTE2NTEwY2xtNzI4Mi00YTx5LTg5OGItZGEwNTQ4ODlhMzNhOjg1MTg5NGQyM2E4ZDQxMW RhZGFmNxJmMzlkYWU5OcY4`

### 5. How do I create, provision and manage the API user and API key?

- Please review Sandbox provisioning process under API Sandbox
- The API User and API Key are used to grant access to the wallet system applicable to a specific country
- API user and Key are wholly managed by the merchant through Partner Portal in production
- Developers can generate or revoke API Keys through the Partner Portal in production

### 6. How do I generate a UUID for my transactions?

- This ID is used, for example, validating the status of the request. 'Universal Unique ID' for the transaction generated using UUID version 4
- Example of Version 4 UUID: `ca58fd96-2478-4624-b663-bdacd5f914ca`

## Callback

### 7. I am not getting any callbacks. How do I verify or configure my callback URL?

Check that you have:

- Registered a **ProviderCallbackHost** when creating your API User
- You have specified a callback URL in the Request
- The Callback URL MUST belong to the same domain as the ProvideCallbackHost. Subdomains are not allowed.

**Example:**

If you have specified your ProviderCallbackHost as `mycallback.com` then the callback URL shall be specified as `https://mycallback.com/`

Using `https://subdomain.mycallback.com/` as callback URL will not work

Callbacks in the sandbox are set by setting the callback host when creating an API user, if my callback URL for traffic is `https://testsite.test.com:1313/api/callback`, the callback host is `testsite.test.com` and the callback host is what is set with the user, but the call back URL is used in every request where a callback is expected

In the production environment, the callback is set in the merchant portal and instructions are sent as part of the onboarding documentation

### Setting up a Callback URL

Transfer and RequestToPay APIs are Asynchronous in MTN MoMo API Platform

When a merchant system sends a POST of either `/transfer`, or `/requesttopay` APIs, the Gateway validates the request and then responds with '202 Accepted'

The transaction is then queued for processing.

Once processed, a callback with the final result of the transaction is sent to the merchant system

In order to receive the callback for your transactions, please consider the following:

#### a) On Sandbox

- Register your callback host by specifying the domain as providerCallbackHost when creating your API Keys. On production this will be done via the Account Portal
- Specify the callback URL in each of your `/requesttopay` or `/tranfer` POST
- Use http and not https on sandbox
- Allow PUT & POST on your callback listener host

#### b) On Production

- After Go-live you will be provided a link to log on to your Accounts Portal
- You will be required to register you callback host on the portal when creating your API keys as shown below
- Only https is allowed on production
- Allow PUT & POST on your callback listener host

**Callback Create API User**

The Wallet Platform will only send the callback once. There is no retry on the callback if the Partner system does not respond. A merchant system can, in cases where a callback was not received , poll for the transaction status as described in the GET method

## Error Code

Transfer is used for transferring money from the provider account to a customer.

### 8. What are the common error codes you may expect?

- The error codes are categorized as follows (**Common Error Codes**, **Preapproval Error Codes**, **RequestToPay Error Codes**, **Transfer Error Codes** and **Validate Account Holder Error Codes**)
- The API User and API Key are used to grant access to the wallet system applicable to a specific country
- More information on error codes can be found under the documentation section

## Support

### 9. How do I get support and join the developer community?

- Select the 'contact support' button
- Select a country from the drop-down list
- Choose WhatsApp and join the developer group - start chatting
- Or connect via Skype

## On-Boarding

### 10. What steps do I need to follow go live?

- Select the 'Go-Live' option on portal
- Select Operating country from predefined list to take products Live in that Operating country
- Choose a Package and Product set
- Provide KYC Information for business owner and business details
- Download, complete and submit KYC documents as well as signed contract
- Submit documents through the Sandbox Portal for Vetting and Approval
- Access to the partner portal granted for you to create the API User and API Key

## MoMo API Developer Community

Join the MoMo API Developer LinkedIn community and be the first to learn about APIs, events, and news relevant to you for accurate and deeper understanding of the APIs.

Let's learn, collaborate, and get insights from the developer community to take your business to the next level using MTN MoMo APIs.