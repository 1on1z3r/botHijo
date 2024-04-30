import time, sys
import datetime
import pyjokes
import pymysql
import random
from vars import *
from urllib import request
import openai
# from twitchAPI.twitch import Twitch

from twitchio import Channel, User
from twitchio.ext import commands



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
        if(autor == "1on1zer"):
            await ctx.send(f'/me Encendiendo motores beeep beeep 100101001 TwitchConHYPE')

    # Comando !ranking
    @commands.command()
    async def ranking(self, ctx: commands.Context):
        autor = ctx.author.name.lower()
        if(autor == "1on1zer" or autor == "patrii19" or autor == "streamelements"):
            respuesta = getRankingDiario(ctx.channel.name.lower())
            await ctx.send(f'/me '+respuesta)

    # Comando !ranking
    @commands.command()
    async def rankingglobal(self, ctx: commands.Context):
        autor = ctx.author.name.lower()
        if (autor == "1on1zer" or autor == "patrii19"):
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

