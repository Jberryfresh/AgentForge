// Simple Node loader for agent/config.json
// Usage:
//   node agent/loadConfig.js --check
//   const { loadConfig, loadSystemPrompt } = require('./agent/loadConfig');
//   const cfg = loadConfig(); const prompt = loadSystemPrompt(cfg);

const fs = require('fs');
const path = require('path');

class ConfigError extends Error {}

function assertCond(cond, msg) {
  if (!cond) throw new ConfigError(msg);
}

function loadConfig(configPath = 'agent/config.json', baseDir = process.cwd()) {
  const cfgAbs = path.isAbsolute(configPath) ? configPath : path.join(baseDir, configPath);
  let raw;
  try {
    raw = fs.readFileSync(cfgAbs, 'utf8');
  } catch (e) {
    throw new ConfigError(`Config file not found: ${cfgAbs}`);
  }
  let data;
  try {
    data = JSON.parse(raw);
  } catch (e) {
    throw new ConfigError(`Invalid JSON in ${cfgAbs}: ${e.message}`);
  }

  assertCond(typeof data.model === 'string' && data.model.trim(), "'model' must be a non-empty string");
  assertCond(typeof data.temperature === 'number', "'temperature' must be a number");
  assertCond(typeof data.top_p === 'number', "'top_p' must be a number");
  assertCond(typeof data.system_prompt_path === 'string' && data.system_prompt_path.trim(), "'system_prompt_path' must be a non-empty string path");

  const temp = Number(data.temperature);
  const topP = Number(data.top_p);
  assertCond(temp >= 0 && temp <= 2, "'temperature' must be between 0.0 and 2.0");
  assertCond(topP > 0 && topP <= 1, "'top_p' must be in (0.0, 1.0]");

  const promptAbs = path.isAbsolute(data.system_prompt_path)
    ? data.system_prompt_path
    : path.join(baseDir, data.system_prompt_path);
  try {
    fs.accessSync(promptAbs, fs.constants.R_OK);
  } catch {
    throw new ConfigError(`system_prompt_path not found: ${promptAbs}`);
  }

  return { ...data, _resolved_system_prompt_path: promptAbs };
}

function loadSystemPrompt(cfg) {
  const p = cfg._resolved_system_prompt_path || cfg.system_prompt_path;
  try {
    return fs.readFileSync(p, 'utf8').trim();
  } catch (e) {
    throw new ConfigError(`Failed to read system prompt from ${p}: ${e.message}`);
  }
}

module.exports = { loadConfig, loadSystemPrompt, ConfigError };

if (require.main === module) {
  const argCheck = process.argv.includes('--check');
  const argPrint = process.argv.includes('--print');
  try {
    const cfg = loadConfig();
    if (argPrint) {
      const prompt = loadSystemPrompt(cfg);
      const preview = (prompt.length > 120 ? prompt.slice(0, 120) + '…' : prompt).replace(/\n/g, ' ');
      console.log(JSON.stringify({
        model: cfg.model,
        temperature: cfg.temperature,
        top_p: cfg.top_p,
        system_prompt_path: cfg._resolved_system_prompt_path,
        prompt_preview: preview,
      }, null, 2));
    } else if (argCheck) {
      console.log('OK: agent/config.json and system prompt look good.');
    } else {
      console.log('Config loads successfully. Use --check or --print for details.');
    }
    process.exit(0);
  } catch (e) {
    console.error(`ERROR: ${e.message}`);
    process.exit(1);
  }
}

