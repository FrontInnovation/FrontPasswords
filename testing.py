import sqlite3
from supporting_functions import *
from difflib import get_close_matches



# Gets companyname based on similar input companyname from app.db
def get_company_name_by_similar_name(companyname):
    """
    Retrieves company name based on similar input company name from the app.db database.

    :param companyname: The name of the company to retrieve data for.
    :return: A string containing the company name found in the database, or None if the company is not found.
    """
    try:
        companyname = format_company_identifier(companyname)
        # Connect to the SQLite database
        conn = sqlite3.connect('databases/app.db')
        c = conn.cursor()
        # Execute a SELECT query to find the accounts data for the specified company
        c.execute("SELECT companyname FROM company_info")
        rows = c.fetchall()
        
        # Extract company names from fetched rows
        company_names = [row[0] for row in rows]

        # Check if the exact company name is present in the database
        if companyname in company_names:
            return companyname
        else:
            # Find the most similar company name
            similar_names = get_close_matches(companyname, company_names, n=1, cutoff=0.75)
            if similar_names:
                return similar_names[0]  # Return the first (most similar) name from the list
            else:
                print("Company not found.")
                return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    print(get_company_name_by_similar_name("Scalemem"))
