# ENERMIZER

### Overview
The goal of this project is to use smartphones and smart IoT devices to transform the home into
a smart power ecosystem. The background process and business rules will monitor current
electricity rates and consume power based on the rate.

### Initial setup
The following are the process involved for initial setup
1. Clone this repository
2. Navigate to the clone directory `cd smart_plug`
3. Install all necessary python packages
4. Execute the following command to start the API_SERVICES
   `python3 api_services.py`
5. You will see the API_SERVICES running of the following link
   `http://192.168.1.166:8080/api/`
6. Using the above services you can perform all the Raspberry Pi operations
   For example: Accessing the GPIO pins, activating and deactivating relays and more.

### Contact 
# Developers
Harishankar Govindsamy | harishankarghs@gmail.com
Muthukumar Neelamegam | kumar.neelamegam17@gmail.com

# Hints for development
Report 1 - Energy consumed over selected time period
Create an api based on from and to date.
Should be post method with two parameters.

------------
Report 2 - Costs of energy consumed = Sum of all hourly Energy consumed x Awattar price
Peter:
The Costs of Energy consumed (energy consumption costs) are for every hour the energy used during this hour times the aWattar price for this hour.
The sum total of these numbers over the defined  period.  This number divided by the energy consumed results in the Average Effective Price.


------------
Report 3 - Average effective price = Costs of energy consumed over period divided by Energy consumed over period


------------
Report 4 - Average Awattar price over period
(DONE)

------------
Peter: In addition the app needs to calculate the average of all awattar prices of the selected period.
Get the average Awattar price over the selected period.
Create an api based on the selected from and to date.
Should be post method with from date and to date.


------------
Report 5 - Savings = Costs of energy consumed minus Sum of all hourly Energy consumed x Average Awattar price

The difference between this average price and the above average effective price will be multiplied with the energy consumed to
result in the total costs saved.

------------

/**
Check the description for creating a reports

Create a single rest method and return the reports results in a Json format
getReports(fromDate, toDate) {

<string name="report1">Energy consumed over period of time</string>
    <string name="report2">Costs of energy consumed</string>
        <string name="report2_subtitle">(Sum of all hourly Energy consumed x Awattar price)</string>
    <string name="report3">Average effective price</string>
        <string name="report3_subtitle">(Costs of energy consumed over period divided by Energy consumed over period)</string>
    <string name="report4">Average Awattar price over period</string>
    <string name="report5">Savings</string>
        <string name="report5_subtitle">Costs of energy consumed minus Sum of all hourly Energy consumed x Average Awattar price</string>


   create a internal method for retrieving the values of all the reports
    // Report 1 - Energy consumed over period of time [DONE]

    // Report 2 - Costs of energy consumed - (Sum of all hourly Energy consumed x Awattar price)

    // Report 3 - Average effective price - (Costs of energy consumed over period divided by Energy consumed over period)

    // Report 4 - Average Awattar price over period [DONE]

    // Report 5 - Savings - Costs of energy consumed minus Sum of all hourly Energy consumed x Average Awattar price

    Formula:
    R1 = Get the data from the Smart-Meter Json api
    R2 = R1 x R4
    R3 = R2 / R1
    R4 = Get the data from Awattar services and Consolidate it
    R5 = R2 - R1 x R4

    return ""

}

