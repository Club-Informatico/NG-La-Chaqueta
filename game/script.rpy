## ============================================================================
##  LA CHAQUETA · Una leyenda de Copiapó
##  Guion principal
## ============================================================================

label start:
    scene negro
    stop music
    play ambiente viento fadein 3.0
    pause 1.0
    show cg titulo with fundido_muy_lento
    pause 3.5
    scene negro with fundido_lento
    centered "{size=+12}Copiapó{/size}\n\nDomingo 8 de noviembre" with dissolve
    jump prologo


## ----------------------------------------------------------------------------
##  PRÓLOGO · La casa de mi papá
## ----------------------------------------------------------------------------

label prologo:
    scene bg casa_noche with fundido_lento
    play music tema_ines fadein 4.0

    "Me llamo Rodolfo Pizarro. Hace veintidós años que manejo un taxi de noche en Copiapó."
    "Antes de cada turno paso donde mi papá. Le dejo el pan, le dejo las pastillas en el platito, le pregunto si comió."
    "Desde que murió mi mamá, la casa se le hizo grande. Él dice que no, que está bien. Que la casa siempre fue de este tamaño."

    show tomas neutral with dissolve

    "Hoy está sentado junto a la ventana, como cada ocho de noviembre."
    "No sé por qué. Nunca lo he sabido. Es la única noche del año en que no prende la tele, no escucha la radio, no duerme."

    t "¿Qué día es hoy, Rodo?"
    r "Ocho, papá. Ocho de noviembre."
    t "Ocho..."

    "Lo dice como quien se toca una herida vieja para ver si todavía duele."
    "En la repisa, junto a la foto de mi mamá, hay un marco puesto boca abajo. Ha estado así toda mi vida."

    menu:
        "Darle vuelta a la foto.":
            $ vio_foto = True
            "Lo levanto con cuidado. El vidrio está limpio, como si alguien lo limpiara seguido aunque nadie lo mire."
            show cg foto with dissolve
            "Es una foto en blanco y negro. Un muchacho flaco, de pelo engominado, sonriendo bajo unos árboles de ramas caídas."
            "Lleva una chaqueta de lana, oscura en la foto, con un prendedor chiquito en la solapa. Una palomita."
            "Tardo un segundo en reconocerlo. Es mi papá. Debe haber tenido veinte años."
            hide cg foto with dissolve
            t "Déjala como estaba, hijo."
            "No lo dice enojado. Lo dice cansado."
            "La dejo boca abajo otra vez."

        "Dejarla como está.":
            $ vio_foto = False
            "Algunas cosas en esta casa no se tocan. Esa foto es una de ellas."
            "Mi mamá me lo dijo una vez, cuando yo era chico: «Esa es de antes de mí. Déjala tranquila.»"

    r "Me voy, papá. Cierre con llave."
    t "Rodo."

    "Me detengo en la puerta."

    t "Si pasas por la plaza..."

    "Se queda mirando por la ventana. Afuera, las luces de las poblaciones en los cerros parecen brasas."

    t "Nada. Anda nomás. Anda con cuidado."

    hide tomas with dissolve

    "Salgo a la calle. La noche está tibia, como casi todas las noches de noviembre en Copiapó."
    "Pero mi papá, al despedirme, se frotó las manos como si tuviera frío."

    stop music fadeout 3.0
    jump plaza


## ----------------------------------------------------------------------------
##  CAPÍTULO 1 · Los pimientos
## ----------------------------------------------------------------------------

label plaza:
    scene bg plaza_noche with fade
    play music noche fadein 3.0
    play motor motor_taxi fadein 2.0

    "Once y cuarenta de la noche."
    "La Plaza Prat a esta hora es otro lugar. De día está llena de gente buscando sombra bajo los pimientos; de noche, los pimientos son lo único que queda."
    "Árboles viejos, enormes, con las ramas colgando hasta casi tocar el suelo. Como pelo largo. Como alguien que se agachó a llorar y se quedó así."
    "En el centro, la estatua de mármol de la fuente brilla blanca. Una mujer de piedra que nunca ha visto una mina."
    "Estaciono junto a la vereda a esperar pasajeros. Hoy es domingo. Los domingos no sale nadie."
    "Entonces siento el olor."
    "Dulce, espeso. Nardos. El olor de las coronas de flores en los velorios."
    "Bajo el pimiento más grande, donde la luz del farol no alcanza, hay alguien."

    show ines neutral at fantasma_aparece(0.72)

    "Una muchacha. Vestido claro, pelo oscuro peinado como en las fotos de mi mamá cuando era joven."
    "Lleva una chaqueta de lana roja que le queda enorme. Las mangas le tapan las manos."
    "No la vi llegar. Juraría que hace un minuto ese pedazo de vereda estaba vacío."

    play sound toc
    "Golpea el vidrio con los nudillos. Tres veces, despacito."

    p "¿Está libre?"
    r "Sí, claro. Súbase."

    jump taxi


## ----------------------------------------------------------------------------
##  CAPÍTULO 2 · Pasaje Los Pimientos 2347
## ----------------------------------------------------------------------------

label taxi:
    scene bg taxi_frente with dissolve
    play sound puerta

    "Se sube atrás. La puerta se cierra sin ruido, o casi."
    "Por el espejo retrovisor la veo acomodarse en el asiento, muy derecha, con las manos escondidas en las mangas."

    r "¿A dónde la llevo?"
    p "Al pasaje Los Pimientos, dos mil trescientos cuarenta y siete."

    "Conozco Copiapó de memoria. Cada pasaje de El Palomar, cada callejón de Paipote, cada población de los cerros."
    "No existe ningún pasaje Los Pimientos."

    r "¿Los Pimientos? ¿Por qué sector queda eso, señorita?"
    p "Usted maneje nomás. Yo le indico."

    "Tiene una voz bajita, educada, de esas que ya no se escuchan. Como de radioteatro."

    play sound tic
    scene bg taxi_frente_detenido

    "El reloj del tablero marca las 23:47."
    "Y se queda ahí."
    "Le doy un golpecito con el dedo. Nada. Los números rojos no se mueven."
    "El taxímetro tampoco avanza. En vez del signo peso muestra un símbolo que no reconozco: una E con un circulito arriba."
    "E°."
    "Debe ser una falla. El auto es viejo. Arranco."

    jump taxi_conversa


label taxi_conversa:
    if len(opciones_taxi) >= 2:
        jump taxi_ruta

    menu:
        set opciones_taxi
        "La avenida está vacía. El silencio pesa."

        "Preguntarle de dónde viene.":
            call taxi_pregunta

        "Prender la radio.":
            call taxi_radio

        "Mirarla por el espejo.":
            call taxi_espejo

    jump taxi_conversa


label taxi_pregunta:
    r "¿Viene de alguna fiesta? Por el vestido, digo."
    p "Vengo de esperar."
    r "¿Esperar?"
    p "Quedamos de juntarnos en la plaza. Debajo del pimiento grande."

    scene bg taxi_atras
    show ines triste at asiento
    with dissolve

    "En el semáforo de la esquina me doy vuelta un segundo."

    p "No llegó."

    "Lo dice sin rabia. Como quien da la hora."

    r "Pucha. A lo mejor se le hizo tarde."
    p "Puede ser. Una se cansa de esperar, ¿sabe? Pero no se cansa de querer que llegue."

    scene bg taxi_frente_detenido with dissolve

    "Vuelve la luz verde. Arranco. Por el espejo veo que me está mirando. No a mis ojos en el espejo: a mí. A mi nuca, a mis manos en el volante."

    p "Usted se parece a alguien."
    r "Me dicen harto eso. Tengo cara de primo de todo el mundo."
    p "No. A alguien."

    "No dice nada más. Yo tampoco."

    $ pistas.add("parecido")
    return


label taxi_radio:
    "Prendo la radio para llenar el silencio."

    play sound estatica
    "Estática. Muevo el dial, y la estática se mueve conmigo, como si la tuviera pegada al dedo."
    "Entonces, sin que yo toque nada, entra una canción."

    stop sound
    play music bolero fadein 1.0 noloop

    "Un bolero antiguo, con ese sonido gastado de las radios de tubo. De los que escuchaba mi abuela mientras planchaba."
    "Atrás, ella tararea. Se sabe la melodía entera."

    p "A él le gustaba esta. Decía que era nuestra canción, aunque nunca la bailamos."

    stop music fadeout 2.5
    "La canción se apaga y una voz de locutor, cálida, de otro tiempo, dice:"

    play sound estatica
    "«...Radio Chañarcillo. Son las veintitrés horas, cuarenta y siete minutos de este viernes ocho de noviembre de mil novecientos sese...»"
    "La estática se traga el resto. Apago la radio."
    "Hoy es domingo."

    stop sound
    play music noche fadein 2.0

    $ pistas.add("radio")
    return


label taxi_espejo:
    "Levanto la vista hacia el espejo retrovisor."

    show cg espejo_vacio with dissolve
    play sound latido

    "El asiento de atrás está vacío."
    "Se me hiela la sangre. Me doy vuelta de golpe."

    scene bg taxi_atras
    show ines neutral at asiento
    with hpunch

    "Está ahí. Sentada, derechita, con las manos en las mangas."

    p "¿Pasa algo?"
    r "No... nada. Me pareció... nada."

    "Vuelvo a mirar el camino. Respiro, y el aliento me sale blanco, como si estuviéramos en pleno julio."
    "Hace diez minutos, el letrero de la farmacia marcaba diecinueve grados."

    scene bg taxi_frente_detenido
    show cg espejo_ines with dissolve

    "En el espejo, ahora sí, están sus ojos. Oscuros. Tranquilos. Mirándome."

    hide cg espejo_ines with dissolve

    $ pistas.add("espejo")
    return


label taxi_ruta:
    scene bg avenida_noche with dissolve

    p "Por la Copayapu. Después a la derecha."

    "Bajamos por la avenida. Las luces de sodio pintan todo de naranjo; detrás de los techos, los cerros pelados del valle son una sola sombra contra las estrellas."
    "En el desierto el cielo nunca está vacío. Esta noche hay tantas estrellas que dan ganas de no mirarlas."

    p "¿Todavía sale la micro de las doce y cuarto a La Serena?"
    r "¿A La Serena? Salen varias en la noche, del terminal. No sé si a esa hora justo."
    p "Antes salía una. Siempre a las doce y cuarto. Nunca se atrasaba."
    p "Era lo único que no se atrasaba en esta ciudad."

    "Se ríe un poquito. Es una risa bonita. Me da más miedo que todo lo demás."

    p "Aquí a la derecha. Por La Paz."

    scene bg muro_cementerio with dissolve

    "Avenida La Paz. A la izquierda, el muro largo y blanco del cementerio, interminable bajo un solo farol."

    p "Aquí. Pare aquí, por favor."

    play motor motor_taxi
    r "Señorita, aquí no hay casas. Es el muro del cementerio."
    p "Yo entro por el pasaje. Siempre entro por el pasaje."

    "Saca una mano de la manga para pagarme. Me deja un billete doblado en la palma."
    "Sus dedos rozan los míos. Están fríos como el agua de una acequia en invierno."

    p "Gracias por traerme."
    if "parecido" in pistas:
        p "Usted tiene las manos de él. ¿Sabía?"
    p "Esta vez sí."

    play sound puerta
    "La puerta. Un paso en la vereda."
    "Bajo la vista para mirar el billete."

    show cg billete with dissolve

    "Diez escudos. Un billete café, blando de tan viejo, con un retrato que no reconozco."
    "Escudos. En Chile no hay escudos desde antes de que yo aprendiera a caminar."
    "E°."

    hide cg billete with dissolve

    "Levanto la cabeza."
    "La vereda está vacía."
    "No hay ningún pasaje. Solo el muro, el farol, y el viento que baja del cerro arrastrando tierra."

    play sound tic
    "El reloj del tablero salta solo: 23:52."

    menu:
        "Bajarme a buscarla.":
            "Me bajo. Camino a lo largo del muro, de un farol al siguiente. Grito «¡Señorita!» y mi voz rebota contra la cal."
            "Nada. Ni una huella en la tierra de la vereda. Solo las mías."
            "A través de la reja de la entrada, a lo lejos, me parece ver una luz moviéndose entre los nichos. Una linterna, o una vela."
            "Cuando parpadeo, ya no está."

        "Quedarme en el taxi.":
            "No me bajo. Me quedo con las manos en el volante, apretándolo, como si el auto fuera lo único sólido que queda en el mundo."
            "Pongo los seguros de las puertas. Me siento ridículo. Los dejo puestos igual."

    "Entonces me doy vuelta para mirar el asiento de atrás."

    jump chaqueta


label chaqueta:
    scene negro
    show cg chaqueta_asiento
    with fundido_lento
    play music tema_ines fadein 2.0

    "La chaqueta roja está ahí. Doblada con cuidado sobre el asiento, como se dobla la ropa de alguien que uno quiere."
    "Se le olvidó."
    "O no se le olvidó."
    "La tomo. Pesa más de lo que debería. Es lana gruesa, de hombre, tejida a mano. Huele a nardos y a algo más viejo. A ropero cerrado. A tierra."
    "En la solapa tiene un prendedor de plata: una palomita con las alas abiertas."

    if vio_foto:
        "Una palomita."
        "La he visto antes. Hace menos de tres horas. En una foto boca abajo."
        "No. No puede ser. Debe haber mil palomitas de plata en Copiapó."

    "En el bolsillo de adentro hay un sobre. Amarillento, cerrado. Con letra redonda, de colegio de monjas, dice:"
    "{i}Para Tomás.{/i}"
    "Tomás."
    "Hay muchos Tomás en Copiapó, me digo. Muchísimos."
    "Me lo digo varias veces."
    "No abro el sobre. No es para mí."
    "Dejo la chaqueta en el asiento del copiloto y arranco. No sé a dónde voy hasta que llego."

    stop music fadeout 2.0
    jump paradero


## ----------------------------------------------------------------------------
##  CAPÍTULO 3 · La niña de los nardos
## ----------------------------------------------------------------------------

label paradero:
    scene bg paradero_noche with fade
    play music noche fadein 2.0
    play motor motor_taxi

    "El paradero de taxis frente al terminal es lo único despierto en el centro a esta hora."
    "Un toldo, una banca, un hervidor enchufado a quién sabe dónde. Y Don Lucho."

    show lucho neutral with dissolve

    "Don Lucho Carvajal tiene ochenta años y hace quince que no maneja. Viene igual todas las noches, con su termo y su gorro de lana, a tomar café y a corregirnos las rutas."
    "Dicen que es el taxista más antiguo de Copiapó. Dicen también que, cuando manejaba, jamás trabajó un ocho de noviembre. Nadie sabe por qué, y nadie le pregunta."

    l "Rodito. Tienes cara de haber atropellado un perro."
    r "Don Lucho... ¿usted ubica el pasaje Los Pimientos?"

    menu:
        "Mostrarle la chaqueta.":
            "No le contesto. Abro la puerta del copiloto y le muestro la chaqueta roja."
            "El termo se le resbala de las manos. El café humea en el suelo."
            show lucho triste
            l "¿Dónde... dónde la subiste?"
            r "En la plaza. Debajo de los pimientos."

        "Contarle solo de la dirección.":
            r "Pasaje Los Pimientos, dos mil trescientos cuarenta y siete. Me lo dio una pasajera."
            "Don Lucho deja de soplar el café."
            show lucho triste
            l "¿Una niña? ¿Con una chaqueta roja?"
            "Yo no le he dicho nada de ninguna chaqueta."
            r "...Sí."

    l "La niña de los nardos."

    "Se sienta en la banca. Se ve más viejo que hace un minuto."

    l "Es un cuento de taxistas, Rodito. De los antiguos. Cada ocho de noviembre, a alguno le toca."
    l "Una niña se sube en la plaza. Da una dirección que no existe. Se baja en el muro del cementerio. Y deja la chaqueta."
    r "¿Y qué hace uno con la chaqueta?"
    l "La lleva al cementerio. Se la entrega al cuidador, al Arsenio, que es el que sabe. Él la deja donde tiene que dejarla."
    l "Al otro día la chaqueta ya no está. Y al año siguiente, otro taxista, otra vez la misma chaqueta."
    r "Don Lucho. Usted ha visto esto antes."

    "No me mira. Tiene una cicatriz vieja que le cruza la mejilla, desde la oreja hasta la comisura. Siempre pensé que era de una pelea."
    "Ahora, a la luz del tubo fluorescente, me parece que es de vidrio."

    l "Yo ya estoy viejo pa' estas cosas."
    l "Anda donde el Arsenio. Ahora, mientras sea de noche. Y no le abras el sobre a la niña."
    r "¿Cómo sabe del sobre?"

    "Pero Don Lucho ya va caminando hacia la esquina, sin su termo, con las manos en los bolsillos."

    hide lucho with dissolve

    "No se da vuelta."

    stop music fadeout 2.0
    jump cementerio


## ----------------------------------------------------------------------------
##  CAPÍTULO 4 · El cuaderno del cuidador
## ----------------------------------------------------------------------------

label cementerio:
    scene bg cementerio_reja with fade
    stop motor fadeout 2.0
    play music tension fadein 3.0
    play ambiente viento

    "La una y media. La reja del cementerio, por la avenida La Paz, está cerrada con cadena."
    "Al fondo, en la caseta, hay una ampolleta encendida."
    "Toco la bocina una vez. Corta. Me da vergüenza hacer ruido aquí."
    "La puerta de la caseta se abre."

    show arsenio neutral with dissolve

    "Un hombre bajo, de poncho y gorro, con una linterna en la mano. Se acerca sin apuro."
    "Mira la chaqueta que llevo en el brazo. Después me mira a mí."

    a "Usted viene por la niña."
    r "¿Usted es Don Arsenio?"
    a "El mismo. Pase. Ella ya no está, pero pase."

    play sound reja
    "La cadena cae. La reja chilla al abrirse."
    "La caseta huele a parafina y a café recalentado. Don Arsenio saca de un cajón un cuaderno grueso, con las tapas forradas en plástico."

    hide arsenio
    show cg libro
    with dissolve

    a "Lo empezó mi papá, que fue cuidador antes que yo. Yo lo seguí."

    "Cada línea es una fecha y un nombre. Todas las fechas dicen lo mismo: ocho de noviembre."
    "1969. 1971. 1972. 1975. 1980. 1988. 1994. 2003. 2011. 2019. 2025."
    "Nombres de taxistas. A algunos los conozco: el finado Rojas, la señora Mirta del paradero de Los Carrera, el Pato Cortés."
    "La primera línea, con la letra temblorosa del papá de Don Arsenio, dice: {i}8 de noviembre de 1969. L. Carvajal. Trajo la chaqueta.{/i}"

    r "Carvajal... Lucho Carvajal."
    a "El primero. Al año justo."
    a "Usted es el número cincuenta y ocho."
    r "¿Al año justo de qué?"

    hide cg libro with dissolve
    show arsenio neutral with dissolve

    a "Venga. Traiga la chaqueta."

    jump pasaje


label pasaje:
    scene bg cementerio_pasaje with fundido_lento

    "Caminamos por la parte vieja. Aquí los nichos son de cal y ladrillo, apilados en paredes altas como edificios para gente muy callada."
    "Flores de plástico desteñidas. Fotos ovaladas. Velas en frascos de mermelada."
    "Al final de un pasillo, clavado en la pared, hay un letrero de lata pintado a mano. Las letras están casi borradas, pero se leen:"
    "{i}Pasaje Los Pimientos.{/i}"

    show arsenio neutral at left with dissolve

    a "Antes había un pimiento aquí. Grande, como los de la plaza. Lo sacaron cuando yo era cabro chico, porque las raíces rompían los nichos."
    a "El nombre quedó. Los viejos todavía le dicen así."

    "Don Arsenio levanta la linterna."

    hide arsenio
    show cg nicho
    with dissolve
    play sound latido

    "Nicho dos mil trescientos cuarenta y siete."
    "{i}Inés Albornoz Vega. 3 de mayo de 1950 — 8 de noviembre de 1968. Tus padres no te olvidan.{/i}"
    "En el óvalo de porcelana, una muchacha de pelo oscuro, peinada como en las fotos de mi mamá."
    "Es ella."
    "No hay ninguna duda. Es la cara que tuve en el espejo retrovisor hace dos horas."

    $ nombre_pasajera = "Inés"

    a "Dieciocho añitos. Murió en un choque, en la salida a Tierra Amarilla. Iba en taxi."
    a "Dicen que el papá la mandaba donde una tía. Para alejarla de un muchacho."
    r "...De un tal Tomás."
    a "Eso no lo sé. Nadie sabe el nombre. Nadie se ha atrevido a abrir el sobre."

    hide cg nicho with dissolve

    "Saco el sobre del bolsillo de la chaqueta. Lo tengo en la mano."

    menu:
        "Abrir el sobre.":
            "Perdón, digo. No sé a quién."
            "El pegamento está seco de tanto tiempo; la solapa se abre sola apenas la toco."

        "No abrirlo.":
            r "No. No es para mí."
            a "Cincuenta y siete taxistas dijeron eso mismo."
            "Me lo dice sin reproche. Pero cuando aprieto el sobre para guardarlo, el pegamento seco cede y la solapa se abre sola, como si hubiera estado esperando."

    "Adentro hay una carta doblada en cuatro. Y dos boletos de bus."

    show cg pasajes with dissolve

    "{i}Estrella del Norte. Copiapó — La Serena. Sábado 9 de noviembre de 1968. Salida: 00:15.{/i}"
    "{i}Pasajero: I. Albornoz V.{/i}"
    "{i}Pasajero: T. Pizarro L.{/i}"
    "Lo leo una vez. Lo leo otra."
    "T. Pizarro L."
    "Tomás Pizarro Leiva."

    play sound latido
    with vpunch

    "Es el nombre de mi papá."

    hide cg pasajes with dissolve

    "No leo la carta. Esa sí que no es para mí."

    show arsenio neutral with dissolve

    a "Pizarro... ¿Usted es Pizarro?"

    "Asiento. No me sale la voz."
    "Don Arsenio se saca el gorro. Se queda un rato mirando el nicho, dándole vueltas al gorro entre las manos."

    a "Cincuenta y ocho años buscando el taxi correcto."
    a "Ella espera hasta que aclara, ¿sabe? Todos los años. Las velas de este pasaje no se apagan hasta que sale el sol."
    a "Si su papá está vivo, señor Pizarro, tráigalo. Antes del amanecer."

    stop music fadeout 3.0
    jump casa


## ----------------------------------------------------------------------------
##  CAPÍTULO 5 · Lo que mi papá nunca contó
## ----------------------------------------------------------------------------

label casa:
    scene bg casa_noche with fade
    stop ambiente fadeout 2.0
    play music tema_ines fadein 3.0

    "Las dos y media de la mañana. La luz de la casa de mi papá está prendida."
    "Claro que está prendida. Es ocho de noviembre. Él no duerme el ocho de noviembre."

    show tomas neutral with dissolve

    "Sigue en la silla, junto a la ventana. No se sorprende de verme."

    t "Rodo. ¿Qué pasó? ¿Chocaste?"

    menu:
        "Mostrarle la chaqueta.":
            "No digo nada. Le pongo la chaqueta roja en las rodillas."
            show tomas triste
            "Mi papá la mira. La toca. Pasa un dedo por la palomita de plata, despacio, como se toca la cara de alguien dormido para no despertarlo."
            t "La palomita de mi mamá..."
            t "¿De dónde sacaste esto? ¿Quién te dio esto?"

        "Contarle todo desde el principio.":
            "Me siento frente a él. Le cuento todo: la plaza, el reloj, la radio, el muro del cementerio. El nicho. El nombre."
            "Cuando digo «Inés», mi papá cierra los ojos."
            show tomas triste
            "Entonces le pongo la chaqueta en las rodillas."
            t "La palomita de mi mamá..."

    r "Papá. ¿Quién era Inés Albornoz?"

    "Se queda callado tanto rato que pienso que no va a contestar."
    "Después estira la mano hacia la repisa y pone derecha la foto que estuvo boca abajo toda mi vida."

    if not vio_foto:
        show cg foto with dissolve
        "Un muchacho flaco, sonriendo bajo los pimientos. Una chaqueta de lana con una palomita en la solapa."
        "Mi papá, a los veinte años."
        hide cg foto with dissolve

    t "Esa foto me la sacó ella. En la plaza. Con una cámara que le pidió prestada a su prima."

    scene cg recuerdo with fundido_muy_lento

    t "Íbamos a irnos juntos, Rodo. A La Serena. Yo tenía trabajo asegurado en una maestranza, y ella iba a estudiar para profesora."
    t "Su papá no me quería. Yo era hijo de pirquinero, y él tenía un almacén en la calle Atacama y una idea muy alta de su apellido."
    t "Compramos los pasajes con lo que juntamos todo el invierno. Se los di a ella pa' que los guardara, porque yo lo pierdo todo."
    t "Una semana antes hizo frío en la plaza, y le presté mi chaqueta. Le dije: me la devuelves arriba de la micro."
    t "El ocho de noviembre la esperé debajo del pimiento grande desde las once."
    t "A las doce y cuarto salió la micro. Yo la miré irse."
    t "Me quedé ahí hasta que aclaró."
    t "Al otro día supe que había muerto. Que el papá la iba a mandar a Tierra Amarilla, donde la tía. Que el taxi chocó en la salida."
    t "Se iba, Rodo. Se iba lejos de mí y no me dejó ni un recado."
    t "Me fui de Copiapó esa misma semana. Me fui al norte, a las minas. Conocí a tu mamá. Volví veinte años después, cuando ya no dolía tanto."
    t "Mentira. Volví cuando aprendí a que me doliera callado."

    scene bg casa_noche with fundido_lento
    show tomas triste

    "Le paso el sobre. Los pasajes. La carta."
    "Mi papá se pone los anteojos con las manos temblando. Desdobla la carta."

    show cg carta with dissolve

    nvl clear
    carta "Tomás:"
    carta "Te escribo esto por si los nervios no me dejan hablar en la micro."
    carta "Ya decidí. Me voy contigo, a La Serena o a donde sea."
    carta "Mi papá sospecha algo. Si esta noche me encierra, igual voy a encontrar la manera. Si llego tarde, espérame. Si no llego, no es porque no quiera: es porque no me dejan."
    carta "Te guardo los pasajes y tu chaqueta. Me queda grande, pero huele a ti, y con eso no tengo frío."
    carta "Cuando estemos lejos me la pides de vuelta, y yo te digo que sí a todo lo otro."
    carta "Tuya,\nInés."
    nvl clear

    hide cg carta with dissolve

    "Mi papá no llora como lloran los viejos en las películas. No hace ruido."
    "Se le caen las lágrimas y él se queda quieto, con la carta en las manos, como si recién ahora, cincuenta y ocho años después, la micro terminara de irse."

    t "No se iba."
    t "No se iba de mí, Rodo."

    r "Papá. Don Arsenio, el cuidador, dice que ella espera hasta que aclara."
    r "Todavía es de noche."

    "Mi papá dobla la carta y la guarda en el bolsillo de la camisa, sobre el corazón. Se levanta de la silla con una agilidad que no le veía hace años."

    show tomas neutral
    t "Pásame la chaqueta, hijo."

    stop music fadeout 3.0
    jump final_cementerio


## ----------------------------------------------------------------------------
##  CAPÍTULO 6 · Hasta que aclare
## ----------------------------------------------------------------------------

label final_cementerio:
    scene bg avenida_noche with fade
    play motor motor_taxi fadein 1.0
    play music noche fadein 3.0

    "Manejo por la Copayapu con mi papá al lado y la chaqueta roja en sus rodillas. Ninguno de los dos habla."
    "En el tablero, el reloj avanza normal. 04:41. 04:42."

    scene bg cementerio_reja with dissolve
    stop motor fadeout 2.0
    play ambiente viento fadein 2.0

    "Don Arsenio nos espera con la reja abierta."
    "Y a su lado, apoyado en el muro, con el gorro de lana entre las manos, está Don Lucho."

    show arsenio neutral at left
    show lucho triste at right
    with dissolve

    a "Lo llamé yo. Ya era hora."

    "Mi papá se detiene. Mira a Don Lucho mucho rato, como quien trata de leer un letrero borrado."

    show tomas neutral at center with dissolve

    t "...Lucho Carvajal. El del taxi negro de la plaza."
    l "Tomás."

    scene bg cementerio_pasaje with fundido_lento
    play music tension fadein 2.0
    show tomas triste at left
    show lucho triste at right
    with dissolve

    "Caminamos juntos hasta el pasaje Los Pimientos. Las velas de los frascos de mermelada están encendidas. Todas. Nadie las prendió."
    "El olor a nardos es tan fuerte que marea."

    l "Tengo que decirte algo, Tomás. Lo tengo atravesado desde hace cincuenta y ocho años."
    l "Esa noche el papá de la Inés me pagó por adelantado. Me dijo: «A Tierra Amarilla, y no pare aunque llore.»"
    l "Ella no lloró. Iba callada. Pero cuando llegamos a la salida del pueblo, me agarró del hombro."
    l "Me dijo: «Vuelva, por favor. Lléveme a la plaza. Me está esperando.»"
    l "Yo tenía veintidós años, Tomás. Me dio pena. Hice una vuelta en U ahí mismo, sin mirar."

    play sound latido
    l "El camión venía sin luces."
    l "Yo salí con un vidrio en la cara. Ella... no."
    l "Nunca le conté a nadie que se estaba devolviendo. Me dio miedo. Me dio vergüenza. Dejé que todos creyeran que iba camino a donde la tía."
    l "Al año siguiente, el ocho de noviembre, la subí en la plaza. Con tu chaqueta. Y me dio esta misma dirección."
    l "La traje aquí. Y nunca tuve el valor de ir a buscarte."

    "Don Lucho llora con la boca apretada. Ochenta años, y llora como un niño castigado."

    menu:
        "Encararlo.":
            r "¿Cincuenta y ocho años, Don Lucho? ¿Cincuenta y ocho años dejando que mi papá creyera que ella lo había dejado?"
            "Don Lucho no se defiende. Asiente, nomás."
            t "Rodo. Basta."

        "Esperar a que hable mi papá.":
            "Me muerdo la lengua. Esto no es mío. Es de ellos dos, y de ella."

    "Mi papá se acerca a Don Lucho. Le pone una mano en el hombro, en el mismo hombro donde ella lo agarró esa noche."

    t "Tú la estabas trayendo donde mí, Lucho."
    t "Eso es lo único que yo necesitaba saber. Lo único que me importa."
    t "Gracias por darte la vuelta."

    "Don Lucho se tapa la cara con el gorro."

    hide lucho with dissolve

    "Entonces el viento se detiene."

    stop ambiente fadeout 3.0
    stop music fadeout 3.0

    "Las velas se quedan quietas. El olor a nardos se vuelve tibio."
    "Al final del pasaje, junto al nicho dos mil trescientos cuarenta y siete, donde antes hubo un pimiento, hay alguien."

    show ines sin at fantasma_aparece(0.7)
    play music tema_ines fadein 4.0

    "Vestido claro. Pelo oscuro. Sin chaqueta, con las manos juntas contra el pecho, como si tuviera frío."
    "Mi papá deja de ser un viejo de setenta y ocho años. No sé explicarlo mejor. Se para derecho. Respira."

    t "Inés."
    p "Llegué tarde, Tomás."
    p "Perdóname. Me costó tanto encontrar el camino."
    t "No, mi niña. Llegaste. Llegaste."

    "Mi papá camina hacia ella con la chaqueta roja abierta entre las manos, como quien lleva una frazada a alguien que se quedó dormido afuera."
    "Se la pone sobre los hombros. Le queda enorme. Las mangas le tapan las manos."

    show ines sonrisa at fantasma(0.7) with dissolve

    t "Te la debía. Te queda grande."
    p "Me queda perfecta."
    p "Te dije que te iba a decir que sí a todo lo otro."
    t "Ya sé. Ya leí."

    "Ella se ríe. La misma risa del taxi. Ya no me da miedo."
    "Después me mira a mí."

    menu:
        "«Él siempre la esperó.»":
            $ palabras = "espera"
            r "Él siempre la esperó, Inés. Todas las noches de noviembre. Yo no sabía qué esperaba, pero esperaba."
            p "Yo sé. Lo veía desde la plaza."

        "«Gracias por elegir mi taxi.»":
            $ palabras = "taxi"
            r "Gracias por elegir mi taxi."
            p "No lo elegí. Lo reconocí. Usted tiene las manos de él."

        "No decir nada.":
            $ palabras = "silencio"
            "No digo nada. Hay cosas que se arruinan con palabras."
            p "Es igual de callado que él. Qué bueno."

    p "Ya le pagué, ¿cierto? No quiero quedar debiendo."
    r "Me pagó de sobra."

    "Por encima del muro, los cerros empiezan a ponerse grises. Después, rosados."

    scene bg cementerio_alba
    show ines sonrisa at desvanecer_lento
    with fundido_muy_lento
    play music amanecer fadein 4.0

    "Amanece en Copiapó."
    "La luz entra en el pasaje Los Pimientos y pasa a través de ella como pasa a través de un vidrio limpio."
    "Lo último que veo es el rojo de la chaqueta. Después, nada. Solo la luz."

    hide ines

    "Las velas se apagan todas al mismo tiempo, como si alguien las hubiera soplado de una sola vez."
    "En el borde del nicho, donde ella estaba, queda brillando algo chiquito."
    "La palomita de plata."
    "Mi papá la recoge. Se la prende en la camisa, sobre la carta, sobre el corazón."

    show tomas neutral at center with dissolve

    t "Vámonos a la casa, Rodo. Tengo sueño."

    "Es la primera vez en mi vida que se lo escucho decir un nueve de noviembre."

    stop music fadeout 4.0
    jump epilogo


## ----------------------------------------------------------------------------
##  EPÍLOGO · Un año después
## ----------------------------------------------------------------------------

label epilogo:
    scene negro with fundido_lento
    centered "Un año después." with dissolve

    scene bg plaza_noche with fundido_lento
    play music amanecer fadein 3.0
    play motor motor_taxi fadein 2.0

    "Ocho de noviembre. Once y cuarenta de la noche."
    "Estoy estacionado frente a la Plaza Prat, junto al pimiento grande."
    "Mi papá murió en julio, en pleno invierno, durmiendo. Tranquilo. Tenía la palomita de plata prendida en la camisa del pijama; nunca se la sacó."
    "Lo enterramos en el cementerio de la avenida La Paz. En la parte vieja."
    "Don Arsenio me ayudó con los papeles. El nicho dos mil trescientos cuarenta y ocho estaba desocupado."
    "Me dijo que siempre lo había estado. Que nadie lo quiso nunca, como si estuviera reservado."

    show cg nichos_final with dissolve

    "Ahora en el pasaje Los Pimientos hay dos placas, una al lado de la otra. Les llevo nardos los domingos."

    hide cg nichos_final with dissolve

    "Don Lucho volvió a manejar. Un solo día al año. Esta noche anda dando vueltas por el centro con su taxi viejo y su termo, porque dice que le debe un ocho de noviembre a la ciudad."
    "En el cuaderno de Don Arsenio, la última línea la escribí yo:"
    "{i}8 de noviembre de 2026. R. Pizarro. Entregada.{/i}"
    "El billete de diez escudos lo tengo guardado en el parasol del taxi. Para acordarme de que hay deudas que sí se pagan."

    scene bg taxi_frente with dissolve

    "El reloj del tablero marca las 23:46."

    play sound tic
    "23:47."
    "Miro la plaza. Miro bajo el pimiento grande, donde la luz del farol no alcanza."
    "No hay nadie."

    play sound tic
    "23:48."
    "Prendo la radio. Pasan una canción de ahora, con un locutor de ahora, que da la hora de ahora."

    if palabras == "espera":
        "Ya no espero a nadie en las noches de noviembre. Pero cuando paso por la plaza, bajo la velocidad. Por costumbre. Por cariño."
    elif palabras == "taxi":
        "A veces, cuando manejo de noche, me quedo mirando mis manos en el volante. Son las manos de él."
    else:
        "Hay cosas que se arruinan con palabras. Por eso esta historia la cuento poco, y solo a taxistas."

    "No hay nadie esperando debajo de los pimientos."
    "Por fin, nadie."

    stop motor fadeout 3.0
    stop music fadeout 4.0
    scene negro with fundido_muy_lento
    centered "{size=+20}FIN{/size}\n\n{size=-4}La chaqueta · Una leyenda de Copiapó{/size}" with dissolve

    return
