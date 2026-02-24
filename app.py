import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

class CertificatePDF(FPDF):
    def header(self):
        # Borde decorativo elegante (Color café oscuro/dorado)
        self.set_draw_color(100, 50, 20) 
        self.set_line_width(1.5)
        # Rectángulo principal (ajustado a formato vertical P)
        self.rect(10, 10, 190, 277)
        # Línea interior más delgada para un toque sofisticado
        self.set_line_width(0.5)
        self.rect(12, 12, 186, 273)

def generate_certificate(name, date_obj):
    # Formatear la fecha a texto (ej: 22 de Febrero de 2026)
    meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
        7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    fecha_formateada = f"{date_obj.day} de {meses[date_obj.month]} de {date_obj.year}"

    pdf = CertificatePDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # --- ENCABEZADO ---
    pdf.set_y(45)
    pdf.set_font('Helvetica', 'B', 38)
    pdf.set_text_color(100, 50, 20)
    pdf.cell(0, 15, 'CERTIFICADO', ln=True, align='C')
    
    pdf.set_font('Helvetica', '', 18)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, 'DE PARTICIPACIÓN', ln=True, align='C')
    
    # --- CUERPO ---
    pdf.ln(25)
    pdf.set_font('Helvetica', '', 15)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 10, 'El reconocimiento es para:', ln=True, align='C')
    
    # Nombre del alumno (Grande y destacado)
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 30)
    pdf.set_text_color(120, 90, 40) # Tono dorado/barista
    pdf.cell(0, 20, name.upper(), ln=True, align='C')
    
    # Descripción profesional
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 13)
    pdf.set_text_color(40, 40, 40)
    texto_detalle = (
        "Por completar el curso de barista integral de (Cata, Espresso, "
        "Latte Art, Brewing) demostrando un profundo conocimiento "
        "en la preparación de café de especialidad."
    )
    pdf.set_x(25) # Margen lateral para el texto
    pdf.multi_cell(160, 9, texto_detalle, align='C')
    
    # --- PIE DE PÁGINA (FIRMA Y DATOS) ---
    
    # Espacio para la firma
    if os.path.exists("firma.png"):
        # Centrado sobre el nombre del instructor
        pdf.image("firma.png", x=135, y=210, w=45)
    
    pdf.set_y(240)
    
    # Izquierda: Ubicación y Fecha
    pdf.set_x(25)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(80, 5, 'Metepec, Estado de México', ln=True, align='L')
    pdf.set_x(25)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(80, 5, fecha_formateada, ln=False, align='L')
    
    # Derecha: Instructor (alineado con la firma)
    pdf.set_y(240)
    pdf.set_x(115)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(70, 5, 'Enrique Morales Medina', ln=True, align='R')
    pdf.set_x(115)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(70, 5, 'Impartido por Barista Certificado SCA', ln=True, align='R')
    
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ DE STREAMLIT ---
st.set_page_config(page_title="Generador de Certificados", page_icon="☕", layout="centered")

st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #643214; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("☕ Generador de Certificados SCA")
st.subheader("Configuración de Reconocimiento Profesional")

with st.form("form_diseno"):
