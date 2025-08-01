from urllib.parse import urljoin
import requests
import random

def mutate_payload(payload):
    mutations = [
        lambda p: p.replace("http://", "hxxp://"),
        lambda p: p.replace("/", "//"),
        lambda p: p + "%00",
        lambda p: p + "%2e",
        lambda p: p + "?",
        lambda p: p[::-1],
    ]
    mutation = random.choice(mutations)
    return mutation(payload)

def follow_redirects(url, max_redirects=3, timeout=5):
    try:
        for _ in range(max_redirects):
            resp = requests.get(url, allow_redirects=False, timeout=timeout)
            if resp.status_code in [301, 302, 303, 307, 308]:
                loc = resp.headers.get('location')
                if not loc:
                    break
                url = urljoin(url, loc)
            else:
                break
        return url, resp.status_code, resp.headers, resp.text
    except Exception:
        return url, None, {}, ""
