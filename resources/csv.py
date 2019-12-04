# #Code credit to Will
# sqlite> .mode csv

# sqlite>.import c:/sqlite/city.csv rivers

# sqlite> .schema rivers
# CREATE TABLE rivers(
#   "name" TEXT,
# );

# SELECT 
#    name
# FROM 
#    rivers;

# DROP TABLE IF EXISTS rivers;


# CREATE TABLE rivers(
#   name TEXT NOT NULL,
# #   population INTEGER NOT NULL 
# );

# sqlite> .mode csv
# sqlite> .import c:/sqlite/city_no_header.csv rivers



#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  


import json
import csv
import requests

def grab_page():
    url = 'https://waterdata.usgs.gov/co/nwis/current/?type=flow'
    resp = requests.get(url)

    with open('usgs-waterdata.html', 'w+') as f:
        f.write(resp.text)

def get_data():
    with open('usgs-waterdata.html', 'r') as f:
        html = f.read()

    # We found <tbody> as the start of the information we car about and </tbody> as the end
    water_data_html = html.split('<tbody>')[1].split('</tbody>')[0]
    return water_data_html


def parse_html(html):
    river_sections = []
    river_system = None
    # https://docs.python.org/3.7/library/stdtypes.html#str.splitlines
    splitlines = html.splitlines()

    # Loop through lines of HTML, user enumerate because we are going to jump ahead using the index
    for i, line in enumerate(splitlines):
         # Get rid of leading or trailing whitespace
        line = line.strip()

        # Based on the pattern we found in the html we know this starts a river system table row
        if line == '<tr>':
            
             # The actual data is 3 lines ahead in list (aka down on HTML page)
            river_system_line = splitlines[i + 3]
           
            # Example of river_system_line  <strong><a name="10180001"><img alt="Group" border="0" width="10" height="10" src="/nwisweb/icons/greendot.gif" />   10180001 North Platte Headwaters</a></strong></font>
            # .split('/>')[1] gives us  />   10180001 North Pl....
            # .split('</a>')[0] gives us   10180001 North Platte Headwaters
            # .strip() gets rid of all the leading spaces
            river_system_text = river_system_line.split('/>')[1].split('</a>')[0].strip() # 
            
            # river_system_text.split(' ') gives list ['10180001', 'North', 'Platte', 'Headwaters'] of words separated by spaces
            # river_system_text.split(' ')[1:] skips ID and just gives name portion => ['North', 'Platte', 'Headwaters']
            # ' '.join creates a string again separating values with space => 'North Platte Headwaters'
            # Set the river_system to be used in the river section rows
            river_system = ' '.join(river_system_text.split(' ')[1:])

            # We are done with this iteration start the next one
            # https://docs.python.org/3.7/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops
            continue

        # If we 'see' valign="top" we know were entering a river section table row
        if 'valign="top"' in line:
            # The data will be on the next line of html so jump ahead
            river_section_line = splitlines[i + 1]

            # There are a bunch of &nbsp; in the row that we don't want so let's
            # get ride of them
            river_section_line = river_section_line.replace('&nbsp;', '')

            # A row looks like this now that we remove the &nbsp:
            # <td align="left"><a href="/co/nwis/uv/?site_no=09371520&amp;PARAmeter_cd=00065,00060">09371520</a></td><td align="left" nowrap="nowrap">MCELMO CREEK ABOVE TRAIL CANYON NEAR CORTEZ, CO</td><td nowrap="nowrap">12/03 08:30 MST</td><td>2.26</td><td><a href="#Ice_affected">Ice</a></td><td>27.0</td><td>25.0</td>
 
            # There are a several places the data for the particular row exist so we 
            # can extract them using a loop. We know the actual data will be between
            # html tags so lets start by spliting the row up

            river_section_split = river_section_line.strip().split('>')

            # river_section_split becomes a list like this:
            # ['<td align="left"', '<a href="/co/nwis/uv/?site_no=06614800&amp;PARAmeter_cd=00065,00060"', '06614800</a', '</td', '<td align="left" nowrap="nowrap"', 'MICHIGAN RIVER NEAR CAMERON PASS, CO</td', '<td nowrap="nowrap"', '12/03 09:00 MST</td', '<td', '2.31</td', '<td', '0.40</td', '<td', '.48</td', '<td', '.44</td', '']
            # We can see the items that we care about look like this:
            # ['06614800</a', 'MICHIGAN RIVER NEAR CAMERON PASS, CO</td', '12/03 09:00 MST</td', '2.31</td', '0.40</td', '.48</td', '.44</td']
            # What do the have in common? They lead with the value you want and
            # end with a closing tag (</a or </td). The items we don't care about
            # lead with < (an opening HTML tag) or a an empty string


            cleaned_td_values = []
            for td in river_section_split:
                # Get rid of empty items and items without '</' because it won't
                # contain data we are interested in
                if not td or '</' not in td:
                    continue

                # Get the actual data between the tags and remove &nbsp;
                cleaned_td_value = td.split('</')[0].strip()
                cleaned_td_values.append(cleaned_td_value)

            # Some rows don't have IDs because they are subrows of river systems.
            # We don't want to deal with those right now but we definitely could
            # decide to in the future. We could add more logic to merge that data
            # into our set properly in the future.
            if not cleaned_td_values or not cleaned_td_values[0]:
                continue
                # Future - Handle the next line scenario

            river_section = {
                'river_system': river_system,
                'river_section_number': cleaned_td_values[0],
                'station_name': cleaned_td_values[1],
                'time_of_reading': cleaned_td_values[2],
                'gauge_height': cleaned_td_values[3],
                'discharge': cleaned_td_values[4],
                'lt_mean_flow': cleaned_td_values[5],
                'lt_median_flow': cleaned_td_values[6]
            }
            river_sections.append(river_section)

    return river_sections


def write_json(data):
    with open('usgs-waterdata.json', 'w+') as f:
        f.write(json.dumps(data))

def write_csv(data):
    """ Data is river_sections list """
    # https://docs.python.org/3.7/library/csv.html#csv.DictWriter
    with open('usgs-waterdata.csv', 'w+') as csvfile:
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for river in data:
            writer.writerow(river)




if __name__ == "__main__":
    # grab_page()
    water_data_html = get_data()
    clean_data = parse_html(water_data_html)

    # We can then create a json file, csv file or write the data to our database
    write_json(clean_data)
    write_csv(clean_data)
    # update_db(clean_data) => we don't have a DB setup but we could do this