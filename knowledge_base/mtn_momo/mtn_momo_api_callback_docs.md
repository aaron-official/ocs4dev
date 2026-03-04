# MoMo API

## Callback

### Setting up a callback URL

**Transfer** and **RequestToPay** APIs are **Asynchronous** in MTN MoMo API Platform

When a merchant system sends a POST of either `/transfer`, or `/requesttopay` APIs, the Gateway validates the request and then responds with **'202 Accepted'**

The transaction is then queued for processing.

Once processed, a callback with the final result of the transaction is sent to the merchant system

In order to receive the callback for your transactions, please consider the following:

#### a) On Sandbox

- Register your callback host by specifying the domain as **providerCallbackHost** when creating your API Keys. On production this will be done via the Account Portal
- Specify the callback URL in each of your `/requesttopay` or `/transfer` POST
- Use **http** and not **https** on sandbox
- Allow **PUT & POST** on your callback listener host

#### b) On Production

- After Go-live you will be provided a link to log on to your **Accounts Portal**
- You will be required to register you callback host on the portal when creating your API keys as shown below
- Only **https** is allowed on production
- Allow **PUT & POST** on your callback listener host

The Wallet Platform will only send the callback **once**. There is no retry on the callback if the Partner system does not respond. A merchant system can, in cases where a callback was not received, poll for the transaction status as described in the **GET method**

Let's look at the **Deposit API** under the product set **Disbursement** for instance.

The are two Deposit APIs - **Deposit-V1** and **Deposit-V2**.

The callback request for **Deposit-V1** can be sent via

```
https://momodeveloper.mtn.com/API-collections#api=disbursement&operation=Deposit-V1
```

The callback received would be of the type **POST**.

### Approved Intermediate CA's for Open API

For Open API callbacks to function, the **3PP Intermediate certificate chains** must be imported on the PG's **tls_keystore** and callback URL's are required to use **https L7 protocol**:

**CN** – Refers to the Common name of the immediate intermediate CA Chain

**Alias** – Name that is used while storing the Certificate in PG's tls_keystore

Below is the list of **Approved Intermediate CA's** that's already available to use:

| Alias | CN |
|-------|-----|
| `GTS_CA_1C3` | CN=GTS CA 1C3; O=Google Trust Services LLC; C=US |
| `Go_Daddy_Secure_Certificate_Authority_-_G2` | CN=Go Daddy Secure Certificate Authority - G2; OU=http://certs.godaddy.com/repository/; O=GoDaddy.com, Inc.; C=US |
| `R3` | CN=R3; O=Let's Encrypt; C=US |
| `Sectigo_RSA_Domain_Validation_Secure_Server_CA` | CN=Sectigo RSA Domain Validation Secure Server CA; O=Sectigo Limited; C=GB |
| `AmazonRCA4` | CN = Amazon Root CA 4,O = Amazon,C = US |
| `AmazonCA1B` | CN = Amazon,OU = Server CA 1B,O = Amazon,C = US |
| `Encryption_Everywhere_DV_TLS_CA_-_G1` | CN=Encryption Everywhere DV TLS CA - G1; OU=www.digicert.com; O=DigiCert Inc; C=US |
| `cPanel,_Inc._Certification_Authority` | CN=cPanel, Inc. Certification Authority; O=cPanel, Inc.; C=US |
| `DigiCert_SHA2_Secure_Server_CA` | CN=DigiCert SHA2 Secure Server CA; O=DigiCert Inc; C=US |
| `GTS_CA_1D4` | CN=GTS CA 1D4; O=Google Trust Services LLC; C=US |
| `Cloudflare_Inc_ECC_CA-3` | CN=Cloudflare Inc ECC CA-3; O=Cloudflare, Inc.; C=US |
| `DigiCert_SHA2_High_Assurance_Server_CA` | CN=DigiCert SHA2 High Assurance Server CA; OU=www.digicert.com; O=DigiCert Inc; C=US |
| `ZeroSSL_RSA_Domain_Secure_Site_CA` | CN=ZeroSSL RSA Domain Secure Site CA; O=ZeroSSL; C=AT |
| `AlphaSSL_CA_-_SHA256_-_G2` | CN=AlphaSSL CA - SHA256 - G2; O=GlobalSign nv-sa; C=BE |
| `RapidSSL_TLS_DV_RSA_Mixed_SHA256_2020_CA-1` | CN=RapidSSL TLS DV RSA Mixed SHA256 2020 CA-1; O=DigiCert Inc; C=US |
| `Thawte_RSA_CA_2018` | CN=Thawte RSA CA 2018; OU=www.digicert.com; O=DigiCert Inc; C=US |
| `GoGetSSL_RSA_DV_CA` | CN=GoGetSSL RSA DV CA; O=GoGetSSL; C=LV |
| `Gandi_Standard_SSL_CA_2` | CN=Gandi Standard SSL CA 2; O=Gandi; C=FR |
| `GlobalSign_RSA_OV_SSL_CA_2018` | CN=GlobalSign RSA OV SSL CA 2018; O=GlobalSign nv-sa; C=BE |
| `DigiCert_TLS_RSA_SHA256_2020_CA1` | CN=DigiCert TLS RSA SHA256 2020 CA1; O=DigiCert Inc; C=US |
| `GeoTrust_RSA_CA_2018` | CN=GeoTrust RSA CA 2018; OU=www.digicert.com; O=DigiCert Inc; C=US |
| `Microsoft_RSA_TLS_CA_02` | CN=Microsoft RSA TLS CA 02; O=Microsoft Corporation; C=US |
| `SSL.com_RSA_SSL_subCA` | CN=SSL.com RSA SSL subCA; O=SSL Corporation; C=US |
| `RapidSSL_TLS_RSA_CA_G1` | CN=RapidSSL TLS RSA CA G1; OU=www.digicert.com; O=DigiCert Inc; C=US |
| `Thawte_EV_RSA_CA_2018` | CN=Thawte EV RSA CA 2018; OU=www.digicert.com; O=DigiCert Inc; C=US |
| `Microsoft_Azure_TLS_Issuing_CA_05` | CN=Microsoft Azure TLS Issuing CA 05; O=Microsoft Corporation; C=US |
| `GeoTrust_TLS_DV_RSA_Mixed_SHA256_2020_CA-1` | CN=GeoTrust TLS DV RSA Mixed SHA256 2020 CA-1; O=DigiCert Inc; C=US |
| `E1` | CN=E1; O=Let's Encrypt; C=US |
| `Sectigo_ECC_Domain_Validation_Secure_Server_CA` | CN=Sectigo ECC Domain Validation Secure Server CA; O=Sectigo Limited; C=GB |
| `COMODO_RSA_Domain_Validation_Secure_Server_CA` | CN=COMODO RSA Domain Validation Secure Server CA; O=COMODO CA Limited; C=GB |
| `entrustl1k_.entrustrootca-g2` | CN = Entrust Certification Authority - L1K,OU = (c) 2012 Entrust\, Inc. - for authorized use only,OU = See www.entrust.net/legal-terms,O = Entrust\, Inc.,C = US |

**NOTE**: In case any Partner's callback URL is not part of the **Approved Intermediate CA's**, callbacks might not work for the said Partners.

---