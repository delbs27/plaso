# -*- coding: utf-8 -*-
"""Language tags helper.

For a list of language tags see:
  https://datatracker.ietf.org/doc/html/rfc5646
"""


class LanguageTagHelper(object):
  """Language tags helper."""

  _LANGUAGE_PER_TAG = {
      'af': 'Afrikaans',
      'af-ZA': 'Afrikaans, South Africa',
      'am': 'Amharic',
      'am-ET': 'Amharic, Ethiopia',
      'ar': 'Arabic',
      'ar-AE': 'Arabic, United Arab Emirates',
      'ar-BH': 'Arabic, Bahrain',
      'ar-DZ': 'Arabic, Algeria',
      'ar-EG': 'Arabic, Egypt',
      'ar-IQ': 'Arabic, Iraq',
      'ar-JO': 'Arabic, Jordan',
      'ar-KW': 'Arabic, Kuwait',
      'ar-LB': 'Arabic, Lebanon',
      'ar-LY': 'Arabic, Libyan Arab Jamahiriya',
      'ar-MA': 'Arabic, Morocco',
      'arn': 'Mapudungun',
      'arn-CL': 'Mapudungun, Chile',
      'ar-OM': 'Arabic, Oman',
      'ar-QA': 'Arabic, Qatar',
      'ar-SA': 'Arabic, Saudi Arabia',
      'ar-SY': 'Arabic, Syrian Arab Republic',
      'ar-TN': 'Arabic, Tunisia',
      'ar-YE': 'Arabic, Yemen',
      'as': 'Assamese',
      'as-IN': 'Assamese, India',
      'az': 'Azerbaijani',
      'az-Cyrl': 'Azerbaijani, Cyrillic',
      'az-Cyrl-AZ': 'Azerbaijani, Cyrillic, Azerbaijan',
      'az-Latn': 'Azerbaijani, Latin',
      'az-Latn-AZ': 'Azerbaijani, Latin, Azerbaijan',
      'ba': 'Bashkir',
      'ba-RU': 'Bashkir, Russian Federation',
      'be': 'Belarusian',
      'be-BY': 'Belarusian, Belarus',
      'bg': 'Bulgarian',
      'bg-BG': 'Bulgarian, Bulgaria',
      'bin-NG': 'Bini, Nigeria',
      'bn': 'Bengali',
      'bn-BD': 'Bengali, Bangladesh',
      'bn-IN': 'Bengali, India',
      'bo': 'Tibetan',
      'bo-BT': 'Tibetan, Bhutan',
      'bo-CN': 'Tibetan, China',
      'br': 'Breton',
      'br-FR': 'Breton, France',
      'bs': 'Bosnian',
      'bs-Cyrl': 'Bosnian, Cyrillic',
      'bs-Cyrl-BA': 'Bosnian, Cyrillic, Bosnia and Herzegovina',
      'bs-Latn': 'Bosnian, Latin',
      'bs-Latn-BA': 'Bosnian, Latin, Bosnia and Herzegovina',
      'ca': 'Catalan',
      'ca-ES': 'Catalan, Spain',
      'chr-US': 'Cherokee, United States',
      'co': 'Corsican',
      'co-FR': 'Corsican, France',
      'cs': 'Czech',
      'cs-CZ': 'Czech, Czech Republic',
      'cy': 'Welsh',
      'cy-GB': 'Welsh, United Kingdom',
      'da': 'Danish',
      'da-DK': 'Danish, Denmark',
      'de': 'German',
      'de-AT': 'German, Austria',
      'de-CH': 'German, Switzerland',
      'de-DE': 'German, Germany',
      'de-LI': 'German, Liechtenstein',
      'de-LU': 'German, Luxembourg',
      'dsb': 'Lower Sorbian',
      'dsb-DE': 'Lower Sorbian, Germany',
      'dv': 'Dhivehi',
      'dv-MV': 'Dhivehi, Maldives',
      'el': 'Modern Greek (1453 and later)',
      'el-GR': 'Modern Greek (1453-), Greece',
      'en': 'English',
      'en-AU': 'English, Australia',
      'en-BZ': 'English, Belize',
      'en-CA': 'English, Canada',
      'en-CB': 'English',
      'en-GB': 'English, United Kingdom',
      'en-HK': 'English, Hong Kong',
      'en-ID': 'English, Indonesia',
      'en-IE': 'English, Ireland',
      'en-IN': 'English, India',
      'en-JM': 'English, Jamaica',
      'en-MY': 'English, Malaysia',
      'en-NZ': 'English, New Zealand',
      'en-PH': 'English, Philippines',
      'en-SG': 'English, Singapore',
      'en-TT': 'English, Trinidad and Tobago',
      'en-US': 'English, United States',
      'en-ZA': 'English, South Africa',
      'en-ZW': 'English, Zimbabwe',
      'es': 'Spanish',
      'es-AR': 'Spanish, Argentina',
      'es-BO': 'Spanish, Bolivia',
      'es-CL': 'Spanish, Chile',
      'es-CO': 'Spanish, Colombia',
      'es-CR': 'Spanish, Costa Rica',
      'es-DO': 'Spanish, Dominican Republic',
      'es-EC': 'Spanish, Ecuador',
      'es-ES': 'Spanish, Spain',
      'es-ES_tradnl': 'Spanish',
      'es-GT': 'Spanish, Guatemala',
      'es-HN': 'Spanish, Honduras',
      'es-MX': 'Spanish, Mexico',
      'es-NI': 'Spanish, Nicaragua',
      'es-PA': 'Spanish, Panama',
      'es-PE': 'Spanish, Peru',
      'es-PR': 'Spanish, Puerto Rico',
      'es-PY': 'Spanish, Paraguay',
      'es-SV': 'Spanish, El Salvador',
      'es-US': 'Spanish, United States',
      'es-UY': 'Spanish, Uruguay',
      'es-VE': 'Spanish, Venezuela',
      'et': 'Estonian',
      'et-EE': 'Estonian, Estonia',
      'eu': 'Basque',
      'eu-ES': 'Basque, Spain',
      'fa': 'Persian',
      'fa-IR': 'Persian, Islamic Republic of Iran',
      'fi': 'Finnish',
      'fi-FI': 'Finnish, Finland',
      'fil': 'Filipino',
      'fil-PH': 'Filipino, Philippines',
      'fo': 'Faroese',
      'fo-FO': 'Faroese, Faroe Islands',
      'fr': 'French',
      'fr-BE': 'French, Belgium',
      'fr-CA': 'French, Canada',
      'fr-CG': 'French, Congo',
      'fr-CH': 'French, Switzerland',
      'fr-CI': 'French, Côte d\'Ivoire',
      'fr-CM': 'French, Cameroon',
      'fr-FR': 'French, France',
      'fr-HT': 'French, Haiti',
      'fr-LU': 'French, Luxembourg',
      'fr-MA': 'French, Morocco',
      'fr-MC': 'French, Monaco',
      'fr-ML': 'French, Mali',
      'fr-RE': 'French, Réunion',
      'fr-SN': 'French, Senegal',
      'fr-West': 'French',
      'fuv-NG': 'Nigerian Fulfulde, Nigeria',
      'fy': 'Western Frisian',
      'fy-NL': 'Western Frisian, Netherlands',
      'ga': 'Irish',
      'ga-IE': 'Irish, Ireland',
      'gaz-ET': 'West Central Oromo, Ethiopia',
      'gd': 'Scottish Gaelic',
      'gd-GB': 'Scottish Gaelic, United Kingdom',
      'gl': 'Galician',
      'gl-ES': 'Galician, Spain',
      'gn-PY': 'Guarani, Paraguay',
      'gsw': 'Swiss German',
      'gsw-FR': 'Swiss German, France',
      'gu': 'Gujarati',
      'gu-IN': 'Gujarati, India',
      'ha': 'Hausa',
      'ha-Latn': 'Hausa, Latin',
      'ha-Latn-NG': 'Hausa, Latin, Nigeria',
      'haw-US': 'Hawaiian, United States',
      'he': 'Hebrew',
      'he-IL': 'Hebrew, Israel',
      'hi': 'Hindi',
      'hi-IN': 'Hindi, India',
      'hr': 'Croatian',
      'hr-BA': 'Croatian, Bosnia and Herzegovina',
      'hr-HR': 'Croatian, Croatia',
      'hsb': 'Upper Sorbian',
      'hu': 'Hungarian',
      'hu-HU': 'Hungarian, Hungary',
      'hy': 'Armenian',
      'hy-AM': 'Armenian, Armenia',
      'ibb-NG': 'Ibibio, Nigeria',
      'id': 'Indonesian',
      'id-ID': 'Indonesian, Indonesia',
      'ig': 'Igbo',
      'ig-NG': 'Igbo, Nigeria',
      'ii': 'Sichuan Yi',
      'ii-CN': 'Sichuan Yi, China',
      'is': 'Icelandic',
      'is-IS': 'Icelandic, Iceland',
      'it': 'Italian',
      'it-CH': 'Italian, Switzerland',
      'it-IT': 'Italian, Italy',
      'iu': 'Inuktitut',
      'iu-Cans': 'Inuktitut, Unified Canadian Aboriginal Syllabics',
      'iu-Cans-CA': 'Inuktitut, Unified Canadian Aboriginal Syllabics, Canada',
      'iu-Latn': 'Inuktitut, Latin',
      'iu-Latn-CA': 'Inuktitut, Latin, Canada',
      'ja': 'Japanese',
      'ja-JP': 'Japanese, Japan',
      'ka': 'Georgian',
      'ka-GE': 'Georgian, Georgia',
      'kk': 'Kazakh',
      'kk-KZ': 'Kazakh, Kazakhstan',
      'kl': 'Kalaallisut',
      'kl-GL': 'Kalaallisut, Greenland',
      'km': 'Central Khmer',
      'km-KH': 'Central Khmer, Cambodia',
      'kn': 'Kannada',
      'kn-IN': 'Kannada, India',
      'ko': 'Korean',
      'kok': 'Konkani (macrolanguage)',
      'kok-IN': 'Konkani (macrolanguage), India',
      'ko-KR': 'Korean, Republic of Korea',
      'kr-NG': 'Kanuri, Nigeria',
      'ky': 'Kirghiz',
      'ky-KG': 'Kirghiz, Kyrgyzstan',
      'lb': 'Luxembourgish',
      'lb-LU': 'Luxembourgish, Luxembourg',
      'lo': 'Lao',
      'lo-LA': 'Lao, Lao People\'s Democratic Republic',
      'lt': 'Lithuanian',
      'lt-LT': 'Lithuanian, Lithuania',
      'lv': 'Latvian',
      'lv-LV': 'Latvian, Latvia',
      'mi': 'Maori',
      'mi-NZ': 'Maori, New Zealand',
      'mk': 'Macedonian',
      'mk-MK': 'Macedonian, The Former Yugoslav Republic of Macedonia',
      'ml': 'Malayalam',
      'ml-IN': 'Malayalam, India',
      'mn': 'Mongolian',
      'mn-Cyrl': 'Mongolian, Cyrillic',
      'mni': 'Manipuri',
      'mn-MN': 'Mongolian, Mongolia',
      'mn-Mong': 'Mongolian, Mongolian',
      'mn-Mong-CN': 'Mongolian, Mongolian, China',
      'moh': 'Mohawk',
      'moh-CA': 'Mohawk, Canada',
      'mr': 'Marathi',
      'mr-IN': 'Marathi, India',
      'ms': 'Malay (macrolanguage)',
      'ms-BN': 'Malay (macrolanguage), Brunei Darussalam',
      'ms-MY': 'Malay (macrolanguage), Malaysia',
      'mt': 'Maltese',
      'mt-MT': 'Maltese, Malta',
      'my-MM': 'Burmese, Myanmar',
      'nb': 'Norwegian Bokmål',
      'nb-NO': 'Norwegian Bokmål, Norway',
      'ne': 'Nepali',
      'ne-IN': 'Nepali, India',
      'ne-NP': 'Nepali, Nepal',
      'nl': 'Dutch',
      'nl-BE': 'Dutch, Belgium',
      'nl-NL': 'Dutch, Netherlands',
      'nn': 'Norwegian Nynorsk',
      'nn-NO': 'Norwegian Nynorsk, Norway',
      'no': 'Norwegian',
      'nso': 'Pedi',
      'nso-ZA': 'Pedi, South Africa',
      'oc': 'Occitan (post 1500)',
      'oc-FR': 'Occitan (post 1500), France',
      'or': 'Oriya',
      'or-IN': 'Oriya, India',
      'pa': 'Panjabi',
      'pa-IN': 'Panjabi, India',
      'pap-AN': 'Papiamento, Netherlands Antilles',
      'pa-PK': 'Panjabi, Pakistan',
      'pl': 'Polish',
      'pl-PL': 'Polish, Poland',
      'plt-MG': 'Plateau Malagasy, Madagascar',
      'prs': 'Dari',
      'prs-AF': 'Dari, Afghanistan',
      'ps': 'Pushto',
      'ps-AF': 'Pushto, Afghanistan',
      'pt': 'Portuguese',
      'pt-BR': 'Portuguese, Brazil',
      'pt-PT': 'Portuguese, Portugal',
      'qut': 'Guatemala',
      'qut-GT': 'Guatemala',
      'quz': 'Cusco Quechua',
      'quz-BO': 'Cusco Quechua, Bolivia',
      'quz-EC': 'Cusco Quechua, Ecuador',
      'quz-PE': 'Cusco Quechua, Peru',
      'rm': 'Romansh',
      'rm-CH': 'Romansh, Switzerland',
      'ro': 'Romanian',
      'ro-MO': 'Romanian, Macao',
      'ro-RO': 'Romanian, Romania',
      'ru': 'Russian',
      'ru-MO': 'Russian, Macao',
      'ru-RU': 'Russian, Russian Federation',
      'rw': 'Kinyarwanda',
      'rw-RW': 'Kinyarwanda, Rwanda',
      'sa': 'Sanskrit',
      'sah': 'Yakut',
      'sah-RU': 'Yakut, Russian Federation',
      'sa-IN': 'Sanskrit, India',
      'sd-IN': 'Sindhi, India',
      'sd-PK': 'Sindhi, Pakistan',
      'se': 'Northern Sami',
      'se-FI': 'Northern Sami, Finland',
      'se-NO': 'Northern Sami, Norway',
      'se-SE': 'Northern Sami, Sweden',
      'si': 'Sinhala',
      'si-LK': 'Sinhala, Sri Lanka',
      'sk': 'Slovak',
      'sk-SK': 'Slovak, Slovakia',
      'sl': 'Slovenian',
      'sl-SI': 'Slovenian, Slovenia',
      'sma': 'Southern Sami',
      'sma-NO': 'Southern Sami, Norway',
      'sma-SE': 'Southern Sami, Sweden',
      'smj': 'Lule Sami',
      'smj-NO': 'Lule Sami, Norway',
      'smj-SE': 'Lule Sami, Sweden',
      'smn': 'Inari Sami',
      'smn-FI': 'Inari Sami, Finland',
      'sms': 'Skolt Sami',
      'sms-FI': 'Skolt Sami, Finland',
      'so-SO': 'Somali, Somalia',
      'sq': 'Albanian',
      'sq-AL': 'Albanian, Albania',
      'sr': 'Serbian',
      'sr-Cyrl': 'Serbian, Cyrillic',
      'sr-Cyrl-BA': 'Serbian, Cyrillic, Bosnia and Herzegovina',
      'sr-Cyrl-CS': 'Serbian, Cyrillic, Serbia and Montenegro',
      'sr-Cyrl-ME': 'Serbian, Cyrillic, Montenegro',
      'sr-Cyrl-RS': 'Serbian, Cyrillic, Serbia',
      'sr-Latn': 'Serbian, Latin',
      'sr-Latn-BA': 'Serbian, Latin, Bosnia and Herzegovina',
      'sr-Latn-CS': 'Serbian, Latin, Serbia and Montenegro',
      'sr-Latn-ME': 'Serbian, Latin, Montenegro',
      'sr-Latn-RS': 'Serbian, Latin, Serbia',
      'st-ZA': 'Southern Sotho, South Africa',
      'sv': 'Swedish',
      'sv-FI': 'Swedish, Finland',
      'sv-SE': 'Swedish, Sweden',
      'sw': 'Swahili (macrolanguage)',
      'sw-KE': 'Swahili (macrolanguage), Kenya',
      'syr': 'Syriac',
      'syr-SY': 'Syriac, Syrian Arab Republic',
      'ta': 'Tamil',
      'ta-IN': 'Tamil, India',
      'te': 'Telugu',
      'te-IN': 'Telugu, India',
      'tg': 'Tajik',
      'tg-Cyrl': 'Tajik, Cyrillic',
      'tg-Cyrl-TJ': 'Tajik, Cyrillic, Tajikistan',
      'th': 'Thai',
      'th-TH': 'Thai, Thailand',
      'ti-ER': 'Tigrinya, Eritrea',
      'ti-ET': 'Tigrinya, Ethiopia',
      'tk': 'Turkmen',
      'tk-TM': 'Turkmen, Turkmenistan',
      'tmz': 'Tamanaku',
      'tmz-MA': 'Tamanaku, Morocco',
      'tn': 'Tswana',
      'tn-ZA': 'Tswana, South Africa',
      'tr': 'Turkish',
      'tr-TR': 'Turkish, Turkey',
      'ts-ZA': 'Tsonga, South Africa',
      'tt': 'Tatar',
      'tt-RU': 'Tatar, Russian Federation',
      'tzm': 'Central Atlas Tamazight',
      'tzm-Latn': 'Central Atlas Tamazight, Latin',
      'tzm-Latn-DZ': 'Central Atlas Tamazight, Latin, Algeria',
      'ug': 'Uighur',
      'ug-CN': 'Uighur, China',
      'uk': 'Ukrainian',
      'uk-UA': 'Ukrainian, Ukraine',
      'ur': 'Urdu',
      'ur-IN': 'Urdu, India',
      'ur-PK': 'Urdu, Pakistan',
      'uz': 'Uzbek',
      'uz-Cyrl': 'Uzbek, Cyrillic',
      'uz-Cyrl-UZ': 'Uzbek, Cyrillic, Uzbekistan',
      'uz-Latn': 'Uzbek, Latin',
      'uz-Latn-UZ': 'Uzbek, Latin, Uzbekistan',
      'ven-ZA': 'South Africa',
      'vi': 'Vietnamese',
      'vi-VN': 'Vietnamese, Viet Nam',
      'wen-DE': 'Sorbian languages, Germany',
      'wo': 'Wolof',
      'wo-SN': 'Wolof, Senegal',
      'xh': 'Xhosa',
      'xh-ZA': 'Xhosa, South Africa',
      'yo': 'Yoruba',
      'yo-NG': 'Yoruba, Nigeria',
      'zh': 'Chinese',
      'zh-CN': 'Chinese, China',
      'zh-Hans': 'Chinese, Han (Simplified variant)',
      'zh-Hant': 'Chinese, Han (Traditional variant)',
      'zh-HK': 'Chinese, Hong Kong',
      'zh-MO': 'Chinese, Macao',
      'zh-SG': 'Chinese, Singapore',
      'zh-TW': 'Chinese, Taiwan, Province of China',
      'zu': 'Zulu',
      'zu-ZA': 'Zulu, South Africa'}

  @classmethod
  def GetLanguages(cls):
    """Retrieveve the language tags with their description.

    Returns:
      tuple[str, str]: lanugage tag and description.
    """
    return sorted(cls._LANGUAGE_PER_TAG.items())

  @classmethod
  def IsLanguageTag(cls, string):
    """Detemines if a string contains a valid language tag.

    Args:
      string (str): a string.

    Returns:
      bool: True if the string contains a language tag.
    """
    return string in cls._LANGUAGE_PER_TAG