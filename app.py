import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# Configuración de la página de Streamlit
st.set_page_config(page_title="Generador de Certificados SCA", page_icon="☕")

class CertificatePDF(FPDF):
    def add_background(self):
        # Si el archivo fondo.png existe, se pone como fondo de toda la página
        if os.path.exists("fondo.png"):
            # x=0, y=0, w=210 (ancho A4), h=297 (alto A4)
            self.image("fondo.png", 0, 0, 210, 297)

def generate_certificate(name, date_obj):
    # Traductor de meses
    meses_es = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
        7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    fecha_texto = f"{date_obj.day} de {meses_es[date_obj.month]} de {date_obj.year}"

    # Creamos el PDF
    pdf = CertificatePDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # 1. Ponemos el fondo primero
    pdf.add_background()
    
    # 2. Logotipo circular (si existe)
    if os.path.exists("logo.png"):
        pdf.image("logo.png", x=155, y=25, w=35)

    # --- TEXTO SOBRE EL FONDO ---
    
    # Título Principal
    pdf.set_y(75) # Ajustado para que no choque con las ondas superiores
    pdf.set_font('Helvetica', 'B', 42)
    pdf.set_text_color(100, 50, 20) # Color café oscuro
    pdf.cell(0, 15, 'CERTIFICADO', ln=True, align='C')
    
    pdf.set_font('Helvetica', '', 18)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, 'De participación', ln=True, align='C')
    
    # Cuerpo
    pdf.ln(25)
    pdf.set_font('Helvetica', '', 15)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, 'El reconocimiento es para:', ln=True, align='C')
    
    # Nombre del Alumno
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 32)
    pdf.set_text_color(120, 90, 40) # Color café dorado
    pdf.cell(0, 20, name.upper(), ln=True, align='C')
    
    # Detalle del curso
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 13)
    pdf.set_text_color(40, 40, 40)
    detalle = (
        "Por completar el curso de barista integral de (Cata, Espresso, "
        "Latte Art, Brewing) demostrando un profundo conocimiento "
        "en la preparación de café de especialidad."
    )
    pdf.set_x(25)
    pdf.multi_cell(160, 9, detalle, align='C')
    
    # --- PIE DE PÁGINA (Sobre las ondas inferiores) ---
    pdf.set_y(255)
    
    # Izquierda: Ubicación y Fecha
    pdf.set_x(25)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(80, 5, 'Metepec, Estado de México', ln=1, align='L')
    pdf.set_x(25)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(80, 5, fecha_texto, ln=0, align='L')
    
    # Derecha: Instructor
    pdf.set_y(255)
    pdf.set_x(115)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(70, 5, 'Enrique Morales Medina', ln=1, align='R')
    pdf.set_x(115)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(70, 5, 'Impartido por Barista Certificado SCA', ln=0, align='R')
    
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ STREAMLIT ---
st.title("☕ Generador de Certificados SCA")
st.write("Crea diplomas con fondo personalizado.")

with st.form("form_final"):
    nombre_alumno = st.text_input("Nombre completo del Alumno")
    fecha_curso = st.date_input("Fecha del curso", value=datetime.now())
    boton = st.form_submit_button("Generar Diploma")

if boton:
    if nombre_alumno:
        try:
            pdf_bytes = generate_certificate(nombre_alumno, fecha_curso)
            st.success(f"✅ Certificado generado con fondo para {nombre_alumno}")
            st.download_button(
                label="⬇️ Descargar PDF",
                data=pdf_bytes,
                file_name=f"Certificado_{nombre_alumno.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("⚠️ Escribe el nombre del alumno.")
