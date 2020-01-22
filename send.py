from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

responses = {}

def response_hook(resp, *args, **kwargs):
    if resp.status_code not in responses:
        responses[resp.status_code] = [resp.url]
    else:
        responses[resp.status_code].append([resp.url])

hooks = { 'response' : response_hook }
with FuturesSession(max_workers=1000) as session:
    futures = []
    for i in range(100):
        url = 'https://www.yahoo.com'
        futures.append(session.get(url, hooks=hooks))

    done = 0
    with open('output.txt', 'w') as f:
        for future in as_completed(futures):
            resp = future.result()
            f.write(resp.url + '\n')
            done += 1
            print(done)
