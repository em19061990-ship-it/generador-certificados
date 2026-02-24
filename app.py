import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

class CertificatePDF(FPDF):
    def header(self):
        # Borde elegante doble
        self.set_draw_color(100, 50, 20) # Color café oscuro
        self.set_line_width(1.5)
        self.rect(5, 5, 200, 287) if self.k == 1 else self.rect(5, 5, 287, 200)

def generate_certificate(name, date):
    # Orientación vertical para coincidir con tu nueva imagen
    pdf = CertificatePDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Título Principal
    pdf.set_y(40)
    pdf.set_font('Helvetica', 'B', 35)
    pdf.set_text_color(100, 50, 20)
    pdf.cell(0, 15, 'CERTIFICADO', ln=True, align='C')
    
    pdf.set_font('Helvetica', '', 18)
    pdf.cell(0, 10, 'De participación', ln=True, align='C')
    
    # Cuerpo del texto
    pdf.ln(20)
    pdf.set_font('Helvetica', '', 14)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, 'El reconocimiento es para:', ln=True, align='C')
    
    # Nombre del alumno
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 28)
    pdf.cell(0, 20, name, ln=True, align='C')
    
    # Descripción profesional (basada en tu imagen)
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 12)
    texto_detalle = (
        "Por completar el curso de barista integral de (Cata, Espresso, "
        "Latte Art, Brewing) demostrando un profundo conocimiento "
        "en la preparación de café de especialidad."
    )
    pdf.multi_cell(0, 8, texto_detalle, align='C')
    
    # Footer: Fecha e Instructor
    pdf.set_y(240)
    
    # Columna Izquierda: Ubicación y Fecha
    pdf.set_x(20)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(80, 5, 'Metepec, Estado de México', ln=0, align='L')
    
    # Columna Derecha: Nombre Instructor
    pdf.set_x(110)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(80, 5, 'Enrique Morales Medina', ln=1, align='R')
    
    # Segunda línea del footer
    pdf.set_x(20)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(80, 5, date, ln=0, align='L')
    
    pdf.set_x(110)
    pdf.cell(80, 5, 'Impartido por Barista Certificado SCA', ln=1, align='R')

    # Posicionamiento de la firma (justo sobre el nombre)
    if os.path.exists("firma.png"):
        pdf.image("firma.png", x=145, y=215, w=40)
    
    return pdf.output(dest='S').encode('latin-1')

# Configuración de la App
st.set_page_config(page_title="Generador de Certificados", page_icon="☕")

st.title("☕ Generador de Certificados Profesional")

with st.form("cert_form"):
    nombre = st.text_input("Nombre completo del alumno")
    fecha_manual = st.text_input("Fecha (ej: 06 Octubre 2025)", value=datetime.now().strftime("%d %B %Y"))
    enviar = st.form_submit_button("Generar Certificado")

if enviar:
    if nombre:
        pdf_bytes = generate_certificate(nombre, fecha_manual)
        st.success("¡Certificado generado!")
        st.download_button("⬇️ Descargar PDF", pdf_bytes, f"Certificado_{nombre}.pdf", "application/pdf")
    else:
        st.error("Por favor ingresa un nombre.")
