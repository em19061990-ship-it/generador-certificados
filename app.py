import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# Configuración de la página de Streamlit
st.set_page_config(page_title="Generador de Certificados SCA", page_icon="☕")

class CertificatePDF(FPDF):
    def header(self):
        # Borde decorativo elegante (Color Café Barista)
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
    fecha_texto = f"{date_obj.day} de {meses_es[date_obj.month]} de {date_obj.year}"

    pdf = CertificatePDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # --- LOGOTIPO ---
    # Se incluirá si existe el archivo logo.png en GitHub
    if os.path.exists("logo.png"):
        pdf.image("logo.png", x=150, y=20, w=40)

    # --- ENCABEZADO ---
    pdf.set_y(50)
    pdf.set_font('Helvetica', 'B', 40)
    pdf.set_text_color(100, 50, 20)
    pdf.cell(0, 15, 'CERTIFICADO', ln=True, align='C')
    
    pdf.set_font('Helvetica', '', 18)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, 'De participación', ln=True, align='C')
