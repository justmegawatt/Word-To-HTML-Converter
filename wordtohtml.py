import worddocumentreader as wdr

NAMESPACE_GROUP = wdr.NAMESPACE + "r"
NAMESPACE_BOLD = wdr.NAMESPACE + "b"
NAMESPACE_ITALICS = wdr.NAMESPACE + "i"
NAMESPACE_UNDERLINE = wdr.NAMESPACE + "u"
NAMESPACE_LINEBREAKS = wdr.NAMESPACE + "br"
NAMESPACE_STRIKE = wdr.NAMESPACE + "strike"

def retrieve_paragraphs(docx_path):
    # This method can be moved to WDR
    xml = wdr.extract_xml_from_word(docx_path)
    return wdr.extract_paragraphs(xml)

def paragraph_text(text):
    return "<p>" + text + "</p>"

def bold_text(text):
    return "<b>" + text + "</b>"

def italicize_text(text):
    return "<i>" + text + "</i>"

def underline_text(text):
    return "<span style='text-decoration: underline;'>" + text + "</span>"

def strike_text(text):
    return "<del>" + text + "</del>"

def is_bold(group):
    # The last 4 lines of all these "IS" methods can be refactored
    bolds = group.iter(NAMESPACE_BOLD)
    is_bold = False
    for bold in bolds:
        is_bold = True
    return is_bold

def is_italics(group):
    italics = group.iter(NAMESPACE_ITALICS)
    is_italic = False
    for italic in italics:
        is_italic = True
    return is_italic

def is_underline(group):
    underlines = group.iter(NAMESPACE_UNDERLINE)
    is_underline = False
    for underline in underlines:
        is_underline = True
    return is_underline

def is_strike(group):
    strikes = group.iter(NAMESPACE_STRIKE)
    is_strike = False
    for strike in strikes:
        is_strike = True
    return is_strike

def needs_linebreak_before(group):
    linebreaks = group.iter(NAMESPACE_LINEBREAKS)
    needs_linebreak = False
    for linebreak in linebreaks:
        needs_linebreak = True
    return needs_linebreak

def grab_text(group):
    return "".join(t.text for t in group.iter(wdr.NS_TEXT))

def change_symbols_to_character_codes(text):
    text = text.replace("&", "&amp;")
    text = text.replace("‘", "&apos;")
    text = text.replace("’", "&apos;")
    text = text.replace(":", "&colon;")
    text = text.replace("–", "&ndash;")
    text = text.replace("“", "&quot;")
    text = text.replace("”", "&quot;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace("…", "...")
    text = text.replace("—", "--")
    return text

def is_blank(text):
    return text == '' or text == '\n'

def save_as_html(html_lines, filename):
    if ".html" not in filename:
        filename += ".html"
    file = open(filename, "w")
    for line in html_lines:
        file.write(line+"\n")
    file.close()

def convert_to_html_lines_from_paragraphs(paragraphs):
    result = []
    for paragraph in paragraphs:
        final_text = ""
        groups = paragraph.iter(NAMESPACE_GROUP)
        for group in groups:
            text = grab_text(group)
            text = change_symbols_to_character_codes(text)

            if is_bold(group):
                text = bold_text(text)
            if is_italics(group):
                text = italicize_text(text)
            if is_underline(group):
                text = underline_text(text)
            if is_strike(group):
                text = strike_text(text)

            if needs_linebreak_before(group):
                final_text += "<br />"
            final_text += text
            #print(final_text)
        if not is_blank(final_text):
            result.append(paragraph_text(final_text))
    return result

def convert_to_html_lines_from_path(docx_path):
    paragraphs = retrieve_paragraphs(docx_path)
    return convert_to_html_lines_from_paragraphs(paragraphs)