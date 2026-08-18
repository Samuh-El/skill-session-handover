# Manuel de uso

## ¿Cuándo y en qué ocasiones se debe invocar /session-handover?

Debes invocar la skill en cualquiera de estas 4 situaciones clave:

1. **Saturación de Contexto (Ventana de Tokens casi llena)**: Cuando la conversación lleva muchos turnos o ejecuciones de herramientas y notas lentitud, degradación en las respuestas o estás cerca del límite de tokens del modelo.
2. **Cambio de Modelo o Agente**: Cuando iniciaste con un modelo de alto razonamiento (por ejemplo, para planificar y diseñar la arquitectura) y deseas traspasar la ejecución a un modelo más rápido o especializado en código.
3. **Pausa o Fin de Jornada de Trabajo**: Cuando vas a cerrar el entorno o terminar tu sesión por el día y quieres asegurar que todas las decisiones técnicas, rutas descartadas y restricciones queden congeladas para continuar mañana sin pérdidas.
4. **Limpieza de Contexto Ruidoso**: Cuando hubo muchos errores de prueba y error en el chat y deseas "reiniciar la conversación desde cero", pero sin perder las decisiones aprobadas ni las restricciones aprendidas.

## Paso a paso

- **Fase 1: En la Sesión Actual (Antes de cerrar o cambiar de modelo)**: 
    1. Escribe el comando en el chat:
    ```
    /session-handover
    ```
    El agente actuará como "Escritor" (Writer):
    * Congelará el contexto.
    * Creará la carpeta docs/icl_state/ en tu proyecto si no existe.
    * Extraerá en exact_decisions.json las metas, decisiones firmes tomadas, alternativas rechazadas (para no volver a proponerlas) y asuntos pendientes.
    * Guardará observaciones residuales (errores raros, logs) en external_storage_m/observations/.
    * Ejecutará el script de validación determinista para comprobar que ningún archivo esté corrupto.
    * Te entregará un resumen de cierre confirmando que el estado está seguro.
- **Fase 2: En la Nueva Sesión (Al reanudar o cambiar de modelo)**:
    1. Abre tu nuevo chat o inicia la nueva sesión con el modelo que prefieras.
    2. Envía el prompt de reanudación inicial:
    "Reanuda el trabajo del proyecto leyendo el estado de transferencia en docs/icl_state/handover_state/active_prompt_v/exact_decisions.json. Respeta estrictamente las decisiones ya tomadas y las alternativas rechazadas."

- De esta forma, el nuevo modelo:
    * Leerá la memoria rígida en pocos tokens.
    * Asimilará las restricciones sin inventar ni re-explorar caminos fallidos.
    * Si necesita ver detalles de algún fallo previo, consultará los punteros de residual_metadata.json bajo demanda.
    * Continuará la tarea exactamente donde la dejaste.