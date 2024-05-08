import random
import sys
import time

import pyjokes
import pymysql
from twitchio import Channel, User
from twitchio.ext import commands

from vars import *


# import openai
# from twitchAPI.twitch import Twitch

def get_chiste_profesor():
    numero = random.randint(0, len(chistes_profesores) - 1)
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

def getPesca(nick):
    hora = time.strftime("%H")
    resultado = ''
    # logica aplastante de limitador por hora
    # pesca_usuarios[nick][hora] = pesca_usuarios[nick][hora] + 1
    peso = random.randint(0, 30)
    decimal = random.randint(0, 99)
    tipo = random.randint(1, 10)
    if pesca_usuarios[nick][hora] <= 3:
        if tipo in [3, 8]:
            longitud = len(peces_excepcionales)-1
            pez = peces_excepcionales[random.randint(0, longitud)]
            resultado = "@"+nick+" Squid1 Squid2 Squid3 Squid2 Squid4 has pescado el pez excepcional "+ str(pez) + " de "+str(peso)+"."+str(decimal)+"kg! Enhorabuena! "
        elif tipo in [1, 2, 4, 9]:
            longitud = len(peces_leyenda)-1
            pez = peces_leyenda[random.randint(0, longitud)]
            resultado = "@"+nick+" SabaPing Has pescado un pez de leyenda " + pez + " de "+str(peso)+"."+str(decimal)+"kg! SabaPing"
        else:
            resultado = "@"+nick+" BibleThump Vaya, has pescado una miñoca de "+str(peso)+"."+str(decimal)+"kg! Más suerte la próxima vez BibleThump"

    # pesca_usuarios[nick][hora] = pesca_usuarios[nick][hora] + 1
    return resultado


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
    query = "SELECT MEN_Usuario, MEN_Contador FROM mensajes WHERE MEN_Canal = '" + canal + "' AND MEN_Fecha = '" + fecha + "' ORDER BY MEN_Contador DESC LIMIT 5 "
    cursor.execute(query)
    result = cursor.fetchall()
    contador = 1
    for linea in result:
        texto = texto + str(contador) + ". " + linea['MEN_Usuario'] + " (" + str(linea['MEN_Contador']) + ") "
        contador = contador + 1
    return texto


def getRankingGlobal(canal):
    texto = "DinoDance Mostrando ranking de mensajes global: "
    fecha = getFechaMySql()
    # canal = "patrii19"
    conexion = pymysql.connect(**datosConexion)
    cursor = conexion.cursor(pymysql.cursors.DictCursor)
    query = "SELECT MEN_Usuario, MEN_Contador FROM mensajes WHERE MEN_Canal = '" + canal + "' GROUP BY MEN_Usuario ORDER BY MEN_Contador DESC LIMIT 5 "
    cursor.execute(query)
    result = cursor.fetchall()
    contador = 1
    for linea in result:
        texto = texto + str(contador) + ". " + linea['MEN_Usuario'] + " (" + str(linea['MEN_Contador']) + ") "
        contador = contador + 1
    return texto


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token='oauth:e26i0khkj7unwfrujjs60ke0xagtfr', prefix='!', initial_channels=canales)

    async def event_join(self, channel: Channel, user: User):
        msg = '[EVENTO ENTRADA] ' + user.name + ' Entra en #' + channel.name.lower()
        print(msg)
        toLog(msg)
        hasRegistro(user.name.lower(), channel.name.lower())

    async def event_part(self, user):
        msg = '[EVENTO SALIDA] ' + user.name + ' Sale de #' + user.channel.name.lower()
        print(msg)
        toLog(msg)

    async def event_ready(self):
        total_mensajes = 0
        print(f'Logueado con el nick | {self.nick}')
        print(f'El id de usuario es | {self.user_id}')
        totalMensajes = 0

    async def event_message(self, message):
        if message.echo:
            return
        print(message.content + ' de ' + message.author.name + ' en #' + message.channel.name)
        author_name = message.author.name.lower()
        message_count[author_name] = message_count.get(author_name, 0) + 1
        incMensaje(message.author.name.lower(), message.channel.name)

        await self.handle_commands(message)

    # Comando saludo
    @commands.command()
    async def saludo(self, ctx: commands.Context):
        await ctx.send(f'Hola {ctx.author.name}!')

    # Comando mensajes
    @commands.command()
    async def mensajes(self, ctx: commands.Context):
        await ctx.send(f'{ctx.author.name.lower()} Llevas escritos ' + str(
            message_count.get(ctx.author.name.lower())) + ' mensajes.')

    # Comando !activate
    @commands.command()
    async def activate(self, ctx: commands.Context):
        autor = ctx.author.name.lower()
        if autor == "1on1zer":
            await ctx.send(f'/me Encendiendo motores beeep beeep 100101001 TwitchConHYPE')

    # Comando !ranking
    @commands.command()
    async def ranking(self, ctx: commands.Context):
        autor = ctx.author.name.lower()
        if autor == "1on1zer" or autor == "patrii19" or autor == "streamelements":
            respuesta = getRankingDiario(ctx.channel.name.lower())
            await ctx.send(f'/me ' + respuesta)

    #EXPERIMENTAL PESCAR -------------------------------------------------------------------------------
    # Comando !pescar
    @commands.command()
    async def pescar(self, ctx: commands.Context):
        respuesta = getPesca(ctx.author.name.lower())
        # logica
        if respuesta != '':
            await ctx.send(f'/me ' + respuesta)

    # EXPERIMENTAL PESCAR -------------------------------------------------------------------------------

    # Comando !ranking
    @commands.command()
    async def rankingglobal(self, ctx: commands.Context):
        autor = ctx.author.name.lower()
        if autor == "1on1zer" or autor == "patrii19":
            respuesta = getRankingGlobal(ctx.channel.name.lower())
            await ctx.send(f'/me ' + respuesta)

    # Comando !activate
    @commands.command()
    async def apagate(self, ctx: commands.Context):
        autor = ctx.author.name.lower()
        await ctx.send(f'/me Apagando mostores beeep beeep 100101001 TwitchConHYPE')
        encendido = False

    # Comando !ticketganador
    @commands.command()
    async def ticketganador(self, ctx: commands.Context):
        await ctx.send(f'/me le pone a {ctx.author.name.lower()} 2 velas negras por gracios@ TwitchConHYPE ')

    # Comando !vashu
    @commands.command()
    async def vashu(self, ctx: commands.Context):
        await ctx.send(f'/me mira lascivamente a @vashu_stomp CurseLit. Tio bueno, guapo nosequeee...')

    # Comando !chiste
    @commands.command()
    async def chiste(self, ctx: commands.Context):
        autor = ctx.author.name.lower()
        if autor == "1on1zer":
            chiste = pyjokes.get_joke(language='es', category='neutral')
            await ctx.send(f"/me " + chiste)
        elif autor == "sarahoria__":
            chiste = get_chiste_profesor()
            await ctx.send(f"/me " + chiste)

    # Comando !aDormir
    @commands.command()
    async def adormir(self, ctx: commands.Context):
        if ctx.author.name.lower() == 'patrii19' or ctx.author.name.lower() == '1on1zer':
            total = 0
            await ctx.send(f'/Buenas noches a todes <3')
            for usuario in message_count:
                print(usuario)
                total = total + message_count[usuario]

            f = open('datalog.txt', 'a')
            f.write('Peticion de desconexion [' + getFechaHora() + ']\n')
            f.write('Mensajes totales: ' + str(total) + '\n')
            f.close()
            sys.exit()

    # Comando totalMensajes
    @commands.command()
    async def totalMensajes(self, ctx: commands.Context):
        total = 0
        for usuario in message_count:
            print(usuario + " : " + str((message_count[usuario])))
            total = total + message_count[usuario]

        await ctx.send(f'/me Se han escrito ' + str(total) + ' mensajes en el chat.\n')
        f = open('datalog.txt', 'a')
        f.write('Peticion de recuento [' + getFechaHora() + ']\n')
        f.write('Mensajes totales: ' + str(total) + '\n')
        f.close()


bot = Bot()
bot.run()
