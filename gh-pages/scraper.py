from urllib2 import Request, urlopen, URLError
import urllib


names = ['Puma concolor', 'Mammalia']

for name in names:
    encoded_name = urllib.quote_plus(name)
    print(encoded_name)
    request = Request("http://api.speciesplus.net/api/v1/taxon_concepts?name="+encoded_name)
    request.add_header('X-Authentication-Token', 'WYjddmVCPlzeonLKsf39rwtt')
    try:
        response = urlopen(request)
        json = response.read()
        print(json)
        print("\n")
    except URLError, e:
        print('Got an error code:', e)

