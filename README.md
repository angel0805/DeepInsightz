# **Deep Insightz - Proyecto de Ciencia de Datos**

🌐 [**Enlace al Proyecto en Hugging Face**](https://huggingface.co/spaces/GMARTINEZMILLA/Final_Project)

---

## **📌 Problemas del Negocio**
 ### 1r Problema Identificado:
 Uno de los problemas que hemos detectado tras hablar con el almacén, es la **falta de herramientas** que permitan a los comerciales **entender de manera eficiente el comportamiento de compra de sus clientes B2B** (aproximadamente 4.000). Actualmente, la empresa se centra en la venta anual del cliente y analiza a los mejores clientes individualmente, **perdiendo oportunidades de crecimiento** entre el resto de clientes por esta limitación.
 ### Retos clave:
 - **Identificar cambios en el comportamiento de compra**: Si un cliente modifica sus hábitos de compra o deja de adquirir productos de una marca específica, resulta difícil detectar estos cambios sin un análisis detallado. Por ejemplo, un cliente que deja de comprar platos de ducha de nuestra empresa para adquirirlos de un competidor podría, al mismo tiempo, aumentar las compras de otros productos debido al crecimiento de su negocio. Este cambio mantendría el volumen global de ventas estable y pasaría inadvertido, representando así una oportunidad de venta perdida.
 - **Saturación de información**: Los vendedores manejan una amplia cartera de clientes y pedidos, lo que dificulta el análisis detallado de cada caso. Como resultado, pierden oportunidades para intervenir a tiempo, mejorar las ventas o corregir patrones de compra.
 - **Limitaciones de acceso a la información**: Los vendedores no disponen de acceso completo a la información de sus clientes, lo que les impide realizar análisis detallados sin depender de la colaboración de personas autorizadas, generando cuellos de botella en el proceso.

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
