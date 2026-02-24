import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# Configuración de la interfaz
st.set_page_config(page_title="Generador de Certificados SCA", page_icon="☕")

class CertificatePDF(FPDF):
    def add_background(self):
        # Inserta la imagen de fondo cubriendo toda la hoja A4
        if os.path.exists("fondo.png"):
            self.image("fondo.png", 0, 0, 210, 297)

def generate_certificate(name, date_obj):
    # Traducción de meses al español para el PDF
    meses_es = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
        7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    fecha_texto = f"{date_obj.day} de {meses_es[date_obj.month]} de {date_obj.year}"

    # Creación del documento
    pdf = CertificatePDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # 1. Capa de Fondo
    pdf.add_background()
    
    # 2. Logotipo (si existe)
    if os.path.exists("logo.png"):
        pdf.image("logo.png", x=155, y=25, w=35)

    # --- SECCIÓN DE TÍTULOS ---
    pdf.set_y(75)
    pdf.set_font('Helvetica', 'B', 42)
    pdf.set_text_color(100, 50, 20) # Tono café oscuro
    pdf.cell(0, 15, 'CERTIFICADO', ln=True, align='C')
    
    pdf.set_font('Helvetica', '', 18)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, 'De participacion', ln=True, align='C')
    
    # --- CUERPO DEL RECONOCIMIENTO ---
    pdf.ln(25)
    pdf.set_font('Helvetica', '', 15)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, 'El reconocimiento es para:', ln=True, align='C')
    
    # Nombre del alumno en mayúsculas
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 32)
    pdf.set_text_color(120, 90, 40)
    pdf.cell(0, 20, name.upper(), ln=True, align='C')
    
    # --- DESCRIPCIÓN DEL CURSO (CENTRADO PERFECTO) ---
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 14)
    pdf.set_text_color(45, 45, 45)
    
    detalle_curso = (
        "Por completar el curso de barista integral de (Cata, Espresso, "
        "Latte Art, Brewing) demostrando un profundo conocimiento "
        "en la preparacion de cafe de especialidad."
    )
    
    # Ajuste de margen para centrar el bloque de texto
    # Usamos un ancho de 170mm centrado en la página de 210mm
    pdf.set_x(20) 
    pdf.multi_cell(170, 8, detalle_curso, align='C')
    
    # --- PIE DE PÁGINA ---
    pdf.set_y(255)
    
    # Lado Izquierdo: Ubicación y Fecha
    pdf.set_x(25)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(80, 5, 'Metepec, Estado de Mexico', ln=1, align='L')
    pdf.set_x(25)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(80, 5, fecha_texto, ln=0, align='L')
    
    # Lado Derecho: Datos del Instructor
    pdf.set_y(255)
    pdf.set_x(115)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(70, 5, 'Enrique Morales Medina', ln=1, align='R')
    pdf.set_x(115)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(70, 5, 'Impartido por Barista Certificado SCA', ln=0, align='R')
    
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ DE USUARIO (STREAMLIT) ---
st.title("☕ Generador de Certificados SCA")
st.write("Configura los datos para emitir el diploma con fondo personalizado.")

with st.form("main_form"):
    nombre_alumno = st.text_input("Nombre completo del Alumno", placeholder="Ej. Juan Perez")
    
    # Calendario: Streamlit usa el idioma del navegador por defecto
    fecha_curso = st.date_input("Selecciona la fecha", value=datetime.now())
    
    submit_button = st.form_submit_button("Generar y Previsualizar")

if submit_button:
    if nombre_alumno:
        try:
            pdf_bytes = generate_certificate(nombre_alumno, fecha_curso)
            st.success(f"✅ ¡Certificado generado para {nombre_alumno}!")
            st.download_button(
                label="⬇️ Descargar PDF",
                data=pdf_bytes,
                file_name=f"Certificado_{nombre_alumno.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error técnico: {e}")
    else:
        st.warning("⚠️ Debes ingresar el nombre del alumno.")
