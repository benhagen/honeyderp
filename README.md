honeyderp
=========

A very dumb web honeypot.


Use an IAM policy like this to restrict the user to ONLY sending messages:

```
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sqs:GetQueueUrl",
        "sqs:SendMessage"
      ],
      "Resource": [
        "arn:aws:sqs:<FULL ARN GOES HERE>"
      ]
    }
  ]
}
```
