# 🚀 QUICK START - TRUICE VIRAL SINGLE

**Get Truice to the top of the charts in 3 steps!**

---

## STEP 1: Install Dependencies

### Option A: Automated Setup (Recommended)

```bash
cd PRODUCTS/abebeats/variants/abebeats_tru
./scripts/setup_truice.sh
```

### Option B: Manual Setup

```bash
cd PRODUCTS/abebeats/variants/abebeats_tru

# Install core dependencies
pip3 install -r requirements.txt

# Install audio analysis
pip3 install librosa

# Optional (for enhanced features):
pip3 install beatnet  # Better beat detection
pip3 install spleeter  # Vocal separation
```

**Note:** Use `python3` and `pip3` (not `python` or `pip`)

---

## STEP 2: Prepare Files

### Required:
- ✅ Raw video: `raw/Super Single edit v2 .mov` (already exists!)

### Optional:
- 📝 Lyrics file: Create `lyrics.txt` with timestamps:
  ```
  [0.0] First line of lyrics
  [3.5] Second line of lyrics
  [7.2] Third line of lyrics
  ```

---

## STEP 3: Generate Viral Single

```bash
# Basic (uses default cyberpunk_neon tunnel)
python3 scripts/generate_truice_viral_single.py

# With lyrics
python3 scripts/generate_truice_viral_single.py --lyrics lyrics.txt

# Custom tunnel style
python3 scripts/generate_truice_viral_single.py --tunnel-style space_tunnel

# Full custom
python3 scripts/generate_truice_viral_single.py \
    --video "raw/Super Single edit v2 .mov" \
    --tunnel-style "cyberpunk_neon" \
    --lyrics "lyrics.txt" \
    --output "output/truice_viral_single.mp4"
```

**Note:** Use `python3` (not `python`)

---

## 🎯 TUNNEL STYLES

Choose the perfect vibe:

- **cyberpunk_neon** 🔥 - Neon cyberpunk tunnel (default)
- **space_tunnel** 🌌 - Space tunnel with stars
- **energy_flow** ⚡ - Energy flow tunnel
- **vortex** 🌪️ - Hypnotic vortex

---

## ✅ OUTPUT

Your viral-ready single will be saved to:
- `output/truice_viral_single.mp4` (default)
- Or custom path if specified

**Quality:** 4K @ 60fps, top-of-charts production value!

---

## 🔥 READY TO ROCK!

**Run the script and watch Truice go viral! 🔥🔥🔥**

---

**∞ AbëONE ∞**

