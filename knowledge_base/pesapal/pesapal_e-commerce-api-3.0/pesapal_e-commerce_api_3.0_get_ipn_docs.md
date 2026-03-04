# Get Registered IPNs

## Get Registered IPNs Endpoint - `Get Request`

This endpoint allows you to fetch all registered IPN URLs for a particular Pesapal merchant account.

The URL to our GetIPNList API is either:

- **Sandbox/Demo URL:** https://cybqa.pesapal.com/pesapalv3/api/URLSetup/GetIpnList
- **Production/Live URL:** https://pay.pesapal.com/v3/api/URLSetup/GetIpnList

## Authentication

**Bearer Token:** Use token generated during authentication.

## Request

No payload is required.

## Response Parameters

| Name | Type | Description |
|------|------|-------------|
| url | String | The notification url Pesapal with send a status alert to. |
| created_date | String | Date and time the IPN URL was registered `UTC` |
| ipn_id | String | A unique identifier that's liked to the IPN endpoint URL. `GUID` |
| error | Integer | |
| status | String | Response code. |

## Sample Response

```json
[
    {
        "url": "https://www.myapplication.com/ipn",
        "created_date": "2022-03-03T17:29:03.7208266Z",
        "ipn_id": "e32182ca-0983-4fa0-91bc-c3bb813ba750",
        "error": null,
        "status": "200"
    },
    {
        "url": "https://ipn.myapplication.com/application2",
        "created_date": "2021-12-05T04:23:45.5509243Z",
        "ipn_id": "c3bb813ba750-0983-4fa0-91bc-e32182ca",
        "error": null,
        "status": "200"
    }
]
```