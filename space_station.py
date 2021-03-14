import pandas as pd
import plotly.express as px
import streamlit as st
import time

url = 'http://api.open-notify.org/iss-now.json'

df = pd.read_json(url)
df['latitude'] = df.loc['latitude', 'iss_position']
df['longitude'] = df.loc['longitude', 'iss_position']
df.reset_index(inplace= True)
df.drop(columns= ['index', 'message'])

latitude = df['latitude'][0]
longitude = df['longitude'][0]



print(latitude, longitude)
main_df = px.data.gapminder()
main_df['latitude'] = latitude
main_df['longitude'] = longitude

menu = ['Home', 'Scatter-Geo', 'Positions of Space Station']
option = st.sidebar.selectbox("Menu", menu)
if option == 'Home':
	st.title('Internation Space Station')
	st.subheader('Here you can see the current location of the Internation Space Station Plotted on Various Maps.')
	st.write()
	st.write('Api used: {url}'.format(url= url))
elif option == 'Scatter-Geo':
	global positions
	st.title("Scatter-Geo ")
	st.subheader('Here you can see the position plotted on the graph.')
	st.write()
	st.write('Projection: Natural Earth')

	fig1 = px.scatter_geo(main_df, 
		lat= 'latitude', 
		lon= 'longitude',
		projection= 'natural earth')

	st.write(fig1)

	fig2 = px.scatter_geo(main_df, 
		lat= 'latitude', 
		lon= 'longitude')

	st.write("Projection: Flat Earth")
	st.write(fig2)


elif option == 'Positions of Space Station':

	df1 = {'latitude': [],
			'longitude': []}

	st.title("Previous Positions of the Space Station:")
	#st.info('Note that the positions are refreshed after every 10 seconds for the entire duration.')
	counter = 2
	duration = st.number_input('Enter the duration (in seconds) for which you want to Plot the positions')
	if duration < 0 :
		st.warning("Please enter a Positive Value !!")
	elif duration == 0:
		st.warning("Please enter a Positive value greater than 0 !!")

	counter = st.number_input('Enter the counter number (default is 2)')
	if counter < 0:
			st.warning("Please enter a Positive Value !!")

	elif counter == 0:
		st.warning("Please enter a Positive value greater than 0 !!")

	submit = st.button("submit")
	
	if ( duration >= 2 and counter >= 2 ) and submit:
		timer = 0
		while True:
			df = pd.read_json(url)
			df['latitude'] = df.loc['latitude', 'iss_position']
			df['longitude'] = df.loc['longitude', 'iss_position']
			df.reset_index(inplace= True)
			df.drop(columns= ['index', 'message'])

			latitude = df['latitude'][0]
			longitude = df['longitude'][0]

			#df1 = pd.read_csv('positions.csv')
			#df1['latitude'].append(latitude)
			#df1['longitude'].append(longitude)
			df1['latitude'].append(latitude)
			df1['longitude'].append(longitude)
			df_main = pd.DataFrame(df1)
			df_main.to_csv('positions.csv')
			if timer == duration:
				break
			else:
				time.sleep(counter)
				timer += counter

		
	df2 = pd.read_csv('positions.csv')
	fig3 = px.scatter_geo(df2, 
		lat= 'latitude', 
		lon= 'longitude',
		projection= 'natural earth')

	st.write(fig3)
		



	

	
