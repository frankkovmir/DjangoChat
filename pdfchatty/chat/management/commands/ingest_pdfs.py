from django.core.management.base import BaseCommand
from django.utils import timezone
from chat.pdf_handler import add_documents_to_db
from chat.models import ProcessedFile
import os
from datetime import datetime

class Command(BaseCommand):
    help = 'Ingest PDFs from the pdfs folder'

    def handle(self, *args, **kwargs):
        pdf_directory = os.path.join(os.path.dirname(__file__), '../../../pdfs')
        pdf_files = [os.path.join(pdf_directory, f) for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

        new_files = []
        for pdf_file in pdf_files:
            filename = os.path.basename(pdf_file)
            last_modified = timezone.make_aware(datetime.fromtimestamp(os.path.getmtime(pdf_file)), timezone.get_current_timezone())
            try:
                processed_file = ProcessedFile.objects.get(filename=filename)
                if processed_file.last_modified < last_modified:
                    new_files.append(pdf_file)
                    processed_file.last_modified = last_modified
                    processed_file.save()
            except ProcessedFile.DoesNotExist:
                new_files.append(pdf_file)
                ProcessedFile.objects.create(filename=filename, last_modified=last_modified)

        if new_files:
            add_documents_to_db(new_files)
            self.stdout.write(self.style.SUCCESS('Successfully ingested new PDFs'))
        else:
            self.stdout.write(self.style.SUCCESS('No new PDFs to ingest'))
