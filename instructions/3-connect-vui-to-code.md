# Build a Simple Echo Buttons Skill in ASK Python SDK
<img src="https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/quiz-game/header._TTH_.png" />

[![Voice User Interface](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/navigation/1-locked._TTH_.png)](./1-voice-user-interface.md)[![Lambda Function](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/navigation/2-locked._TTH_.png)](./2-lambda-function.md)[![Connect VUI to Code](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/navigation/3-on._TTH_.png)](./3-connect-vui-to-code.md)[![Testing](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/navigation/4-off._TTH_.png)](./4-testing.md)

## Connecting Your Voice User Interface To Your Lambda Function

On the [first page](./1-voice-user-interface.md) of this guide, we created a voice user interface for the intents and utterances we expect from our users.  On the [second page](./2-lambda-function.md), we created a Lambda function that contains all of our logic for the skill.  On this page, we need to connect those two pieces together.

1.  Go back to the **[Amazon Developer Portal](https://developer.amazon.com/edw/home.html#/skills/list)** and select your skill from the list. You may still have a browser tab open if you started at the beginning of this tutorial.

2. Select the **Endpoint** tab on the left side navigation panel.

    ![Endpoint Tab](./images/endpoint-tab.png)

3.  Select the **AWS Lambda ARN** option for your endpoint. You have the ability to host your code anywhere that you would like, but for the purposes of simplicity and frugality, we are using AWS Lambda. ([Read more about Hosting Your Own Custom Skill Web Service](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/developing-an-alexa-skill-as-a-web-service).)  With the AWS Free Tier, you get 1,000,000 free requests per month, up to 3.2 million seconds of compute time per month. Learn more at [aws.amazon.com/free](https://aws.amazon.com/free/).  In addition, Amazon now offers [AWS Promotional Credits for developers who have live Alexa skills that incur costs on AWS related to those skills](https://developer.amazon.com/alexa-skills-kit/alexa-aws-credits).

4.  Paste your Lambda's ARN (Amazon Resource Name) into the textbox provided for **Default Region**.

    ![Endpoint](./images/endpoint.png)

5. Click the **Save Endpoints** button at the top of the main panel.

    ![Save Endpoint](./images/save-endpoint.png)

[![Next](https://m.media-amazon.com/images/G/01/mobile-apps/dex/alexa/alexa-skills-kit/tutorials/general/buttons/button_next_testing._TTH_.png)](./4-testing.md)