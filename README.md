# **Deep Insightz - Proyecto de Ciencia de Datos**

🌐 [**Enlace al Proyecto en Hugging Face**](https://huggingface.co/spaces/GMARTINEZMILLA/Final_Project)

---

## **📌 Problema del Negocio**

El objetivo de este proyecto es ayudar a una empresa de fontanería que vende a clientes B2B (instaladores, constructoras) a **optimizar sus ventas**. El problema principal es la **falta de herramientas que permitan entender el comportamiento de compra** de los clientes sin necesidad de analizar cada albarán de manera manual.

---

## **📊 Recolección de Datos**

- **Origen de los datos**: Los datos provienen de los albaranes de compra históricos de los clientes B2B de la empresa.
- **Formato**: Cada albarán contiene información clave como: cliente, fabricante, producto, cantidad y fecha de compra.

---

## **🔍 Patrones Importantes Encontrados**

- **Preferencias de Fabricantes**: Muchos clientes muestran preferencia por ciertos fabricantes, comprando repetidamente de ellos.
- **Comportamientos de Compra**: Identificamos clientes que realizan compras de manera irregular y otros que mantienen una frecuencia de compra estable.

---

## **⚙️ Algoritmos y Métricas Utilizadas**

- **Algoritmo**: Se utilizó **LightGBM** para las predicciones, por su eficiencia al manejar grandes cantidades de datos con muchos valores cero, debido a la gran cantidad de fabricantes.
- **Métricas de Evaluación**: 
  - **MAE** (Mean Absolute Error)
  - **RMSE** (Root Mean Square Error)
  - **SMAPE** (Symmetric Mean Absolute Percentage Error)

Estas métricas nos permitieron medir la precisión de las predicciones y garantizar su utilidad para la empresa.

---

## **💻 Aplicación Web en Funcionamiento**

Nuestra web incluye dos herramientas clave:

1. **Análisis de Clientes**: Predicción de ventas por fabricante, ayudando a los equipos de ventas a tomar decisiones basadas en datos.
2. **Recomendación de Artículos**: Sugiere productos complementarios basados en cestas de compra anteriores de los clientes.

![Imagen del Proyecto en Funcionamiento](URL_de_la_imagen)

---

## **🚀 Mejoras Futuras**

Algunas de las mejoras propuestas para el proyecto incluyen:

- **Entrenamiento continuo del modelo**: Seguir afinando el modelo con nuevos datos de ventas.
- **Expansión al sector B2C**: Aplicar las herramientas de análisis y recomendación también para clientes B2C.
- **Mejora de la interfaz**: Optimizar la experiencia de usuario, especialmente en dispositivos móviles.

---

## **👥 Colaboradores**

- **Nombre del colaborador 1** - Data Scientist
- **Nombre del colaborador 2** - Full Stack Developer
- **Nombre del colaborador 3** - Especialista en Ventas B2B
