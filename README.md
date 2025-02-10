Hey there, 

Here is a project that I realised: it uses a ML model to estimate the value of real estate properties in Paris. The model was trained on all the properties that were sold in Paris in 2023. It takes into account parameters such as: Square Meters, Number of Rooms, Location, Condition....

The dataset that I used has some limits (e.g. doesn't take into account the construction year of the building or the conditon). In an effort to make it as accurate as possible, I added 2 coefficients: Property Condition and Floor Level. These are not perfect but allow to give more details to the computation. 

The repository also includes a server and a HTML/CSS webpage to have a fully functioning interface where the user can fill the information.

The datat that was used is from a Kaggle dataset that you can found here: https://www.kaggle.com/datasets/nechbamohammed/real-estate-dataset
