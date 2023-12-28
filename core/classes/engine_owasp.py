import collections
import json
import os
import re
import subprocess
import uuid

import weasyprint
from bs4 import BeautifulSoup
from decouple import config

from core.classes.tools import Tools, ToolsS3
from scan.models import ScanReports

obj_tools = Tools()
obj_tools_s3 = ToolsS3()


class EngineOWASP:
    def __init__(self):
        pass

    def scan(self, client_id, url, expires=300):
        temp_file = uuid.uuid4().hex
        local_dir_tmp = '/tmp/report/'

        process_scan = subprocess.Popen(
            [
                'script/owasp/processor', temp_file, url
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        scan = obj_tools.logodata()

        while True:
            return_code = process_scan.poll()
            if return_code is not None:
                f = open(local_dir_tmp+temp_file, "r")
                soup = BeautifulSoup(f.read(), features="html.parser")
                for img in soup.findAll('img'):
                    img['src'] = str(scan)

                with open(local_dir_tmp+temp_file+".html", "w", encoding='utf-8') as file:
                    html_out = re.sub("ZAP Scanning Report", config('REPORT_TITLE', default='CyberScan - Report Scan'), str(soup), flags=re.IGNORECASE)
                    file.write(str(html_out))

                file.close()
                f.close()

                f = open(local_dir_tmp+temp_file+".html", "r")
                c = collections.OrderedDict()
                l = None
                for td in soup.findAll('td'):
                    if td.text == 'High' or td.text == 'Medium' or td.text == 'Low' or td.text == 'Informational':
                        l = str(td.text)
                        continue

                    if len(c) >= 4:
                        continue

                    c[l] = int(td.text)
                f.close()

                # { "High": 0, "Medium": 0, "Low": 0, "Informational": 0}
                json_access_complexity_data = json.dumps(c, default=str)

                html_name = temp_file+".html"
                html_outpath = local_dir_tmp+temp_file+".html"
                json_outpath = local_dir_tmp+temp_file+".json"
                pdf_name = temp_file+".pdf"
                pdf_outpath = local_dir_tmp+pdf_name

                pdf = weasyprint.HTML(html_outpath).write_pdf()
                open(pdf_outpath, 'wb').write(pdf)

                bucket_path_report = "report/{}/{}".format(client_id, pdf_name)
                obj_tools_s3.upload_file(
                    pdf_outpath,
                    config('AWS_UPLOAD_BUCKET'),
                    bucket_path_report
                )

                json_file = open(json_outpath, "r")

                scanreport_data = ScanReports.objects.create(
                    user_id=client_id,
                    json_result=str(json_file.read()),
                    report_path=str(bucket_path_report)
                )

                json_file.close()

                os.remove(local_dir_tmp + str(temp_file))
                os.remove(str(html_outpath))
                os.remove(str(json_outpath))
                os.remove(str(pdf_outpath))

                link_expires_on = int(expires)
                url_signed = obj_tools_s3.create_presigned_url(
                    config('AWS_UPLOAD_BUCKET'),
                    str(bucket_path_report),
                    link_expires_on
                )

                break

        return url_signed, link_expires_on, scanreport_data.id, json_access_complexity_data