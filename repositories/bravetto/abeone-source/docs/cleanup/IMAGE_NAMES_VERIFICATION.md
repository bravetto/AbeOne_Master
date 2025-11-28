# Image Name Consistency Verification

##  Verified Image Names

All image names are now consistent across:
- `docker-compose.yml`
- `scripts/build-all-images.sh`
- `scripts/build-all-images.ps1`

##  Image Name Mapping

| Service Name | Image Name | Container Name |
|-------------|-----------|----------------|
| Gateway | `aiguards-gateway:dev` | `codeguardians-gateway-dev` |
| TokenGuard | `aiguards-tokenguard:dev` | `codeguardians-tokenguard` |
| TrustGuard | `aiguards-trustguard:dev` | `codeguardians-trustguard` |
| ContextGuard | `aiguards-contextguard:dev` | `codeguardians-contextguard` |
| BiasGuard | `aiguards-biasguard:dev` | `codeguardians-biasguard` |
| HealthGuard | `aiguards-healthguard:dev` | `codeguardians-healthguard` |

##  Naming Convention

- **Image Names**: `aiguards-{service}:{tag}`
  - Prefix: `aiguards-`
  - Service names: `gateway`, `tokenguard`, `trustguard`, `contextguard`, `biasguard`, `healthguard`
  - Default tag: `dev`
  
- **Container Names**: `codeguardians-{service}`
  - Prefix: `codeguardians-`
  - Gateway uses `codeguardians-gateway-dev` (with `-dev` suffix)

##  Verification Results

### Docker Compose Images:
-  `aiguards-gateway:dev`
-  `aiguards-tokenguard:dev`
-  `aiguards-trustguard:dev`
-  `aiguards-contextguard:dev`
-  `aiguards-biasguard:dev`
-  `aiguards-healthguard:dev`

### Build Script Output (with IMAGE_TAG=dev):
-  `aiguards-gateway:dev`
-  `aiguards-tokenguard:dev`
-  `aiguards-trustguard:dev`
-  `aiguards-contextguard:dev`
-  `aiguards-biasguard:dev`
-  `aiguards-healthguard:dev`

##  Status

**All image names are consistent!** 

The build scripts will create images with names that exactly match what `docker-compose.yml` expects.

