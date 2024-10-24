# **Deep Insightz - Proyecto de Ciencia de Datos**

🌐 [**Enlace al Proyecto en Hugging Face**](https://huggingface.co/spaces/GMARTINEZMILLA/Final_Project)

---

## **📌 Problemas del Negocio**
 ### 🚩Primer Problema Identificado:
 Hemos detectado una **falta de herramientas** que permitan a los comerciales **analizar de manera eficiente el comportamiento de compra de sus clientes B2B** (aproximadamente 4.000). 
 El análisis que realiza la empresa actualmente, se centra en las ventas anuales de los mejores clientes, **limitando la identificación de oportunidades de crecimiento** entre el resto de sus clientes, además de reducir el potencial de intervención en decisiones clave.
 ### Retos clave:
 - **Detección de cambios en los hábitos de compra**: Si un cliente modifica sus hábitos de compra o deja de adquirir productos de una marca en particular, resulta difícil detectar estos cambios sin un análisis detallado. Por ejemplo, un cliente que deja de comprar platos de ducha de nuestra empresa para adquirirlos de un competidor podría, al mismo tiempo, aumentar las compras de otros productos debido al crecimiento de su negocio. Este cambio mantendría el volumen global de ventas estable y pasaría inadvertido, representando así una oportunidad de venta perdida.
 - **Saturación de información**: Los comerciales gestionan una amplia cartera de clientes y pedidos, lo que les dificulta analizar a fondo el comportamiento individual de cada cliente. Esto resulta en una pérdida de oportunidades estratégicas, ya que, debido a la gran variedad de productos, es probable que terminen ofreciendo opciones que no se ajustan a las necesidades o intereses específicos del cliente.
 - **Acceso limitado a la información clave**: Los vendedores no disponen de acceso completo a la información de sus clientes, lo que les impide realizar análisis detallados sin depender de la colaboración de personas autorizadas. Esta situación genera cuellos de botella y retrasa la toma de decisiones, reduciendo la agilidad en la atención y respuesta a las necesidades de los clientes.
 ### 🚩Segundo Problema Identificado:
 La empresa de fontanería enfrenta un desafío significativo en la gestión de su extenso catálogo de productos. Aunque en los datos analizados se detectaron 10.000 productos únicos, la base de datos de la empresa contiene 40.000 artículos registrados. Esta enorme cantidad de artículos obliga a la empresa a depender del conocimiento y experiencia de sus trabajadores para ofrecer productos relevantes a los clientes.
 ### Retos clave:
 - **Catálogo Extenso y Complejo**: El aprendizaje suele ocurrir sobre la marcha, conforme el trabajador se enfrenta a preguntas de los clientes o recibe formación de la empresa, además de su propio interés en aprender.
 - **Expectativas de Rapidez**: Los clientes profesionales, **esperan pasar el menor tiempo posible en la tienda**. Por esta razón, los trabajadores tienen que operar a un ritmo rápido, lo que genera situaciones en las que, por falta de tiempo, los empleados pueden olvidar sugerir productos complementarios que podrían incrementar el valor de la cesta, además de **evitarle al cliente un viaje de vuelta a la tienda**.
 - **Tiempo limitado**: Los trabajadores con experiencia suelen estar **muy ocupados atendiendo a sus propios clientes**, lo que deja poco tiempo para ayudar a los nuevos empleados a familiarizarse con el catálogo. Esta situación es especialmente difícil en **momentos de alta demanda**, donde **no es posible dejar de atender a los clientes** para apoyar a los trabajadores nuevos en la recomendación de productos.
 

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
