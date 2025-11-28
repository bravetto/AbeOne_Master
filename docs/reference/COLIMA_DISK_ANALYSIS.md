# Colima Disk Analysis - What's Inside

## Disk Files Overview

| File | Size (ls) | Actual Size (du) | Type | Description |
|------|-----------|------------------|------|-------------|
| `diffdisk` | 20GB | 1.4GB | Sparse disk image | VM diff disk (changes from base) |
| `datadisk` | 60GB | 60GB | Disk image | Main VM data disk |
| `basedisk` | 347MB | 347MB | Base image | Base VM image |

## Key Finding: Sparse File

The **diffdisk** shows as **20GB allocated** but only **1.4GB actual disk usage**. This is a **sparse file** - it's allocated space but mostly empty.

### What This Means:
- The VM was configured with a 20GB diff disk
- Only 1.4GB is actually being used
- The remaining ~18.6GB is allocated but empty (sparse)

## Disk Image Type

The diffdisk is a **DOS/MBR boot sector** with:
- Partition table (GPT)
- Extended partition
- 41,943,039 sectors allocated

## What's Likely Inside

Since Colima is a Docker/Lima VM, the diffdisk likely contains:

1. **Docker Images & Containers**
   - Pulled Docker images
   - Running/stopped containers
   - Container filesystems

2. **Docker Volumes**
   - Named volumes
   - Bind mounts data

3. **System Changes**
   - Installed packages
   - Configuration files
   - Logs and temporary files

4. **Application Data**
   - Any data written by containers
   - Build artifacts
   - Cache files

## Actual Usage Breakdown

- **Allocated**: 20GB (virtual size)
- **Used**: ~1.4GB (actual data)
- **Free**: ~18.6GB (sparse/unused)

## To See Actual Contents

If you want to inspect what's actually stored:

1. **Start Colima** (if needed):
   ```bash
   colima start
   ```

2. **SSH into the VM**:
   ```bash
   colima ssh
   ```

3. **Check disk usage inside VM**:
   ```bash
   df -h
   docker system df
   ```

4. **List Docker images/containers**:
   ```bash
   docker images
   docker ps -a
   docker volume ls
   ```

## Recommendations

### If Not Using Colima:
- **Delete the VM** to free ~61.4GB:
  ```bash
  colima delete
  ```

### If Using Colima:
- **Compact the sparse disk** (if supported):
  - The sparse file will grow as you use Docker
  - Consider cleaning unused Docker resources:
    ```bash
    docker system prune -a --volumes
    ```

### To Reduce Size:
- Clean Docker images: `docker image prune -a`
- Clean volumes: `docker volume prune`
- Clean build cache: `docker builder prune`

## Summary

The **20GB diffdisk** is a **sparse virtual disk** for your Colima Docker VM. It's allocated 20GB but only uses **1.4GB** of actual disk space. The contents are Docker-related (images, containers, volumes) that accumulate as you use Docker through Colima.

