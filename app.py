import streamlit as st
import pandas as pd
import requests

# URL base de GitHub para los PDFs
GITHUB_REPO_URL = "https://raw.githubusercontent.com/leo-da-niel/azul/main/archivos/"

# Tu token de acceso personal de GitHub (reemplázalo por el token real)
GITHUB_TOKEN = "+645gniurfhgh"

# Función para obtener el archivo PDF desde GitHub
def get_pdf_from_github(pdf_filename):
    url = f"{GITHUB_REPO_URL}{pdf_filename}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}  # Agregar el token al encabezado
    response = requests.get(url, headers=headers)  # Hacer la solicitud con los encabezados
    
    st.write(f"URL solicitada: {url}")  # Imprime la URL para depuración
    
    if response.status_code == 200:
        return response.content  # Si la respuesta es exitosa, devolver el contenido del PDF
    else:
        st.error(f"No se pudo cargar el archivo {pdf_filename}. Código de estado: {response.status_code}")
        return None

# Interfaz principal de Streamlit
st.title("Prueba de API - Compra Consolidada Complementaria 2021")

# Cargar los datos del archivo Excel
excel_file = "rela.xlsx"  # Especifica la ruta a tu archivo Excel
data = pd.read_excel(excel_file)

# Mostrar los registros en formato de tabla
st.write("### Registros en el Archivo Excel")
st.dataframe(data)

# Filtro para seleccionar un registro específico
record_id = st.selectbox("Selecciona un registro para ver el PDF asociado", data["ID"].tolist())

# Mostrar detalles del registro seleccionado
selected_record = data[data["ID"] == record_id].iloc[0]
st.write(f"**Información del Registro Seleccionado:**")
st.json(selected_record.to_dict())

# Obtener el nombre del archivo PDF asociado
pdf_filename = selected_record["PDF Filename"]  # Asegúrate de que esta columna está en tu archivo Excel

# Mostrar el PDF
if st.button("Ver PDF"):
    pdf_content = get_pdf_from_github(pdf_filename)
    if pdf_content:
        st.download_button(
            label="Descargar PDF",
            data=pdf_content,
            file_name=pdf_filename,
            mime="application/pdf",
        )
        st.write("### Visualización del PDF")
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{pdf_content.decode("latin1")}" width="700" height="1000"></iframe>',
            unsafe_allow_html=True,
        )
