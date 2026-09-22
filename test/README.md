# 🧪 Suite de Tests - Selenium Scraper Quickstarter

## 📊 Resumen de Cobertura

Total de tests: **61 tests** ✅

## 📁 Archivos de Test

### 1️⃣ `test_config.py` - 4 tests

Tests para verificar la configuración del proyecto:

- ✅ Existencia de variables de configuración
- ✅ Valores por defecto correctos
- ✅ Tipos de datos correctos
- ✅ Validación de valores positivos

**Cobertura:** `utils/config.py`

---

### 2️⃣ `test_security.py` - 8 tests 🔒

Tests para el sistema de autenticación Bearer Token:

- ✅ Autenticación con token válido
- ✅ Rechazo de token inválido
- ✅ Rechazo sin token (missing)
- ✅ Rechazo de token mal formado
- ✅ Rechazo de Bearer vacío
- ✅ Verificación case-sensitive del token
- ✅ Rechazo de tokens con espacios extra
- ✅ Rechazo de 'bearer' en minúsculas

**Cobertura:** `utils/security.py`

**Casos de uso probados:**

```python
✅ "Bearer sample"           # Válido
❌ "Bearer invalid_token"    # Inválido
❌ Sin header                # Unauthorized
❌ "sample"                  # Falta "Bearer "
❌ "bearer sample"           # Case-sensitive
```

---

### 3️⃣ `test_error.py` - 8 tests

Tests para el manejo de errores personalizados:

- ✅ Creación de excepciones messageError
- ✅ Herencia correcta de Exception
- ✅ Lanzamiento y captura de errores
- ✅ Manejo de mensajes vacíos
- ✅ Manejo de caracteres especiales
- ✅ Manejo de mensajes multilínea
- ✅ Verificación de herencia

**Cobertura:** `utils/error.py`

---

### 4️⃣ `test_file_manager.py` - 17 tests 📂

Tests para gestión de archivos y directorios:

- ✅ Creación de directorios de descarga
- ✅ Limpieza de nombres de archivo
- ✅ Limpieza de directorios completos
- ✅ Limpieza recursiva de subdirectorios
- ✅ Obtención de archivos desde Base64
- ✅ Obtención de archivos desde bytes
- ✅ Creación de archivos temporales
- ✅ Manejo de formatos inválidos
- ✅ Caracteres especiales y Unicode

**Cobertura:** `utils/file_manager.py`

**Funciones testeadas:**

- `create_download_directory()`
- `clear_directory()`
- `clean_filename()`
- `get_file()`
- `createTempFile()`

---

### 5️⃣ `test_handle_request.py` - 12 tests 🔄

Tests para el manejo de peticiones HTTP:

- ✅ Rechazo sin autenticación (401)
- ✅ Rechazo con token inválido (401)
- ✅ Rechazo sin body JSON (400)
- ✅ Rechazo con campos faltantes (400)
- ✅ Rechazo con JSON vacío (400)
- ✅ Validación de estructura de respuesta
- ✅ Inclusión de tiempo de ejecución
- ✅ Filtrado de passwords en logs
- ✅ Manejo de JSON mal formado
- ✅ Procesamiento con datos válidos
- ✅ Case-sensitivity de Bearer
- ✅ Validación de espacios extra

**Cobertura:** `utils/handle_request.py`

**Estructura de respuesta validada:**

```json
{
  "status": "OK|ERROR",
  "message": "...",
  "time": 0.123
}
```

---


Tests para el sistema de logging y rotación:

- ✅ Importación correcta de configuración
- ✅ Limpieza de registros antiguos
- ✅ Eliminación de archivos vacíos
- ✅ Rotación de logs cuando son muy antiguos
- ✅ Preservación de logs recientes
- ✅ Preservación de contenido al rotar
- ✅ Manejo de múltiples archivos
- ✅ Manejo de timestamps mezclados


---

### 7️⃣ `test_main.py` - 3 tests 🚀

Tests para endpoints de la API Flask:

- ✅ Endpoint raíz de health check
- ✅ Endpoint /sample sin autenticación
- ✅ Endpoint /sample con datos faltantes

**Cobertura:** `main.py`

**Nota:** Los tests de Selenium se omiten en CI/CD porque requieren ChromeDriver.

---

## 🚀 Ejecutar Tests

### Todos los tests

```bash
pytest test/ -v
```

### Con reporte de cobertura

```bash
pytest test/ --cov=. --cov-report=html
```

### Test específico

```bash
pytest test/test_security.py -v
pytest test/test_file_manager.py::test_clean_filename_basic -v
```

### Tests con output detallado

```bash
pytest test/ -v --tb=short
```

---

## 📈 Componentes Testeados

| Componente | Archivo de Test | Tests | Estado |
|------------|-----------------|-------|--------|
| Configuración | test_config.py | 4 | ✅ |
| Autenticación | test_security.py | 8 | ✅ |
| Manejo de Errores | test_error.py | 8 | ✅ |
| Gestión de Archivos | test_file_manager.py | 17 | ✅ |
| Manejo de Requests | test_handle_request.py | 12 | ✅ |
| API Flask | test_main.py | 3 | ✅ |
| **TOTAL** | **7 archivos** | **61** | **✅** |

---

## 🔍 Componentes sin Tests

Los siguientes componentes **NO** tienen tests porque requieren Selenium/ChromeDriver:

- ❌ `actions/click_element.py`
- ❌ `actions/login.py`
- ❌ `actions/search_element.py`
- ❌ `actions/web_driver.py`
- ❌ `actions/write_element.py`
- ❌ `controller/controller_sample.py`

Para testear estos componentes, se recomienda:

1. Usar mocks de Selenium
2. Usar un entorno con ChromeDriver instalado
3. Tests de integración E2E separados

---

## 🎯 Mejores Prácticas Implementadas

✅ **Fixtures de pytest** - Reutilización de configuración  
✅ **Tests aislados** - Cada test es independiente  
✅ **Archivos temporales** - Uso de `tempfile` para tests de archivos  
✅ **Context managers** - Limpieza automática de recursos  
✅ **Nombres descriptivos** - Tests fáciles de entender  
✅ **Documentación** - Docstrings en cada test  
✅ **Cobertura completa** - Tests positivos y negativos  

---

## 🐛 Debug de Tests

Si un test falla:

```bash
# Ver traceback completo
pytest test/test_security.py -v --tb=long

# Ver solo el último test que falló
pytest test/ --lf

# Ejecutar hasta el primer fallo
pytest test/ -x

# Modo verbose con prints
pytest test/ -v -s
```

---

## 📝 Notas

- Los tests utilizan `pytest` como framework
- Se utiliza `Flask.test_client()` para tests de endpoints
- Los archivos temporales se limpian automáticamente
- Los tests no requieren configuración externa (.env)
- Compatible con CI/CD (GitHub Actions)

---

**Última actualización:** 2025-12-19  
**Total de tests:** 61 ✅  
**Tasa de éxito:** 100% 🎉
