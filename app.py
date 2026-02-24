import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# Configuración inicial de la página
st.set_page_config(page_title="Generador de Certificados SCA", page_icon="☕")

class CertificatePDF(FPDF):
    def header(self):
        # Doble borde decorativo (Color Café)
        self.set_draw_color(100, 50, 20) 
        self.set_line_width(1.5)
        self.rect(10, 10, 190, 277)
        self.set_line_width(0.5)
        self.rect(12, 12, 186, 273)

def generate_certificate(name, date_obj):
    # Diccionario para nombres de meses en español
    meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
        7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    fecha_formateada = f"{date_obj.day} de {meses[date_obj.month]} de {date_obj.year}"

    pdf = CertificatePDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # --- LOGOTIPO ---
    # Se añade solo si el archivo logo.png existe en el repositorio
    if os.path.exists("logo.png"):
        pdf.image("logo.png", x=150, y=20, w=40)

    # --- ENCABEZADO ---
    pdf.set_y(50)
    pdf.set_font('Helvetica', 'B', 40)
    pdf.set_text_color(100, 50, 20)
    pdf.cell(0, 15, 'CERTIFICADO', ln=True, align='C')
    
    pdf.set_font('Helvetica', '', 18)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, 'De participacion', ln=True, align='C')
    
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
    
    # Texto del curso (Sin caracteres especiales complejos para evitar errores de PDF)
    detalle_curso = (
        "Por completar el curso de barista integral de (Cata, Espresso, "
        "Latte Art, Brewing) demostrando un profundo conocimiento "
        "en la preparacion de cafe de especialidad."
    )
    pdf.set_x(25)
    pdf.multi_cell(160, 9, detalle_curso, align='C')
    
    # --- PIE DE PAGINA ---
    pdf.set_y(250)
    
    # Izquierda: Ubicacion y Fecha
    pdf.set_x(25)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(80, 5, 'Metepec, Estado de Mexico', ln=1, align='L')
    pdf.set_x(25)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(80, 5, fecha_formateada, ln=0, align='L')
    
    # Derecha: Instructor
    pdf.set_y(250)
    pdf.set_x(115)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(70, 5, 'Enrique Morales Medina', ln=1, align='R')
    pdf.set_x(115)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(70, 5, 'Impartido por Barista Certificado SCA', ln=0, align='R')
    
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ DE STREAMLIT ---
st.title("☕ Generador de Certificados SCA")
st.write("Ingresa los datos del alumno para generar el diploma.")

# El formulario agrupa los elementos y evita que la app se recargue a cada momento
with st.form("generador_form"):
    nombre = st.text_input("Nombre del Alumno", placeholder="Ej: Juan Perez")
    
    # Calendario: Streamlit usa el idioma del navegador. 
    # Si tu navegador esta en español, se vera en español.
    fecha = st.date_input("Selecciona la fecha", value=datetime.now())
    
    boton_crear = st.form_submit_button("Generar Certificado")

if boton_crear:
    if nombre:
        try:
            archivo_pdf = generate_certificate(nombre, fecha)
            st.success(f"✅ ¡Certificado para {nombre} generado con éxito!")
            st.download_button(
                label="⬇️ Descargar PDF",
                data=archivo_pdf,
                file_name=f"Certificado_{nombre.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Ocurrió un error al generar el PDF: {e}")
    else:
        st.warning("⚠️ Por favor, ingresa el nombre del alumno.")
