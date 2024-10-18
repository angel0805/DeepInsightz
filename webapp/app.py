import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import lightgbm as lgb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_absolute_error, mean_squared_error
from joblib import dump, load
from utils import recomienda_tf
import requests

# Page configuration
st.set_page_config(page_title="DeepInsightz", page_icon=":bar_chart:", layout="wide")

# Custom CSS for dynamic theme styling
# Streamlit detects light and dark mode automatically via the user's settings in Hugging Face Spaces
if st.get_option("theme.base") == "dark":
    background_color = "#282828"
    text_color = "white"
    metric_box_color = "#4f4f4f"
    sidebar_color = "#282828"
    plot_bgcolor = "rgba(0, 0, 0, 0)"
    primary_color = '#00FF00'  # for positive delta
    negative_color = '#FF0000'  # for negative delta
else:
    background_color = "#f4f4f4"
    text_color = "#black"
    metric_box_color = "#dee2e8"
    sidebar_color = "#dee2e8"
    plot_bgcolor = "#f4f4f4"
    primary_color = '#228B22'  # for positive delta in light mode
    negative_color = '#8B0000'  # for negative delta in light mode

st.markdown(f"""
    <style>
    body {{
        background-color: {background_color};
        color: {text_color};
    }}
    [data-testid="stMetric"] {{
        background-color: {metric_box_color};
        border-radius: 10px;
        text-align: center;
        padding: 15px 0;
        margin-bottom: 20px;
    }}
    [data-testid="stMetricLabel"] {{
        display: flex;
        justify-content: center;
        align-items: center;
        color: {text_color};
    }}
    [data-testid="stSidebar"] {{
        background-color: {sidebar_color};
    }}
    </style>
""", unsafe_allow_html=True)

# Load CSV files at the top
df = pd.read_csv("df_clean.csv")
nombres_proveedores = pd.read_csv("nombres_proveedores.csv", sep=';')
euros_proveedor = pd.read_csv("euros_proveedor.csv", sep=',')
ventas_clientes = pd.read_csv("ventas_clientes.csv", sep=',')
customer_clusters = pd.read_csv('predicts/customer_clusters.csv')  # Load the customer clusters here
df_agg_2024 = pd.read_csv('predicts/df_agg_2024.csv')
pca_data_5 = pd.read_csv('pca_data.csv')
historical_data = pd.read_csv('historical_data.csv')


with st.sidebar:
    st.image("logo/logo.png", use_column_width=True)
    page = st.sidebar.selectbox("Selecciona la herramienta que quieres utilizar...", ["📃 Resumen", "🕵️ Análisis de Cliente", "💡 Recomendación de Artículos"])

# Generamos la columna total_sales
ventas_clientes['total_sales'] = ventas_clientes[['VENTA_2021', 'VENTA_2022', 'VENTA_2023']].sum(axis=1)
ventas_clientes_3 = ventas_clientes
ventas_clientes_3['total_sales'] = ventas_clientes['total_sales'] / 3
# Ordenar los clientes de mayor a menor según sus ventas totales
ventas_top_100 = ventas_clientes.sort_values(by='total_sales', ascending=False).head(100)
ventas_top_100['total_sales'] = ventas_top_100['total_sales'] / 3


# Ensure customer codes are strings
df['CLIENTE'] = df['CLIENTE'].astype(str)
nombres_proveedores['codigo'] = nombres_proveedores['codigo'].astype(str)
euros_proveedor['CLIENTE'] = euros_proveedor['CLIENTE'].astype(str)
customer_clusters['cliente_id'] = customer_clusters['cliente_id'].astype(str)  # Ensure customer IDs are strings
fieles_df = pd.read_csv("clientes_relevantes.csv")
cestas = pd.read_csv("cestas.csv")
productos = pd.read_csv("productos.csv")
df_agg_2024['cliente_id'] = df_agg_2024['cliente_id'].astype(str)
marca_id_mapping = load('marca_id_mapping.joblib')

# Convert all columns except 'CLIENTE' to float in euros_proveedor
for col in euros_proveedor.columns:
    if col != 'CLIENTE':
        euros_proveedor[col] = pd.to_numeric(euros_proveedor[col], errors='coerce')

# Check for NaN values after conversion
if euros_proveedor.isna().any().any():
    st.warning("Some values in euros_proveedor couldn't be converted to numbers. Please review the input data.")

# Ignore the last two columns of df
df = df.iloc[:, :-2]

# Function to get supplier name
def get_supplier_name(code):
    code = str(code)  # Ensure code is a string
    name = nombres_proveedores[nombres_proveedores['codigo'] == code]['nombre'].values
    return name[0] if len(name) > 0 else code

def image_exists(url):
    """Verifica si la imagen existe en la URL proporcionada"""
    response = requests.head(url)
    return response.status_code == 200

def get_supplier_name_encoded(encoded_code):
    try:
        # Ensure the encoded code is an integer
        encoded_code = int(encoded_code)
        print(f"Encoded Code: {encoded_code}")

        # Use the label encoder to map the encoded code back to the original manufacturer code
        if encoded_code < len(marca_id_mapping.classes_):
            real_code = marca_id_mapping.inverse_transform([encoded_code])[0]
            print(f"Real Manufacturer Code: {real_code}")
        else:
            print(f"Encoded code not found in the label encoder: {encoded_code}")
            return f"Unknown code: {encoded_code}"  # Handle case where encoded code is not found

        # Now, use the real_code to find the manufacturer name in nombres_proveedores
        name = nombres_proveedores[nombres_proveedores['codigo'] == str(real_code)]['nombre'].values
        print(f"Manufacturer Name Found: {name}")  # Check what name is returned

        # Return the manufacturer name if found, otherwise return the real_code
        return name[0] if len(name) > 0 else real_code

    except Exception as e:
        print(f"Error encountered: {e}")
        return f"Error for code: {encoded_code}"

# Custom Donut Chart with Plotly for Inbound/Outbound Percentage
def create_donut_chart(values, labels, color_scheme, title):
    fig = px.pie(
        values=values, 
        names=labels, 
        hole=0.7,
        color_discrete_sequence=color_scheme
    )
    fig.update_traces(textinfo='percent+label', hoverinfo='label+percent', textposition='inside', showlegend=False)
    fig.update_layout(
        annotations=[dict(text=f"{int(values[1])}%", x=0.5, y=0.5, font_size=40, showarrow=False)],
        title=title,
        height=300,
        margin=dict(t=30, b=10, l=10, r=10),
        paper_bgcolor=plot_bgcolor,  # Use theme-dependent background color
        plot_bgcolor=plot_bgcolor
    )
    return fig

# Donut chart with color scheme based on theme
if st.get_option("theme.base") == "dark":
    donut_color_scheme = ['#155F7A', '#29b5e8']  # Dark mode colors
else:
    donut_color_scheme = ['#007BFF', '#66b5ff']  # Light mode colors

# Function to create radar chart with square root transformation
def radar_chart(categories, values, amounts, title):
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(projection='polar'))
    
    # Apply square root transformation
    sqrt_values = np.sqrt(values)
    sqrt_amounts = np.sqrt(amounts)
    
    max_sqrt_value = max(sqrt_values)
    normalized_values = [v / max_sqrt_value for v in sqrt_values]
    
    # Adjust scaling for spend values
    max_sqrt_amount = max(sqrt_amounts)
    scaling_factor = 0.7  # Adjust this value to control how much the spend values are scaled up
    normalized_amounts = [min((a / max_sqrt_amount) * scaling_factor, 1.0) for a in sqrt_amounts]
    
    normalized_values += normalized_values[:1]
    ax.plot(angles, normalized_values, 'o-', linewidth=2, color='#FF69B4', label='% Units (sqrt)')
    ax.fill(angles, normalized_values, alpha=0.25, color='#FF69B4')
    
    normalized_amounts += normalized_amounts[:1]
    ax.plot(angles, normalized_amounts, 'o-', linewidth=2, color='#4B0082', label='% Spend (sqrt)')
    ax.fill(angles, normalized_amounts, alpha=0.25, color='#4B0082')
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=8, wrap=True)
    ax.set_ylim(0, 1)
    
    circles = np.linspace(0, 1, 5)
    for circle in circles:
        ax.plot(angles, [circle]*len(angles), '--', color='gray', alpha=0.3, linewidth=0.5)
    
    ax.set_yticklabels([])
    ax.spines['polar'].set_visible(False)
    
    plt.title(title, size=16, y=1.1)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    
    return fig



if page == "📃 Resumen":
    # st.title("Welcome to DeepInsightz")
    # st.markdown("""
    #     ### Data-driven Customer Clustering
    #     We analyzed thousands of customers and suppliers to help businesses make smarter sales decisions.
    # """)

    # Create layout with three columns
    col1, col2, col3 = st.columns((1.5, 4, 2.5), gap='medium')

    # Left Column (Red): Metrics and Donut Charts
    with col1:
        st.markdown('#### Información General')
        st.metric(label="Rango de fechas", value="2021-2023")
        st.metric(label="Clientes analizados", value="3.000")
        st.metric(label="Productos únicos vendidos", value="10.702")
        st.metric(label="Líneas de venta totales", value="764.396")
        


    # Middle Column (White): 3D Cluster Model and Bar Chart
    with col2:
        st.markdown('#### Cluster de Clientes 3D')

        # Create 3D PCA plot using actual data from pca_data_5
        fig_cluster = px.scatter_3d(
            pca_data_5, 
            x='PC1', 
            y='PC2', 
            z='PC3', 
            color='cluster_id', 
            hover_name='CustomerID',
            color_continuous_scale='Turbo'
        )
        fig_cluster.update_layout(
            scene=dict(aspectratio=dict(x=1, y=1, z=0.8)),  # Adjusted aspect ratio for better balance
            margin=dict(t=10, b=10, l=10, r=10),  # Tighten margins further
            height=600,  # Slightly increased height for better visibility
        )
        st.plotly_chart(fig_cluster, use_container_width=True)
    
    # Right Column (Blue): Key Metrics Overview and Data Preparation Summary
    with col3:
        # Mostrar la tabla con los 100 mejores clientes
        st.markdown('#### Top 100 Clientes')

        # Configurar columnas para mostrar los clientes y las ventas totales
        st.dataframe(ventas_top_100[['codigo_cliente', 'total_sales']],
                    column_order=("codigo_cliente", "total_sales"),
                    hide_index=True,
                    width=350,  # Ajustar el ancho de la tabla
                    height=400,  # Ajustar la altura de la tabla
                    column_config={
                        "codigo_cliente": st.column_config.TextColumn(
                            "Código de Cliente",
                        ),
                        "total_sales": st.column_config.ProgressColumn(
                            "Venta Total (€)",
                            format="%d",
                            min_value=0,
                            max_value=ventas_top_100['total_sales'].max()
                        )}
                    )
        # Calculate sales insights
        sales_min = ventas_clientes[ventas_clientes['total_sales'] > 0]['total_sales'].min()
        sales_max = ventas_clientes['total_sales'].max()
        sales_median = ventas_clientes['total_sales'].median()
        sales_90th = ventas_clientes['total_sales'].quantile(0.9)
        sales_10th = ventas_clientes['total_sales'].quantile(0.1)

        # About Section with relevant data insights
        with st.expander('Clientes al detalle', expanded=True):
            st.write(f'''
                - **Venta Mediana**: €{sales_median:,.0f} .
                - **Percentil 90**: €{sales_90th:,.0f}.
                - **Percentil 10**: €{sales_10th:,.0f}.
            ''')
# Customer Analysis Page
elif page == "🕵️ Análisis de Cliente":
    st.markdown("""
    <h2 style='text-align: center; font-size: 2.5rem;'>Análisis de Cliente</h2>
    <p style='text-align: center; font-size: 1.2rem; color: gray;'> 
    Introduce el código del cliente para explorar información detallada del mismo, incluyendo ventas anteriores, predicciones para el año actual e información específica por fabricante.
    </p>
    """, unsafe_allow_html=True)

    # Combine text input and dropdown into a single searchable selectbox
    customer_code = st.selectbox(
        "Escribe o selecciona el código de tu cliente",
        df['CLIENTE'].unique(),  # All customer codes

        format_func=lambda x: str(x),  # Ensures the values are displayed as strings
        help="Start typing to search for a specific customer code"
    )

    if st.button("Calcular"):
        if customer_code:
            with st.spinner("Estamos identificando el grupo del cliente..."):
                # Find Customer's Cluster
                customer_match = customer_clusters[customer_clusters['cliente_id'] == customer_code]
                time.sleep(1)
                
                if not customer_match.empty:
                    cluster = customer_match['cluster_id'].values[0]
                
            with st.spinner(f"Seleccionando el modelo predictivo..."):
                # Load the Corresponding Model
                model_path = f'models/modelo_cluster_{cluster}.txt'
                gbm = lgb.Booster(model_file=model_path)

            with st.spinner("Preparando los datos..."):
                # Load predict data for that cluster
                predict_data = pd.read_csv(f'predicts/predict_cluster_{cluster}.csv')
                
                # Convert cliente_id to string
                predict_data['cliente_id'] = predict_data['cliente_id'].astype(str)

            with st.spinner("Filtrando data..."):
                # Filter for the specific customer
                customer_code_str = str(customer_code)
                customer_data = predict_data[predict_data['cliente_id'] == customer_code_str]

            with st.spinner("Geneerando predicciones de venta..."):
                if not customer_data.empty:
                    # Define features consistently with the training process
                    lag_features = [f'precio_total_lag_{lag}' for lag in range(1, 25)]
                    features = lag_features + ['mes', 'marca_id_encoded', 'año', 'cluster_id']
    
                    # Prepare data for prediction
                    X_predict = customer_data[features]

                    # Convert categorical features to 'category' dtype
                    categorical_features = ['mes', 'marca_id_encoded', 'cluster_id']
                    for feature in categorical_features:
                        X_predict[feature] = X_predict[feature].astype('category')
                    
                    # Make Prediction for the selected customer
                    y_pred = gbm.predict(X_predict, num_iteration=gbm.best_iteration)

                    # Reassemble the results
                    results = customer_data[['cliente_id', 'marca_id_encoded', 'fecha_mes']].copy()
                    results['ventas_predichas'] = y_pred

                    # Load actual data from df_agg_2024
                    actual_sales = df_agg_2024[df_agg_2024['cliente_id'] == customer_code_str]
                    
                    if not actual_sales.empty:
                        # Merge predictions with actual sales
                        results = results.merge(actual_sales[['cliente_id', 'marca_id_encoded', 'fecha_mes', 'precio_total']], 
                                                on=['cliente_id', 'marca_id_encoded', 'fecha_mes'], 
                                                how='left')
                        results.rename(columns={'precio_total': 'ventas_reales'}, inplace=True)
                    else:
                        # If no actual sales data for 2024, fill 'ventas_reales' with 0
                        results['ventas_reales'] = 0

                    # Ensure any missing sales data is filled with 0
                    results['ventas_reales'].fillna(0, inplace=True)

                    # Define the cutoff date for the last 12 months
                    fecha_inicio = pd.to_datetime("2023-01-01")
                    fecha_corte = pd.to_datetime("2024-09-01")

                    # Convertir fecha_mes a datetime en el DataFrame historical_data
                    historical_data['fecha_mes'] = pd.to_datetime(historical_data['fecha_mes'], errors='coerce')

                    # Ensure cliente_id is of type string and strip any leading/trailing whitespace
                    historical_data['cliente_id'] = historical_data['cliente_id'].astype(str).str.strip()
                    customer_code_str = str(customer_code).strip()  # Ensure the customer code is also properly formatted

                    filtered_historical_data = historical_data[historical_data['cliente_id'] == customer_code_str]


                    # Filtrar los datos históricos por cliente y por el rango de fechas (2023)
                    fecha_inicio_2023 = pd.to_datetime("2023-01-01")
                    fecha_fin_2023 = pd.to_datetime("2023-12-31")

                    datos_historicos = historical_data[
                        (historical_data['cliente_id'] == customer_code_str) &
                        (historical_data['fecha_mes'] >= fecha_inicio_2023) &
                        (historical_data['fecha_mes'] <= fecha_fin_2023)
                    ].groupby('fecha_mes')['precio_total'].sum().reset_index()

                    # Renombrar la columna 'precio_total' a 'ventas_historicas' si no está vacía
                    if not datos_historicos.empty:
                        datos_historicos.rename(columns={'precio_total': 'ventas_historicas'}, inplace=True)
                    else:
                        # Si los datos históricos están vacíos, generar fechas de 2023 con ventas_historicas = 0
                        fechas_2023 = pd.date_range(start='2023-01-01', end='2023-12-31', freq='M')
                        datos_historicos = pd.DataFrame({'fecha_mes': fechas_2023, 'ventas_historicas': [0] * len(fechas_2023)})

                    # Filtrar los datos de predicciones y ventas reales para 2024
                    datos_cliente_total = results.groupby('fecha_mes').agg({
                        'ventas_reales': 'sum',
                        'ventas_predichas': 'sum'
                    }).reset_index()

                    # Asegurarnos de que fecha_mes en datos_cliente_total es datetime
                    datos_cliente_total['fecha_mes'] = pd.to_datetime(datos_cliente_total['fecha_mes'], errors='coerce')

                    # Generar un rango de fechas para 2024 si no hay predicciones
                    fechas_2024 = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
                    fechas_df_2024 = pd.DataFrame({'fecha_mes': fechas_2024})

                    # Asegurarnos de que fecha_mes en fechas_df_2024 es datetime
                    fechas_df_2024['fecha_mes'] = pd.to_datetime(fechas_df_2024['fecha_mes'], errors='coerce')

                    # Combinar datos históricos con predicciones y ventas reales usando un merge
                    # Usamos how='outer' para asegurarnos de incluir todas las fechas de 2023 y 2024
                    datos_combinados = pd.merge(datos_historicos, datos_cliente_total, on='fecha_mes', how='outer').sort_values('fecha_mes')

                    # Rellenar los NaN: 0 en ventas_historicas donde faltan predicciones, y viceversa
                    datos_combinados['ventas_historicas'].fillna(0, inplace=True)
                    datos_combinados['ventas_predichas'].fillna(0, inplace=True)
                    datos_combinados['ventas_reales'].fillna(0, inplace=True)

                    # Crear la gráfica con Plotly
                    fig = go.Figure()

                    # Graficar ventas históricas
                    fig.add_trace(go.Scatter(
                        x=datos_combinados['fecha_mes'], 
                        y=datos_combinados['ventas_historicas'], 
                        mode='lines+markers', 
                        name='Ventas Históricas', 
                        line=dict(color='blue')
                    ))

                    # Graficar ventas predichas
                    fig.add_trace(go.Scatter(
                        x=datos_combinados['fecha_mes'], 
                        y=datos_combinados['ventas_predichas'], 
                        mode='lines+markers', 
                        name='Ventas Predichas', 
                        line=dict(color='orange')
                    ))

                    # Graficar ventas reales
                    fig.add_trace(go.Scatter(
                        x=datos_combinados['fecha_mes'], 
                        y=datos_combinados['ventas_reales'], 
                        mode='lines+markers', 
                        name='Ventas Reales', 
                        line=dict(color='green')
                    ))

                    # Personalizar el layout para enfocarse en 2023 y 2024
                    fig.update_layout(
                        title=f"Ventas Históricas, Predichas y Reales para Cliente {customer_code}",
                        xaxis_title="Fecha",
                        yaxis_title="Ventas (€)",
                        height=600,
                        xaxis_range=[fecha_inicio_2023, pd.to_datetime("2024-09-30")],  # Ajustar el rango del eje x a 2023-2024
                        legend_title="Tipo de Ventas",
                        hovermode="x unified"
                    )

                    # Mostrar la gráfica en Streamlit
                    st.plotly_chart(fig)

                    # Calculate metrics for 2024 data
                    datos_2024 = datos_combinados[datos_combinados['fecha_mes'].dt.year == 2024]
                    actual = datos_2024['ventas_reales']
                    predicted = datos_2024['ventas_predichas']

                    def calculate_mape(y_true, y_pred):
                        mask = y_true != 0
                        return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

                    mae = mean_absolute_error(actual, predicted)
                    mse = mean_squared_error(actual, predicted)
                    rmse = np.sqrt(mse)
                    mape = calculate_mape(actual, predicted)
                    smape = np.mean(2 * np.abs(actual - predicted) / (np.abs(actual) + np.abs(predicted))) * 100

                    # Display metrics
                    st.subheader("Métricas de Predicción (2024)")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("MAE", f"{mae:.2f} €",help="Promedio de la diferencia absoluta entre las predicciones y los valores reales.")
                    col2.metric("MAPE", f"{mape:.2f}%",help="Porcentaje promedio de error en las predicciones.")
                    col3.metric("RMSE", f"{rmse:.2f} €",help="Medida de la desviación estándar de los residuos de predicción.")
                    col4.metric("SMAPE", f"{smape:.2f}%",help="Alternativa al MAPE que maneja mejor los valores cercanos a cero.")


                    # Split space into two columns
                    col1, col2 = st.columns(2)

                    # Column 1: Radar chart for top manufacturers
                    with col1:
                        st.subheader("¡Esto tiene buena pinta!")
                        st.info("Su cliente ha superado las ventas predichas de las siguientes marcas:")

                        # Group results by manufacturer to calculate the total predicted and actual sales
                        grouped_results = results.groupby('marca_id_encoded').agg({
                            'ventas_reales': 'sum',
                            'ventas_predichas': 'sum'
                        }).reset_index()

                        # Identify manufacturers that exceeded predicted sales
                        overperforming_manufacturers = grouped_results[grouped_results['ventas_reales'] > grouped_results['ventas_predichas']].copy()

                        if not overperforming_manufacturers.empty:
                            # Calculate the extra amount (difference between actual and predicted sales)
                            overperforming_manufacturers['extra_amount'] = overperforming_manufacturers['ventas_reales'] - overperforming_manufacturers['ventas_predichas']

                            # Sort by the highest extra amount
                            overperforming_manufacturers = overperforming_manufacturers.sort_values(by='extra_amount', ascending=False)

                            # Limit to top 10 overperforming manufacturers
                            top_overperformers = overperforming_manufacturers.head(10)

                            # Display two cards per row
                            for i in range(0, len(top_overperformers), 2):
                                cols = st.columns(2)  # Create two columns for two cards in a row

                                for j, col in enumerate(cols):
                                    if i + j < len(top_overperformers):
                                        row = top_overperformers.iloc[i + j]
                                        manufacturer_name = get_supplier_name_encoded(row['marca_id_encoded'])
                                        predicted = row['ventas_predichas']
                                        actual = row['ventas_reales']
                                        extra = row['extra_amount']

                                        # Use st.metric for compact display in each column
                                        with col:
                                            st.metric(
                                                label=f"{manufacturer_name}",
                                                value=f"{actual:.2f}€",
                                                delta=f"Exceeded by {extra:.2f}€",
                                                delta_color="normal"
                                            )


                        # Radar chart logic remains the same
                        customer_df = df[df["CLIENTE"] == str(customer_code)]
                        all_manufacturers = customer_df.iloc[:, 1:].T
                        all_manufacturers.index = all_manufacturers.index.astype(str)

                        customer_euros = euros_proveedor[euros_proveedor["CLIENTE"] == str(customer_code)]
                        sales_data = customer_euros.iloc[:, 1:].T
                        sales_data.index = sales_data.index.astype(str)

                        sales_data_filtered = sales_data.drop(index='CLIENTE', errors='ignore')
                        sales_data_filtered = sales_data_filtered.apply(pd.to_numeric, errors='coerce')
                        all_manufacturers = all_manufacturers.apply(pd.to_numeric, errors='coerce')

                        top_units = all_manufacturers.sort_values(by=all_manufacturers.columns[0], ascending=False).head(10)
                        top_sales = sales_data_filtered.sort_values(by=sales_data_filtered.columns[0], ascending=False).head(10)
                        combined_top = pd.concat([top_units, top_sales]).index.unique()[:20]

                        combined_top = [m for m in combined_top if m in all_manufacturers.index and m in sales_data_filtered.index]

                        if combined_top:
                            combined_data = pd.DataFrame({
                                'units': all_manufacturers.loc[combined_top, all_manufacturers.columns[0]],
                                'sales': sales_data_filtered.loc[combined_top, sales_data_filtered.columns[0]]
                            }).fillna(0)

                            combined_data_sorted = combined_data.sort_values(by=['units', 'sales'], ascending=False)
                            non_zero_manufacturers = combined_data_sorted[combined_data_sorted['units'] > 0]
                            
                            if len(non_zero_manufacturers) < 3:
                                zero_manufacturers = combined_data_sorted[combined_data_sorted['units'] == 0].head(3 - len(non_zero_manufacturers))
                                manufacturers_to_show = pd.concat([non_zero_manufacturers, zero_manufacturers])
                            else:
                                manufacturers_to_show = non_zero_manufacturers

                            values = manufacturers_to_show['units'].tolist()
                            amounts = manufacturers_to_show['sales'].tolist()
                            manufacturers = [get_supplier_name(m) for m in manufacturers_to_show.index]

                            if manufacturers:
                                fig = radar_chart(manufacturers, values, amounts, f'Gráfico de radar para los {len(manufacturers)} principales fabricantes del cliente {customer_code}')
                                st.pyplot(fig)

                    # Column 2: Alerts and additional analysis
                    with col2:
                        st.subheader("¡Puede que tengas que revisar esto!")
                        st.warning("Se esperaba que tu cliente comprara más productos de las siguientes marcas:")

                        # Group results by manufacturer to calculate the total predicted and actual sales
                        grouped_results = results.groupby('marca_id_encoded').agg({
                            'ventas_reales': 'sum',
                            'ventas_predichas': 'sum'
                        }).reset_index()

                        # Identify manufacturers that didn't meet predicted sales
                        underperforming_manufacturers = grouped_results[grouped_results['ventas_reales'] < grouped_results['ventas_predichas']].copy()

                        if not underperforming_manufacturers.empty:
                            # Calculate the missed amount
                            underperforming_manufacturers['missed_amount'] = underperforming_manufacturers['ventas_predichas'] - underperforming_manufacturers['ventas_reales']

                            # Sort by the highest missed amount
                            underperforming_manufacturers = underperforming_manufacturers.sort_values(by='missed_amount', ascending=False)

                            # Limit to top 10 missed amounts
                            top_misses = underperforming_manufacturers.head(10)

                            # Display two cards per row
                            for i in range(0, len(top_misses), 2):
                                cols = st.columns(2)  # Create two columns for two cards in a row

                                for j, col in enumerate(cols):
                                    if i + j < len(top_misses):
                                        row = top_misses.iloc[i + j]
                                        manufacturer_name = get_supplier_name_encoded(row['marca_id_encoded'])
                                        predicted = row['ventas_predichas']
                                        actual = row['ventas_reales']
                                        missed = row['missed_amount']

                                        # Use st.metric for compact display in each column
                                        with col:
                                            st.metric(
                                                label=f"{manufacturer_name}",
                                                value=f"{actual:.2f}€",
                                                delta=f"Missed by {missed:.2f}€",
                                                delta_color="inverse"
                                            )
                        else:
                            st.success("All manufacturers have met or exceeded predicted sales.")

                        # # Gráfico adicional: Comparar las ventas predichas y reales para los principales fabricantes
                        # st.markdown("### Predicted vs Actual Sales for Top Manufacturers")
                        # top_manufacturers = results.groupby('marca_id_encoded').agg({'ventas_reales': 'sum', 'ventas_predichas': 'sum'}).sort_values(by='ventas_reales', ascending=False).head(10)

                        # fig_comparison = go.Figure()
                        # fig_comparison.add_trace(go.Bar(x=top_manufacturers.index, y=top_manufacturers['ventas_reales'], name="Actual Sales", marker_color='blue'))
                        # fig_comparison.add_trace(go.Bar(x=top_manufacturers.index, y=top_manufacturers['ventas_predichas'], name="Predicted Sales", marker_color='orange'))

                        # fig_comparison.update_layout(
                        #     title="Actual vs Predicted Sales by Top Manufacturers",
                        #     xaxis_title="Manufacturer",
                        #     yaxis_title="Sales (€)",
                        #     barmode='group',
                        #     height=400,
                        #     hovermode="x unified"
                        # )

                        # st.plotly_chart(fig_comparison, use_container_width=True)

                        # Gráfico de ventas anuales
                        ventas_clientes['codigo_cliente'] = ventas_clientes['codigo_cliente'].astype(str).str.strip()

                        sales_columns = ['VENTA_2021', 'VENTA_2022', 'VENTA_2023']
                        if all(col in ventas_clientes.columns for col in sales_columns):
                            customer_sales_data = ventas_clientes[ventas_clientes['codigo_cliente'] == customer_code]

                            if not customer_sales_data.empty:
                                customer_sales = customer_sales_data[sales_columns].values[0]
                                years = ['2021', '2022', '2023']

                                # Convert 'fecha_mes' to datetime format if it's not already
                                if not pd.api.types.is_datetime64_any_dtype(results['fecha_mes']):
                                    results['fecha_mes'] = pd.to_datetime(results['fecha_mes'], errors='coerce')

                                # Add the 2024 actual and predicted data
                                if 'ventas_predichas' in results.columns and 'ventas_reales' in results.columns:
                                    actual_sales_2024 = results[results['fecha_mes'].dt.year == 2024]['ventas_reales'].sum()
                                    predicted_sales_2024 = results[results['fecha_mes'].dt.year == 2024]['ventas_predichas'].sum()

                                    # Assuming only 9 months of actual data are available, annualize the sales
                                    months_available = 9
                                    actual_sales_2024_annual = (actual_sales_2024 / months_available) * 12

                                    # Prepare data for the bar chart
                                    sales_values = list(customer_sales) + [actual_sales_2024_annual]
                                    predicted_values = list(customer_sales) + [predicted_sales_2024]

                                    years.append('2024')

                                    # Create the bar chart for historical and 2024 data
                                    fig_sales_bar = go.Figure()
                                    fig_sales_bar.add_trace(go.Bar(
                                        x=years[:3],  
                                        y=sales_values[:3],
                                        name="Historical Sales",
                                        marker_color='blue'
                                    ))

                                    fig_sales_bar.add_trace(go.Bar(
                                        x=[years[3]],  
                                        y=[sales_values[3]],
                                        name="2024 Actual Sales (Annualized)",
                                        marker_color='green'
                                    ))

                                    fig_sales_bar.add_trace(go.Bar(
                                        x=[years[3]],  
                                        y=[predicted_values[3]],
                                        name="2024 Predicted Sales",
                                        marker_color='orange'
                                    ))

                                    # Customize layout
                                    fig_sales_bar.update_layout(
                                        title=f"Ventas anuales de tu cliente",
                                        xaxis_title="Year",
                                        yaxis_title="Sales (€)",
                                        barmode='group',
                                        height=600,
                                        legend_title_text="Sales Type",
                                        hovermode="x unified"
                                    )

                                    # Display the chart
                                    st.plotly_chart(fig_sales_bar, use_container_width=True)

                                else:
                                    st.warning(f"No predicted or actual data found for customer {customer_code} for 2024.")

# Customer Recommendations Page
elif page == "💡 Recomendación de Artículos":
    # Carga de CSV necesarios cestas y productos
    cestas = pd.read_csv('cestas.csv') 
    productos = pd.read_csv('productos.csv')
    
    # Estilo principal de la página
    st.markdown(
        "<h1 style='text-align: center;'>Recomendación de Artículos</h1>", 
        unsafe_allow_html=True
    )
    st.markdown("""<p style='text-align: center; color: #5D6D7E;'>Obtén recomendaciones personalizadas para tus clientes basadas en su cesta de compra.</p>""", unsafe_allow_html=True)

    st.write("### Selecciona los artículos y asigna las cantidades para la cesta:")

    # Añadir separador para mejorar la segmentación visual
    st.divider()

    # Mostrar lista de artículos disponibles (ahora se usa el código asociado a cada descripción)
    available_articles = productos[['ARTICULO', 'DESCRIPCION']].drop_duplicates()

    # Crear diccionario para asignar las descripciones a los códigos
    article_dict = dict(zip(available_articles['DESCRIPCION'], available_articles['ARTICULO']))

    # Permitir seleccionar las descripciones, pero trabajar con los códigos
    selected_descriptions = st.multiselect("Selecciona los artículos", available_articles['DESCRIPCION'].unique())
    
    quantities = {}

    if selected_descriptions:
        st.write("### Selecciona los artículos, las unidades, y visualiza la imagen:")

        for description in selected_descriptions:
            code = article_dict[description]  # Usar el código del artículo
            col1, col2, col3 = st.columns([1, 2, 2])  # Ajustar proporciones para que las imágenes y textos se alineen

            with col1:
                # Mostrar la imagen del artículo
                img_url = f"https://www.saneamiento-martinez.com/imagenes/articulos/{code}_1.JPG"
                st.image(img_url, width=100)

            with col2:
                # Mostrar la descripción del artículo
                st.write(f"**{description}**")
            
            with col3:
                # Caja de número para la cantidad, asociada al código
                quantities[code] = st.number_input(f"Cantidad {code}", min_value=0, step=1, key=code)

    # Añadir un botón estilizado "Calcular" con icono
    if st.button("🛒 Obtener Recomendaciones"):
        # Crear una lista de artículos basada en los códigos y cantidades
        new_basket = []
        for code in quantities:
            quantity = quantities[code]
            if quantity > 0:
                new_basket.extend([code] * quantity)  # Añadir el código tantas veces como 'quantity'
        
        if new_basket:
            # Procesar la lista para recomendar utilizando tu función 'recomienda_tf'
            recommendations_df = recomienda_tf(new_basket, cestas, productos)

            if not recommendations_df.empty:
                st.success("### Según tu cesta, te recomendamos que consideres añadir estos artículos:")

                # Mostrar los artículos recomendados con imágenes y relevancia
                for idx, row in recommendations_df.iterrows():
                    rec_code = row['ARTICULO']
                    rec_desc = row['DESCRIPCION']
                    rec_relevance = row['RELEVANCIA']  # Usar la relevancia calculada
                    rec_img_url = f"https://www.saneamiento-martinez.com/imagenes/articulos/{rec_code}_1.JPG"
                    
                    # Verificar si la imagen existe antes de mostrar el artículo
                    if image_exists(rec_img_url):
                        rec_col1, rec_col2, rec_col3 = st.columns([1, 3, 1])  # Añadir una columna para la relevancia
                        with rec_col1:
                            st.image(rec_img_url, width=100)
                        with rec_col2:
                            st.write(f"**{rec_desc}** (Código: {rec_code})")
                        with rec_col3:
                            st.metric(label="Relevancia",value =f"{rec_relevance * 100:.2f}%") # Mostrar la relevancia con 4 decimales
            else:
                st.warning("⚠️ No se encontraron recomendaciones para la cesta proporcionada.")
        else:
            st.warning("⚠️ Por favor selecciona al menos un artículo y define su cantidad.")



# elif page == "💡 Recomendación de Artículos":
#     # Carga de CSV necesarios cestas y productos
#     cestas = pd.read_csv('cestas.csv') 
#     productos = pd.read_csv('productos.csv')
#     # Estilo principal de la página
#     st.markdown(
#         "<h1 style='text-align: center;'>Recomendación de Artículos</h1>", 
#         unsafe_allow_html=True
#     )
#     st.markdown("""
#         <p style='text-align: center; color: #5D6D7E;'>Obtén recomendaciones personalizadas para tus clientes basadas en su cesta de compra.</p>
#     """, unsafe_allow_html=True)
#     st.write("### Selecciona los artículos y asigna las cantidades para la cesta:")
#     # Añadir separador para mejorar la segmentación visual
#     st.divider()
#     # Mostrar lista de artículos disponibles (ahora se usa el código asociado a cada descripción)
#     available_articles = productos[['ARTICULO', 'DESCRIPCION']].drop_duplicates()
    
#     # Crear diccionario para asignar las descripciones a los códigos
#     article_dict = dict(zip(available_articles['DESCRIPCION'], available_articles['ARTICULO']))
#     # Permitir seleccionar las descripciones, pero trabajar con los códigos
#     selected_descriptions = st.multiselect("Select Articles", available_articles['DESCRIPCION'].unique())
#     quantities = {}
    
#     if selected_descriptions:
#         st.write("### Selecciona los artículos y las unidades:")
#         for description in selected_descriptions:
#             code = article_dict[description]  # Usar el código del artículo
#             col1, col2 = st.columns([1, 3])  # Ajustar proporciones para que las cantidades vayan a la izquierda
#             with col1:
#                 # Caja de número para la cantidad, asociada al código
#                 quantities[code] = st.number_input(f"Quantity {code}", min_value=0, step=1, key=code)
#             with col2:
#                 # Mostrar la descripción del artículo
#                 st.write(description)
    
#     # Añadir un botón estilizado "Calcular" con icono
#     if st.button("🛒 Obtener Recomendaciones"):
#         # Crear una lista de artículos basada en los códigos y cantidades
#         new_basket = []
#         for code in quantities:
#             quantity = quantities[code]
#             if quantity > 0:
#                 new_basket.extend([code] * quantity)  # Añadir el código tantas veces como 'quantity'
#         if new_basket:
#             # Procesar la lista para recomendar
#             recommendations_df = recomienda_tf(new_basket, cestas, productos)
            
#             if not recommendations_df.empty:
#                 st.success("### Según tu cesta, te recomendamos que consideres añadir uno de estos artículos:")
#                 st.dataframe(recommendations_df, height=300, width=800)  # Ajustar el tamaño del DataFrame
#             else:
#                 st.warning("⚠️ No recommendations found for the provided basket.")
#         else:
#             st.warning("⚠️ Please select at least one article and set its quantity.")
