import googlemaps
import json
import pandas as pd
import requests
from sklearn.cluster import KMeans
import plotly.graph_objects as go
from plotly.subplots import make_subplots

'''
Objective: Given a graph that starts and ends on the same vertex, this script outputs the shorest path(s).
Inputs: The address of the origin, addresses of all orders, and the number of driver.
Outputs: Shorest path(s) based on the number of drivers.

'''


# Load the number of driver.
n_driver=int(input("Enter the number of drivers: "))

# Load all addresses into list.
file_path=input(

"Enter full path to the CSV file containing all \
addresses stored in a key column 'Addresses'. \
The first row must be the Origin: \n"

)

df=pd.read_csv(file_path.strip())
delivery_center=df['Addresses'][0]
df=df.drop(df.index[0])
addresses=list(df['Addresses'])

# Load GoogleAPI.
google_api_key=input("\nEnter your google API key: \n")

# Load RoutXL API.
print("\nYou'd need an account from https://www.routexl.com/register ")
user_name=input("Enter username: ")
user_password=input("Enter user password: ")

print("Loading ... ")


def address_to_latlng(address):

    gmaps = googlemaps.Client(key=google_api_key.strip())
    gmaps_result = gmaps.geocode(address)
    result = gmaps_result[0]['geometry']['location']
    lat=result['lat']
    lng=result['lng']
    return lat, lng

# Map Origin's address into x, y.
o_lat, o_lng = address_to_latlng(delivery_center)

# Map all  addresses besides Origin into X, Y.
name, lat, lng = [],[],[]

for address in addresses:
    try:
        name.append(address)
        lati,lngi=address_to_latlng(address)
        lat.append(lati)
        lng.append(lngi)
    except IndexError:
        print(" The number {} address is missing".format(locations.index(address)))
        lat.append(0)
        lng.append(0)

df=pd.DataFrame(data={'name':name,'lat':lat,'lng':lng})


# Compute k Clusters
X_columns=['lat','lng']
X=df[X_columns].values
kmeans = KMeans(n_clusters=n_driver).fit(X)
y_kmeans = kmeans.predict(X)
df['class']=y_kmeans # Add the classified labels back to the original list


# Extract N lists(clusters).

dic={}
for i in range(n_driver):
	dic[i] = 0

for key, value in dic.items():
    dic.update({key:df.loc[df['class']==int(key)]})
    dic[key]=dic[key].drop(['class'],axis=1)


# Add Origin back to each list.

origin={'name': delivery_center,'lat':o_lat,'lng':o_lng}

for i in dic.keys():
    dic[i]=pd.concat([pd.DataFrame(origin,index=[0]), dic[i]], sort = True) # Add to the beginning
    dic[i]=dic[i].append(pd.DataFrame(origin,index=[0]), sort = True, ignore_index = True) # Add to the end
    dic[i]={'locations': dic[i].to_json(orient = 'records')} # Gather data
    dic[i]=requests.post(url='https://api.routexl.com/tour', auth=(user_name.strip(), user_password.strip()), data = dic[i]) # Get tour
    dic[i]=pd.read_json(json.dumps(dic[i].json()[u'route'],sort_keys = True), orient = 'index') # Return as pd.df


# Visualize K Clusters & Ouputs

specs=[[{"type":"scatter","rowspan": 2}],[ None ]]
table_titles=[None,]

for i in range(len(dic)):
    specs_list=[{"type":"table"}]
    specs.append(specs_list)
    table_titles.append("Driver "+str(i)+" 's List:")

fig = make_subplots(
    rows = 2 + n_driver,
    cols=1,
    vertical_spacing=0.07,
    specs=specs,
    subplot_titles=table_titles
    )


fig.add_trace(go.Scatter(
    x=X[:, 0],
    y=X[:, 1],
    mode="markers",
    name="Location",
    showlegend=False,
    marker=dict(
        symbol="circle",
        opacity=0.7,
        color=y_kmeans,
        colorscale='Earth',
        size=40
        )
    ),
    row=1, col=1
)


centers = kmeans.cluster_centers_

fig.add_trace(go.Scatter(
    x=centers[:, 0],
    y=centers[:, 1],
    mode="markers",
    name="Centroid",
    showlegend=True,
    marker=dict(
        symbol="circle",
        opacity=0.6,
        color='Black',
        size=10
        )
    ),
    row=1, col=1
)


fig.add_trace(go.Scatter(
    x=[o_lat],
    y=[o_lng],
    mode='markers',
    name="Origin",
    showlegend=True,
    marker=dict(
        symbol="cross-dot",
        color='Red',
        size=30
        )
    ),
    row=1, col=1
)


fig.update_layout(

    title_text="K Clustering: Each list is colored-coded; locations are in circle."
    margin=dict(l=20, r=20, t=40, b=40),
    width=1024,
    height=1024
)

# Set x, y axes titles
fig.update_yaxes(title_text="<b>Longitude(y)/latitude(x)<b>", row=1, col=1)


for i in dic.keys():

    fig.add_trace(go.Table(
        header=dict(
            values=['Order','Address','Arrival','Distance Factor'],
            fill_color='Black',
            align='left',
            font=dict(color='white', size=12)
            ),

        cells=dict(
            values=[dic[i].index.values,dic[i].name, dic[i].arrival, dic[i].distance],
            fill_color='lavender',
            align='left')
            ),
            row=int(i)+3, col=1
        )

    fig.update_yaxes(range=[0,944],row=int(i)+3, col=1)
    fig.update_xaxes(domain=[0,984],row=int(i)+3, col=1)


# Show figure.

if __name__ == '__main__':
    fig.show()
