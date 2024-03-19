import typer, os, json, time, shutil
from pathlib import Path
from dotenv import load_dotenv
from pprint import pprint
from rich import print as rprint
from .api import *


# High Level Configs

app = typer.Typer()
env_file = Path(str(Path.home()) + '/scanerr/.env')

load_dotenv(dotenv_path=env_file)

API_KEY = f'Token {os.getenv('API_KEY')}'
API_ROOT = f'{os.getenv('API_ROOT') if os.getenv('API_ROOT') is not None else 'https://api.scanerr.io'}'






@app.command()
def config(api_key: str, api_root: str='https://api.scanerr.io') -> None:

    """ 
    Setup and configure the Scanerr CLI for initial use 
    """

    # deleting .env if exists
    if env_file.exists():
        shutil.rmtree(env_file)
    
    # creating new .env file
    os.mkdir(Path(f'{Path.home()}/scanerr'))

    # adding new configs tp .env
    with open(env_file, "w") as f:
        f.write(f'API_KEY={api_key}\n')
        f.write(f'API_ROOT={api_root}\n')
    
    # print response
    rprint(
        '[green bold]' +
        u'\u2714' +
        '[/green bold]'+
        f" Configs have been updated"
    )
    return None



def check_key_and_root():
    success = True
    if len(os.getenv('API_KEY')) <= 0:
        success = False
        rprint(
            '[red bold]' +
            u'\u2718' +
            '[/red bold]' +
            ' api_key exists'
        )
    else:
        rprint(
            '[green bold]' +
            u'\u2714' +
            '[/green bold]' +
            ' api_key exists'
        )

    if len(os.getenv('API_ROOT')) <= 0:
        success = False
        rprint(
            '[red bold]' +
            u'\u2718' +
            '[/red bold]' +
            ' api_root exists'
        )
    else:
        rprint(
            '[green bold]' +
            u'\u2714' +
            '[/green bold]' +
            ' api_root exists'
        )
    
    return success




@app.command()
def check():
    
    """ 
    Check that Scanerr CLI is properly configured
    """

    # completing checks
    success = True
    if not env_file.exists():
        success = False
        rprint(
            '\n[red bold]' + 
            u'\u2718' + 
            '[/red bold]' + 
            ' .env exists'
        )
        
    else:
        rprint(
            '\n[green bold]' +
            u'\u2714' +
            '[/green bold]' +
            ' .env exists'
        )
        success = check_key_and_root()

    
    if success:
        rprint(
            '\n[green bold]' +
            u'\u2714' +
            '[/green bold]'+
            f" All checks passed - Scanerr is confgured correctly\n"
        )
        rprint(f" API_KEY  : Token •••••••••••••••••••••••••••")
        rprint(f" API_ROOT : {API_ROOT}\n\n")

    if not success:
        rprint(
            '\n[red bold]' +
            u'\u2718' +
            '[/red bold]'+ 
            f" Some Checks Failed!"
        )
        rprint(
            'To fix, please run: \n' +
            ' scanerr config <api_key>'+ 
            ' --api-root=<private_api_root>\n'
        )




def print_formated_response(response: dict, verbose: bool=True) -> None: 

    """ 
    Generic formatter for any api response 
    """

    if response['success']:
        rprint('[green bold]' + u'\u2714' + '[/green bold] Success')
    if not response['success']:
        rprint('[red bold]' + u'\u2718' + '[/red bold] Failed')
    if verbose:
        rprint(response['data'])




@app.command()
def add_site(site_url: str, v: bool=True, api_key: str=None):

    """ 
    Add a `Site` object to your Scanerr account
    """

    # sending request
    resp = api_add_site(
        site_url=site_url, 
        page_urls=None,
        api_key=api_key,
    )

    # printing output
    print_formated_response(
        response=resp,
        verbose=v
    )


    

@app.command()
def get_sites(site_id: str=None, v: bool=True, api_key: str=None):

    """ 
    Get one or more `Site` objects associated
    with your account
    """

    # sending request
    resp = api_get_sites(
        site_id=site_id,
        api_key=api_key, 
    )

    # printing output
    print_formated_response(
        response=resp,
        verbose=v
    )




@app.command()
def crawl_site(site_id: str, v: bool=True, api_key: str=None):

    """ 
    Crawl a specific `Site` for new `Page` objects
    """

    # sending request
    resp = api_crawl_site(
        site_id=site_id,
        api_key=api_key, 
    )

    # printing output
    print_formated_response(
        response=resp,
        verbose=v
    )




@app.command()
def delete_site(site_id: str, v: bool=True, api_key: str=None):

    """ 
    Delete a specific `Site` object 
    """

    # sending request
    resp = api_delete_site(
        site_id=site_id, 
        api_key=api_key,
    )

    # printing output
    print_formated_response(
        response=resp,
        verbose=v
    )




@app.command()
def add_page(site_id: str, page_url: str, v: bool=True, api_key: str=None):

    """ 
    Add a new `Page` object to a specific `Site` object
    """

    # sending request
    resp = api_add_page(
        site_id=site_id, 
        page_url=page_url,
        api_key=api_key,
    )

    # printing output
    print_formated_response(
        response=resp,
        verbose=v
    )




@app.command()
def get_pages(page_id: str=None, site_id: str=None, v: bool=True, api_key: str=None):

    """ 
    Get one or more `Page` objects associated
    with a specific `Site`
    """

    # sending request
    resp = api_get_pages(
        page_id=page_id, 
        site_id=site_id, 
        api_key=api_key,
    )

    # printing output
    print_formated_response(
        response=resp,
        verbose=v
    )




@app.command()
def delete_page(page_id: str, v: bool=True, api_key: str=None):

    """ 
    Delete a specific `Page` object 
    """

    # sending request
    resp = api_delete_page(
        page_id=page_id,
        api_key=api_key, 
    )

    # printing output
    print_formated_response(
        response=resp,
        verbose=v
    )




@app.command()
def scan_site(site_id: str, v: bool=True, api_key: str=None):

    """ 
    Create new `Scan` objects for each `Page` associated
    with a specific `Site`
    """

    # sending request
    resp = api_scan_site(
        site_id=site_id, 
        api_key=api_key,
    )

    # printing output
    print_formated_response(
        response=resp,
        verbose=v
    )




@app.command()
def scan_page(page_id: str, v: bool=True, api_key: str=None):

    """ 
    Create a new `Scan` object for a specific `Page`
    """

    # sending request
    resp = api_scan_page(
        page_id=page_id, 
        api_key=api_key,
    )

    # printing output
    print_formated_response(
        response=resp,
        verbose=v
    )




@app.command()
def get_scans(scan_id: str=None, page_id: str=None, v: bool=True, api_key: str=None):

    """ 
    Get one or more `Scan` objects associated
    with a specific `Page`
    """

    # sending request
    resp = api_get_scans(
        scan_id=scan_id, 
        page_id=page_id, 
        api_key=api_key,
    )

    # printing output
    print_formated_response(
        response=resp,
        verbose=v
    )




@app.command()
def test_page(page_id: str, pre_scan_id: str, post_scan_id: str, v: bool=True, api_key: str=None):

    """ 
    Create a new `Test` for a specific `Page`
    """

    # sending request
    resp = api_test_page(
        page_id=page_id, 
        pre_scan=pre_scan_id, 
        post_scan=post_scan_id, 
        api_key=api_key,
    )

    # printing output
    print_formated_response(
        response=resp,
        verbose=v
    )




@app.command()
def get_tests(page_id: str=None, test_id: str=None, v: bool=True, api_key: str=None):

    """ 
    Get one or more `Test` objects associated
    with a specific `Page`
    """

    # sending request
    resp = api_get_tests(
        page_id=page_id, 
        test_id=test_id,
        api_key=api_key,
    )

    # printing output
    print_formated_response(
        response=resp,
        verbose=v
    )




@app.command()
def test_site(
        site_id: str, 
        max_wait_time :int=120,
        min_score: int=90,
        api_key: str=None
    ):

    """ 
    Run a full `Test` of all the `Page` objects associated
    with a specific `Site`
    """

    # sending request
    resp = api_test_site(
        site_id=site_id, 
        max_wait_time=max_wait_time,
        min_score=min_score,
        api_key=api_key,
    )

    if not resp:
        raise Exception('- Scanerr Tests Failed -')




## --- CLI entry point --- ##
def root():
    app()