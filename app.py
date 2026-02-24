import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# Configuración de idioma para que Streamlit use calendario en español
# Nota: Streamlit usa el idioma del navegador por defecto, pero forzamos 
# el formato de texto en el PDF.

class CertificatePDF(FPDF):
    def header(self):
        # Borde decorativo inspirado en el diseño de Canva
        self.set_draw_color(100, 50, 20) # Café Barista
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
    fecha_texto = f"{date_obj.day} de {meses[date_obj.month]} de {date_obj.year}"

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
    
    # Nombre del alumno (Elegante y grande)
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 32)
    pdf.set_text_color(120, 90, 40)
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
    pdf.set_x(25)
    pdf.multi_cell(160, 9, texto_detalle, align='
