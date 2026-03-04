# MoMo API

## Sandbox Use Cases

To facilitate testing a set of predefined users and Test accounts are provided. These users and accounts have a predefined test scenario. A developer needs to Signup and Subscribe to a Product before accessing any of the APIs.

In order to test Sandbox Use cases, Merchants/Agents/Partners/Testers needs to use the Sandbox Provisioning Collection and generate the apiuser and apikey and the same needs to be used for testing any of the sandbox Use cases. Existing Partner Accounts created on Partner GUI can't be used for testing the sandbox usecases.

## OAuth Token

OAuth Token is generated from the merchants' API Key and Secret. The API Key and API Secret can be obtained through the provisioning API in Sandbox, as described in the API User and API Key Management section.

## Test Environment

The Target Environment used in Testing is **'Sandbox'**

## Test Currency

The currency used in Sandbox is **EUR**

## Sandbox Use Case

The following Numbers are predefined with respective response for all Testcases.

| Sandbox Use Case | Testing Values |
|------------------|----------------|
| AccountBalanceResponses | Success, AccountNotFound, ZeroBalance, NegativeBalance, NotAllowed, NotAllowedTargetEnvironment, InternalProcessingError, ServiceUnavailable |
| AccountHolderActiveMsisdnNotFound | 46733123450 |
| AccountHolderActiveMsisdnNotActive | 46733123451 |
| AccountHolderActiveMsisdnNotAllowed | 46733123452 |
| AccountHolderActiveMsisdnNotAllowedTargetEnvironment | 46733123453 |
| AccountHolderActiveMsisdnInternalProcessingError | 46733123454 |
| AccountHolderActiveMsisdnServiceUnavailable | 46733123455 |
| AccountHolderActiveEmailNotFound | notfound@email.com |
| AccountHolderActiveEmailNotActive | notactive@email.com |
| AccountHolderActiveEmailNotAllowed | notallowed@email.com |
| AccountHolderActiveEmailNotAllowedTargetEnvironment | notallowedtargetenvironment@email.com |
| AccountHolderActiveEmailInternalProcessingError | internalprocessingerror@email.com |
| AccountHolderActiveEmailServiceUnavailable | serviceunavailable@email.com |
| AccountHolderActivePartyCodeNotFound | 5cecb5a7-8bd0-4f49-87b1-8eb9ecc7b7bc |
| AccountHolderActivePartyCodeNotActive | b0040b3c-b426-4a90-af6e-673e65861cd7 |
| AccountHolderActivePartyCodeNotAllowed | 4d5f500f-c385-4901-9be5-25b6d36ad220 |
| AccountHolderActivePartyCodeNotAllowedTargetEnvironment | d2265f9b-0c22-496d-908f-79a65ad66266 |
| AccountHolderActivePartyCodeInternalProcessingError | 8f548a78-ceb8-4d12-a243-5640b91e91a4 |
| AccountHolderActivePartyCodeServiceUnavailable | 585c07a4-2c80-42f7-9e73-e586b36dee68 |
| RequestToPayPayerFailed | 46733123450 |
| RequestToPayPayerRejected | 46733123451 |
| RequestToPayPayerExpired | 46733123452 |
| RequestToPayPayerOngoing | 46733123453 |
| RequestToPayPayerDelayed | 46733123454 |
| RequestToPayPayerNotFound | 46733123455 |
| RequestToPayPayerPayeeNotAllowedToReceive | 46733123456 |
| RequestToPayPayerNotAllowed | 46733123457 |
| RequestToPayPayerNotAllowedTargetEnvironment | 46733123458 |
| RequestToPayPayerInvalidCallbackUrlHost | 46733123459 |
| RequestToPayPayerInvalidCurrency | 46733123460 |
| RequestToPayPayerInternalProcessingError | 46733123461 |
| RequestToPayPayerServiceUnavailable | 46733123462 |
| RequestToPayPayerCouldNotPerformTransaction | 46733123463 |
| PreApprovalPayerFailed | 46733123450 |
| PreApprovalPayerRejected | 46733123451 |
| PreApprovalPayerExpired | 46733123452 |
| PreApprovalPayerOngoing | 46733123453 |
| PreApprovalPayerDelayed | 46733123454 |
| PreApprovalPayerNotFound | 46733123455 |
| PreApprovalPayerNotAllowed | 46733123456 |
| PreApprovalPayerNotAllowedTargetEnvironment | 46733123457 |
| PreApprovalPayerInvalidCallbackUrlHost | 46733123458 |
| PreApprovalPayerInvalidCurrency | 46733123459 |
| PreApprovalPayerInternalProcessingError | 46733123460 |
| PreApprovalPayerServiceUnavailable | 46733123461 |
| RequestToWithdrawPayerFailed | 46733123450 |
| RequestToWithdrawPayerRejected | 46733123451 |
| RequestToWithdrawPayerExpired | 46733123452 |
| RequestToWithdrawPayerOngoing | 46733123453 |
| RequestToWithdrawPayerDelayed | 46733123454 |
| RequestToWithdrawPayerNotFound | 46733123455 |
| RequestToWithdrawPayerPayeeNotAllowedToReceive | 46733123456 |
| RequestToWithdrawPayerNotAllowed | 46733123457 |
| RequestToWithdrawPayerNotAllowedTargetEnvironment | 46733123458 |
| RequestToWithdrawPayerInvalidCallbackUrlHost | 46733123459 |
| RequestToWithdrawPayerInvalidCurrency | 46733123460 |
| RequestToWithdrawPayerInternalProcessingError | 46733123461 |
| RequestToWithdrawPayerServiceUnavailable | 46733123462 |
| RequestToWithdrawPayerCouldNotPerformTransaction | 46733123463 |
| RefundTransactionNotFound | 1 |
| RefundTransactionFailed | 2 |
| RefundTransactionRejected | 3 |
| RefundTransactionExpired | 4 |
| RefundTransactionOngoing | 5 |
| RefundTransactionDelayed | 6 |
| RefundTransactionNotAllowed | 7 |
| RefundTransactionNotAllowedTargetEnvironment | 8 |
| RefundTransactionInvalidCallbackUrlHost | 9 |
| RefundTransactionInvalidCurrency | 10 |
| RefundTransactionInternalProcessingError | 11 |
| RefundTransactionServiceUnavailable | 12 |
| RefundTransactionCouldNotPerformTransaction | 13 |
| DepositPayerFailed | 46733123450 |
| DepositPayerRejected | 46733123451 |
| DepositPayerExpired | 46733123452 |
| DepositPayerOngoing | 46733123453 |
| DepositPayerDelayed | 46733123454 |
| DepositPayerNotFound | 46733123455 |
| DepositPayerPayeeNotAllowedToReceive | 46733123456 |
| DepositPayerNotAllowed | 46733123457 |
| DepositPayerNotAllowedTargetEnvironment | 46733123458 |
| DepositPayerInvalidCallbackUrlHost | 46733123459 |
| DepositPayerInvalidCurrency | 46733123460 |
| DepositPayerInternalProcessingError | 46733123461 |
| DepositPayerServiceUnavailable | 46733123462 |
| DepositPayerCouldNotPerformTransaction | 46733123463 |
| TransferPayeeFailed | 46733123450 |
| TransferPayeeRejected | 46733123451 |
| TransferPayeeExpired | 46733123452 |
| TransferPayeeOngoing | 46733123453 |
| TransferPayeeDelayed | 46733123454 |
| TransferPayeeNotEnoughFunds | 46733123455 |
| TransferPayeePayerLimitReached | 46733123456 |
| TransferPayeeNotFound | 46733123457 |
| TransferPayeeNotAllowed | 46733123458 |
| TransferPayeeNotAllowedTargetEnvironment | 46733123459 |
| TransferPayeeInvalidCallbackUrlHost | 46733123460 |
| TransferPayeeInvalidCurrency | 46733123461 |
| TransferPayeeInternalProcessingError | 46733123462 |
| TransferPayeeServiceUnavailable | 46733123463 |
| Oauth2CustomScopes | all_info |
| Oauth2AccountHolderNotFound | 46733123450 |
| Oauth2ConsentRejected | 46733123451 |
| Oauth2ConsentPending | 46733123452 |
| Oauth2ConsentExpired | 46733123453 |
| Oauth2ConsentExpiredRefreshToken | 46733123454 |
| Oauth2ConsentRevoked | 46733123455 |
| Oauth2ConsentDeletedScope | 46733123456 |
| Oauth2ConsentAlreadyUsed | 46733123457 |
| Oauth2FinancialNoFunds | 46733123458 |
| Oauth2FinancialPayeeNotFound | 46733123459 |
| Oauth2FinancialConsentMismatch | 46733123460 |
| Oauth2FinancialPayerLimitReached | 46733123461 |
| Oauth2FinancialPayeeNotAllowedToReceive | 46733123462 |
| CashTransferTransactionNotFound | 1 |
| CashTransferTransactionFailed | 2 |
| CashTransferTransactionRejected | 3 |
| CashTransferTransactionExpired | 4 |
| CashTransferTransactionPayeeNotFound | 5 |
| CashTransferTransactionPayeeNotAllowedToReceive | 6 |
| CashTransferTransactionNotAllowed | 7 |
| CashTransferTransactionNotAllowedTargetEnvironment | 8 |
| CashTransferTransactionInvalidCallbackUrlHost | 9 |
| CashTransferTransactionInvalidCurrency | 10 |
| CashTransferTransactionInternalProcessingError | 11 |
| CashTransferTransactionServiceUnavailable | 12 |
| CashTransferTransactionCouldNotPerformTransaction | 13 |

**Note:** Any other number results in Success