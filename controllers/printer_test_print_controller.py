from google.appengine.api import taskqueue

from oauth2client.appengine import StorageByKeyName

import ann_config

from controllers.base_controller import BaseHandler
from helpers.print_job_enqueuer import PrintJobEnqueuer
from models.printer import Printer
from models.gcp_credentials import GcpCredentials

class PrinterTestPrintController(BaseHandler):
    def __init__(self, *args, **kw):
        super(PrinterTestPrintController, self).__init__(*args, **kw)
        self._require_login()

    def post(self):
        gcp_cred_storage = StorageByKeyName(GcpCredentials, self.user_bundle.user.user_id(), 'credentials')
        gcp_creds = gcp_cred_storage.get()

        if not gcp_creds:
            return self.redirect("/printers/add")

        printer = Printer.get_by_id(int(self.request.get("printer_key_id")))

        PrintJobEnqueuer.enqueue_to_printer(
            printer,
            "Distributed Press Test Print",
            "http://distributedpress.appspot.com"
        )

        self.redirect("/dashboard")
