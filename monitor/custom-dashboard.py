##############################################################################
# Copyright (c) 2018 Huawei Tech and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import json

def customize_query(filename, rowtitle, panelname, expr):
    with open(filename, 'r+') as f:
        data = json.load(f)
        x = data['rows'] #this is an array of rows of the dashboard
        for y in x:
            if y['title'] == rowtitle:
                pan = y['panels']
                for i in range(len(pan)-1) :
                    z = pan[i]
                    if z['title'] == panelname:
                        tar = z['targets']
                        for a in tar:
                            a['expr'] = expr
                            f.seek(0)       # <--- reset file position to start
                            json.dump(data, f, indent=4)
                            f.truncate()

customize_query("/home/opnfv/bottlenecks/monitor/custom-query-dashboard.json",
    "Dashboard Row", "Memory Usage per Container", "Sample Prometheus Query")

