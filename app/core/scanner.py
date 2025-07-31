# app/core/scanner.py
import requests
from urllib.parse import urljoin, urlparse
from requests.exceptions import InvalidURL, RequestException
from app.core.payloads import PAYLOADS

def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return bool(parsed.scheme and parsed.netloc)
    except:
        return False

def is_redirecting(url, payload):
    try:
        full_url = urljoin(url, payload)
        if not is_valid_url(full_url):
            return False
        resp = requests.get(full_url, allow_redirects=False, timeout=5)
        return resp.status_code in [301, 302, 303, 307, 308] and 'location' in resp.headers
    except (InvalidURL, RequestException):
        return False

def storm_mode(urls, log_callback=print):
    results = []
    for url in urls:
        log_callback(f"\n🌩 Scanning {url}...")

        for payload in PAYLOADS:
            try:
                full_url = urljoin(url, payload)

                if not is_valid_url(full_url):
                    log_callback(f"🛑 Skipped invalid URL: {full_url}")
                    continue

                resp = requests.get(full_url, allow_redirects=False, timeout=5)
                status = resp.status_code
                location = resp.headers.get('location', '')

                log_callback(f"↪️  Tried {payload} → Status: {status} | Location: {location}")

                if status in [301, 302, 303, 307, 308] and 'location' in resp.headers:
                    log_callback(f"⚠️  Potential vuln: {url} with payload `{payload}`")
                    results.append((url, payload))
                    break  # one vuln per host is enough
            except InvalidURL as e:
                log_callback(f"🛑 Invalid URL: {payload} → {e}")
                continue
            except RequestException as e:
                log_callback(f"❌ Network error trying {payload} → {e}")
                continue

    return results


def snipe_mode(urls, log_callback=print):
    results = []
    for url in urls:
        log_callback(f"[snipe] 🎯 Probing: {url}")
        for payload in PAYLOADS:
            try:
                full_url = urljoin(url, payload)

                if not is_valid_url(full_url):
                    log_callback(f"    🛑 Skipped invalid URL: {full_url}")
                    continue

                log_callback(f"  🔍 Payload: {payload}")
                resp = requests.get(full_url, allow_redirects=False, timeout=5)
                loc = resp.headers.get('location', '')
                if loc and any(ev in loc for ev in ['evil.com', 'http', '//']):
                    log_callback(f"    🎯 Found vuln: {loc}")
                    results.append((url, payload, loc))
            except InvalidURL as e:
                log_callback(f"    🛑 Invalid URL: {payload} → {e}")
                continue
            except RequestException as e:
                log_callback(f"    ⚠️ Network error: {e}")
                continue
    return results
