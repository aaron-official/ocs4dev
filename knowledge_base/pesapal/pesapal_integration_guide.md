# Integration Guide

We have outlined below the steps involved in integrating a website with PesaPal. To view samples and the complete API reference, please click **here**.

## Step 1: Build your site / application that will accept payments from your customers

The site / application will:

- Collect customer information, such as First Name, Last Name and Email Address
- Collect payment information, such as Amount and Currency

**Please Note:** the information you collect will be dependent on your site / application requirements. But some information is required by PesaPal

## Step 2: Package the request to post to PesaPal

Once you have the customer and payment details, you need to package it to send to PesaPal.

This involves a few steps as we need to ensure that the communication between your site and PesaPal happens in a secure manner.

PesaPal uses **JSON Web Tokens (JWT)** to make sure that no one else interfers with the request you post to PesaPal

## Step 3: Post the request to PesaPal and load the PesaPal payments page

When a request is posted, PesaPal will display a payments page. This is where the customer will make the payment.

You can embed this payments page directly in your site, providing a seamless experience to your customers. You can do this by inserting an IFrame on the page on your site customers land on when they click pay or checkout.

## Step 4: Display a post-payment page to your customer

Once the customer has completed the payment proces on PesaPal, they will be redirected to a page on your site.

You can use this page to inform the customer that their payment is being processed.

Optionally, you can also query PesaPal at this point to see if the payment has completed succesfully, has failed, or is still being processed.

## Step 5: Query PesaPal for payment status

One last step! When you receive an IPN notification from PesaPal, you need to query PesaPal for the payment status using the orderTrackingId that was sent with the notification

A **PENDING** status indicates that the payment is being processed by PesaPal and the final status of payment (**COMPLETED** or **FAILED**) is not yet known.