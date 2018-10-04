#! /usr/bin/python
try:
    from jinja2 import Environment, FileSystemLoader
except ImportError as msg:
    print("ImportError: %s" % msg)
    exit(1)
try:
    from yaml import load, dump
except ImportError as msg:
    print("ImportError: %s" % msg)
    exit(1)

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import os


# TODO: change absolute path to relative ones
# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(THIS_DIR, "templates{0}sections_template_default".format(os.sep))
DEFAULT_TEMPLATE = u'cv.tex'

MACROS_CONF = {
    "STYLE_DIR": os.path.join(THIS_DIR, "includes{0}cls".format(os.sep)),
    "MACROS": os.path.join(THIS_DIR, "includes{0}macros".format(os.sep)),
    "BIBSTYLE": os.path.join(THIS_DIR, "includes{0}bibstyle".format(os.sep))
}


def get_style(style_path=MACROS_CONF["STYLE_DIR"], style_filename="myRes"):
    return os.path.join(style_path, style_filename).replace('\\', '/')


def get_amcros(macro_path=MACROS_CONF["MACROS"]):
    return [os.path.join(macro_path, f).replace('\\', '/') for f in os.listdir(macro_path)]


def get_tex_doc(config, **options):
    """Generate tex code"""

    template_dir = options.get("template_dir", TEMP_DIR)
    template_filename = options.get("template", DEFAULT_TEMPLATE)
    j2_env = Environment(loader=FileSystemLoader(template_dir),
                         trim_blocks=True)

    if "macros" in config:
        pass
    else:
        config["macros"] = get_amcros()

    if "stylefile" in config:
        pass
    else:
        config["stylefile"] = get_style()

    return j2_env.get_template(template_filename).render(
        {
            "cv": config
        }
    )


def gen_tex_file(tex_doc, filename="example.tex", overwrite_handler=None):
    """Write the tex code into a file"""
    add_msg = "%% This file is generated by Jinja2"

    if os.path.exists(filename):
        if not (overwrite_handler is None):
            if not overwrite_handler(filename):
                return False

    with open(filename, 'w') as texf:
        texf.write("%s\n" % add_msg)
        texf.write(tex_doc)
    return True


if __name__ == "__main__":
    content = load(open("_config.yaml", "r"))
    #gen_tex_file(get_tex_doc(config=content), filename="long_full_2018.tex")
    #gen_tex_file(get_tex_doc(config=content), filename="long_intern_2019.tex")
