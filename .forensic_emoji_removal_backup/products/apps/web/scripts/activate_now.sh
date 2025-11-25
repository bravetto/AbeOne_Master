#!/bin/bash
# 🔥 ACTIVATE WEBINAR INFRASTRUCTURE NOW
# Pattern: ACTIVATION × CONVERGENCE × NOW × ONE

set -e

echo "🔥 ACTIVATING WEBINAR INFRASTRUCTURE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 1: Activate new API route
echo "1️⃣ Activating new registration API route..."
if [ -f "app/api/webinar/register/route.new.ts" ]; then
  if [ -f "app/api/webinar/register/route.ts" ]; then
    mv app/api/webinar/register/route.ts app/api/webinar/register/route.old.ts
    echo "   ✅ Backed up old route"
  fi
  mv app/api/webinar/register/route.new.ts app/api/webinar/register/route.ts
  echo "   ✅ New route activated"
else
  echo "   ⚠️  New route file not found (may already be activated)"
fi
echo ""

# Step 2: Check credentials
echo "2️⃣ Checking AbëKEYs vault credentials..."
if [ -f ~/.abekeys/credentials/database.json ]; then
  echo "   ✅ Database credentials found"
else
  echo "   ⚠️  Database credentials missing"
  echo "   Run: ./scripts/setup_webinar_abekeys.sh"
fi

if [ -f ~/.abekeys/credentials/sendgrid.json ]; then
  echo "   ✅ SendGrid credentials found"
else
  echo "   ⚠️  SendGrid credentials missing"
  echo "   Run: ./scripts/setup_webinar_abekeys.sh"
fi
echo ""

# Step 3: Install dependencies
echo "3️⃣ Checking dependencies..."
if [ ! -d "node_modules" ]; then
  echo "   Installing dependencies..."
  npm install
else
  echo "   ✅ Dependencies installed"
fi
echo ""

# Step 4: Database migrations
echo "4️⃣ Running database migrations..."
if [ -f "prisma/schema.prisma" ]; then
  echo "   Generating Prisma client..."
  npm run db:generate || echo "   ⚠️  Prisma generate failed (may need DATABASE_URL)"
  
  echo "   Running migrations..."
  npm run db:migrate || echo "   ⚠️  Migrations failed (may need DATABASE_URL in AbëKEYs vault)"
else
  echo "   ⚠️  Prisma schema not found"
fi
echo ""

# Step 5: Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ ACTIVATION COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "  1. Ensure credentials in AbëKEYs vault (if not done)"
echo "  2. Start dev server: npm run dev"
echo "  3. Start email worker (separate terminal): npm run webinar:worker"
echo ""
