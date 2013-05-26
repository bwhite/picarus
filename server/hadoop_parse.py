import requests
from lxml import etree
import pyquery


def parse_counters(pq):
    a = [x for x in pq('td') if x.text and x.text.strip() == 'File System Counters'][0].getparent().getparent()
    out = {}
    group_out = None
    group = None
    for row in a.getchildren():
        children = row.getchildren()
        if any(x.tag != 'td' for x in children):
            continue
        if len(children) == 5:
            if group_out is not None:
                out[group] = group_out
            group_out = {}
            group = children[0].text.strip()
            children = children[1:]
        elif len(children) != 4:
            continue
        children = [x.text for x in children]
        group_out[children[0]] = [int(x.replace(',', '')) for x in children[1:]]
    if group_out is not None:
        out[group] = group_out
    return out


def parse_config(pq):
    out = {}
    for row in list(pq('table.datatable').children()[1]):
        out[row[0][0].text] = row[1].text
    return out


def parse_jobs(server):
    tree = etree.HTML(requests.get(server + '/jobtracker.jsp').content)
    pq = pyquery.PyQuery(tree)
    type_jobs = {}
    for status_type in ('running', 'completed'):
        jobs = set()
        try:
            table = pq('h2#%s_jobs' % status_type).next()[0]
            for row in list(list(table)[1]):
                jobid = list(list(row)[0])[0].text
                job_row = list(row)[3].text
                jobs.add((jobid, job_row))
        except IndexError:
            pass
        type_jobs[status_type] = jobs
    return type_jobs


def fetch_counters(server, jobid):
    a = requests.get(server + '/jobdetails.jsp?jobid=' + jobid).content
    tree = etree.HTML(a)
    pq = pyquery.PyQuery(tree)
    try:
        return parse_counters(pq)
    except:
        pass


def fetch_config(server, jobid):
    tree = etree.HTML(requests.get(server + '/jobconf.jsp?jobid=' + jobid).content)
    pq = pyquery.PyQuery(tree)
    try:
        return parse_config(pq)
    except:
        pass


def scrape_hadoop_jobs(server, completed_jobs=None):
    out = {}
    completed_jobs = set(completed_jobs) if completed_jobs is not None else set()
    for status, jobids in parse_jobs(server).items():
        for jobid, row in set(jobids):
            try:
                columns = {'status': status}
                #config = fetch_config(server, jobid)
                #row = str(config['picarus.job.row'])
                if row in completed_jobs:
                    continue
                try:
                    status_counters = fetch_counters(server, jobid)['STATUS']
                except KeyError:
                    pass
                for x in ['goodRows', 'badRows']:
                    try:
                        columns[x] = str(status_counters[x][2])
                    except KeyError:
                        pass
                out[row] = columns
            except:
                pass
    return out


def main():
    server = 'http://localhost:50030'
    print(scrape_hadoop_jobs(server))

if __name__ == '__main__':
    main()
