App for outdoor enthusiasts and related industry.  Provides flow rates and data of river sections, weather forecast for the sections, and campgrounds.  Will require web scraping for river data, API for weather, and may manually put in campgrounds which is the stretch goal.

User can view all major river systems.  They can select a river system and view data sets on different sections of the rivers.  Additionally, they can view the weather forecast for the area.  This will allow the user to see the status of their favored river, and the forecast to plan a recreational trip to the area.  The data will be in updated daily. Additionally, users can select favorite rivers.

TBD: How to organize rivers as the data sets are by sections which are unrelated to the typical put-ins for rafting or fishing or even public access
DATA: Webscraping river system datasets that need to be updated daily, weather API updated every 3-4 hours.  Campgrounds don't need to be updated.

Stretch goals:
1) Tie in campgrounds to the river sections
2) Allow users to comment and provide pictures or information of their day.
3) Flood/Fire alerts

<HEADER>
RIVER SYSTEMS  RIVER SECTIONS  MY RIVERS  LOGIN/OUT

----RIVER SYSTEMS------
Colorado River System (clickable)
San Juan River System
etc
*When clicked, react changes page to the related river sections that have data


----RIVER SECTIONS-----
River Section / Time/ River flow / historigcal average
7 Day forecast
Campgrounds
River Section / Time / River flow etc
7 Day forecast
Campgrounds

----MY RIVERS -----
River Section / Time/ River flow / historigcal average
7 Day forecast
Campgrounds


models
user: email, password
River Systems: WebScraping (river), weather API
River Sections: Webscrapting (river), weather API, foriegn key for river
Favorite Rivers: Webscrapting (river), weather API, userID, foreign key for river and user

Setup flask repo (models, controllers, resources) - when you send tests through postman you get responses i expect
