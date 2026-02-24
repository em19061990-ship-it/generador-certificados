import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

class CertificatePDF(FPDF):
    def header(self):
        # Borde decorativo inspirado en tu diseño de Canva
        self.set_draw_color(100, 50, 20) 
        self.set_line_width(1.5)
        self.rect(10, 10, 190, 277)
        self.set_line_width(0.5)
        self.rect(12, 12, 186, 273)

def generate_certificate(name, date_obj):
    # Traductor de meses para el PDF
    meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
        7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    fecha_texto = f"{date_obj.day} de {meses[date_obj.month]} de {date_obj.year}"

    pdf = CertificatePDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # --- TÍTULOS ---
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
    # Texto corregido para evitar errores de comillas
    texto_detalle = (
        "Por completar el curso de barista integral de (Cata, Espresso, "
        "Latte Art, Brewing) demostrando un profundo conocimiento "
        "en la preparación de café de especialidad."
    )
    pdf.set_x(25)
    pdf.multi_cell(160, 9, texto_detalle, align='C')
    
    # --- FIRMA E INSTRUCTOR ---
    if os.path.exists("firma.png"):
        pdf.image("firma.png", x=135, y=210, w=45)
    
    pdf.set_y(245)
    # Izquierda
    pdf.set_x(25)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(80, 5, 'Metepec, Estado de México', ln=1, align='L')
    pdf.set_x(25)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(80, 5, fecha_texto, ln=0, align='L')
    
    # Derecha
    pdf.set_y(245)
    pdf.set_x(115)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(70, 5, 'Enrique Morales Medina', ln=1, align='R')
    pdf.set_x(115)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(70, 5, 'Impartido por Barista Certificado SCA', ln=0, align='R')
    
    return pdf.output(dest='S').encode('latin
