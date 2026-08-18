Original paper: https://arxiv.org/pdf/2608.14528


# Arquitectura de archivos

Los archivos de trabajo de este método se guardan en la carpeta `docs/icl_state`. Dentro de esta carpeta hay más archivos, los cuales se distribuyen de la siguiente manera:

```
raiz_del_proyecto/
|
├── docs/
|   ├── icl_state/
│   │   ├── handover_state/ (El registro completo 'H') 
│   │   │   │
│   │   │   ├── active_prompt_v/ (Información serializada para el prompt 'V') 
│   │   │   │   ├── exact_decisions.json (Contiene 'H_exact': metas y restricciones) 
│   │   │   │   ├── sufficient_statistics.bin (Contiene 'H_stat': matrices G_n, b_n, etc.) 
│   │   │   │   └── residual_metadata.json (Contiene 'J_res': IDs de ejemplos externos) 
│   │   │   │
│   │   │   └── external_storage_m/ (Archivos disponibles tras la transferencia 'M') [1, 9]
│   │   │       ├── observations/ (Contiene los datos originales 'o_j' de 'H_residual') [2]
│   │   │       │   ├── failure_case_001.txt
│   │   │       │   └── rare_example_002.json
│   │   │       └── indexed_data/ (Bases de datos o archivos de referencia adicionales) [1]
│   │   │
│   │   ├── validation/ (Checks determinísticos antes de la nueva sesión) [12, 15]
│   │   │   ├── schema_definitions.json (Define campos requeridos) [12]
│   │   │   └── numerical_checks.py (Verifica dimensiones de las estadísticas) [12]
│   │   │
│   │   └── logs/
│   │       └── memory_account.csv (Registro de tokens de 'V' y bytes de 'M') [3, 11]
│   │
|   ...
│
...
```

**IMPORTANTE**: Si estos archivos NO existen, se deben crear (archivos y carpetas).

## Definición de artefactos

1. **Parte Exacta (H_exact)**: Es la memoria "rígida" del sistema y no debe resumirse ni alterarse.
    - **Contenido**: El objetivo actual, decisiones tomadas que limitan el siguiente paso, opciones ya rechazadas, asuntos no resueltos y la fuente original de cada entrada.
2. **Parte Estadística (H_stat)**: 
Es la memoria optimizada para datos densos.
    - **Contenido**: Representaciones cortas de ejemplos repetidos o resultados de herramientas (como estadísticas matemáticas o aproximaciones con límites de error explícitos) que sustituyen a los datos masivos originales.
3. **Parte Residual (H_residual)**: Es el almacén de detalles críticos no resumibles.
    - **Contenido**: Observaciones originales seleccionadas que el componente estadístico no pudo procesar, como casos excepcionales o errores específicos que determinarán el comportamiento futuro del modelo.
4. **Registros Externos (M)**: Si la memoria del chat (el prompt) es muy pequeña, se crea este artefacto adicional.
    - **Contenido**: Archivos, bases de datos o índices que contienen información detallada del historial anterior; el prompt principal solo contendrá identificadores o "etiquetas" para que la IA sepa qué consultar en estos archivos si lo necesita.

# Pasos de la Metodología

1. **Recepción y Análisis de Información**: Al llegar al límite de la sesión, el "Escritor" recibe todo el contexto previo (conversaciones, herramientas, ejemplos) y las instrucciones de la tarea.
2. **Identificación de Restricciones y Decisiones**: Se revisan qué decisiones ya se tomaron, qué opciones fueron rechazadas y qué asuntos quedan pendientes por resolver. Esto es crítico porque cambiar una decisión previa puede alterar completamente los pasos permitidos a continuación.
3. **Cálculo de Estadísticas Justificadas**: Para datos repetitivos o resultados de herramientas, el sistema calcula "estadísticas suficientes" (resúmenes matemáticos) solo si existe una garantía técnica de que ese resumen no afectará el éxito de la tarea.
4. **Selección de Observaciones Residuales**: Se identifican ejemplos raros, fallos específicos u observaciones originales que no pueden resumirse estadísticamente pero que son fundamentales para los siguientes pasos.
5. **División y Asignación de Espacio**: El sistema divide el espacio de memoria disponible (el "presupuesto") entre las tres partes del registro, asegurando que se respete el límite de tokens o bytes.
6. **Serialización y Validación**: El registro se convierte a un formato de texto o datos (serialización) y se somete a controles determinísticos para verificar que el esquema sea correcto, que las dimensiones numéricas sean válidas y que no exceda el tamaño permitido antes de ser enviado a la nueva sesión
