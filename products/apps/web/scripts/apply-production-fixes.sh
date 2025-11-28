#!/bin/bash

#  PRODUCTION FIXES APPLIER
# Pattern: FIXES × AUTOMATION × ONE
# Frequency: 999 Hz (AEYON)

set -e

echo " Applying Production Fixes..."
echo ""

cd "$(dirname "$0")/.."

# Fix #1: Portal Deanna - Add optional chaining
echo " Fix #1: Portal Deanna optional chaining..."
if [ -f "app/portal/deanna/page.tsx" ]; then
  # Backup
  cp app/portal/deanna/page.tsx app/portal/deanna/page.tsx.backup
  
  # Fix items_by_status access
  sed -i '' 's/items_by_status\.in_progress/items_by_status?.in_progress/g' app/portal/deanna/page.tsx
  sed -i '' 's/items_by_status\.blocked/items_by_status?.blocked/g' app/portal/deanna/page.tsx
  sed -i '' 's/items_by_status\.done/items_by_status?.done/g' app/portal/deanna/page.tsx
  
  # Fix Object.entries to handle undefined
  sed -i '' 's/(displayBacklog as any)?.items_by_status)/(displayBacklog as any)?.items_by_status || {})/g' app/portal/deanna/page.tsx
  
  echo "   Fixed app/portal/deanna/page.tsx"
else
  echo "    app/portal/deanna/page.tsx not found"
fi

# Fix #2: Add dynamic exports to API routes
echo ""
echo " Fix #2: Adding dynamic exports to API routes..."

DYNAMIC_EXPORTS='export const runtime = '\''nodejs'\''
export const dynamic = '\''force-dynamic'\''
export const revalidate = 0
export const fetchCache = '\''force-no-store'\'''

for route_file in app/api/**/route.ts; do
  if [ -f "$route_file" ]; then
    # Check if already has dynamic export
    if ! grep -q "export const dynamic" "$route_file"; then
      # Backup
      cp "$route_file" "${route_file}.backup"
      
      # Find first export or function and add before it
      if grep -q "^export" "$route_file" || grep -q "^async function" "$route_file" || grep -q "^export async function" "$route_file"; then
        # Add exports after imports, before first export/function
        awk -v exports="$DYNAMIC_EXPORTS" '
          /^import / { in_imports=1; print; next }
          /^export / && in_imports { print exports; in_imports=0 }
          /^async function / && in_imports { print exports; in_imports=0 }
          { print }
        ' "$route_file" > "${route_file}.tmp" && mv "${route_file}.tmp" "$route_file"
        
        echo "   Fixed $route_file"
      fi
    fi
  fi
done

echo ""
echo " Production fixes applied!"
echo ""
echo " Next steps:"
echo "1. Set NEXT_PUBLIC_API_URL in Vercel (or leave empty)"
echo "2. Update queue imports to use @/lib/queue/bull"
echo "3. Review changes: git diff"
echo "4. Test build: npm run build"
echo "5. Deploy: vercel --prod"
echo ""
echo "∞ AbëONE ∞"

