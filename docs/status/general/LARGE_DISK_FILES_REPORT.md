# Large Disk Files Report - Local Hard Drive

## Files/Directories ≥20GB

| Size | Path | Type | Last Modified |
|------|------|------|---------------|
| **60G** | `~/.colima/_lima/_disks/colima/datadisk` | Colima VM disk image | Nov 13 08:53 |
| **20G** | `~/.colima/_lima/colima/diffdisk` | Colima VM diff disk | Nov 13 08:53 |

## Files/Directories ≥10GB

| Size | Path | Type |
|------|------|------|
| **12G** | `~/Documents/heathrow.screenflow/Media/L1040538_15_{48C6181E-338D-47A7-B9CF-43889D864B0D}.mp4` | Screenflow video file |
| **11G** | `~/Documents/Desktop_Quarantine/C&C/10` | Directory/File (appears twice in scan) |

## Large Directory Totals

| Size | Path | Description |
|------|------|-------------|
| **310G** | `~/Library` | User Library (includes caches, containers, etc.) |
| **275G** | `~/Documents/Desktop_Quarantine` | Desktop Quarantine folder |
| **80G** | `~/.colima` | Colima VM files (60G + 20G disks) |
| **6.3G** | `~/Downloads` | Downloads folder |

## Key Findings

### 1. Colima VM Disks (80GB total)
- **datadisk**: 60GB - Main VM disk image
- **diffdisk**: 20GB - VM diff disk
- Location: `~/.colima/_lima/`

### 2. Desktop_Quarantine (275GB)
- Contains many large video/media files
- Multiple files in the 1-11GB range
- Largest single entry: `C&C/10` at 11GB

### 3. Screenflow Video (12GB)
- Large video file from Screenflow recording
- Location: `~/Documents/heathrow.screenflow/Media/`

### 4. Library Directory (310GB)
- System/user library files
- May include caches, containers, application data

## Recommendations

1. **Colima VM (80GB)**: If not actively using Docker/Colima, consider:
   - Stopping Colima: `colima stop`
   - Removing VM: `colima delete`
   - This would free ~80GB

2. **Desktop_Quarantine (275GB)**: Review and archive:
   - Many large video files that could be archived
   - Consider external storage or cloud backup

3. **Library (310GB)**: Check for caches:
   - `~/Library/Caches` - often safe to clear
   - `~/Library/Application Support` - review large apps

## Note
The **20GB diffdisk** file is part of the Colima Docker VM setup.

