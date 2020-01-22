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
    with open('url.txt') as url_file:
        for url in url_file:
            futures.append(session.get(url[:-1]))

    done = 0
    success = 0
    failure = 0
    with open('success.txt', 'a') as success_file:
        with open('failure.txt', 'a') as failure_file:
            with open('done.txt', 'a') as done_file:
                for future in as_completed(futures):
                    resp = future.result()
                    done_file.write("{}\n".format(resp.url))

                    if resp.status_code == 200:
                        success_file.write('{"url": ' +resp.url+ ', "text": ' +resp.text+ '}\n')
                        success += 1
                    else:
                        failure_file.write("{}\n".format(resp.url))
                        failure += 1

                    done += 1
                    print("Done: {}/{}, Success: {}, Failure: {}".format(done, len(futures), success, failure))
