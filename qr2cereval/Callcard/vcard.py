def create_VCard(name, phone, email, phone2=None, email2=None ,company=None):
    VCard = f"""
BEGIN:VCARD
VERSION:3.0
N:{name}
TEL:{phone}
EMAIL:{email}
"""
    if phone2:
        VCard += f"TEL:{phone2}\n"
    if email2:
        VCard += f"EMAIL:{email2}\n"
    if company:
        VCard += f"ORG:{company}\n"
    VCard += "END:VCARD\n"
    return VCard
