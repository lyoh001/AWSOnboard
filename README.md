# AWS - CDK Stack
## 1. Introduction
### 1.1	Overview

The following CDK stack will deploy the following resources.
- API Gateway
- Lambda
- DynamoDB
- SNS topic and SMS subscription
- SQS
- S3 bucket
- WAF


## 2 Logical Architecture
### 2.1	Logical System Component Overview
![Figure 1: Logical Architecture Overview](./.images/workflow.png)
1. WAF integration with APIGW.
2. Invoke GET rest api via APIGW.
3. Lambda will perform business logic.
4. Lambda will
    - Write to DynamoDB.
    - Write to S3.
    - Send msg to SNS.
5. SNS will send SMS to mobile for alert.





