"""
knowledge_base.py
Financial literacy knowledge base — curated documents covering UPI, budgeting,
interest rates, online safety, and personal finance for Indian users.
"""

FINANCIAL_DOCUMENTS = [
    # ── UPI & Digital Payments ───────────────────────────────────────────────
    {
        "id": "upi_001",
        "category": "upi",
        "title": "How to Send Money via UPI",
        "content": """
UPI (Unified Payments Interface) is a real-time payment system developed by NPCI (National Payments Corporation of India).

HOW TO SEND MONEY VIA UPI:
1. Open your UPI-enabled app (BHIM, Google Pay, PhonePe, Paytm, etc.)
2. Select 'Send Money' or 'Pay'
3. Enter the recipient's UPI ID (e.g., name@upi, name@okicici, mobile@paytm)
   OR scan their QR code
   OR enter their mobile number linked to UPI
4. Enter the amount
5. Add a remark (optional)
6. Click 'Pay' and enter your 4–6 digit UPI PIN to confirm
7. You will receive a transaction confirmation message

DAILY LIMITS:
- Most banks allow up to ₹1,00,000 per transaction
- Maximum 20 transactions per day (NPCI guideline)
- Some banks offer higher limits for verified merchants

UPI IDs — FORMATS:
- mobilenumber@upi (BHIM)
- name@okicici (ICICI via Google Pay)
- name@ybl (PhonePe)
- name@paytm (Paytm)

IMPORTANT SAFETY TIPS:
- Never share your UPI PIN with anyone, including bank officials
- A UPI PIN is only needed to SEND money, never to RECEIVE
- If someone asks for your PIN to 'transfer' money to you, it is a SCAM
- Always verify the recipient's name shown on the confirmation screen
        """,
        "source": "NPCI / RBI Guidelines",
        "tags": ["upi", "payment", "digital", "bhim", "send money"]
    },
    {
        "id": "upi_002",
        "category": "upi",
        "title": "UPI Security and Common Scams",
        "content": """
COMMON UPI SCAMS TO AVOID:

1. COLLECT REQUEST SCAM:
   - Scammers send a 'Collect Request' saying "Accept to receive money"
   - Accepting and entering your PIN actually SENDS money FROM you
   - Rule: Never enter your UPI PIN to receive money

2. SCREEN SHARING SCAM:
   - Scammer asks you to install AnyDesk/TeamViewer for 'help'
   - They watch your screen to steal your UPI PIN and OTP
   - Rule: Never share your screen with unknown persons

3. FAKE CUSTOMER CARE:
   - Fake numbers appear on Google search results
   - They ask for your UPI ID, bank details, OTP
   - Rule: Always call the number on the back of your bank card or the official bank website

4. QR CODE SCAM:
   - Scammer sends a QR code saying "scan to receive your refund"
   - Scanning and paying through a QR code SENDS money, never receives it
   - Rule: QR codes are for paying, not for receiving

5. LOTTERY / KYC SCAM:
   - "Your account will be blocked unless you update KYC via this link"
   - Banks never ask for PIN or OTP through SMS links
   - Rule: Visit your bank branch or official app for KYC

WHAT TO DO IF SCAMMED:
- Immediately call your bank's 24×7 helpline
- File complaint on cybercrime.gov.in or call 1930
- Report to NPCI via helpdesk.npci.org.in
        """,
        "source": "RBI, Cybercrime.gov.in",
        "tags": ["upi", "scam", "fraud", "security", "safety"]
    },

    # ── Interest Rates ───────────────────────────────────────────────────────
    {
        "id": "interest_001",
        "category": "interest_rates",
        "title": "Understanding Interest Rates on Loans",
        "content": """
WHAT IS AN INTEREST RATE?
Interest rate is the cost of borrowing money, expressed as a percentage per annum (p.a.).
If you borrow ₹1,00,000 at 10% p.a., you pay ₹10,000 interest per year.

TYPES OF INTEREST:
1. Simple Interest (SI): Interest calculated only on the principal
   Formula: SI = (P × R × T) / 100
   Example: ₹1,00,000 at 10% for 2 years = ₹20,000 interest

2. Compound Interest (CI): Interest calculated on principal + accumulated interest
   Formula: CI = P × (1 + R/n)^(n×T) – P
   Banks typically use monthly or quarterly compounding

SAFE INTEREST RATES (as of RBI guidelines):
- Home Loans: 8.5% – 10.5% p.a. (Floating / Fixed)
- Personal Loans: 10% – 24% p.a.
- Car Loans: 8% – 15% p.a.
- Gold Loans: 7% – 18% p.a.
- Education Loans: 9% – 15% p.a.
- Microfinance (SHG/JLG): Up to 26% p.a. (RBI cap)
- Credit Card Outstanding: 24% – 48% p.a.

WARNING SIGNS OF PREDATORY LENDING:
- Interest rates above 36% p.a. from unregistered lenders
- "Instant loan apps" not registered with RBI
- Upfront fee or processing fee demanded before disbursement
- No written loan agreement provided

ALWAYS CHECK:
- Is the lender registered with RBI? (rbi.org.in → NBFC list)
- What is the APR (Annual Percentage Rate) including all fees?
- Are there prepayment penalties?
        """,
        "source": "RBI, NHB Guidelines",
        "tags": ["interest rate", "loan", "EMI", "personal loan", "home loan"]
    },
    {
        "id": "interest_002",
        "category": "interest_rates",
        "title": "EMI Calculation and Loan Planning",
        "content": """
EMI (Equated Monthly Installment) = Fixed monthly payment to repay a loan.

EMI FORMULA:
EMI = [P × R × (1+R)^N] / [(1+R)^N – 1]
Where:
  P = Principal loan amount
  R = Monthly interest rate (Annual rate / 12 / 100)
  N = Number of monthly installments

EXAMPLE:
Loan: ₹5,00,000 | Rate: 12% p.a. | Tenure: 5 years (60 months)
Monthly Rate R = 12/12/100 = 0.01
EMI = [5,00,000 × 0.01 × (1.01)^60] / [(1.01)^60 – 1]
EMI ≈ ₹11,122 per month
Total Payment = ₹6,67,320 | Total Interest = ₹1,67,320

TIPS FOR SMART BORROWING:
1. Keep EMI below 40% of your monthly take-home salary
2. Compare rates from at least 3 lenders before deciding
3. A shorter tenure means higher EMI but less total interest paid
4. Improve your CIBIL score (750+) to get lower interest rates
5. Prepay whenever possible to reduce interest burden

CIBIL SCORE RANGES:
- 750–900: Excellent — best rates available
- 700–749: Good — competitive rates
- 650–699: Fair — may face higher rates
- Below 650: Poor — loans may be rejected or very expensive
        """,
        "source": "RBI, Banking Codes and Standards Board of India",
        "tags": ["EMI", "loan", "CIBIL", "credit score", "interest"]
    },

    # ── Budgeting & Personal Finance ─────────────────────────────────────────
    {
        "id": "budget_001",
        "category": "budgeting",
        "title": "Personal Budgeting Basics — The 50/30/20 Rule",
        "content": """
WHAT IS A BUDGET?
A budget is a plan for how you will spend and save your income each month.
It helps you avoid debt, build savings, and reach financial goals.

THE 50/30/20 RULE (Simple Budgeting Framework):
Divide your take-home (after-tax) income into three buckets:

50% — NEEDS (Essential Expenses)
  • Rent / Home loan EMI
  • Groceries and food
  • Utility bills (electricity, water, gas)
  • Transportation (bus, petrol, auto)
  • Insurance premiums
  • Minimum loan repayments

30% — WANTS (Discretionary Spending)
  • Dining out and entertainment
  • Shopping (clothes, gadgets)
  • OTT subscriptions
  • Hobbies and travel

20% — SAVINGS & INVESTMENTS
  • Emergency fund (target: 6 months of expenses)
  • PPF, NPS, Mutual Funds, FD
  • Extra loan repayment
  • Goal-based savings (education, marriage, home)

EXAMPLE (Monthly Salary ₹30,000):
  Needs: ₹15,000
  Wants: ₹9,000
  Savings: ₹6,000

HOW TO START BUDGETING:
1. Track all expenses for 1 month (use an app or notebook)
2. Categorise each expense as Need / Want
3. Calculate your total income
4. Apply the 50/30/20 split and adjust as needed
5. Review your budget every month
        """,
        "source": "National Financial Literacy Mission, RBI",
        "tags": ["budget", "savings", "50/30/20", "personal finance", "planning"]
    },
    {
        "id": "budget_002",
        "category": "budgeting",
        "title": "Emergency Fund and Savings Goals",
        "content": """
EMERGENCY FUND — Your Financial Safety Net

WHAT IS IT?
An emergency fund is money saved specifically for unexpected expenses:
- Job loss or pay cut
- Medical emergencies
- Urgent home/vehicle repairs
- Family emergencies

HOW MUCH TO SAVE?
Minimum: 3 months of total monthly expenses
Ideal: 6 months of total monthly expenses
Example: If monthly expenses = ₹20,000 → Emergency fund target = ₹1,20,000

WHERE TO KEEP IT?
- Savings Bank account (easy access)
- Liquid Mutual Fund (slightly better returns, redeemable in 1 day)
- Short-term FD (if you can lock for 3–6 months)
DO NOT invest emergency funds in stocks, crypto, or long-term FDs

HOW TO BUILD IT FAST?
1. Start with ₹500–₹1,000 per month
2. Save any windfalls (bonus, tax refund, gifts)
3. Cut one "want" category temporarily
4. Set up an automatic transfer on salary day

SAVINGS GOALS — SMART FRAMEWORK:
S = Specific (e.g., "Buy a scooter worth ₹80,000")
M = Measurable (₹80,000 in 24 months = ₹3,333/month)
A = Achievable (fits within your 20% savings bucket)
R = Relevant (you actually need it)
T = Time-bound (by December 2026)

GOVERNMENT SAVINGS SCHEMES:
1. PPF (Public Provident Fund): 7.1% p.a., 15-year lock-in, tax-free
2. NSC (National Savings Certificate): 7.7% p.a., 5-year term
3. Sukanya Samriddhi Yojana: 8.2% p.a. (for girl children under 10)
4. Senior Citizens Savings Scheme: 8.2% p.a. (age 60+)
5. PM Jan Dhan Yojana: Zero-balance account with RuPay card
        """,
        "source": "Ministry of Finance, Post Office Savings Schemes",
        "tags": ["emergency fund", "savings", "PPF", "goal", "investment"]
    },

    # ── Online Safety & Fraud ────────────────────────────────────────────────
    {
        "id": "fraud_001",
        "category": "online_safety",
        "title": "Protecting Yourself from Online Financial Fraud",
        "content": """
TOP ONLINE FINANCIAL FRAUDS IN INDIA:

1. PHISHING:
   - Fake emails/SMS pretending to be your bank
   - Links lead to fake websites that steal your login
   - PROTECT: Always type bank URL manually; check for HTTPS and correct domain

2. VISHING (Voice Phishing):
   - Caller claims to be from bank/TRAI/police
   - Creates urgency: "Your SIM will be blocked", "You have a pending arrest"
   - Asks for OTP, CVV, or UPI PIN
   - PROTECT: Hang up and call back on official number

3. SIM SWAP FRAUD:
   - Fraudster convinces telecom to issue duplicate SIM
   - Receives all your OTPs and drains bank account
   - PROTECT: If your SIM stops working suddenly, call telecom immediately

4. FAKE LOAN / INVESTMENT APPS:
   - Offer "instant loans" or "guaranteed 30% returns"
   - Collect your documents and money, then disappear
   - PROTECT: Only use RBI-registered lenders; check SEBI for investment advisors

5. OLX / MARKETPLACE SCAMS:
   - Buyer sends extra money by "mistake" and asks for refund via UPI
   - The original payment is fake; the refund is real
   - PROTECT: Verify payment in your bank account, not just screenshots

RED FLAGS:
❌ Anyone asking for your OTP, CVV, or UPI PIN
❌ "Congratulations, you won!" messages
❌ Requests to install remote access apps
❌ Upfront fees to claim a prize or loan
❌ Pressure to "act now or lose the offer"

REPORT FRAUD:
📞 Cyber Crime Helpline: 1930
🌐 cybercrime.gov.in
📞 RBI Ombudsman: 14448
        """,
        "source": "cybercrime.gov.in, RBI Consumer Education",
        "tags": ["fraud", "phishing", "scam", "OTP", "online safety", "vishing"]
    },
    {
        "id": "fraud_002",
        "category": "online_safety",
        "title": "Safe Online Banking Practices",
        "content": """
SAFE ONLINE BANKING — ESSENTIAL PRACTICES:

PASSWORD & LOGIN SECURITY:
✅ Use a strong password: 12+ characters, mix of letters, numbers, symbols
✅ Never use birthdate, name, or "password123"
✅ Use different passwords for banking vs social media
✅ Enable 2-Factor Authentication (2FA) on all financial apps
✅ Change your banking password every 3–6 months
✅ Never save banking passwords in browser on shared computers

DEVICE SECURITY:
✅ Keep your phone OS and apps updated
✅ Only install banking apps from official App Store / Play Store
✅ Enable screen lock (fingerprint/PIN) on your device
✅ Do not use public Wi-Fi for banking transactions
✅ Install a reputable antivirus app
✅ If your phone is lost, immediately block your SIM and freeze accounts

TRANSACTION SAFETY:
✅ Register for SMS alerts for all transactions
✅ Check your bank statement monthly
✅ Set daily transaction limits on your account
✅ Use virtual cards for online shopping
✅ Verify merchant website SSL certificate (https://)

WHAT BANKS WILL NEVER DO:
❌ Ask for your full card number over phone/email
❌ Ask for OTP, CVV, PIN via SMS/email
❌ Send you a link to "verify" your account
❌ Ask you to transfer money to a "safe account"
        """,
        "source": "RBI, Banking Codes and Standards Board of India",
        "tags": ["online banking", "password", "security", "safe", "2FA"]
    },

    # ── Government Schemes ───────────────────────────────────────────────────
    {
        "id": "scheme_001",
        "category": "government_schemes",
        "title": "Key Government Financial Schemes for Citizens",
        "content": """
IMPORTANT GOVERNMENT FINANCIAL SCHEMES:

1. PM JAN DHAN YOJANA (PMJDY):
   - Zero-balance savings account for unbanked citizens
   - Free RuPay Debit Card with ₹2 lakh accident insurance
   - ₹10,000 overdraft facility after 6 months of good conduct
   - Enroll at any bank branch with Aadhaar + Passport photo

2. PRADHAN MANTRI MUDRA YOJANA (PMMY):
   - Loans for small businesses / self-employed
   - Shishu: Up to ₹50,000 | Kishore: ₹50,001–₹5 lakh | Tarun: ₹5–₹10 lakh
   - No collateral required for Shishu and Kishore
   - Apply at any bank, MFI, or mudra.org.in

3. ATAL PENSION YOJANA (APY):
   - Guaranteed pension of ₹1,000–₹5,000/month after age 60
   - Open to workers in unorganised sector (age 18–40)
   - Government co-contributes 50% for first 5 years (for non-income-tax payers)
   - Enroll via your savings bank account

4. PM SURAKSHA BIMA YOJANA (PMSBY):
   - Accidental death / disability insurance
   - Premium: ₹20/year | Coverage: ₹2 lakh
   - Available for bank account holders aged 18–70

5. PM JEEVAN JYOTI BIMA YOJANA (PMJJBY):
   - Life insurance scheme
   - Premium: ₹436/year | Coverage: ₹2 lakh on death
   - Available for bank account holders aged 18–50

6. STAND UP INDIA:
   - Loans of ₹10 lakh–₹1 crore for SC/ST and women entrepreneurs
   - Apply at standupmitra.in

HOW TO CHECK ELIGIBILITY:
Visit myscheme.gov.in — Government's official scheme finder portal
        """,
        "source": "Ministry of Finance, Jan Dhan Yojana Official Portal",
        "tags": ["government scheme", "PMJDY", "MUDRA", "APY", "insurance", "pension"]
    },

    # ── Financial Planning ───────────────────────────────────────────────────
    {
        "id": "planning_001",
        "category": "financial_planning",
        "title": "Basic Investment Options for Beginners",
        "content": """
INVESTMENT OPTIONS FOR BEGINNERS IN INDIA:

LOW RISK (Capital Protection):
1. Fixed Deposits (FD): 6–8% p.a., insured up to ₹5 lakh per bank by DICGC
2. Recurring Deposits (RD): Invest monthly, similar returns to FD
3. PPF: 7.1% tax-free, 15-year lock-in, government-backed
4. Post Office Schemes: NSC, MIS, POTD — government-guaranteed

MEDIUM RISK (Moderate Returns):
5. Debt Mutual Funds: Invest in bonds/govt securities, 6–9% average returns
6. Balanced/Hybrid Mutual Funds: Mix of equity + debt, 8–12% average
7. NPS (National Pension System): Tax benefit + market-linked returns

HIGH RISK (Higher Potential Returns):
8. Equity Mutual Funds (SIP): Invest in stocks via SIP from ₹500/month
   - Long-term (10+ years) historical average: 12–15% p.a.
9. Direct Stocks: Buy shares on NSE/BSE via SEBI-registered broker
   - Requires knowledge and higher risk tolerance
10. Gold (Digital / SGB): Hedge against inflation, 2–3% annual interest on SGBs

GOLDEN RULES OF INVESTING:
✅ Start early — even ₹500/month grows significantly over 20 years
✅ Diversify — never put all money in one place
✅ Invest regularly (SIP) rather than trying to time the market
✅ Match investment to your goal timeline (short/medium/long term)
✅ Never invest in unregistered schemes promising unrealistic returns
✅ Check SEBI registration at sebi.gov.in before investing

TAX-SAVING INVESTMENTS (Section 80C, limit ₹1.5 lakh/year):
PPF, ELSS Mutual Funds, NSC, 5-year FD, NPS (additional ₹50,000)
        """,
        "source": "SEBI Investor Education, AMFI",
        "tags": ["investment", "mutual fund", "SIP", "FD", "PPF", "stock market"]
    },
    {
        "id": "planning_002",
        "category": "financial_planning",
        "title": "Insurance Basics — Why You Need It",
        "content": """
TYPES OF INSURANCE EVERY INDIAN SHOULD HAVE:

1. HEALTH INSURANCE:
   - Covers hospitalisation, surgery, and medical bills
   - Recommended: ₹5–10 lakh individual cover; ₹10–20 lakh family floater
   - Government option: Ayushman Bharat — ₹5 lakh/year for eligible families (free)
   - Private options: Star Health, HDFC ERGO, Niva Bupa, etc.
   - Buy early — premiums are lower when young and healthy

2. TERM LIFE INSURANCE:
   - Pays lump sum to family if you die during the term
   - Recommended: 10–15× your annual income
   - Pure term plans (no investment) are cheapest: ₹500–₹1,000/month for ₹1 crore cover (age 30)
   - Buy only from IRDAI-registered insurers

3. VEHICLE INSURANCE:
   - Third-party liability insurance is MANDATORY by law
   - Comprehensive insurance also covers your own vehicle damage

4. COMMON MISTAKES:
   ❌ Buying insurance for investment returns (endowment/ULIP often underperform)
   ❌ Under-insuring to save premium
   ❌ Not reading policy exclusions
   ❌ Letting policy lapse due to non-payment

5. HOW TO BUY:
   - Compare on Policybazaar, Coverfox, or directly from insurer website
   - Always read the Policy Wording document
   - Disclose pre-existing conditions honestly

CLAIM PROCESS:
- Health: Cashless at network hospital OR reimbursement within 30 days
- Life: Submit death certificate + policy + KYC to insurer
- Complaints: irdai.gov.in or call 155255
        """,
        "source": "IRDAI, Ayushman Bharat Portal",
        "tags": ["insurance", "health insurance", "life insurance", "term plan", "IRDAI"]
    },
    # ── UPI Introduction (plain definitional doc) ────────────────────────────
    {
        "id": "upi_000",
        "category": "upi",
        "title": "What is UPI?",
        "content": """
WHAT IS UPI?
UPI (Unified Payments Interface) is India's real-time digital payment system, built and
operated by NPCI (National Payments Corporation of India) and regulated by the Reserve Bank
of India (RBI). Launched in 2016, UPI lets you instantly transfer money between any two bank
accounts using just a smartphone — 24 hours a day, 7 days a week, including holidays.

KEY FEATURES:
- Instant bank-to-bank transfers in under 10 seconds
- No need to share bank account number or IFSC code
- Works through a simple UPI ID (e.g., yourname@upi, mobile@paytm)
- Free for users — no transaction charges for sending money
- Supported by 300+ banks and payment apps in India
- Maximum transaction limit: ₹1,00,000 per transaction (RBI guideline)

HOW IT WORKS:
Each user has a UPI ID (Virtual Payment Address) linked to their bank account.
To pay, you enter the recipient's UPI ID and your UPI PIN — the money moves directly
between bank accounts without sharing any sensitive details.

POPULAR UPI APPS:
- BHIM (government app by NPCI)
- Google Pay (Tez)
- PhonePe
- Paytm
- Amazon Pay
- YONO SBI, iMobile (bank apps)

WHY UPI IS SAFE:
- Transactions require your secret UPI PIN — never stored on your phone
- Two-factor authentication (bank + PIN) on every payment
- RBI-regulated — all disputes can be raised with your bank

REMEMBER: Your UPI PIN is only for SENDING money.
No legitimate app or person ever needs your PIN to SEND money TO you.
        """,
        "source": "NPCI, RBI",
        "tags": ["upi", "what is upi", "digital payment", "NPCI", "introduction", "basics"]
    },
]

# Category metadata for UI display
CATEGORIES = {
    "upi": {"label": "UPI & Digital Payments", "icon": "💳", "color": "#3b82f6"},
    "interest_rates": {"label": "Interest Rates & Loans", "icon": "📊", "color": "#10b981"},
    "budgeting": {"label": "Budgeting & Savings", "icon": "💰", "color": "#f59e0b"},
    "online_safety": {"label": "Online Safety & Fraud", "icon": "🛡️", "color": "#ef4444"},
    "government_schemes": {"label": "Government Schemes", "icon": "🏛️", "color": "#8b5cf6"},
    "financial_planning": {"label": "Investments & Insurance", "icon": "📈", "color": "#06b6d4"},
}

# Quick answer lookup for very common questions
QUICK_ANSWERS = {
    "upi pin": "Your UPI PIN is a 4–6 digit secret number used only to SEND money. NEVER share it with anyone. No one needs your UPI PIN to send money TO you.",
    "1930": "1930 is India's Cyber Crime Helpline. Call immediately if you have been financially defrauded online.",
    "cibil": "CIBIL score ranges from 300–900. A score above 750 is considered excellent and helps you get loans at lower interest rates.",
}
