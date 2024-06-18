import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#st.title('Trastornos Mentales en el Mundo')

# Cargar datos y asegurar que la columna 'Year' sea de tipo entero
data = pd.read_csv('data_cleaned.csv')
data['Year'] = pd.to_numeric(data['Year'], errors='coerce')  # Convertir a numérico, poniendo NaN en caso de error
data = data.dropna(subset=['Year'])  # Eliminar filas con NaN en 'Year'
data['Year'] = data['Year'].astype(int)  # Convertir a enteros

# Filtrar columnas numéricas relevantes para el análisis de correlación
numeric_columns = ['Schizophrenia (%)', 'Bipolar disorder (%)', 'Eating disorders (%)', 
                   'Anxiety disorders (%)', 'Drug use disorders (%)', 'Depression (%)', 
                   'Alcohol use disorders (%)', 'Anxiety disorders (%)_scaled', 
                   'Depression (%)_scaled']

# Seleccionar solo las columnas numéricas para el análisis de correlación
data_numeric = data[numeric_columns]

# Menú lateral para seleccionar el tipo de análisis
seccion = st.sidebar.radio('Seleccione una sección', ('Información y Contexto', 'Visualizaciones Gráficas', 'Curiosidades'))

# Según la selección, mostrar los resultados
if seccion == 'Información y Contexto':
    st.header('Información y Contexto')
    st.write("""
    Dataset con información de trastornos mentales.
    """)
    st.dataframe(data.head())
    # Título
    st.header('Variables del Dataset')

    # Lista de variables con descripciones
    variables_info = """
    - **Entidad:** Identificador único para cada país o región incluido en el conjunto de datos.
    - **Código:** Código único asociado con una Entidad/País o región incluido en el conjunto de datos.
    - **Año:** Año en que se recopilaron los datos sobre esa Entidad/País en particular.
    - **Esquizofrenia(%):** Porcentaje de personas con esquizofrenia en ese país/región durante ese año.
    - **Trastorno bipolar(%):** Porcentaje de personas con trastorno bipolar en ese país/región durante ese año.
    - **Trastornos alimentarios(%):** Porcentaje de personas con trastornos alimentarios en ese país/región durante ese año.
    - **Trastornos de ansiedad(%):** Porcentaje de personas con trastornos de ansiedad en ese país/región durante ese año.
    - **Trastornos por uso de drogas(%):** Porcentaje de personas con trastornos por uso de drogas en ese país/región durante ese año.
    - **Depresión(%):** Porcentaje de personas con depresión en ese país/región durante ese año.
    - **Trastornos por uso de alcohol(%):** Porcentaje de personas con trastornos por uso de alcohol en ese país/región durante ese año.
    """

    # Mostrar la información utilizando markdown
    st.markdown(variables_info)
elif seccion == 'Visualizaciones Gráficas':
    st.header('Visualizaciones Gráficas')
    # Título de la aplicación
    st.header('Prevalencia de Trastornos Mentales en el Mundo')

    # Lista de opciones para el usuario
    options = {
        'Depresión': 'Depression (%)_scaled',
        'Esquizofrenia': 'Schizophrenia (%)',
        'Trastorno Bipolar': 'Bipolar disorder (%)',
        'Trastornos Alimenticios': 'Eating disorders (%)',
        'Trastornos de Ansiedad': 'Anxiety disorders (%)_scaled',
        'Trastornos por Uso de Drogas': 'Drug use disorders (%)',
        'Trastornos por Uso de Alcohol': 'Alcohol use disorders (%)'
    }

    # Selección de enfermedad
    selected_option = st.selectbox('Seleccione la enfermedad', list(options.keys()))

    # Selección de color
    color = st.color_picker('Seleccione el color para la gráfica', '#3498db')

    # Filtrar y calcular top 10 países
    selected_column = options[selected_option]
    top_countries = data.groupby('Entity')[selected_column].mean().nlargest(10).index
    filtered_data = data[data['Entity'].isin(top_countries)]

    # Crear gráfico de barras
    plt.figure(figsize=(12, 8))
    sns.barplot(x=selected_column, y='Entity', data=filtered_data, ci=None, color=color)
    plt.title(f'Top 10 Países con Mayor Prevalencia de {selected_option}')
    plt.xlabel('Prevalencia Escalada')
    plt.ylabel('País')

    # Mostrar gráfico en Streamlit
    st.pyplot(plt)

    # Título de la nueva sección
    st.header('Evolución Temporal de Trastornos Mentales')

    # Selección de país y periodo de tiempo
    selected_country = st.selectbox('Seleccione el país', data['Entity'].unique())
    start_year, end_year = st.slider('Seleccione el periodo de tiempo', 
                                    2005, 
                                    int(data['Year'].max()), 
                                    (2005, int(data['Year'].max())))

    # Filtrar datos por país y periodo de tiempo
    filtered_time_data = data[(data['Entity'] == selected_country) & 
                            (data['Year'] >= start_year) & 
                            (data['Year'] <= end_year)]

    # Asegurarse de seleccionar solo columnas numéricas para calcular la media
    numeric_columns = filtered_time_data.select_dtypes(include='number').columns
    yearly_mean_data = filtered_time_data.groupby('Year')[numeric_columns].mean()

    # Crear gráfico de línea
    plt.figure(figsize=(10, 6))
    plt.plot(yearly_mean_data.index, yearly_mean_data[selected_column], marker='o', linestyle='-', color=color)
    plt.title(f'Evolución de {selected_option} en {selected_country} ({start_year}-{end_year})')
    plt.xlabel('Año')
    plt.ylabel(f'Tasa de {selected_option} (%)')
    plt.grid(True)
    plt.xticks(yearly_mean_data.index, rotation=45)
    plt.tight_layout()

    # Mostrar gráfico en Streamlit
    st.pyplot(plt)

    # Título de la aplicación
    st.header('Prevalencia de Trastornos Mentales en el Mundo')

    # Lista de opciones para el usuario
    options = {
        'Depresión': 'Depression (%)_scaled',
        'Esquizofrenia': 'Schizophrenia (%)',
        'Trastorno Bipolar': 'Bipolar disorder (%)',
        'Trastornos Alimenticios': 'Eating disorders (%)',
        'Trastornos de Ansiedad': 'Anxiety disorders (%)_scaled',
        'Trastornos por Uso de Drogas': 'Drug use disorders (%)',
        'Trastornos por Uso de Alcohol': 'Alcohol use disorders (%)'
    }

    # Selección de trastornos mentales para el gráfico tipo tarta
    selected_options = st.multiselect('Seleccione los trastornos mentales', list(options.keys()))

    # Obtener los top 10 países con mayor prevalencia promedio para cada trastorno seleccionado
    prevalences = {}
    for option in selected_options:
        column_name = options[option]
        top_countries = data.groupby('Entity')[column_name].mean().nlargest(10).index
        filtered_data = data[data['Entity'].isin(top_countries)]
        mean_prevalence = filtered_data.groupby('Entity')[column_name].mean()
        prevalences[option] = mean_prevalence

    # Crear gráfico tipo tarta para cada trastorno seleccionado
    for option, prevalence_data in prevalences.items():
        plt.figure(figsize=(8, 8))
        plt.pie(prevalence_data, labels=prevalence_data.index, autopct='%1.1f%%', startangle=140)
        plt.title(f'Prevalencia Promedio de {option} en los Top 10 Países')
        st.pyplot(plt)

    # Título de la aplicación
    st.header('Relación entre Prevalencia de Trastornos Mentales y Factores Socioeconómicos')

    # Crear un heatmap para visualizar correlaciones entre variables seleccionadas
    correlation_matrix = data_numeric.corr()
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Correlación entre Prevalencia de Trastornos Mentales y Factores Socioeconómicos')
    plt.tight_layout()

    # Mostrar heatmap en Streamlit
    st.pyplot(plt)

elif seccion == 'Curiosidades':
    st.title('Curiosidades sobre Trastornos Mentales')
    st.write("""
    Aquí puedes encontrar datos interesantes o curiosidades relacionadas con los trastornos mentales y el dataset.
    """)
    # Agregar una imagen desde un archivo local
    st.image('salud-mental.jpg', caption='', use_column_width=True)

    st.header(f"Correlaciones entre trastornos mentales")
    # Análisis de las correlaciones
    st.markdown("""
    ### Análisis y conclusiones:

    - **Esquizofrenia y Trastorno Bipolar**: Existe una correlación moderada positiva entre esquizofrenia y trastorno bipolar (coeficiente de correlación cercano a 0.5).
    
    - **Depresión y Trastornos de Ansiedad**: Se observa una fuerte correlación positiva entre depresión y trastornos de ansiedad (coeficiente superior a 0.7).

    - **Uso de Drogas y Uso de Alcohol**: Hay una correlación significativa entre trastornos por uso de drogas y trastornos por uso de alcohol (coeficiente aproximado de 0.6).

    Estas correlaciones sugieren que ciertos trastornos mentales pueden coexistir o influirse mutuamente en diferentes poblaciones.
    """)







