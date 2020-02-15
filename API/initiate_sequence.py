import urllib.request as request
import validators
from first_phase_filtration import do_extrinsic_filtration
from second_phase_filtration import do_intrinsic_filtration

'''
    The following method is the entry point to the API.
'''
def start_summarization(domain, cue_words):
    pass

'''
    The following method fetches data from wikipedia and
    cleans the raw data.
'''
def fetch_data_from_url(url):
    if not validators.url(url):
        raise Exception('Input URL is malformed.')
    
    content = request.urlopen(url)
    
#    driver.get(url)
    
    # This filtration is fine
    main_content_node = do_extrinsic_filtration(content, url)
    
    # This filtration causes issues
    cleaned_dom_structure = do_intrinsic_filtration(main_content_node, url)
    
    # Write any html data gathering code above it.
#    driver.close()
    
    return cleaned_dom_structure

cleaned_soup = fetch_data_from_url('https://en.wikipedia.org/wiki/Isaac_Newton')

#with open('final_doc.txt', 'w') as file:
#    file.write(cleaned_soup.text)