import streamlit as st
import requests

# Configura la URL de tu API (ajusta según tu servidor)
API_URL = "https://appcreditrisk-production-a154.up.railway.app/capture/"
API_URL_PREDICT = "https://appcreditrisk-production-a154.up.railway.app/features/predict_and_explain/"

# Configurar navegación en la barra lateral
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a", ["Captura de Datos", "Buscar Resultados"])

if page == "Captura de Datos":
    # Página 1: Captura de datos (ya implementada)
    st.title("Formulario de Captura de Datos para Préstamos")
    st.markdown(
        """
        ### Instrucciones:
        Completa el formulario con los datos del cliente y haz clic en **Enviar datos** para registrarlos en la base de datos.
        """
    )

    # Campos del formulario
    person_age = st.number_input(
        "Edad de la persona",
        min_value=18,
        max_value=100,
        step=1,
        help="Indica la edad del solicitante. Debe ser mayor o igual a 18 años."
    )
    person_income = st.number_input(
        "Ingreso anual",
        min_value=0.0,
        step=1000.0,
        help="Especifica el ingreso anual del solicitante en su moneda local."
    )
    person_home_ownership = st.selectbox(
        "Tipo de vivienda",
        options=["RENT", "OWN", "MORTGAGE"],
        help="Selecciona el estado de propiedad de la vivienda del solicitante."
    )
    person_emp_length = st.number_input(
        "Años de empleo",
        min_value=0.0,
        step=1.0,
        help="Número de años que el solicitante ha estado empleado en su trabajo actual."
    )
    loan_intent = st.selectbox(
        "Intención del préstamo",
        options=["PERSONAL", "EDUCATION", "VENTURE", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION", "MEDICAL"],
        help="Selecciona la razón principal del préstamo."
    )
    loan_grade = st.selectbox(
        "Calificación del préstamo",
        options=["A", "B", "C", "D", "E", "F", "G"],
        help="Calificación crediticia del préstamo."
    )
    loan_amnt = st.number_input(
        "Monto del préstamo",
        min_value=0.0,
        step=1000.0,
        help="Monto total del préstamo solicitado."
    )
    loan_int_rate = st.number_input(
        "Tasa de interés (%)",
        min_value=0.0,
        step=0.1,
        help="Porcentaje de la tasa de interés del préstamo solicitado."
    )
    loan_percent_income = st.number_input(
        "Porcentaje del ingreso dedicado al préstamo",
        min_value=0.0,
        step=0.01,
        help="Proporción del ingreso mensual dedicado al préstamo."
    )
    cb_person_default_on_file = st.selectbox(
        "Historial de incumplimientos",
        options=["Y", "N"],
        help="Indica si el solicitante tiene un historial de incumplimientos registrado."
    )
    cb_person_cred_hist_length = st.number_input(
        "Longitud del historial crediticio (años)",
        min_value=0,
        step=1,
        help="Número de años que el solicitante ha tenido un historial crediticio activo."
    )

    # Botón para enviar datos
    if st.button("Enviar datos"):
        payload = {
            "person_age": person_age,
            "person_income": person_income,
            "person_home_ownership": person_home_ownership,
            "person_emp_length": person_emp_length,
            "loan_intent": loan_intent,
            "loan_grade": loan_grade,
            "loan_amnt": loan_amnt,
            "loan_int_rate": loan_int_rate,
            "loan_percent_income": loan_percent_income,
            "cb_person_default_on_file": cb_person_default_on_file,
            "cb_person_cred_hist_length": cb_person_cred_hist_length,
        }
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                st.success("Datos enviados exitosamente")
            else:
                st.error(f"Error al enviar los datos: {response.status_code}")
        except Exception as e:
            st.error(f"Error al conectar con la API: {e}")

if page == "Buscar Resultados":
    # Página: Buscar Predicción
    st.header("Buscar Resultados y Explicación")

    # Buscar cliente por ID
    client_id = st.text_input("Ingresa el ID del cliente para buscar:")

    if st.button("Buscar y Explicar"):
        if not client_id:
            st.warning("Por favor ingresa un ID válido.")
        else:
            try:
                # Llamar al endpoint de explicación
                response = requests.post(f"{API_URL_PREDICT}{client_id}")

                if response.status_code == 200:
                    result = response.json()

                    # Mostrar datos del cliente
                    st.subheader("Datos del Cliente")
                    st.json(result["client_data"])

                    # Mostrar resultado de la predicción
                    st.subheader("Resultado de la Predicción")
                    st.write(f"Predicción: {result['prediction_result']}")
                    st.write(f"Probabilidad: {result['probability']}")

                else:
                    st.error("Cliente no encontrado o error al procesar.")
            except Exception as e:
                st.error(f"Error al buscar el cliente: {e}")
