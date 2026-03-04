# Pesapal Plugin Installation Guides

## PrestaShop Installation Guide

### Step 1
- Download our pesapal_prestashop_module_8.1.0 zipped file, unzip it, then inside the file locate the Pesapal folder and zip it.

### Step 2
- Log in to your PrestaShop administration panel (e.g., http://yourdomain.com/admin).

### Step 3
- Go to Modules, Module Manager. Click on the "Upload a Module" button.

### Step 4
- Browse for the module's downloaded compressed file on your local machine and select the Pesapal zipped file from Step 1.

### Step 5
- After a successful upload, "Module installed!" click on "Configure" to finish the installation.

- **Live:** Enter the Consumer Key & Consumer Secret. You should have received these from the Pesapal registration email. If you lost them, log in to your Pesapal merchant account, scroll to the bottom of the dashboard to find them.
- **Demo:** To use our Demo, you will have to use our demo consumer keys and secret available here: https://developer.pesapal.com/api3-demo-keys.txt

- Save Settings, then proceed to test the gateway on your store.

---

## WooCommerce Installation Guide

This detailed step by step process below explains how to add Pesapal to your woocommerce Shop to enable you to accept payments using Mobile money (MPESA, Airtel, Voda MPESA, Tigo Pesa, Various Mobile banking apps) and Cards (Visa, MasterCard and American Express).

### Step 1: Download the plugin

Download our Pesapal woo-commerce plugin from our official plugins to a known location, preferably your desktop for easy browsing.

**PLEASE NOTE:** We recommend you download only the WooCommerce plugin to avoid confusion when setting up. Our latest WooCommerce version to date is v3.1.3

### Step 2: Install the plugin

1. Login in to the admin side of your website. Your website admin link is usually looks like this *https://yourwebsite.com/wp-admin*.
2. Point to Plugins >> Select "Add New" to install the plugin.
3. Select "Upload Plugin" to browse for the plugin from the location you had previously saved the plugin to during step 1 above.
4. After browsing for the file, select "Install Now".
5. After Installing the plugin, Activate it.
6. From your navigation bar, point to WooCommerce >> Settings. From the settings page, select "Payments" Tab
7. You will be able to see Pesapal among the list of payment options you have already added.
8. Select "Manage" to enable and configure/set the integration keys
9. Enable the plugin by checking the "Enable Pesapal Payment" option.
10. Enter your live consumer and secret keys as was sent on your email upon your account creation. If you intend to use demo keys, check the "Use Demo Gateway" option.
11. Make sure you save your changes for you be to be able to receive payments through Pesapal

To set email notifications for IPN, scroll down the page and enter the email addresses you would like to receive IPN notification. **Please note** that this step is optional. Only use it if you wish to track your IPN call

**Note** When payments are completed, you can choose between "Completed" and "Processing" for your WooCommerce order status when setting up our plugin. Simply go to WooCommerce settings > Payments > Pesapal>Mange>Update Paid Orders To to make your selection. This gives you more control over your order management.

### Step 3: Confirm all is well

To do so, go to your shop and checkout a product to see if Pesapal payment option appears

You can now select "Place Order" to see the Pesapal Payment options listed above

---

## Magento Installation Guide

### Step 1: Install the Plugin

1. Copy the Pesapal folder into to app/code directory
2. Run the magento setup upgrade function: bin/magento setup:upgrade

Should the upgrade function fail, click here for a possible solution.

### Step 2: Setup plugin and complete Configurations

Once you have done this, you need to follow these steps to get it working:

1. Create a merchant account (Business account) at https://www.pesapal.com. After registration, Pesapal will send you an email with you consumer keys and consumer secret needed to use on the website.
2. Log into your Magento admin and Clear your cache

Go to System or Stores -> Configuration -> Sales -> Payment Methods and you will see. "Pesapal Express"

3. Set your configurations as below;
   - **Enabled:** YES.
   - **Test API:** NO (If you set this to yes, this means you are using our demo Pesapal API. You will have to use our demo consumer keys and secret available here: https://developer.pesapal.com/api3-demo-keys.txt)
   - **Consumer Key & Consumer Secret:** You should have received this from the pesapal registration mail . If you lose this, login to your Pesapal merchant account, scroll to the bottom of the dashboard to find them.
   - **New order status:** This is the default order status set when a user selects pesapal to "processing". All orders with this status mean the user created an order but pending the payment.

4. Save configurations

---

## WHMCS Installation Guide

Please follow the instructions below to setup the PesaPal gateway module.

### Note

1. The PesaPal gateway module requires the use of modified templates that are provided with this distribution.
2. The templates provided are based on WHMCS 7.1.X ++ and the default theme.

### Step 1: Install the WHMCS Plugin

1. Upload pesapal.php and the pesapal folder to your whmcs's modules/gateways folder.
2. Upload the callback/pesapal.php file to your whmcs's modules/gateways/callback folder.
3. Upload templates/pesapal_callback.tpl and templates/pesapal_iframe.tpl to your template directory. This usually under : templates/six/
4. Enable the PesaPal module in the WHMCS admin area by going to Addons-> Apps & Integrations->Browse->Payments(On the left)->View All->Under Additional Apps click on pesapal to activate then manage. Paste in your administrator username, Consumer Key and Consumer Secret.
5. To get your consumer Key and Consumer Secret, Open a Pesapal business account on www.pesapal.com or Pesapal test credentials.
   - If you opened an account on www.pesapal.com(live account), the key and secret have been sent to the email address you registered with.
   - Find Pesapal test credentials here, https://developer.pesapal.com/api3-demo-keys.txt
   - Ensure when you are done testing the plugin using the demo/sandbox account you switch to the live API.
6. Save configurations.

**NB:** Do not change display name in the configuration.

---

## Shopify Installation Guide

This reading will guide you on how to setup your Shopify Store to accept online payments with Pesapal. Upon completion, your customers will be able to checkout online and pay with the payment options supported in your country such as Visa, Master Card, Amex, MPESA, Airtel Money, Tigo Pesa and others.

### Step 1 - Ensure you have a Pesapal Account

If you already have an account with www.pesapal.com go to Step 2.

In case you have not yet created a Pesapal Business account, you can create a new PesaPal Business account by registering here: Create a Business Account

If you would like guidance on creating an account, you may contact us here

### Step 2 - Find your Consumer Key and Secret

Go to the email address you used to register your Pesapal Business account and search for "**pesapal integration information**". The email should look similar to this:

In case you cannot find this email, you can resend it by going to your Pesapal dashboard, scrolling to the bottom of the page and under Api Credentials, click **RESEND.**

This should resend the consumer key and secret to your email.

### Step 3 - Install the Pesapal App

Open https://apps.shopify.com/pesapal-payments then click **Add App** then you will be directed to a page to confirm installation.

In case you have not yet logged in, you might be prompted to login using your Pesapal Business account **username** and **password**.

If you are not redirected to the application after entering the username and password it may mean your username or password was entered incorrectly of which you should double check your credentials.

Fill in the Shop Details Form with the consumer key and secret from Step 2 above and press save.

Paste your Pesapal Consumer Key and Secret

You will then be redirected back to your Shopify Store Admin Dashboard to activate the Pesapal App.

### Step 4 - Activate the Pesapal App

Scroll to the bottom then Click 'Activate' at the bottom of the page to activate. (Ensure the "Enable Test Mode" option is NOT selected as shown in the screenshot below).

Activate The Pesapal App

### Step 5 - Ensure customers can checkout

Visit your store website. Select an item and checkout. You should be able to see Pesapal as a payment option. Confirm the Pesapal App has been installed correctly by clicking "Pay with Pesapal". You should be directed to a Pesapal page where you can select the various payment methods supported.

### What is Test Mode?

Test mode allows you to checkout and see how the Pesapal payment process works without using real money.

To enable the Pesapal App Test Mode, go to your Store Admin Dashboard → Settings → Payments → Pesapal -> Manage

Scroll to the bottom, Activate "test mode" and press "save"

Then go to your store/shop, add items to your cart, checkout an item and select Pesapal.

You will then see our demo payment page where you can make a "dummy payment" without using real money.

**IMPORTANT:** remember to turn off "test mode" as soon as you are done previewing the check out process. Otherwise your customers will not be able to make payments.

How to Enable Test Mode

In case you see any error, please send an email to developer@pesapal.com and kindy include screenshots so that we can assist you more efficiently.