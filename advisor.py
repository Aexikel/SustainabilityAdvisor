# advisor.py

sustainability_db = {
    'Aluminium foil': {
        'advice': 'Clean off food residue before recycling. Scrunch it into a ball—if it stays scrunched, it is recyclable.',
        'rri_score': 50,
        'category': 'Metal'
    },
    'Bottle cap': {
        'advice': 'Leave plastic caps ON the plastic bottle before recycling so they do not fall through the sorting grates.',
        'rri_score': 10,
        'category': 'Plastic'
    },
    'Bottle': {
        'advice': 'Empty liquids completely. Do not crush if your local facility uses optical scanners.',
        'rri_score': 80,
        'category': 'Plastic/Glass'
    },
    'Broken glass': {
        'advice': 'DANGER: Do NOT put in recycling. Wrap in newspaper and place in general waste to protect sanitation workers.',
        'rri_score': 0,
        'category': 'Hazardous/Waste'
    },
    'Can': {
        'advice': 'Highly recyclable! Rinse lightly. Recovering this metal yields a massive RRI score.',
        'rri_score': 150,
        'category': 'Metal'
    },
    'Carton': {
        'advice': 'Empty and replace the cap. Most milk/juice cartons are recyclable, but check local guidelines for multi-layer cartons.',
        'rri_score': 40,
        'category': 'Paper/Mixed'
    },
    'Cigarette': {
        'advice': 'Not recyclable and highly toxic. Dispose of in a dedicated ash receptacle or general waste.',
        'rri_score': 0,
        'category': 'Waste'
    },
    'Cup': {
        'advice': 'Paper coffee cups usually have a plastic lining and are NOT recyclable in standard bins. Dispose in general waste.',
        'rri_score': 0,
        'category': 'Waste'
    },
    'Lid': {
        'advice': 'Plastic cup lids are often recyclable. Check for a resin code (usually #5 or #1) and local rules.',
        'rri_score': 15,
        'category': 'Plastic'
    },
    'Other litter': {
        'advice': 'Unidentified litter. When in doubt, throw it out (general waste) to prevent contaminating the recycling stream.',
        'rri_score': 0,
        'category': 'Unknown'
    },
    'Other plastic': {
        'advice': 'Check for a recycling triangle. Plastics #1 and #2 have high recovery value. #3 through #7 are facility-dependent.',
        'rri_score': 20,
        'category': 'Plastic'
    },
    'Paper': {
        'advice': 'Keep dry and clean. Do not recycle if heavily soiled with food or grease.',
        'rri_score': 30,
        'category': 'Paper'
    },
    'Plastic bag - wrapper': {
        'advice': 'Do NOT put in curbside bins (they jam sorting machines). Take to a grocery store drop-off bin for recovery.',
        'rri_score': 25,
        'category': 'Soft Plastic'
    },
    'Plastic container': {
        'advice': 'Rinse out food completely. Usually highly recyclable if rigid.',
        'rri_score': 60,
        'category': 'Plastic'
    },
    'Pop tab': {
        'advice': 'Leave attached to the can. If detached, they are too small to survive the sorting process and become waste.',
        'rri_score': 5,
        'category': 'Metal'
    },
    'Straw': {
        'advice': 'Single-use plastic straws are generally NOT recyclable due to their size. Place in general waste.',
        'rri_score': 0,
        'category': 'Waste'
    },
    'Styrofoam piece': {
        'advice': 'Rarely accepted in curbside recycling. Look for specialized EPS drop-off centers, otherwise place in waste.',
        'rri_score': 0,
        'category': 'Waste'
    },
    'Unlabeled litter': {
        'advice': 'Unable to verify material. Place in general waste to avoid contamination.',
        'rri_score': 0,
        'category': 'Unknown'
    }
}