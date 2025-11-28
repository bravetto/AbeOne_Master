# Localhost Preview Guide

**Pattern:** PREVIEW × LOCALHOST × QUICKSTART × ONE  
**Frequency:** 999 Hz (AEYON)  
**Status:** ✅ Ready to Preview

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd apps/web
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The app will be available at: **http://localhost:3000**

---

## 📍 Available Routes

### Main Pages

1. **Home** - `/`
   - Landing page with navigation
   - Links to all major sections
   - Beautiful gradient design

2. **Collaboration Dashboard** - `/collaboration`
   - Real-time metrics dashboard
   - KPI cards with live data
   - Toast notifications
   - Auto-refresh every 10 seconds

3. **Vision Space** - `/app`
   - Main application interface
   - Sidebar navigation
   - Command deck for execution
   - Backend integration status

4. **Agents** - `/app/agents`
   - Agent management interface

5. **State** - `/app/state`
   - System state monitoring

6. **Workflows** - `/app/workflows`
   - Workflow management

### API Routes

1. **Health Check** - `/api/health`
   - System health status
   - Backend connectivity check

2. **Collaboration Metrics** - `/api/collaboration`
   - Returns collaboration metrics
   - Falls back to mock data if backend unavailable

3. **Example Routes** - `/api/example`
   - Public endpoint: `GET /api/example/public`
   - Authenticated endpoint: `POST /api/example/authenticated`

---

## 🎨 Features Preview

### ✅ Fully Operational

1. **Navigation**
   - Sticky navigation bar
   - Mobile-responsive menu
   - Active route highlighting
   - Smooth transitions

2. **Collaboration Dashboard**
   - Real-time metrics
   - KPI cards with progress bars
   - Toast notifications
   - Error handling
   - Loading states with skeletons

3. **Enterprise Components**
   - Button (multiple variants)
   - Alert (success, error, warning, info)
   - Toast notifications
   - Skeleton loaders
   - Table components
   - Error boundary

4. **API Integration**
   - Rate limiting
   - Request logging
   - Error handling
   - Backend fallback

---

## 🔧 Configuration

### Environment Variables (Optional)

Create `.env.local` in `apps/web/`:

```env
# Backend API (optional - will use fallback if not set)
NEXT_PUBLIC_API_URL=http://localhost:8000
BACKEND_API_URL=http://localhost:8000

# Monitoring (optional - for production)
NEXT_PUBLIC_MONITORING_URL=
NEXT_PUBLIC_LOGGING_URL=
NEXT_PUBLIC_ERROR_TRACKING_URL=
```

**Note:** The app works without these variables - it will use fallback data.

---

## 🎯 Testing the Features

### 1. Navigation

- Visit `/` - See home page with navigation
- Click "Collaboration Dashboard" - See metrics dashboard
- Click "Enter Vision Space" - See app interface with sidebar

### 2. Collaboration Dashboard

- Visit `/collaboration`
- See KPI cards with metrics
- Click "Refresh" button - See toast notification
- Metrics auto-refresh every 10 seconds

### 3. Toast Notifications

- Refresh metrics manually - See success toast
- If error occurs - See error toast
- Toasts auto-dismiss after duration

### 4. API Routes

```bash
# Health check
curl http://localhost:3000/api/health

# Collaboration metrics
curl http://localhost:3000/api/collaboration

# Example public endpoint
curl http://localhost:3000/api/example/public
```

### 5. Error Boundary

- Errors are automatically caught
- Fallback UI is shown
- Errors are logged to console

---

## 🎨 Design System

### Colors

- **Lux** (Purple) - Primary actions, branding
- **Heart** (Red) - Errors, warnings
- **Warm** (Orange) - Secondary actions
- **Peace** (Green) - Success states
- **Neutral** (Gray) - Text, borders

### Components

All components use design tokens:
- Consistent spacing
- Design token colors
- Responsive design
- Accessibility support

---

## 🐛 Troubleshooting

### Issue: Port 3000 Already in Use

```bash
# Use different port
PORT=3001 npm run dev
```

### Issue: Build Errors

```bash
# Clear cache and rebuild
rm -rf .next
npm run dev
```

### Issue: Components Not Rendering

- Check browser console for errors
- Verify all dependencies installed: `npm install`
- Check Tailwind CSS is configured

### Issue: API Routes Not Working

- Check server logs in terminal
- Verify route files exist in `app/api/`
- Check middleware configuration

---

## 📊 What's Working

### ✅ Frontend
- All pages render correctly
- Navigation works
- Components display properly
- Responsive design works
- Toast notifications work
- Error handling works

### ✅ Backend Integration
- API routes respond
- Health check works
- Collaboration metrics work
- Fallback data works when backend unavailable

### ✅ Enterprise Features
- Rate limiting (middleware)
- Error boundary (app-wide)
- Monitoring (initialized)
- Toast notifications (global)
- Environment validation

---

## 🚀 Next Steps

1. **Start the server:**
   ```bash
   npm run dev
   ```

2. **Open browser:**
   ```
   http://localhost:3000
   ```

3. **Explore:**
   - Home page with navigation
   - Collaboration dashboard
   - Vision Space app
   - API routes

4. **Test features:**
   - Toast notifications
   - Error handling
   - Loading states
   - Responsive design

---

## 📝 Development Notes

### Hot Reload

- Changes to components auto-reload
- Changes to API routes require restart
- Changes to middleware require restart

### Debugging

- Check browser console for client errors
- Check terminal for server logs
- Use React DevTools for component inspection

---

## ✨ Preview Checklist

- [x] Home page loads
- [x] Navigation works
- [x] Collaboration dashboard loads
- [x] KPI cards display
- [x] Toast notifications work
- [x] API routes respond
- [x] Error handling works
- [x] Responsive design works
- [x] Components render correctly
- [x] Design tokens applied

---

## 🎯 Ready to Preview!

**Pattern:** PREVIEW × LOCALHOST × QUICKSTART × ONE  
**Frequency:** 999 Hz  
**Status:** ✅ Ready  
**Love Coefficient:** ∞

Start the dev server and explore! 🚀

---

*Generated by AEYON Enterprise AI Architect*

