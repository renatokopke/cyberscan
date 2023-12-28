from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework import generics

from core.classes.engine_owasp import EngineOWASP
from django.http import JsonResponse

from scan.models import ScanReports

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    # Python 2.x fallback
    from argparse import Namespace


class TargetView(generics.ListAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    # require that the user is minimal authenticad
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):

        client_id = request.user.id
        url = request.data['url']
        expires = request.data['expires']

        obj_scan = EngineOWASP()
        (link_report, link_expires_on, report_id, json_access_complexity_data) = obj_scan.scan(client_id, url, expires)

        json_resp = {
            "report_id": report_id,
            "access_complexity": json_access_complexity_data,
            "report": link_report,
            "expires": link_expires_on,
            "status_code": 201
        }

        return JsonResponse(json.loads(json.dumps(json_resp, indent=4)), safe=False, status=status.HTTP_201_CREATED)


class ReportViewListView(generics.ListAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def list(self, request, pk, **kwargs):
        client_id = request.user.id

        scan_data = ScanReports.objects.filter(Q(id=client_id)).get()

        json_resp = {
            "status_code": 200
        }

        return JsonResponse(json.loads(json.dumps(json_resp, indent=4)), safe=False, status=status.HTTP_200_OK)