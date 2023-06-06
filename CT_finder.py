import streamlit as st
import requests
import json
import pandas as pd

def get_clinical_trials(disease: str, country: str, state: str = None, status: str = None):
    base_url = 'https://clinicaltrials.gov/api/query/study_fields?expr='
    fields = '&fields=NCTId,BriefTitle,OverallStatus,Condition,InterventionName,LocationFacility,LocationCity,LocationState,LocationZip,LocationCountry'
    url = base_url + disease + fields + '&min_rnk=1&max_rnk=100&fmt=json'
    response = requests.get(url)
    data = response.json()

    trials = []
    for study in data['StudyFieldsResponse']['StudyFields']:
        trial = {}
        trial['NCTId'] = study.get('NCTId', [None])[0]
        trial['BriefTitle'] = study.get('BriefTitle', [None])[0]
        trial['OverallStatus'] = study.get('OverallStatus', [None])[0]
        trial['Condition'] = ', '.join(study.get('Condition', []))
        trial['InterventionName'] = ', '.join(study.get('InterventionName', []))

        # Extracting location details
        trial['LocationFacility'] = ', '.join(study.get('LocationFacility', []))
        trial['LocationCity'] = ', '.join(study.get('LocationCity', []))
        trial['LocationState'] = ', '.join(study.get('LocationState', []))
        trial['LocationZip'] = ', '.join(study.get('LocationZip', []))
        trial['LocationCountry'] = ', '.join(study.get('LocationCountry', []))

        trials.append(trial)

    return trials

def main():
    st.title("Clinical TrialsBot")

    disease = st.text_input("Enter the disease or condition: ")
    country = st.text_input("Enter the country: ")
    state = None
    if country.lower() == 'united states':
        state = st.text_input("Enter the state: ")
    status = st.selectbox("Select the status of the trial: ", ["", "Not yet recruiting", "Recruiting", "Enrolling by invitation", "Active, not recruiting", "Suspended", "Terminated", "Completed", "Withdrawn", "Unknown"])

    if st.button("Search Clinical Trials"):
        if disease and country:
            trials = get_clinical_trials(disease, country, state, status)

            if not trials:
                st.write("No trials found")
            else:
                st.dataframe(pd.DataFrame(trials))  # Display results in a table format
        else:
            st.write("Please enter both disease and country.")

if __name__ == "__main__":
    main()
