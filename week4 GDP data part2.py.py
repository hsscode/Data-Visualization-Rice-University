import csv
import math

def build_country_code_converter(codeinfo):
    """
    Build a dictionary mapping plot codes to data codes.

    Args:
        codeinfo (dict): A dictionary specifying the details of the country code CSV file.

    Returns:
        dict: A dictionary mapping plot codes to data codes.
    """
    # Load country code mappings from CSV file
    codefile = codeinfo['codefile']
    plot_codes_key = codeinfo['plot_codes']
    data_codes_key = codeinfo['data_codes']

    with open(codefile, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=codeinfo['separator'], quotechar=codeinfo['quote'])
        code_mappings = {row[plot_codes_key].strip(): row[data_codes_key].strip() for row in reader}

    return code_mappings










def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Reconcile countries by their codes.

    Args:
        codeinfo (dict): A country code information dictionary.
        plot_countries (dict): Dictionary of plot library country codes and corresponding names.
        gdp_countries (dict): Dictionary of country codes used in GDP data.

    Returns:
        tuple: A tuple containing a dictionary and a set.
            The dictionary maps country codes from plot_countries to country codes from gdp_countries.
            The set contains the country codes from plot_countries that did not have a country with a corresponding
            code in gdp_countries.
    """
    # Load country code mappings from CSV file
    codefile = codeinfo['codefile']
    plot_codes_key = codeinfo['plot_codes']
    data_codes_key = codeinfo['data_codes']


    with open(codefile, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=codeinfo['separator'], quotechar=codeinfo['quote'])
        code_mappings = {row[plot_codes_key].strip().lower(): row[data_codes_key].strip() for row in reader}

# Convert country codes to lowercase for case-insensitive comparison
    plot_countries_lower = {code.lower(): code for code in plot_countries}
    gdp_countries_lower = {code.lower(): code for code in gdp_countries}

    # Initialize the result dictionary and set
    result_dict = {}
    unmatched_set = set()


    # Iterate over each plot country code
    for plot_code, country_name in plot_countries.items():
        plot_code_lower = plot_code.lower()

        # Check if plot country code is in GDP data
        if plot_code_lower in gdp_countries_lower:
            # Map the plot country code to GDP country code
            result_dict[plot_countries_lower[plot_code_lower]] = gdp_countries_lower[plot_code_lower]
        else:
            # Check if plot country code is in code mappings
            if plot_code_lower in code_mappings:
                gdp_code = code_mappings[plot_code_lower]
                if gdp_code.lower() in gdp_countries_lower:
                    result_dict[plot_countries_lower[plot_code_lower]] = gdp_countries_lower[gdp_code.lower()]
                else:
                    unmatched_set.add(plot_code)
            else:
                # Add to unmatched set if not found in GDP data or code mappings
                unmatched_set.add(plot_code)

    return result_dict, unmatched_set
#############################################
def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    plot_dict ={}
    plot_dict_1 ={}
    plot_set_1 = set()
    plot_set_2 = set()
    new_data_dict = {}
    
    with open(gdpinfo['gdpfile'], 'r') as data_file:
        data = csv.DictReader(data_file, delimiter=gdpinfo['separator']
                                        ,quotechar = gdpinfo['quote'])
        for row in data:
            new_data_dict[row[gdpinfo['country_code']]] = row
    
    plot_dict, plot_set_1 = reconcile_countries_by_code(codeinfo,plot_countries, new_data_dict)
    
    plot_set_1.clear()
    val = ""
    for key,value in plot_countries.items():
        for codekey,codeval in plot_dict.items():
            if key in plot_dict:
                if key.lower() ==  codekey.lower():
                    val = codeval
                else:
                    val = ""
            else:
                plot_set_1.add(key)
        if val!="" and val not in new_data_dict:
            plot_set_1.add(key)
        
     
    for key,value in plot_dict.items():
        for key1,val1 in new_data_dict.items():
            if value.lower() == key1.lower():
                if val1[year]!='':
                    plot_dict_1[key] = math.log(float(val1[year]),10)
                else:
                    plot_set_2.add(key)

    return plot_dict_1, set(plot_set_1), set(plot_set_2)