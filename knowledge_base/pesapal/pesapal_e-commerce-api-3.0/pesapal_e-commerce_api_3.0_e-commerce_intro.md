# Pesapal API 3.0

Welcome to **Pesapal API 3.0**. Getting started with Pesapal is quick and easy!

In this release, you will learn how to use our API endpoints to access Pesapal services. Our APIs are built on **REST (Representational State Transfer)** thus our data entities are represented as HTTP resources and are accessed using HTTP verbs **GET** and **POST**. Requests and responses are **JSON encoded**.

Find information about integrating your website with Pesapal. This documentation includes sample codes for each API we have.

**Postman URL**: https://documenter.getpostman.com/view/6715320/UyxepTv1

## Base URLs

| Environment | URL |
|-------------|-----|
| Sandbox | https://cybqa.pesapal.com/pesapalv3 |
| Live | https://pay.pesapal.com/v3 |

## Error Object

In case an error occurs during any API call, Pesapal will respond with a json string in the following format:

```json
{
    "error": {
        "type": "error_type",
        "code": "response_code",
        "message": "Detailed error message goes here..."
    }
}
```
