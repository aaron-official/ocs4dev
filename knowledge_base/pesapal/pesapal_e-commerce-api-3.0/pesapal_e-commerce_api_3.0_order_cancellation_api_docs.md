# Order Cancellation API

## Definitions

The Order Cancellation API enables you to revoke a previously placed order request that remains incomplete on our end. This API facilitates the cancellation of orders that have encountered failures or are pending transactions.

However, there are certain constraints associated with cancelling a prior request:

1. Cancellation is exclusively supported for failed or pending payments.
2. A cancellation request can only be submitted once.
3. Cancellation is not allowed for payments that have already been processed.

You can access our Cancel Order API via the endpoints provided below:

- **Sandbox/Demo URL:** https://cybqa.pesapal.com/pesapalv3/api/Transactions/CancelOrder
- **Production/Live URL:** https://pay.pesapal.com/v3/api/Transactions/CancelOrder

## Authentication

**Bearer Token:** Use token generated during authentication.

## HTTP Request Headers

**Accept:** The response format, which is required for operations with a response body.
**Content-Type:** The request format, which is required for operations with a request body.

| Parameter | Required | Description |
|-----------|----------|-------------|
| Accept | Required | Should be set to `application/json` |
| Content-Type | Required | Should be set to `application/json` |

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| order_tracking_id | Guid | Required | This refers to the original Pesapal Order tracking ID that was returned after submitting your order request earlier during the initial submit order request api call. |

## Sample Request

```json
{
    "order_tracking_id": "xxxxxxxxxxxxxxxxxxxxxxx"
}
```

After successfully cancelling the request, the order shall be cancelled on our systems preventing a customer from making further payments to an already cancelled order.

## Response Parameters

| Name | Type | Description |
|------|------|-------------|
| status | message | 200 – Order Successfully cancelled. 500 – Order could not be cancelled. |
| message | String | A summary of the response received. |

Status **200** mean your request to cancel the order has been processed successfully.

Status **500** mean your request to cancel your order has failed due to one or more reasons as shared earlier on the introduction page above.

## Sample Response

```json
{
    "status": "200",
    "message": "Order successfully cancelled."
}
```

**Important Note:** The Order Cancellation API uses the Pesapal Order Tracking ID to cancel the order. It's important that you store the Pesapal Order Tracking ID that is sent back to your system during your initial order placement stage i.e. on the submit order request endpoint.