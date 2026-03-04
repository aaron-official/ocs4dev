# MoMo API

## Common Error Codes

The complete definitions of error codes are found in the swagger documentation. Below is the list of error codes available.

### Common Error Codes

| HTTP Code | Error Response Code | Description | Action |
|-----------|-------------------|-------------|--------|
| **409** | `RESOURCE_ALREADY_EXIST` | Duplicated Reference ID. Every request must have a unique reference ID; using an ID of the previous request will result in this error response. | Check **X-Reference ID** used is unique and is in **UUID V4** format |
| **401** | `ACCESS DENIED DUE TO INVALID SUBSCRIPTION KEY` | Authentication failed. Credentials invalid. Header **Ocp-APIM-Subscription-Key** value is incorrect. | Check the User Profile Section to verify the related product subscription key is used. **Collection**, **Disbursement** and **Remittance** have different subscription keys. If the primary key doesn't work, try the secondary key. Contact MTN support if both provided keys aren't working.<br>- Sandbox subscription key are located in https://momodeveloper.mtn.com/developer<br>- Production subscription key are located in https://momoapi.mtn.com/developer |
| **404** | `RESOURCE NOT FOUND` | Reference ID not found. Requested resource does not exist. Predominantly occurs with **Get Status API** and implies that the requested reference ID does not exist. This results in the Request to Debit or Transfer transaction being unsuccessful. | Check if the original request to pay or the transfer (disbursement) operation was successful with response code **202**. |
| **400** | `REQUEST REJECTED/ BAD REQUEST` | Bad request. Request does not follow the specification. | This relates to any of the below scenarios:<br>- Incorrect/wrong values in the headers, and/or the **X-ref ID** does not meet **UUID Version 4**.<br>- Inputting a Body in an API that is not supported e.g. `/Token API`<br>- Having unsupported special characters in the Body request for example an apostrophe (`'`).<br>- Invalid currency – needs to match the target environment currency.<br>- More than 160 characters in the note and message; explore utilizing the notification API for increased number of characters.<br>- The URL posted to needs to reviewed e.g. incorrect number of forward slashes (`///`). |
| **403** | `FORBIDDEN IP` | Authorization failed. IP not authorized to utilize **Disbursement API**. | Share your originating Public IP from which the APIs are called with your MTN Account Manager. |
| **500** | `NOT_ALLOWED` | Authorization failed. User does not have permission. The account authenticated with the Request via Token is restricted. | Contact your MTN Account Manager. |
| **500** | `NOT_ALLOWED_TARGET_ENVIRONMENT` | Value passed in header **X-Target-Environment** is incorrect | Use the correct **X-Target-Environment** corresponding to below country:<br>- MTN Uganda = `mtnuganda`<br>- MTN Ghana = `mtnghana`<br>- MTN Ivory Coast = `mtnivorycoast`<br>- MTN Zambia = `mtnzambia`<br>- MTN Cameroon = `mtncameroon`<br>- MTN Benin = `mtnbenin`<br>- MTN Congo = `mtncongo`<br>- MTN Swaziland = `mtnswaziland`<br>- MTN GuineaConakry = `mtnguineaconakry`<br>- MTN SouthAfrica = `mtnsouthafrica`<br>- MTN Liberia = `mtnliberia`<br><br>For Test Environment = `sandbox` |
| **500** | `INVALID_CALLBACK_URL_HOST` | Callback URL with different host name to configured for API User. Check the Host of the Call Back URL in the request header; this needs to match what was configured on the partner portal when creating the API user and Key. | Host needs to be configured using **Hostname** and not **IP address**. |
| **500** | `INVALID_CURRENCY` | Currency not supported on the requested account | Use **Currency Code** specific to the Country. |
| **503** | `SERVICE_UNAVAILABLE` | Service temporary unavailable, try again later | Enquire with MTN Support. |

### Common Error Responses with Action

| Type | Description | Action |
|------|-------------|--------|
| `INTERNAL_PROCESSING_ERROR` | Default or Generic error code used when there is no specific error mapping. This predominantly occurs due to insufficient customer funds to complete the transaction. Also related to service denied or Wallet Platform is not reachable. | Advice customer to ensure they have sufficient funds to complete the transaction. Also request the customer to retry the transaction. If the problem still occurs with sufficient customer funds, please contact your MTN Account Manager for further investigation. |
| `PAYEE_NOT_FOUND` | The **MSISDN** being paid to is invalid. | **MSISDN** format must include country code. **MSISDN** is not registered for Mobile Money Service. |
| `PAYER_NOT_FOUND` | **MSISDN** of the number from whom the money was requested in invalid. | **MSISDN** format must include country code. **MSISDN** is not registered for Mobile Money Service. |
| `COULD_NOT_PERFORM_TRANSACTION` | This can be attributed to transaction timeout. This predominantly occurs with a delay to approve a transaction within the given time frame (5 minutes). | Advise customer to try again and approve transaction within **5 minutes**. |

---
