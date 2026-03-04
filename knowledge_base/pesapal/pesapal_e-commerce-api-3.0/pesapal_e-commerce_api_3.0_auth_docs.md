# Authentication

## Authentication Endpoint - `Post Request`

Pesapal's API Authentication requests are done via a POST request.

Your Pesapal merchant **consumer_key** and **consumer_secret** will be used to generate an access token.

This access token is valid for a maximum period of **5 minutes.** Use this token (sent as a Bearer Token) to access all other Pesapal API 3.0 endpoints.

The URL to our token generation API is either:

- **Sandbox/Demo URL:** https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken
- **Production/Live URL:** https://pay.pesapal.com/v3/api/Auth/RequestToken

## HTTP Request Headers

**Accept:** The response format, which is required for operations with a response body. **Content-Type:** The request format, which is required for operations with a request body.

| Parameter | Required | Description |
|-----------|----------|-------------|
| Accept | `Required` | Should be set to `application/json` |
| Content-Type | `Required` | Should be set to `application/json` |

## Request Parameters

Your live/production **consumer_key** and **consumer_secret** will be sent to your merchant email on opening a business/merchant account.

Please click here to open a live/production business account.

Click here to download test credentials to use while connecting to our **demo/sandbox** API.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| consumer_key | String | `Required` | The consumer_key parameter must be set to `merchant consumer_key` |
| consumer_secret | String | `Required` | The consumer_secret parameter must be set to `merchant consumer_secret.` |

## Sample Request

```json
{
    "consumer_key": "xxxxx",
    "consumer_secret": "xxxxxx"
}
```

## Response Parameters

| Name | Type | Description |
|------|------|-------------|
| token | String | The access token string as issued by the server. The access token issued will have permission to invoke all Pesapa API operations. |
| expiryDate | String | Date and time the token will expire. The access token usually expires after 5mins - `UTC` |
| error | Object | Error object |
| status | String | Response code |
| message | String | A brief description about the response received. |

## Sample Response

```json
{
    "token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYa",
    "expiryDate": "2021-08-26T12:29:30.5177702Z",
    "error": null,
    "status": "200",
    "message": "Request processed successfully"
}
```