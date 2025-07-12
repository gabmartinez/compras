def physical_document_number_validator(document_number: str) -> bool:
    """Check if the document number is a valid Dominican Republic document number."""
    if len(document_number) != 11 or not document_number.isdigit():
        return False

    coefficients = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]

    summary = 0
    for i in range(10):
        digit = int(document_number[i])
        result = digit * coefficients[i]
        if result >= 10:
            summary += (result // 10) + (result % 10)
        else:
            summary += result

    control_digits = (10 - (summary % 10)) % 10
    return control_digits == int(document_number[-1])


def juridical_document_number_validator(document_number: str) -> bool:
    """Check if the RNC is a valid Dominican Republic RNC."""
    if len(document_number) != 9 or not document_number.isdigit():
        return False

    coefficients = [7, 9, 8, 6, 5, 4, 3, 2]
    summary = 0
    for i in range(8):
        digit = int(document_number[i])
        summary += digit * coefficients[i]

    control_digits = (11 - (summary % 11)) % 11
    if control_digits == 10:
        control_digits = 1
    elif control_digits == 11:
        control_digits = 0

    return control_digits == int(document_number[-1])
