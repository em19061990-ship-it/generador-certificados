import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# --- CÓDIGO PARA OCULTAR MARCA DE AGUA Y MENÚS ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            #stDecoration {display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Configuración de la interfaz de la aplicación
st.set_page_config(page_title="Genera tu Certificado Barista", page_icon="☕")

class CertificatePDF(FPDF):
    def add_background(self):
        # Inserta la imagen de fondo cubriendo toda la hoja A4 (210x297mm)
        if os.path.exists("fondo.png"):
            self.image("fondo.png", 0, 0, 210, 297)

def generate_certificate(name, date_obj):
    # Diccionario para nombres de meses en español
    meses_es = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
        7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    fecha_texto = f"{date_obj.day} de {meses_es[date_obj.month]} de {date_obj.year}"

    # Crear instancia del PDF en orientación vertical (Portrait)
    pdf = CertificatePDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # 1. Capa de Fondo (se dibuja primero)
    pdf.add_background()
    
    # 2. Logotipo (si el archivo logo.png existe en GitHub)
    if os.path.exists("logo.png"):
        pdf.image("logo.png", x=155, y=25, w=35)

    # --- SECCIÓN DE TÍTULOS ---
    pdf.set_y(75)
    pdf.set_font('Helvetica', 'B', 42)
    pdf.set_text_color(100, 50, 20) # Café oscuro
    pdf.cell(0, 15, 'CERTIFICADO', ln=True, align='C')
    
    pdf.set_font('Helvetica', '', 18)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, 'De participación', ln=True, align='C')
    
    # --- CUERPO DEL TEXTO ---
    pdf.ln(25)
    pdf.set_font('Helvetica', '', 15)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, 'El reconocimiento es para:', ln=True, align='C')
    
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 32)
    pdf.set_text_color(120, 90, 40) # Café dorado
    pdf.cell(0, 20, name.upper(), ln=True, align='C')
    
    # --- DESCRIPCIÓN EN 2 LÍNEAS ---
    # Reducimos ligeramente el tamaño a 13 y ampliamos el ancho a 185mm
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 13)
    pdf.set_text_color(45, 45, 45)
    
    detalle_curso = (
        "Por completar el curso de barista integral de (Cata, Espresso, Latte Art, "
        "Brewing) demostrando un profundo conocimiento en la preparación de café de especialidad."
    )
    
    # Centramos el bloque aumentando el espacio horizontal para que no salte a 3 líneas
    pdf.set_x(12.5) 
    pdf.multi_cell(185, 8, detalle_curso, align='C')
    
    # --- PIE DE PÁGINA ---
    pdf.set_y(255)
    
    # Ubicación y Fecha (Izquierda)
    pdf.set_x(25)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(80, 5, 'Metepec, Estado de México', ln=1, align='L')
    pdf.set_x(25)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(80, 5, fecha_texto, ln=0, align='L')
    
    # Instructor (Derecha)
    pdf.set_y(255)
    pdf.set_x(115)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(70, 5, 'Enrique Morales Medina', ln=1, align='R')
    pdf.set_x(115)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(70, 5, 'Impartido por Barista Certificado SCA', ln=0, align='R')
    
    # Retornar el PDF como un flujo de bytes
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ DE USUARIO EN STREAMLIT ---
st.title("☕ Genera tu Certificado Barista")
st.write("Gracias por estar en el curso de Baristas Dulce Fénix.")

with st.form("form_emision"):
    nombre_alumno = st.text_input("Nombre completo del Alumno", placeholder="Ej. Dulce Fénix")
    fecha_curso = st.date_input("¿Cuándo terminaste tu curso?", value=datetime.now())
    
    submit = st.form_submit_button("Generar Diploma")

if submit:
    if nombre_alumno:
        try:
            pdf_out = generate_certificate(nombre_alumno, fecha_curso)
            st.success(f"✅ ¡Diploma generado para {nombre_alumno}!")
            st.download_button(
                label="⬇️ Descargar PDF",
                data=pdf_out,
                file_name=f"Certificado_{nombre_alumno.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error al generar el archivo: {e}")
    else:
        st.warning("⚠️ Por favor, ingresa el nombre del alumno.")
