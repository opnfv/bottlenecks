import json
from pprint import pprint


with open('test-dash.json', 'r+') as f:
    data = json.load(f)
    x = data['rows'] #this is an array
    for y in x:
        #print y['title']
        if y['title'] == "Dashboard Row":
            pan = y['panels']
            #for z in pan:
            for i in range(len(pan)-1) :
                z = pan[i]
                print z['id']
                if z['id'] == 31:
                    print z['id']
                    tar = z['targets']
                    for a in tar:
                        pprint(a['expr'])
                        print a['expr']
                        a['expr'] = "gfhgbj"
                        f.seek(0)        # <--- should reset file position to the beginning.
                        json.dump(data, f, indent=4)
                        f.truncate()


def main_f(filename, rowtitle, panelid, expr):
    with open(filename, 'r+') as f:
        data = json.load(f)
        x = data['rows'] #this is an array
        for y in x:
        #print y['title']
            if y['title'] == rowtitle:
                pan = y['panels']
            #for z in pan:
                for i in range(len(pan)-1) :
                    z = pan[i]
                    print z['id']
                    if z['id'] == panelid:
                        print z['id']
                        tar = z['targets']
                        for a in tar:
                            pprint(a['expr'])
                            print a['expr']
                            a['expr'] = expr
                            f.seek(0)        # <--- should reset file position to the beginning.
                            json.dump(data, f, indent=4)
                            f.truncate()


main_f("test-dash.json", "Dashboard Row", 31, "sdffdf")

