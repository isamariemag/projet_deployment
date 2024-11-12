import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Chargement des données
df = pd.read_csv('/app/get_around_pricing_ML.csv')
# Nouveau dataset pour l'analyse des retards
df_delay = pd.read_csv('/app/get_around_delay_analysis.csv', sep=';')

# Titre du dashboard
st.title("Dashboard Getaround isa")

# Afficher deux graphiques côte à côte
#st.subheader("Distribution des types d'enregistrement et de l'état de location")
col1, col2 = st.columns(2)

# Graphique 1: Distribution des valeurs de type d'enregistrement
with col1:
    fig_checkin_type = px.histogram(df_delay, x='checkin_type', title="Types d'enregistrement", template='plotly_white')
    fig_checkin_type.update_layout(title={'x': 0.5, 'xanchor': 'center'})
    st.plotly_chart(fig_checkin_type)

# Graphique 2: Distribution des valeurs de l'état de location des voitures
with col2:
    fig_state = px.histogram(df_delay, x='state', title="État de location des voitures", template='plotly_white')
    fig_state.update_layout(title={'x': 0.5, 'xanchor': 'center'})
    st.plotly_chart(fig_state)

# Sous-titre pour chaque question et graphique correspondant

# Impact des retours tardifs des voitures sur la satisfaction client
st.subheader("Quel est l'impact des retours tardifs des voitures sur la satisfaction client ?")
# Ajout d'une nouvelle colonne indiquant si le retour est tardif (seuil > 30 minutes)
df_delay['late_return'] = df_delay['delay_at_checkout_in_minutes'] > 30
fig_impact_late_return = px.histogram(df_delay, x='state', color='late_return', barmode='group', title="Impact des retours tardifs sur l'état de la location", template='plotly_white', labels={'late_return': 'Retour tardif'})
st.plotly_chart(fig_impact_late_return)

# Seuil : quelle doit être la durée minimale du délai ?
st.subheader("Seuil : quelle doit être la durée minimale du délai ?")
# Ajout nouvelle colonne pour catégoriser les délais en intervalles
bins = [0, 30, 60, 90, 120, 180, float('inf')]
labels = ['0-30', '30-60', '60-90', '90-120', '120-180', '>180']
df_delay['delay_interval'] = pd.cut(df_delay['time_delta_with_previous_rental_in_minutes'], bins=bins, labels=labels)
# Calcul pourcentage de retours tardifs pour chaque intervalle
delay_analysis = df_delay.groupby('delay_interval')['late_return'].mean() * 100
fig_delay_analysis = px.bar(delay_analysis, x=delay_analysis.index, y=delay_analysis.values, labels={'x': 'Délai entre les locations (en minutes)', 'y': 'Pourcentage de retours tardifs (%)'}, title='Pourcentage de retours tardifs par intervalle de délai entre les locations', template='plotly_white')
st.plotly_chart(fig_delay_analysis)

# Portée : devons-nous activer la fonctionnalité pour toutes les voitures ? Uniquement pour les voitures connectées ?
st.subheader("Portée : devons-nous activer la fonctionnalité pour toutes les voitures ? Uniquement pour les voitures connectées ?")

# Utiliser un countplot pour compter les occurrences de 'checkin_type' et 'late_return'
df_delay_grouped = df_delay.groupby('checkin_type')['late_return'].mean().reset_index()

fig_checkin_type_performance = px.bar(
    df_delay_grouped, 
    x='checkin_type', 
    y='late_return', 
    title='Différence de Performance Entre Voitures Connectées et Non Connectées', 
    labels={'checkin_type': 'Type de Check-in', 'late_return': 'Proportion de Retours Tardifs'}, 
    template='plotly_white'
)
fig_checkin_type_performance.update_yaxes(title='Proportion de Retours Tardifs (%)', tickformat='.0%')
fig_checkin_type_performance.update_xaxes(title='Type de Check-in')

st.plotly_chart(fig_checkin_type_performance)


# Combien de locations seraient affectées par la fonctionnalité en fonction du seuil et de la portée choisis ?
st.subheader("Combien de locations seraient affectées par la fonctionnalité en fonction du seuil et de la portée choisis ?")
seuils = [90, 120]
mobile_data = df_delay[df_delay['checkin_type'] == 'mobile']
connect_data = df_delay[df_delay['checkin_type'] == 'connect']
locations_affectees_mobile = [mobile_data[mobile_data['time_delta_with_previous_rental_in_minutes'] < seuil].shape[0] for seuil in seuils]
locations_affectees_connect = [connect_data[connect_data['time_delta_with_previous_rental_in_minutes'] < seuil].shape[0] for seuil in seuils]

fig_locations_affectees = go.Figure()
fig_locations_affectees.add_trace(go.Bar(x=seuils, y=locations_affectees_mobile, name='Mobile', marker_color='blue'))
fig_locations_affectees.add_trace(go.Bar(x=seuils, y=locations_affectees_connect, name='Connect', marker_color='green'))
fig_locations_affectees.update_layout(title='Nombre de Locations Affectées par Seuil et Type de Check-In', xaxis_title='Seuil (minutes)', yaxis_title='Nombre de Locations Affectées', barmode='group', template='plotly_white')
st.plotly_chart(fig_locations_affectees)


# Sous-titre DATASET PRIX
st.subheader("Analyse des prix de location des voitures")

# Ajout de filtres
model_key = st.selectbox("Sélectionner un modèle de voiture", options=["Tous"] + list(df['model_key'].unique()))
engine_power = st.slider("Puissance du moteur (en chevaux)", int(df['engine_power'].min()), int(df['engine_power'].max()), (int(df['engine_power'].min()), int(df['engine_power'].max())))
fuel_type = st.multiselect("Type de carburant", options=df['fuel'].unique(), default=df['fuel'].unique())
paint_color = st.multiselect("Couleur de la peinture", options=df['paint_color'].unique(), default=df['paint_color'].unique())
car_type = st.multiselect("Type de voiture", options=df['car_type'].unique(), default=df['car_type'].unique())
private_parking_available = st.radio("Parking privé disponible ?", options=["Tous", True, False])

# Filtrage des données
filtered_df = df.copy()

if model_key != "Tous":
    filtered_df = filtered_df[filtered_df['model_key'] == model_key]

filtered_df = filtered_df[(filtered_df['engine_power'] >= engine_power[0]) & (filtered_df['engine_power'] <= engine_power[1])]
filtered_df = filtered_df[filtered_df['fuel'].isin(fuel_type)]
filtered_df = filtered_df[filtered_df['paint_color'].isin(paint_color)]
filtered_df = filtered_df[filtered_df['car_type'].isin(car_type)]

if private_parking_available != "Tous":
    filtered_df = filtered_df[filtered_df['private_parking_available'] == (private_parking_available == True)]

# Distribution des prix de location
st.subheader("Distribution des prix de location par jour")
fig = px.histogram(filtered_df, x='rental_price_per_day', nbins=20, title='Distribution des prix de location', labels={'rental_price_per_day': 'Prix de location par jour'}, template='plotly_white', color_discrete_sequence=['#1DD0F1'])
fig.update_layout(xaxis_title='Prix de location par jour', yaxis_title='Fréquence')

st.plotly_chart(fig)

# Statistiques descriptives
st.subheader("Statistiques descriptives des prix de location")
st.write(filtered_df['rental_price_per_day'].describe())