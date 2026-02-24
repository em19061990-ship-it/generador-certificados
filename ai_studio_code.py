import streamlit as st
from fpdf import FPDF
from datetime import datetime

class CertificatePDF(FPDF):
    def header(self):
        # Marco exterior
        self.set_line_width(1)
        self.rect(5, 5, 287, 200)
        # Marco interior dorado (simulado con gris oscuro/marrón)
        self.set_draw_color(180, 150, 100)
        self.set_line_width(2)
        self.rect(10, 10, 277, 190)

def generate_certificate(name, date):
    pdf = CertificatePDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    
    # Título
    pdf.set_text_color(30, 30, 30)
    pdf.set_font('Helvetica', 'B', 40)
    pdf.cell(0, 50, 'Certificado de Participación', ln=True, align='C')
    
    # Texto por defecto
    pdf.set_font('Helvetica', '', 18)
    pdf.cell(0, 10, 'Gracias por asistir a tu curso', ln=True, align='C')
    
    # Nombre del participante
    pdf.ln(20)
    pdf.set_font('Helvetica', '', 14)
    pdf.cell(0, 10, 'Se otorga el presente a:', ln=True, align='C')
    
    pdf.set_font('Helvetica', 'BI', 32)
    pdf.set_text_color(180, 150, 100)
    pdf.cell(0, 25, name, ln=True, align='C')
    
    # Fecha
    pdf.ln(10)
    pdf.set_text_color(60, 60, 60)
    pdf.set_font('Helvetica', '', 14)
    pdf.cell(0, 10, f'Fecha del curso: {date}', ln=True, align='C')
    
    # Información del Instructor (Abajo a la derecha)
    pdf.set_y(170)
    pdf.set_x(200)
    pdf.set_text_color(30, 30, 30)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(80, 10, 'Enrique Morales Medina', ln=True, align='R')
    
    pdf.set_x(200)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(80, 5, 'Barista SCA 000111222333', ln=True, align='R')
    
    return pdf.output(dest='S').encode('latin-1')

# Interfaz de Streamlit
st.set_page_config(page_title="Generador de Certificados", page_icon="☕")

st.title("☕ Generador de Certificados Barista")
st.write("Completa los datos para generar el certificado en PDF.")

with st.form("certificate_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        nombre = st.text_input("Nombre del participante", placeholder="Ej. Juan Pérez")
    
    with col2:
        fecha = st.date_input("Fecha del curso", value=datetime.now())
    
    submit = st.form_submit_button("Generar Certificado")

if submit:
    if nombre:
        fecha_str = fecha.strftime("%d/%m/%Y")
        pdf_bytes = generate_certificate(nombre, fecha_str)
        
        st.success(f"¡Certificado para {nombre} listo!")
        
        st.download_button(
            label="Descargar Certificado PDF",
            data=pdf_bytes,
            file_name=f"Certificado_{nombre.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Por favor, ingresa el nombre del participante.")