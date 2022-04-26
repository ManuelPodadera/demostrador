import requests
import json
import ast
import pandas as pd
import streamlit as st

from reglas import dame_reglas
from content import recomendacion_content_based
from collaborative import resultado_colaborativo
from hibrido import recomendacion_hibrida


st.set_page_config(page_title="Sistema de Recomendación",page_icon="R",layout="wide")


titulo_pagina = st.container()
populares_venidas = st.container()
populares_valoradas = st.container()
regla_de_asociacion = st.container()
content_based = st.container()
colaborative = st.container()
hibrido = st.container()


########## diccionario de items - url #######
df = pd.read_csv("Items.csv",header=0)
dict_urls = {}
for ind in df.index:
    dict_urls[df["asin"][ind]] = df["imageURLHighRes"][ind]
#############################################

######### diccionario de usuario - nombre #####
df = pd.read_csv("user_name_group.csv",header=0)
dict_user_name = {}
dict_user_tipo = {}
for ind in df.index:
    dict_user_name[df["reviewerID"][ind]] = df["reviewerName"][ind]
    dict_user_tipo[df["reviewerID"][ind]] = df["grupo"][ind]
################################################



asociados = ("B00005R8BL","B000IOE9Y6","B000BW56WO","B00005N7SG","B00005N7PN","B000ILY9LW","B00007AWXX","B001LF4EVO","B01HI8V1I6")

content_lista_items = ("B01HI8V1I6","B000NDESM0","B000NJBIRW","B000NJM34O","B000NY15YI","B000O1PKOG","B000OONSVU")

usuarios = ("A3GHUXTBNEA9PI","A15INOMS30BOUT","A1SP8HCJ1MCE89","A2P1CE9CC6BRVF","A1XUVLLZB9JBTE","A3774MBQJ66HJS","A2CVQ25SHQFVX9")


dict_regla = dame_reglas()




with titulo_pagina:
    st.title("Trabajo Fin de Máster")
    st.title("Diseño, desarrollo y despliegue de un Sistema de Recomendación para E-Commerce.")
    st.subheader("Master Big Data & Business Analytics 20-21")
    st.subheader("Manuel Podadera Valenzuela")

    st.markdown("""---""")

with populares_venidas:
    st.header("Popularity Model: Más Vendido")
    agree = st.checkbox('Ver más VENDIDAS')
    if agree:
        mas_vendidos = requests.get("https://manuelpodaderatfm555.ue.r.appspot.com/listado_mas_vendidos")
        test_string = json.loads(mas_vendidos.text)

        res = ast.literal_eval(test_string)
        images_on_page = []
        for i in res:
            imagen = dict_urls[i["asin"]]
            images_on_page.append(imagen)

        st.image(images_on_page, width=200)
    st.markdown("""---""")

with populares_valoradas:
    st.header("Popularity Model: Más Valoradas")
    agree = st.checkbox('Ver más VALORADAS')
    if agree:
        mas_valorados = requests.get("https://manuelpodaderatfm555.ue.r.appspot.com/listado_mas_valorados")
        test_string = json.loads(mas_valorados.text)

        res = ast.literal_eval(test_string)
        images_on_page = []
        for i in res:
            imagen = dict_urls[i["asin"]]
            images_on_page.append(imagen)
        st.image(images_on_page, width=200)

    st.markdown("""---""")

with regla_de_asociacion:
    st.header("Reglas de Asociación")
    ver_regla = st.checkbox('Ver más REGLAS de ASOCIACIÓN')
    if ver_regla:
        option_regla = st.selectbox('Seleccione una Revista de la lista para Regla de Asociación',asociados)

        imagen = dict_urls[option_regla]

        st.text("Los usuarios que compraron la REVISTA")
        st.image(imagen, width=300)

        if option_regla in dict_regla.keys():
            revista_asociada = dict_regla[option_regla]

            imagen_junto = dict_urls[revista_asociada]
            st.text("Frecuentemente comprados tambien la REVISTA")
            st.image(imagen_junto, width=300)
        else:
            st.subheader("ESTA REVISTA NO TIENE REGLA DE ASOCIACIÓN")

    st.markdown("""---""")

with content_based:
    st.header("CONTENT BASED")
    ver_content = st.checkbox('Ver más CONTENT BASED')
    if ver_content:
        option_content = st.selectbox('Seleccione una Revista de la lista',content_lista_items)

        imagen = dict_urls[option_content]
        st.image(imagen, width=300)

        test_string_content = recomendacion_content_based(option_content)

        images_on_page_content = []
        c = 0
        for i in test_string_content:

            imagen = dict_urls[i]
            images_on_page_content.append(imagen)
            c = c + 1
            if c > 9:
                break

        st.image(images_on_page_content, width=200)

        st.markdown("""---""")

with colaborative:
    st.header("MODELO COLABORATIVO")
    ver_content = st.checkbox('Ver más COLABORATIVO')
    if ver_content:
        usuario = st.selectbox('Seleccione un USUARIO de la lista',usuarios)

        Nombre = dict_user_name[usuario]
        st.text("el usuaruo seleccinado se llama: "+Nombre)



        resultado_collabo = resultado_colaborativo(usuario)

        images_on_page_content = []
        c = 0
        for i in resultado_collabo:
            revista = i[0]
            imagen = dict_urls[revista]
            images_on_page_content.append(imagen)
            c = c + 1
            if c > 9:
                break

        st.image(images_on_page_content, width=200)

    st.markdown("""---""")
with hibrido:
    st.header("MODELO HIBRIDO")
    ver_content = st.checkbox('Ver más MODELO HIBRIDO')
    if ver_content:
        usuario1 = st.selectbox('Seleccione USUARIO de la lista',usuarios)
        revista2 = st.selectbox('Seleccione REVISTA de la lista',content_lista_items)

        Nombre = dict_user_name[usuario1]
        grupo = dict_user_tipo[usuario1]
        st.text("el usuaruo seleccinado se llama: "+Nombre)
        st.text("el usuaruo seleccinado es del GRUPO: "+grupo)

        imagen = dict_urls[revista2]
        st.image(imagen, width=300)

        resultado_hibrido = recomendacion_hibrida(usuario1,revista2)

        images_on_page_hibrido = []

        for revista in resultado_hibrido:
            imagen = dict_urls[revista]
            images_on_page_hibrido.append(imagen)

        st.image(images_on_page_hibrido, width=200)