# Coloca aquí el logo de la Universidad San Sebastián

Guarda el escudo como **logo_uss.png** en esta carpeta (assets/logo_uss.png).
Luego regenera los documentos:

    python src/exportar_pdf.py
    python src/exportar_docx.py

Las portadas del PDF y del Word lo insertarán automáticamente. Mientras no exista
el archivo, la portada usa el encabezado tipográfico (sin error).
