#!/usr/bin/env node
/**
 * Git hook script to block forbidden files from being staged or committed.
 * Reads patterns from .forbidden-paths.regex and checks staged files.
 */

import { execSync } from 'node:child_process'
import { readFileSync, existsSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const projectRoot = join(__dirname, '..', '..')

function loadForbiddenPatterns() {
  const patternsFile = join(projectRoot, '.forbidden-paths.regex')
  if (!existsSync(patternsFile)) {
    console.log('No .forbidden-paths.regex found, skipping check.')
    return []
  }

  const content = readFileSync(patternsFile, 'utf-8')
  return content
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith('#'))
    .map((pattern) => new RegExp(pattern))
}

function getStagedFiles() {
  try {
    const output = execSync('git diff --cached --name-only --diff-filter=ACMR', {
      encoding: 'utf-8',
      cwd: projectRoot,
    })
    return output.trim().split('\n').filter(Boolean)
  } catch {
    return []
  }
}

function main() {
  const patterns = loadForbiddenPatterns()
  if (patterns.length === 0) process.exit(0)

  const stagedFiles = getStagedFiles()
  if (stagedFiles.length === 0) process.exit(0)

  const forbidden = []
  for (const file of stagedFiles) {
    for (const pattern of patterns) {
      if (pattern.test(file)) {
        forbidden.push({ file, pattern: pattern.source })
        break
      }
    }
  }

  if (forbidden.length > 0) {
    console.error('Forbidden files detected in staging area:')
    for (const { file, pattern } of forbidden) {
      console.error(`- ${file}`)
      console.error(`  Pattern: ${pattern}`)
    }
    console.error('Fix: git reset HEAD <file> and update .gitignore if needed.')
    process.exit(1)
  }

  console.log('No forbidden files in staging area')
  process.exit(0)
}

main()
#!/usr/bin/env node
/**
 * Git hook script to block forbidden files from being staged or committed.
 * Reads patterns from .forbidden-paths.regex and checks staged files.
 */

import { execSync } from 'node:child_process'
import { readFileSync, existsSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const projectRoot = join(__dirname, '..', '..')

function loadForbiddenPatterns() {
  const patternsFile = join(projectRoot, '.forbidden-paths.regex')
  if (!existsSync(patternsFile)) {
    console.log('No .forbidden-paths.regex found, skipping check.')
    return []
  }

  const content = readFileSync(patternsFile, 'utf-8')
  return content
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith('#'))
    .map((pattern) => new RegExp(pattern))
}

function getStagedFiles() {
  try {
    const output = execSync('git diff --cached --name-only --diff-filter=ACMR', {
      encoding: 'utf-8',
      cwd: projectRoot,
    })
    return output.trim().split('\n').filter(Boolean)
  } catch {
    return []
  }
}

function main() {
  const patterns = loadForbiddenPatterns()
  if (patterns.length === 0) process.exit(0)

  const stagedFiles = getStagedFiles()
  if (stagedFiles.length === 0) process.exit(0)

  const forbidden = []
  for (const file of stagedFiles) {
    for (const pattern of patterns) {
      if (pattern.test(file)) {
        forbidden.push({ file, pattern: pattern.source })
        break
      }
    }
  }

  if (forbidden.length > 0) {
    console.error('Forbidden files detected in staging area:')
    for (const { file, pattern } of forbidden) {
      console.error(`- ${file}`)
      console.error(`  Pattern: ${pattern}`)
    }
    console.error('Fix: git reset HEAD <file> and update .gitignore if needed.')
    process.exit(1)
  }

  console.log('No forbidden files in staging area')
  process.exit(0)
}

main()
