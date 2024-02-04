from django.views.generic import View
from org.junit.jupiter.api.Assertions import assertEquals
from rest_framework.views import APIView

fruit_stock = {
    'apple': 42,
    'orange': 21,  # [syntax-error]
    'banana': 12
}
dict_fruit_stock = {'apple': 42, 'orange': 21, 'banana': 12}
print(fruit_stock['apple'])
print(dict_fruit_stock['apple'])
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with open('templates/index.html', 'r') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(content, 'utf8'))
        except:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404: File not found')

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with open('templates/index.html', 'r') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(content, 'utf8'))
        except:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404: File not found')

httpd = HTTPServer(('', 8000), MyHandler)
httpd.serve_forever()
import org.junit.jupiter.api.Assertions.assertEquals
import static

// import org.junit.jupiter.api.Test;

public class Main {
  public static void main(String[] args) {
    System.out.println("Hello world!");
  }

  // @Test
  // void addition() {
  //     assertEquals(2, 1 + 1);
  // }
}class EventGenerateAPIView(APIView):
  permission_classes = ALL_PERMISSIONS

  def get_queryset(self):
      user = self.request.user
      event_id = self.kwargs.get("event_id")
      queryset = Event_Management.objects.filter(id=event_id)
      if user.role.code == RoleCodes.ADMIN:
          return queryset
      elif user.role.code in [
          RoleCodes.IIB_ADMIN,
          RoleCodes.MG_ADMIN,
          RoleCodes.FVV_ADMIN,
      ]:
          return queryset.filter(responsible_to_event__user=user)
      else:
          return queryset.filter(created_by=user)

  def get(self, request, *args, **kwargs):
      queryset = self.get_queryset()
      if not queryset.exists():
          return Response(
              {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
          )

      event = queryset.first()
      mg_armed_force_exists = Responsible.objects.filter(
          event_management=event, armed_force__short_name_uz=AgencyCodes.MG
      ).exists()
      allocated_technical_means = Allocated_Technical_Means.objects.filter(
          event_management=event
      )
      service_types = Service_Type.objects.all().order_by("id")
      iib_numbers = get_allocated_technical_means_numbers(
          allocated_technical_means, AgencyCodes.IIB, service_types
      )
      mg_numbers = get_allocated_technical_means_numbers(
          allocated_technical_means, AgencyCodes.MG, service_types
      )
      fvv_numbers = get_allocated_technical_means_numbers(
          allocated_technical_means, AgencyCodes.FVV, service_types
      )
      template_path = "apps/event/fixtures/event_3.docx"
      doc = DocxTemplate(template_path)

      context = {
          "responsible": event.responsible,
          "document_name": event.document_name,
          "date": f"{event.date.day}.{event.date.month}.{event.date.year}",
          "time": event.time,
          "event_object_name": event.event_object_name,
          "number_of_citizens": event.number_of_citizens,
          "instruction_time": event.instruction_time,
          "mg_armed_force_exists": mg_armed_force_exists,
          "col_labels": service_types.values_list("name_cyr", flat=True),
          "tbl_contents": [
              {
                  "label": "ИИВ",
                  "cols": [iib_numbers[i] for i in range(10)],
              },
              {
                  "label": "ФВВ",
                  "cols": [fvv_numbers[i] for i in range(10)],
              },
              {"label": "Жами", "cols": total_number(iib_numbers, fvv_numbers)},
          ],
          "f_tbl_contents": [
              {
                  "label": "ИИВ",
                  "cols": [iib_numbers[i] for i in range(10)],
              },
              {
                  "label": "МГ",
                  "cols": [mg_numbers[i] for i in range(10)],
              },
              {
                  "label": "ФВВ",
                  "cols": [fvv_numbers[i] for i in range(10)],
              },
              {
                  "label": "Жами",
                  "cols": total_number(iib_numbers, fvv_numbers, mg_numbers),
              },
          ],
      }
      doc.render(context)

      # Convert DOCX to PDF
      pdf_buffer = BytesIO()
      temp_docx_path = "/tmp/temp_docx.docx"

      # Save the rendered DOCX content to a temporary file
      doc.save(temp_docx_path)

      # Use LibreOffice to convert DOCX to PDF
      libreoffice_command = [
          "libreoffice",
          "--headless",
          "--convert-to",
          "pdf",
          "--outdir",
          "/tmp",
          temp_docx_path,
      ]

      try:
          subprocess.run(libreoffice_command, check=True)
      except subprocess.CalledProcessError as e:
          # Handle the conversion error as needed
          raise Exception(f"LibreOffice conversion error: {e}")

      # Read the generated PDF file
      with open("/tmp/temp_docx.pdf", "rb") as pdf_file:
          pdf_buffer = BytesIO(pdf_file.read())

      # Prepare the response with the PDF content
      response = HttpResponse(pdf_buffer, content_type="application/pdf")
      response["Content-Disposition"] = 'attachment; filename="event_3.pdf"'
      return response 
        End of EventGenerateAPIView class