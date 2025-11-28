#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const SOURCE = path.join(__dirname, '..', '.ai-context-source-of-truth.json');

const status = JSON.parse(fs.readFileSync(SOURCE, 'utf8'));

function md() {
  return `# SYSTEM STATUS – EVENT DRIVEN ORGANISM

**Last Updated**: ${status.timestamp}
**Health**: ${status.health.score}% (${status.health.status})

## BACKEND

${status.backend.running ? '[RUNNING]' : '[NOT RUNNING]'} (Port ${status.backend.port})

## EXTENSION

${status.extension.exists ? '[EXISTS]' : '[NOT FOUND]'} (${status.extension.manifest?.version || 'unknown'})

## GIT

Latest Commit: ${status.commit}

`;
}

fs.writeFileSync(
  path.join(__dirname, '..', 'DRIFT_STATUS_VISUAL.md'),
  md()
);

console.log("Dashboards updated.");
