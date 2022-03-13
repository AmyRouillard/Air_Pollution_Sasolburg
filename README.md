# Air_Pollution_Sasolburg

This repository contains code relating to twist challenge 2. For this challenge an interactive dashboard was built to visualise historical air pollution data from the Sasolburg area. In addition, a seven-day forecast if made to predict air pollution levels at each of seven air pollution monitoring sites. 
Data retrieved for the South African air quality information system [SAAQIS]( https://saaqis.environment.gov.za) was used to create a database of historical air pollution data from seven site within a 20 km radius of Sasolburg. This is detailed a notebook [here]( https://github.com/AmyRouillard/Air_Pollution_Sasolburg/blob/main/0_Create_Database.ipynb). Each site monitors different pollutants as detailed [here]( https://github.com/AmyRouillard/Air_Pollution_Sasolburg/blob/main/1_EDA.ipynb).

Using this air pollution database, a multivariate time series model is created for each site using a long short-term memory (LSTM) architecture. The training of these models is shown [here]( https://github.com/AmyRouillard/Air_Pollution_Sasolburg/blob/main/2_training_LSTM.ipynb). Finally, the trained models are used to create a seven-day forecast for air pollution levels at each site, as presented [here]( https://github.com/AmyRouillard/Air_Pollution_Sasolburg/blob/main/3_forcast.ipynb).

The code and assets relating to the dashboard can be found in the [App folder]( https://github.com/AmyRouillard/Air_Pollution_Sasolburg/tree/main/App). 

<img src=https://github.com/AmyRouillard/Air_Pollution_Sasolburg/blob/main/App/assets/image121.png alt="map" width="80%" class="center"/>
