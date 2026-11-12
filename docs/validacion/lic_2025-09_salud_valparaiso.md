# Validación del dataset — MCDI500

**Archivo:** `lic_2025-09_salud_valparaiso.csv` · 2361 filas × 110 columnas

## Perfil de variables

| variable | dtype | rol | unicos | pct_nulos |
| --- | --- | --- | --- | --- |
| Codigo | int64 | continua | 130 | 0.0 |
| Link | str | texto libre | 130 | 0.0 |
| CodigoExterno | str | alta cardinalidad | 130 | 0.0 |
| Nombre | str | texto libre | 129 | 0.0 |
| Descripcion | str | texto libre | 119 | 0.0 |
| CriteriosRequisitosAmbientales | str | binaria | 2 | 0.0 |
| DescripcionCriteriosRequisitosAmbientales | str | nominal | 5 | 67.6 |
| CriteriosRequisitosSociales | str | nominal | 1 | 0.0 |
| DescripcionCriteriosRequisitosSociales | str | nominal | 1 | 67.8 |
| DescripcionCriteriosRequisitosSociales.1 | str | nominal | 1 | 67.8 |
| CriteriosEvaluacion | str | texto libre | 117 | 3.0 |
| Tipo de Adquisicion | str | nominal | 6 | 0.0 |
| CodigoEstado | int64 | discreta | 5 | 0.0 |
| Estado | str | nominal | 4 | 0.0 |
| CodigoOrganismo | int64 | discreta | 19 | 0.0 |
| NombreOrganismo | str | alta cardinalidad | 18 | 0.0 |
| sector | str | nominal | 1 | 0.0 |
| RutUnidad | str | alta cardinalidad | 23 | 0.0 |
| CodigoUnidad | int64 | discreta | 28 | 0.0 |
| NombreUnidad | str | alta cardinalidad | 27 | 0.0 |
| DireccionUnidad | str | alta cardinalidad | 34 | 4.8 |
| ComunaUnidad | str | alta cardinalidad | 16 | 4.8 |
| RegionUnidad | str | nominal | 1 | 0.0 |
| Informada | int64 | discreta | 1 | 0.0 |
| CodigoTipo | int64 | binaria | 2 | 0.0 |
| Tipo | str | nominal | 6 | 0.0 |
| TipoConvocatoria | int64 | binaria | 2 | 0.0 |
| CodigoMoneda | str | binaria | 2 | 0.0 |
| Moneda Adquisicion | str | binaria | 2 | 0.0 |
| Etapas | int64 | binaria | 2 | 0.0 |
| EstadoEtapas | int64 | binaria | 2 | 0.0 |
| TomaRazon | int64 | discreta | 1 | 0.0 |
| EstadoPublicidadOfertas | int64 | binaria | 2 | 0.0 |
| JustificacionPublicidad | str | texto libre | 1 | 97.0 |
| EstadoCS | int64 | binaria | 2 | 0.0 |
| Contrato | float64 | discreta | 3 | 0.5 |
| Obras | int64 | binaria | 2 | 0.0 |
| CantidadReclamos | int64 | discreta | 19 | 0.0 |
| FechaCreacion | str | fecha | 53 | 0.0 |
| FechaCierre | str | fecha | 30 | 0.0 |
| FechaInicio | str | fecha | 22 | 0.0 |
| FechaFinal | str | fecha | 32 | 0.0 |
| FechaPubRespuestas | str | fecha | 29 | 0.0 |
| FechaActoAperturaTecnica | str | fecha | 30 | 0.0 |
| FechaActoAperturaEconomica | str | fecha | 30 | 0.0 |
| FechaPublicacion | str | fecha | 21 | 0.0 |
| FechaAdjudicacion | str | fecha | 63 | 0.0 |
| FechaEstimadaAdjudicacion | str | fecha | 57 | 0.0 |
| FechaSoporteFisico | str | fecha | 3 | 0.0 |
| FechaTiempoEvaluacion | int64 | discreta | 4 | 0.0 |
| UnidadTiempoEvaluacion | str | binaria | 2 | 3.9 |
| FechaEstimadaFirma | str | fecha | 4 | 0.0 |
| FechasUsuario | int64 | discreta | 3 | 0.0 |
| FechaVisitaTerreno | str | fecha | 1 | 0.0 |
| DireccionVisita | str | fecha | 1 | 0.0 |
| FechaEntregaAntecedentes | str | fecha | 1 | 0.0 |
| DireccionEntrega | str | fecha | 1 | 0.0 |
| Estimacion | int64 | binaria | 2 | 0.0 |
| FuenteFinanciamiento | str | alta cardinalidad | 30 | 42.8 |
| VisibilidadMonto | int64 | binaria | 2 | 0.0 |
| MontoEstimado | str | alta cardinalidad | 104 | 0.0 |
| Tiempo | float64 | discreta | 13 | 25.3 |
| UnidadTiempo | str | nominal | 3 | 0.0 |
| Modalidad | str | nominal | 3 | 0.0 |
| TipoPago | int64 | discreta | 4 | 0.0 |
| ProhibicionContratacion | str | texto libre | 22 | 87.9 |
| SubContratacion | int64 | binaria | 2 | 0.0 |
| UnidadTiempoDuracionContrato | int64 | discreta | 3 | 0.0 |
| TiempoDuracionContrato | int64 | discreta | 14 | 0.0 |
| TipoDuracionContrato | str | nominal | 1 | 99.5 |
| JustificacionMontoEstimado | str | texto libre | 26 | 54.8 |
| ObservacionContrato | str | texto libre | 23 | 70.2 |
| ExtensionPlazo | int64 | binaria | 2 | 0.0 |
| EsBaseTipo | int64 | discreta | 1 | 0.0 |
| UnidadTiempoContratoLicitacion | int64 | discreta | 3 | 0.0 |
| PeriodoTiempoRenovacion | float64 | vacía | 0 | 100.0 |
| EsRenovable | int64 | discreta | 1 | 0.0 |
| TipoAprobacion | float64 | discreta | 3 | 4.1 |
| NumeroAprobacion | str | alta cardinalidad | 121 | 4.1 |
| FechaAprobacion | str | fecha | 53 | 4.1 |
| NumeroOferentes | int64 | discreta | 20 | 0.0 |
| Correlativo | int64 | discreta | 81 | 0.0 |
| CodigoEstadoLicitacion | int64 | discreta | 5 | 0.0 |
| Codigoitem | int64 | continua | 703 | 0.0 |
| CodigoProductoONU | int64 | continua | 266 | 0.0 |
| Rubro1 | str | alta cardinalidad | 37 | 0.0 |
| Rubro2 | str | alta cardinalidad | 87 | 0.0 |
| Rubro3 | str | alta cardinalidad | 190 | 0.0 |
| Nombre producto genrico | str | alta cardinalidad | 266 | 0.0 |
| Nombre linea Adquisicion | str | alta cardinalidad | 266 | 0.0 |
| Descripcion linea Adquisicion | str | texto libre | 693 | 0.1 |
| UnidadMedida | str | nominal | 15 | 0.0 |
| Cantidad | int64 | continua | 161 | 0.0 |
| CodigoProveedor | int64 | continua | 383 | 0.0 |
| CodigoSucursalProveedor | int64 | continua | 386 | 0.0 |
| RutProveedor | str | alta cardinalidad | 383 | 0.0 |
| NombreProveedor | str | alta cardinalidad | 386 | 0.0 |
| RazonSocialProveedor | str | alta cardinalidad | 383 | 0.0 |
| DescripcionProveedor | str | texto libre | 2134 | 0.0 |
| Monto Estimado Adjudicado | str | alta cardinalidad | 114 | 1.2 |
| Nombre de la Oferta | str | alta cardinalidad | 483 | 0.0 |
| Estado Oferta | str | binaria | 2 | 0.0 |
| Cantidad Ofertada | int64 | continua | 161 | 0.0 |
| Moneda de la Oferta | str | binaria | 2 | 0.0 |
| MontoUnitarioOferta | str | alta cardinalidad | 1316 | 0.0 |
| Valor Total Ofertado | str | alta cardinalidad | 1629 | 0.0 |
| CantidadAdjudicada | str | alta cardinalidad | 173 | 0.0 |
| MontoLineaAdjudica | str | alta cardinalidad | 516 | 0.0 |
| FechaEnvioOferta | str | fecha | 50 | 0.0 |
| Oferta seleccionada | str | binaria | 2 | 0.0 |

## Requisitos del curso

| estado | requisito | detalle |
| --- | --- | --- |
| OK | Al menos 2000 filas | 2361 filas |
| OK | Al menos 12 columnas | 110 columnas |
| OK | Combina al menos 3 roles analíticos | alta cardinalidad, discreta, binaria, fecha, nominal, texto libre, continua |
| OK | Al menos una variable numérica | 27 numéricas (continuas o discretas) |
| OK | Al menos una variable categórica | 31 categóricas (nominales, binarias u ordinales) |
| OK | Presencia de valores faltantes | máximo 100.0% en una variable |
| AVISO | Ninguna variable sobre 60% de faltantes | máximo 100.0% |
| OK | Incluye alguna variable de fecha | 18 detectadas |
| OK | Incluye texto o categórica de alta cardinalidad | 33 detectadas |
| OK | Archivo bajo 100 MB | 4.1 MB |
| OK | Sin filas duplicadas exactas | ninguna |

## Resultado

El conjunto **cumple** los requisitos mínimos.