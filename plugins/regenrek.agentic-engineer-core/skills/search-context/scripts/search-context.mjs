#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = path.resolve(SCRIPT_DIR, '..');

const KNOWN_COMMANDS = new Set(['help', 'check', 'run', 'library', 'clean']);
const BOOL_FLAGS = new Set([
  'help',
  'dry-run',
  'json',
  'verbose',
  'ssh',
  'refresh',
  'include-forks',
  'include-archived',
  'include-private',
  'no-clone',
  'project-local',
  'allow-unignored-worktree',
  'use-library'
]);

const STOPWORDS = new Set([
  'a', 'an', 'and', 'are', 'as', 'at', 'be', 'best', 'build', 'but', 'by', 'can', 'code',
  'create', 'do', 'for', 'from', 'generate', 'gernate', 'give', 'how', 'i', 'in', 'into',
  'is', 'it', 'latest', 'make', 'modern', 'new', 'of', 'on', 'or', 'our', 'please', 'project',
  'projects', 'reference', 'references', 'repo', 'repos', 'search', 'show', 'that', 'the', 'this',
  'to', 'use', 'using', 'want', 'we', 'what', 'with', 'wir', 'ich', 'brauche', 'suche', 'und',
  'oder', 'für', 'fuer', 'eine', 'einen', 'ein', 'der', 'die', 'das', 'als', 'latest'
]);

const DEFAULT_EXCLUDES = [
  '!.git',
  '!node_modules',
  '!vendor',
  '!dist',
  '!build',
  '!target',
  '!.next',
  '!coverage',
  '!DerivedData',
  '!Pods',
  '!Carthage',
  '!.build',
  '!__pycache__'
];

function main() {
  const { positional, opts } = parseArgs(process.argv.slice(2));
  let cmd = positional.shift() || 'help';

  if (!KNOWN_COMMANDS.has(cmd)) {
    positional.unshift(cmd);
    cmd = 'run';
  }

  try {
    if (cmd === 'help' || opts.help) {
      printHelp();
      return;
    }
    if (cmd === 'check') {
      commandCheck();
      return;
    }
    if (cmd === 'run') {
      commandRun(positional.join(' '), opts);
      return;
    }
    if (cmd === 'library') {
      const sub = positional.shift();
      if (sub === 'add') {
        commandLibraryAdd(positional, opts);
        return;
      }
      if (sub === 'list') {
        commandLibraryList(opts);
        return;
      }
      if (sub === 'search') {
        commandLibrarySearch(positional.join(' '), opts);
        return;
      }
      throw new Error('Expected: library add <path>, library list, or library search <query>');
    }
    if (cmd === 'clean') {
      commandClean(opts);
      return;
    }
  } catch (error) {
    console.error(`\nerror: ${error.message}`);
    if (opts.verbose && error.stack) {
      console.error(error.stack);
    }
    process.exitCode = 1;
  }
}

function parseArgs(argv) {
  const positional = [];
  const opts = {};

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--') {
      positional.push(...argv.slice(i + 1));
      break;
    }
    if (arg.startsWith('--')) {
      const raw = arg.slice(2);
      const eq = raw.indexOf('=');
      const key = eq >= 0 ? raw.slice(0, eq) : raw;
      const value = eq >= 0 ? raw.slice(eq + 1) : undefined;
      if (BOOL_FLAGS.has(key)) {
        opts[key] = value === undefined ? true : value !== 'false';
      } else if (value !== undefined) {
        opts[key] = value;
      } else {
        const next = argv[i + 1];
        if (!next || next.startsWith('--')) {
          throw new Error(`Missing value for --${key}`);
        }
        opts[key] = next;
        i += 1;
      }
    } else if (arg.startsWith('-') && arg.length > 1) {
      const key = shortFlag(arg);
      if (!key) {
        throw new Error(`Unknown short flag ${arg}`);
      }
      const next = argv[i + 1];
      if (!next || next.startsWith('--')) {
        throw new Error(`Missing value for ${arg}`);
      }
      opts[key] = next;
      i += 1;
    } else {
      positional.push(arg);
    }
  }

  return { positional, opts };
}

function shortFlag(flag) {
  if (flag === '-p') return 'preset';
  if (flag === '-o') return 'output';
  if (flag === '-n') return 'max-repos';
  return null;
}

function printHelp() {
  console.log(`github-reference-context\n\nUsage:\n  search-context check\n  search-context run <query> [options]\n  search-context library add <path> [options]\n  search-context library list [options]\n  search-context library search <query> [options]\n  search-context clean [options]\n\nExamples:\n  search-context run "visual progress indicator ring for ios app latest 2026" --preset ios-swift\n  search-context run "React circular progress ring" --preset web-react --use-library\n  search-context run "SwiftUI progress ring" --sources library,github --project current\n  search-context library add ../third-party/some-repo --tags react,ui --presets web-react --project current\n  search-context library search "Circle().trim"\n\nRun options:\n  --preset <id>          ios-swift, web-react, generic\n  --sources <list>       github, library, or library,github; default github\n  --use-library          shorthand for --sources library,github\n  --project <id>         use a named library cluster; use current for this worktree\n  --max-repos <n>        repos to include in the manifest, default 5\n  --candidates <n>       candidates per GitHub search phrase, default 12\n  --library-candidates <n> local library candidates to inspect, default max repos\n  --searches <n>         max expanded search phrases, default 6\n  --min-stars <n>        minimum stars, default 5\n  --fresh <yyyy-mm-dd>   pushed-after filter, default Jan 1 two years ago\n  --cache-dir <path>     cache root, default OS user cache\n  --refs-dir <path>      clone target, default <cache>/refs\n  --output <path>        manifest path, default <cache>/runs/<timestamp>/reference-context.md\n  --project-local        use .refs and .context in the current directory\n  --allow-unignored-worktree  allow writes inside a git worktree even if not ignored\n  --ssh                  clone via ssh_url\n  --include-forks        include forks\n  --include-archived     include archived repositories\n  --include-private      do not add is:public to GitHub search\n  --refresh              refresh cached repos\n  --dry-run              discover and rank without cloning\n  --json                 print JSON summary\n  --verbose              print extra details\n`);
}

function commandCheck() {
  const tools = [
    { name: 'node', args: ['--version'], required: true },
    { name: 'gh', args: ['--version'], required: true },
    { name: 'git', args: ['--version'], required: true },
    { name: 'rg', args: ['--version'], required: true }
  ];

  let ok = true;
  console.log('Checking local tools...\n');
  for (const tool of tools) {
    const result = runCommand(tool.name, tool.args, { allowFailure: true });
    if (result.ok) {
      const firstLine = `${result.stdout}${result.stderr}`.trim().split('\n')[0];
      console.log(`✓ ${tool.name}: ${firstLine}`);
    } else {
      ok = false;
      console.log(`✗ ${tool.name}: not available`);
    }
  }

  const auth = runCommand('gh', ['auth', 'status'], { allowFailure: true });
  if (auth.ok) {
    console.log('✓ gh auth: authenticated');
  } else {
    ok = false;
    console.log('✗ gh auth: not authenticated, run `gh auth login`');
  }

  if (!ok) {
    process.exitCode = 1;
  }
}

function commandRun(rawQuery, opts) {
  const query = cleanGoal(rawQuery);
  if (!query) {
    throw new Error('Missing query. Example: search-context run "SwiftUI progress ring" --preset ios-swift');
  }

  const presetId = opts.preset || inferPreset(query);
  const preset = loadPreset(presetId);
  const maxRepos = intOption(opts, 'max-repos', 5);
  const candidates = intOption(opts, 'candidates', 12);
  const maxSearches = intOption(opts, 'searches', 6);
  const minStars = intOption(opts, 'min-stars', 5);
  const fresh = normalizeFresh(opts.fresh || defaultFreshDate());
  const { refsDir, output, cacheRoot, projectLocal } = resolveRunPaths(opts);
  const dryRun = Boolean(opts['dry-run'] || opts['no-clone']);
  const sources = resolveSources(opts);

  guardRunTargets({ refsDir, output, dryRun, opts });
  ensureDir(path.dirname(output));
  if (!dryRun) ensureDir(refsDir);

  const searchPhrases = expandSearchPhrases(query, preset).slice(0, maxSearches);
  const inspectTerms = buildInspectTerms(query, preset);

  log(opts, `Preset: ${preset.id}`);
  log(opts, `Sources: ${sources.join(', ')}`);
  log(opts, `Search phrases: ${searchPhrases.join(' | ')}`);

  const libraryDiscovery = sources.includes('library')
    ? discoverLibraryReferences({ query, preset, inspectTerms, opts })
    : emptyDiscovery();

  const githubDiscovery = sources.includes('github')
    ? discoverRepositories({ query, preset, searchPhrases, candidates, minStars, fresh, opts })
    : emptyDiscovery();

  const scored = githubDiscovery.repositories
    .map((repo) => scoreRepoMetadata(repo, query, preset, { fresh }))
    .sort((a, b) => b.score - a.score);

  const githubSelected = scored.slice(0, Math.max(maxRepos, 0));
  const failures = [...libraryDiscovery.failures, ...githubDiscovery.failures];

  if (libraryDiscovery.repositories.length === 0 && githubSelected.length === 0) {
    failures.push(`No repositories were discovered from sources: ${sources.join(', ')}.`);
  }

  for (const repo of githubSelected) {
    if (dryRun) {
      repo.clone = { status: 'dry-run', localPath: null };
      repo.inspection = { matches: [], files: [], score: 0, terms: inspectTerms };
      continue;
    }

    try {
      repo.clone = cloneRepository(repo, refsDir, opts);
      repo.localPath = repo.clone.localPath;
    } catch (error) {
      repo.clone = { status: 'failed', error: error.message, localPath: null };
      repo.inspection = { matches: [], files: [], score: 0, terms: inspectTerms };
      failures.push(`Clone failed for ${repo.fullName}: ${error.message}`);
      continue;
    }

    try {
      repo.inspection = inspectRepository(repo, preset, inspectTerms, opts);
      repo.score += repo.inspection.score;
      repo.reasons.push(...repo.inspection.reasons);
    } catch (error) {
      repo.inspection = { matches: [], files: [], score: 0, terms: inspectTerms, reasons: [] };
      failures.push(`Inspection failed for ${repo.fullName}: ${error.message}`);
    }
  }

  const selected = [...libraryDiscovery.repositories, ...githubSelected].sort((a, b) => b.score - a.score).slice(0, Math.max(maxRepos, 0));
  selected.sort((a, b) => b.score - a.score);

  const summary = {
    generatedAt: new Date().toISOString(),
    goal: query,
    preset: preset.id,
    settings: {
      maxRepos,
      candidates,
      minStars,
      fresh,
      refsDir,
      output,
      cacheRoot,
      projectLocal,
      sources,
      dryRun
    },
    searchPhrases,
    inspectTerms,
    discovery: {
      total: libraryDiscovery.total + githubDiscovery.repositories.length,
      failures: [...libraryDiscovery.failures, ...githubDiscovery.failures],
      reports: githubDiscovery.reports,
      library: libraryDiscovery.reports
    },
    repositories: selected,
    failures
  };

  const manifest = renderManifest(summary, preset);
  fs.writeFileSync(output, manifest, 'utf8');

  const jsonOutput = jsonOutputPath(output);
  fs.writeFileSync(jsonOutput, JSON.stringify(toJsonSafe(summary), null, 2), 'utf8');

  console.log(`\nWrote manifest: ${formatPathForDisplay(output)}`);
  console.log(`Wrote JSON:     ${formatPathForDisplay(jsonOutput)}`);
  if (!dryRun) {
    console.log(`Refs dir:       ${formatPathForDisplay(refsDir)}`);
  }

  if (opts.json) {
    console.log(JSON.stringify(toJsonSafe(summary), null, 2));
  }
}

function commandLibraryAdd(positional, opts) {
  const rawPath = positional.shift();
  if (!rawPath) {
    throw new Error('Missing path. Example: search-context library add ../third-party/repo --tags react,ui');
  }

  const localPath = path.resolve(process.cwd(), rawPath);
  if (!fs.existsSync(localPath) || !fs.statSync(localPath).isDirectory()) {
    throw new Error(`library path must be an existing directory: ${formatPathForDisplay(localPath)}`);
  }

  const registry = loadLibraryRegistry(opts);
  const entry = buildLibraryEntry(localPath, opts);
  upsertLibraryEntry(registry, entry);

  const project = resolveProjectRef(opts);
  if (project) {
    attachLibraryEntryToProject(registry, project, entry.id, opts.notes || '');
  }

  saveLibraryRegistry(registry, opts);
  console.log(`Added library reference: ${entry.id}`);
  console.log(`Path: ${formatPathForDisplay(entry.localPath)}`);
  if (project) console.log(`Project: ${project.id}`);
}

function commandLibraryList(opts) {
  const registry = loadLibraryRegistry(opts);
  const project = resolveProjectRef(opts);
  const repositories = project ? repositoriesForProject(registry, project.id) : registry.repositories;

  if (repositories.length === 0) {
    console.log(project ? `No library references for project ${project.id}.` : 'No library references registered.');
    return;
  }

  for (const repo of repositories) {
    const tags = repo.tags?.length ? ` [${repo.tags.join(', ')}]` : '';
    const presets = repo.presets?.length ? ` presets=${repo.presets.join(',')}` : '';
    console.log(`${repo.id}${tags}${presets}`);
    console.log(`  ${formatPathForDisplay(repo.localPath)}`);
  }
}

function commandLibrarySearch(rawQuery, opts) {
  const query = cleanGoal(rawQuery);
  if (!query) {
    throw new Error('Missing library search query.');
  }
  const roots = collectLibrarySearchRoots(opts);
  if (roots.length === 0) {
    throw new Error('No local references found. Add one with `search-context library add <path>` or run a GitHub search first.');
  }

  const args = [
    '--line-number',
    '--no-heading',
    '--smart-case',
    '--hidden',
    '--fixed-strings',
    '--max-count',
    String(intOption(opts, 'max-count', 20)),
    '--glob', '!.git',
    '--glob', '!node_modules',
    '--glob', '!dist',
    '--glob', '!build',
    '-e', query
  ];
  args.push(...roots.map((root) => root.localPath));

  const result = runCommand('rg', args, { allowFailure: true });
  if (!result.ok && result.status !== 1) {
    throw new Error(result.stderr || result.stdout || 'rg failed');
  }
  const out = result.stdout.trim();
  if (!out) {
    console.log('No local reference matches.');
    return;
  }
  console.log(out);
}

function commandClean(opts) {
  const refsDir = resolveRefsDir(opts);
  const olderThan = opts['older-than'] || '30d';
  const ms = parseDuration(olderThan);
  if (!fs.existsSync(refsDir)) {
    console.log(`Nothing to clean. Missing refs dir: ${formatPathForDisplay(refsDir)}`);
    return;
  }

  const now = Date.now();
  const entries = fs.readdirSync(refsDir, { withFileTypes: true });
  let removed = 0;

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const dir = path.join(refsDir, entry.name);
    const gitDir = path.join(dir, '.git');
    if (!fs.existsSync(gitDir)) continue;
    const stat = fs.statSync(dir);
    if (now - stat.mtimeMs > ms) {
      fs.rmSync(dir, { recursive: true, force: true });
      removed += 1;
      console.log(`removed ${path.relative(process.cwd(), dir)}`);
    }
  }

  console.log(`Clean complete. Removed ${removed} cached reference repos.`);
}

function discoverLibraryReferences({ query, preset, inspectTerms, opts }) {
  const registry = loadLibraryRegistry(opts);
  const project = resolveProjectRef(opts);
  const entries = project ? repositoriesForProject(registry, project.id) : mergeLibraryEntries(registry.repositories, referenceEntriesFromRefsDir(opts));
  const maxCandidates = intOption(opts, 'library-candidates', intOption(opts, 'max-repos', 5));
  const failures = [];
  const reports = [];

  const candidates = entries
    .filter((entry) => fs.existsSync(entry.localPath))
    .map((entry) => scoreLibraryEntry(entry, query, preset, project))
    .filter((entry) => entry.score > 0 || hasPresetMatch(entry, preset) || hasQueryTokenMatch(entry, query))
    .sort((a, b) => b.score - a.score)
    .slice(0, Math.max(maxCandidates, 0));

  for (const entry of entries) {
    if (!fs.existsSync(entry.localPath)) {
      failures.push(`Library reference missing on disk: ${entry.id} at ${entry.localPath}`);
    }
  }

  const repositories = [];
  for (const entry of candidates) {
    const repo = libraryEntryToRepo(entry);
    try {
      repo.inspection = inspectRepository(repo, preset, inspectTerms, opts);
      repo.score += repo.inspection.score;
      repo.reasons.push(...repo.inspection.reasons);
    } catch (error) {
      repo.inspection = { matches: [], files: [], score: 0, terms: inspectTerms, reasons: [] };
      failures.push(`Library inspection failed for ${entry.id}: ${error.message}`);
    }
    repositories.push(repo);
  }

  reports.push({
    source: 'library',
    project: project?.id || null,
    candidates: entries.length,
    inspected: repositories.length
  });

  return { repositories, failures, reports, total: entries.length };
}

function emptyDiscovery() {
  return { repositories: [], failures: [], reports: [], total: 0 };
}

function discoverRepositories({ preset, searchPhrases, candidates, minStars, fresh, opts }) {
  const languages = parseLanguages(opts.language, preset.github?.languages || []);
  const searchCombos = [];

  for (const phrase of searchPhrases) {
    if (languages.length === 0) {
      searchCombos.push({ phrase, language: null });
    } else {
      for (const language of languages) {
        searchCombos.push({ phrase, language });
      }
    }
  }

  const repos = new Map();
  const failures = [];
  const reports = [];

  for (const combo of searchCombos) {
    const q = buildGitHubQuery(combo.phrase, combo.language, { minStars, fresh, opts });
    const args = [
      'api',
      '-X', 'GET',
      'search/repositories',
      '-f', `q=${q}`,
      '-f', 'sort=updated',
      '-f', 'order=desc',
      '-f', `per_page=${candidates}`
    ];

    log(opts, `gh ${args.map(shellQuote).join(' ')}`);
    const result = runCommand('gh', args, { allowFailure: true });
    const report = { phrase: combo.phrase, language: combo.language, query: q, ok: result.ok, count: 0 };

    if (!result.ok) {
      const message = compactWhitespace(result.stderr || result.stdout || `gh api failed with status ${result.status}`);
      failures.push(`GitHub search failed for ${combo.phrase}${combo.language ? ` / ${combo.language}` : ''}: ${message}`);
      report.error = message;
      reports.push(report);
      continue;
    }

    let parsed;
    try {
      parsed = JSON.parse(result.stdout);
    } catch (error) {
      failures.push(`Could not parse GitHub response for ${combo.phrase}: ${error.message}`);
      report.error = error.message;
      reports.push(report);
      continue;
    }

    const items = Array.isArray(parsed.items) ? parsed.items : [];
    report.count = items.length;
    reports.push(report);

    for (const item of items) {
      const repo = normalizeRepo(item, combo.phrase, combo.language);
      if (!repo.fullName) continue;
      const existing = repos.get(repo.fullName);
      if (existing) {
        existing.matchedSearchPhrases.add(combo.phrase);
        if (combo.language) existing.matchedLanguages.add(combo.language);
        continue;
      }
      repos.set(repo.fullName, repo);
    }
  }

  return { repositories: [...repos.values()], failures, reports };
}

function normalizeRepo(item, phrase, language) {
  return {
    id: item.id,
    fullName: item.full_name,
    name: item.name,
    owner: item.owner?.login || '',
    description: item.description || '',
    url: item.html_url,
    cloneUrl: item.clone_url,
    sshUrl: item.ssh_url,
    defaultBranch: item.default_branch || null,
    language: item.language || null,
    stars: item.stargazers_count || 0,
    forks: item.forks_count || 0,
    watchers: item.watchers_count || 0,
    size: item.size || 0,
    archived: Boolean(item.archived),
    disabled: Boolean(item.disabled),
    fork: Boolean(item.fork),
    pushedAt: item.pushed_at || null,
    updatedAt: item.updated_at || null,
    createdAt: item.created_at || null,
    license: item.license?.spdx_id || item.license?.name || null,
    matchedSearchPhrases: new Set([phrase]),
    matchedLanguages: new Set(language ? [language] : [])
  };
}

function buildLibraryEntry(localPath, opts) {
  const remoteUrl = gitConfig(localPath, 'remote.origin.url');
  const fullName = parseGitRemoteFullName(remoteUrl);
  const name = opts.name || fullName || path.basename(localPath);
  const id = fullName || `local:${hashString(localPath).slice(0, 12)}`;
  const existingMeta = readSearchContextMeta(localPath);

  return {
    id,
    name,
    fullName,
    localPath,
    source: fullName ? 'github-cache' : 'local',
    remoteUrl: remoteUrl || null,
    url: fullName ? `https://github.com/${fullName}` : null,
    tags: parseList(opts.tags),
    presets: parseList(opts.presets || opts.preset),
    license: opts.license || existingMeta?.license || detectLicense(localPath),
    notes: opts.notes || '',
    addedAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };
}

function upsertLibraryEntry(registry, entry) {
  const existingIndex = registry.repositories.findIndex((repo) => repo.id === entry.id || path.resolve(repo.localPath) === path.resolve(entry.localPath));
  if (existingIndex >= 0) {
    const existing = registry.repositories[existingIndex];
    registry.repositories[existingIndex] = {
      ...existing,
      ...entry,
      addedAt: existing.addedAt || entry.addedAt,
      tags: unique([...(existing.tags || []), ...(entry.tags || [])]),
      presets: unique([...(existing.presets || []), ...(entry.presets || [])])
    };
  } else {
    registry.repositories.push(entry);
  }
  registry.repositories.sort((a, b) => String(a.id).localeCompare(String(b.id)));
  registry.updatedAt = new Date().toISOString();
}

function attachLibraryEntryToProject(registry, project, repoId, notes) {
  const current = registry.projects[project.id] || {
    id: project.id,
    name: project.name,
    root: project.root,
    preferredRepos: [],
    ignoredRepos: [],
    notes: ''
  };
  current.name = project.name;
  current.root = project.root;
  current.preferredRepos = unique([...(current.preferredRepos || []), repoId]);
  current.notes = notes || current.notes || '';
  current.updatedAt = new Date().toISOString();
  registry.projects[project.id] = current;
}

function repositoriesForProject(registry, projectId) {
  const project = registry.projects[projectId];
  if (!project) return [];
  const preferred = new Set(project.preferredRepos || []);
  const ignored = new Set(project.ignoredRepos || []);
  return registry.repositories.filter((repo) => preferred.has(repo.id) && !ignored.has(repo.id));
}

function referenceEntriesFromRefsDir(opts) {
  const refsDir = resolveRefsDir(opts);
  if (!fs.existsSync(refsDir)) return [];

  const entries = [];
  for (const dirent of fs.readdirSync(refsDir, { withFileTypes: true })) {
    if (!dirent.isDirectory()) continue;
    const localPath = path.join(refsDir, dirent.name);
    if (!fs.existsSync(path.join(localPath, '.git'))) continue;
    const meta = readSearchContextMeta(localPath);
    const fullName = meta?.fullName || dirent.name.replace(/__/g, '/');
    entries.push({
      id: fullName,
      name: fullName.split('/').pop(),
      fullName,
      localPath,
      source: 'github-cache',
      remoteUrl: meta?.cloneUrl || null,
      url: meta?.url || (fullName.includes('/') ? `https://github.com/${fullName}` : null),
      tags: [],
      presets: [],
      license: meta?.license || detectLicense(localPath),
      notes: 'cached GitHub reference clone',
      addedAt: meta?.updatedAt || null,
      updatedAt: meta?.updatedAt || null
    });
  }
  return entries;
}

function mergeLibraryEntries(primary, secondary) {
  const map = new Map();
  for (const entry of [...secondary, ...primary]) {
    map.set(entry.id || path.resolve(entry.localPath), entry);
  }
  return [...map.values()];
}

function scoreLibraryEntry(entry, query, preset, project) {
  const tokens = extractTokens(query);
  const haystack = `${entry.id} ${entry.name} ${entry.fullName || ''} ${(entry.tags || []).join(' ')} ${entry.notes || ''}`.toLowerCase();
  const tokenMatches = tokens.filter((token) => haystack.includes(token.toLowerCase()));
  const reasons = ['registered local library reference'];
  let score = 20;

  if (tokenMatches.length) {
    score += Math.min(24, tokenMatches.length * 4);
    reasons.push(`intent terms matched library metadata: ${tokenMatches.slice(0, 6).join(', ')}`);
  }
  if (hasPresetMatch(entry, preset)) {
    score += 15;
    reasons.push(`preset match: ${preset.id}`);
  }
  if (project) {
    score += 10;
    reasons.push(`project library match: ${project.id}`);
  }
  if (entry.license) {
    score += 5;
    reasons.push(`license: ${entry.license}`);
  }

  return { ...entry, score, reasons };
}

function hasPresetMatch(entry, preset) {
  return (entry.presets || []).includes(preset.id);
}

function hasQueryTokenMatch(entry, query) {
  const haystack = `${entry.id} ${entry.name} ${entry.fullName || ''} ${(entry.tags || []).join(' ')}`.toLowerCase();
  return extractTokens(query).some((token) => haystack.includes(token.toLowerCase()));
}

function libraryEntryToRepo(entry) {
  const fullName = entry.fullName || entry.name || entry.id;
  return {
    id: entry.id,
    fullName,
    name: entry.name || path.basename(entry.localPath),
    owner: entry.fullName ? entry.fullName.split('/')[0] : 'local',
    description: entry.notes || '',
    url: entry.url || entry.remoteUrl || entry.localPath,
    cloneUrl: null,
    sshUrl: null,
    defaultBranch: null,
    language: null,
    stars: 0,
    forks: 0,
    watchers: 0,
    size: 0,
    archived: false,
    disabled: false,
    fork: false,
    pushedAt: null,
    updatedAt: entry.updatedAt || null,
    createdAt: entry.addedAt || null,
    license: entry.license || null,
    localPath: entry.localPath,
    source: 'library',
    clone: { status: 'library', localPath: entry.localPath },
    score: entry.score || 0,
    reasons: entry.reasons || ['registered local library reference'],
    matchedSearchPhrases: new Set(),
    matchedLanguages: new Set()
  };
}

function scoreRepoMetadata(repo, query, preset, settings) {
  const reasons = [];
  let score = 0;

  const haystack = `${repo.fullName} ${repo.description}`.toLowerCase();
  const tokens = extractTokens(query);
  const tokenMatches = tokens.filter((t) => haystack.includes(t.toLowerCase()));
  if (tokenMatches.length) {
    const points = Math.min(24, tokenMatches.length * 4);
    score += points;
    reasons.push(`intent terms matched metadata: ${tokenMatches.slice(0, 6).join(', ')}`);
  }

  const languages = new Set((preset.github?.languages || []).map((l) => l.toLowerCase()));
  if (repo.language && languages.has(repo.language.toLowerCase())) {
    score += 15;
    reasons.push(`language match: ${repo.language}`);
  } else if (repo.language) {
    score += 3;
    reasons.push(`primary language: ${repo.language}`);
  }

  if (!repo.archived) {
    score += 10;
    reasons.push('not archived');
  } else {
    score -= 50;
    reasons.push('archived');
  }

  if (!repo.fork) {
    score += 6;
    reasons.push('not a fork');
  } else {
    score -= 8;
    reasons.push('fork');
  }

  if (repo.license) {
    score += 5;
    reasons.push(`license: ${repo.license}`);
  }

  if (repo.pushedAt && settings.fresh && dateGte(repo.pushedAt, settings.fresh)) {
    score += 15;
    reasons.push(`pushed after ${settings.fresh}`);
  } else if (repo.pushedAt) {
    score -= 6;
    reasons.push(`older than freshness target: ${repo.pushedAt.slice(0, 10)}`);
  }

  const starScore = Math.min(18, Math.round(Math.log10(repo.stars + 1) * 7));
  score += starScore;
  if (repo.stars > 0) reasons.push(`${repo.stars} stars`);

  if (repo.size > 0 && repo.size < 50000) {
    score += 6;
    reasons.push('small or medium repo size');
  } else if (repo.size > 200000) {
    score -= 8;
    reasons.push('large repo size');
  }

  const exampleWords = ['example', 'examples', 'demo', 'sample', 'showcase', 'starter'];
  const exampleHit = exampleWords.find((word) => haystack.includes(word));
  if (exampleHit) {
    score += 8;
    reasons.push(`example/demo signal: ${exampleHit}`);
  }

  return { ...repo, score, reasons };
}

function cloneRepository(repo, refsDir, opts) {
  const localName = sanitizeRepoName(repo.fullName);
  const localPath = path.join(refsDir, localName);
  ensureDir(refsDir);

  if (fs.existsSync(localPath)) {
    if (opts.refresh) {
      const branch = repo.defaultBranch || 'HEAD';
      const fetch = runCommand('git', ['-C', localPath, 'fetch', '--depth=1', '--filter=blob:none', '--no-tags', 'origin', branch], { allowFailure: true });
      if (!fetch.ok) {
        throw new Error(fetch.stderr || fetch.stdout || 'git fetch failed');
      }
      const checkout = runCommand('git', ['-C', localPath, 'checkout', '--detach', 'FETCH_HEAD'], { allowFailure: true });
      if (!checkout.ok) {
        throw new Error(checkout.stderr || checkout.stdout || 'git checkout failed');
      }
      writeRepoMeta(localPath, repo, 'refreshed');
      return { status: 'refreshed', localPath };
    }
    return { status: 'cached', localPath };
  }

  const url = opts.ssh ? repo.sshUrl : repo.cloneUrl;
  if (!url) {
    throw new Error('missing clone URL');
  }

  const args = ['clone', '--depth=1', '--filter=blob:none', '--single-branch', '--no-tags'];
  if (repo.defaultBranch) {
    args.push('--branch', repo.defaultBranch);
  }
  args.push(url, localPath);

  let result = runCommand('git', args, { allowFailure: true });
  if (!result.ok && repo.defaultBranch) {
    const retryArgs = ['clone', '--depth=1', '--filter=blob:none', '--single-branch', '--no-tags', url, localPath];
    result = runCommand('git', retryArgs, { allowFailure: true });
  }

  if (!result.ok) {
    throw new Error(result.stderr || result.stdout || 'git clone failed');
  }

  writeRepoMeta(localPath, repo, 'cloned');
  return { status: 'cloned', localPath };
}

function inspectRepository(repo, preset, terms, opts) {
  if (!repo.localPath || !fs.existsSync(repo.localPath)) {
    return { matches: [], files: [], score: 0, terms, reasons: ['no local path'] };
  }

  const args = [
    '--json',
    '--line-number',
    '--smart-case',
    '--hidden',
    '--fixed-strings',
    '--max-count', '8'
  ];

  for (const exclude of DEFAULT_EXCLUDES) {
    args.push('--glob', exclude);
  }

  const fileGlobs = Array.isArray(preset.fileGlobs) ? preset.fileGlobs : [];
  for (const glob of fileGlobs) {
    args.push('--glob', glob);
  }

  const usableTerms = unique(terms.filter((t) => t && t.trim().length >= 2)).slice(0, 32);
  for (const term of usableTerms) {
    args.push('-e', term);
  }
  args.push(repo.localPath);

  const result = runCommand('rg', args, { allowFailure: true, maxBuffer: 10 * 1024 * 1024 });
  if (!result.ok && result.status !== 1) {
    throw new Error(result.stderr || result.stdout || 'rg failed');
  }

  const matches = parseRipgrepJson(result.stdout, repo.localPath).slice(0, 160);
  const files = groupMatchesByFile(matches, preset).slice(0, 8);
  const matchedTerms = unique(matches.map((m) => m.matchText).filter(Boolean));
  const score = Math.min(35, files.reduce((sum, file) => sum + file.score, 0));
  const reasons = [];

  if (files.length > 0) {
    reasons.push(`local matches in ${files.length} relevant file${files.length === 1 ? '' : 's'}`);
  } else {
    reasons.push('no local implementation matches from inspection terms');
  }
  if (matchedTerms.length > 0) {
    reasons.push(`matched local terms: ${matchedTerms.slice(0, 6).join(', ')}`);
  }

  return { matches, files, score, terms: usableTerms, reasons };
}

function parseRipgrepJson(stdout, root) {
  const matches = [];
  const lines = stdout.split('\n');
  for (const line of lines) {
    if (!line.trim()) continue;
    let event;
    try {
      event = JSON.parse(line);
    } catch {
      continue;
    }
    if (event.type !== 'match') continue;
    const data = event.data || {};
    const absPath = data.path?.text || '';
    const relPath = path.relative(root, absPath);
    const lineText = (data.lines?.text || '').replace(/\s+$/u, '');
    const sub = Array.isArray(data.submatches) && data.submatches.length > 0 ? data.submatches[0] : null;
    const matchText = sub?.match?.text || null;
    matches.push({
      file: relPath || absPath,
      line: data.line_number || 0,
      text: lineText,
      matchText
    });
  }
  return matches;
}

function groupMatchesByFile(matches, preset) {
  const map = new Map();
  for (const match of matches) {
    if (!map.has(match.file)) {
      map.set(match.file, { file: match.file, matches: [], uniqueTerms: new Set(), score: 0 });
    }
    const group = map.get(match.file);
    group.matches.push(match);
    if (match.matchText) group.uniqueTerms.add(match.matchText.toLowerCase());
  }

  const positives = (preset.positivePathHints || []).map((x) => x.toLowerCase());
  const negatives = (preset.negativePathHints || []).map((x) => x.toLowerCase());

  const groups = [...map.values()].map((group) => {
    const p = group.file.toLowerCase();
    let score = Math.min(12, group.matches.length * 2) + group.uniqueTerms.size * 3;
    for (const hint of positives) {
      if (p.includes(hint)) score += 3;
    }
    for (const hint of negatives) {
      if (p.includes(hint)) score -= 6;
    }
    const snippets = group.matches.slice(0, 4).map((m) => ({
      line: m.line,
      text: trimSnippet(m.text)
    }));
    return {
      file: group.file,
      score,
      matchCount: group.matches.length,
      terms: [...group.uniqueTerms].slice(0, 8),
      snippets
    };
  });

  return groups.sort((a, b) => b.score - a.score);
}

function renderManifest(summary, preset) {
  const lines = [];
  lines.push('# Reference Context');
  lines.push('');
  lines.push(`Generated: ${summary.generatedAt}`);
  lines.push('');
  lines.push('## Goal');
  lines.push('');
  lines.push(summary.goal);
  lines.push('');
  lines.push('## Search settings');
  lines.push('');
  lines.push(`- Preset: \`${summary.preset}\``);
  lines.push(`- Sources: \`${summary.settings.sources.join(', ')}\``);
  lines.push(`- Max cloned repos: \`${summary.settings.maxRepos}\``);
  lines.push(`- Freshness: \`${summary.settings.fresh || 'none'}\``);
  lines.push(`- Minimum stars: \`${summary.settings.minStars}\``);
  lines.push(`- Dry run: \`${summary.settings.dryRun ? 'yes' : 'no'}\``);
  lines.push(`- Project local: \`${summary.settings.projectLocal ? 'yes' : 'no'}\``);
  lines.push(`- Refs dir: \`${formatPathForDisplay(summary.settings.refsDir)}\``);
  lines.push('');
  lines.push('## Search phrases');
  lines.push('');
  for (const phrase of summary.searchPhrases) {
    lines.push(`- ${phrase}`);
  }
  lines.push('');
  lines.push('## Agent instructions');
  lines.push('');
  lines.push('Open only the listed relevant files first. Study implementation patterns, API choices, state flow, animation behavior, styling, and example usage. Do not copy large code blocks. Respect repository licenses.');
  lines.push('');

  if (Array.isArray(preset.study) && preset.study.length > 0) {
    lines.push('Study these aspects:');
    lines.push('');
    for (const item of preset.study) lines.push(`- ${item}`);
    lines.push('');
  }

  if (Array.isArray(preset.doNotCopy) && preset.doNotCopy.length > 0) {
    lines.push('Do not copy:');
    lines.push('');
    for (const item of preset.doNotCopy) lines.push(`- ${item}`);
    lines.push('');
  }

  lines.push('## Best references');
  lines.push('');

  if (summary.repositories.length === 0) {
    lines.push('No repositories selected.');
    lines.push('');
  }

  summary.repositories.forEach((repo, index) => {
    lines.push(`### ${index + 1}. ${repo.fullName}`);
    lines.push('');
    lines.push(`- URL: ${repo.url}`);
    lines.push(`- Source: ${repo.source || 'github'}`);
    lines.push(`- Local path: ${repo.localPath ? `\`${formatPathForDisplay(repo.localPath)}\`` : '`not cloned`'}`);
    lines.push(`- Clone status: ${repo.clone?.status || 'unknown'}`);
    lines.push(`- Primary language: ${repo.language || 'unknown'}`);
    lines.push(`- Stars: ${repo.stars}`);
    lines.push(`- Pushed: ${repo.pushedAt ? repo.pushedAt.slice(0, 10) : 'unknown'}`);
    lines.push(`- License: ${repo.license || 'unknown'}`);
    lines.push(`- Score: ${Math.round(repo.score)}`);
    lines.push('');

    if (repo.description) {
      lines.push('Description:');
      lines.push('');
      lines.push(trimSnippet(repo.description, 260));
      lines.push('');
    }

    lines.push('Why useful:');
    lines.push('');
    for (const reason of unique(repo.reasons || []).slice(0, 10)) {
      lines.push(`- ${reason}`);
    }
    lines.push('');

    const files = repo.inspection?.files || [];
    if (files.length > 0) {
      lines.push('Relevant files:');
      lines.push('');
      for (const file of files.slice(0, 6)) {
        lines.push(`- \`${file.file}\` (${file.matchCount} matches)`);
        for (const snippet of file.snippets.slice(0, 3)) {
          lines.push(`  - line ${snippet.line}: ${inlineCode(snippet.text)}`);
        }
      }
      lines.push('');
    } else {
      lines.push('Relevant files: none verified by local inspection.');
      lines.push('');
    }

    if (repo.clone?.error) {
      lines.push(`Clone error: ${repo.clone.error}`);
      lines.push('');
    }
  });

  lines.push('## Search diagnostics');
  lines.push('');
  lines.push(`- Repositories discovered before ranking: ${summary.discovery.total}`);
  lines.push(`- Inspect terms used: ${summary.inspectTerms.slice(0, 24).map((t) => `\`${t}\``).join(', ')}`);
  lines.push('');

  if (summary.failures.length > 0) {
    lines.push('## Uncertainty and failures');
    lines.push('');
    for (const failure of unique(summary.failures)) {
      lines.push(`- ${failure}`);
    }
    lines.push('');
  }

  lines.push('## Next step for the coding agent');
  lines.push('');
  lines.push('Read the relevant files above, adapt the best patterns to the current project, then implement the requested feature. Keep copied snippets small and verify the result with the project build or tests when available.');
  lines.push('');

  return `${lines.join('\n')}\n`;
}

function expandSearchPhrases(raw, preset) {
  const clean = cleanGoal(raw);
  const tokens = extractTokens(clean);
  const lowerTokens = new Set(tokens.map((t) => t.toLowerCase()));
  const phrases = [];

  const compact = tokens.slice(0, 7).join(' ');
  if (compact) phrases.push(compact);

  for (const expansion of preset.expansions || []) {
    const triggers = expansion.whenAny || [];
    if (triggers.some((t) => lowerTokens.has(t.toLowerCase()) || clean.toLowerCase().includes(t.toLowerCase()))) {
      phrases.push(...(expansion.phrases || []));
    }
  }

  phrases.push(...(preset.searchPhrases || []));

  if (phrases.length === 0 && clean) phrases.push(clean);
  return unique(phrases.map(compactWhitespace).filter(Boolean));
}

function buildInspectTerms(raw, preset) {
  const terms = [];
  terms.push(...(preset.inspectTerms || []));

  const tokens = extractTokens(raw).filter((t) => t.length >= 4);
  terms.push(...tokens.slice(0, 12));

  for (let i = 0; i < tokens.length - 1 && i < 8; i += 1) {
    terms.push(`${tokens[i]} ${tokens[i + 1]}`);
  }

  return unique(terms.map((t) => String(t).trim()).filter(Boolean));
}

function buildGitHubQuery(phrase, language, { minStars, fresh, opts }) {
  const parts = [phrase];
  if (language) parts.push(`language:${quoteQualifier(language)}`);
  if (!opts['include-forks']) parts.push('fork:false');
  if (!opts['include-archived']) parts.push('archived:false');
  if (!opts['include-private']) parts.push('is:public');
  if (fresh) parts.push(`pushed:>=${fresh}`);
  if (minStars > 0) parts.push(`stars:>=${minStars}`);
  return parts.join(' ');
}

function parseLanguages(raw, fallback) {
  if (!raw) return Array.isArray(fallback) ? fallback : [];
  return parseList(raw);
}

function parseList(raw) {
  if (!raw) return [];
  if (Array.isArray(raw)) return unique(raw.map((x) => String(x).trim()).filter(Boolean));
  return unique(String(raw)
    .split(',')
    .map((x) => x.trim())
    .filter(Boolean));
}

function inferPreset(query) {
  const q = query.toLowerCase();
  if (/\b(ios|swift|swiftui|uikit|xcode|apple watch|watchos)\b/.test(q)) return 'ios-swift';
  if (/\b(react|next\.js|nextjs|vite|tailwind|shadcn|tsx|jsx)\b/.test(q)) return 'web-react';
  return 'generic';
}

function loadPreset(id) {
  const file = path.join(SKILL_ROOT, 'presets', `${id}.json`);
  if (!fs.existsSync(file)) {
    throw new Error(`Unknown preset '${id}'. Expected a JSON file at ${file}`);
  }
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function runCommand(cmd, args, options = {}) {
  const result = spawnSync(cmd, args, {
    encoding: 'utf8',
    maxBuffer: options.maxBuffer || 5 * 1024 * 1024,
    env: process.env
  });

  if (result.error) {
    return {
      ok: false,
      status: null,
      stdout: result.stdout || '',
      stderr: result.error.message
    };
  }

  const out = {
    ok: result.status === 0,
    status: result.status,
    stdout: result.stdout || '',
    stderr: result.stderr || ''
  };

  if (!out.ok && !options.allowFailure) {
    throw new Error(out.stderr || out.stdout || `${cmd} failed with status ${out.status}`);
  }

  return out;
}

function resolveSources(opts) {
  const raw = opts.sources || (opts['use-library'] ? 'library,github' : 'github');
  const sources = parseList(raw).map((source) => source.toLowerCase());
  const allowed = new Set(['github', 'library']);
  for (const source of sources) {
    if (!allowed.has(source)) {
      throw new Error(`Invalid --sources value '${source}'. Use github, library, or library,github.`);
    }
  }
  return sources.length ? unique(sources) : ['github'];
}

function loadLibraryRegistry(opts) {
  const file = libraryRegistryPath(opts);
  if (!fs.existsSync(file)) {
    return { version: 1, updatedAt: null, repositories: [], projects: {} };
  }

  const parsed = JSON.parse(fs.readFileSync(file, 'utf8'));
  return {
    version: parsed.version || 1,
    updatedAt: parsed.updatedAt || null,
    repositories: Array.isArray(parsed.repositories) ? parsed.repositories : [],
    projects: parsed.projects && typeof parsed.projects === 'object' ? parsed.projects : {}
  };
}

function saveLibraryRegistry(registry, opts) {
  const file = libraryRegistryPath(opts);
  ensureDir(path.dirname(file));
  registry.updatedAt = new Date().toISOString();
  fs.writeFileSync(file, JSON.stringify(registry, null, 2), 'utf8');
}

function libraryRegistryPath(opts) {
  return path.join(resolveCacheRoot(opts), 'library', 'repositories.json');
}

function collectLibrarySearchRoots(opts) {
  const roots = new Map();
  const registry = loadLibraryRegistry(opts);
  const project = resolveProjectRef(opts);
  const entries = project ? repositoriesForProject(registry, project.id) : registry.repositories;

  for (const entry of entries) {
    if (entry.localPath && fs.existsSync(entry.localPath)) {
      roots.set(path.resolve(entry.localPath), { id: entry.id, localPath: path.resolve(entry.localPath), source: 'registry' });
    }
  }

  const refsDir = resolveRefsDir(opts);
  if (!project && fs.existsSync(refsDir)) {
    for (const entry of fs.readdirSync(refsDir, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const localPath = path.join(refsDir, entry.name);
      if (fs.existsSync(path.join(localPath, '.git'))) {
        roots.set(path.resolve(localPath), { id: entry.name, localPath: path.resolve(localPath), source: 'refs' });
      }
    }
  }

  return [...roots.values()];
}

function resolveProjectRef(opts) {
  if (!opts.project) return null;
  if (opts.project !== 'current') {
    return { id: String(opts.project), name: String(opts.project), root: null };
  }

  const root = currentProjectRoot();
  const id = `project:${hashString(root).slice(0, 12)}`;
  return { id, name: path.basename(root), root };
}

function currentProjectRoot() {
  const result = runCommand('git', ['-C', process.cwd(), 'rev-parse', '--show-toplevel'], { allowFailure: true });
  if (result.ok && result.stdout.trim()) return path.resolve(result.stdout.trim());
  return process.cwd();
}

function gitConfig(cwd, key) {
  const result = runCommand('git', ['-C', cwd, 'config', '--get', key], { allowFailure: true });
  return result.ok ? result.stdout.trim() : null;
}

function parseGitRemoteFullName(remoteUrl) {
  if (!remoteUrl) return null;
  const match = String(remoteUrl).match(/github\.com[:/]([^/\s]+)\/([^/\s]+?)(?:\.git)?$/i);
  if (!match) return null;
  return `${match[1]}/${match[2]}`;
}

function readSearchContextMeta(localPath) {
  const metaPath = path.join(localPath, '.search-context-meta.json');
  if (!fs.existsSync(metaPath)) return null;
  try {
    return JSON.parse(fs.readFileSync(metaPath, 'utf8'));
  } catch {
    return null;
  }
}

function detectLicense(localPath) {
  const names = ['LICENSE', 'LICENSE.md', 'COPYING'];
  for (const name of names) {
    if (fs.existsSync(path.join(localPath, name))) return 'present';
  }
  return null;
}

function hashString(value) {
  return crypto.createHash('sha1').update(String(value)).digest('hex');
}

function resolveRunPaths(opts) {
  const cacheRoot = resolveCacheRoot(opts);
  const projectLocal = Boolean(opts['project-local']);
  const refsDir = path.resolve(
    process.cwd(),
    opts['refs-dir'] || (projectLocal ? '.refs' : path.join(cacheRoot, 'refs'))
  );
  const output = path.resolve(
    process.cwd(),
    opts.output || (projectLocal
      ? path.join('.context', 'reference-context.md')
      : path.join(cacheRoot, 'runs', createRunId(), 'reference-context.md'))
  );

  return { refsDir, output, cacheRoot, projectLocal };
}

function resolveRefsDir(opts) {
  if (opts['refs-dir']) return path.resolve(process.cwd(), opts['refs-dir']);
  if (opts['project-local']) return path.resolve(process.cwd(), '.refs');
  return path.join(resolveCacheRoot(opts), 'refs');
}

function resolveCacheRoot(opts = {}) {
  const configured = opts['cache-dir'] || process.env.GITHUB_REFERENCE_CONTEXT_CACHE_DIR || process.env.SEARCH_CONTEXT_CACHE_DIR;
  if (configured) return path.resolve(process.cwd(), configured);

  if (process.platform === 'darwin') {
    return path.join(os.homedir(), 'Library', 'Caches', 'github-reference-context');
  }
  if (process.platform === 'win32') {
    return path.join(process.env.LOCALAPPDATA || path.join(os.homedir(), 'AppData', 'Local'), 'github-reference-context');
  }
  return path.join(process.env.XDG_CACHE_HOME || path.join(os.homedir(), '.cache'), 'github-reference-context');
}

function createRunId() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, 'Z').replace(/[:]/g, '-');
}

function guardRunTargets({ refsDir, output, dryRun, opts }) {
  if (opts['allow-unignored-worktree']) return;

  const targets = [{ label: 'manifest output', path: output, directory: false }];
  if (!dryRun) targets.push({ label: 'refs dir', path: refsDir, directory: true });

  const failures = [];
  for (const target of targets) {
    const worktree = gitWorktreeForPath(target.path);
    if (!worktree) continue;
    if (isGitIgnored(worktree, target.path, target.directory)) continue;
    failures.push(`${target.label}: ${formatPathForDisplay(target.path)} inside ${formatPathForDisplay(worktree)}`);
  }

  if (failures.length === 0) return;

  throw new Error([
    'refusing to write unignored search-context files inside a git worktree.',
    ...failures.map((failure) => `- ${failure}`),
    'Use the default user cache, add .refs/ and .context/ to .gitignore, pass --project-local after ignoring them, or pass --allow-unignored-worktree.'
  ].join('\n'));
}

function gitWorktreeForPath(targetPath) {
  const start = nearestExistingPath(path.resolve(targetPath));
  if (!start) return null;

  const cwd = fs.statSync(start).isDirectory() ? start : path.dirname(start);
  const result = runCommand('git', ['-C', cwd, 'rev-parse', '--show-toplevel'], { allowFailure: true });
  if (!result.ok) return null;

  const root = path.resolve(result.stdout.trim());
  return isPathInside(root, targetPath) ? root : null;
}

function nearestExistingPath(targetPath) {
  let current = path.resolve(targetPath);
  while (!fs.existsSync(current)) {
    const parent = path.dirname(current);
    if (parent === current) return null;
    current = parent;
  }
  return current;
}

function isGitIgnored(worktreeRoot, targetPath, isDirectory) {
  const rel = toGitPath(path.relative(worktreeRoot, path.resolve(targetPath)));
  if (!rel || rel.startsWith('../')) return false;

  const candidates = isDirectory ? [ensureTrailingSlash(rel), `${trimTrailingSlash(rel)}/.search-context-placeholder`] : [rel];
  return candidates.some((candidate) => {
    const result = runCommand('git', ['-C', worktreeRoot, 'check-ignore', '--quiet', '--no-index', '--', candidate], { allowFailure: true });
    return result.status === 0;
  });
}

function isPathInside(parent, child) {
  const rel = path.relative(path.resolve(parent), path.resolve(child));
  return rel === '' || (rel && !rel.startsWith('..') && !path.isAbsolute(rel));
}

function toGitPath(value) {
  return String(value).split(path.sep).join('/');
}

function ensureTrailingSlash(value) {
  return value.endsWith('/') ? value : `${value}/`;
}

function trimTrailingSlash(value) {
  return value.replace(/\/+$/u, '');
}

function jsonOutputPath(output) {
  return /\.md$/i.test(output) ? output.replace(/\.md$/i, '.json') : `${output}.json`;
}

function formatPathForDisplay(targetPath) {
  const resolved = path.resolve(targetPath);
  const relative = path.relative(process.cwd(), resolved);
  if (relative && !relative.startsWith('..') && !path.isAbsolute(relative)) return relative;
  if (!relative) return '.';

  const home = os.homedir();
  if (home && isPathInside(home, resolved)) {
    const fromHome = path.relative(home, resolved);
    return fromHome ? path.join('~', fromHome) : '~';
  }

  return resolved;
}

function cleanGoal(raw) {
  return compactWhitespace(String(raw || '').replace(/\$search-context/g, '').trim());
}

function extractTokens(raw) {
  const tokens = String(raw || '')
    .toLowerCase()
    .replace(/\b20\d{2}\b/g, ' ')
    .match(/[a-z0-9+#.]+/gi);
  if (!tokens) return [];
  return unique(tokens
    .map((t) => t.toLowerCase())
    .filter((t) => t.length >= 3)
    .filter((t) => !STOPWORDS.has(t))
  );
}

function normalizeFresh(value) {
  if (!value || String(value).toLowerCase() === 'none') return null;
  const text = String(value).trim();
  if (!/^\d{4}-\d{2}-\d{2}$/.test(text)) {
    throw new Error(`Invalid --fresh value '${value}'. Use yyyy-mm-dd or none.`);
  }
  return text;
}

function defaultFreshDate() {
  const year = new Date().getFullYear() - 2;
  return `${year}-01-01`;
}

function dateGte(iso, yyyyMmDd) {
  return String(iso).slice(0, 10) >= yyyyMmDd;
}

function intOption(opts, key, fallback) {
  if (opts[key] === undefined) return fallback;
  const n = Number.parseInt(String(opts[key]), 10);
  if (!Number.isFinite(n) || n < 0) {
    throw new Error(`Invalid --${key}: ${opts[key]}`);
  }
  return n;
}

function parseDuration(text) {
  const match = String(text).trim().match(/^(\d+)(d|h|m)$/i);
  if (!match) {
    throw new Error(`Invalid duration '${text}'. Use values like 30d, 12h, 60m.`);
  }
  const value = Number.parseInt(match[1], 10);
  const unit = match[2].toLowerCase();
  if (unit === 'd') return value * 24 * 60 * 60 * 1000;
  if (unit === 'h') return value * 60 * 60 * 1000;
  return value * 60 * 1000;
}

function writeRepoMeta(localPath, repo, action) {
  const meta = {
    action,
    fullName: repo.fullName,
    url: repo.url,
    cloneUrl: repo.cloneUrl,
    sshUrl: repo.sshUrl,
    defaultBranch: repo.defaultBranch,
    pushedAt: repo.pushedAt,
    license: repo.license,
    updatedAt: new Date().toISOString()
  };
  fs.writeFileSync(path.join(localPath, '.search-context-meta.json'), JSON.stringify(meta, null, 2), 'utf8');
}

function sanitizeRepoName(fullName) {
  return String(fullName).replace(/[\\/]/g, '__').replace(/[^a-zA-Z0-9._-]/g, '_');
}

function quoteQualifier(value) {
  if (/^[a-zA-Z0-9_.+-]+$/.test(value)) return value;
  return `"${String(value).replace(/"/g, '\\"')}"`;
}

function shellQuote(value) {
  const s = String(value);
  if (/^[a-zA-Z0-9_./:=+@-]+$/.test(s)) return s;
  return `'${s.replace(/'/g, `'\\''`)}'`;
}

function trimSnippet(text, max = 180) {
  const clean = compactWhitespace(String(text || ''));
  if (clean.length <= max) return clean;
  return `${clean.slice(0, max - 1)}…`;
}

function inlineCode(text) {
  const clean = trimSnippet(text).replace(/`/g, "'");
  return `\`${clean}\``;
}

function compactWhitespace(text) {
  return String(text || '').replace(/\s+/g, ' ').trim();
}

function unique(values) {
  const seen = new Set();
  const out = [];
  for (const value of values) {
    const key = String(value);
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(value);
  }
  return out;
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function log(opts, message) {
  if (opts.verbose) console.log(message);
}

function toJsonSafe(value) {
  return JSON.parse(JSON.stringify(value, (_key, val) => {
    if (val instanceof Set) return [...val];
    return val;
  }));
}

main();
