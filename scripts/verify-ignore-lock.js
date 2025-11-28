#!/usr/bin/env node
const { validateIgnoreLock } = require('./validate-ignore-lock');
if (require.main === module) {
  process.exit(validateIgnoreLock());
}
module.exports = { validateIgnoreLock };

