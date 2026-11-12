# Validación del dataset — MCDI500

**Archivo:** `oc_2025-09_salud_valparaiso.csv` · 13855 filas × 79 columnas

## Perfil de variables

| variable | dtype | rol | unicos | pct_nulos |
| --- | --- | --- | --- | --- |
| ID | int64 | continua | 5687 | 0.0 |
| Codigo | str | alta cardinalidad | 5687 | 0.0 |
| Link | str | texto libre | 5687 | 0.0 |
| Nombre | str | alta cardinalidad | 5049 | 0.0 |
| Descripcion/Obervaciones | str | texto libre | 4090 | 0.0 |
| Tipo | str | nominal | 5 | 0.0 |
| ProcedenciaOC | str | alta cardinalidad | 19 | 38.0 |
| EsTratoDirecto | str | binaria | 2 | 38.0 |
| EsCompraAgil | str | binaria | 2 | 0.0 |
| CodigoTipo | int64 | discreta | 5 | 0.0 |
| CodigoAbreviadoTipoOC | str | nominal | 5 | 0.0 |
| DescripcionTipoOC | str | nominal | 5 | 0.0 |
| CodigoProyectoPlanAnualCompras | str | alta cardinalidad | 325 | 36.7 |
| codigoEstado | int64 | discreta | 5 | 0.0 |
| Estado | str | nominal | 5 | 0.0 |
| codigoEstadoProveedor | int64 | discreta | 5 | 0.0 |
| EstadoProveedor | str | nominal | 5 | 0.0 |
| FechaCreacion | str | fecha | 120 | 0.0 |
| FechaEnvio | str | fecha | 25 | 0.0 |
| FechaSolicitudCancelacion | str | fecha | 107 | 3.9 |
| fechaUltimaModificacion | str | fecha | 181 | 0.0 |
| FechaAceptacion | str | fecha | 100 | 1.7 |
| FechaCancelacion | str | fecha | 1 | 100.0 |
| tieneItems | int64 | discreta | 1 | 0.0 |
| PromedioCalificacion | str | alta cardinalidad | 181 | 0.0 |
| CantidadEvaluacion | int64 | discreta | 60 | 0.0 |
| MontoTotalOC | str | alta cardinalidad | 4315 | 0.0 |
| TipoMonedaOC | str | nominal | 3 | 0.0 |
| MontoTotalOC_PesosChilenos | str | alta cardinalidad | 4318 | 0.0 |
| Impuestos | str | alta cardinalidad | 3781 | 0.0 |
| TipoImpuesto | str | nominal | 3 | 0.0 |
| Descuentos | str | alta cardinalidad | 30 | 0.0 |
| Cargos | object | alta cardinalidad | 73 | 0.0 |
| TotalNetoOC | str | alta cardinalidad | 4182 | 0.0 |
| CodigoUnidadCompra | int64 | discreta | 53 | 0.0 |
| RutUnidadCompra | str | alta cardinalidad | 35 | 0.0 |
| UnidadCompra | str | alta cardinalidad | 47 | 0.0 |
| CodigoOrganismoPublico | int64 | discreta | 30 | 0.0 |
| OrganismoPublico | str | alta cardinalidad | 29 | 0.0 |
| sector | str | nominal | 1 | 0.0 |
| ActividadComprador | str | alta cardinalidad | 23 | 21.7 |
| CiudadUnidadCompra | str | alta cardinalidad | 32 | 0.0 |
| RegionUnidadCompra | str | binaria | 2 | 0.0 |
| PaisUnidadCompra | str | nominal | 3 | 10.5 |
| CodigoSucursal | int64 | continua | 1677 | 0.0 |
| RutSucursal | str | alta cardinalidad | 1634 | 0.0 |
| Sucursal | str | alta cardinalidad | 1706 | 0.0 |
| CodigoProveedor | int64 | continua | 1634 | 0.0 |
| NombreProveedor | str | alta cardinalidad | 1632 | 0.0 |
| ActividadProveedor | str | texto libre | 969 | 0.4 |
| ComunaProveedor | str | alta cardinalidad | 144 | 14.2 |
| RegionProveedor | str | alta cardinalidad | 17 | 15.7 |
| PaisProveedor | str | binaria | 2 | 53.8 |
| Financiamiento | str | fecha | 1173 | 74.2 |
| PorcentajeIva | str | nominal | 4 | 0.0 |
| Pais | str | nominal | 3 | 10.5 |
| TipoDespacho | int64 | discreta | 4 | 0.0 |
| FormaPago | int64 | discreta | 3 | 0.0 |
| CodigoLicitacion | str | alta cardinalidad | 1020 | 67.4 |
| Codigo_ConvenioMarco | str | nominal | 11 | 85.2 |
| IDItem | int64 | identificador | 13855 | 0.0 |
| codigoCategoria | float64 | continua | 814 | 14.8 |
| Categoria | str | texto libre | 820 | 14.8 |
| codigoProductoONU | int64 | continua | 2144 | 0.0 |
| NombreroductoGenerico | str | alta cardinalidad | 3363 | 0.0 |
| RubroN1 | str | alta cardinalidad | 55 | 14.8 |
| RubroN2 | str | alta cardinalidad | 238 | 14.8 |
| RubroN3 | str | alta cardinalidad | 820 | 14.8 |
| EspecificacionComprador | str | texto libre | 12074 | 0.4 |
| EspecificacionProveedor | str | texto libre | 9998 | 19.2 |
| cantidad | str | alta cardinalidad | 821 | 0.0 |
| UnidadMedida | str | alta cardinalidad | 65 | 14.8 |
| monedaItem | str | nominal | 3 | 0.0 |
| precioNeto | str | alta cardinalidad | 6042 | 0.0 |
| totalCargos | int64 | discreta | 1 | 0.0 |
| totalDescuentos | int64 | discreta | 1 | 0.0 |
| totalImpuestos | float64 | discreta | 1 | 50.9 |
| totalLineaNeto | str | alta cardinalidad | 8429 | 0.0 |
| Forma de Pago | str | binaria | 2 | 12.8 |

## Requisitos del curso

| estado | requisito | detalle |
| --- | --- | --- |
| OK | Al menos 2000 filas | 13855 filas |
| OK | Al menos 12 columnas | 79 columnas |
| OK | Combina al menos 3 roles analíticos | alta cardinalidad, nominal, discreta, fecha, texto libre, continua, binaria |
| OK | Al menos una variable numérica | 17 numéricas (continuas o discretas) |
| OK | Al menos una variable categórica | 18 categóricas (nominales, binarias u ordinales) |
| OK | Presencia de valores faltantes | máximo 100.0% en una variable |
| AVISO | Ninguna variable sobre 60% de faltantes | máximo 100.0% |
| OK | Incluye alguna variable de fecha | 7 detectadas |
| OK | Incluye texto o categórica de alta cardinalidad | 36 detectadas |
| OK | Archivo bajo 100 MB | 22.8 MB |
| OK | Sin filas duplicadas exactas | ninguna |

## Resultado

El conjunto **cumple** los requisitos mínimos.