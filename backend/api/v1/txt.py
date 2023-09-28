from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pagesizes import letter

# urls.py
# path('venue_pdf', views.venue_pdf, name='venue_pdf'),


def venue_pdf(request):
	buf = io.BytesIO()
	c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
	textob = c.beginText()
	textob.setTextOrigin(inch, inch)
	textob.setFont("Helvetica", 14)

	venues = Venue.objects.all()

	lines = []

	for venue in venues:
		lines.append(venue.name)
		lines.append(venue.address)
		lines.append(venue.zip_code)
		lines.append(venue.phone)
		lines.append(venue.web)
		lines.append(venue.email_address)
		lines.append(" ")

	for line in lines:
		textob.textLine(line)

	c.drawText(textob)
	c.showPage()
	c.save()
	buf.seek(0)

	return FileResponse(buf, as_attachment=True, filename='venue.pdf')
