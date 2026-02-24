import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# Clase para el diseño del PDF
class CertificatePDF(FPDF):
    def header(self):
        # Borde decorativo doble (Café Barista)
        self.set_draw_color(100, 50, 20) 
        self.set_line_width(1.5)
        self.rect(10, 10, 190, 277)
        self.set_line_width(0.5)
        self.rect(12, 12, 186, 273)

def generate_certificate(name, date_obj):
    # Traductor de meses para el PDF final
    meses_es = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
        7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    fecha_formateada = f"{date_obj.day} de {meses_es[date_obj.month]} de {date_obj.year}"

    pdf = CertificatePDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # --- ENCABEZADO ---
    pdf.set_y(45)
    pdf.set_font('Helvetica', 'B', 40)
    pdf.set_text_color(100, 50, 20)
    pdf.cell(0, 15, 'CERTIFICADO', ln=True, align='C')
    
    pdf.set_font('Helvetica', '', 18)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, 'De participación', ln=True, align='C')
    
    # --- CUERPO ---
    pdf.ln(25)
    pdf.set_font('Helvetica', '', 15)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, 'El reconocimiento es para:', ln=True, align='C')
    
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 32)
    pdf.set_text_color(120, 90, 40)
    pdf.cell(0, 20, name.upper(), ln=True, align='C')
    
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 13)
    pdf.set_text_color(40, 40, 40)
    # Texto alineado al diseño de Canva
    detalle = (
        "Por completar el curso de barista integral de (Cata, Espresso, "
        "Latte Art, Brewing) demostrando un profundo conocimiento "
        "en la preparación de café de especialidad."
    )
    pdf.set_x(25)
    pdf.multi_cell(160, 9, detalle, align='C')
    
    # --- FIRMA Y PIE DE PÁGINA ---
    if os.path.exists("firma.png"):
        # Posicionada exactamente sobre el nombre del instructor
        pdf.image("firma.png", x=135, y=210, w=45)
    
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

# --- INTERFAZ DE USUARIO ---
st.set_page_config(page_title="Generador de Certificados SCA", page_icon="☕")

st.title("☕ Generador de Certificados SCA")
st.write("Bienvenido, Enrique. Ingresa los datos para emitir el diploma.")

# Formulario para evitar recargas innecesarias
with st.form("form_emision"):
    nombre_alumno = st.text_input("Nombre del Alumno", placeholder="Ej. Juan Pérez")
    
    # El calendario de Streamlit responde al idioma de tu navegador automáticamente
    fecha_curso = st.date_input("Fecha del curso", value=datetime.now())
    
    boton_generar = st.form_submit_button("Generar Diploma")

if boton_generar:
    if nombre_alumno:
        try:
            pdf_out = generate_certificate(nombre_alumno, fecha_curso)
            st.success(f"✅ ¡Diploma para {nombre_alumno} generado con éxito!")
            st.download_button(
                label="⬇️ Descargar PDF",
                data=pdf_out,
                file_name=f"Certificado_{nombre_alumno.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error técnico al generar el archivo: {e}")
    else:
        st.warning("⚠️ Debes escribir el nombre del alumno para continuar.")
