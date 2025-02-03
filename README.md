## **📌 Documento Técnico – Extracción de Datos Legislativos en Chile (2023)

**

---

## **1. Introducción**

Kitsune está desarrollando un nuevo servicio de análisis legislativo basado en los datos generados por el Congreso de Chile durante el año 2023. Este documento describe las fuentes de datos utilizadas, la estructura de la información recuperada y el proceso de extracción automatizada.

El propósito es brindar claridad a una multinacional del sector hidrocarburos sobre la actividad legislativa que puede impactar su operación en Chile.

---

## **2. Fuentes de Datos**

Para garantizar información confiable, se han seleccionado fuentes **primarias** del  **Congreso de Chile** , evitando intermediarios.

### **2.1. Listado de Proyectos de Ley**

📌 **Fuente:** Portal del Senado de Chile

🔗 [https://tramitacion.senado.cl/appsenado/templates/tramitacion](https://tramitacion.senado.cl/appsenado/templates/tramitacion)

📄 **Formato:** **CSV manual / Web Scraping**

**Descripción:**

* Contiene el listado completo de proyectos de ley.
* Permite filtrar por año para obtener solo los proyectos de  **2023** .

**Método de Extracción:**

1. **Filtrar por año 2023** en la plataforma.
2. **Descargar manualmente el CSV** con la lista de proyectos de ley.
3. **Extraer la columna de boletines** (IDs únicos de cada proyecto).
4. Guardar el archivo como `boletines_2023.csv`.

**Ejemplo de Datos Descargados:**

| boletin_id | titulo                                          |
| ---------- | ----------------------------------------------- |
| 16535-24   | Establece el 11 de agosto como Día del Hip Hop |
| 16536-24   | Reforma sobre regulación de hidrocarburos      |

---

### **2.2. Información Detallada de Cada Proyecto de Ley**

📌 **Fuente:** API pública del Senado de Chile

🔗 `https://tramitacion.senado.cl/wspublico/tramitacion.php?boletin=<boletin_id>`

📄 **Formato:** **XML**

**Descripción:**

* Devuelve los detalles de un  **proyecto de ley específico** .
* Contiene campos como:
  * **Boletín ID**
  * **Título del Proyecto**
  * **Fecha de presentación**
  * **Estado actual**
  * **Comisión asignada**
  * **Tipo de iniciativa** (Nueva ley, Modificación, Reforma)
  * **Lista de legisladores involucrados**
  * **Descripción del proyecto**
  * **Historial de tramitación**

---

## **3. Estructura de los Datos Recuperados**

La API devuelve la información en  **XML** , con la siguiente estructura:

### **Ejemplo de Respuesta XML**

```xml
<proyectos>
    <proyecto>
        <descripcion>
            <boletin>16535-24</boletin>
            <titulo>Establece el 11 de agosto de cada año como el Día Nacional del Hip Hop</titulo>
            <fecha_ingreso>29/12/2023</fecha_ingreso>
            <iniciativa>Moción</iniciativa>
            <camara_origen>C.Diputados</camara_origen>
            <urgencia_actual>Sin urgencia</urgencia_actual>
            <etapa>Primer trámite constitucional (C.Diputados)</etapa>
            <subetapa>Primer informe de comisión de Cultura, Artes y Comunicaciones</subetapa>
            <leynro/>
            <diariooficial/>
            <estado>En tramitación</estado>
            <refundidos/>
            <link_mensaje_mocion>http://www.senado.cl/appsenado/index.php?mo=tramitacion&ac=getDocto&iddocto=17103&tipodoc=mensaje_mocion</link_mensaje_mocion>
        </descripcion>
        <autores>
            <autor>
                <PARLAMENTARIO>Camaño Cárdenas, Felipe</PARLAMENTARIO>
            </autor>
            <autor>
                <PARLAMENTARIO>Manouchehri Lobos, Daniel</PARLAMENTARIO>
            </autor>
            <autor>
                <PARLAMENTARIO>Olivera De La Fuente, Erika</PARLAMENTARIO>
            </autor>
            <autor>
                <PARLAMENTARIO>Santibáñez Novoa, Marisela</PARLAMENTARIO>
            </autor>
            <autor>
                <PARLAMENTARIO>Veloso Ávila, Consuelo</PARLAMENTARIO>
            </autor>
        </autores>
        <tramitacion>
            <tramite>
                <SESION>/</SESION>
                <FECHA>29/12/2023</FECHA>
                <DESCRIPCIONTRAMITE>Ingreso de proyecto</DESCRIPCIONTRAMITE>
                <ETAPDESCRIPCION>Primer trámite constitucional</ETAPDESCRIPCION>
                <CAMARATRAMITE>C.Diputados</CAMARATRAMITE>
            </tramite>
            <tramite>
                <SESION>129/371</SESION>
                <FECHA>10/01/2024</FECHA>
                <DESCRIPCIONTRAMITE>Cuenta de proyecto. Pasa a Comisión de Cultura, Artes y Comunicaciones</DESCRIPCIONTRAMITE>
                <ETAPDESCRIPCION>Primer trámite constitucional</ETAPDESCRIPCION>
                <CAMARATRAMITE>C.Diputados</CAMARATRAMITE>
            </tramite>
        </tramitacion>
    </proyecto>
</proyectos>
```

---

## **4. Proceso de Extracción de Datos**

El flujo de extracción de datos sigue estos pasos:

1️⃣ **Obtener la lista de proyectos de ley**

* Descarga manual del CSV con los boletines del  **2023** .

2️⃣ **Realizar consultas a la API**

* Para cada `boletin_id`, hacer una petición HTTP.

3️⃣ **Procesar la respuesta en XML**

* Extraer información relevante.
* Convertir los datos a formato estructurado.

4️⃣ **Guardar en un formato accesible**

* Almacenar en  **CSV o base de datos SQL** .

---

## **5. Riesgos y Limitaciones**

Si bien los datos provienen de fuentes oficiales, existen algunos riesgos:

| Riesgo                           | Impacto                                                 | Mitigación                              |
| -------------------------------- | ------------------------------------------------------- | ---------------------------------------- |
| **API no documentada**     | Puede cambiar sin aviso                                 | Implementar manejo de errores            |
| **Datos faltantes**        | Algunos proyectos pueden no tener información completa | Validar y registrar valores vacíos      |
| **Bloqueo de solicitudes** | La API podría bloquear por exceso de consultas         | Agregar `time.sleep()`entre peticiones |

---

## **6. Recomendaciones de Almacenamiento**

| Opción                         | Beneficio                      | Recomendación                        |
| ------------------------------- | ------------------------------ | ------------------------------------- |
| **Google Sheets**         | Fácil acceso para la analista | Exploración rápida                  |
| **PostgreSQL**            | Consultas avanzadas            | Si se necesita análisis estructurado |
| **BigQuery**              | Manejo de grandes volúmenes   | Si hay necesidad de escalabilidad     |
| **AWS S3 / Google Drive** | Almacenamiento simple de CSV   | Para acceso compartido                |

Se recomienda iniciar con  **Google Sheets o PostgreSQL** , dependiendo de la necesidad del equipo de análisis.
