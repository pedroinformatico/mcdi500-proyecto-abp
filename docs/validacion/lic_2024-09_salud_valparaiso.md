# Validación del dataset — MCDI500

**Archivo:** `lic_2024-09_salud_valparaiso.csv` · 2726 filas × 110 columnas

## Perfil de variables

| variable | dtype | rol | unicos | pct_nulos |
| --- | --- | --- | --- | --- |
| Codigo | int64 | discreta | 136 | 0.0 |
| Link | str | texto libre | 136 | 0.0 |
| CodigoExterno | str | alta cardinalidad | 136 | 0.0 |
| Nombre | str | texto libre | 134 | 0.0 |
| Descripcion | str | texto libre | 134 | 0.0 |
| CriteriosRequisitosAmbientales | str | nominal | 1 | 0.0 |
| DescripcionCriteriosRequisitosAmbientales | float64 | vacía | 0 | 100.0 |
| CriteriosRequisitosSociales | str | nominal | 1 | 0.0 |
| DescripcionCriteriosRequisitosSociales | float64 | vacía | 0 | 100.0 |
| DescripcionCriteriosRequisitosSociales.1 | float64 | vacía | 0 | 100.0 |
| CriteriosEvaluacion | str | texto libre | 99 | 17.3 |
| Tipo de Adquisicion | str | nominal | 6 | 0.0 |
| CodigoEstado | int64 | discreta | 5 | 0.0 |
| Estado | str | nominal | 4 | 0.0 |
| CodigoOrganismo | int64 | discreta | 21 | 0.0 |
| NombreOrganismo | str | alta cardinalidad | 21 | 0.0 |
| sector | str | nominal | 1 | 0.0 |
| RutUnidad | str | alta cardinalidad | 25 | 0.0 |
| CodigoUnidad | int64 | discreta | 29 | 0.0 |
| NombreUnidad | str | alta cardinalidad | 25 | 0.0 |
| DireccionUnidad | str | alta cardinalidad | 41 | 14.5 |
| ComunaUnidad | str | nominal | 15 | 14.5 |
| RegionUnidad | str | nominal | 1 | 0.0 |
| Informada | int64 | discreta | 1 | 0.0 |
| CodigoTipo | int64 | binaria | 2 | 0.0 |
| Tipo | str | nominal | 6 | 0.0 |
| TipoConvocatoria | int64 | binaria | 2 | 0.0 |
| CodigoMoneda | str | binaria | 2 | 0.0 |
| Moneda Adquisicion | str | binaria | 2 | 0.0 |
| Etapas | int64 | binaria | 2 | 0.0 |
| EstadoEtapas | int64 | binaria | 2 | 0.0 |
| TomaRazon | int64 | binaria | 2 | 0.0 |
| EstadoPublicidadOfertas | int64 | binaria | 2 | 0.0 |
| JustificacionPublicidad | str | texto libre | 1 | 82.7 |
| EstadoCS | int64 | binaria | 2 | 0.0 |
| Contrato | float64 | discreta | 3 | 2.1 |
| Obras | int64 | binaria | 2 | 0.0 |
| CantidadReclamos | int64 | discreta | 21 | 0.0 |
| FechaCreacion | str | fecha | 41 | 0.0 |
| FechaCierre | str | fecha | 29 | 0.0 |
| FechaInicio | str | fecha | 19 | 0.0 |
| FechaFinal | str | fecha | 27 | 0.0 |
| FechaPubRespuestas | str | fecha | 29 | 0.0 |
| FechaActoAperturaTecnica | str | fecha | 30 | 0.0 |
| FechaActoAperturaEconomica | str | fecha | 30 | 0.0 |
| FechaPublicacion | str | fecha | 19 | 0.0 |
| FechaAdjudicacion | str | fecha | 64 | 0.0 |
| FechaEstimadaAdjudicacion | str | fecha | 65 | 0.0 |
| FechaSoporteFisico | str | fecha | 4 | 0.0 |
| FechaTiempoEvaluacion | int64 | discreta | 3 | 0.0 |
| UnidadTiempoEvaluacion | str | binaria | 2 | 0.0 |
| FechaEstimadaFirma | str | fecha | 6 | 0.0 |
| FechasUsuario | int64 | discreta | 3 | 0.0 |
| FechaVisitaTerreno | str | fecha | 1 | 0.0 |
| DireccionVisita | str | fecha | 1 | 0.0 |
| FechaEntregaAntecedentes | str | fecha | 1 | 0.0 |
| DireccionEntrega | str | fecha | 1 | 0.0 |
| Estimacion | int64 | binaria | 2 | 0.0 |
| FuenteFinanciamiento | str | alta cardinalidad | 23 | 77.9 |
| VisibilidadMonto | int64 | binaria | 2 | 0.0 |
| MontoEstimado | str | alta cardinalidad | 111 | 0.0 |
| Tiempo | float64 | discreta | 14 | 50.7 |
| UnidadTiempo | str | nominal | 3 | 0.0 |
| Modalidad | str | nominal | 4 | 0.0 |
| TipoPago | int64 | discreta | 4 | 0.0 |
| ProhibicionContratacion | str | texto libre | 22 | 88.2 |
| SubContratacion | int64 | binaria | 2 | 0.0 |
| UnidadTiempoDuracionContrato | int64 | discreta | 4 | 0.0 |
| TiempoDuracionContrato | int64 | discreta | 15 | 0.0 |
| TipoDuracionContrato | float64 | vacía | 0 | 100.0 |
| JustificacionMontoEstimado | str | texto libre | 17 | 70.8 |
| ObservacionContrato | str | alta cardinalidad | 18 | 84.5 |
| ExtensionPlazo | int64 | binaria | 2 | 0.0 |
| EsBaseTipo | int64 | discreta | 1 | 0.0 |
| UnidadTiempoContratoLicitacion | int64 | discreta | 3 | 0.0 |
| PeriodoTiempoRenovacion | float64 | vacía | 0 | 100.0 |
| EsRenovable | int64 | discreta | 1 | 0.0 |
| TipoAprobacion | float64 | binaria | 2 | 4.2 |
| NumeroAprobacion | str | fecha | 120 | 4.2 |
| FechaAprobacion | str | fecha | 55 | 4.2 |
| NumeroOferentes | int64 | discreta | 20 | 0.0 |
| Correlativo | int64 | discreta | 47 | 0.0 |
| CodigoEstadoLicitacion | int64 | discreta | 5 | 0.0 |
| Codigoitem | int64 | continua | 680 | 0.0 |
| CodigoProductoONU | int64 | continua | 246 | 0.0 |
| Rubro1 | str | alta cardinalidad | 39 | 0.0 |
| Rubro2 | str | alta cardinalidad | 88 | 0.0 |
| Rubro3 | str | alta cardinalidad | 180 | 0.0 |
| Nombre producto genrico | str | alta cardinalidad | 246 | 0.0 |
| Nombre linea Adquisicion | str | alta cardinalidad | 246 | 0.0 |
| Descripcion linea Adquisicion | str | texto libre | 664 | 0.0 |
| UnidadMedida | str | alta cardinalidad | 18 | 0.0 |
| Cantidad | float64 | discreta | 120 | 0.0 |
| CodigoProveedor | int64 | continua | 437 | 0.0 |
| CodigoSucursalProveedor | int64 | continua | 441 | 0.0 |
| RutProveedor | str | alta cardinalidad | 437 | 0.0 |
| NombreProveedor | str | alta cardinalidad | 441 | 0.0 |
| RazonSocialProveedor | str | alta cardinalidad | 436 | 0.0 |
| DescripcionProveedor | str | texto libre | 2318 | 0.0 |
| Monto Estimado Adjudicado | str | alta cardinalidad | 124 | 1.9 |
| Nombre de la Oferta | str | alta cardinalidad | 556 | 0.0 |
| Estado Oferta | str | binaria | 2 | 0.0 |
| Cantidad Ofertada | float64 | discreta | 120 | 0.0 |
| Moneda de la Oferta | str | binaria | 2 | 0.0 |
| MontoUnitarioOferta | str | alta cardinalidad | 1716 | 0.0 |
| Valor Total Ofertado | str | alta cardinalidad | 2071 | 0.0 |
| CantidadAdjudicada | str | alta cardinalidad | 125 | 0.0 |
| MontoLineaAdjudica | str | alta cardinalidad | 486 | 0.0 |
| FechaEnvioOferta | str | fecha | 50 | 0.0 |
| Oferta seleccionada | str | binaria | 2 | 0.0 |

## Requisitos del curso

| estado | requisito | detalle |
| --- | --- | --- |
| OK | Al menos 2000 filas | 2726 filas |
| OK | Al menos 12 columnas | 110 columnas |
| OK | Combina al menos 3 roles analíticos | alta cardinalidad, discreta, binaria, fecha, nominal, texto libre, continua |
| OK | Al menos una variable numérica | 25 numéricas (continuas o discretas) |
| OK | Al menos una variable categórica | 29 categóricas (nominales, binarias u ordinales) |
| OK | Presencia de valores faltantes | máximo 100.0% en una variable |
| AVISO | Ninguna variable sobre 60% de faltantes | máximo 100.0% |
| OK | Incluye alguna variable de fecha | 19 detectadas |
| OK | Incluye texto o categórica de alta cardinalidad | 32 detectadas |
| OK | Archivo bajo 100 MB | 4.5 MB |
| AVISO | Sin filas duplicadas exactas | 3 duplicadas |

## Resultado

El conjunto **cumple** los requisitos mínimos.