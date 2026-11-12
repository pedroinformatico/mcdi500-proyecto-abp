# Validación del dataset — MCDI500

**Archivo:** `oc_2024-09_salud_valparaiso.csv` · 12025 filas × 78 columnas

## Perfil de variables

| variable | dtype | rol | unicos | pct_nulos |
| --- | --- | --- | --- | --- |
| ID | int64 | continua | 4598 | 0.0 |
| Codigo | str | alta cardinalidad | 4598 | 0.0 |
| Link | str | texto libre | 4598 | 0.0 |
| Nombre | str | alta cardinalidad | 4024 | 0.0 |
| Descripcion/Obervaciones | str | texto libre | 3596 | 0.6 |
| Tipo | str | nominal | 4 | 0.0 |
| ProcedenciaOC | str | alta cardinalidad | 17 | 0.0 |
| EsTratoDirecto | str | binaria | 2 | 0.0 |
| EsCompraAgil | str | binaria | 2 | 0.0 |
| CodigoTipo | int64 | discreta | 4 | 0.0 |
| CodigoAbreviadoTipoOC | str | nominal | 4 | 0.0 |
| DescripcionTipoOC | str | nominal | 4 | 0.0 |
| codigoEstado | int64 | discreta | 5 | 0.0 |
| Estado | str | nominal | 5 | 0.0 |
| codigoEstadoProveedor | int64 | discreta | 5 | 0.0 |
| EstadoProveedor | str | nominal | 5 | 0.0 |
| FechaCreacion | str | fecha | 100 | 0.0 |
| FechaEnvio | str | fecha | 25 | 0.0 |
| FechaSolicitudCancelacion | str | fecha | 84 | 0.0 |
| fechaUltimaModificacion | str | fecha | 161 | 0.0 |
| FechaAceptacion | str | fecha | 86 | 2.2 |
| FechaCancelacion | float64 | vacía | 0 | 100.0 |
| tieneItems | int64 | discreta | 1 | 0.0 |
| PromedioCalificacion | str | alta cardinalidad | 188 | 0.0 |
| CantidadEvaluacion | int64 | discreta | 68 | 0.0 |
| MontoTotalOC | str | alta cardinalidad | 3535 | 0.0 |
| TipoMonedaOC | str | nominal | 4 | 0.0 |
| MontoTotalOC_PesosChilenos | str | alta cardinalidad | 3535 | 0.0 |
| Impuestos | str | alta cardinalidad | 3047 | 0.0 |
| TipoImpuesto | str | nominal | 4 | 0.0 |
| Descuentos | str | alta cardinalidad | 19 | 0.0 |
| Cargos | object | alta cardinalidad | 73 | 0.0 |
| TotalNetoOC | str | alta cardinalidad | 3437 | 0.0 |
| CodigoUnidadCompra | int64 | discreta | 47 | 0.0 |
| RutUnidadCompra | str | alta cardinalidad | 32 | 0.0 |
| UnidadCompra | str | alta cardinalidad | 43 | 0.0 |
| CodigoOrganismoPublico | int64 | discreta | 29 | 0.0 |
| OrganismoPublico | str | alta cardinalidad | 28 | 0.0 |
| sector | str | nominal | 1 | 0.0 |
| ActividadComprador | str | alta cardinalidad | 19 | 16.6 |
| CiudadUnidadCompra | str | alta cardinalidad | 35 | 0.0 |
| RegionUnidadCompra | str | nominal | 1 | 0.0 |
| PaisUnidadCompra | str | nominal | 3 | 4.6 |
| CodigoSucursal | int64 | continua | 1528 | 0.0 |
| RutSucursal | str | alta cardinalidad | 1475 | 0.0 |
| Sucursal | str | alta cardinalidad | 1550 | 0.0 |
| CodigoProveedor | int64 | continua | 1476 | 0.0 |
| NombreProveedor | str | alta cardinalidad | 1476 | 0.0 |
| ActividadProveedor | str | texto libre | 945 | 0.3 |
| ComunaProveedor | str | alta cardinalidad | 126 | 16.4 |
| RegionProveedor | str | alta cardinalidad | 16 | 16.5 |
| PaisProveedor | str | binaria | 2 | 38.8 |
| Financiamiento | str | fecha | 931 | 71.2 |
| PorcentajeIva | str | nominal | 4 | 0.0 |
| Pais | str | nominal | 3 | 4.6 |
| TipoDespacho | int64 | discreta | 6 | 0.0 |
| FormaPago | int64 | discreta | 4 | 0.0 |
| CodigoLicitacion | str | alta cardinalidad | 898 | 66.9 |
| Codigo_ConvenioMarco | str | nominal | 9 | 84.9 |
| IDItem | int64 | identificador | 12025 | 0.0 |
| codigoCategoria | float64 | continua | 789 | 15.1 |
| Categoria | str | texto libre | 792 | 15.1 |
| codigoProductoONU | int64 | continua | 1971 | 0.0 |
| NombreroductoGenerico | str | alta cardinalidad | 2910 | 0.0 |
| RubroN1 | str | alta cardinalidad | 52 | 15.1 |
| RubroN2 | str | alta cardinalidad | 229 | 15.1 |
| RubroN3 | str | alta cardinalidad | 792 | 15.1 |
| EspecificacionComprador | str | texto libre | 10204 | 1.4 |
| EspecificacionProveedor | str | texto libre | 8980 | 16.3 |
| cantidad | str | alta cardinalidad | 701 | 0.0 |
| UnidadMedida | str | alta cardinalidad | 61 | 15.1 |
| monedaItem | str | nominal | 4 | 0.0 |
| precioNeto | str | alta cardinalidad | 5406 | 0.0 |
| totalCargos | int64 | discreta | 1 | 0.0 |
| totalDescuentos | int64 | discreta | 1 | 0.0 |
| totalImpuestos | float64 | binaria | 2 | 32.9 |
| totalLineaNeto | str | alta cardinalidad | 7330 | 0.0 |
| Forma de Pago | str | binaria | 2 | 9.2 |

## Requisitos del curso

| estado | requisito | detalle |
| --- | --- | --- |
| OK | Al menos 2000 filas | 12025 filas |
| OK | Al menos 12 columnas | 78 columnas |
| OK | Combina al menos 3 roles analíticos | alta cardinalidad, nominal, discreta, texto libre, fecha, continua, binaria |
| OK | Al menos una variable numérica | 16 numéricas (continuas o discretas) |
| OK | Al menos una variable categórica | 19 categóricas (nominales, binarias u ordinales) |
| OK | Presencia de valores faltantes | máximo 100.0% en una variable |
| AVISO | Ninguna variable sobre 60% de faltantes | máximo 100.0% |
| OK | Incluye alguna variable de fecha | 6 detectadas |
| OK | Incluye texto o categórica de alta cardinalidad | 35 detectadas |
| OK | Archivo bajo 100 MB | 19.8 MB |
| OK | Sin filas duplicadas exactas | ninguna |

## Resultado

El conjunto **cumple** los requisitos mínimos.