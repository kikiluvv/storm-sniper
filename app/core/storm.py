import requests
from urllib.parse import urljoin
from requests.exceptions import RequestException, InvalidURL
from app.core.payloads import PAYLOADS
from app.core.detector import is_valid_url
from app.workers.helpers import mutate_payload, follow_redirects
import concurrent.futures

def storm_mode(urls, log_callback=print, max_workers=10):
    results = []
    summary = []

    log_callback(f"▶ Running storm scan on {len(urls)} URLs with payload mutations and multi-methods...")

    http_methods = ['GET', 'POST', 'HEAD']

    def scan_url_payload(url, payload):
        try:
            mutated_payload = mutate_payload(payload)
            full_url = urljoin(url, mutated_payload)
            if not is_valid_url(full_url):
                log_callback(f"🛑 Skipped invalid URL: {full_url}")
                return None

            for method in http_methods:
                if method == 'GET':
                    resp = requests.get(full_url, allow_redirects=False, timeout=5)
                elif method == 'POST':
                    resp = requests.post(full_url, data={}, allow_redirects=False, timeout=5)
                elif method == 'HEAD':
                    resp = requests.head(full_url, allow_redirects=False, timeout=5)

                status = resp.status_code
                location = resp.headers.get('location', '')

                log_callback(f"↪ [{method}] Tried {mutated_payload} → Status: {status} | Location: {location}")

                if status in [301,302,303,307,308] and location:
                    final_url, final_status, final_headers, _ = follow_redirects(urljoin(url, location), max_redirects=2)
                    log_callback(f"🔄 Followed redirect chain to: {final_url} (Status: {final_status})")

                    if final_status in [301,302,303,307,308]:
                        final_location = final_headers.get('location', '')
                        if final_location:
                            log_callback(f"⚠️ Redirect chain points to: {final_location}")

                    results.append((url, mutated_payload, method, status, location))

        except InvalidURL as e:
            log_callback(f"🛑 Invalid URL {payload}: {e}")
        except RequestException as e:
            log_callback(f"❌ Network error on {payload}: {e}")
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for url in urls:
            for payload in PAYLOADS:
                futures.append(executor.submit(scan_url_payload, url, payload))
        concurrent.futures.wait(futures)

    if results:
        for (url, payload, method, status, location) in results:
            summary.append(f"🚨 Potential vuln on {url} [{method}] with `{payload}` (Status: {status} Location: {location})")
        summary.append("💡 Run Snipe mode for deeper confirmation.")
    else:
        summary.append("💤 No vulns found in Storm mode.")

    return results, "\n".join(summary)


