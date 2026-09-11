import re
import json

# this line is to be able to read the raw text
with open("input/raw-text.txt", "r") as file:
    text = file.read()

# these are the REGEX patterns

# this is for the normal email address
email_pattern = r"\b[\w\.-]+@[\w\.-]+\.\w+\b"

# This is for the official ALU email
alu_email = r"\b[\w\.-]+@alueducation\.com\b"

# Alumni email
alu_alumni = r"\b[\w\.-]+@alumni\.alueducation\.com\b"

# SI email
si_email = r"\b[\w\.-]+@si\.alueducation\.com\b"

# url
url_pattern = r"https?://[^\s]+"

# credit card
# this one will accept spaces as credit card numbers are designed like that
# even with hyphens at times depending on the page so we consider both
credit_card = r"\b(?:\d{4}[-\s]){3}\d{4}\b"

# Phone number
phone_pattern = r"(?:\+\d{3}\s?)?\d{3}[-.\s]\d{3}[-.\s]\d{3}"

# INPUT VALIDATION
# here we will be checking if that thing is actually what it claims to be
def validate_input(text):

    # This line will reject empty input
    if not text.strip():
        return False

    return True

# Remove obvious unsafe content before extraction
unsafe_content = False

if re.search(r"<script.*?>.*?</script>", text, re.IGNORECASE | re.DOTALL):
    unsafe_content = True
    text = re.sub(
        r"<script.*?>.*?</script>",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

if re.search(r"javascript:", text, re.IGNORECASE):
    unsafe_content = True
    text = re.sub(
        r"javascript:\S+",
        "",
        text,
        flags=re.IGNORECASE
    )

# Extraction
# it runs the program's regex against raw text and pulls out any matches.
if validate_input(text):

    emails = re.findall(email_pattern, text)
    alu_emails = re.findall(alu_email, text)
    alumni_emails = re.findall(alu_alumni, text)
    si_emails = re.findall(si_alumni, text) if False else re.findall(si_email, text)
    urls = re.findall(url_pattern, text)
    credit_cards = re.findall(credit_card, text)
    phone_numbers = re.findall(phone_pattern, text)

    # Masking Credit card numbers
    masked_credit_cards = []

    for card in credit_cards:

        # Remove spaces and hyphens for validation
        digits = re.sub(r"[-\s]", "", card)

        # masking the credit card number by replacing all but the last 4 digits with asterisks
        masked_credit_cards.append(
            "**** **** **** " + digits[-4:]
        )

    # create results
    results = {
        "emails": emails,
        "alu_emails": alu_emails,
        "alumni_emails": alumni_emails,
        "si_emails": si_emails,
        "urls": urls,
        "credit_cards": masked_credit_cards,
        "phone_numbers": phone_numbers
    }

    # Save results to a JSON file
    with open("output/sample-output.json", "w") as file:
        json.dump(
            results,
            file,
            indent=4
        )

    # Display results
    if unsafe_content:
        print("Unsafe content detected and ignored.")

    print("Data extracted successfully.")
    print(
        json.dumps(
            results,
            indent=4
        )
    )

else:
    print(
        "invalid or unsafe input."
    )