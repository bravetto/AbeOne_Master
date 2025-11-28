# 📧 EMAIL ANALYSIS - QUICK SETUP

To run the email convergence analysis, you need to provide email credentials. Here are your options:

## Option 1: Quick Environment Variables (Fastest)

```bash
# For Gmail (use App Password - see below)
export EMAIL_ADDRESS='your@gmail.com'
export EMAIL_REPLACE_ME

# Then run:
python3 scripts/analyze_email_convergence.py
```

### Get Gmail App Password:
1. Go to: https://myaccount.google.com/apppasswords
2. Select "Mail" → "Other (Custom name)"
3. Enter "Email Analysis Script"
4. Copy the 16-character password
5. Use that as EMAIL_PASSWORD

## Option 2: Sign in to 1Password First

```bash
# Sign in to 1Password
eval $(op signin)

# Make sure you have an email/Gmail item in 1Password with:
# - Email address field
# - Password field

# Then run:
python3 scripts/analyze_email_convergence.py
```

The script will automatically find and use your email credentials from 1Password.

## Option 3: Interactive Mode

```bash
python3 scripts/analyze_email_convergence.py
```

Then enter your credentials when prompted.

---

## What Happens Next

Once credentials are provided, the script will:
1. ✅ Fetch emails from the last 3 days
2. ✅ Identify AI newsletters
3. ✅ Analyze for convergence opportunities
4. ✅ Analyze for emergence opportunities
5. ✅ Generate JSON and Markdown reports

---

**Ready to run?** Set up credentials using one of the options above, then run:
```bash
python3 scripts/analyze_email_convergence.py
```

