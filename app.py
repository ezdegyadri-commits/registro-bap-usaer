import streamlit as st
from google import genai
from docx import Document
from fpdf import FPDF
import io
from datetime import date

# Configuración con el nuevo SDK de Google GenAI
client = genai.Client(api_key="AQ.Ab8RN6JM_YMzUguhKme19dTI9laFp2pEaKDzojA5eEQR6nqrRw")

st.set_page_config(page_title="Instrumento de Registro BAP", page_icon="📝", layout="wide")

# Estilos CSS
st.markdown("""
<style>
    .caja-datos {
        background-color: #F6F1E9;
        border: 2px solid #C4A462;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        color: #333333;
    }
    .caja-instrucciones {
        border: 2px solid #2B5B41;
        padding: 20px;
        margin-bottom: 20px;
        background-color: #ffffff;
        color: #333333;
    }
    .titulo-seccion {
        color: #2B5B41;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def generar_docx(texto_informe, alumno):
    doc = Document()
    doc.add_heading('Informe de Análisis BAP', 0)
    doc.add_heading(f'Alumno: {alumno}', 1)
    doc.add_paragraph(texto_informe)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def generar_pdf(texto_informe, alumno):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    texto_limpio = texto_informe.encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(200, 10, txt=f"Informe de Analisis BAP - {alumno}", ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 7, txt=texto_limpio)
    return bytes(pdf.output())

# Encabezado
st.title("Instrumento de registro de las barreras para el aprendizaje y la participación")

# Datos Generales
st.markdown('<div class="caja-datos">', unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #333;'>DATOS GENERALES</h4>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
centro_escolar = col1.text_input("Centro Escolar:")
subsistema = col2.text_input("Subsistema:")
turno = col3.text_input("Turno:")

col4, col5 = st.columns(2)
grado = col4.text_input("Grado:")
grupo = col5.text_input("Grupo:")

nivel = st.radio("Nivel:", ["Inicial", "Preescolar", "Primaria", "Secundaria", "Laboral"], horizontal=True)
nombre_docentes = st.text_area("Nombre y función de las y los docentes, agentes educativos o equipo de apoyo:")
fecha_eval = st.date_input("Fecha:", value=date.today())
st.markdown('</div>', unsafe_allow_html=True)

# Instrucciones
st.markdown("""
<div class="caja-instrucciones">
    <p><strong>INSTRUCCIONES:</strong></p>
    <p>Después de revisar y analizar los diferentes insumos que se emplearon durante el proceso de diagnóstico socioeducativo, registren aquellas Barreras para el Aprendizaje y la Participación (BAP) que están enfrentando NNAJ. Identifiquen qué tipo de barrera es, la posible persona o agente educativo que la esté generando y el contexto en el cual se está presentando.</p>
</div>
""", unsafe_allow_html=True)

# Selección de BAP
st.markdown("<h3 class='titulo-seccion'>Clasificación de Barreras</h3>", unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["Estructurales", "Normativas", "Didácticas", "Actitudinales (Matriz)"])

bap_seleccionadas = []

with tab1:
    st.write("**BARRERAS ESTRUCTURALES: Normalizan la exclusión**")
    est_1 = st.checkbox("Negar la atención educativa por falta de recursos humanos, materiales, apoyos, capacitación, entre otras.")
    est_2 = st.checkbox("Infraestructura inadecuada (escolar o en el aula), falta de rampas, accesos, adecuaciones.")
    if est_1: bap_seleccionadas.append("Falta de recursos o capacitación (Estructural)")
    if est_2: bap_seleccionadas.append("Infraestructura inadecuada (Estructural)")

with tab2:
    st.write("**BARRERAS NORMATIVAS: Impedimento desde la Ley, norma, disposición política, etc.**")
    nor_1 = st.checkbox("Desconocimiento de los documentos normativos que regulan la atención educativa.")
    nor_2 = st.checkbox("Falta de un Programa Analítico que contextualice los Contenidos acordes a la diversidad.")
    if nor_1: bap_seleccionadas.append("Desconocimiento normativo (Normativa)")
    if nor_2: bap_seleccionadas.append("Falta de contextualización (Normativa)")

with tab3:
    st.write("**BARRERAS DIDÁCTICAS: Métodos de enseñanza y evaluación que no son acordes a las necesidades.**")
    did_1 = st.checkbox("Práctica docente homogeneizada sin considerar la diversidad.")
    did_2 = st.checkbox("Ausencia de Ajustes Razonables (AR) acordes a las necesidades específicas.")
    if did_1: bap_seleccionadas.append("Práctica homogeneizada (Didáctica)")
    if did_2: bap_seleccionadas.append("Ausencia de Ajustes Razonables (Didáctica)")

with tab4:
    st.write("**BARRERAS ACTITUDINALES: Relacionadas con las interacciones y concepciones sociales.**")
    col_desc, col_aula, col_escuela, col_familia = st.columns([4, 1, 1, 1])
    col_desc.write("**Descripción de la Barrera**")
    col_aula.write("**AULA/SALA**")
    col_escuela.write("**ESCUELA/CENTRO**")
    col_familia.write("**FAMILIA**")
    
    lista_act = [
        "Apatía, rechazo o indiferencia hacia las condiciones específicas.",
        "Segregación y/o exclusión en los procesos de inclusión.",
        "Sobreprotección.",
        "Bajas expectativas sobre su desarrollo y aprendizaje."
    ]
    
    for barrera in lista_act:
        c1, c2, c3, c4 = st.columns([4, 1, 1, 1])
        c1.write(f"• {barrera}")
        if c2.checkbox(" ", key=f"aula_{barrera}"): bap_seleccionadas.append(f"{barrera} (Actitudinal - Aula)")
        if c3.checkbox(" ", key=f"esc_{barrera}"): bap_seleccionadas.append(f"{barrera} (Actitudinal - Escuela)")
        if c4.checkbox(" ", key=f"fam_{barrera}"): bap_seleccionadas.append(f"{barrera} (Actitudinal - Familia)")

st.divider()

# Generación de informe
if st.button("Generar Informe Asistido por IA", type="primary"):
    if not bap_seleccionadas:
        st.warning("Selecciona al menos una BAP en las pestañas superiores.")
    else:
        with st.spinner("Procesando análisis técnico con IA..."):
            prompt = f"""
            Redacta un informe formal de Educación Especial sobre las BAP.
            Centro: {centro_escolar}, Nivel: {nivel} {grado} {grupo}.
            Docentes/Especialistas: {nombre_docentes}.
            Barreras detectadas: {', '.join(bap_seleccionadas)}.
            Estructura el informe respondiendo de forma técnica y práctica a la intervención socioeducativa.
            """
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                
                st.success("Informe generado con éxito.")
                
                col_w, col_p = st.columns(2)
                with col_w:
                    docx_file = generar_docx(response.text, "Alumno_Evaluado")
                    st.download_button("📄 Descargar Word", data=docx_file, file_name="Informe_BAP.docx")
                with col_p:
                    pdf_file = generar_pdf(response.text, "Alumno_Evaluado")
                    st.download_button("📕 Descargar PDF", data=pdf_file, file_name="Informe_BAP.pdf")
                
                st.write(response.text)
            except Exception as e:
                st.error(f"Error de conexión: {e}")
