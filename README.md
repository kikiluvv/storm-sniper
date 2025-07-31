# 🌪️ StormSniper - Open Redirect Hunter 🎯
*a2h*

**StormSniper** is a Python tool built to fuzz for open redirect vulnerabilities.

Whether you want to storm URLs in bulk or snipe precise targets, this app’s got your back.

---

## Features
- **Singlular or Bulk Processing**: Scan URLs one by one, or dump a whole list to query.
- **Storm Mode:** Bulk fuzzing to uncover hidden redirect weaknesses.  
- **Snipe Mode:** Laser-focused scanning for confirming and detailing vulnerabilities.  
- **Log Saving:** Capture your hunt’s story with session logs, dump them anytime, or get prompted on exit.  
- **URL Loader:** Load your quarry of queries from `.txt` files.  
- **Shitty UI:** UI not updated yet lol...

---

## Getting Started

### Requirements

- Python 3.8+  
- PyQt5  
- Additional libs: aiohttp, tqdm, etc. (see `requirements.txt`)

```bash
pip install -r requirements.txt
```

### Running the App
```bash
python -m app.main
```

### How to Use
**1. Save Logs (Optional):**

Toggle `💾 Enable Log Saving` to capture session logs. You can dump logs manually, but you will be prompted to save if you close the app without dumping.

**2. Select Mode:**

Pick Storm to flood test a list of URLs, or Snipe to confirm vulnerabilities in a targeted batch.

**3. Load URLs:**

Manually paste URLs, one per line, or load from a .txt file.

**4. Run Scan:**

Hit 🚀 Run Scan and watch your hunt unfold.
If Storm mode finds potential targets, 🎯 Snipe Vulnerable URLs will activate.

---

## Final note
This app was made for educational and testing purposes. Please do not use StormSniper on sources without explicit permission.

---

## TODO:

- Refactor for modularity according to structure plan outlined above in this readme
- Decouple logic for CLI use
- Custom payloads
- Cleanup UI
- Add support for md, json, etc, in bulk processing

---

## IDEAS:
### UX & Workflow Enhancements
- **Dark Mode Toggle:** 
    - who tf uses light mode
- **Session History:** 
    - auto-save past hunts, reload them like saved games.
- **Project Management:** 
    - organize scans under named sessions — storm logs, snipe logs, payloads, all bundled.

### New Scan Modes
- **Cloaked Mode:**
    - rotate headers, user agents, or mimic search engine bots to dodge WAFs.
- **Passive Recon:**
    - scan without firing — just analyze parameters, domains, redirects, and structure.
- **Smart Storm:** 
    - prioritize suspicious URLs by entropy, token count, or redirect history.

### Payload + Heuristics Enhancements
- **Payload Builder:**
    - GUI to combine base + injection parts (e.g. origin + callback) on the fly.
- **Heuristic Filters:** 
    - flag only redirects that lead out of domain, or use open redirect patterns (//, %2f, @, etc).
- **Machine-Learned Payload Ranking:** 
    - score redirects based on past known vuln patterns.

### Utilities
- **Param Miner:** 
    - auto-extract parameters from URLs (?next=, redirect=, continue=, etc).
- **Redirect Chain Viewer:** 
    - show multi-hop redirects like a tree or breadcrumb trail.
- **Stats Overlay:** 
    - count tested URLs, matches, redirects, domains hit, etc.

### Advanced Config
- **Custom Wordlists:**
    - allow import of custom payload lists or parameter wordlists.
- **Rate Control:** 
    - slider to control request concurrency (save yourself from bans).
- **Cookie & Header Injection:** 
    - auth headers, tokens, and cookies to simulate logged-in states.

### Output / Reporting
- **Markdown Report Export:** 
    - generate vuln reports in pretty Markdown, including which payloads triggered.
- **CSV / JSON Exports:** 
    - for feeding into other tools or spreadsheets.
- **Screenshot on Hit (Headless Browser):** 
    - optional puppeteer pass to screenshot final redirect.

### Integration Dreams
- **Burp Proxy Mode:** 
    - forward all outgoing traffic through a Burp listener.
- **Shodan/Dork Scanner:** 
    - auto-pull open redirect-prone domains via Google Dorks or Shodan API.
- **Nuclei Template Export:** 
    - convert confirmed vulns into .yaml Nuclei templates.

### optional chaos sauce:

- **Hider Mode:** 
    - obfuscate payloads using unicode homoglyphs or split path injection.
- **Discord Webhook Alerts:** 
    - notify you instantly when a vuln triggers.
- **"Lucky Shot" Button:** 
    - fire a single payload to all URLs just to see if the gods are watching.
