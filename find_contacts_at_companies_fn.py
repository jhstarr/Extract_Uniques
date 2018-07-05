# Jeff Starr, 3 July, 2018
# This is a program that takes two input csv files and returns an output file.
# One input file contains a list of target companies.  One input file
# contains a list of human contacts.  The output file contains a list of
# all contacts who work at companies that appear to match companies
# in the list of target companies.  The challenge comes in matching company
# names like "Disney" and "The Walt Disney Company" or "Chevron USA" and
# "Chevron", catching punctuation differences, etc.

import csv
import regex
import nltk
from nltk.corpus import stopwords
from cleanco import cleanco


def find_contacts_at_companies(input_companies_fname, input_contacts_fname):


# Initialize lists
    target_company_list = []
    contacts_matrix = []
    contacts_at_companies_matrix = []
    any_contacts_at_company = False
    contact_match_count = 0
    companies_with_matches = []


# Create constants that correspond to field positions.
    
    COMPANYNAME_OF_COMPANIES = 0
    COMPANYNAME_OF_COMPANIES_CLEANSED = 1
    FULLNAME_OF_CONTACT = 0
    EMAIL1_OF_CONTACT = 30
    EMAIL2_OF_CONTACT = 31
    COMPANY_OF_CONTACT = 64
    COMPANY_OF_CONTACT_CLEANSED = 65
    TITLE_OF_CONTACT = 66+1
    DEPARTMENT_OF_CONTACT = 67+1

# Read data into lists from files
    with open(input_companies_fname, encoding='utf-8') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            target_company_list.append(row)
       
    with open(input_contacts_fname, encoding='utf-8') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            contacts_matrix.append(row)

# Pop off the top row of each input.

    target_company_list.pop(0)
    contacts_matrix.pop(0)

# The code below will subtract 1 every time a company has no matching 
# contacts.
    print("Number of target accounts: ", len(target_company_list))


# Insert a cleansed version of the company name in each row in the company
# data and in the contact data.

# Clean company control names

    for row_companies in target_company_list:
        row_companies.insert(
            COMPANYNAME_OF_COMPANIES_CLEANSED,
            cleanco(row_companies[COMPANYNAME_OF_COMPANIES]).clean_name()
            )

# Remove punctuation

        row_companies[
            COMPANYNAME_OF_COMPANIES_CLEANSED
            ] = regex.sub(
                r"[[:punct:]]+", "", row_companies[
                    COMPANYNAME_OF_COMPANIES_CLEANSED
                    ]
                )

# Make lower case and handl certain foreign language capitalization
# conventions.
        row_companies[
            COMPANYNAME_OF_COMPANIES_CLEANSED
            ] = row_companies[
                    COMPANYNAME_OF_COMPANIES_CLEANSED
                    ].casefold()

# Repeat above for company of contact

    for row_contacts in contacts_matrix:
        row_contacts.insert(
            COMPANY_OF_CONTACT_CLEANSED,
            cleanco(row_contacts[COMPANY_OF_CONTACT]).clean_name()
            )

        row_contacts[
            COMPANY_OF_CONTACT_CLEANSED
            ] = regex.sub(
                r"[[:punct:]]+", "", row_contacts[
                COMPANY_OF_CONTACT_CLEANSED
                ]
            )

        row_contacts[
            COMPANY_OF_CONTACT_CLEANSED
            ] = row_contacts[
                COMPANY_OF_CONTACT_CLEANSED
                ].casefold()



# for row_contacts in contacts_matrix:

# Go through target companies and grab relevant fields where company name
# matches.

# Walk through the companies list.  

    for row_companies in target_company_list:
        any_contacts_at_company = False
        c = row_companies[COMPANYNAME_OF_COMPANIES_CLEANSED]
        c_token = nltk.word_tokenize(c)
        c_token = [t for t in c_token if t not in stopwords.words('english')]
        for row_contacts in contacts_matrix:
            coc = row_contacts[COMPANY_OF_CONTACT_CLEANSED]
            if coc != "":
                coc_token = nltk.word_tokenize(coc)
                coc_token = [
                    t for t in coc_token if t not in stopwords.words('english')
                    ]   
                if c == coc or (set(coc_token)< set(c_token)):
                    contacts_at_companies_matrix.append([
                        row_companies[COMPANYNAME_OF_COMPANIES],
                        row_contacts[COMPANY_OF_CONTACT],
                        row_contacts[FULLNAME_OF_CONTACT],
                        row_contacts[TITLE_OF_CONTACT],
                        row_contacts[DEPARTMENT_OF_CONTACT],
                        row_contacts[EMAIL1_OF_CONTACT],
                        row_contacts[EMAIL2_OF_CONTACT]
                        ])
                    any_contacts_at_company = True
                    contact_match_count += 1
                    companies_with_matches.append(
                        row_companies[COMPANYNAME_OF_COMPANIES]
                        )
        if any_contacts_at_company == False:
            contacts_at_companies_matrix.append([
                    row_companies[COMPANYNAME_OF_COMPANIES]])

    contacts_at_companies_matrix.insert(0,[
        "Company Name",
        "Contact Company Name",
        "Contact Full Name",
        "Contact Title",
        "Contact Department",
        "Contact Email1",
        "Contact Email2"
        ])

    companies_with_matches = list(sorted(set(companies_with_matches)))


    print("Number of target accounts with contacts: ", 
        len(companies_with_matches))
    print("Number of contacts found at target accounts: ",contact_match_count)

    return contacts_at_companies_matrix, companies_with_matches