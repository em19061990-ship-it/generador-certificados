import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

class CertificatePDF(FPDF):
    def header(self):
        # Borde decorativo elegante
        self.set_draw_color(100, 50, 20) 
        self.set_line_width(1.5)
        self.rect(10, 10, 190, 277)
        self.set_line_width(0.5)
        self.rect(12, 12, 186, 273)

def generate_certificate(name, date_obj):
    meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
        7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    fecha_formateada = f"{date_obj.day} de {meses[date_obj.month]} de {date_obj.year}"

    pdf = CertificatePDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Título
    pdf.set_y(45)
    pdf.set_font('Helvetica', 'B', 38)
    pdf.set_text_color(100, 50, 20)
    pdf.cell(0, 15, 'CERTIFICADO', ln=True, align='C')
    
    pdf.set_font('Helvetica', '', 18)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, 'DE PARTICIPACIÓN', ln=True, align='C')
    
    # Cuerpo
    pdf.ln(25)
    pdf.set_font('Helvetica', '', 15)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, 'El reconocimiento es para:', ln=True, align='C')
    
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 30)
    pdf.set_text_color(120, 90, 40)
    pdf.cell(0, 20, name.upper(), ln=True, align='C')
    
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 13)
    pdf.set_text_color(40, 40, 40)
    texto_detalle = (
        "Por completar el curso de barista integral de (Cata, Espresso, "
        "Latte Art, Brewing) demostrando un profundo conocimiento "
        "en la preparación de café de especialidad."
    )
    pdf.set_x(25)
    pdf.multi_cell(160, 9, texto_detalle, align='C')
    
    # Firma (se posiciona antes del texto del instructor)
    if os.path.exists("firma.png"):
        pdf.image("firma.png", x=140, y=215, w=40)
    
    pdf.set_y(245)
    # Izquierda: Ubicación y Fecha
    pdf.set_x(25)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(80, 5, 'Metepec, Estado de México', ln=1, align='L')
    pdf.set_x(25)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(80, 5, fecha_formateada, ln=0, align='L')
    
    # Derecha: Instructor
    pdf.set_y(245)
    pdf.set_x(115)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(70, 5, 'Enrique Morales Medina', ln=1, align='R')
    pdf.set_x(115)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(70, 5, 'Impartido por Barista Certificado SCA', ln=0, align='R')
    
    return pdf.output(dest='S').encode('latin-1')

# Interfaz Streamlit
st.set_page_config(page_title="Generador de Certificados", page_icon="☕")

st.title("☕ Generador de Certificados SCA")
st.subheader("Configuración de Reconocimiento")

# EL FORMULARIO (CORREGIDO)
with st.form("form_diseno"):
    nombre_input = st.text_input("Nombre del Alumno", placeholder="Escribe el nombre completo")
    fecha_input = st.date_input("Selecciona la fecha del curso", value=datetime.now())
    # El botón DEBE estar dentro del bloque 'with'
    submit_button = st.form_submit_button("Generar Certificado")

if submit_button:
    if nombre_input:
        try:
            pdf_data = generate_certificate(nombre_input, fecha_input)
            st.success(f"✅ ¡Certificado para {nombre_input} generado!")
            st.download_button(
                label="⬇️ Descargar PDF",
                data=pdf_data,
                file_name=f"Certificado_{nombre_input.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error al generar: {e}")
    else:
        st.warning("Escribe el nombre del alumno.")
