# Build a Simple Echo Buttons Skill in ASK Python SDK
<img src="https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/quiz-game/header._TTH_.png" />

[![Voice User Interface](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/navigation/1-locked._TTH_.png)](./1-voice-user-interface.md)[![Lambda Function](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/navigation/2-on._TTH_.png)](./2-lambda-function.md)[![Connect VUI to Code](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/navigation/3-off._TTH_.png)](./3-connect-vui-to-code.md)[![Testing](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/navigation/4-off._TTH_.png)](./4-testing.md)

## Prepare the Code for Deployment
We have provided the code for this skill on [here](../lambda/py). To properly upload this code to Lambda, you'll need to perform the following:

1. This skill uses the [ASK SDK for Python](https://github.com/alexa/alexa-skills-kit-sdk-for-python) for development. The skill code is provided in the [hello_buttons.py](../lambda/py/hello_buttons.py), and the dependencies are mentioned in [requirements.txt](../lambda/py/requirements.txt). Download the contents of the [lambda/py](../lambda/py) folder.

2. On your system, navigate to the lambda folder and install the dependencies in a new folder called “skill_env” using the following command:

  ```
  pip install -r py/requirements.txt -t skill_env
  ```

3. Copy the contents of the `lambda/py` folder into the `skill_env` folder.

  ```
  cp -r py/* skill_env/
  ```

4. Zip the contents of the `skill_env` folder. Remember to zip the **contents** of the folder and **NOT** the folder itself. We will deploy this code in the following section after setting up the Lambda function.

## Setting Up A Lambda Function Using Amazon Web Services

In the [first step of this guide](./1-voice-user-interface.md), we built the Voice User Interface (VUI) for our Alexa skill.  On this page, we will be creating an AWS Lambda function using [Amazon Web Services](http://aws.amazon.com).  You can [read more about what a Lambda function is](http://aws.amazon.com/lambda), but for the purposes of this guide, what you need to know is that AWS Lambda is where our code lives.  When a user asks Alexa to use our skill, it is our AWS Lambda function that interprets the appropriate interaction, and provides the conversation and button actions back to the user(s).

### Create the Lambda Function

1.  Go to **[AWS](https://aws.amazon.com)** and sign in to the console. If you don't already have an account, you will need to create one.  [If you don't have an AWS account, check out this quick walkthrough for setting it up](https://github.com/alexa/alexa-cookbook/blob/master/guides/aws-security-and-setup/set-up-aws.md).

2.  Click **Services** at the top of the screen, and type "Lambda" in the search box.  You can also find Lambda in the list of services.  It is in the "Compute" section.

    [![Lambda](./images/lambda.png)](https://console.aws.amazon.com/lambda/home)

3.  **Check your AWS region.** AWS Lambda only works with the Alexa Skills Kit in these regions: US East (N. Virginia), US West (Oregon), Asia Pacific (Tokyo)  and EU (Ireland).  Make sure you choose the region closest to your customers.

    ![Check Region](./images/useast.png)

4.  **Click the orange "Create function" button.** It should be near the top of your screen.  (If you don't see this button, it is because you haven't created a Lambda function before.  Click the blue "Get Started" button near the center of your screen.)

    ![Create lambda function](./images/create-function.png)

5.  There are three boxes labeled "Author from scratch", "Blueprints" and "Serverless Application Repository". **Click the radio button in the box titled  "Author From Scratch"**

6. In the "Author from Scratch" section give you funcation a **name**, select **Python 3.6** as the **Runtime**, and select **Create a custom role** for the **Role**.

7. A new window or tab will appear, taking you to the creation of a new IAM role. This sets up permissions for execution of your Lambda. In the **IAM Role** selection choose **lambda_basic_execution** and for **Policy** select **Create a new Role Policy**.

   ![Role](./images/role.png)

8. Click the **Allow** button to return to the previous screen.

9. Click the **Create Function** button.

   ![Create Lambda](./images/create-lambda.png)

10. You are now on the screen that defines your Lambda. Under the **Add Triggers** section on the left select **Alexa Skills Kit** to allow your skill to call this Lambda.

    ![ASK Trigger](./images/ask.png)

11. Under **Configure Triggers**, at the bottom of the page, select **Disable** for **Skill ID Verification**. Next click the **Add** button in the lower right corner.

    **Note:** If you wish to secure this Lambda function in the future there is a guide  [here](https://github.com/alexa/alexa-cookbook/blob/master/guides/aws-security-and-setup/secure-lambda-function.md)

12. Select your Lambda at the top middle of the page (above the boxes for Alexa Skills Kit and Amazon Cloudwatch Logs) and then scroll down the page until you see a section called **Function code**.

    ![Lambda Selection](./images/buttons-trivia.png)

13. Change the **Code entry type** to **Upload a ZIP** and select the zip you created in the **Prepare the Code for Deployment** section.

    ![Function Code](./images/function-code.png)

    *(Optional)* Follow the ASK Python SDK [Getting Started](https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/GETTING_STARTED.html#adding-the-ask-sdk-for-python-to-your-project) documentation, to check alternative ways of installing the sdk and deploying to AWS Lambda console.

14. In the same section change the **Handler** name to **hello_buttons.handler**

15. Save the Lambda by clicking the **Save** button in the upper right corner of the screen.

16. (Optional) Click the **Configure test events** dropdown menu on the top of the page.

    1. Select 'Alexa Start Session' from the 'Event Template' dropdown.
    2. Type `LaunchRequest` into the 'Event Name' field.
    3. Click the orange 'Create' button at the bottom of the page
    4. Click the **Test** button at the top of the page.
    5. You should see a light green box with the message: *Execution result: succeeded* at the top of the page.

17. You should see the Amazon Resource Name (ARN) a unique identifier for this function in the top right corner of the page. **Copy the ARN value for this Lambda function** for use in the next section of the guide.

    ![Copy ARN](./images/arn.png)


[![Next](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/general/buttons/button_next_connect_vui_to_code._TTH_.png)](./3-connect-vui-to-code.md)
