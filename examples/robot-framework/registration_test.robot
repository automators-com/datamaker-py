*** Settings ***
Library    Browser
Library    DataMakerLibrary.py

*** Variables ***
${BROWSER}    chromium
${URL}        http://example.com/register

*** Test Cases ***
Register New User
    ${user_data}=    Generate User Data
    New Browser    browser=${BROWSER}    headless=False
    New Page    ${URL}
    Fill Registration Form    ${user_data}
    Submit Registration
    Registration Should Be Successful    ${user_data}
    [Teardown]    Close Browser

*** Keywords ***
Generate User Data
    ${template}=    Create Template
    ${result}=    Generate Data    ${template}
    RETURN    ${result}[0]

Fill Registration Form
    [Arguments]    ${user_data}
    Fill Text    id=first-name    ${user_data}[first_name]
    Fill Text    id=last-name    ${user_data}[last_name]
    Fill Text    id=email    ${user_data}[email]

Submit Registration
    Click    id=submit-button

Registration Should Be Successful
    [Arguments]    ${user_data}
    Get Text    id=confirmation-message    ==    Registration Successful
    Get Text    id=welcome-message    contains    Welcome, ${user_data}[first_name] ${user_data}[last_name]!
