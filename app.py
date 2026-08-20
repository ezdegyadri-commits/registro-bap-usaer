import streamlit as st
from google import genai
from docx import Document
from fpdf import FPDF
import io
from datetime import date

# 1. Configuración de la API con tu clave válida
client = genai.Client(api_key="AQ.Ab8RN6JM_YMzUguhKme19dTI9laFp2pEaKDzojA5eEQR6nqrRw")

st.set_page_config(page_title="Instrumento de Registro BAP", page_icon="📝", layout="wide")

# --- ESTILOS CSS ---
st.markdown("""
<style>
    .caja-datos { background-color: #F6F1E9; border: 2px solid #C4A462; border-radius: 15px; padding: 25px; margin-bottom: 20px; color: #333333; }
    .caja-instrucciones { border: 2px solid #2B5B41; padding: 20px; margin-bottom: 20px; background-color: #ffffff; color: #333333; }
    .titulo-seccion { color: #2B5B41; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- FUNCIONES DE EXPORTACIÓN ---
def generar_docx(texto_informe, alumno):
    doc = Document()
    doc.add_heading('Informe de Análisis y Estrategias BAP', 0)
    doc.add_heading(f'Alumno(a): {alumno}', 1)
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

# --- ENCABEZADO ---
st.title("Instrumento de registro de las barreras para el aprendizaje y la participación")

# --- DATOS GENERALES ---
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
nombre_alumno = st.text_input("Nombre de la o el estudiante (NNAJ):")
nombre_docentes = st.text_area("Nombre y función del equipo itinerante, docentes y agentes educativos:")
fecha_eval = st.date_input("Fecha:", value=date.today())
st.markdown('</div>', unsafe_allow_html=True)

# --- CLASIFICACIÓN DE BARRERAS (Checkboxes) ---
st.markdown("<h3 class='titulo-seccion'>1. Clasificación de Barreras</h3>", unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["Estructurales", "Normativas", "Didácticas", "Actitudinales"])

bap_seleccionadas = []

with tab1:
    st.write("**Estructurales: Normalizan la exclusión**")
    if st.checkbox("Falta de recursos humanos, materiales, apoyos, capacitación."): bap_seleccionadas.append("Falta de recursos o capacitación (Estructural)")
    if st.checkbox("Infraestructura inadecuada (escolar o aula), falta de rampas, accesos."): bap_seleccionadas.append("Infraestructura inadecuada (Estructural)")
    if st.checkbox("Invisibilizar e ignorar la presencia de NNAJ por su condición."): bap_seleccionadas.append("Invisibilización de NNAJ (Estructural)")

with tab2:
    st.write("**Normativas: Impedimentos desde la Ley, norma o disposición.**")
    if st.checkbox("Desconocimiento de los documentos normativos de inclusión."): bap_seleccionadas.append("Desconocimiento normativo (Normativa)")
    if st.checkbox("Falta de un Programa Analítico contextualizado a la diversidad."): bap_seleccionadas.append("Falta de contextualización en el Programa Analítico (Normativa)")
    if st.checkbox("Procesos de gestión excluyentes, descontextualizados, segregatorios."): bap_seleccionadas.append("Gestión excluyente (Normativa)")

with tab3:
    st.write("**Didácticas: Métodos de enseñanza y evaluación no acordes.**")
    if st.checkbox("Práctica docente homogeneizada sin considerar la diversidad."): bap_seleccionadas.append("Práctica homogeneizada (Didáctica)")
    if st.checkbox("Ausencia de Ajustes Razonables (AR) acordes a la condición."): bap_seleccionadas.append("Ausencia de Ajustes Razonables (Didáctica)")
    if st.checkbox("Mecanismos de evaluación homogéneos sin considerar capacidades."): bap_seleccionadas.append("Evaluación homogénea (Didáctica)")

with tab4:
    st.write("**Actitudinales: Relacionadas con interacciones y concepciones sociales.**")
    c_desc, c_aula, c_esc, c_fam = st.columns([4, 1, 1, 1])
    c_desc.write("**Condición observada**"); c_aula.write("**AULA**"); c_esc.write("**ESCUELA**"); c_fam.write("**FAMILIA**")
    
    actitudinales = ["Apatía, rechazo o indiferencia.", "Sobreprotección.", "Bajas expectativas sobre su aprendizaje.", "Acoso y/o bullying."]
    for barrera in actitudinales:
        c1, c2, c3, c4 = st.columns([4, 1, 1, 1])
        c1.write(f"• {barrera}")
        if c2.checkbox(" ", key=f"a_{barrera}"): bap_seleccionadas.append(f"{barrera} (Aula)")
        if c3.checkbox(" ", key=f"e_{barrera}"): bap_seleccionadas.append(f"{barrera} (Escuela)")
        if c4.checkbox(" ", key=f"f_{barrera}"): bap_seleccionadas.append(f"{barrera} (Familia)")

st.divider()

# --- MÓDULO DE INTERPRETACIÓN CUALITATIVA ---
st.markdown("<h3 class='titulo-seccion'>2. Interpretación y Estrategias (Preguntas Guía)</h3>", unsafe_allow_html=True)
st.info("💡 Responde brevemente lo que aplique. El modelo de Inteligencia Artificial procesará estas ideas para redactar un informe profesional.")

with st.expander("Desplegar formulario de análisis cualitativo", expanded=True):
    col_preg1, col_preg2 = st.columns(2)
    
    with col_preg1:
        q1 = st.text_input("1. ¿En qué contextos están enfrentando BAP?")
        q2 = st.text_input("2. ¿Quiénes son los agentes que las están generando?")
        q4 = st.text_input("4. Priorización: ¿Con cuáles BAP empezar la intervención?")
        q5 = st.text_area("5. ¿Se minimizan desde el aula o necesitan plan complementario?")
        
    with col_preg2:
        q6 = st.text_area("6. ¿Cuáles son las posibles estrategias a realizar?")
        q7 = st.text_input("7. Responsabilidades de cada integrante del colectivo:")
        q8 = st.text_input("8. ¿En qué plazo se realizarán las acciones?")
        q9 = st.text_input("9. ¿Cómo aportarán estas acciones a la inclusión?")
    
    q10 = st.text_area("10. Cualquier otro dato que aporte a la interpretación y establecimiento de acciones:")

st.divider()

# --- GENERACIÓN DE INFORME IA ---
if st.button("✨ Generar Informe Potenciado por IA", type="primary"):
    if not bap_seleccionadas and not q1:
        st.warning("Selecciona al menos una barrera o responde alguna pregunta de la guía antes de generar.")
    else:
        with st.spinner("Procesando análisis técnico con base en las respuestas del docente..."):
            
            # Construcción del prompt uniendo los checkboxes con el análisis del especialista
            prompt = f"""
            Actúa como un experto en Educación Especial y redacta el "Informe de las BAP que enfrentan niñas, niños, adolescentes y jóvenes".
            
            DATOS DE IDENTIFICACIÓN:
            Alumno: {nombre_alumno} ({nivel} {grado} {grupo}, {centro_escolar})
            Equipo a cargo: {nombre_docentes}
            
            1. BARRERAS DETECTADAS (Checkboxes):
            {', '.join(bap_seleccionadas) if bap_seleccionadas else 'No se marcaron casillas específicas.'}
            
            2. ANÁLISIS CUALITATIVO DEL DOCENTE (Usa esta información como la base central de la propuesta estratégica):
            - Contextos: {q1}
            - Personas que generan BAP: {q2}
            - Priorización de intervención: {q4}
            - Alcance (Aula vs Complementario): {q5}
            - Estrategias propuestas: {q6}
            - Responsabilidades del colectivo: {q7}
            - Plazos de acción: {q8}
            - Aportación a la inclusión: {q9}
            - Datos extra relevantes: {q10}
            
            REGLAS DE REDACCIÓN:
            Integra ambos apartados en un documento narrativo, profesional, formal y pedagógico, sin que parezca un formato de preguntas y respuestas. Usa títulos y viñetas para estructurar el plan de intervención. Si alguna pregunta cualitativa quedó vacía, no la menciones, deduce la estrategia con base en las barreras marcadas.
            """
            
            try:
                # Modifica el nombre del modelo (gemini-3.6-flash / gemini-1.5-flash) según la versión activa de tu API
                response = client.models.generate_content(
                    model="gemini-3.6-flash", 
                    contents=prompt
                )
                
                st.success("¡Informe técnico redactado con éxito!")
                
                col_w, col_p = st.columns(2)
                with col_w:
                    docx_file = generar_docx(response.text, nombre_alumno)
                    st.download_button("📄 Descargar Word", data=docx_file, file_name=f"Informe_BAP_{nombre_alumno}.docx")
                with col_p:
                    pdf_file = generar_pdf(response.text, nombre_alumno)
                    st.download_button("📕 Descargar PDF", data=pdf_file, file_name=f"Informe_BAP_{nombre_alumno}.pdf")
                
                with st.expander("Ver borrador del informe", expanded=True):
                    st.write(response.text)
                    
            except Exception as e:
                st.error(f"Error de conexión con la IA: {e}")
