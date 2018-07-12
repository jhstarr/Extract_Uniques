# Jeff Starr, 3 July, 2018
# This is a program that takes two input csv files and returns two output 
# files.  
# One input file contains a list of target companies.  One input file
# contains a list of contacts at companies.  One output file contains a list of
# all contacts who work at companies that appear to match companies
# in the list of target companies.  The other output file lists the companies
# in the target list for which contacts were found.
# The challenge comes in matching company
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
    contacts_matrix_noblanks = []
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

# Pop off the top row of each input containing the text tile row.

    target_company_list.pop(0)
    contacts_matrix.pop(0)

    print("Number of target accounts: ", len(target_company_list))
    print("Number of contacts in database: ", len(contacts_matrix))


# Insert a cleansed version of the company name in each row in the company
# data and in the contact data.

# Insert a cleansed company field in the target company list data.

    for row_companies in target_company_list:
        row_companies.insert(
            COMPANYNAME_OF_COMPANIES_CLEANSED,
            row_companies[COMPANYNAME_OF_COMPANIES])

# Clean company control names like "Inc.," "Incorporated," etc.

    for row_companies in target_company_list:
        row_companies[COMPANYNAME_OF_COMPANIES_CLEANSED]=cleanco(
            row_companies[COMPANYNAME_OF_COMPANIES_CLEANSED]
            ).clean_name()

# Remove punctuation

        row_companies[
            COMPANYNAME_OF_COMPANIES_CLEANSED
            ] = regex.sub(
                r"[[:punct:]]+", "", row_companies[
                    COMPANYNAME_OF_COMPANIES_CLEANSED
                    ]
                )

# Make lower case and handle certain foreign language capitalization
# conventions with casefold().

        row_companies[
            COMPANYNAME_OF_COMPANIES_CLEANSED
            ] = row_companies[
                    COMPANYNAME_OF_COMPANIES_CLEANSED
                    ].casefold()

        row_companies[COMPANYNAME_OF_COMPANIES_CLEANSED] = nltk.word_tokenize(
            row_companies[COMPANYNAME_OF_COMPANIES_CLEANSED])
        
        row_companies[COMPANYNAME_OF_COMPANIES_CLEANSED] = [
            t for t in row_companies[
                COMPANYNAME_OF_COMPANIES_CLEANSED
                ] if t not in stopwords.words('english')
            ]

# Get rid of all contacts without a company using list comprehension.

    contacts_matrix_noblanks = [
        row for row in contacts_matrix if (
            row[COMPANY_OF_CONTACT] != ""
            )
        ]

# Now cleanse the contact company names.

    for row_contacts in contacts_matrix_noblanks:
        row_contacts.insert(
            COMPANY_OF_CONTACT_CLEANSED,
            row_contacts[COMPANY_OF_CONTACT])

    for row_contacts in contacts_matrix_noblanks:
        row_contacts[COMPANY_OF_CONTACT_CLEANSED]=cleanco(
            row_contacts[COMPANY_OF_CONTACT_CLEANSED]).clean_name()

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
   
        row_contacts[COMPANY_OF_CONTACT_CLEANSED] = nltk.word_tokenize(
            row_contacts[COMPANY_OF_CONTACT_CLEANSED])
        
        row_contacts[COMPANY_OF_CONTACT_CLEANSED] = [
            t for t in row_contacts[COMPANY_OF_CONTACT_CLEANSED]
                if t not in stopwords.words('english')
            ]

# Walk through the companies list.  For each company, go through companies
# of contacts (in the noblanks matrix) and find matches or approximate
# matches where 

    for row_companies in target_company_list:
        any_contacts_at_company = False
        c = row_companies[COMPANYNAME_OF_COMPANIES_CLEANSED]
        for row_contacts in contacts_matrix_noblanks:
            coc = row_contacts[COMPANY_OF_CONTACT_CLEANSED]
            if c == coc or (set(coc)< set(c)) or (set(c)< set(coc)):
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