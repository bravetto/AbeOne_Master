#!/bin/bash
# North Shore Data Collection Script
# EEAAO Execution - Immediate Action

set -e

echo "🔥 NORTH SHORE DATA COLLECTION - EEAAO EXECUTION"
echo "================================================"
echo ""

# Configuration
DATA_EMAIL="jimmy@bravetto.com"
NORTH_SHORE_CONTACTS=(
    "trish@northshore.com"
    "ryan@northshore.com"
    "larry@northshore.com"
)

# Step 1: Send Data Collection Request
echo "📧 Step 1: Sending Data Collection Request..."
cat > /tmp/data_collection_email.txt << EOF
Subject: Spiceworks CSV Export - Partnership Data Collection

Hey Larry,

Following up on our meeting - we're ready to start the data analysis!

Can you export the Spiceworks tickets as CSV and send to ${DATA_EMAIL}?

We'll have actionable insights back to you within 20 minutes of receipt.

Thanks!
Michael & Bryan
EOF

echo "✅ Email draft created: /tmp/data_collection_email.txt"
echo ""

# Step 2: Create Customer Survey Questions
echo "📋 Step 2: Creating Customer Survey Questions..."
cat > /tmp/customer_survey_questions.txt << EOF
NORTH SHORE CUSTOMER SURVEY - DECEMBER MEETINGS

1. What's your biggest operational challenge right now?
2. How much time do you spend on front desk management?
3. What compliance tasks take the most time?
4. What would make your life easier?
5. What technology would you pay for?
6. What's your biggest pain point with employees?
7. What support issues come up most often?
8. What would 10x your efficiency?
9. What keeps you up at night?
10. What would you automate if you could?

Please send responses to: ${DATA_EMAIL}
EOF

echo "✅ Survey questions created: /tmp/customer_survey_questions.txt"
echo ""

# Step 3: Create Follow-Up Meeting Template
echo "📅 Step 3: Creating Follow-Up Meeting Template..."
cat > /tmp/followup_meeting_agenda.txt << EOF
NORTH SHORE × AV1 FOLLOW-UP MEETING AGENDA

Date: Week 2 (TBD)
Duration: 60 minutes

AGENDA:
1. Review Spiceworks data analysis (20 min)
   - Pattern detection results
   - Revenue opportunities identified
   - Solution recommendations

2. Present 10 revenue opportunities (15 min)
   - Prioritized list
   - Revenue potential
   - Implementation timeline

3. Demo Wellness Agent.ai (10 min)
   - Front desk automation
   - Pilot client results
   - Service package

4. Discuss next steps (15 min)
   - Pilot deployment
   - Revenue model
   - Partnership expansion
EOF

echo "✅ Meeting agenda created: /tmp/followup_meeting_agenda.txt"
echo ""

# Step 4: Create Data Analysis Preparation Script
echo "🤖 Step 4: Preparing Av1 Data Analysis..."
cat > /tmp/av1_analysis_prep.sh << EOF
#!/bin/bash
# Av1 Data Analysis Preparation

echo "Preparing Av1 for Spiceworks CSV analysis..."

# Wait for CSV file
echo "Waiting for Spiceworks CSV export..."
while [ ! -f "spiceworks_export.csv" ]; do
    sleep 60
done

echo "CSV file received! Starting analysis..."

# Run Av1 analysis
python3 -c "
import av1
from av1.intelligence import analyze_support_tickets

# Load CSV
data = av1.load_csv('spiceworks_export.csv')

# Run analysis
results = analyze_support_tickets(data)

# Generate insights
insights = results.generate_insights()
opportunities = results.identify_revenue_opportunities()

# Output results
print('✅ Analysis complete!')
print(f'📊 Insights: {len(insights)}')
print(f'💰 Revenue Opportunities: {len(opportunities)}')
"

echo "✅ Analysis complete!"
EOF

chmod +x /tmp/av1_analysis_prep.sh
echo "✅ Analysis script created: /tmp/av1_analysis_prep.sh"
echo ""

# Summary
echo "================================================"
echo "✅ DATA COLLECTION SETUP COMPLETE"
echo ""
echo "Next Steps:"
echo "1. Send data collection email to Larry"
echo "2. Send survey questions to Trish"
echo "3. Schedule follow-up meeting"
echo "4. Prepare Av1 for data analysis"
echo ""
echo "LFG! LFG! LFG! LFG!"
echo ""

