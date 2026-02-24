def generate_certificate(name, date_obj):
    # ... (mismo código anterior para meses y fecha_formateada) ...
    meses_es = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
                7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
    fecha_formateada = f"{date_obj.day} de {meses_es[date_obj.month]} de {date_obj.year}"

    pdf = CertificatePDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # --- LOGOTIPO (NUEVA SECCIÓN) ---
    if os.path.exists("logo.png"):
        # x=155 para la derecha, y=20 para arriba, w=35 de ancho
        pdf.image("logo.png", x=155, y=20, w=35)

    # --- ENCABEZADO ---
    pdf.set_y(50) # Bajamos un poco el título para que no choque con el logo
    pdf.set_font('Helvetica', 'B', 40)
    pdf.set_text_color(100, 50, 20)
    pdf.cell(0, 15, 'CERTIFICADO', ln=True, align='C')
    
    # ... (el resto del código de cuerpo, firma y pie de página se mantiene igual) ...
