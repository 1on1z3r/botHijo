import time, sys
import pyjokes
import pymysql
from urllib import request
from twitchAPI.twitch import Twitch


from twitchio import Channel, User
from twitchio.ext import commands

message_count = {}
canales = ['#1on1zer', '#patrii19']
exclusiones_usuarios = ['nightbot',
                        'streamelements',
                        "comanderroot",
                        'testigo19']

# msyql
server = 'PMYSQL143.dns-servicio.com'
usuario = 'daniel'
clave = '*ek0vA979'
db = '8267796_dani'
datosConexion = {"host": server, "port": 3306, "user":usuario,"passwd":clave,"db":db}

def getFechaHora():
    return time.strftime("%Y/%m/%d %H:%M:%S")

def getFecha():
    return time.strftime("%d/%m/%y")

def getHora():
    return time.strftime("%H:%M:%S")

def cuentaFollowers(usuario):
    # funcion que mira los followers de los usuarios
   
    print("Seguidores de "+usuario+": "+str(len(respuestajson['follows'])))
def hasRegistro(usuario,canal):
    if usuario not in exclusiones_usuarios:
        cuentaFollowers(usuario)
        canal.replace("#","")
        # devuelve true si existe el registro
        print("Entra en hasRegistro")
        conexion = pymysql.connect(**datosConexion)
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM mensajes WHERE MEN_Usuario = '"+usuario+"' AND MEN_Fecha = DATE_FORMAT(NOW(), '%Y-%m-%d') AND MEN_Canal='"+canal+"'"
        print("[hasRegistro] "+query)
        cursor.execute(query)
        print(str(cursor.rowcount))
        if cursor.rowcount > 0:
            print("Existe el registro para el usuario "+usuario+" en "+canal)
            return True
        else:
            print("No existe el registro para el usuario "+usuario+" en " +canal)
            creaRegistro(usuario,canal)
            return False

        cursor.close()
        conexion.close()

def incMensaje(usuario,canal):
    if usuario not in exclusiones_usuarios:
        canal.replace("#","")
        query = "UPDATE mensajes SET MEN_Contador = MEN_Contador + 1 WHERE MEN_Usuario = '"+usuario+"' AND MEN_Fecha = DATE_FORMAT(NOW(), '%Y-%m-%d') AND MEN_Canal='"+canal+"'"
        hasRegistro(usuario, canal)
        ejecutaSQL(query)
        print("[QUERY] "+query)

def ejecutaSQL(query = ""):
    if query != "":
        conexion = pymysql.connect(**datosConexion)
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        print("[QUERY] "+query)
        cursor.execute(query)
        cursor.close()
        conexion.close()

def creaRegistro(usuario,canal):
    consulta="INSERT INTO mensajes(MEN_Fecha,MEN_Usuario,MEN_Canal,BOT_ID, MEN_Contador) VALUES(now(),'"+usuario+"','"+canal+"',1,0)"
    ejecutaSQL(consulta)
def toLog(mensaje):
    if mensaje != '':
        query="INSERT INTO logs(LOG_Mensaje, BOT_Id, LOG_FechaHora) VALUES(\'"+mensaje+"\',1,\'"+getFechaHora()+"\')"
        print("[QUERY] "+query)
        ejecutaSQL(query)
        print("[LOG] "+mensaje)

msj = "Empieza el registro [BOT 1]"
toLog(msj)


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token='oauth:e26i0khkj7unwfrujjs60ke0xagtfr', prefix='!', initial_channels=canales)

    async def event_join(self, channel: Channel, user: User):
        msg = '[EVENTO ENTRADA] ' + user.name + ' Entra en #'+channel.name.lower()
        print(msg)
        toLog(msg)
        hasRegistro(user.name.lower(),channel.name.lower())

    async def event_part(self, user):
        msg = '[EVENTO SALIDA] ' + user.name + ' Sale de #' + channel.name.lower()
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
        incMensaje(message.author.name.lower(),message.channel.name)

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

    # Comando !ticketganador
    @commands.command()
    async def ticketganador(self, ctx: commands.Context):
        await ctx.send(f'/me le pone a {ctx.author.name.lower()} 2 velas negras por gracioso TwitchConHYPE ')

    # Comando !vashu
    @commands.command()
    async def vashu(self, ctx: commands.Context):
        await ctx.send(f'/me mira lascivamente a @vashu_stomp CurseLit. Tio bueno, guapo nosequeee...')

    # Comando !chiste
    @commands.command()
    async def chiste(self,ctx:commands.Context):
        chiste = pyjokes.get_joke(language='es', category='neutral')
        await ctx.send(f"/me "+ chiste)

    # Comando !aDormir
    @commands.command()
    async def aDormir(self, ctx: commands.Context):
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
            print(usuario + " : " +str((message_count[usuario])))
            total = total + message_count[usuario]

        await ctx.send(f'/me Se han escrito ' + str(total) + ' mensajes en el chat.\n')
        f = open('datalog.txt', 'a')
        f.write('Peticion de recuento [' + getFechaHora() + ']\n')
        f.write('Mensajes totales: ' + str(total) + '\n')
        f.close()

bot = Bot()
bot.run()
