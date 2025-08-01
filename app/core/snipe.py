import requests
from urllib.parse import urljoin
from requests.exceptions import RequestException, InvalidURL
from app.core.payloads import PAYLOADS
from app.core.detector import is_valid_url
import concurrent.futures
import re

def snipe_mode(urls, log_callback=print, max_workers=5):
    results = []
    summary = []

    log_callback(f"▶ Running snipe scan on {len(urls)} URLs with enhanced heuristics...")

    redirect_pattern = re.compile(
        r'(https?:\/\/|\/\/)[\w\.-]*', re.IGNORECASE
    )

    suspicious_domains = ['evil.com', 'malicious.net', 'badredirect.org']

    def scan_url_payload(url, payload):
        try:
            full_url = urljoin(url, payload)
            if not is_valid_url(full_url):
                log_callback(f"🛑 Skipped invalid URL: {full_url}")
                return None

            log_callback(f"🔍 Payload: {payload}")
            resp = requests.get(full_url, allow_redirects=False, timeout=5)
            loc = resp.headers.get('location', '')

            if loc:
                if redirect_pattern.search(loc) or any(dom in loc for dom in suspicious_domains):
                    log_callback(f"🎯 Confirmed vuln via header redirect: {loc}")
                    results.append((url, payload, loc))

            refresh = resp.headers.get('Refresh', '')
            if refresh and redirect_pattern.search(refresh):
                log_callback(f"🎯 Confirmed vuln via Refresh header: {refresh}")
                results.append((url, payload, refresh))

            if resp.text:
                meta_refresh = re.search(r'<meta\s+http-equiv=["\']refresh["\']\s+content=["\']\d+;\s*url=([^"\']+)["\']', resp.text, re.IGNORECASE)
                if meta_refresh:
                    meta_url = meta_refresh.group(1)
                    if redirect_pattern.search(meta_url) or any(dom in meta_url for dom in suspicious_domains):
                        log_callback(f"🎯 Confirmed vuln via meta refresh: {meta_url}")
                        results.append((url, payload, meta_url))

                # basic JS redirect pattern (very naive)
                js_redirect = re.search(r'window\.location\s*=\s*[\'"]([^\'"]+)[\'"]', resp.text, re.IGNORECASE)
                if js_redirect:
                    js_url = js_redirect.group(1)
                    if redirect_pattern.search(js_url) or any(dom in js_url for dom in suspicious_domains):
                        log_callback(f"🎯 Confirmed vuln via JS redirect: {js_url}")
                        results.append((url, payload, js_url))

        except InvalidURL as e:
            log_callback(f"🛑 Invalid URL {payload}: {e}")
        except RequestException as e:
            log_callback(f"⚠️ Network error on {payload}: {e}")
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for url in urls:
            for payload in PAYLOADS:
                futures.append(executor.submit(scan_url_payload, url, payload))
        concurrent.futures.wait(futures)

    if results:
        for url, payload, loc in results:
            summary.append(f"🚨 Confirmed vuln on {url} with `{payload}` redirecting to {loc}")
    else:
        summary.append("💤 No vulns found in Snipe mode.")

    return results, "\n".join(summary)
