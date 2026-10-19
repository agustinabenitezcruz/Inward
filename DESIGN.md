---
version: 1
name: INWARD
description: Sistema de diseño de INWARD, consultora de inmigración y movilidad internacional en Francia. Fondo blanco, un único acento violeta oscuro #202045 tomado de la paleta primaria del brand book, y dos tintes ácidos (verde agua y amarillo) que aparecen sólo como fondo de celdas del bento. La geometría es rectángulo con esquinas redondeadas en una sola escala. La tipografía combina un display geométrico de x-height alta con un cuerpo tipo Futura. El ritmo lo da la alternancia entre blanco y el gris #eeeeee del brand book, nunca un fondo saturado: el violeta es acento, jamás fondo de sección. Serio pero luminoso, nunca corporativo azul-genérico.

brand:
  isotipo: hexágono (alusión al perímetro de Francia) con una flecha entrando
  fuente-de-verdad: assets/css/styles.css, bloque :root
  regla: ningún componente escribe un color a mano, todo sale de un token

colors:
  ground: "#ffffff"
  surface: "#eeeeee"
  surface-2: "#e3e3e6"
  text: "#101010"
  text-2: "#4d4d6b"
  text-3: "#71718f"
  accent: "#202045"
  on-accent: "#ffffff"
  accent-soft: "rgba(32,32,69,.09)"
  fill: "#202045"
  fill-hi: "#15152e"
  fill-ink: "#ffffff"
  line: "rgba(32,32,69,.15)"
  line-strong: "rgba(32,32,69,.3)"
  tint-1: "#55ffd2"
  tint-2: "#ebff76"
  tint-ink: "#101010"
  alt: "#eeeeee"
  alt-ink: "#101010"
  alt-ink-2: "#4d4d6b"
  alt-accent: "#202045"
  alt-label: "#71718f"

typography:
  display-xl:
    fontFamily: "Outfit, Figerona, 'Helvetica Neue', Arial, sans-serif"
    fontSize: "clamp(2.15rem, 3.9vw, 3.55rem)"
    fontWeight: 500
    lineHeight: 1.04
    letterSpacing: "-0.032em"
  display-lg:
    fontFamily: "Outfit, Figerona, 'Helvetica Neue', Arial, sans-serif"
    fontSize: "clamp(1.95rem, 3.4vw, 3rem)"
    fontWeight: 500
    lineHeight: 1.06
    letterSpacing: "-0.026em"
  heading-sm:
    fontFamily: "Outfit, Figerona, 'Helvetica Neue', Arial, sans-serif"
    fontSize: "clamp(1.1rem, 1.45vw, 1.3rem)"
    fontWeight: 500
    lineHeight: 1.26
    letterSpacing: "-0.012em"
  lead:
    fontFamily: "Jost, Walkway, 'Helvetica Neue', Arial, sans-serif"
    fontSize: "clamp(1.05rem, 1.4vw, 1.28rem)"
    fontWeight: 300
    lineHeight: 1.55
  body:
    fontFamily: "Jost, Walkway, 'Helvetica Neue', Arial, sans-serif"
    fontSize: 17px
    fontWeight: 400
    lineHeight: 1.62
  body-sm:
    fontFamily: "Jost, Walkway, 'Helvetica Neue', Arial, sans-serif"
    fontSize: "0.96rem"
    lineHeight: 1.6
  label:
    fontFamily: "Jost, Walkway, 'Helvetica Neue', Arial, sans-serif"
    fontSize: "0.7rem"
    fontWeight: 500
    textTransform: uppercase
    letterSpacing: "0.19em"
    color: accent

layout:
  container: 1360px
  gutter: "clamp(20px, 4.5vw, 64px)"
  navHeight: 72px
  sectionPadding: "clamp(4.5rem, 10vh, 7.5rem)"
  gridGap: 14px
  breakpoints: [600, 900, 1080, 1240]

shapes:
  radius: 18px
  radiusSmall: 10px
  radiusBand: 28px
  button: pill

motion:
  easeOut: "cubic-bezier(.23, 1, .32, 1)"
  easeInOut: "cubic-bezier(.77, 0, .175, 1)"
  press: "scale(0.97) en 160ms"
  reveal: "opacity + translateY(22px) en 700ms"
---

## Overview

INWARD es una consultora francesa de inmigración y movilidad internacional que
atiende a dos públicos a la vez: particulares que se instalan en Francia y
empresas que mueven colaboradores. El sitio tiene que transmitir rigor
administrativo sin caer en el azul corporativo genérico de la categoría.

La solución es un fondo blanco con **un solo acento**, el azul eléctrico
`#202045` de la paleta secundaria del brand book, y dos tintes ácidos que
aparecen únicamente como fondo de celdas dentro de una grilla. El ritmo de la
página no lo dan las tarjetas sino **dos bandas de color pleno** que cortan el
blanco en puntos fijos.

Serio pero luminoso. La fotografía es real, de luz natural y clave alta, y por
eso el fondo es blanco: sobre oscuro las fotos se leen como recortes pegados.

El hero ocupa el alto completo de la ventana (`100svh`, nunca `vh`) con video de
fondo a sangre.

## Colors

### Ritmo de fondos

Sólo dos fondos de sección: **blanco `#ffffff` y gris `#eeeeee`**, el gris del
brand book. Alternan: blanco (B2B), gris (logos de clientes), blanco (B2C),
gris (quiénes somos), blanco (recursos), gris (contacto), blanco (footer). El
hero es la excepción: video a sangre con texto blanco.

**El gris nunca arranca ni termina con una línea.** Entra y sale con degradado,
así que en toda la página no queda ni un borde horizontal visible. Medido: cero
saltos bruscos de luminancia por debajo del hero. Un borde duro cada 800 px es
lo que hace que una página se lea como bloques apilados, que es justo lo que la
clienta no quería.

**El bloque gris de empresas no es sólo `#entreprises`.** Arranca tiñendo la
mitad inferior de la sección de avis, cubre empresas y sigue por la franja de
logos, que es su prueba social y ya vive pegada a su CTA. Vuelve al blanco
dentro del padding superior de particulares.

Las celdas del bento pasan a **blancas**: sobre una sección gris, una celda gris
sólo existiría por su borde.

Eso obliga a una excepción a la regla de abajo. El bloque que se va es la franja
de logos, de 86 px, y una rampa de 0,17 de luminancia en 86 px banda. **Cuando
el bloque que se va es un intersticio, la rampa se muda al padding del que
llega**, porque una rampa necesita largo antes que dueño.

**El degradado de entrada vive en la sección de arriba, no en la gris.** La
banda de contacto es gris plano de punta a punta; quien se tiñe es la sección de
recursos, en toda su mitad inferior. Un degradado largo que ocupa media sección
disimula el límite mucho mejor que uno corto encerrado dentro de la sección
gris, donde el ojo todavía encuentra dónde empieza el color. La regla general:
la transición pertenece al bloque que se está yendo.

**Excepción, y es la única: el footer corta en seco.** Ese sí es un borde que
queremos que se lea: es el final de la página, no una costura entre dos
secciones.

**La salida del gris vive en la sección gris**, por la misma regla: la
transición pertenece al bloque que se está yendo. Mientras el footer venía justo
después de contacto no hacía falta, porque ese corte lo queríamos. Al meter la
FAQ en el medio, el gris pasó a terminar contra el blanco y apareció un filo de
**0,145** de luminancia, el único de la página por debajo del hero. Medido, no
estimado: cuando se agrega una sección hay que volver a pasar el escáner de
costuras, porque una sección nueva cambia quién limita con quién.

**Ninguna sección lleva fondo saturado.** El violeta es acento, nunca fondo. Una
banda azul a sangre compite con la fotografía y con los tintes del bento, y
convierte la página en un damero. Si una sección necesita separarse de la
anterior, la respuesta es el gris, no el color.

### Acento

Hay **un** acento en toda la página: `#202045`, el VIOLETA OSCURO de la paleta
primaria. Es la combinación que eligió la clienta: paleta secundaria (verde
agua y amarillo como tintes) con el violeta oscuro de la primaria como acento.
Se descartó el azul `#3600f9`, que daba 8,5:1 sobre blanco contra los 15:1 del
violeta y leía más eléctrico que profesional. Es a la vez color de texto de
acento (labels, links, títulos destacados) y relleno de los CTA, con texto
blanco encima. Da 9,5:1 sobre blanco, así que sirve para ambas cosas sin
inventar una segunda variante.

No existe un segundo acento. Si una sección parece necesitar otro color, la
respuesta es tinte de fondo, no acento nuevo.

### Tintes

`--tint-1` verde agua `#55ffd2` y `--tint-2` amarillo `#ebff76` son **fondos de
celda**, nunca color de texto ni de icono suelto. Ambos llevan texto `#101010`
encima. Su función es romper una grilla que si no sería de tarjetas planas
todas iguales.

**Máximo dos celdas tintadas por grilla, y nunca contiguas.** Se usan en el
bento de empresas (2 de 5) y en las tarjetas del blog (2 de 3, con la del medio
neutra). Una tercera tinta o dos pegadas convierten la sección en un mosaico y
le sacan jerarquía al acento.

Sobre tinte, el texto secundario baja a `opacity: .75` y el metadato a `.68`.
Por debajo de eso el texto chico deja de pasar AA sobre el verde agua.

### Bandas alternas

Los tokens `--alt-*` visten las secciones grises. Son gris con texto oscuro.
Existen como grupo aparte para poder afinarlas sin tocar el resto, no porque
tengan otro esquema de color.

### Neutros

Los grises están sesgados hacia el violeta (`#4d4d6b`, `#71718f`) y las líneas
son el azul de acento a baja opacidad, no gris neutro. Es lo que hace que el
blanco no se sienta frío.

### Regla dura

Ningún componente escribe un hex a mano. Todo sale del bloque `:root` de
`assets/css/styles.css`. Cambiar de paleta es cambiar ese bloque.

## Typography

### Familias

- **Display:** Outfit. Geométrica, x-height alta, aperturas cerradas. Sustituye
  a **Figerona**, la tipografía de titulares del brand book.
- **Cuerpo:** Jost. Geométrica tipo Futura, x-height baja, formas redondas
  amplias. Sustituye a **Walkway**, la de textos del brand book.

El contraste entre las dos no es de estilo sino de x-height y de ancho. Por eso
funcionan juntas siendo ambas geométricas.

### Jerarquía

El peso hace el trabajo, no el tamaño. Display siempre en 500, nunca 700: la
escala y el tracking negativo (`-0.032em` en h1) ya dan presencia. El `lead` va
en 300 para abrir aire bajo cada titular.

Los labels de sección son versalitas de 0.7rem con `letter-spacing: 0.19em` en
color de acento. **Máximo uno cada tres secciones.** Un label sobre cada
titular produce el ritmo templado de sitio generado.

El titular del hero es la excepción a la escala: tiene la suya,
`clamp(2.15rem, 5.7vw, 5.1rem)`, bastante por encima del h1 general. Es la única
pieza que compite con un video a pantalla completa, y con el tamaño heredado y
tres líneas cortas ocupaba poco más de un tercio del ancho: el video se lo
comía. Dos líneas largas lo estiran de punta a punta del contenedor.

**Los cortes de línea del hero están escritos en el marcado**, en `<span
class="ln">`, porque cada uno entra con su propio retardo. Eso obliga a dos
cosas. No lleva `max-width`: un tope en `ch` sólo podría provocar un tercer
salto que nadie previó. Y por debajo de 900 px los tramos pasan a `inline` para
que el texto fluya solo, porque esos cortes en un teléfono darían cinco líneas
visuales con quiebres en lugares raros; ahí la entrada se anima en bloque, ya
que una animación de `transform` no tiene efecto sobre una caja inline.

### Nota sobre las sustituciones

Figerona y Walkway no están auto-hospedadas todavía. Figerona es licencia de
uso personal: para producción hay que comprar licencia comercial o cambiarla.
Cuando lleguen los .woff2 se declaran con `@font-face` y sólo cambian
`--font-display` y `--font-body`.

## Layout

### Cabeceras de sección

El ancho lo fija cada elemento, **nunca el contenedor**. Un `max-width` en `ch`
sobre el contenedor se mide con la tipografía del cuerpo y estrangula un titular
de 48 px a media columna. La regla:

- titular: `max-width: 18em`, en `em`, así escala con su propio tamaño
- párrafo de entrada: `max-width: 56ch`, que es medida de lectura

Cuando la cabecera deja mucho blanco al costado, la solución es `.sec-head-row`:
titular a la izquierda y **un elemento funcional** a la derecha, alineados por
la base. Nunca un párrafo de relleno flotando en la columna derecha.

Contenedor de 1360 px con gutter fluido de 20 a 64 px. Grilla de 14 px de gap
en todo el sitio, sin excepción.

El bento del bloque de empresas es asimétrico de seis columnas: una celda de
`span 4` con foto y cuatro de `span 2`. **Tantas celdas como contenido haya**;
si sobra un hueco, la grilla está mal planteada, no falta una tarjeta vacía.

Ninguna familia de layout se repite. A lo largo de la página: hero a sangre con
cifras, bento asimétrico, fila de logos, lista de filas que se abren con vista
previa, split de retratos, grilla de tres tarjetas, split de formulario. Siete
estructuras distintas.

Las cabeceras de sección van apiladas (label, titular, párrafo) y el CTA de la
sección va **después** del contenido, nunca en la cabecera.

Todo layout multicolumna declara su colapso a una columna antes de 900 px.

## Shapes

Una sola escala de radios, sin excepciones:

| Token | Valor | Dónde |
|---|---|---|
| `--r` | 18 px | Media, celdas del bento, tarjetas. Utilidad `.rounded` |
| `--r-band` | 28 px | Esquinas superiores de la banda que se desliza sobre el hero |
| `--r-sm` | 10 px | Campos de formulario |
| — | pill | Botones y selector de idioma |

No hay ningún `border-radius` suelto en el CSS. Un componente nuevo usa
`.rounded` o una de esas variables.

## Components

### Métricas

Van **dentro del hero**, en una tira horizontal debajo de los CTA, separadas por
un hairline. Números chicos (2,15 rem como máximo) con su etiqueta debajo.

Las tres cifras son **reales y confirmadas por la clienta**: 99 % de tasa de
éxito, +45 nacionalidades acompañadas, +1000 expedientes tratados. Ninguna
está inventada ni redondeada por nosotros.

Se probaron antes como sección propia sobre banda de color, primero con tres
columnas iguales y después con una cifra en display gigante. Las dos versiones
fallaron por lo mismo: una cifra sola no llena una sección entera. En el hero
refuerzan el mensaje sin pedir su propio bloque, y la página arranca directo en
los servicios.

Es el patrón de Revolut, una de las referencias del brief.

### Botones

Pill. El primario es relleno de acento con texto blanco; el fantasma es
transparente con borde `--line-strong`. `scale(0.97)` en `:active` a 160 ms:
sin ese feedback el botón se siente muerto.

**El relleno de los CTA es el violeta `#202045`.** Se probó pasarlos a los
tintes de la paleta y se volvió atrás. La medición explica por qué conviene
dejarlo así:

| Relleno | Texto sobre el botón | Botón sobre gris | Botón sobre blanco |
|---|---|---|---|
| Violeta `#202045` | 15,5:1 | **13,4:1** | **15,5:1** |
| Verde agua `#55ffd2` | 15,1:1 | 1,09:1 | 1,26:1 |
| Amarillo `#ebff76` | 17,3:1 | 1,06:1 | 1,10:1 |

El texto se lee perfecto en los tres. Lo que cambia es **cuánto se despega el
botón del fondo**. Con un tinte, el CTA existe por su texto, no por su forma.
Y hay un segundo motivo: verde agua y amarillo ya son colores decorativos acá
(bento, blog, FAQ, mega menú), así que un CTA tintado deja de ser lo único con
derecho a ese color y se confunde con el relleno de al lado.

**Los dos botones del hero son la excepción: blancos con el texto en violeta.**
El pie del velo del hero deja el fondo en 0,015 de luminancia y el violeta sobre
eso da **1,05:1**: el botón existía como texto pero no como forma. En blanco da
16:1. El acento no desaparece, se muda al texto.

Y son iguales entre sí. Uno relleno y otro fantasma hacía que el segundo
pareciera una opción de segunda, cuando las dos audiencias valen lo mismo y el
orden ya dice cuál va primero. Van también un punto más grandes que el resto de
los botones, porque compiten contra una imagen a pantalla completa y no contra
fondo blanco.

### Orden de las audiencias

**Empresas va siempre primero.** En el menú, en los botones del hero, en el
selector del formulario, en las columnas del pie y en el orden de las secciones.
No es alfabético ni casual: es la audiencia de mayor valor por dossier y la
clienta quiere que sea lo primero que se ve. Cualquier par
particulier/entreprise que se agregue después sigue esta regla.

### Celdas y tarjetas

**Las cinco celdas de empresas son iguales: mismo ancho, mismo alto, misma
tipografía.** Antes una de ellas llevaba foto, ocupaba cuatro columnas de seis y
el doble de alto, así que a simple vista parecía el servicio principal y los
otros cuatro, secundarios. Son cinco prestaciones del mismo rango. Al bajar de
ancho cambia la cantidad de columnas (5 → 3 → 2 → 1), nunca el tamaño relativo
de una celda: en la última fila queda un hueco vacío, y está bien, es una
grilla incompleta y no una jerarquía.

Los dos tintes se mantienen, alternados en la segunda y la cuarta. Alternar lee
como ritmo, no como ranking; lo que leía como ranking era el tamaño.

**Todas las secciones entran enteras en pantalla.** No sólo empresas y
particulares: es una regla de la página. Verificado a 1280×800, 1366×768,
1440×900, 1512×982, 1728×1117 y 1920×1080, descontando los 72 px de la barra
fija. El piso está en unos 730 px de alto útil; por debajo de eso el contenido
no comprime más sin quedar apretado, y parte de la culpa es que `--band-gap`
es fijo y no encoge con la ventana.

**Corolario para cualquier bloque nuevo: el alto se mide contra la ventana, no
contra el ancho.** La banda a sangre de "Qui sommes-nous" empezó con
`aspect-ratio: 16/5` y crecía con el ancho de la pantalla, 450 px a 1440 y 472
a 1512, justo lo que hacía que la sección no entrara. Con
`height: clamp(160px, 24svh, 280px)` entra siempre. Es lo que pagó quitar la foto del bento, apretar los encabezados
y dejar el acordeón de particulares cerrado al cargar: una fila abierta por
defecto costaba 94 px y en un portátil de 768 px de alto era la diferencia entre
ver la sección completa o no.

**Todas las cajas de la página llevan el mismo borde**, del token
`--line-card` (`rgba(32,32,69,.24)`): celdas del bento, tarjetas del blog,
tarjetas de avis, preguntas de la FAQ, el bloque de llamada del mega menú y el
panel del formulario. También las tintadas, que antes lo llevaban transparente.

Es una sola línea para todas a propósito: si alguien la quiere más marcada o
más suave, toca el token y cambian las seis familias a la vez. Un borde por
componente es cómo se llega a lo que había antes, que era tres criterios
distintos conviviendo.

Más oscura que `--line` porque su trabajo es distinto: `--line` separa cosas
dentro de un bloque (filetes, campos), `--line-card` recorta la caja del fondo
para que no flote.

Las celdas del bento se agrupan por **relleno** además del borde. El contenido va
**arriba**, no abajo: una caja con el texto pegado al piso y aire muerto encima
se lee como un error de maquetado, no como respiro. La celda con foto es la
excepción, porque su texto va sobre el degradado inferior de la imagen. Las tarjetas del
blog al revés: fondo blanco con borde de 1 px. Dos tratamientos distintos
porque son dos jerarquías distintas; no se mezclan.

**El hover es uno solo para toda la página**: la tarjeta sube 4 px y proyecta
sombra. Da igual que sea celda del bento o tarjeta del blog, tintada o no. Antes
había tres comportamientos conviviendo (celda que sólo subía, tarjeta gris que
subía y cambiaba el borde a acento, tarjeta tintada que sólo subía porque el
borde no se ve sobre relleno de color) y al recorrer la página se notaba como
inconsistencia. El borde no sirve como señal común justamente porque las
tintadas no lo tienen; la sombra sí funciona en los dos casos.

El levante se escribe en `translate`, **no** en `transform`. Las tarjetas llevan
`.rv`, cuya animación `riseIn` corre con `both` y por lo tanto queda dueña de
`transform` de forma permanente: una animación gana sobre cualquier declaración
normal en la cascada, así que un `transform` en `:hover` no se renderiza nunca.
`translate` es una propiedad independiente y se compone con el `transform` de la
animación. Lo mismo vale para la transición: `transition:translate`, no
`transition:transform`.

Nada lleva sombra en reposo salvo elementos que flotan de verdad: el mega menú y
el panel de notas. Las sombras van tintadas con el acento, nunca negro puro.

### Qui sommes-nous

**No lleva retratos de las fundadoras.** La sección cuenta qué es INWARD, no
quién la firma; los nombres siguen en el JSON-LD, que es donde sirven. Las
fotos de retrato están en `assets/img/` por si vuelven en la página interna.

**Su maquetado es deliberadamente distinto al de particulares**, que viene
inmediatamente antes. Allá son dos columnas, una lista de filas separadas por
filetes horizontales y una foto al lado del texto. Acá no hay dos columnas: es
una pila editorial a todo el ancho, enunciado → imagen a sangre → tres pilares
separados por filetes **verticales** → acción. Eje contrario en los filetes, y
la foto no convive con el texto sino que corta la página de borde a borde. Es,
junto al hero, el único bloque a sangre.

Dos secciones seguidas con la misma familia de maquetado se leen como la misma
sección repetida dos veces, por más que el contenido cambie.

Apilados en pantalla chica los pilares vuelven al filete horizontal: una raya
vertical entre dos bloques que ya no están lado a lado no separa nada.

### FAQ

Otro acordeón, pero **no el mismo que el de particulares**. Allá son filas
separadas por filetes horizontales sobre el fondo de la sección; acá son
bloques con relleno gris separados por aire. Regla contra relleno: el mismo par
de opuestos que ya distingue las celdas del bento de las tarjetas del blog. El
marcador también cambia, un chevron que rota en vez de la cruz.

**Ciclo de tres: verde agua, amarillo, gris.** Sólo los dos tintes de la
paleta; el gris hace de tercer tiempo. Con dos colores alternados y nada más,
seis bloques dan un damero, y el gris rompe ese ritmo sin meter un color que no
es de la marca. Se probó con el lila `#d2d2ff` como tercer tinte y la clienta
lo descartó: **el lila no forma parte de esta paleta.**

Ninguna queda sin color por jerarquía: el gris es un tiempo del ciclo, no una
pregunta menos importante.

Usa **`<details>` nativo, no un botón con JavaScript**. Se abre sin JS, el
teclado y los lectores de pantalla ya saben qué es, y el buscador ve las
respuestas aunque estén cerradas. El despliegue se anima con
`::details-content` e `interpolate-size` donde el navegador lo soporta; donde
no, abre de golpe, que es el comportamiento nativo de siempre.

**El tinte vive en el `summary`, no en la tarjeta.** La pregunta conserva su
color al abrirse y lo que se pone gris es el panel de la respuesta, así la fila
de colores se sigue leyendo entera aunque haya una abierta. La abierta se
enmarca con un filete interior de `rgba(16,16,16,.18)`, que es la única señal
disponible: el fondo de la pregunta ya no puede cambiar.

Lo que **no** sirve como señal de estado es el acento: con el violeta oscuro,
un título en acento sobre un fondo claro es casi indistinguible del texto
normal, porque `#202045` contra `#101010` no se lee como un cambio. Vale para
toda la página: el acento quedó como color de acción, no de estado.

Todas cerradas al cargar. Seis respuestas abiertas hacen una sección más alta
que la pantalla, y la primera pregunta no es más importante que las otras cinco.

Cuando lleguen las respuestas reales conviene agregar el JSON-LD `FAQPage`.
Hoy no: Google exige que las respuestas marcadas sean las que el visitante ve,
y cinco de las seis todavía no existen.

### Footer

Cierra la página con **el mismo peso que el header**: negro de marca `#0f0f12`,
logo a 38 px, cuatro columnas de enlaces y el selector de idioma.

**Borde recto de lado a lado, sin esquinas redondeadas.** Se probó con el mismo
redondeo que usa la primera sección sobre el hero y ahí no funciona: el hero
sigue existiendo detrás, así que ese panel se apoya sobre algo. El footer no
tiene nada debajo. Redondeado leía como una tarjeta más en una página que ya
tiene muchas, y dejaba dos cuñas de gris en las puntas superiores sin nada que
las justifique. Es el final de la página y corta de punta a punta.

Redefine sus propios tokens en claro, igual que el header sobre el video: el
violeta `#202045` no se lee sobre negro, así que el acento del footer pasa a
verde agua `--tint-1`, que sí está en la paleta. Sólo pinta el hover de los
enlaces. Antes era el lila `#d2d2ff`, descartado con el resto del lila.

**El logo del pie va entero en blanco.** El isotipo toma `--accent`, y como el
pie redefine el acento para el hover de los enlaces, el isotipo se pintaba de
ese color. Un isotipo de un color distinto al de la cabecera no es una variante,
es otra marca.

Se probó bajando con degradado de blanco a negro y quedaba como una nube gris.
Un panel es una forma deliberada; una rampa larga parece un error de render.
Es la única excepción a la regla de no usar bordes duros, y lo es porque es una
forma, no una costura.

### Header

72 px de alto, una sola línea. Sobre el video del hero es **transparente y
redefine sus propios tokens en blanco**, así que el logo y los links se adaptan
solos sin blancos escritos a mano. Se vuelve blanco opaco al scrollear, y
también al abrir un mega menú, porque si no el panel quedaría con texto blanco
sobre fondo blanco.

El mega menú es a ancho completo, con las columnas alineadas al contenedor.
Cuidado con el shorthand `padding`: pisa el `padding-inline` heredado del
contenedor y el contenido termina pegado a los bordes.

### Menú desplegable (por debajo de 1080 px)

**El panel es el mismo `<nav>` de escritorio**, no un segundo menú. La consulta
media lo convierte en un panel a pantalla completa y reordena los mega menús
como acordeón. No hay marcado duplicado, así que no existe la posibilidad de que
una versión tenga un enlace que la otra no.

En escritorio los grupos se abren con `:hover` y no interviene JavaScript. En el
panel eso no existe: cada grupo se abre al tocarlo y se marca con `data-open` en
el `.nav-item`. **La consulta media es la única fuente de verdad sobre el ancho**;
el JS pregunta por ella con `matchMedia`, nunca compara `innerWidth` contra un
número escrito aparte, que es como se llega a dos criterios que discrepan.

El panel va **`position: absolute` contra la barra, no `fixed` contra la
ventana**. La barra lleva `backdrop-filter` cuando está sólida, y un elemento con
`backdrop-filter` se convierte en el bloque contenedor de sus descendientes
fijos: un `position: fixed` ahí queda recortado a los 72 px de alto de la barra y
del panel se ve apenas la primera línea. Peor todavía, el recorte aparece y
desaparece según la barra esté sólida o transparente.

**Dentro del panel el mega menú va a dos columnas**, no en una lista corrida.
Ocho entradas con subtítulo en una sola columna dan un scroll largo en el que
hay que recordar dónde empezaba cada grupo; en dos columnas los dos grupos se
ven a la vez y el menú entero entra en una pantalla de tablet. El bloque de
llamada ocupa el ancho completo debajo, que es donde se lee como cierre y no
como una tercera categoría. Por debajo de 640 px vuelve a una columna: dos
columnas de títulos largos en un teléfono no entran.

El contenido del grupo abierto va **sangrado a los dos lados** respecto del
título que lo abre. La sangría es lo que muestra la jerarquía, y de paso lo
despega del borde del panel, donde antes quedaba 3 px a la izquierda del propio
título. A los dos lados y no sólo a la izquierda porque el bloque de llamada
ocupa el ancho completo y con un solo lado se vería descentrado. El filete que
separa los grupos sigue de lado a lado: es lo que deja claro que el contenido
sangrado pertenece al grupo de arriba.

Al pasar `.mega-in` a grilla hay que anularle el `margin-inline: auto` que
hereda de `.wrap`. **Un item de grilla con márgenes automáticos deja de
estirarse y se centra sobre su ancho de contenido**: el panel se veía como una
columna angosta flotando en el medio de la pantalla.

El plegado usa `grid-template-rows: 0fr → 1fr` sobre un hijo con
`overflow: hidden`, igual que el acordeón de B2C. **El relleno de abajo va en el
último hijo, no en la caja recortada**: el padding propio de un elemento no lo
recorta su propio `overflow`, y el grupo cerrado deja ver una franja con el
primer título adentro.

Al abrir, el scroll del documento se bloquea. Sin eso el dedo arrastra la página
detrás del panel y al cerrar el visitante aparece en otra parte del sitio. Al
pasar a escritorio el panel se cierra por JS: si quedara marcado abierto, el
bloqueo del scroll sobreviviría al cambio de ancho.

### Favicon

**Isologo en violeta oscuro sobre fondo transparente**, sin el cuadrado de
color que tenía antes. Se genera a partir de `assets/img/logo/inward-isotipo.svg`
y sale en `favicon.svg`, `favicon.ico` (16 y 32) y los PNG de 192 y 512.

**El `apple-touch-icon` es la excepción y va sobre blanco.** iOS no respeta la
transparencia: compone el icono sobre negro, y un isologo violeta oscuro sobre
negro desaparece. Blanco con el isologo violeta es la misma identidad y se ve.

### Rail de secciones

Un filete vertical de 2 px con el segmento activo en acento y escalado. **No** se
repite el isotipo seis veces al costado: una marca que se repite deja de ser
marca. El logo aparece dos veces por página, header y footer, y nada más.

Va a **un tercio del margen izquierdo, no a la mitad**: es un indicador anclado
a la ventana, no una columna de contenido. A mitad de camino quedaba pegado al
texto y competía con la lectura. En pantallas anchas el margen crece pero el
riel se queda cerca del borde, que es donde tiene que estar; el `max(16px, …)`
evita que lo toque a 1241 px, el ancho más angosto en el que todavía se muestra.
Por debajo de 1240 px desaparece.

### Lista de servicios en acordeón

La cabecera de esta sección va **dentro de la columna de texto**, no encima de
las dos. Así la foto arranca a la misma altura que el label y termina a la
misma altura que el CTA: los dos bloques comparten borde superior e inferior.
Si la cabecera queda afuera, la foto empieza más abajo y la fila se desalinea.

La foto **se estira hasta el alto de esa columna** (`align-items: stretch`), no
impone su propia proporción. Con un 3/4 fijo
sobresalía por abajo y parecía caerse de la sección. El recorte va con
`object-position: 50% 34%` para que las caras no queden cortadas cuando el
alto baja.


Filas separadas por hairline. Un clic abre, otro cierra, y se puede quedar todo
cerrado. **Sin apertura al pasar el cursor:** volvería a abrir la fila que
acabás de cerrar. La fila abierta se marca sólo con el título en acento y el
signo rotado a cruz, sin fondo de color: un lavado violeta detrás del texto
ensucia y compite con las bandas plenas.

El aviso previo queda en la última imagen al cerrar, así el bloque no se vacía.

**Por debajo de 900 px la foto se oculta entera.** En una columna cae después
del acordeón, o sea al final de una lista larga y plegable, donde casi nadie
llega. Y su única función es cambiar al abrir cada fila: si no se ve al mismo
tiempo que la fila que la dispara, no comunica nada. Dejarla ahí de adorno
alarga la sección sin dar información. El `display: none` además evita que se
descarguen las cuatro imágenes, porque un `loading="lazy"` dentro de una caja
sin renderizar nunca llega a interseccionar el viewport.

### Avis Google

Familia de maquetado propia: bloque de nota fijo a la izquierda y un **carril
horizontal** de tarjetas a la derecha. El carril no es un capricho: la API
devuelve **entre una y cinco** opiniones y ese número cambia solo, sin que nadie
toque el código. Una grilla de tres se rompe sola en cuanto llegan cuatro. Un
carril acepta cualquier cantidad sin recomponer nada, y mantiene la sección en
una sola fila, que es lo que le permite entrar en pantalla.

El carril **no se desplaza solo**. Un marquee automático en un bloque de texto
obliga a leer a la velocidad de la animación.

Va **antes de Empresas**, apenas terminado el hero: es la prueba social que
sostiene todo lo que viene después. Los logos de clientes siguen donde estaban,
pegados al CTA de empresas. Son dos pruebas distintas para dos audiencias: las
opiniones vienen de particulares, los logos de empresas.

**Lo que muestra cada tarjeta no es decorativo, es obligatorio.** Nombre y foto
del autor, fecha relativa y enlace a la opinión original los exige la política
de Google; la fecha de la visita la exige la ley francesa. Ninguno de esos
elementos se puede quitar por razones de diseño.

Si no hay datos, la sección muestra el aviso de pendiente. **Nunca una opinión
inventada**: un testimonio falso en un sitio de un despacho es un problema
legal, no una licencia de maquetado.

### Fila de logos de clientes

Gris al reposo con opacidad 0,72, color al hover. Cada logo lleva su propia
altura calculada según su proporción: un mot-symbole ancho a 26 px, una marca
compacta a 41 px. Si se les da la misma altura a todos, la fila queda
descompensada. Sólo logos, nunca una etiqueta de rubro debajo.

Es una **franja intersticial**, no una sección: va sobre blanco liso y no lleva
padding propio. Todo su respiro sale del token `--band-gap`, hoy **65 px**, y la
relación es **1:2, menos arriba que abajo**: `#entreprises` cierra con
`--band-gap` y `#particuliers` abre con el doble.

El valor es fijo, no relativo al alto de la ventana como el resto del padding
vertical de la página. Es una distancia entre dos piezas concretas, no un ritmo
de página: la franja tiene que quedar a la misma distancia del CTA en un portátil
y en un monitor grande.

No es simetría, y es a propósito. La prueba social pertenece al CTA de empresas:
pegada a él funciona como su respaldo justo cuando alguien está por pedir una
reunión, y separada de la sección siguiente deja claro que no es el encabezado
de Particuliers. Se probó centrada, con el mismo aire de los dos lados, y la
franja se leía como una sección suelta sin dueño.

La escritura importa tanto como el valor: **la relación vive en un solo lugar**.
Si el respiro se reparte entre el padding de la banda y el de las dos vecinas,
mantener el 1:2 obliga a recalcular tres selectores cada vez que se toca uno.

### Formularios

Label arriba del campo, siempre. Nunca placeholder como label. Foco con borde
de acento más un halo de 3 px en `--accent-soft`.

**Un solo formulario con dos perfiles.** Empresa pide razón social y sólo
acepta correo profesional; particular no. El campo que no corresponde se quita
con el atributo `hidden` y `disabled`: así sale del formulario y del recorrido
por teclado, en vez de quedar invisible pero enfocable y enviándose igual.

**Para que `hidden` funcione hay que declararlo.** `[hidden] { display: none }`
vive en la hoja del navegador y tiene especificidad cero, así que cualquier
`display` escrito en una clase le gana. `.fld { display: grid }` lo pisaba y el
campo de razón social se seguía viendo en el perfil particular con el atributo
puesto. La hoja declara `[hidden] { display: none !important }` para todo el
sitio.

El correo profesional se valida **listando lo que no se acepta** (mensajerías
personales y desechables), no listando lo permitido: al revés dejaría afuera a
cualquier empresa con un dominio que no conozcamos, que son casi todas.

**El error tiene su renglón reservado debajo del campo.** Si aparece y empuja
el resto del formulario, el clic que el visitante ya tenía apuntado cae en otro
lado. Por el mismo motivo el mensaje es corto: en dos renglones desborda la
reserva y vuelve a empujar.

**Las celdas de una fila de dos campos van con `align-items: start`.** Por
defecto se estiran a la altura de la más alta, y el campo de email es más alto
porque reserva el renglón del error: el de nombre se estiraba para igualarlo y
su caja quedaba 11 px más alta y 10 px más abajo que la de al lado.

El rojo del error es un color propio, `#b3261e`, no un token de marca. Un error
tiene que leerse como error, y el violeta de INWARD es justamente el color de
lo que está bien: botones, enlaces, foco.

## Motion

**La continuidad es un requisito del brief, no un adorno.** La clienta pidió
explícitamente que la página no se sintiera cortada por sección. Tres cosas la
sostienen, y las tres tienen que sobrevivir a cualquier rediseño:

1. Los fondos entran y salen con degradado, sin bordes duros.
2. El reveal va atado al scroll con `animation-timeline: view()`: el elemento
   avanza con la rueda en vez de aparecer de golpe al cruzar un umbral. El
   `IntersectionObserver` queda sólo de reserva para navegadores sin soporte.
3. Parallax suave en las fotos grandes, que se mueven a otra velocidad que la
   página y desdibujan dónde empieza cada sección.

El padding vertical tampoco es igual en todas las secciones: un ritmo idéntico
una tras otra también las hace leer como bloques sueltos.

Cada animación tiene que poder justificarse en una frase. Las que hay:

- **Hero:** a `100svh`, con video de fondo. Las líneas del h1 suben con reveal
  por clip, escalonadas 90 ms.
- **La barra tiene su propio velo cuando flota sobre el vídeo.** Medido: en los
  tramos claros del vídeo el fondo detrás del menú llega a 0,754 de luminancia y
  el texto blanco daba **1,31:1**, ilegible. El velo del hero no alcanza, porque
  arriba es justamente donde más lo aclaramos para que se viera el edificio.
  Éste es local, 72 px de alto y se desvanece, así que no oscurece la imagen,
  sólo la franja de la barra. Con él: menú 6,9:1 y logo 8,3:1 en el peor punto.
  Va en un pseudo-elemento para poder desvanecerlo con la misma transición con
  la que la barra se vuelve sólida.
- **El velo del hero se concentra abajo, donde está el texto**, y suelta la
  parte alta de la imagen. Antes era una capa casi pareja que tapaba también el
  edificio y dejaba el hero mucho más oscuro que el resto de la página, que es
  clara. Las paradas del degradado están calculadas contra el contraste real
  del texto blanco sobre el vídeo, no a ojo: el tercio superior quedó un 72 %
  más luminoso y, aun así, el titular pasó de 2,87:1 (por debajo del mínimo) a
  3,22:1. Si se cambia el vídeo hay que volver a medir.
- **Continuidad:** el hero es sticky y las bandas siguientes se deslizan por
  encima con el radio superior abierto. Es lo que evita que la página se sienta
  como bloques separados.
- **Salida del hero:** `animation-timeline: scroll()`, fuera del hilo principal.
- **Mega menú:** 200 ms ease-out, ítems escalonados 40 ms.
- **Filas de servicios:** se abren y cambian la foto de vista previa con
  crossfade más blur, que tapa el salto entre dos imágenes distintas.
- **Reveal al entrar en pantalla:** visible por defecto, oculto sólo si el
  elemento está fuera de pantalla al cargar.

### La impronta de cada sección

El reveal **no es el mismo en toda la página**. Con un único gesto repetido, el
scroll se vuelve previsible y las secciones pierden carácter: se distinguen por
lo que dicen, no por cómo llegan.

Lo que se mantiene igual es el **encabezado**: todos los `h2` entran con
`riseIn`. Ese es el hilo que sostiene la página como un solo sistema. Lo que
cambia es el contenido, y cada gesto sale de la forma de lo que anima, no de
las ganas de variar:

| Sección | Gesto | Por qué |
|---|---|---|
| B2B | mosaicos que se posan (y + escala, escalonado en diagonal) | es una grilla de piezas, y se arman pieza por pieza |
| Clientes | sólo opacidad, de izquierda a derecha | pasar lista. Siete marcas heterogéneas moviéndose a la vez es ruido |
| B2C | los filetes se trazan de izquierda a derecha y el texto aparece | eje horizontal, el mismo de los filetes. La foto entra desde el lado opuesto |
| FAQ | las preguntas entran por los costados, una de cada lado | son cajas cerradas: una caja que se desliza se lee como una caja, no como una desalineación |
| Nosotras | la banda a sangre se descubre de arriba abajo con `clip-path` | la foto no se mueve, se revela; es el único gesto de recorte de la página |
| Recursos | cascada: cada tarjeta viene de más lejos y todas terminan a la vez | llegan en abanico y se emparejan |
| Contacto | un solo bloque, sin escalonar, el recorrido más largo | un formulario que aparece campo por campo se siente inestable |

Dos calibraciones que decidieron si esto se ve o no:

**Los rangos se miden sobre `cover`, no sobre `entry`.** El tramo `entry` de un
elemento dura lo que mide el elemento: para una fila de logos de 41 px, la
animación entera transcurre en 41 px de scroll y termina antes de que el
elemento esté bien a la vista. `cover` mide el paso completo por la ventana, así
que el gesto se ve mientras el elemento sube. Fue la razón principal por la que
la primera versión pasaba desapercibida.

**Cada gesto se apoya en una propiedad distinta**, no en una distancia distinta:
escala, opacidad, eje horizontal, eje vertical, recorte. Variar sólo cuántos
píxeles se desplaza un mismo movimiento no se percibe; cambiar qué propiedad se
mueve, sí. Es lo que permite que las amplitudes sean chicas y aun así se note
la diferencia: 30 px en horizontal se distinguen de 14 px en vertical porque el
eje cambia, no porque el recorrido sea grande.

**La opacidad termina al 55 % del recorrido, el desplazamiento sigue hasta el
final.** Lo que estorba la lectura no es que algo se mueva unos píxeles: es
tener que leer texto a medio opacar. Con este reparto el texto es legible
enseguida y lo único que queda por resolverse son los últimos píxeles del
movimiento, que el ojo ya no persigue.

**La FAQ además termina en el CTA.** Las seis preguntas están asentadas en el
instante en que el botón "Contactez une experte" asoma por abajo. Los topes no
se eligieron a ojo: en ese instante la última pregunta está al **8,6 %** de su
propio paso por la ventana, y ése es el techo de todo el conjunto.

Las seis arrancan en `cover 0%` y terminan escalonadas **hacia atrás** (11 %,
10,4 %… 8 %). Parece al revés y no lo es: cada pregunta está más abajo que la
anterior, así que entra en pantalla más tarde. Arrancar todas en 0 da igual una
entrada en secuencia, y los finales decrecientes hacen que las seis terminen
casi a la vez en scroll absoluto. Verificado a 1280×800, 1366×768, 1440×900 y
1512×982.

**Todo tiene que estar quieto antes de la zona de lectura.** Los rangos
terminan alrededor de `cover 20-30 %`, o sea cuando el elemento todavía está en
el tercio inferior de la pantalla. Si la animación sigue corriendo cuando el
contenido llegó al centro, la página se vuelve incómoda por más discreto que
sea el gesto. Se probó con rangos hasta `cover 40 %` y amplitudes del doble, y
era exactamente eso.

**Una caja sí puede entrar de costado; un renglón de texto no.** La FAQ entra
lateralmente y funciona, porque cada pregunta es una caja cerrada, con relleno
y borde, y una caja que se desliza se lee como una caja que se desliza. Las
filas de B2C no podían: eran renglones de texto alineados con el titular, y
cualquier desplazamiento lateral se leía como un error de maquetado. El gesto
no se elige por la sección, se elige por lo que hay dentro.

**Un gesto no puede romper una alineación, ni por un instante.** La primera
versión de B2C entraba la fila entera desplazada 30 px desde la izquierda. Como
las cuatro filas están alineadas entre sí y con el titular, mientras duraba el
escalonado se veían mal alineadas: la última todavía corrida cuando las de
arriba ya estaban en su sitio. No se lee como animación, se lee como un error
de maquetado. En una lista de renglones alineados lo que se mueve tiene que ser
otra cosa: acá se traza el filete con `scaleX` y el texto sólo aparece. Mismo
carácter horizontal, cero desplazamiento del texto.

**El escalonado no se hace con `animation-delay`.** Con `animation-timeline` el
delay se ignora: se corre el `animation-range` de cada elemento. Además de ser
lo único que funciona, ata el retardo al scroll y no al reloj, así que si
alguien sube y baja, la animación acompaña en vez de volver a arrancar.

Todo esto vive dentro de `@supports (animation-timeline: view())`. Un navegador
sin soporte recibe el `riseIn` parejo de siempre por `IntersectionObserver`, que
es una degradación correcta: pierde la impronta, no el contenido.

**`overflow: hidden` mata las animaciones de scroll de todo lo que tenga
adentro.** Un elemento con `overflow: hidden` es un contenedor de scroll, así
que el `view()` de sus descendientes se mide contra él y no contra la ventana;
como no scrollea, la línea de tiempo queda inactiva y la animación no corre
nunca. `.ct` lo tenía y el formulario de contacto aparecía sin ninguna entrada,
en silencio, sin error en consola. **Para recortar se usa `overflow: clip`**,
que recorta igual sin crear el contenedor. Es la misma razón por la que la raíz
usa `overflow-x: clip`. Si una sección deja de animar, esto es lo primero que
hay que mirar.

**Nunca** un listener de `scroll`. Sólo `IntersectionObserver` o
`animation-timeline`. Todo cae a estático bajo `prefers-reduced-motion`.

## Do's and Don'ts

### Do

- Un solo acento en toda la página, tomado de `:root`.
- Fotografía real del shooting. Hay 67 fotos y un video en `assets/`.
- Dos bandas de color pleno por página, siempre en la misma posición.
- Una familia de layout por sección.
- Marcar el contenido que falta con `.todo` en vez de inventarlo.
- Cifras reales o marcadas como pendientes. Nada de precisión falsa.

### Don't

- Un segundo acento porque una sección "pide color". Usá un tinte de fondo.
- Verde digital `#00ff5e` sobre blanco: da 1,4:1, es ilegible. Vive sólo sobre
  las bandas de color.
- Un label de versalitas sobre cada titular.
- Fondo de sección saturado. Sólo blanco y gris.
- Repetir el isotipo como viñeta, marca de agua o nodo. El logo va en header y
  footer, dos veces por página.
- Fondo de color detrás del texto de un ítem abierto: para eso está el acento
  en el título.
- Tres tarjetas iguales en fila.
- Sombras negras. Van tintadas con el acento.
- Nombres, logos, testimonios o cifras inventados. Es una consultora real con
  clientes reales.
- Radios sueltos fuera de la escala.

## Responsive

**Las pistas de grid traen `min-width: auto`**, así que un hijo que no encoge
(un `select`, un `input`, una palabra larga) desborda la columna y genera scroll
horizontal en pantallas chicas. Todos los contenedores de grid llevan
`min-width: 0` en sus hijos directos. Es la causa habitual del problema.

Por debajo de 1080 px el selector de idioma sale del header y pasa al pie del
menú desplegable: no entran logo, idioma, CTA y menú a la vez, y un selector que
sólo existe en escritorio deja al visitante de teléfono sin forma de cambiar de
idioma. El CTA se queda en todos los anchos, que es la acción principal del
sitio.

Ese selector del menú es el tercero de la página, junto con el del header y el
del pie. `build.py` reescribe **los tres**; si alguno quedara sin tocar, `/es/`
enlazaría a `/es/en/` y el idioma activo se marcaría en la página equivocada. El
script falla si no encuentra exactamente tres.

Breakpoints en 600, 900, 1080 y 1240 px. A 1080 el menú pasa a hamburguesa; a
1240 desaparece el rail lateral de secciones. Todo grid multicolumna colapsa a
una columna antes de 900.

El hero usa `svh`, nunca `vh`: en iOS la barra de direcciones hace saltar el
layout.

## Anclas y navegación

El rail lateral y los enlaces internos apuntan a `id` de sección. Dos reglas que
ya costaron un bug:

- **Un elemento `position: sticky` no sirve como destino de ancla.** El hero
  está pegado arriba, así que el navegador considera que ya está a la vista y no
  scrollea. `#top` vive en un `div` de altura cero al principio del `body`, no
  en el hero.
- Ese mismo `div` no cae nunca en la banda central del `rootMargin` del
  observer, así que el estado activo de `#top` lo maneja la sentinela del
  header, no el observer de secciones.

Las secciones llevan `scroll-margin-top: calc(var(--nav-h) + 12px)` para que la
barra fija no tape el titular al llegar.

## Iteration Guide

Para cambiar la paleta entera, tocá el bloque `:root` de
`assets/css/styles.css` y nada más. Hay una variante con la paleta primaria del
brand book (negro, violeta oscuro `#202045`, violeta claro `#a67bff`, verde
digital) que usa exactamente este mismo CSS con otros 29 valores.

Para agregar una página, seguí la escala de radios, el gap de 14 px y el
contenedor de 1360. Y antes de dar por terminada una sección, comprobá que su
familia de layout no se repite con ninguna de las que ya están.

## Fuente de contenido: `Textos_web.md`

El documento de la clienta (descarga del Google Doc) es la **única fuente de
texto**. Todo lo que está en él va literal a la página; todo lo que no está se
marca con `.todo` y no se inventa. Volcado del 23/09 en la home:

| Sección | Qué entró del doc |
| --- | --- |
| Entreprises | Cuerpo real; H1 = opción 1 de las dos del doc; CTA = opción 1 de cuatro |
| Particuliers | Cuerpo real + **los seis servicios** (antes eran cuatro inventados); CTA = opción 1 de dos |
| À propos | H1 real + **los seis engagements** numerados; CTA "L'histoire d'Inward" |

Lo que quedó marcado porque el propio doc no lo resuelve:

- Bento 4 (Naturalisation): el doc duda entre ese servicio y *housing*
  («DUDA: Esto o housing?» en la landing Entreprise).
- Engagement 02 anuncia respuesta en **-12 h** y la landing Fundadoras dice
  **24 h**. Un solo plazo.
- F&Q: respuesta 1 sigue en lorem ipsum, respuesta 2 sin redactar.
- Los "voir plus" de cada servicio de particulares apuntan a la landing
  Particuliers, que todavía no existe.
- Blog y Términos y Condiciones están vacíos en el doc.

### Por qué cambiaron los altos

Seis servicios y seis engagements donde había cuatro y tres suman ~250 px. La
regla «cada sección entra entera en pantalla» se mantuvo comprimiendo la fila y
la franja, no el aire entre secciones, que es lo que da el ritmo:

- `.row-btn` 1,15rem → 0,68rem de padding vertical.
- `.about-band` 24svh → 9,8svh (la franja cede el alto que piden los seis
  engagements).
- `.pillars` pasa de tres columnas con filete vertical a **3×2** con filetes por
  posición y numeración por `counter()`, no escrita a mano.
- El enunciado de À propos ya no es grilla de dos columnas: el doc no trae
  párrafo de presentación, así que «Nos engagements, votre garantie» es el
  rótulo de la lista en vez de un lead inventado.

Medido a 1280×800 (728 px útiles): entreprises 697, particuliers 721, about
713, f&q 636, contact 696. A 1366×768 (696 útiles) ninguna entra, tampoco antes
de este cambio: ese alto está por debajo del piso de ~730 px del diseño.

## Regla: ninguna animación sigue cuando ya se ve el CTA

Lo que se hizo en la F&Q ahora vale para toda la página. El límite de cada
sección es **el instante en que su CTA asoma por el borde inferior**: a partir
de ahí no puede quedar nada moviéndose ni a medio opacar.

Los topes no se eligen a ojo. Para cada elemento:

```
scroll del CTA   = topeDoc(CTA) − alto de ventana
progreso(elem)   = (scrollCTA − (topeDoc(elem) − vh)) / (alto(elem) + vh)
```

El porcentaje que sale de ahí es el techo de su `animation-range`. Depende del
alto de ventana, así que se toma el más exigente de los tres medidos
(1920×1080 da siempre el techo más bajo):

| Sección | Techo medido | Rango aplicado |
| --- | --- | --- |
| Entreprises, tuiles | 18,4 % | `cover 0%` → 11 / 13 / 15 / 16,5 / 18 % |
| Particuliers, filas 1→6 | 28,4 → 6,7 % | `cover 0%` → 26 / 22 / 18 / 14 / 9 / 4,5 % |
| À propos | 21,9 % | 4 → 20 % (ya cumplía) |
| Contact | 28,1 % | 2 → 22 % (ya cumplía) |
| F&Q | 7,3 % | 0 → 11 … 8 % (ya cumplía) |

El patrón es siempre el mismo: **todas arrancan en `cover 0%` y los finales
bajan**. Parece al revés y no lo es: cada elemento está más abajo que el
anterior, así que entra en pantalla más tarde; con finales decrecientes todos
terminan casi a la vez en scroll absoluto.

Dos elementos quedan fuera de la regla a propósito: el propio CTA (su aparición
*es* el límite) y el parallax de la foto de À propos, que no es un reveal y
dura toda la sección. Ressources tampoco entra: su botón está arriba del
bloque, no después de las tarjetas.

Verificado con `verify.mjs`: a 1280×800, 1440×900 y 1920×1080 se scrollea al
instante exacto del CTA de cada sección y se recorre el DOM comprobando que
ningún descendiente animado tenga `opacity < 1` o un `transform` distinto de la
identidad.

## À propos sin foto

Se quitó la franja a sangre de la sección. Con eso desaparecen `.about-band`,
la animación `unveil` y el parallax de esa foto (el keyframe `parallax` ya no
tiene quién lo use y también se borró). `team.webp` sigue en el proyecto: la
usa la galería de particulares.

Sin la franja, la sección es **enunciado → rótulo → seis engagements → CTA**, y
el gesto de entrada es un fundido simple: una lista numerada no admite un
movimiento que compita con la numeración. Se devolvió el aire que se le había
quitado a `#about` para hacerle sitio a la foto (padding, `row-gap` y el margen
del rótulo vuelven a sus valores holgados). Queda en 684 px a 1280×800, la
sección más baja de la página después de la F&Q.

## El lila vuelve a la paleta

`--tint-3:#d2d2ff`. La paleta de acento pasa a tener tres tintes en vez de dos:
verde agua, lila y amarillo.

- **Pie de página**: el acento pasa de verde agua a lila. Los dos pasan de
  sobra sobre el negro del pie (13,1:1 el lila, 15,2:1 el verde agua), y el
  lila tiene la ventaja de no competir con el verde de los CTA. Pinta el hover
  de los enlaces y la píldora del idioma activo.
- **Bento de empresas**: la tercera celda pasa de gris a lila, así los tres
  tintes quedan repartidos (2 verde agua, 3 lila, 4 amarillo) y siguen siendo
  tres cajas tintadas contra dos planas, sin que ninguna pese más.
- Texto sobre lila: 13,1:1 en negro de marca, 10,6:1 en violeta oscuro.

- **F&Q**: la tercera de cada tres deja de ser gris y pasa a lila. Las seis
  preguntas rotan ahora los tres tintes: verde agua, amarillo, lila.
- **Centre de ressources**: la tarjeta del medio, que era gris, toma el lila.
  Las tres quedan tintadas.
- **Hover de los botones sobre el vídeo** (y sobre la foto de la landing): se
  probó en lila y volvió a verde agua. Sobre el vídeo, que es oscuro y sin
  color propio, el verde agua es el que se lee como un cambio de estado.

- **Isologo del pie**: el isotipo pasa de blanco a lila; la palabra sigue en
  blanco. Toma `--accent`, que el pie ya redefine en lila, y da 13,1:1 sobre el
  negro. El de la cabecera no cambia: ahí el fondo es claro.

Con esto el lila aparece en las cuatro familias de caja de la página —bento,
preguntas, tarjetas de blog y pie— más la marca del pie, y no queda como un
color suelto en un solo sitio.

## Segunda página: la landing de empresas

`/entreprises/`. Se llega desde tres sitios: el botón **« Vous êtes une
entreprise ? »** del hero, **cada caja del bento** de la home (cada una a su
servicio) y el menú **Entreprises** de la cabecera, más la columna «Services
entreprises» del pie. Los seis enlaces del menú caen en los cinco anclas de la
landing (`#visas`, `#detachement`, `#audit`, `#installation`,
`#naturalisation`).

### El shell deja de estar duplicado

Seis páginas con la cabecera copiada a mano es la forma segura de terminar con
dos menús distintos. Los bloques compartidos —sprite del logo, cabecera,
sección de contacto y pie— viven **sólo en index.html**, entre marcas:

```html
<!-- shell:header --> … <!-- /shell:header -->
```

y `tools/sync_shell.py` los copia al resto. Al copiar resuelve lo que depende
de dónde está la página:

- las rutas a recursos reciben tantos `../` como haga falta;
- un enlace que apunta a la propia página se vuelve ancla, para que no recargue
  (`entreprises/#audit` → `#audit`);
- un ancla a una sección que esa página no tiene se vuelve enlace a la home más
  el ancla (`#faq` → `../#faq`);
- el selector de idioma apunta a **esta** página en el otro idioma, no a la
  home de ese idioma.

`tools/pages.py` es la lista de páginas; de ahí salen la profundidad y las
rutas, y la leen tanto `sync_shell.py` como `build.py` y
`extract_strings.py`, así que no pueden discrepar.

**Orden de trabajo**: editar el francés → `python3 tools/sync_shell.py` →
`python3 tools/extract_strings.py` → `python3 build.py`.

`build.py` ahora recorre las páginas en vez de una sola, y genera
`en/entreprises/index.html` y `es/entreprises/index.html`. El CSV de textos es
uno solo para todo el sitio: la cabecera y el formulario son los mismos en
todas las páginas y un texto repetido se traduce una vez.

### Decisiones de la landing

- **Hero a media altura** (`min-height:clamp(460px,66svh,660px)`), misma
  familia que el de la home pero sin gastar una pantalla entera: es una página
  interior. `min-height` y no `height`, porque en teléfono el titular de tres
  líneas se metía debajo de la barra fija.
- **Contraste medido, no estimado**: con el velo original el rótulo quedaba en
  3,79:1 y el titular en 4,35:1. El texto vive en la columna izquierda, así que
  el refuerzo se puso en el degradado horizontal (.50 → .62) en vez de oscurecer
  toda la foto. Ahora: rótulo 5,7:1, titular 6,6:1, cuerpo 11,9:1, botones
  14,0:1.
- **Los cinco servicios, con todo el texto a la vista.** Se probó en acordeón
  (las dos variantes que propone el documento) y se descartó: en una landing
  de servicios, esconder el texto detrás de un clic es pedirle al visitante
  que trabaje para saber qué vendemos. La sección ya no entra en una pantalla
  y está bien: es el contenido principal de la página, no un índice.
  Cada servicio va en su caja, con el mismo lenguaje que el bento de la home:
  fondo blanco sobre la banda gris, filete de caja y redondeo. Dos columnas y
  el quinto a todo el ancho, porque cinco cajas en dos columnas dejan un hueco
  y un hueco en una grilla se lee como algo que falta.
  El CTA de cada servicio es un enlace y no un botón: cinco botones seguidos
  compiten entre sí y con el CTA principal de la página.
- **Animaciones**: mismo criterio que la home. Como los CTA de esta sección
  viven dentro de cada ficha, el límite es la lista entera a la vista; en ese
  instante la ficha 1 está al 34 % de su paso por la ventana y la 5 al 6 %, y
  los topes (22/18/14/10/5 %) quedan por debajo.
- Medido a 1280×800 (728 útiles): agilité 610, services 597, contact 696. Las
  tres entran enteras.

### Lo que falta en esta página

- Servicio 5: el documento duda entre **naturalisation** y **housing**, y no
  da CTA para ese bloque. Las dos cosas están marcadas.
- El documento pide una foto de coworking para el hero: se usa `team.webp`, la
  sesión en sala de reuniones, que es lo más cercano del banco de fotos actual.

## Revisión: header, rail, hover y F&Q

### El header ya no lleva una sombra pegada

El degradado que se desvanecía hacia abajo era un parche: una mancha sin borde
que existía sólo para que el texto se leyera, y encima se comía el CTA. La
barra pasa a ser **una superficie**: ocupa su alto exacto, tiene un filete
abajo que la termina, y en vez de tapar la imagen la **desenfoca**
(`backdrop-filter: blur(18px) saturate(130%)` sobre `rgba(9,9,20,.46)`). El
vídeo se sigue viendo a través, movido; la franja se lee como vidrio.

El CTA de la derecha iba en violeta de marca sobre una franja oscura: mismo
valor, el botón existía como texto pero no como forma. Sobre el vídeo va en
**blanco**, igual que los botones del hero, y vuelve al violeta en cuanto la
barra se aclara.

Medido con el texto oculto y muestreo de píxeles: menú 7,05:1, fondo bajo el
CTA 4,15:1 (el botón blanco recorta contra eso), y el violeta del CTA sobre
blanco 15,6:1.

### La g de «immigration»

El reveal por líneas del titular recorta con `overflow:hidden`, y ese recorte
se comía los descendentes. La caja gana `padding-bottom:.16em` (devuelto con
un margen negativo para no mover el interlineado) y el arranque de la
animación sube de 105 % a 122 %, para que la línea siga naciendo fuera de la
caja ya crecida.

### El rail se ve sobre cualquier fondo

Dos mecanismos, porque uno solo no alcanza:

1. **Inversión por banda.** Un observer con `rootMargin: -49.9%` detecta
   cuándo una banda oscura (hero, pie) cruza la línea media de la ventana, que
   es donde vive el rail, y le pone `data-dark`. Los colores están en tokens
   del propio rail, así que cambia todo de una vez, con transición.
2. **Doble contorno de 1 px** en cada marca: aro claro + halo oscuro. Hace
   falta porque al llegar al pie el rail queda *a caballo* entre dos bandas
   —arriba gris, abajo negro— y ahí ningún color único funciona.

Dos errores que costaron encontrar, anotados para no repetirlos:

- `rootMargin: -50%` exacto deja la zona de observación de **alto cero**, y una
  zona vacía no interseca con nada: el observer no dispara nunca. Con -49,9 %
  quedan dos píxeles de banda y funciona.
- Sumar +1/-1 según `isIntersecting` **no sirve**: la primera notificación
  llega con una entrada por cada elemento observado, así que el hero (+1) y el
  pie (−1) se anulaban justo cuando el hero sí estaba cubriendo el centro. Hay
  que guardar *qué* elementos están cruzando, no un contador.
- Y el que más costó: `var rail` ya existía más abajo en `main.js` (el carril
  de las opiniones). Como `var` no tiene ámbito de bloque, eran **la misma
  variable** y el observer escribía el atributo en el elemento equivocado.

Medido con muestreo: la peor marca contra su propio fondo da 2,19:1 sobre las
bandas claras y 3,19:1 sobre el vídeo; la activa, 11,9:1 y 19,1:1.

### Hover

La transición escrita en el estado base es la de **salida**; la de **entrada**
va dentro de `:hover` y es más larga (520-620 ms contra 340-420 ms) con curva
de desaceleración. Esa asimetría es la mitad del trabajo: entrar despacio se
siente atento, salir despacio se siente pegajoso.

La otra mitad es que se mueve más de una cosa: las tarjetas suben 6 px, ganan
una sombra larga y el borde se oscurece, las tres con duraciones distintas.
En los botones la flecha arranca 40 ms después y vuelve antes, y ese desfase
es lo que hace que se lea como un movimiento y no como un salto.

### F&Q

Las seis cajas de colores plenos no funcionaban como sistema: el color no
agrupaba ni jerarquizaba —sólo rotaba—, competía con los CTA, y seis bloques
saturados seguidos hacen que nadie lea el texto, que es justamente para lo que
existe la sección.

Ahora es **un panel** con seis filas separadas por filetes. El color sale del
fondo y queda un único acento: una barra de verde agua en el canto izquierdo
de la fila abierta, que crece con el mismo gesto con el que se despliega la
respuesta. El fondo tintado va en la fila entera, no sólo en la pregunta: si
no, la respuesta queda flotando sobre el blanco y el bloque abierto se parte.

El acordeón es **exclusivo sin una línea de JavaScript** (`name="faq"` en cada
`<details>`): abrir una cierra la anterior, siempre hay una sola respuesta a la
vista y la sección no crece sin control. El desplegado se anima de verdad con
`interpolate-size: allow-keywords` y `::details-content`; donde no está
soportado abre y cierra igual, sin transición. La función nunca depende del
efecto.

La animación de entrada también cambió: ya no son seis cajas entrando por los
costados (eso rompía la unidad del panel), sino el panel como bloque y las
filas encendiéndose en orden.

## Ajustes de la revisión

**La franja blanca de la F&Q** era una regla vieja que sobrevivió al rediseño:
`.qas{display:grid;gap:8px}`, del tiempo en que eran seis cajas sueltas. Con
el panel único ese hueco de 8 px dejaba ver el fondo blanco justo debajo de la
fila abierta, que es lo único que se nota porque es la única fila con fondo.
Borrada la regla, el gris llega hasta el filete.

**El rail cambiaba de color a medias.** El fondo se transicionaba en 420 ms
pero el contorno saltaba de golpe en el mismo instante, así que lo que se veía
era el parpadeo del halo, no un cambio de color. Ahora los dos van juntos y
más largos (700 ms): el rail se revela al entrar en la banda oscura. Las
marcas inactivas también subieron de opacidad (.34 → .50 sobre claro, .42 →
.55 sobre oscuro).

**La salida del hover.** Estaba en 380 ms con la misma curva de desaceleración
fuerte que la entrada: la tarjeta pegaba un tirón al final y se leía como un
corte. Se separa en dos curvas: `--ease-out` para entrar (desacelera, llega y
se queda) y `--ease-soft` —`cubic-bezier(.33,0,.18,1)`, simétrica— para
volver. Y la salida pasa a ser **más larga** que la entrada: 620 ms contra
560 ms en las tarjetas. Un retorno más lento que la ida es lo que hace que no
se sienta un corte; al revés se siente pegajoso.

## El bug que dejaba a las tarjetas sin salida de hover

`.rv` llevaba `transition:none` dentro del `@supports (animation-timeline)`.
Estaba puesto para anular el reveal de reserva, pero `transition:none` no
anula sólo el reveal: **anula todas las transiciones del elemento**. Como las
celdas del bento, las tarjetas del blog y las de opiniones son `.rv`, la única
transición que les quedaba era la declarada dentro de `:hover`, o sea la de
entrada. Al salir volvían de golpe.

Arreglado declarando la transición de reserva sólo en `.rv[data-hidden]`, que
es el atributo que pone el JavaScript cuando no hay soporte de scroll
timeline. Regla general: `transition:none` en un selector compartido es casi
siempre un error; hay que apuntar a las propiedades concretas.

Y el subrayado del hover de las celdas era `text-decoration`, que no se puede
transicionar: aparecía y desaparecía de golpe. Ahora se dibuja con un fondo de
1 px que crece y se retira.

## Los desplegables de Particuliers

Mismo idioma que la F&Q, dibujo distinto, porque son dos secciones y tienen que
notarse distintas:

| | F&Q | Particuliers |
| --- | --- | --- |
| Contenedor | panel cerrado con borde | filas al aire sobre el fondo |
| Marcador | chevron desnudo que gira 180° | cruz dentro de un círculo que se rellena |
| Acento | barra vertical en el canto de la fila | filete que acompaña a la respuesta |
| Fila abierta | se tinta entera de gris | no se tinta; el titular se desplaza 0,3 rem |

La estructura no cambia y la foto sigue cambiando al abrir cada fila. El filete
de acento no se anima como borde —animar un `border` no da nada— sino con una
tapa del color del fondo que se retira de arriba abajo.

## El rail, versión final

- **Sobre el hero, blanco. Sobre claro, violeta de marca.** Al 50 % de opacidad
  no se veía; las marcas inactivas van a .62 y engordan medio píxel.
- **No entra en el pie: se apoya en él.** A medida que el pie sube, el rail se
  levanta 190 px y se desvanece. El movimiento está atado al scroll, no a un
  reloj: la línea de tiempo es la entrada del pie en la ventana
  (`view-timeline` en el pie + `timeline-scope` en `:root`), así que sube al
  ritmo exacto al que scrolleás y baja si volvés. Sin soporte, el mismo efecto
  por clase con un observer.
- El centrado vive en `transform` y el empuje en `translate`, que son dos
  propiedades distintas y se componen: por eso la animación puede tocar una sin
  pisar la otra.

**Y el error de fondo que había detrás de todo esto:** el hero es `sticky`, se
queda pegado arriba tapado por las secciones siguientes, así que para un
IntersectionObserver está *siempre* a la vista — por eso el rail se quedaba
blanco toda la página. Y observar el cruce de un borde tampoco sirve: con un
salto de ancla el elemento cruza la banda entre dos fotogramas y no hay
notificación. Lo que sí es fiable es **la sección activa**, que ya la mantienen
los observers del rail y sí se actualiza al saltar.

## Particuliers, segunda vuelta

Dos intentos descartados antes del bueno, y por qué:

1. **Filete de acento al lado del texto.** Quedaba flotando: una raya de color
   apoyada junto a un párrafo, sin pertenecer a nada.
2. **La fila abierta como tarjeta que sobresale de la columna.** Rompía la
   línea vertical que comparten el titular, las filas y el botón, que es lo que
   sostiene la sección entera. Se veía desalineado, que es peor que soso.

3. **Panel de respuesta con remate de color.** Alineado, sí, pero seguía
   siendo una caja: un objeto más compitiendo con la foto grande que tiene al
   lado, y se leía pegado encima de la lista.

Lo que quedó, y el criterio que lo ordena: **esta sección no necesita una
caja**. Es una lista editorial dentro de una columna de texto, al lado de una
foto. Así que el acento no es una pieza nueva sino **una que ya estaba
cambiando de estado**: al abrir, el filete que separa las filas se enciende en
verde agua y se traza de izquierda a derecha. La respuesta fluye debajo del
título, sin fondo. Nada flota, nada se desalinea, nada compite con la foto.

El marcador tampoco se rellena de oscuro al abrir —pesaba demasiado para una
lista de texto—: el contorno y la cruz pasan al violeta y la cruz gira.

| | F&Q | Particuliers |
| --- | --- | --- |
| Contenedor | panel permanente con borde | lista al aire, sin panel |
| Al abrir | se tinta la fila entera | aparece un panel sólo para la respuesta |
| Acento | barra vertical en el canto izquierdo | remate superior del panel, trazado |
| Marcador | chevron desnudo, gira 180° | cruz en un círculo que se rellena |

## Nos engagements: de grilla a pestañas

Seis párrafos en una grilla de filetes era lo más parecido a una plantilla que
tenía la página: información correcta, cero intención. Y la grilla se rompía
sola —los filetes verticales dejaban de llegar al horizontal en cuanto había
separación entre filas—, que es la señal de que ese layout no era el adecuado.

Ahora son **pestañas**: la lista numerada a la izquierda, el texto grande a la
derecha, y un indicador que se desliza de una a otra. Se recorren solas con una
barra de progreso y se paran **para siempre** en cuanto el usuario toca, enfoca
o pasa por encima: una animación que insiste después de que alguien la
interrumpió es una animación que molesta. También se para si la sección no está
a la vista.

El indicador es **uno solo y se mueve**: dos barras encendiéndose y apagándose
se leen como dos cosas; una que se desplaza se lee como una sola atención que
cambia de sitio. Y su parte llena es la barra de progreso, así que la misma
pieza dice dónde estás y cuánto falta.

Es además el único gesto de este tipo en la página —el bento es una grilla,
particulares una lista, el blog tarjetas, la F&Q un acordeón—, así que la
sección tiene una impronta que no se repite. El marcado es un `tablist` de
verdad (teclado y lectores de pantalla), y los seis textos están siempre en el
DOM para el buscador. En móvil la lista se vuelve una tira de números.

## F&Q

Se probó a dos columnas con el enunciado sticky al costado y se descartó: en
horizontal la sección perdía el ritmo vertical del resto de la página. Vuelve
al apilado —enunciado, panel, CTA— con dos cosas que sí se quedaron: **el
número de cada pregunta** (seis preguntas sueltas se leen como una lista; seis
numeradas, como un índice) y más aire abajo.

## Las tarjetas del blog

Foto arriba, texto y leyenda debajo, en ese orden. El relleno vive en el
cuerpo y no en la tarjeta, así la foto llega a los bordes; el redondeo lo
hereda del recorte. Al pasar por encima la foto hace un zoom lento —1200 ms—
que es el único movimiento de la tarjeta además del que ya tenía.

Las fotos son **provisionales**: salen del banco actual y hay que cambiarlas
por las de cada artículo real.

## Engagements, segunda pasada

El UX estaba bien pero la UI era de plantilla. Lo que cambió:

- La lista pasa a ser un **índice tipográfico con filetes**, separado del panel
  por una línea vertical. Es el mismo recurso que ordena particulares y la
  F&Q, así la sección pertenece a la página en vez de parecer un módulo
  pegado. La pestaña activa se corre hacia la derecha.
- El panel deja de ser texto pequeño en un hueco grande: **el número va enorme
  y hueco** detrás —sólo contorno, porque relleno sólido competiría con el
  titular—, el titular sube a tamaño editorial y el cuerpo va en tamaño de
  lead, no en letra chica.
- Un filete de acento sobre el titular que se traza al cambiar de pestaña: el
  mismo gesto que en particulares, en el otro extremo de la pieza.

Sin tarjetas, por pedido: todo el peso lo llevan la tipografía, los filetes y
el número.

## Engagements, tercer concepto: una regla horizontal

Los dos intentos anteriores fallaban por lo mismo: trataban los seis
compromisos como una **lista de items**, y una lista de seis items
equivalentes no tiene forma propia. Ahora se tratan como una **escala**: los
seis están a la vista al mismo tiempo, alineados sobre una regla horizontal, y
lo único que cambia es dónde está puesta la atención. La promesa activa se lee
abajo en cuerpo grande, como una declaración, no como el párrafo de una ficha.

La regla no se subraya entera: se llena el tramo del compromiso activo, y ese
relleno es el temporizador. Al pasar al siguiente, el tramo se desliza en vez
de encenderse.

El eje horizontal no se repite en ninguna otra sección —el bento es una
grilla, particulares y la F&Q listas verticales, el blog tarjetas—, así que la
impronta es única sin inventar un lenguaje nuevo.

## Dos arreglos chicos

- **Particuliers**: fuera el círculo del marcador. En una lista de texto era un
  objeto de más; queda la cruz sola, que gira al abrir.
- **Header**: el panel del mega menú dejaba dos franjas de fondo a los
  costados. La causa era `position:relative` en `.hdr-in`: los paneles tomaban
  *ese* bloque como referencia y su `left:0/right:0` caía en el borde interior
  del contenedor. Ahora el velo de la barra se pinta detrás con `z-index:-1`
  (y `isolation` en el header para que ese negativo no se escape), `.hdr-in`
  deja de estar posicionado, y la referencia vuelve a ser la barra —que ocupa
  todo el ancho—. El panel llega de borde a borde.

## Los dos acentos, con trabajo repartido

El problema de fondo en engagements y en la F&Q era el mismo: el verde agua
flotando sobre fondos claros. Sobre blanco da 1,3:1 — no alcanza ni para una
línea de 3 px, y por eso todo se veía "al aire".

La regla que ordena las dos secciones ahora:

- **Verde agua** sólo donde hay **texto oscuro encima**: la pastilla del número
  activo. Ahí rinde 13:1 y se ve como un color, no como un velo.
- **Violeta de marca** para todo lo que tiene que leerse contra el fondo: el
  tramo lleno de la regla, el canto de la fila abierta, el título activo.
  15,6:1 sobre claro.

La **pastilla del número es la misma pieza en las dos secciones**, y eso es lo
que hace que se lean como un sistema y no como dos módulos sueltos.

### Engagements

El bloque se apoya ahora en un **panel blanco** con el mismo borde que las
demás cajas de la página. La sección es gris; el panel la recorta y le da
presencia sin inventar un lenguaje nuevo. La regla de progreso vive en el borde
inferior de la fila de pestañas, y el número hueco enorme queda como marca de
agua dentro del panel, no flotando fuera.

### La F&Q se quedó como estaba

Se probó a aligerarla igual que engagements y la clienta prefirió la versión
anterior. Vuelve tal cual: peso 500 en las preguntas, canto de 3 px en verde
agua, fila abierta en gris.

### Los desplegables de Particuliers

Los ajustes de peso y acento iban acá, no en la F&Q:

- Los títulos bajan a **400** (el abierto sube a 500, que es toda la jerarquía
  que hace falta). Seis títulos en 500 se leían gritados.
- La fila abierta se apoya en un **velo del violeta de marca al 4 %**: suelo
  suficiente para que el bloque deje de flotar, sin meter un gris neutro. El
  velo respeta exactamente el ancho de la columna.
- El filete de acento lleva **los dos colores repartidos**: arranca en verde
  agua durante 54 px —un tramo corto, donde se nota— y sigue en violeta, que
  es el que se lee contra el fondo claro.

## El número de engagements, relleno

El contorno de 1 px a 6 rem se veía como un dibujo a mano alzada. Pasa a
relleno sólido al 14 % del violeta: pesa lo justo para ser marca de agua sin
competir con la declaración.

## Particuliers, versión definitiva: un panel de la familia

La lista suelta sobre el fondo no pertenecía a la página. El resto son cajas
blancas con un filete —el bento, la F&Q, el panel de engagements— y esto eran
seis renglones al aire. Pasa a ser **un panel de la misma familia**, y lo que
la distingue de la F&Q es el detalle, no el envase:

| | F&Q | Particuliers |
| --- | --- | --- |
| Marcador | número + chevron que gira 180° | cruz que gira a × |
| Acento | barra **vertical** en el canto izquierdo | filete **horizontal** al pie de la fila, bicolor |
| Fila abierta | gris | gris, y la foto de al lado cambia |

Tres cosas que arreglan lo que se veía mal:

- **Los filetes internos van más claros que el borde del panel**
  (`rgba(32,32,69,.09)` contra `--line-card`). Dentro de una caja, una línea al
  mismo valor que el contorno se lee como si la caja estuviera partida en seis.
- **Peso 400 y cuerpo más contenido** en los títulos. En la Outfit el 500 a
  1,3 rem se lee casi como negrita, y seis títulos así seguidos gritan.
- El marcador se centra con `margin-top` y no con `translate`: esa propiedad la
  usan las animaciones de entrada y no conviene que dos cosas escriban la
  misma.

Y un bug que venía de antes: el bloque de animación seguía creando un
`::before` en cada fila para trazar los filetes viejos, **pisando el `::before`
del acento**. Los filetes ahora son bordes internos del panel, así que esa
animación se reemplazó por la misma que usa la F&Q: entra el panel como bloque
y dentro las filas se encienden en orden.

## Una sola cápsula en la barra

El selector de idioma era una píldora al lado del botón de cita. Dos cápsulas
de altura parecida y pegadas se leen como **dos botones**, y el CTA dejaba de
ser el único sitio donde hacer clic. Además estaban al revés de lo que valen:
el idioma se usa una vez por visita, el CTA es la conversión de la página. Y
cuando dos cosas comparten forma, el usuario espera que compartan
comportamiento — el selector no es un botón.

Ahora es texto: `FR | EN | ES`, con el activo en el acento, en 600 y con un
subrayado corto. Tres señales en vez de una, porque sobre el vídeo el acento
es blanco y el contraste de color entre activo e inactivo es mínimo: ahí el
subrayado es lo que hace el trabajo.

Los separadores se **dibujan** con un pseudo-elemento, no se escriben: un
` / ` en el marcado lo leería el lector de pantalla y lo recogería el
extractor de textos para traducir.

Medido: sobre el vídeo los inactivos quedaban en 4,21:1 con el `--text-2`
general (texto chico, hace falta 4,5), así que en ese estado suben a blanco al
94 % → 4,73:1. Sobre la barra clara, 7,9:1. El activo, 5,1 y 15,1.

## La landing sigue el ritmo de fondos de la home

Tenía franjas: gris de 86 px entre el hero oscuro y una sección blanca, y dos
bloques grises seguidos partidos por un degradado al blanco en el medio. La
regla de la home es la contraria: **bloques largos de un color con rampas en
los bordes, nunca franjas sueltas**.

    hero oscuro
    blanco   → marcas + cuerpo (la rampa al gris la hace el bloque que se va)
    gris     → servicios + contacto
    blanco   → último tramo de contacto, antes del corte al pie

Y el primer bloque claro arranca con las esquinas redondeadas sobre el hero
(`band-top`), que es lo que hace que la página se lea como una hoja que sube
por encima de la imagen — igual que en la home.

**El logo vuelve a la home** desde cualquier página interior. Lo resuelve
`sync_shell.py` al copiar la cabecera y el pie: en la home el logo es un ancla
al principio de la página, en una página interior tiene que volver a la raíz,
que es lo que todo el mundo espera al hacer clic en un logo. En `/en/…` vuelve
a `/en/`, no a la home francesa.

## Lo que ya se ve al cargar no se anima con el scroll

Las entradas de la página van atadas al scroll. Para lo que está en la primera
pantalla eso **no funciona**: el progreso de una animación de scroll depende de
cuánto scrolleaste, así que el elemento arranca a medio camino y se queda ahí
hasta que el usuario mueve la rueda. En la landing eso dejaba media franja de
marcas invisible al cargar.

El JavaScript marca los elementos que están en la primera pantalla y el CSS les
cancela la animación y hace el fundido con una **transición**, escalonada, que
termina alrededor del segundo.

Dos cosas que costaron encontrar:

- **No alcanza con cambiar `animation-timeline` a `auto`.** Chromium deja la
  animación en `playState: "running"` con `currentTime: null`, porque el
  elemento conserva la ViewTimeline inactiva. Se ve como si nunca arrancara. Hay
  que cancelar la animación y usar otra cosa.
- **Hacen falta dos `requestAnimationFrame`** antes de disparar la transición:
  con uno solo, el estado inicial y el final caen en el mismo recálculo y no hay
  nada que animar.

Y el escalonado se corta a 60 ms por elemento y 420 ms en total: con muchos
elementos arriba, un retardo proporcional dejaría al último entrando varios
segundos después de que la página ya está quieta.

## Dos arreglos en el hero de la landing

- **Aire entre el hero y la franja de marcas**: la banda de logos arranca con
  su propio padding superior, no pegada al corte de la foto.
- **El botón fantasma desaparecía al pasar el mouse.** La regla local pintaba
  fondo y borde pero no el color del texto, así que ganaba el `.btn-ghost:hover`
  general, que lo pone en violeta de marca — invisible sobre el hero oscuro. El
  color va escrito.

## El hover del botón fantasma del hero

Verde agua, igual que el del botón blanco de al lado: los dos botones del hero
responden con el mismo color. El texto va oscuro, que es donde ese verde rinde
(12,3:1 en violeta de marca sobre verde agua).

## Tercera página: la landing de particulares

`/particuliers/`. Primer boceto, con el mismo esqueleto que la de empresas
—hero a media altura, bloques largos de fondo con rampas, panel de contacto
compartido— y dos cosas propias:

**La franja de opiniones de Google**, que el documento pide expresamente en
esta página. Es el mismo bloque que en la home y lo alimenta el mismo
endpoint. Para eso hubo que cambiar cómo la página encuentra el endpoint: antes
se deducía de la URL quitando la carpeta de idioma, y eso no escala —no se
puede saber, mirando `/particuliers/`, si esa carpeta es un idioma o una
página—. Ahora la sección lo declara en `data-api`.

**Dos modos de acompañamiento, lado a lado.** No son dos servicios
equivalentes sino dos formas de trabajar, así que van en paralelo y no en
lista, y la de gestión completa lleva el tinte verde agua: es la que la
agencia quiere vender, y es la única diferencia de peso entre las dos.

### Lo que hay que confirmar con la clienta

El documento lista, en este orden: dos modos de acompañamiento, dos servicios
numerados y un recuadro con dos prestaciones. **Aquí los dos numerados cuelgan
de «Gestion des démarches» y los dos del recuadro de «Conseil et guide»**, que
es la lectura que hace coherente la lista — pero es una interpretación, y está
marcada como tal en la página. Si la clienta los quiere sueltos, es mover dos
bloques.

También sigue abierto el CTA: el documento da cuatro opciones sin elegir. Queda
«Contactez-nous», el único que no depende de una decisión comercial todavía
pendiente (el primero, «Consultation gratuite ?», lleva signo de pregunta en el
propio documento).

## Entrar a las landings desde el header y desde los servicios

**Los nombres de grupo del menú son enlaces.** «Entreprises» y «Particuliers»
dejan de ser botones y llevan a su landing; el panel se sigue abriendo al pasar
por encima o al enfocar. «Ressources» sigue siendo botón porque todavía no
tiene página.

En teléfono no hay hover, así que el primer toque sobre el nombre **despliega
el grupo en vez de navegar**: un toque no puede sacarte de la página antes de
haberte dejado ver el menú. El enlace sigue disponible dentro del panel.

Dos detalles que esto rompió y hubo que arreglar:

- `aria-expanded` sólo se escribe si el elemento es un `<button>`: en un enlace
  ese atributo no significa nada.
- El panel tenía un listener que lo cerraba al tocar cualquier `<a>` de
  adentro, para que el ancla no saltara detrás del menú. Ahora los nombres de
  grupo también son enlaces, así que tocarlos cerraba el panel entero —
  deshaciendo justo lo que el usuario acababa de pedir. Quedan excluidos.

**«Voir plus» en cada fila de particulares**, que es lo que pide el documento
de la clienta, apuntando a la landing. Es un enlace y no un botón: dentro de la
fila ya hay una jerarquía —título, respuesta— y un botón por fila competiría
con el CTA de la sección.

Las cajas del bento de empresas ya llevaban a su servicio en la landing desde
antes.

---

## Fondo único, botones verde agua, texto con más peso (08/10)

**Fondo.** La página es blanca de punta a punta. La única excepción es
"Nos engagements, votre garantie" (`.tinted`), en el gris de marca `#eeeeee`
plano. Ya no hay ningún `linear-gradient` de fondo: `#avis`, `#entreprises`,
`.clients`, `#particuliers`, `.res`, `.band-alt` y, en las landings,
`#agilite`, `#services` y `#approche` apuntan todos a `--ground`. Las reglas
se dejan escritas en vez de borradas para que se vea que es una decisión y no
una sección a la que se le olvidó el fondo. Con un solo corte en toda la
página no hay nada que disimular, que era para lo que estaban las rampas.

**Verde agua, dos valores.** El verde de marca `#55ffd2` sólo sirve sobre
oscuro: sobre blanco da **1,26:1** y desaparece. Para fondo claro hace falta
una versión más oscura del mismo tono (163°), `--aqua-deep:#12a383`, **3,19:1**,
que es el mínimo de un elemento gráfico. La usa el rail al cruzar las secciones
blancas.

**Botones.** El verde agua con fondo transparente es **sólo de los dos botones
del banner de la home** (`.hero .btn`): ahí compiten contra una imagen a
pantalla completa y el verde de marca rinde 15,5:1. El resto de los CTA de la
página siguen con el esquema de siempre (azul macizo el primario, filete el
fantasma), porque sobre blanco ese mismo verde no se lee.

La regla del CTA blanco sobre el vídeo se acotó a `.hdr-right`: antes alcanzaba
a cualquier `.btn-primary` dentro de la barra, incluido el del panel del mega
menú, que terminaba blanco sobre la caja verde agua.

**Velo de la barra sobre el vídeo.** Era `rgba(9,9,20,.46)`, un gris azulado
que no está en ninguna paleta. Ahora es el azul de marca, `rgba(32,32,69,.52)`.
El alfa sube de .46 a .52 porque el azul es más claro que el gris que había y
sin eso el blanco de la barra perdía contraste contra el vídeo.

**Peso del texto.** El cuerpo estaba en 400 y el `.lead` en 300: a 17px, Jost
en esos pesos se lee como una nota al pie. Cuerpo a **450**, `.lead` y
`.body-2` a 400/450, y `--text-2` de `#4d4d6b` a `#3d3d5c`. Para que 450 sea
un peso real y no uno sintetizado, el `<link>` de Google Fonts pasa de pesos
sueltos (`wght@300;400;500;600`) a rango variable (`wght@300..600`).

**Rail.** `--rail-on` pasa de `--accent` (azul) a `--aqua-deep` sobre claro y a
`--aqua` sobre oscuro; el apagado, a `rgba(18,163,131,.6)` y
`rgba(85,255,210,.55)`. El 3,19:1 del activo sobre blanco pasa el mínimo de
elemento gráfico.

---

## El color como detalle (08/10, 2ª tanda)

Dirección de la clienta: **el color se usa en detalles**, no como fondo.

**Banner.** El H1 pasa a "Votre expert en immigration en France". Sigue en dos
`.ln` para que la animación de entrada entre por líneas.

**Nombre de sección.** Cada sección lleva su `.label` y es el único sitio de la
página donde el verde agua hace de texto. Se añadieron los dos que faltaban:
"Blog" y "Contact". `"Ils nous font confiance"` cuenta como el nombre de la
franja de logos y toma el mismo color. Sobre claro va `--aqua-ink` (#0d7d63,
**5,09:1**); el pie y los heros oscuros lo pisan con el verde de marca.

**Barra de progreso en lila.** El lila de marca `#d2d2ff` da 1,4:1 sobre
blanco. Se añade `--lilac-deep:#8686e0`, mismo tono (240°), **3,23:1**, que es
el mínimo de un elemento gráfico. Sobre oscuro vuelve el `--tint-3` de marca.

**Logo recortado en Safari.** Era `height:26px` + `width:auto` +
`aspect-ratio:1138/278`. Chrome y Firefox deducen el ancho del aspect-ratio;
Safari se queda con el viewport por defecto de un `<svg>` sin atributos
(300×150) y corta el logo por la derecha. Ahora el ancho se calcula:
`--logo-h` × 1138 / 278. Mismo resultado en los tres motores y sin depender de
ninguna heurística. De paso, `.hdr.is-solid` llevaba `backdrop-filter` sin
`-webkit-`: en Safari la barra sólida no desenfocaba. Auditado el resto:
`interpolate-size`, `::details-content` y todo lo de scroll-driven ya están
detrás de `@supports`, con la caída por IntersectionObserver.

**Empresas: listado en vez de mosaico.** El titular y su bajada se quedan a la
izquierda; los cinco servicios bajan en columna a la derecha, separados por
filetes (referencia: *L'approche JJ Capinvest*). Dos razones: cinco cajas en
fila obligaban a leer en zigzag una lista, y tres de ellas tenían el fondo
pintado, que era justo el uso del color que la clienta no quiere. El color
queda en el número (01…05) y en el filete que crece al pasar por encima. La
sección baja de 641 px y sigue entrando en pantalla.

Cuidado con el nombre de las clases: las landings ya usan `.svc`, `.svcs` y
`.svc-n` para otra cosa. El listado de la home es `.b2b-list` / `.b2b-row`.

**Blog.** "Centre de ressources" → "Derniers articles". Las tarjetas pasan a
ser la foto: el texto va encima, sobre un velo degradado. Medido ocultando el
texto y muestreando el fondo bajo cada titular: **10,9:1** en el peor píxel de
las tres. Cada tarjeta tiene un color de la paleta y lo usa en dos sitios, el
rótulo y el borde que se enciende en hover (verde agua, lila, amarillo). Las
fotos siguen siendo provisionales.

---

## Iconos, presencia de la prueba social y filete completo (08/10, 3ª tanda)

**Empresas, iconos en vez de números.** Una numeración dice "primero,
segundo, tercero" y los cinco servicios valen lo mismo: el icono identifica
sin ordenar. Cinco símbolos de trazo 1.5 en cuadro de 24, en un sprite local
de la sección (no el compartido: el listado es sólo de la home). Los atributos
`fill`/`stroke` van en cada `<symbol>`, no en un `<g>` que los envuelva — un
`<g>` del sprite no se clona con `<use>` y los iconos salen negros macizos.

**"Ils nous font confiance".** Pasaba inadvertida: 86 px entre dos secciones
grandes se leen como un intersticio. Ahora tiene respiro propio y los logos
son un 40 % más grandes — las medidas se tocaron en los atributos
`width`/`height` de cada `<img>`, que es donde vive el equilibrio óptico de la
fila, no con un `transform:scale`, que no ocupa espacio. 206 px. Sigue sin
fondo: la presencia la da el espacio.

**Particuliers, el filete llega al final.** Eran 56 px de verde agua y el
resto violeta. Ahora va de `--tint-1` a `--aqua-deep`: el verde de marca solo
da 1,2:1 contra el gris de la fila abierta y el extremo derecho desaparecía;
oscureciéndolo hacia la derecha se lee verde agua en todo el ancho y el filete
existe de punta a punta.

---

## Perfil fijo en las landings (08/10)

El formulario de contacto es un bloque compartido (`shell:contact`), así que
no se puede editar a mano en cada landing: `sync_shell.py` lo reescribiría en
la siguiente pasada. La variación vive en el script, en `lock_profil()`: en
`entreprises/` y `particuliers/` el selector Entreprise / Particulier
desaparece y el perfil queda fijo en el de la landing.

El valor sigue viajando en un `<input type="hidden" name="profil">`, así que
el backend recibe exactamente lo mismo que desde la home, y `data-profil` del
form queda escrito en el HTML: `setProfil()` corre igual al cargar y muestra u
oculta los campos `data-only` sin que haya radios que escuchar. El campo
oculto no abre fila en la grilla del formulario — la hoja del navegador ya le
pone `display:none`.

La home conserva el selector: es la única página donde el visitante puede ser
cualquiera de los dos.

---

## Banner de las landings (08/10)

Los dos botones del hero de cada landing pasan al mismo esquema que el banner
de la home: verde agua de marca, filete del mismo color y fondo transparente.
Antes eran blancos macizos. `.btn` y `.btn-ghost` quedan iguales a proposito —
aqui tampoco hay un CTA que valga mas que el otro — y el color se escribe en
los dos estados, porque si no gana el `.btn-ghost:hover` general, que pinta
violeta de marca y sobre el hero oscuro desaparece.

El resto de los CTA de las landings, los que van sobre blanco, no cambian: ahi
el verde de marca da 1,26:1.

---

## SEO y GEO (08/10)

### robots.txt
Criterio pedido por la clienta: Google entra a todo, **GPTBot bloqueado**,
**OAI-SearchBot permitido**. La misma lógica se aplicó al resto: los
rastreadores que alimentan una **búsqueda** —y que por tanto pueden citar y
enlazar— entran (Bingbot, PerplexityBot, ChatGPT-User, Claude-SearchBot,
Applebot); los que solo recogen texto para **entrenar** no (CCBot,
Applebot-Extended, Bytespider, Meta-ExternalAgent).

`Google-Extended` se deja **abierto** a propósito: bloquearlo saca a INWARD de
Gemini y de las respuestas de IA de Google, que es lo contrario de lo que se
busca con el GEO. Si la clienta prefiere cerrarlo, es una línea.

Ojo con una regla de robots.txt que se olvida siempre: **los grupos no se
heredan**. Un `User-agent` con bloque propio ignora por completo el grupo `*`,
por eso cada permitido lleva su `Allow` escrito aunque parezca redundante.

### sitemap.xml
Lo genera `build.py` a partir de `tools/pages.py`, con tres reglas:
no entra una página marcada `noindex`; no entra una traducción incompleta
(build.py ya le pone `noindex`); y cada URL declara sus alternativas con
`xhtml:link`, que es lo que le dice a Google que `/en/` y `/es/` son la misma
página en otro idioma y no contenido duplicado.

### Páginas nuevas
`/blog/`, dos artículos con URL propia, `/videos/` y una página por vídeo. Las
crea `tools/newpage.py`, que escribe la cabeza completa —canonical, hreflang,
og:, JSON-LD— para que ninguna página nazca coja. Las dos de artículo van con
`noindex` hasta que la clienta escriba el texto: una página vacía indexada
hace más daño que no existir. Al publicar el texto: quitar el meta, añadir
`datePublished` al JSON-LD y borrar la bandera en `pages.py`.

### Enlaces
Ya no queda ni un `href="#"` en el sitio. Lo que tiene destino es un `<a href>`
real y navega sin JavaScript: las tarjetas del blog, "Tous les articles",
el grupo "Ressources" del menú (que era un `<button>` y ahora es un enlace a
`/blog/`) y el pie. Lo que **no** tiene destino —mentions légales, RGPD, CGV,
recrutement, l'histoire d'Inward— dejó de ser un enlace y pasó a ser texto con
el marcador de pendiente: un ancla vacía es un enlace roto para un rastreador
y un callejón sin salida para quien navega con teclado.

### Imágenes
Nombres de archivo descriptivos en francés
(`hero.webp` → `fondatrices-inward-palais-garnier-paris.webp`,
`duo.webp` → `consultantes-inward-bureau-cabinet.webp`, los logos con prefijo
`logo-`) y alt repasado uno por uno; los de los logos pasan a "Logo de X,
client d'INWARD". Se generó además la imagen de compartir que faltaba,
`og-inward-partage.jpg`, 1200×630 recortada del hero.

### JSON-LD
Un solo `@graph` por página con `@id` compartidos: la organización se declara
**una vez**, en la home (`#organization`), y las demás páginas la referencian.
Así Google ve una entidad INWARD y no ocho fichas sueltas. Qué lleva cada una:

| página | nodos |
|---|---|
| home | Organization, WebSite, WebPage, ItemList de los **chiffres clés** (99 %, +45, +1000 como `QuantitativeValue`), ItemList de servicios B2B y B2C, VideoObject |
| landings | WebPage, BreadcrumbList, Service con `hasOfferCatalog`, ItemList |
| blog | Blog, CollectionPage, BreadcrumbList, ItemList de artículos |
| artículo | BlogPosting, BreadcrumbList |
| vídeos | CollectionPage, BreadcrumbList, ItemList |
| vídeo | VideoObject (duración y medidas sacadas del archivo con ffprobe) |

Los servicios de las landings **se generan del propio HTML** de la página, así
que la ficha no puede acabar diciendo algo distinto de lo que se lee.

Lo que no se sabe no se escribe: teléfono, email, redes sociales y la fecha de
publicación del vídeo siguen pendientes de la clienta y por eso no están. Una
ficha incompleta es correcta; una con datos inventados es un problema. Y la
`FAQPage` se añade cuando existan las seis respuestas: hoy la primera es texto
de relleno y marcarlo como FAQ sería marcado engañoso, que es sanción directa.

### Dos bugs que salieron en la auditoría
- Las landings no tenían `#hdrSentinel`: la barra nunca pasaba a sólida y
  bajaba en blanco sobre fondo blanco. Añadido a 50 vh.
- Una página sin hero oscuro necesitaba la barra sólida desde el principio;
  ahora `main.js` se la pone cuando no encuentra centinela.

---

## Landing entreprises, segunda pasada (08/10)

**La barra de progreso no funcionaba.** Las secciones observadas estaban
escritas a mano en `main.js` con los ids de la home
(`#avis,#entreprises,#particuliers,…`), así que en las landings no se
observaba ninguna y el indicador no se movía nunca. Ahora salen **del propio
rail**: si tiene un enlace, su sección se observa. Una página nueva funciona
sola y no hay dos listas que puedan discrepar.

**Banner más claro.** El velo baja de `.9/.8/.68/.5/.4` a `.74/.64/.54/.46/.42`
y el refuerzo lateral de `.62` a `.5`. Más claro no se puede: medido ocultando
el texto y muestreando el fondo real, el rótulo verde agua —el texto más
pequeño— queda en 7,0:1, el H1 en 5,1:1 y el párrafo en 7,4:1. Un escalón más
y el rótulo baja de 4,5. La parte de arriba del hero es la zona clara de la
foto y es justo donde viven el rótulo y el titular.

**"Ils nous font confiance".** Los logos de esta página llevaban sus propias
medidas (no es un bloque compartido) y se habían quedado al tamaño viejo:
crecidos un 40 % como en la home. La sección pasa de 86 a 206 px.

**Checklist "Ce que vous y gagnez".** El párrafo que había decía cuatro cosas
seguidas y no se leía ninguna. Las mismas cuatro, una por línea, con título y
marca. La marca es un tilde dibujado con dos bordes y una rotación, no un `✓`
de texto: un carácter cambia de forma con la fuente y no se alinea.

**Servicios en acordeón.** `<details>` nativo, una columna. Cerrado se ve el
título y **una** línea recortada; "Voir plus" abre el resto y el CTA. El
atributo `name` lo hace exclusivo sin una línea de JavaScript, y todo el texto
está en el DOM aunque esté cerrado: esto es presentación, no contenido oculto,
y el buscador lo ve igual.

Dos detalles: el `<summary>` no lleva `<h3>` —su modelo de contenido admite
*phrasing content* o **un** encabezado, y aquí hacen falta título, resumen y
marcador—, así que el título es un `<span role="heading" aria-level="3">`. Y
"Voir plus"/"Voir moins" son dos `<span>` que se alternan por CSS, no un
`::before` con `content`: el texto de un pseudoelemento no lo ve
`extract_strings.py` y esas dos palabras se quedarían sin traducir.

**Types de visa.** Dos filas con dos trabajos distintos: arriba *qué* se puede
obtener (cinco cajas en el gris de marca, icono en verde agua), abajo *qué* se
puede hacer con ello (los tres CTA, las únicas cajas macizas de la página). La
diferencia de peso dice cuál es información y cuál es acción sin un solo
rótulo que lo explique.

**Avis Google y F&Q.** Añadidas. La F&Q lleva las cinco preguntas del
documento que son de empresa, no las seis de la home: repetir la lista entera
en dos páginas es contenido duplicado y las dos de particular no pintan nada
aquí.

El JSON-LD de la página se regeneró: los cinco servicios, los tipos de visa y
las tres gestiones salen del propio HTML, así que la ficha no puede acabar
diciendo algo distinto de lo que se lee.

---

## Confiance como sección y números en verde agua (08/10)

**"Ils nous font confiance" pasa a ser una sección entera** en la landing de
empresas (631 px, el mismo peso que las demás). Mantiene el marcado y la clase
`.logos`; lo que cambia es que las marcas pasan de fila a rejilla de cuatro
columnas, con el nombre de sección y un H2 como el resto de la página. En la
home sigue siendo la franja compacta: ahí es una nota al pie entre dos
secciones, aquí es argumento de venta.

**Sin líneas entre celdas, a propósito.** Una rejilla cuadriculada solo queda
bien cuando el número de marcas es múltiplo del número de columnas: con 7
logos y 4 columnas, la celda vacía deja el marco abierto por dos lados. Y el
número va a cambiar —van a llegar más marcas—, así que el diseño no puede
depender de él. Con aire en vez de filetes, las celdas que sobran son
invisibles y la rejilla acepta cualquier cantidad sin tocar nada. Las dos
únicas líneas son las del bloque entero, arriba y abajo: esas existen siempre.

Por la misma razón la animación entra como bloque y no logo a logo: el
escalonado de la home está escrito con `nth-child` para siete, y aquí el siete
no es un número fijo.

**Los números de "Nos services" en verde agua**, sin la opacidad del 50 % que
tenían. Pasan de `--accent` al 50 % a `--aqua-deep` sólido.

---

## Solo colores de la paleta (12/10)

Se eliminan los tres tonos derivados que había inventado para resolver
contraste: `--aqua-deep` (#12a383), `--aqua-ink` (#0d7d63) y `--lilac-deep`
(#8686e0). En la hoja no queda ningún hex fuera del Brand Book salvo el rojo
de error de formulario.

**El verde agua deja de ser tinta y pasa a ser fondo.** El problema de origen:
#55ffd2 sobre blanco da 1,26:1, así que como texto no existe, y oscurecerlo es
inventar un color. La solución es darlo vuelta — letra negra sobre una
pastilla verde agua, **16,4:1**, con la misma forma de píldora que los
botones. Lo usan el nombre de sección (`.label`), `"Ils nous font confiance"`
y el rótulo de la checklist.

Una sola regla sirve para fondo claro y oscuro: la pastilla no depende de lo
que tenga detrás, así que desaparecen las excepciones que había para el hero
y el pie. Lleva `justify-self:start` **y** `width:fit-content` porque el
rótulo aparece en rejillas, en flex y en flujo normal, y en una rejilla un
`display:inline-block` se blockifica y se estira a todo el ancho.

Los números de lista (`.svc-n`, `.mode-n`) usan la misma pastilla, más chica.

**Iconos y filetes** van en el verde agua de marca tal cual. Sobre blanco
pierden fuerza y es una decisión tomada: antes que inventar un tono, el icono
se ve flojo. El filete de particulares pasa a 3 px y a un solo color, sin
degradado a ningún derivado: el estado abierto ya lo dicen el fondo y la cruz
girada, el filete solo lo subraya.

**La barra de progreso** pasa al violeta oscuro de marca (`--accent`), sólida
en la activa y al 45 % en las inactivas.

Dos cosas que mordieron al hacerlo, las dos por especificidad:
`.lp-hero .label` seguía pintando el texto del mismo verde que la pastilla y
lo borraba; y `.lp-split-txt p + p` le ganaba al rótulo de la checklist —que
también es un `<p>` detrás de otro `<p>`— y le quitaba la tinta negra.

---

## Favicon que sigue el tema del navegador (16/10)

`favicon.svg` lleva su propia hoja de estilos y su propia consulta de medios:

```svg
<style>
  .ico{fill:#202045}
  @media (prefers-color-scheme:dark){ .ico{fill:#ffffff} }
</style>
```

Sobre barra clara el isologo va en el violeta de marca; sobre barra oscura, en
blanco. Un favicon SVG se evalúa como documento propio, así que esto no
necesita ni una línea de JavaScript ni un segundo archivo.

El `fill` del `<g>` se deja escrito como atributo **y** la clase lo pisa: un
motor que no entienda la regla pinta igual el violeta de marca en vez del
negro por defecto.

**El límite, medido y conocido:** Chromium rasteriza el SVG **una sola vez**,
con el esquema que esté activo cuando lo descarga, y cachea ese bitmap por
URL. Si alguien cambia el tema del sistema con la pestaña ya abierta, el icono
se queda del color anterior hasta que recargue. Firefox y Safari sí lo
reevalúan. La solución completa serían dos archivos de color fijo
(`favicon-light.svg` / `favicon-dark.svg`) y cuatro líneas en el `<head>` que
elijan con `matchMedia` y escuchen el `change`; no se hizo porque el sitio
evita JavaScript y el caso —cambiar de tema con la pestaña abierta— es raro.

`favicon.ico` sigue siendo el de respaldo para motores sin soporte de SVG, y
va en violeta fijo.

---

## Los enlaces de contenido llevan al principio de la landing (19/10)

Las cinco filas de servicios de empresas y los seis "Voir plus" de
particulares apuntaban a un ancla dentro de la landing
(`entreprises/#audit`, `particuliers/#services`). El efecto era que el
visitante caía a mitad de página, encima del mismo servicio que acababa de
leer en la home: saltaba el hero, el contexto y los otros cuatro servicios.
Ahora apuntan a `entreprises/` y `particuliers/` a secas.

**El mega menú y el pie conservan el ancla a propósito.** Ahí no estás
leyendo nada: estás eligiendo un destino concreto de una lista, y caer en él
es lo que pediste. Además esos dos son bloques compartidos: quitarles el
fragmento haría que, estando ya en la landing, el ítem del menú se convirtiera
en un enlace a `#top` (`sync_shell.py` reescribe los enlaces a la propia
página como ancla), o sea que el menú dejaría de servir justo donde más se
usa.

Comprobado con el navegador: las cuatro rutas de la home a una landing
aterrizan en `scrollY = 0`.

---

## La marca de agua de engagements, en verde agua (19/10)

El número grande del panel pasa del violeta al 14 % al verde agua de marca.
Repite el número de la pastilla activa de arriba, así que compartir color ata
las dos piezas en vez de dejar una gris y otra de color.

Sobre blanco el verde da 1,26:1 — ilegible como texto y exactamente el peso
que busca una marca de agua: se ve el color, no compite con la declaración.
Es el `--tint-1` de la paleta, sin derivar ningún tono.

---

## Más luz en los banners de las landings (19/10)

El velo del hero baja de `.74/.64/.54/.46/.42` a `.60/.50/.40/.32/.28`, y el
refuerzo lateral de `.50` a `.40`. Las dos landings comparten la regla, así
que el límite lo fija la foto más clara, que es la de empresas.

Medido ocultando el texto y muestreando el **peor píxel** del fondo bajo cada
bloque, en las dos páginas:

| | empresas | particulares | mínimo |
|---|---|---|---|
| titular | 3,89:1 | 4,96:1 | 3 (texto grande) |
| bajada | **4,73:1** | 6,25:1 | 4,5 |
| botones | 12,9:1 | 7,8:1 | 4,5 |

Un escalón más de luz y la bajada de empresas cae a 3,83:1, por debajo del
mínimo. Así que esto es el tope.

De paso: el hero de landing ya no lleva rótulo, así que el texto más exigente
pasó a ser la bajada. Antes era el rótulo, que es más chico.

---

## Particuliers: textos nuevos de "Nos services" (19/10)

Se probó a reducir la sección a dos filas de un acordeón simple y la clienta
prefirió el diseño anterior, así que vuelve tal cual: selector de dos modos,
dos paneles y dentro de cada uno sus dos prestaciones plegables. Lo único que
cambia es el texto.

- Los títulos de los dos modos pasan a **"Conseil et guide"** y
  **"Gestion et prise en charge"**. El segundo venía como
  "gestion / Prise en charge"; una barra en un título queda rara.
- Los cuatro cuerpos se reemplazan por los dos párrafos que mandó la clienta
  por servicio. Encajan uno a uno con las prestaciones que ya existían:
  párrafo 1 del servicio 1 → *Conseil, diagnostic et guide*; párrafo 2 →
  *Vérification du dossier*; y lo mismo en el servicio 2 con *Gestion de la
  demande de visa* y *freelances et créateurs d'entreprise*.

Se conservan los rótulos del selector (Autonomie / Clés en main), las frases
de entrada de cada panel y los dos CTA: la clienta mandó el texto de los
servicios, no el del envoltorio.

---

## Particuliers: dos secciones nuevas (19/10)

Entran entre "Nos services" y la F&Q, y usan **componentes distintos a
propósito**: las dos son listas que se abren, y si se vieran iguales el
visitante no tendría por qué entender que hablan de cosas distintas. Una
enumera, la otra acompaña.

| | componente | marca | se ve |
|---|---|---|---|
| **Les visas que nous accompagnons** | `.svc` (landing de empresas) | pastilla verde con el número + "Voir plus" | 7 filas, 808 px |
| **Soutien au nouvel arrivant** | `.rows` (particulares de la home) | sin número, cruz que gira a × y filete verde al pie | 4 filas, 563 px |

Ninguno de los dos necesitó CSS nuevo.

Lo que la clienta todavía no mandó va en **lorem ipsum**, no con el marcador
de pendiente: estas dos secciones son para mostrarle la maqueta y un `?` en
cada fila ensucia la lectura. El resto del sitio conserva sus marcadores,
que señalan cosas más delicadas (teléfonos, email, respuestas de la F&Q).

Queda sin confirmar el intitulado de la fila 06: "Rece" se leyó como la carte
de séjour *recherche d'emploi ou création d'entreprise*. Y los dos H2 los puse
yo; la clienta sólo nombró la segunda sección.

**Un arreglo que hizo falta:** el acordeón de `.row` cerraba *todas* las filas
de la página al abrir una. Con un solo panel en la home daba igual; aquí hay
dos listas y abrir un visa cerraba la fila abierta de soutien. Ahora sólo se
cierran las hermanas del mismo `.rows`, y `showShot` solo corre si la fila
trae `data-img`, que son únicamente las de la home.

Los tres enlaces del mega menú (Visa visiteur, étudiant, famille) pasan de
apuntar a `#gestion-visa` a su fila exacta, que ahora existe. `abreDestino()`
la abre al llegar.

---

## Soutien au nouvel arrivant: acordeón horizontal (19/10)

La disposición sale de una referencia que mandó la clienta: columnas que se
abren **de costado**. Cerradas son una franja angosta con la cruz arriba y el
nombre al pie; la abierta se ensancha y muestra el texto.

La referencia era un panel azul oscuro y así se probó primero: no funcionó.
Va en el **gris de marca**, texto negro, y el verde agua sólo en el filete
superior de la columna abierta y en el círculo activo. La columna abierta sale
en **blanco**, al revés que el panel: ese cambio de claro es lo que la
destaca, sin gastar color.

El panel no es blanco porque la sección de arriba ya es un panel blanco sobre
página blanca, y dos bloques blancos seguidos se leen como uno solo.

**El ancho se anima con `grid-template-columns`**, no con un `width` por
columna. La condición para que el navegador interpole es que los dos estados
declaren la misma cantidad de pistas, y por eso cada `data-open` escribe las
cuatro (`2.6fr 1fr 1fr 1fr`, `1fr 2.6fr 1fr 1fr`…). El JavaScript sólo escribe
qué número está abierto: la animación vive entera en la hoja de estilos.

El cuerpo de una columna cerrada **sigue en el DOM** —el buscador lo ve— y se
oculta con opacidad, no con `display:none`, que haría saltar la rejilla al
reaparecer. Se saca del tabulador con `inert`.

La marca +/× son dos barras y una rotación: ningún icono que cargar. Y el
botón cubre la columna entera con un `::after`: en una franja angosta obligar
a apuntar al círculo es pedir puntería.

En teléfono la rejilla de cuatro columnas no existe: pasa a lista vertical con
el mismo gesto, el nombre al lado del botón y el cuerpo abriéndose hacia abajo
con `grid-template-rows: 0fr → 1fr`.
