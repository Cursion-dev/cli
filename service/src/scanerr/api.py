import requests, json, os, time
from dotenv import load_dotenv
from pathlib import Path
from rich import print as rprint

env_file = Path(str(Path.home()) + '/scanerr/.env')

load_dotenv(dotenv_path=env_file)

# import env vars
SCANERR_API_BASE_URL = f'{os.getenv('API_ROOT') if os.getenv('API_ROOT') is not None else 'https://api.scanerr.io'}/v1/ops'
SCANERR_API_TOKEN = f'Token {os.getenv('API_KEY')}'
headers = {
   "content-type": "application/json",
   "Authorization" : SCANERR_API_TOKEN
}




def format_response(response: dict) -> dict:

    # checking response for error
    success = True
    if not str(response.status_code).startswith('2'):
        success = False

    # retrieve response data
    json_response = response.json()

    # format response
    resp = {
        'success': success,
        'data': json_response
    }

    return resp




def check_headers(api_key:str = None):

    # check headers for API KEY
    if 'None' in headers["Authorization"] or \
        len(headers["Authorization"]) < 20:

        # check if API_KEY was passed
        if api_key is None:
            rprint(
                '[red bold]' + u'\u2718' + '[/red bold]' +
                f' please pass --api-key=<api-key>'
            )
            return None

        # updated header if api_key is present
        headers["Authorization"] = f'Token {api_key}'
        return headers

    # return unchanged headers 
    else:
        return headers




def api_add_site(*args, **kwargs):

    """ 
    This Endpoint will create a `Site` object 
    with the root url being the passed "site_url". 
    Also initiates Crawler() which creates new `Pages` 
    and new `Scans` for each new `Page`.
    """

    # get kwargs
    site_url = kwargs.get('site_url')
    page_urls = kwargs.get('page_urls')
    api_key = kwargs.get('api_key')

    # setup configs
    url = f'{SCANERR_API_BASE_URL}/site'

    data = {
        "site_url": site_url,
        "page_urls": page_urls if page_urls is not None else None
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)
        
    # send the request
    res = requests.post(
        url=url, 
        headers=headers, 
        data=json.dumps(data)
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_crawl_site(*args, **kwargs):

    """
    This Endpoint will crawl the site for any new `Pages` not 
    already recorded (Stopping once "Account.max_pages" has been reached), 
    and auto create a `Scan` for each new `Page` it records.
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    api_key = kwargs.get('api_key')

    # setup configs
    url = f'{SCANERR_API_BASE_URL}/site/{site_id}/crawl' 

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # send the request
    res = requests.post(
        url=url, 
        headers=headers, 
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_get_sites(*args, **kwargs):

    """
    This endpoint will return the `Site` object 
    associated with the passed "site_id"
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    api_key = kwargs.get('api_key')

    # setup configs
    url = f'{SCANERR_API_BASE_URL}/site'

    params = {
        "site_id": site_id,
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # send the request
    res = requests.get(
        url=url, 
        headers=headers, 
        params=params
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_delete_site(*args, **kwargs):

    """
    This endpoint will delete the `Site` object 
    associated with the passed "site_id" /site/<site_id>
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    api_key = kwargs.get('api_key')

    # setup configs
    url = f'{SCANERR_API_BASE_URL}/site/{site_id}'

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # send the request
    res = requests.delete(
        url=url, 
        headers=headers, 
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_add_page(*args, **kwargs):

    """
    This endpoint will create a new `Page` 
    object associated with the passed "site_id". 
    Also creates an initial `Scan` object for each new `Page`
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    page_url = kwargs.get('page_url')
    page_urls = kwargs.get('page_urls')
    api_key = kwargs.get('api_key')

    # setup configs
    url = f'{SCANERR_API_BASE_URL}/page'

    data = {
        "site_id": site_id,   
        "page_url": page_url if page_url is not None else None,
        "page_urls": page_urls if page_urls is not None else None, 
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # send the request
    res = requests.post(
        url=url, 
        headers=headers, 
        data=json.dumps(data)
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_get_pages(*args, **kwargs):

    """ 
    This endpoint will retrieve a list of `Page` 
    objects filtered by the passed "site_id".
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    page_id = kwargs.get('page_id')
    api_key = kwargs.get('api_key')

    # setup configs
    url = f'{SCANERR_API_BASE_URL}/page'

    params = {
        "site_id": site_id,
        "page_id": page_id, # OPTIONAL for returning a specific Page
        "lean": "true" 
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # send the request
    res = requests.get(
        url=url, 
        headers=headers, 
        params=params
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_delete_page(*args, **kwargs):

    """
    This endpoint will delete the `Page` object 
    associated with the passed "page_id" /page/<page_id>
    """

    # get kwargs
    page_id = kwargs.get('page_id')
    api_key = kwargs.get('api_key')

    # setup configs
    url = f'{SCANERR_API_BASE_URL}/page/{page_id}'

    # check headers for API KEY
    headers = check_headers(api_key=api_key)
    
    # send the request
    res = requests.delete(
        url=url, 
        headers=headers, 
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_scan_site(*args, **kwargs):

    """ 
    This endpoint will create a new `Scan` for each 
    `Page` associated with the passed "site_id".
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    api_key = kwargs.get('api_key')

    # setup configs
    url = f'{SCANERR_API_BASE_URL}/scan'

    data = {
        "site_id": site_id 
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # send the request
    res = requests.post(
        url=url, 
        headers=headers, 
        data=json.dumps(data)
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_scan_page(*args, **kwargs):

    """
    This Endpoint will create a `Scan` for 
    only the passed "page_id" 
    """

    # get kwargs
    page_id = kwargs.get('page_id')
    api_key = kwargs.get('api_key')

    # setup configs
    url = f'{SCANERR_API_BASE_URL}/scan'

    data = {
        "page_id": page_id
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # send the request
    res = requests.post(
        url=url, 
        headers=headers, 
        data=json.dumps(data)
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_get_scans(*args, **kwargs):

    """
    This Endpoint will retrieve one or more `Scans` for 
    only the passed "page_id" - recommend using "lean=true"
    """

    # get kwargs
    page_id = kwargs.get('page_id')
    scan_id = kwargs.get('scan_id')
    api_key = kwargs.get('api_key')

    # setup configs
    url = f'{SCANERR_API_BASE_URL}/scan'

    params = {
        'scan_id': scan_id,  # OPTIONAL for returning a specific Scan
        'page_id': page_id,
        'lean': 'true'
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # send the request
    res = requests.get(
        url=url, 
        headers=headers, 
        params=params
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_test_page(*args, **kwargs):

    """
    This Endpoint will create a `Test` for only the passed "page_id".
    Current version requires both the "pre_scan" and "post_scan" to be 
    passed in the API call.
    """

    # get kwargs
    page_id = kwargs.get('page_id')
    pre_scan = kwargs.get('pre_scan')
    post_scan = kwargs.get('post_scan')
    api_key = kwargs.get('api_key')

    # setup configs
    url = f'{SCANERR_API_BASE_URL}/test'

    data = {
        "page_id": page_id,
        "pre_scan": pre_scan, 
        "post_scan": post_scan,
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # send the request
    res = requests.post(
        url=url, 
        headers=headers, 
        data=json.dumps(data)
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_get_tests(*args, **kwargs):

    """
    This Endpoint will retrieve one or more `Tests` for 
    only the passed "page_id" - recommend using "lean=true"
    """

    # get kwargs
    page_id = kwargs.get('page_id')
    test_id = kwargs.get('test_id')
    api_key = kwargs.get('api_key')

    # setup configs
    url = f'{SCANERR_API_BASE_URL}/test'

    params = {
        'test_id': test_id, 
        'page_id': page_id,
        'lean': 'true'
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # send the request
    res = requests.get(
        url=url, 
        headers=headers, 
        params=params
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_get_cases(*args, **kwargs):

    """
    This Endpoint will retrieve one or more `Cases` for 
    only the passed "site_id"
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    case_id = kwargs.get('case_id')
    api_key = kwargs.get('api_key')

    # setup configs
    url = f'{SCANERR_API_BASE_URL}/case'

    params = {
        'case_id': case_id, 
        'site_id': site_id,
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # send the request
    res = requests.get(
        url=url, 
        headers=headers, 
        params=params
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_get_testcases(*args, **kwargs):

    """
    This Endpoint will retrieve one or more `Testcases` for 
    only the passed "site_id"
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    testcase_id = kwargs.get('testcase_id')
    api_key = kwargs.get('api_key')

    # setup configs
    url = f'{SCANERR_API_BASE_URL}/testcase'

    params = {
        'testcase_id': testcase_id,
        'site_id': site_id,
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # send the request
    res = requests.get(
        url=url, 
        headers=headers, 
        params=params
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def api_add_testcases(*args, **kwargs):

    """
    This Endpoint will create and run a new `Testcases` 
    for the passed "site_id" & "case_id"
    """

    # get kwargs
    site_id = kwargs.get('site_id')
    case_id = kwargs.get('case_id')
    updates = kwargs.get('updates')
    api_key = kwargs.get('api_key')

    # setup configs
    url = f'{SCANERR_API_BASE_URL}/testcase'

    data = {
        'case_id': case_id,
        'site_id': site_id,
        'updates': updates
    }

    # check headers for API KEY
    headers = check_headers(api_key=api_key)

    # send the request
    res = requests.post(
        url=url, 
        headers=headers,
        data=json.dumps(data)
    )

    # format response
    resp = format_response(res)

    # return object as dict
    return resp




def wait_for_completion(ids: list, obj: str) -> None:

    """ 
    This method waits for either a set of `Scan` or `Test` objects
    finish running - or timesout at max_wait_time (900s)
    """

    max_wait_time = 900
    wait_time = 0
    completions = []
    while (len(completions) != len(ids)) and wait_time < max_wait_time:
        # sleeping for 10 seconds
        time.sleep(10)
        wait_time += 15
        # checking status of obj
        for id in ids:
            if obj == 'scan':
                time_complete = api_get_scans(scan_id=id, page_id=None)['data']['time_completed']
            if obj == 'test':
                time_complete = api_get_tests(test_id=id, page_id=None)['data']['time_completed']
            if obj == 'testcase':
                time_complete = api_get_testcases(testcase_id=id)['data']['time_completed']
            
            # alerting completion
            if time_complete is not None and id not in completions:
                rprint('[green bold]' + u'\u2714' + '[/green bold]' + f' {obj} completed -> {id}')
                completions.append(id)

    return None




def api_test_site(
        site_id: str,
        max_wait_time: int=120,
        threshold: int=95,
        api_key: str=None
    ):
    
    """ 
    This method will run a full `Test` for the `Site`
    asocaited with the passed id's. 
    Full flow:
        1. Determine if testing full site or page
        2. Wait for `Site` to be available
        3. Get all `Pages` for associated `Site`
        4. Get all "pre_scan" id's for each `Page`
        5. Check for all "pre_scan" completion
        6. Create new "post_scans" for each `Page`
        7. Check for all "post_scan" completion
        8. Create new `Test` for each `Page`
        9. Check for all `Test` completion
    """

    # 1. get the site
    site = api_get_sites(site_id=site_id, api_key=api_key)['data']

    # 2. Check for crawl completion
    wait_time = 0
    site_status = 500
    print(f'checking site availablity...')
    while str(site_status).startswith('5') and wait_time < max_wait_time:
        # sleeping for 5 seconds
        time.sleep(5)
        wait_time += 5
        # check site status
        site_status = requests.get(url=site['site_url']).status_code
    
    # determine if timeout 
    if wait_time >= max_wait_time:
        rprint(
            '[red bold]' + u'\u2718' + '[/red bold]' + 
            ' max wait time reached - proceeding with caution...'
        )
    else:
        rprint(
            '[green bold]' + u'\u2714' + '[/green bold]' 
            + ' site is available'
        )

    # 3. Get all `Pages` for associated `Site` 
    print(f'\nretrieving pages...')
    pages = api_get_pages(site_id=str(site['id']), api_key=api_key)['data']['results']
    rprint('[green bold]' + u'\u2714' + '[/green bold]' + f' retrieved pages')

    # 4. Get all "pre_scan" id's for each `Page`
    pre_scan_ids = []
    for page in pages:
        # option 1. - get scan ids from `Page` object already in memory
        pre_scan_id = str(page['info']['latest_scan']['id'])
        pre_scan_ids.append(pre_scan_id)

    # 5. Check for all "pre_scan" completion
    print(f'\nchecking pre_scans for each page...')
    wait_for_completion(ids=pre_scan_ids, obj='scan')
    
    # 6. Create new "post_scans" for each `Page`
    print(f'\ncreating post_scans for each page...')
    post_scan_ids = api_scan_site(site_id=str(site['id']), api_key=api_key)['data']['ids']
    rprint('[green bold]' + u'\u2714' + '[/green bold]' + f' post_scans created')

    # 7. Check for all "post_scan" completion
    print(f'\nchecking post_scans for each page...')
    wait_for_completion(ids=post_scan_ids, obj='scan')

    # 8. Create new `Test` for each `Page`
    pages = api_get_pages(site_id=str(site['id']), api_key=api_key)['data']['results']
    test_ids = []
    i = 0
    for page in pages:
        # send the request
        test_id = api_test_page(
            page_id=str(page['id']),
            pre_scan=str(pre_scan_ids[i]),
            post_scan=str(page['info']['latest_scan']['id']),
            api_key=api_key
        )['data']['ids'][0]
        # record test_id
        test_ids.append(test_id)
        rprint(str(f'\ntesting page {page['page_url']}\
            \n test_id    : {test_id}\
            \n pre_scan   : {pre_scan_ids[i]}\
            \n post_scan  : {page["info"]["latest_scan"]["id"]}'
        ))
        i += 1

    # 9. Check for all `Test` completion
    print(f'\nchecking test completion for each page...')
    wait_for_completion(ids=test_ids, obj='test')

    # checking scores
    success = True
    print('\nTest results:')
    for test_id in test_ids:
        score = api_get_tests(test_id=test_id, api_key=api_key)['data']['score']
        _score = str(round(score, 2))
        if score >= threshold:
            rprint(
                ' [green bold]' + u'\u2714' + '[/green bold]' + 
                f' passed {_score}% : https://app.scanerr.io/test/{test_id}'
            )
        else:
            rprint(
                ' [red bold]' + u'\u2718' + '[/red bold]' +
                f' failed {_score}% : https://app.scanerr.io/test/{test_id}'
            )
            success = False

    # returning results
    return success




def api_testcase_site(
        site_id: str,
        case_id: str,
        max_wait_time: int=120,
        api_key: str=None,
        updates: dict=None,
    ):
    
    """ 
    This method will run a full `Testcase` for the `Site`
    asocaited with the passed id's. 
    Full flow:
        1. Determine if testing full site or page
        2. Wait for `Site` to be available
        3. Adjust steps data (from **kwargs)
        4. Initiate the `Testcase`
        5. Check for `Testcase` completion
    """

    # 1. get the site
    site = api_get_sites(site_id=site_id, api_key=api_key)['data']

    # 2. Wait for `Site` to be available
    wait_time = 0
    site_status = 500
    print(f'checking site availablity...')
    while str(site_status).startswith('5') and wait_time < max_wait_time:
        # sleeping for 5 seconds
        time.sleep(5)
        wait_time += 5
        # check site status
        site_status = requests.get(url=site['site_url']).status_code
    
    # determine if timeout 
    if wait_time >= max_wait_time:
        rprint(
            '[red bold]' + u'\u2718' + '[/red bold]' + 
            ' max wait time reached - proceeding with caution...'
        )
    else:
        rprint(
            '[green bold]' + u'\u2714' + '[/green bold]' 
            + ' site is available'
        )

    # 3. Adjust steps data (from **kwargs)
    print(f'\nadjusting step data...')
    _updates = []
    for i in updates:
        if '-' not in i or ':' not in i:
            rprint(
                '[red bold]' + u'\u2718' + '[/red bold]' + 
                ' step data formatted incorrectly (step-0:value)'
            )
            return

        # parsing data from step
        _str = str(i).split(':')
        value = _str[1]
        index = int(_str[0].split('-')[1])-1

        # adding data to updates
        _updates.append({
            'index': index,
            'value': value
        })

    # done parsing and updating
    rprint('[green bold]' + u'\u2714' + '[/green bold]' + f' step data updated')

    # 4. Create new `Testcase`
    testcase_data = api_add_testcases(
        case_id=case_id,
        site_id=site_id,
        updates=_updates
    )

    if not testcase_data['success']:
        rprint(testcase_data)
        return False
    
    # saving testcase_id
    testcase_id = testcase_data['data']['id']

    # 5. Check for `Testcase` completion
    print(f'\nwaiting for Testcase completion...')
    wait_for_completion(ids=[testcase_id], obj='testcase')
    testcase = api_get_testcases(testcase_id=testcase_id, api_key=api_key)['data']
    passed = testcase['passed']

    failed = []
    i = 1
    # getting failed steps;
    for step in testcase['steps']:
        if not step['action']['passed']:
            failed.append(f'Step #{i}')
        i += 1

    # displaying results
    print('\nTestcase results:')
    if passed:
        rprint(
            '[green bold]' + u'\u2714' + '[/green bold]' + 
            f' Passed : https://app.scanerr.io/testcase/{testcase_id}' 
        )
    else:
        rprint(
            f'{"\n[red bold]" + u"\u2718" + "[/red bold]"}' + 
            f' Failed : https://app.scanerr.io/testcase/{testcase_id}' + 
            f'\n failed steps : {[n for n in failed]}'
        )

    # returning results
    return passed










