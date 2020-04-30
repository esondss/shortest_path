
# Multi-Source Shortest Path (SF Hacks)

_The Chinese Postman Problem With Multiple Sources_

## Overview

This code base solves the shortest path problem with multiple agents (e.g. catering delivery) and displays the output in HTML. Given a network that starts and ends on the same vertex, the objective of the model is to find the shortest path(s) to visit all other vertices in the network given **n** number of sources. The "sources" is described as "drivers" in the script. The model script is tailored to work specifically with Google & RouteXL api. Below are the linkes to register:

1. [Google API](https://console.cloud.google.com/)
2. [RouteXL](https://www.routexl.com/register)

#### Model Inputs: <br>
1. The number of drivers.
2. A file that contains all addresses including the starting Origin.

#### Model Outputs: <br>
The list(s) of addresses each driver should be responsible for.

## Example

The sample data `'sample_addresses.csv'` contains addresses to 8 universities in the San Francisco Bay Area, with the Origin being at San Francisco International Airport. Below graph shows a clustering of the addresses with regard to the Origin. A detailed interactive output of the script is shown in `'output.html'`

<img width="1021" alt="clustering" src="https://user-images.githubusercontent.com/53110326/62250774-af61b200-b3a2-11e9-9946-277bab1d55ef.png">

## *Attachment

To save the ouput, WebVector can convert html file to png or svg. A Java runtime is required to run WebVector. In terminal, `cd` to where the webvector file is located and then simply call: `java -jar webvector-<version>.jar <url> <output_file> <format>` where:

- < url > is the URL of the page to convert.
- < output_file > is the resulting file name.
- < format > is either svg or png.
