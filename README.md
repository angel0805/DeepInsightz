<div align="center">

# **Deep Insightz - Proyecto de Ciencia de Datos**

🖥️ [**Enlace a la web del proyecto**](https://huggingface.co/spaces/GMARTINEZMILLA/Final_Project) 🖥️

</div>

---

## **🚨 Problemas Identificados**
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

## **🛠 Soluciones Propuestas**

### 1. **🕵️ Análisis de Clientes**
Para abordar la falta de herramientas que permita a los comerciales analizar eficazmente el comportamiento de compra de los clientes, hemos desarrollado la herramienta de Análisis de Cliente. Esta solución proporciona una visión clara de las ventas por fabricante para cada cliente, facilitando la detección de cambios en los hábitos de compra. Al mostrar las predicciones de ventas futuras, comparadas con los resultados reales, los comerciales pueden identificar rápidamente si un cliente ha dejado de adquirir productos de una marca específica y así poder tomar medidas preventivas o correctivas.

Además, la herramienta **simplifica la gestión de información**, en lugar de tener que solicitar datos o realizar análisis manuales, ofrece una visión global del cliente, permitiendo a los comerciales revisar de un vistazo sus preferencias y tendencias de compra. Esto agiliza la toma de decisiones y mejora la capacidad de respuesta ante las necesidades del cliente.

### 2. **💡 Recomendación de Artículos**
La herramienta de Recomendación de Artículos permite a los vendedores sugerir productos complementarios basados en las compras realizadas por todos los clientes. Esto **facilita la venta cruzada**, incluso en situaciones donde el trabajador **no está familiarizado con todo el catálogo de productos**, ya que la herramienta sugiere opciones relevantes de manera automática.

Además, esta solución optimiza el tiempo en tienda al proporcionar recomendaciones rápidas, evitando que el cliente tenga que volver por productos que podrían haber olvidado. De esta manera, se mejora la experiencia de compra y se incrementa el valor de la cesta, ayudando a maximizar las oportunidades de venta sin aumentar la carga de trabajo del vendedor.

---

## **📊 Recolección y preparación de datos**
Los datos utilizados en este proyecto provienen de los albaranes de compra históricos de los clientes B2B de la empresa, que nos entregaron con la información de los clientes codificada. A continuación, se describen los pasos más relevantes en el proceso de limpieza y preparación de los datos:

- **Corrección de errores en los códigos**: Durante la exportación, algunos códigos numéricos se transformaron en notación científica (ej. '09E+12'), lo que requirió ajustar la forma en que se exportaron. También se solucionaron errores en los caracteres, como la sustitución incorrecta de la letra "Ñ".
- **Eliminación de datos irrelevantes**: Se eliminaron instancias con artículos nulos o descripciones erróneas (como aquellas que contenían "DSCTL"). También se neutralizaron los productos devueltos, descartando las devoluciones donde no hubo compras desde 2021.
- **Generación de nuevos campos**: Se crearon identificadores únicos de facturas combinando serie y número. Asimismo, se calculó la frecuencia anual de compra y el total de ventas anuales por cliente para obtener una visión clara de su comportamiento.
- **Reducción del conjunto de fabricantes**: Dado que muchos fabricantes tenían ventas muy bajas, se decidió concentrar los análisis en los 99 fabricantes más relevantes, aquellos con más de 1.000 artículos vendidos en los últimos 4 años.
- **Enriquecimiento de datos**: Se añadieron columnas que incluyen el grupo de productos y las categorías de clientes previamente definidas por la empresa (plomero, electricista, constructor, etc.).

---

## **🔍 Datos Clave del Dataset**
El análisis del dataset reveló algunos aspectos importantes sobre los clientes y sus patrones de compra. A continuación, se destacan algunos puntos clave:
- **Volumen de datos**: El dataset utilizado contiene un total de 764,396 líneas de ventas distribuidas entre 4.000 clientes B2B y 99 fabricantes seleccionados, lo que representa una reducción de los más de 300 fabricantes originalmente presentes en los datos.
- **Preferencias de Fabricantes**: Un pequeño porcentaje de fabricantes domina las ventas. Por ejemplo, el 20% de los fabricantes más vendidos representan el 80% de las ventas totales. Esto nos permitió concentrarnos en los fabricantes con más relevancia, asegurando que las recomendaciones y predicciones fueran más precisas.
-**Distribución de Compras por Cliente**: Se detectaron diferencias marcadas en el comportamiento de compra de los clientes. Mientras que el 90% de los clientes compraron menos de 1.000 artículos en total, un 10% de los clientes son responsables de las compras de más de 10.000 artículos, representando a los clientes más valiosos.
-**Frecuencia de Compra**: Los clientes tienen patrones de compra variados, desde compras regulares y estables a lo largo del tiempo, hasta clientes que compran de manera intermitente. Identificamos que aproximadamente el 10% de los clientes realizan compras significativas con frecuencia, lo que refuerza la importancia de segmentar correctamente las estrategias de venta.

---

## **⚙️ Algoritmos y Métricas Utilizadas**
### 1. **🕵️ Análisis de Clientes**
- **Algoritmo**: Se utilizó **LightGBM** para las predicciones, por su eficiencia al manejar grandes cantidades de datos con muchos valores cero, debido a la gran cantidad de fabricantes.
- **Métricas de Evaluación**: 
  - **MAE** (Mean Absolute Error)
El MAE mide el error medio absoluto entre las predicciones y los valores reales. 
Simplemente toma la diferencia absoluta entre ambos y luego calcula el promedio. 
Es fácil de entender, ya que nos dice cuántas unidades (en promedio) nos hemos desviado de los valores reales.

**Ejemplo**: 
Si predecimos que un cliente comprará 200 unidades y realmente compra 220, la diferencia absoluta es 20 unidades. 
Si repetimos esto para varios clientes y obtenemos diferencias como 10, 15, y 25, el MAE sería el promedio de esas diferencias, 
es decir, (20 + 10 + 15 + 25) / 4 = 17.5 unidades.

  - **RMSE** (Root Mean Square Error)
El RMSE también mide la diferencia entre los valores reales y predichos, pero penaliza más los errores grandes. 
Esto se logra elevando al cuadrado las diferencias antes de hacer la media y tomando la raíz cuadrada del resultado.

**Ejemplo**: 
Si tenemos las mismas diferencias que antes (20, 10, 15, 25), elevamos cada una al cuadrado: 400, 100, 225, 625. 
Luego, calculamos el promedio de estos números: (400 + 100 + 225 + 625) / 4 = 337.5. 
Finalmente, tomamos la raíz cuadrada, obteniendo un RMSE de aproximadamente 18.37 unidades. 
Este valor es más sensible a las grandes diferencias.

  - **SMAPE** (Symmetric Mean Absolute Percentage Error)

El SMAPE es una métrica que se utiliza para medir la precisión de los modelos de predicción. Es una variación del MAPE (Mean Absolute Percentage Error), diseñada para evitar los problemas que surgen cuando los valores reales son muy pequeños o cercanos a cero. A diferencia del MAPE, que puede volverse inestable en estas situaciones, el SMAPE es más robusto y proporciona una mejor representación de los errores de predicción.

![Fórmula de SMAPE](images/SMAPE.jpg)

**Ejemplo**:
Cuando tenemos valores cercanos a 0, el MAPE se puede ir a infinito.
En este ejemplo, predecimos que se venderían 5 unidades y se venden 0. Aquí el MAPE se vuelve problemático:

![Ejemplo SMAPE y MAPE](images/SMAPE_2.jpg)

En este caso, el SMAPE devuelve un valor finito y más razonable, lo que lo hace más adecuado cuando se trata de valores cercanos a cero. En comparación, el MAPE, incluso si le asignamos un valor muy pequeño, puede generar un porcentaje extremadamente alto. Dado que en nuestro proyecto es probable que encontremos escenarios con valores cercanos a cero, el SMAPE nos permite evaluar de manera más precisa la efectividad de las predicciones.

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

- [**Angel Colina**](https://github.com/angel0805)
- [**Maria Ortega Rivas**](https://github.com/mariaorrri)
- [**Guillermo Martínez Millá**](https://github.com/GuillePrograma94)
