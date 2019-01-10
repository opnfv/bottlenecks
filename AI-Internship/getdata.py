import logging
import json
import os
import requests

from urllib2 import Request, urlopen, URLError

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)
   
test_results = None
scenario_results = None
  
#url = ('http://testresults.opnfv.org/test/api/v1/results?project=bottlenecks&case_name=posca_moon_resources')
#url = ('http://testresults.opnfv.org/test/api/v1/results?project=functest&case_name=yardstick-tc005')
#url = ('http://testresults.opnfv.org/test/api/v1/results?project=yardstick&case_name=smoke')
url=('http://testresults.opnfv.org/test/api/v1/results?project=functest&case_name=barometercollectd')


try:
	request = Request(url)
	response = urlopen(request)
        k = response.read()
        results = json.loads(k)
        test_results = results['results']
        try:
            page = results['pagination']['total_pages']
            if page > 1:
                test_results = []
                for i in range(1, page + 1):
                    url_page = url + "&page=" + str(i)
                    request = Request(url_page)
                    response = urlopen(request)
                    k = response.read()
                    results = json.loads(k)
                    test_results += results['results']
		    #print(test_results)
		writeToJSONFile('./','file-name',test_results)
		    
		    
        except KeyError:
            print "No pagination detected"
except URLError as err:
        print 'Got an error code: {}'.format(err)
