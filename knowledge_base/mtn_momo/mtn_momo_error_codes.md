# Error Codes

MoMo OpenAPI Team is thrilled to announce that we've been listening to your feedback, and as a result, we've made significant updates to improve the failure handling with MoMoOpenAPI experience for developers, businesses, and customers.

## Improved Failure Reasons and Error Codes

In our ongoing effort to provide a seamless and intuitive experience, we've revamped our failure reasons and error codes. These updates ensure that error messages are clearer, more concise, and provide actionable insights. This enhancement enables developers and businesses to quickly identify and resolve issues, reducing friction and improving overall efficiency.

## Benefits for all

These updates bring numerous benefits to the MoMoOpenAPI ecosystem, including:

1. **Enhanced Customer Experience:** Improved failure reasons and new actions lead to better, more seamless customer experiences.
2. **Increased Efficiency:** Developers and businesses can now manage MoMo customer experiences more efficiently, reducing time and resources spent on issue resolution.
3. **Reduced Friction:** Updated error codes and messages reduce friction, making it easier to resolve issues and get back to business as usual.

## Common Error Codes

### NOT_ENOUGH_FUNDS
**Description:** The payer does not have enough funds.

**Action:** Notify the payer of the total amount with fees before initiating debit, and also to ensure availability of the MoMo funds

### PAYER_NOT_FOUND
**Description:** Payer does not exist

**Action:** Before initiating debit, use the Get accountholder Status to confirm the payer has an active MoMo Wallet

### TRANSACTION_NOT_FOUND
**Description:** The transaction could not be found

**Action:** The transaction could not be found

### PAYEE_NOT_ALLOWED_TO_RECEIVE
**Description:** The payee is unable to receive funds.

**Action:** The payee is unable to receive funds, due to a non active wallet status. If encountered request customer for an alternative MoMo number.

### SENDER_ACCOUNT_NOT_ACTIVE
**Description:** SENDER ACCOUNT NOT ACTIVE

**Action:** The MoMo wallet used for the transfer has not been activated. Please contact your account manager in your respective country to activate the wallet for transactions

### COULD_NOT_PERFORM_TRANSACTION
**Description:** Transaction Not Completed

**Action:** Debit transactions have a 5-minute approval window. If the transaction times out, please retry the transaction to complete the debit

### PAYER_LIMIT_REACHED
**Description:** The payer's limit has been breached.

**Action:** Customer's wallet has reached its set limits for debits, which vary by country. To resolve this, the customer must either reduce the debit amount or use another MoMo wallet

### PAYEE_LIMIT_REACHED
**Description:** The payee's limit has been breached.

**Action:** Customer's wallet has reached its set limits for transfers, which vary by country. To resolve this, the customer must either reduce the transfer amount or share another MoMo wallet

### RESOURCE_ALREADY_EXIST
**Description:** Duplicated reference id. Creation of resource failed.

**Action:** Error implies that the X-Reference-Id header in your financial API POST request is duplicated To resolve this issue, you need to ensure that each financial API POST request has a unique X-Reference-Id header in UUID Version 4 format.

### PAYEE_NOT_FOUND
**Description:** Payee does not active

**Action:** Error generated for Debit requests when the business account is blocked

### VALIDATION_ERROR
**Description:** Request failing Validation

**Action:** Validation failures can occur due to incorrect data types, unsupported decimals, empty fields, incorrect field lengths, unsupported currencies, and invalid payer messages or notes (which cannot be null and must be within 128 characters).