import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development

# Set configuracion

st.set_page_config(
    page_title="Cáncer en Chile 1998-2019",
    page_icon="🦫",
    layout="wide",
)


# Dashboard title.
st.title("Cáncer en Chile (1998-2019)")
st.markdown(
    '<span style="font-style: italic; margin-right: 10px;">Esteban Navarro</span>'
    '<a href="https://www.linkedin.com/in/nlesteban/" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" style="width: 25px; height: 25px; margin-right: 10px;"></a>'
    '<a href="https://github.com/estebannl" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub" style="width: 25px; height: 25px; margin-right: 10px;"></a>'
    '<a href="https://estebannl.netlify.app/" target="_blank"><img src="https://cdn-icons-png.flaticon.com/512/25/25256.png" alt="Sitio web" style="width: 25px; height: 25px; margin-right: 10px;"></a>'
    'A partir de los Registros Poblacionales de Cáncer. Fuente: Ministerio de Salud',
    unsafe_allow_html=True
)


# Data
data_cancer = pd.read_spss("rpc_chile.sav", convert_categoricals = False)

# Define filtro principal
option_list = np.append('Todos los diagnósticos', np.unique(data_cancer['Grupo_diag_1']))
option = st.selectbox(
    "Seleccione diagnóstico:",
    option_list)
st.write("Selección:", option)

# Data filtrada
if (option == 'Todos los diagnósticos'):
    data_cancer2 = data_cancer
else: 
    data_cancer2 = data_cancer.query(f'Grupo_diag_1 == @option')

# Etiqueta RPC
dict_rpc = {5: 'Región de Arica y Parinacota',
            1: 'Región de Antofagasta',
            6: 'Región del Maule',
            3: 'Provincia de Biobío',
            2: 'Provincia de Concepción',
            4: 'Región de Los Ríos'}
data_cancer2['RPC_'] = data_cancer2['RPC'].replace(dict_rpc)

# Etiqueta Sexo
dict_Sexo = {1: 'Hombre',
             2: 'Mujer'}
data_cancer2['Sexo_'] = data_cancer2['Sexo'].replace(dict_Sexo)

# Etiqueta edad
dict_edad = {1: '0-14',
             2: '15-29',
             3: '30-49',
             4: '50-69',
             5: '70 +'}
data_cancer2['Grupo_edad'] = data_cancer2['Grupo_edad_1'].replace(dict_edad)

# Etiqueta Base diagnostico
dict_Base_diagnostico = {0: 'Solo certificado de defunción',
             1: 'Clínico',
             2: 'Investigación clínica',
             4: 'Bioquímica o inmunología',
             5: 'Citología',
             6: 'Histología de una metástasis',
             7: 'Histología de un tumor primario',
             9: 'Desconocido'}
# Aplica etiquetas
data_cancer2['Base_diagnostico_'] = data_cancer2['Base_diagnostico'].replace(dict_Base_diagnostico)


# Etiqueta Estado
dict_estado = {1: 'Vivo',
               2: 'Fallecido'}
# Aplica etiquetas
data_cancer2['Estado'] = data_cancer2['VM'].replace(dict_estado)


# Etiqueta Causa de fallecimiento
dict_causa_def = {1: 'Cáncer',
                  2: 'Otra causa',
                  9: 'Desconocida'}
# Aplica etiquetas
data_cancer2['Causa_defuncion_'] = data_cancer2['Causa_defuncion'].replace(dict_causa_def)

# Fallecidos por cáncer hasta 2014
data_cancer3 = (data_cancer2.
                query('Causa_defuncion == 1 and Año_diag <= 2014'))

# Crea diferencia de dias: desde diagnostico hasta muerte por cancer
data_cancer3['Fecdiag'] = pd.to_datetime(data_cancer3['Fecdiag'])
data_cancer3['fecha_defuncion_act2020'] = pd.to_datetime(data_cancer3['fecha_defuncion_act2020'])
data_cancer3 = data_cancer3.assign(
    dif_dias=lambda x: (x['fecha_defuncion_act2020'] - x['Fecdiag']).dt.days)


# Cálculos ---------------------------------------------------------------------

# Cantidad de registros por RPC
registros_data_cancer2 = data_cancer2.shape[0]

# Diagnosticos totales por RPC
tbl_diag = (data_cancer2.value_counts("RPC_")).sort_index().reset_index()
tbl_diag['porc'] = np.round(100*tbl_diag['count']/np.sum(tbl_diag['count']),1)

# Diagnosticos por año y RPC
# Tbl
tbl_diag_ano = (data_cancer2.value_counts(['Año_diag', "RPC_"])).sort_index().reset_index()
# Fig
fig_diag_ano = px.bar(tbl_diag_ano, 
              x="Año_diag", y="count", color="RPC_", 
              title="Diagnósticos de cáncer 1998-2019 según Registro Poblacional",
              color_discrete_sequence=px.colors.qualitative.Bold,
              hover_name = 'Año_diag', hover_data= ['RPC_', 'count']
              )
fig_diag_ano.update_layout(
    dragmode=False  # Deshabilita el modo de arrastre (zoom)
)

# Diagnosticos por sexo
tbl_sexo = data_cancer2['Sexo_'].value_counts().sort_index().reset_index()
tbl_sexo['pct'] = round(100*tbl_sexo['count']/np.sum(tbl_sexo['count']),1)
# tbl_sexo = tbl_sexo.sort_values(by = "Sexo_")
#Fig
fig_sexo = px.pie(tbl_sexo, values='count', names='Sexo_', 
                  category_orders = {'Sexo_': ['Mujer', 'Hombre']},
                  color_discrete_sequence=px.colors.qualitative.Bold,
                  opacity= 0.8,
                  title='Distribución por sexo')
fig_sexo.update_layout(
    dragmode=False  # Deshabilita el modo de arrastre (zoom)
)


# Diagnosticos por grupo de edad
tbl_edad = data_cancer2['Grupo_edad'].value_counts().sort_index().reset_index()
tbl_edad['pct'] = round(100*tbl_edad['count']/np.sum(tbl_edad['count']),1)
# tbl_edad = tbl_edad.sort_values(by = 'Grupo_edad')
# Fig
fig_edad = px.bar(tbl_edad, x = 'pct', y = 'Grupo_edad',
                  title = "Distribución por grupos de edad", orientation='h',
                  text_auto=True)
fig_edad.update_layout(
    dragmode=False  # Deshabilita el modo de arrastre (zoom)
)

# Tabla Base diagnostico
tbl_base_diag = data_cancer2.value_counts(['Base_diagnostico', 'Base_diagnostico_']).reset_index()
tbl_base_diag['pct'] = round(100*tbl_base_diag['count']/np.sum(tbl_base_diag['count']),1)
tbl_base_diag = tbl_base_diag.sort_values(by = 'Base_diagnostico')
tbl_base_diag = tbl_base_diag.drop(['Base_diagnostico'], axis=1)
# Fig
fig_base_diag = px.bar(tbl_base_diag, x = 'pct', y = 'Base_diagnostico_',
                  title = "Distribución según base del diagnóstico", orientation='h',
                  text_auto=True)
fig_base_diag.update_layout(
    dragmode=False  # Deshabilita el modo de arrastre (zoom)
)

# Tabla Descriptivos por edad
tbl_edad_descH = data_cancer2.query('Sexo == 1')['Edad'].describe().reset_index().rename(columns = {'Edad' : 'Hombre'})
tbl_edad_descM = data_cancer2.query('Sexo == 2')['Edad'].describe().reset_index().rename(columns = {'Edad' : 'Mujer'})
tbl_edad_descA = data_cancer2['Edad'].describe().reset_index().rename(columns = {'Edad' : 'Ambos Sexos'})

tbl_edad_desc = (tbl_edad_descH.
 merge(tbl_edad_descM, how = 'left', on = 'index').
 merge(tbl_edad_descA, how = 'left', on = 'index')
 ).rename(columns = {'index': 'Indicador'})

# Histograma edad
fig_hist = px.histogram(data_cancer2, 
                        nbins=50,
                        x="Edad",
                        color="Sexo_",
                        color_discrete_sequence=px.colors.qualitative.Bold,
                        histnorm='probability density',   
                        marginal='box', 
                        opacity= 0.7,
                        hover_data=data_cancer2.columns,
                        category_orders = {'Sexo_': ['Mujer', 'Hombre']})
fig_hist.update_layout(barmode='overlay',
                       title='Distribución de la edad al diagnóstico, según sexo')
fig_hist.update_layout(
    dragmode=False  # Deshabilita el modo de arrastre (zoom)
)

# Tabla Estado hasta 2020 de pacientes diagnosticados
tbl_estado = data_cancer2.value_counts(['Estado']).reset_index()
tbl_estado['pct'] = round(100*tbl_estado['count']/np.sum(tbl_estado['count']),1)
tbl_estado = tbl_estado.sort_values(by = "Estado")
# Fig
fig_estado = px.pie(tbl_estado, values='count', names='Estado', 
                    category_orders = {'Estado': ['Fallecido', 'Vivo']},
                    title='Estado hasta diciembre 2020',
                    color_discrete_sequence=px.colors.qualitative.Bold_r)
fig_estado.update_layout(
    dragmode=False  # Deshabilita el modo de arrastre (zoom)
)



# Tabla Causa de muerte
tbl_causa_def = (data_cancer2.query('VM == 2').value_counts('Causa_defuncion_')).reset_index()
tbl_causa_def['pct'] = round(100*tbl_causa_def['count']/np.sum(tbl_causa_def['count']),1)
tbl_causa_def = tbl_causa_def.sort_values(by = "Causa_defuncion_")
# Fig
fig_causa_def = px.pie(tbl_causa_def, values='count', names='Causa_defuncion_',
                       category_orders = {'Causa_defuncion_': ['Cáncer', 'Otra causa']},
                       title='Causa de muerte hasta diciembre 2020',
                       color_discrete_sequence=px.colors.qualitative.Bold_r)
fig_causa_def.update_layout(
    dragmode=False  # Deshabilita el modo de arrastre (zoom)
)

# Dias tras el diagnostico hasta la defuncion  (fallecidos por cáncer
# Fig
ymax = data_cancer3['dif_dias'].quantile(0.9)
fig_dif_dias = px.box(data_cancer3, y="dif_dias", x='Año_diag',
                                        title='Días transcurridos desde el diagnóstico hasta el fallecimiento por cáncer')
fig_dif_dias.update_yaxes(range=[0, ymax])  # Establece el rango máximo del eje Y, por ejemplo, de 0 a 100
fig_dif_dias.update_layout(
    dragmode=False  # Deshabilita el modo de arrastre (zoom)
)



# UI --------------------------------------------------------------------------------

# Configuración para deshabilitar todas las funciones interactivas
config = {
    'staticPlot': True,  # Hacer que el gráfico sea estático
    'displayModeBar': False,  # Ocultar la barra de herramientas de modo
    'scrollZoom': False,  # Deshabilitar el zoom con la rueda del ratón
    'doubleClick': 'reset',  # Deshabilitar el doble clic para restablecer el zoom
    'showTips': False,  # Deshabilitar las herramientas emergentes
    'responsive': True  # Hacer que el gráfico sea responsivo
}
st.markdown(f'#### 1. Evolución diagnósticos: {option}')       

# creating a single-element container
placeholder = st.empty()

with placeholder.container():
    # create two columns for charts
    fig_col1, fig_col2 = st.columns([1,3])
    with fig_col1:
        st.write(f'''
                 * Total de registros: **{registros_data_cancer2}**''')
        st.write("**Diagnósticos según Registro Poblacional**")
        # st.table(tbl_diag.reset_index(drop=True))
        st.dataframe(tbl_diag, hide_index=True)
        
        
    with fig_col2:
        # Tabla
        # st.plotly_chart(fig_diag_ano, config = config)
        st.write(fig_diag_ano)
 

st.markdown(f'#### 2. Características de los diagnosticados: {option}')       


placeholder2 = st.empty()

with placeholder2.container():
    # create two columns for charts
    col1, col2, col3 = st.columns([2,2,3])
    with col1:
        st.write(fig_sexo)

    with col2:
        st.write(fig_edad)        
    with col3: 
        st.write(fig_base_diag)
 

placeholder3 = st.empty()

with placeholder3.container():
    # create two columns for charts
    col1, col2 = st.columns([1,2])
    with col1:
        st.markdown('**Estadísticos descriptivos: edad al momento del diagnóstico**')
        st.dataframe(tbl_edad_desc, hide_index = True)

    with col2:
        st.write(fig_hist)        

# st.dataframe(table3)

st.markdown(f'#### 3. Estado de los pacientes diagnosticados: {option}')      

placeholder4 = st.empty()

with placeholder4.container():
    # create two columns for charts
    col1, col2, col3 = st.columns([1,1,2])
    with col1:
        st.write(fig_estado)

    with col2:
        st.write(fig_causa_def)        
        
    with col3:
        st.write(fig_dif_dias)        




 


# st.table(pd.crosstab(data_cancer2['Año_diag'] , data_cancer2['RPC_'],
#                      margins=True))

# Estilo CSS para centrar contenido
st.markdown("""
         
         #### Sobre esta App
         
         * Desarrollada con Streamlit (Python).
         * Datos: Registros Poblacionales de Cáncer: Datos del Ministerio de Salud de Chile. Base de datos actualizada al 04 de agosto de 2023. 
         Disponible en: https://epi.minsal.cl/registros-poblacionales-de-cancer-bd/
         """)
