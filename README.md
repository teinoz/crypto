# crypto_project
Inside the Git repository it is possible to access two folders (crypto_app and crypto_project):
1) Crypto_app contains all the Python scripts running through Django ( models.py, views.py and commands folder).
2) Crypto_project contains the settings for the server.

The code is structured as follows:

#Crypto class and CoinValue class to create the crypto cascade object.
#Command to add a coin in the database with all his values and make predictions (crypto_update).
#Form Addcrypto to add a crypto from the web app.
#Command crypto_rt that corresponds to the MQTT receiver and manages the update of the data sent by the cron job.
#Command crypto_predict to make the predictions for all the crypto objects.
#View function show_crypto that allows you to take forecasts from the database and view them on the web app.
#View function new_crypto usable from the web interface only by admin users to add a new crypto to the database with his related coin values.
#View function graph that displays a dynamic graph of the trend of a given currency in real time.

In the web app ( accessible here: http://18.232.144.163/) it is possible to see the current price of the crypto currencies already stored in the database along with the relative predictions of the close value for the current day. 

It is also possible to visualize:
- the percentage change associated with our prediction, calculated on the close price of the previous day
- the forecast for the next hour compared to the current one. 

The predictions, as mentioned above, are updated daily. Moreover by using an admin view, it is also possible to type a crypto name and symbol and directly load all the data in the database and automatically produces the graph with his output.
