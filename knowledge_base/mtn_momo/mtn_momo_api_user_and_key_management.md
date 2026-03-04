# MoMo API Documentation

## API User and Key Management

### Authentication

There are two credentials used in the Open API:

1. **Subscription Key**
2. **API User and API Key**

The subscription key is used to give access to APIs in the API Manager portal. A user is assigned a subscription key when the user subscribes to products in the API Manager Portal.

The API User and API Key are used to grant access to the wallet system in a specific country. API user and Key are wholly managed by the user through Partner Portal.

Users are allowed to generate/revoke API Keys through the Partner Portal.

However, on Sandbox Environment a Provisioning API is exposed to enable users to generate their own API User and API Key for testing purposes only.

### Subscription Key

The subscription key is part of the header of all requests sent to the API Manager. The subscription key can be found under user profile in the API Manager Portal.

The subscription key is assigned to the `Ocp-Apim-Subscription-Key` parameter of the header.

### API User and API Key for OAuth 2.0

The API user and API key are provisioned differently in the sandbox and production environment.

In the Sandbox a provisioning API is used to create the API User and API Key, whereas in the production environment the provisioning is done through the User Portal.

The sections below describe the different steps required in creating API User and API key in Sandbox and Production Environments.

## Create API User

1. The Provider sends a `POST {baseURL}/apiuser` request to Wallet platform.
2. The Provider specifies the UUID Reference ID in the request Header and the subscription Key
3. Reference ID will be used as the User ID for the API user to be created.
4. Wallet Platform creates the User and responds with 201

### Example

**Request**
```http
POST {baseURL}/apiuser HTTP/1.1
Host: momodeveloper.mtn.com
X-Reference-Id: c72025f5-5cd1-4630-99e4-8ba4722fad56
Ocp-Apim-Subscription-Key: d484a1f0d34f4301916d0f2c9e9106a2

{
  "providerCallbackHost": "clinic.com"
}
```

**Response**
```http
201 Created
```

## Create API Key

1. The Provider sends a `POST {baseURL}/apiuser/{APIUser}/apikey` request to Wallet platform.
2. The Provider specifies the API User in the URL and subscription Key in the header.
3. Wallet Platform creates the API Key and responds with 201 Created with the newly Created API Key in the Body.
4. Provider now has both API User and API Key created.

### Example

**Request**
```http
POST {baseURL}/apiuser/c72025f5-5cd1-4630-99e4-8ba4722fad56/apikey HTTP/1.1
Host: momodeveloper.mtn.com
Ocp-Apim-Subscription-Key: d484a1f0d34f4301916d0f2c9e9106a2
```

**Response**
```http
HTTP/1.1 201 Created
Date: Wed, 10 Oct 2018 09:16:15 GMT
Content-Type: application/json;charset=utf-8
Content-Length: 45

{
  "apiKey": "f1db798c98df4bcf83b538175893bbf0"
}
```

## GET API User Details

It is possible to fetch API user details such as Call Back Host. However, it is not possible to fetch the API key. Provider shall be required to generate a new Key should they lose the existing one.

1. The Provider sends a `GET {baseURL}/apiuser/{APIUser}` request to Wallet platform.
2. The Provider specifies the API User in the URL and subscription Key in the header.
3. Wallet Platform responds with 200 OK and details of the user.

**Note:** TargetEnvironment is preconfigured to sandbox in the Sandbox environment, therefore Providers will not have the option of setting it to a different parameter.

### Example

**Request**
```http
GET {baseURL}/apiuser/c72025f5-5cd1-4630-99e4-8ba4722fad56
Host: momodeveloper.mtn.com
Ocp-Apim-Subscription-Key: d484a1f0d34f4301916d0f2c9e9106a2
```

**Response**
```http
HTTP/1.1 200 Accepted
Date: Wed, 10 Oct 2018 09:16:15 GMT

{
  "providerCallbackHost": "clinic.com",
  "targetEnvironment": "sandbox"
}
```

## OAuth 2.0

The Open API uses OAuth 2.0 token for authentication of request. User will request an access token using Client Credential Grant according to RFC 6749. The token received is according to RFC 6750 Bearer Token.

The API user and API key are used in the basic authentication header when requesting the access token. The API user and key are managed in the Partner GUI for the country where the account is located. The Partner can create and manage API user and key from the Partner GUI.

In the Sandbox, the API Key and API User are managed through the Provisioning API.

The received token has an expiry time. The same token can be used for transactions until it expires. A new token is requested by using the `POST /token` service in the same way as the initial token. The new token can be requested for before the previous one has expired to avoid authentication failure due to expired token.

**Important:** The token must be treated as a credential and kept secret. The party that have access to the token will be authenticated as the user that requested the token.

### Authentication Flow

The below sequence describes the flow for requesting a token and using the token in a request:

1. Provider system requests an access token using the API Key and API user as authentication.
2. Wallet platform authenticates credentials and responds with the access token
3. Provider system will use the access token for any request that is sent to Wallet Platform, e.g. `POST /requesttopay`

**Note:** The same token shall be used if it is not expired.

## API Methods

The API uses POST, GET, PUT methods. This section gives an overview of the interaction sequence used in the API and the usage of the methods.

### POST

POST method is used for creating a resource in Wallet Platform. The request includes a reference id which is used to uniquely identify the specific resource that are created by the POST request. If a POST is using a reference id that is already used, then a duplication error response will be sent to the client.

**Example:** `POST /requesttopay`

The POST is an asynchronous method. The Wallet Platform will validate the request to ensure that it is correct according to the API specification and then answer with HTTP 202 Accepted. The created resource will get status PENDING. Once the request has been processed the status will be updated to SUCCESSFUL or FAILED. The requester may then be notified of the final status through callback.

### GET

GET is used for requesting information about a specific resource. The URL in the GET shall include the reference of the resource. If a resource was created with POST then the reference id that was provided in the request is used as the identity of the resource.

**Example:**
- `POST /requesttopay` request is sent with `X-Reference-Id = 11377cbe-374c-43f6-a019-4fb70e57b617`
- `GET /requesttopay/11377cbe-374c-43f6-a019-4fb70e57b617` will return the status of the request.

### PUT

The PUT method is used by the Open API when sending callbacks. Callback is sent if a callback URL is included in the POST request. The Wallet Platform will only send the callback once. There is no retry on the callback if the Partner system does not respond. If the callback is not received, then the Partner system can use GET to validate the status.