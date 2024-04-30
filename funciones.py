def get_chiste_profesor():
    numero = random.randint(0, len(chistes_profesores)-1)
    print(numero)
    return chistes_profesores[numero]
def getFechaHora():
    return time.strftime("%Y/%m/%d %H:%M:%S")


def getFecha():
    return time.strftime("%d/%m/%y")

def getFechaMySql():
    return time.strftime("%Y/%m/%d")


def getHora():
    return time.strftime("%H:%M:%S")


# def cuentaFollowers(usuario):
    # funcion que mira los followers de los usuarios

    #print("Seguidores de " + usuario + ": " + str(len(respuestajson['follows'])))



def hasRegistro(usuario, canal):
    if usuario not in exclusiones_usuarios:
        # cuentaFollowers(usuario)
        canal.replace("#", "")
        # devuelve true si existe el registro
        conexion = pymysql.connect(**datosConexion)
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM mensajes WHERE MEN_Usuario = '" + usuario + "' AND MEN_Fecha = DATE_FORMAT(NOW(), '%Y-%m-%d') AND MEN_Canal='" + canal + "'"
        print("[hasRegistro] " + query)
        cursor.execute(query)
        print(str(cursor.rowcount))
        if cursor.rowcount > 0:
            print("Existe el registro para el usuario " + usuario + " en " + canal)
            return True
        else:
            print("No existe el registro para el usuario " + usuario + " en " + canal)
            creaRegistro(usuario, canal)
            return False

        cursor.close()
        conexion.close()


def incMensaje(usuario, canal):
    if usuario not in exclusiones_usuarios:
        canal.replace("#", "")
        query = "UPDATE mensajes SET MEN_Contador = MEN_Contador + 1 WHERE MEN_Usuario = '" + usuario + "' AND MEN_Fecha = DATE_FORMAT(NOW(), '%Y-%m-%d') AND MEN_Canal='" + canal + "'"
        hasRegistro(usuario, canal)
        ejecutaSQL(query)
        print("[QUERY] " + query)


def ejecutaSQL(query=""):
    if query != "":
        conexion = pymysql.connect(**datosConexion)
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        print("[QUERY] " + query)
        cursor.execute(query)
        cursor.close()
        conexion.close()


def creaRegistro(usuario, canal):
    consulta = "INSERT INTO mensajes(MEN_Fecha,MEN_Usuario,MEN_Canal,BOT_ID, MEN_Contador) VALUES(now(),'" + usuario + "','" + canal + "',1,0)"
    ejecutaSQL(consulta)


def toLog(mensaje):
    if mensaje != '':
        query = "INSERT INTO logs(LOG_Mensaje, BOT_Id, LOG_FechaHora) VALUES(\'" + mensaje + "\',1,\'" + getFechaHora() + "\')"
        print("[QUERY] " + query)
        ejecutaSQL(query)
        print("[LOG] " + mensaje)


msj = "Empieza el registro [BOT 1]"
toLog(msj)

def getRankingDiario(canal):
    texto = "DinoDance Mostrando ranking de mensajes diario: "
    fecha = getFechaMySql()
    # canal = "patrii19"
    conexion = pymysql.connect(**datosConexion)
    cursor = conexion.cursor(pymysql.cursors.DictCursor)
    query = "SELECT MEN_Usuario, MEN_Contador FROM mensajes WHERE MEN_Canal = '"+canal+"' AND MEN_Fecha = '"+fecha+"' ORDER BY MEN_Contador DESC LIMIT 5 "
    cursor.execute(query)
    result = cursor.fetchall()
    contador = 1
    for linea in result:
        texto = texto + str(contador)+". "+linea['MEN_Usuario']+" ("+str(linea['MEN_Contador'])+") "
        contador = contador + 1
    return texto

def getRankingGlobal(canal):
    texto = "DinoDance Mostrando ranking de mensajes global: "
    fecha = getFechaMySql()
    # canal = "patrii19"
    conexion = pymysql.connect(**datosConexion)
    cursor = conexion.cursor(pymysql.cursors.DictCursor)
    query = "SELECT MEN_Usuario, MEN_Contador FROM mensajes WHERE MEN_Canal = '"+canal+"' GROUP BY MEN_Usuario ORDER BY MEN_Contador DESC LIMIT 5 "
    cursor.execute(query)
    result = cursor.fetchall()
    contador = 1
    for linea in result:
        texto = texto + str(contador)+". "+linea['MEN_Usuario']+" ("+str(linea['MEN_Contador'])+") "
        contador = contador + 1
    return texto
