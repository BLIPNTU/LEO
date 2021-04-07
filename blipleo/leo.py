import os
import logging
from pathlib import Path

from pyinkscape import Canvas, PieChart
from pyinkscape.charts import STYLE_REDDOT
from pyinkscape.styles import Style
from pyinkscape.render import prepare_output_dir, svg_to_pdf, merge_pdf
from .charts import SpiderChart


# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------

def getLogger():
    return logging.getLogger(__name__)


# ------------------------------------------------------------------------------
# Styles
# ------------------------------------------------------------------------------
TEMPLATE_DIR = Path(os.path.dirname(__file__)) / 'templates'
PAGE1_TEMPLATE = TEMPLATE_DIR / 'leo_page1.svg'
PAGE2_TEMPLATE = TEMPLATE_DIR / 'leo_page2.svg'
PAGE3_TEMPLATE = TEMPLATE_DIR / 'leo_page3.svg'
PIE_RADIUS = 57
CHART_RADIUS = (57, 57)
PEOPLE_NAME_STYLE = Style(font_size='16px', font_family='D-DINCondensed', font_weight="Bold", fill='#000000', fill_opacity='1', text_anchor="middle", dominant_baseline="hanging")

# ----------------------------------------
# Page 1
P1_BABY_NAME_LOC = (297, 75.69)
P1_BABY_AGE_LOC = (297, 122.1)
P1_BABY_NAME_STYLE = Style(font_size="50px", fill="#232323", font_style="normal", font_variant="normal",
                           font_weight="bold", font_stretch="normal", font_family='D-DIN Condensed',
                           text_anchor="middle", dominant_baseline="central")
P1_BABY_AGE_STYLE = Style(font_size="15px", fill="#000000", font_style="normal", font_variant="normal",
                          font_weight="bold", font_stretch="normal", font_family='D-DIN Condensed',
                          text_anchor="middle", dominant_baseline="central")
# ----------------------------------------
# Page 2
P2_BABY_NAME_LOC = (30, 82)
P2_BABY_AGE_LOC = (31, 120)
P2_BABY_NAME_STYLE = Style(font_size="45px", fill="#232323", font_style="normal", font_variant="normal",
                           font_weight="bold", font_stretch="normal", font_family='D-DIN Condensed',
                           text_anchor="start", dominant_baseline="central")
P2_BABY_AGE_STYLE = Style(font_size="14px", fill="#000000", font_style="normal", font_variant="normal",
                          font_weight="bold", font_stretch="normal", font_family='D-DIN Condensed',
                          text_anchor="start", dominant_baseline="central")
P2_BABY_PIE_LOC = (495, 118)
P2_PIE_COLS = (104, 241, 379, 517)
P2_PIE_LINE = 323
P2_NAME_LINE = 390
P2_USAGE_LINE = 412
P2_SPIDER_LINE = 500

# ----------------------------------------
# Page 3
P3_LANG_NAME_STYLE = Style(font_size='15px', font_family='D-DINCondensed', font_weight="Bold", fill='#000000', fill_opacity='1', text_anchor="start", dominant_baseline="central")
P3_PEOPLE_NAME_STYLE = Style(font_size='16px', font_family='D-DINCondensed', font_weight="Bold", fill='#000000', fill_opacity='1', text_anchor="middle", dominant_baseline="hanging")
# language legends
P3_LANG_ROW1 = 139.27
P3_LANG_ROW2 = 170
P3_LANG_BALL_COLS = (35, 182, 326, 471)
P3_LANG_TEXT_COLS = (54, 201, 343, 491)
# pie chart & names
P3_PIE_ROW = 323.27
P3_PIE_COLS = (82, 219, 360, 500)
# names & usage lines
P3_NAME_ROW = 390
P3_USAGE_ROW = 412
# spider chart
P3_SPIDER_ROW = 500


def generate_leo(profile, output_dir='output', overwrite=False, auto_clean=True, mkdir=False):
    ''' Generate LEO report '''
    output_dir = prepare_output_dir(output_dir, mkdir=mkdir)
    # generate color map
    color_map = profile.build_language_color_map()
    # page 1
    getLogger().info("Generating page 1 SVG")
    t1 = Canvas(PAGE1_TEMPLATE)
    g1 = t1.group('leo')
    g1.text(profile.baby.name.upper(), center=P1_BABY_NAME_LOC, style=P1_BABY_NAME_STYLE, id_prefix="p1_BabyName")
    g1.text(profile.baby.age.upper(), center=P1_BABY_AGE_LOC, style=P1_BABY_AGE_STYLE, id_prefix="p1_BabyAge")
    # page 2
    getLogger().info("Generating page 2 SVG")
    t2 = Canvas(PAGE2_TEMPLATE)
    g2 = t2.group('leo')
    # name & age
    g2.text(profile.baby.name.upper(), center=P2_BABY_NAME_LOC, style=P2_BABY_NAME_STYLE, id_prefix="p2_BabyName")
    g2.text(profile.baby.age.upper(), center=P2_BABY_AGE_LOC, style=P2_BABY_AGE_STYLE, id_prefix="p2_BabyAge")
    # baby's chart
    baby_languages = list(profile.baby.languages.keys())
    baby_colors = [color_map[l] for l in baby_languages]
    baby_slides = (x.dist for lang, x in profile.baby.languages.items())
    pie = PieChart(g2, center=P2_BABY_PIE_LOC, radius=CHART_RADIUS, colors=baby_colors)
    pie.slide(*baby_slides)
    pie.render(id_prefix="p2_baby_piechart")
    for i, person in enumerate(profile.people[:4]):
        languages = [lang for lang, p in person.languages.items() if p.dist > 0]
        colors = [color_map[l] for l in languages]
        g2.text(person.name.strip().upper(), center=(P2_PIE_COLS[i], P2_NAME_LINE), style=PEOPLE_NAME_STYLE, id_prefix=f"p2_person{i}_name")
        if person.usage != -1:
            g2.text(f"{round(person.usage)}%", center=(P2_PIE_COLS[i], P2_USAGE_LINE), style=PEOPLE_NAME_STYLE, id_prefix=f"p2_person{i}_usage")
        else:
            g2.text(f"- N/A -", center=(P2_PIE_COLS[i], P2_USAGE_LINE), style=PEOPLE_NAME_STYLE, id_prefix=f"p2_person{i}_usage")
        # render pie charts
        slides = [x.dist for x in person.languages.values() if x.dist > 0]
        if not person.piesize:
            _adjust = 100
        elif person.piesize > 10:
            _adjust = person.piesize
        else:
            # draw draw the pie chart too small
            _adjust = 10
        radius = (PIE_RADIUS * _adjust / 100, PIE_RADIUS * _adjust / 100)
        getLogger().debug(f"{person.name} -- adjust -> {_adjust}")
        pie = PieChart(g2, center=(P2_PIE_COLS[i], P2_PIE_LINE), radius=radius, colors=colors)
        pie.slide(*slides)
        pie.render(id_prefix=f"p2_person{i}_piechart")
        # render spider charts
        spider_matrix = [x.skills for x in person.languages.values() if x.skills.is_valid()]
        if not spider_matrix:
            getLogger().warning(f": {profile.reportID}/page 2 - person `{person.name.strip()}` does not have a spider chart")
            continue
        spider_languages = [lang for lang in person.languages.keys()]
        spider_colors = [color_map[l] for l in spider_languages]
        ch = SpiderChart(cx=P2_PIE_COLS[i], cy=P2_SPIDER_LINE, rx=64, max_score=8)
        ch.render(g2, spider_matrix, colors=spider_colors, id_prefix=f"p2_person{i}_spiderchart")
    # page 3
    getLogger().info("Generating page 3 SVG")
    t3 = Canvas(PAGE3_TEMPLATE)
    g3 = t3.group('leo')
    # List languages
    _languages = profile.languages if profile.languages else profile.get_extra_language_legends()
    colors = [color_map[l] for l in _languages]
    for idx, (lang, color) in enumerate(zip(_languages, colors)):
        g3.text(lang.upper(), center=(P3_LANG_TEXT_COLS[idx], P3_LANG_ROW2), style=P3_LANG_NAME_STYLE, id_prefix=f"language_legends_text{idx}")
        g3.circle((P3_LANG_BALL_COLS[idx], P3_LANG_ROW2), 10, style=STYLE_REDDOT.clone(fill=color, stroke="none"), id_prefix=f"language_legends_circle_{idx}")
    # ----------------------------------------
    # draw charts & names
    for i, person in enumerate(profile.people[4:8]):
        languages = [lang for lang, p in person.languages.items() if p.dist > 0]
        colors = [color_map[l] for l in languages]
        g3.text(person.name.strip().upper(), center=(P3_PIE_COLS[i], P3_NAME_ROW), style=P3_PEOPLE_NAME_STYLE, id_prefix=f"p3_person{i}_name")
        if person.usage != -1:
            g3.text(f"{round(person.usage)}%", center=(P3_PIE_COLS[i], P3_USAGE_ROW), style=P3_PEOPLE_NAME_STYLE, id_prefix=f"p3_person{i}_usage")
        else:
            g3.text(f"- N/A -", center=(P3_PIE_COLS[i], P3_USAGE_ROW), style=P3_PEOPLE_NAME_STYLE, id_prefix=f"p3_person{i}_usage")
        # render pie charts
        slides = [x.dist for x in person.languages.values() if x.dist > 0]
        if not person.piesize:
            _adjust = 100
        elif person.piesize > 10:
            _adjust = person.piesize
        else:
            # draw draw the pie chart too small
            _adjust = 10
        radius = (PIE_RADIUS * _adjust / 100, PIE_RADIUS * _adjust / 100)
        getLogger().debug(f"{person.name} -- adjust -> {_adjust}")
        pie = PieChart(g3, center=(P3_PIE_COLS[i], P3_PIE_ROW), radius=radius, colors=colors)
        pie.slide(*slides)
        pie.render(id_prefix=f"p3_person{i}_piechart")
        # render spider charts
        spider_matrix = [x.skills for x in person.languages.values() if x.skills.is_valid()]
        if not spider_matrix:
            getLogger().warning(f"{profile.reportID}/page 3 - person `{person.name.strip()}` does not have a spider chart")
            continue
        spider_languages = [lang for lang in person.languages.keys()]
        spider_colors = [color_map[l] for l in spider_languages]
        ch = SpiderChart(cx=P3_PIE_COLS[i], cy=P3_SPIDER_ROW, rx=64, max_score=8)
        ch.render(g3, spider_matrix, colors=spider_colors, id_prefix=f"p3_person{i}_spiderchart")
    # Render SVG files
    pdf_filename_stem = profile.output_filename()[:-4] if profile.output_filename().endswith('.pdf') else profile.output_filename()
    getLogger().info("Exporting SVG files ...")
    t1.render(output_dir / f'{pdf_filename_stem}_leo_page1.svg', overwrite=overwrite)
    t2.render(output_dir / f'{pdf_filename_stem}_leo_page2.svg', overwrite=overwrite)
    t3.render(output_dir / f'{pdf_filename_stem}_leo_page3.svg', overwrite=overwrite)
    getLogger().debug("Exporting PDF pages ...")
    svg_to_pdf(output_dir / f'{pdf_filename_stem}_leo_page1.svg', overwrite=overwrite)
    svg_to_pdf(output_dir / f'{pdf_filename_stem}_leo_page2.svg', overwrite=overwrite)
    svg_to_pdf(output_dir / f'{pdf_filename_stem}_leo_page3.svg', overwrite=overwrite)
    getLogger().debug("Combining PDF pages ...")
    output_filepath = output_dir / profile.output_filename()
    if not overwrite and output_filepath.exists():
        getLogger().warning(f"{output_filepath} report file exists. SKIPPED")
    else:
        merge_pdf(output_path=output_filepath,
                  input_paths=[output_dir / f"{pdf_filename_stem}_leo_page1.pdf",
                               output_dir / f"{pdf_filename_stem}_leo_page2.pdf",
                               output_dir / f"{pdf_filename_stem}_leo_page3.pdf"])
    # generated output filename
    if auto_clean and output_filepath.is_file():
        (output_dir / f'{pdf_filename_stem}_leo_page1.svg').unlink()
        (output_dir / f'{pdf_filename_stem}_leo_page2.svg').unlink()
        (output_dir / f'{pdf_filename_stem}_leo_page3.svg').unlink()
        (output_dir / f'{pdf_filename_stem}_leo_page1.pdf').unlink()
        (output_dir / f'{pdf_filename_stem}_leo_page2.pdf').unlink()
        (output_dir / f'{pdf_filename_stem}_leo_page3.pdf').unlink()
    return output_filepath
