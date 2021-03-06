# -*- coding: utf-8 -*-
'''
*******************Developed by********************************
    
Alfredo Albélis Batista Filho - https://github.com/AlfredoFilho
Pedro Henrique Bernini Silva - https://github.com/PedroBernini

***************************************************************
'''

import Cats.Calcular as Calcular
import GifMaker.GifMaker as GifMaker
import os
import codecs

tabuleiro = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10),
             (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10),
             (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10),
             (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10),
             (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10),
             (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10),
             (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10),
             (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10),
             (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10),
             (9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10),
             (10,0), (10,1), (10,2), (10,3), (10,4), (10,5), (10,6), (10,7), (10,8), (10,9), (10,10)]

dark_green = "#4a8e52"
light_green = "#61b76b"

dir = 'Gifs/Gif_aStar.gif'

class no:
    def __init__(self, coordenada, total_F, distanciaComeco_G, distanciaAteFinal_H, pai):
        self.coordenada = coordenada
        self.total_F = total_F
        self.distanciaComeco_G = distanciaComeco_G
        self.distanciaAteFinal_H = distanciaAteFinal_H
        self.pai = pai

def expandir(estadoEscolhido, listaAberta, listaFechada, images, bloqueados, estadoFinal, ArquivoLog):
    # lista com as nos inicias em volta do pai
    listaExpansaoSuja = []
    
    #Lista expansao limpa (sem bloqueados e dentro do tabuleiro)
    listaExpansao = []
    
    if estadoEscolhido[0] % 2 != 0: #Se a linha do gato for par
        listaExpansaoSuja = [(estadoEscolhido[0], estadoEscolhido[1] + 1),      #Leste
                             (estadoEscolhido[0] + 1, estadoEscolhido[1] + 1),  #Sudeste
                             (estadoEscolhido[0] + 1, estadoEscolhido[1]),      #Sudoeste
                             (estadoEscolhido[0], estadoEscolhido[1] - 1),      #Oeste
                             (estadoEscolhido[0] - 1, estadoEscolhido[1]),      #Noroeste
                             (estadoEscolhido[0] - 1, estadoEscolhido[1] + 1)]  #Nordeste
    else:
        listaExpansaoSuja = [(estadoEscolhido[0], estadoEscolhido[1] + 1),      #Leste
                             (estadoEscolhido[0] + 1, estadoEscolhido[1]),      #Sudeste
                             (estadoEscolhido[0] + 1, estadoEscolhido[1] - 1),  #Sudoeste
                             (estadoEscolhido[0], estadoEscolhido[1] - 1),      #Oeste
                             (estadoEscolhido[0] - 1, estadoEscolhido[1] - 1),  #Noroeste
                             (estadoEscolhido[0] - 1, estadoEscolhido[1])]      #Nordeste
    
    
    #Retirar da lista suja bloqueados e fora do tabuleiro
    for coordenada in listaExpansaoSuja:
        valido = True
        if coordenada not in bloqueados and coordenada in tabuleiro:
            for no in listaFechada:
                if coordenada == no.coordenada:
                    valido = False
            if valido == True:
                for no in listaAberta:
                    if coordenada == no.coordenada:
                        valido = False
            if valido == True:
                if(coordenada != estadoFinal):
                    images.append(GifMaker.fill_dot(coordenada, "gray", images))
                listaExpansao.append(coordenada)
    
    return listaExpansao


def preencherNo(listaExpansao, estadoInicial, estadoFinal, estadoEscolhido, listaAberta, listaFechada, ArquivoLog):
    
    #print("\nEstado escolhido:", estadoEscolhido)
    ArquivoLog.write("Estado escolhido: " + str(estadoEscolhido))

    #print("Nós expandidos:")
    ArquivoLog.write("\n\n    Nós expandidos:")

    if(len(listaExpansao) == 0):
        ArquivoLog.write('\n\n        SEM EXPANSÕES POSSÍVEIS ou ENCONTROU O FINAL\n')
    
    else:
        for coordenada in listaExpansao:
            distanciaComeco_G = Calcular.G(estadoInicial, estadoEscolhido, listaFechada, listaAberta) + 1
            distanciaAteFinal_H = Calcular.H(coordenada, estadoFinal)
            total_F = distanciaComeco_G + distanciaAteFinal_H
            
            #print("    Coordenada:", coordenada, "F = ", total_F, "G = ",distanciaComeco_G, "H = ", distanciaAteFinal_H)
            ArquivoLog.write("\n        Coordenada: " + str(coordenada) + "\n            F = " + str(total_F) + 
            "\n            G = " + str(distanciaComeco_G) + "\n            H = " + str(distanciaAteFinal_H) + '\n')
            
            listaAberta.append(no(coordenada, total_F, distanciaComeco_G, distanciaAteFinal_H, estadoEscolhido))
    
    #print("\nLista aberta:")
    ArquivoLog.write("\nLista aberta:")
    
    for classe in listaAberta:
        #print("    ", classe.coordenada)
        ArquivoLog.write("  " + str(classe.coordenada))

    #print("\nLista fechada:")
    ArquivoLog.write("\nLista fechada:")

    for classe in listaFechada:
        #print("    ", classe.coordenada)
        ArquivoLog.write("  " + str(classe.coordenada))

    #print("----------------------")
    ArquivoLog.write("\n\n----------------------\n\n")
#    os.system("pause")
    return listaAberta


def ordenarNoPorHeuristica(listaAberta):

    elementos = len(listaAberta) - 1
    ordenado = False
    while not ordenado:
        ordenado = True
        for i in range(elementos):
            if listaAberta[i].total_F > listaAberta[i + 1].total_F:
                listaAberta[i], listaAberta[i + 1] = listaAberta[i + 1], listaAberta[i]
                ordenado = False
    return listaAberta

def aStar(estadoInicial, estadoFinal, bloqueados):

    fullNameFile = 'Logs/Log_aStar.txt'
    ArquivoLog = codecs.open(fullNameFile, "w", encoding="utf8")
    ArquivoLog.write("------------- Log de execuções aStar -------------\n\n")

    estadoEscolhido = estadoInicial
    images = []
    
    #Fazer imagem inicial do gif - cat, bloqueios e estadoFinal
    images.append(GifMaker.compute_initial_image(estadoInicial, bloqueados, estadoFinal, images))
    
    listaFechada = [] #lista visitados
    listaAberta = []  #lista não visitados

    #estrutura para a coordenada inicial
    distanciaComeco_G = 0
    distanciaAteFinal_H = Calcular.H(estadoEscolhido, estadoFinal)
    total_F = distanciaComeco_G + distanciaAteFinal_H
    listaAberta.append(no(estadoEscolhido, total_F, distanciaComeco_G, distanciaAteFinal_H, None))

#-----------------------------------------------------------------------
    while estadoEscolhido != estadoFinal:

        listaExpansao = expandir(estadoEscolhido, listaAberta, listaFechada, images, bloqueados, estadoFinal, ArquivoLog)
        listaAberta = preencherNo(listaExpansao, estadoInicial, estadoFinal, estadoEscolhido, listaAberta, listaFechada, ArquivoLog)
        
        listaFechada.append(listaAberta[0])
        listaAberta.pop(0)
        
        listaAberta = ordenarNoPorHeuristica(listaAberta)
        
        #Escolher próximo nó
        if len(listaAberta) == 0:
            
            #print("Sem saida")
            ArquivoLog.write("\nSem saida")
            ArquivoLog.close()
            images[0].save(dir,
                   save_all=True,
                   append_images=images[1:],
                   duration=200,
                   loop=0)
            os.remove("GifMaker/ImagemTemp.png")
            os.remove("GifMaker/ImagemTemp2.png")
            return 0
        else:
            estadoEscolhido = listaAberta[0].coordenada
        
        images.append(GifMaker.fill_dot(estadoEscolhido, "black" , images))
#-----------------------------------------------------------------------
    
    #Adicionar estadoFinal na lista fechada
    cont = 0
    for struct in listaAberta:
        if struct.coordenada == estadoFinal:
            listaFechada.append(struct)
            listaAberta.pop(cont)
            break
        cont = cont + 1
    
    listaComMelhorCaminho = []
    listaComMelhorCaminho.append(estadoFinal)
    
    #Fazer caminho inverso pela lista fechada até a coordenada inicial(cat)
    aux = True
    while aux:
        for struct in listaFechada:
            if struct.coordenada == estadoEscolhido:
                estadoEscolhido = struct.pai
                listaComMelhorCaminho.append(estadoEscolhido)
                if estadoEscolhido == estadoInicial:
                    aux = False
                break
    
    #Fazer parte do gif que volta da estadoFinal até o inicio
    for coordenada in listaComMelhorCaminho:
        images.append(GifMaker.fill_dot(coordenada, dark_green, images))
    
    #inverter a lista
    listaComMelhorCaminho.reverse()

    #Fazer parte do gif que anda até o fim
    for coordenada in listaComMelhorCaminho:
        images.append(GifMaker.fill_dot(coordenada, light_green, images))
    
    #salvar gif
    images[0].save(dir,
                       save_all=True,
                       append_images=images[1:],
                       duration=200,
                       loop=0)
    
    #print("\nGif Gerado")
    #print("\nInicio", estadoInicial)
    ArquivoLog.write("Inicio: " + str(estadoInicial))
    ArquivoLog.write("\nFim: " + str(estadoFinal))
    #print("\nBloqueios", bloqueados)
    ArquivoLog.write("\nBloqueios: " + str(bloqueados))
    #print("\nQuantidade de nós visitados:", len(listaFechada)-1)
    ArquivoLog.write("\nQuantidade de nós visitados: " + str(len(listaFechada)-1))
    #print("\nCaminho encontrado: ", listaComMelhorCaminho)
    ArquivoLog.write("\nCaminho encontrado: " + str(listaComMelhorCaminho))
    ArquivoLog.close()
    
    os.remove("GifMaker/ImagemTemp.png")
    os.remove("GifMaker/ImagemTemp2.png")
