# Importacion de Librerias 
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from st_social_media_links import SocialMediaIcons

# Agregar el logo en la parte superior izquierda
st.markdown(
    """
    <style>
    .header-container {
        display: flex;
        align-items: center;
    }
    .header-container img {
        margin-right: 20px;
    }
    .header-container h1, .header-container p {
        text-align: center;
        flex: 1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Encabezado de la Aplicacion de Streamlit con logo
st.markdown(
    """
    <div class="header-container">
        <img src="https://cdn-icons-gif.flaticon.com/17576/17576923.gif" width="50" height="50">
        <div>
            <h1>Agente de Inversiones con IA</h1>
            <p>Compara acciones en el mercado de valores con la IA de Openai</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Ingreso de la Clave API de OpenAi
openai_api_key = st.text_input("Ingresa tu clave API de OpenAI", type="password")

# Configuracion de las respuestas del asistente 
if openai_api_key:
    assistant = Assistant(llm=OpenAIChat(model="gpt-4o", api_key=openai_api_key),
                          tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
                          show_tool_calls=False)
    
    # Barra lateral para seleccionar el periodo de análisis
    periodo = st.sidebar.selectbox("Selecciona el periodo de análisis", ["1mo", "3mo", "6mo", "1y", "5y"])

    stock1 = st.text_input("Ingresa el símbolo de la primera acción")
    stock2 = st.text_input("Ingresa el símbolo de la segunda acción")
    
    if stock1 and stock2:
        # Obtener información para la primera acción
        query1 = f"Da información sobre {stock1}."
        response1 = assistant.run(query1, stream=False)
        st.write(response1)

        # Obtener datos históricos de la primera acción
        data1 = yf.download(stock1, period=periodo)

        # Obtener ratios financieros de la primera acción
        info1 = yf.Ticker(stock1).info
        pe_ratio1 = info1.get('trailingPE', 'N/A')
        pb_ratio1 = info1.get('priceToBook', 'N/A')
        dividend_yield1 = info1.get('dividendYield', 'N/A')
        debt_to_equity1 = info1.get('debtToEquity', 'N/A')

        # Mostrar ratios financieros de la primera acción en tarjetas
        st.markdown(f"### Ratios financieros clave de {stock1}")
        st.markdown(
            f"""
            <style>
            .card {{
                padding: 10px;
                border-radius: 5px;
                background-color: #f0f2f6;
                margin: 5px;
                display: inline-block;
                width: 23%;
                text-align: center;
            }}
            </style>
            <div style="display: flex; justify-content: space-around;">
                <div class="card">
                    <strong>P/E Ratio</strong><br>{pe_ratio1}
                </div>
                <div class="card">
                    <strong>P/B Ratio</strong><br>{pb_ratio1}
                </div>
                <div class="card">
                    <strong>Dividend Yield</strong><br>{dividend_yield1 if dividend_yield1 != 'N/A' else 'No aplica'}
                </div>
                <div class="card">
                    <strong>Debt-to-Equity</strong><br>{debt_to_equity1}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Crear gráfico para la primera acción
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=data1.index, y=data1['Close'], mode='lines', name=stock1))
        fig1.update_layout(title=f'Histórico de {stock1}', xaxis_title='Fecha', yaxis_title='Precio de Cierre')
        st.plotly_chart(fig1, use_container_width=True)

        # Análisis de sentimiento para la primera acción
        query_sent1 = f"¿Cuál es el sentimiento general de las noticias recientes sobre {stock1}?"
        response_sent1 = assistant.run(query_sent1, stream=False)
        st.write(f"Análisis de sentimiento para {stock1}: {response_sent1}")

        # Obtener información para la segunda acción
        query2 = f"Da información sobre {stock2}."
        response2 = assistant.run(query2, stream=False)
        st.write(response2)

        # Obtener datos históricos de la segunda acción
        data2 = yf.download(stock2, period=periodo)

        # Obtener ratios financieros de la segunda acción
        info2 = yf.Ticker(stock2).info
        pe_ratio2 = info2.get('trailingPE', 'N/A')
        pb_ratio2 = info2.get('priceToBook', 'N/A')
        dividend_yield2 = info2.get('dividendYield', 'N/A')
        debt_to_equity2 = info2.get('debtToEquity', 'N/A')

        # Mostrar ratios financieros de la segunda acción en tarjetas
        st.markdown(f"### Ratios financieros clave de {stock2}")
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-around;">
                <div class="card">
                    <strong>P/E Ratio</strong><br>{pe_ratio2}
                </div>
                <div class="card">
                    <strong>P/B Ratio</strong><br>{pb_ratio2}
                </div>
                <div class="card">
                    <strong>Dividend Yield</strong><br>{dividend_yield2 if dividend_yield2 != 'N/A' else 'No aplica'}
                </div>
                <div class="card">
                    <strong>Debt-to-Equity</strong><br>{debt_to_equity2}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Crear gráfico para la segunda acción
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=data2.index, y=data2['Close'], mode='lines', name=stock2))
        fig2.update_layout(title=f'Histórico de {stock2}', xaxis_title='Fecha', yaxis_title='Precio de Cierre')
        st.plotly_chart(fig2, use_container_width=True)

        # Análisis de sentimiento para la segunda acción
        query_sent2 = f"¿Cuál es el sentimiento general de las noticias recientes sobre {stock2}?"
        response_sent2 = assistant.run(query_sent2, stream=False)
        st.write(f"Análisis de sentimiento para {stock2}: {response_sent2}")

# Estilo para hacer la barra lateral más angosta, con fondo negro y texto blanco
st.markdown(
    """
    <style>
    /* Ajustar el ancho de la barra lateral */
    .css-1d391kg {
        width: 150px; /* Reducir el ancho a 150px */
        background-color: black; /* Fondo negro */
    }
    /* Cambiar el color de texto a blanco en la barra lateral */
    .css-1d391kg .css-1v3fvcr, 
    .css-1d391kg .css-16huue1, 
    .css-1d391kg .css-1ku1hv8, 
    .css-1d391kg .css-1sbp0i2 {
        color: white;  /* Cambiar el color del texto a blanco */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Pie de página con información del desarrollador y logos de redes sociales
st.markdown("""
---
**Desarrollador:** Edwin Quintero Alzate<br>
**Email:** egqa1975@gmail.com<br>
""")

social_media_links = [
    "https://www.facebook.com/edwin.quinteroalzate",
    "https://www.linkedin.com/in/edwinquintero0329/",
    "https://github.com/Edwin1719"]

social_media_icons = SocialMediaIcons(social_media_links)
social_media_icons.render()