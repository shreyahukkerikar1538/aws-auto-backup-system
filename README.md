# aws-auto-backup-system
A serverless project using AWS S3, Lambda, and SNS to auto-backup files and send notifications.


## 🛠️ Step-by-Step Setup Guide

### ✅ Step 1: Create S3 Buckets

1. Login to AWS Console.
2. Go to **S3 → Create bucket**.
3. Create two buckets:
   - `source-bucket-shreya`
   - `backup-bucket-shreya`
4. Keep default settings (block public access, SSE-S3 encryption enabled).

---

### ✅ Step 2: Create an SNS Topic for Email Notification

1. Go to **SNS → Topics → Create topic**.
2. Type: **Standard**, Name: `file-backup-alerts`
3. After creating:
   - Click **Create subscription**
   - Protocol: **Email**
   - Endpoint: `your-email@example.com`
   - Confirm subscription via email

---

### ✅ Step 3: Create IAM Role for Lambda

1. Go to **IAM → Roles → Create role**
2. Trusted entity type: **Lambda**
3. Skip attaching permissions for now, name: `lambda-backup-role`
4. Add this inline policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::*/*"
    },
    {
      "Effect": "Allow",
      "Action": "sns:Publish",
      "Resource": "arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:file-backup-alerts"
    }
  ]
}

---

### ✅ Step 4: Create the Lambda Function
1. Go to Lambda > Create function.
2. Name: autoBackupFunction
3. Runtime: Python 3.12
4.Permissions:
    Choose “Use an existing role”
    Select: lambda-backup-role
5.Click Create function
---

### ✅ Step 5: Create the Lambda Function
1.Paste the following code in the Lambda editor(code provided)
2.Click Deploy after saving.

---

### ✅ Step 6: Add Trigger from S3
1. Go to Lambda function → Configuration > Triggers → Click “Add trigger”
2.Select: Trigger type: S3
3.Bucket: source-bucket-shreya
4.Event type: PUT (ObjectCreated:Put)
5.Uncheck recursive invocation box (avoid loops)
6.Click Add

---

### ✅ Step 7: Upload a File for Testing
1. Go to S3 → source-bucket-shreya → Upload
2.Upload a test file like testfile.txt
3.Once uploaded: Lambda gets triggered
4.File is copied to backup-bucket-shreya
5.You receive an email via SNS









