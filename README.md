# Sitio web Innovahub — versión beta 0.2

Implementación en HTML, CSS y JavaScript planos del wireframe **"Wireframe Web Innovahub v2 sobrio"** (Claude Design, 13 artboards), ya con imágenes, ilustraciones, mapa y logos. No requiere servidor ni proceso de build para verse: basta abrir `index.html` en el navegador.

## Páginas

| Archivo | Artboards que implementa |
|---------|--------------------------|
| `index.html` | 01 Home desktop · 02 Home móvil |
| `servicio-formacion-virtual.html` | 03 / 04 Página de servicio (plantilla, con Formación virtual como ejemplo) |
| `casos.html` | 05 / 06 Casos de éxito, portafolio filtrable con estado vacío y hoja de filtros en móvil |
| `caso-ciclo-genero.html` | 07 Detalle de caso (Ciclo de Género, Rama Judicial) |
| `como-trabajamos.html` | 08 Cómo trabajamos (ciclo orbital + tabla de tres columnas) |
| `nosotros.html` | 09 Nosotros |
| `contacto.html` | 10 / 11 Contacto |
| — | 12 Hero en inglés: no se implementa como página; el layout resiste titulares largos por diseño |
| `assets/css/styles.css` | 13 Sistema de componentes (tokens, botones, chips, tarjetas, acordeón, formulario) |

## Estructura

```
beta/
├── index.html … contacto.html    ← páginas generadas (no editar a mano)
├── build.py                      ← ensambla src/pages + src/partials → raíz e inserta el mapa ({{MAPA}})
├── src/
│   ├── partials/ head.html · header.html · footer.html · mapa.svg (generado)
│   └── pages/    una por página, con línea de metadatos al inicio
├── tools/
│   ├── make_map.py         ← mapa Equal Earth de los 13 países desde TopoJSON world-atlas 110m
│   ├── voxel.py            ← ilustraciones isométricas voxel y avatares (SVG)
│   ├── brochure_assets.py  ← recupera los íconos 3D oficiales del brochure con transparencia
│   ├── case_images.py      ← compone las imágenes 16:10 de los casos (1200×750)
│   └── preview-assets.html ← tablero de revisión de activos
└── assets/
    ├── css/styles.css
    ├── js/main.js
    ├── img/
    │   ├── ilustraciones/  hero-hub · aula-virtual · equipo · avatar-1…6 (SVG)
    │   ├── marca/          íconos 3D oficiales (formación, diagnóstico, sistematización, producción, plataformas), escena, isologo, globo, esfera
    │   ├── casos/          18 imágenes de productos reales
    │   ├── aliados/        undp · unicef · wwf · idb (SVG)
    │   └── mapa-13-paises.svg
    └── docs/ brochure-innovahub.pdf
```

Para editar una página, modifica `src/pages/<página>.html` o un parcial y ejecuta `python build.py`. Para regenerar activos: `python tools/make_map.py`, `python tools/voxel.py`, `python tools/brochure_assets.py`, `python tools/case_images.py` (estos dos últimos leen `../Brochure-IH-fundaciones.pdf` y `../_fuentes/`).

## Activos visuales y su origen

| Activo | Origen | Estado |
|--------|--------|--------|
| Ilustraciones voxel (hero, aula virtual, equipo) | Generadas a código en SVG siguiendo la línea "escenarios isométricos voxelados" del manual | Definitivas o reemplazables por render 3D con el prompt del manual |
| Íconos 3D de las 5 líneas de servicio | Recuperados del brochure oficial (JPEG + máscara → PNG transparente) | Oficiales; resolución ~300 px, suficiente para 76 px |
| Mapa de 13 países | SVG generado con proyección Equal Earth; puntos en las capitales con tooltip y pulso | Definitivo |
| Capturas de casos | Sitios publicados: EJRLB (wireframe público), WWF LFA, Atlas UNDP, Banco de experiencias, Infosegura, campus, Genially, YouTube | Definitivas |
| Portadas y fotogramas de casos | Extraídos del brochure (≈300 px) y compuestos sobre fondo de marca | Reemplazar por originales en alta cuando se ubiquen |
| Avatares del equipo | Personajes voxel SVG con seis variantes | Provisionales; el manual define personajes 3D generados a partir de fotos |
| Logos de aliados | PNUD, UNICEF, WWF y BID en SVG (Wikimedia Commons); ONU Mujeres, OIM y OPS como marca tipográfica | Completar con los logos oficiales que entregue cada organización |

## Interacciones implementadas

- Header sticky que se compacta al hacer scroll; menú Servicios desplegable; menú hamburguesa en móvil con el CTA siempre visible.
- Contadores de cifras que suben al entrar en viewport; timeline de cinco pasos que se ilumina paso a paso; ilustraciones con flotación suave; puntos del mapa con pulso y tooltip por país.
- Acordeones accesibles (primer ítem abierto) en "Cómo lo hacemos" y FAQ.
- Portafolio: filtros combinables por línea, sector y país, buscador, contador de resultados, estado vacío, chips activos y hoja inferior en móvil. Los accesos por audiencia del home aterrizan con el filtro aplicado (`casos.html?sector=cooperacion`).
- Ciclo orbital: al pasar el cursor o enfocar un nodo se resalta su fila en la tabla.
- Formulario de contacto con validación por campo, estados de foco y error, y mensajes de éxito y error.
- Accesibilidad: enlace "ir al contenido", foco visible en Keppel, `aria-pressed` en filtros, `aria-expanded` en acordeones y menús, áreas táctiles de 44 px, `prefers-reduced-motion` respetado, textos alternativos descriptivos en todas las imágenes.

## Pendientes para pasar de beta a producción

1. **Fichas de los otros 11 casos** y **páginas de las otras 4 líneas de servicio**. La plantilla ya existe; solo cambia contenido, color de hero e ilustración.
2. **Datos de contacto por confirmar:** correo `contacto@innovahub.org`, número de WhatsApp, enlace de agenda, redes sociales y política de tratamiento de datos.
3. **Envío real del formulario** (hoy solo valida en el navegador). Opciones: Formspree, función serverless o backend propio.
4. **Testimonios reales** en el home y en la ficha de caso.
5. **Nombres y avatares del equipo**, logos oficiales de ONU Mujeres, OIM y OPS, y originales en alta de las portadas del brochure.
6. **Versión en inglés.** El selector ES | EN está presente pero deshabilitado.
7. **Tipografía Proxima Nova.** El manual la define para titulares; la beta usa Montserrat desde Google Fonts porque Proxima Nova requiere licencia. Al contar con los archivos, cambiar `--font-titulos` en `styles.css`.
8. Quitar la etiqueta "BETA" del pie (`.beta-nota` en el parcial `footer.html`).

## Verificación realizada

Capturas con Chrome headless a 1440 px y 500 px de todas las páginas (`../_capturas/`). Sintaxis de JavaScript verificada con `node --check`.
