import os
import subprocess
from docutils import nodes
from docutils.parsers.rst import Directive
from tutorials import categories, tutorials

class LocalPages(object):
    def __init__(self):
        self._content = dict()
        self._broken = dict()

    def add(self, num, case, type_, link):
        if (num, case, type_) not in self._content:
            if link != "":
                self._content[(num, case, type_)] = f"""
    <!DOCTYPE HTML>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta http-equiv="refresh" content="0;url={link}" />
            <link rel="canonical" href="{link}" />
        </head>
        <body>
            <p>
                You are being redirected to <a href="{link}">{link}</a>
            </p>
        </body>
    </html>
    """
                self._broken[(num, case, type_)] = False
            else:
                self._content[(num, case, type_)] = f"""
    <!DOCTYPE HTML>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta http-equiv="refresh" content="0;url={link}" />
            <link rel="canonical" href="{link}" />
        </head>
        <body>
            <p>
                Running this tutorial on the requested platform is still a work in progress.
            </p>
        </body>
    </html>
    """
                self._broken[(num, case, type_)] = True
                return ""
        if link != "":
            return self.url(num, case, type_)
        else:
            return ""

    def items(self):
        for key in self._content.keys():
            yield (key, self._content[key], self._broken[key])

    @staticmethod
    def url(num, case, type_):
        if case == "-":
            return os.path.join("tutorials", num, type_)
        else:
            return os.path.join("tutorials", num, case, type_)

local_pages = LocalPages()

class Tutorials(Directive):

    def run(self):
        output = list()
        for (category_id, (category, tutorials_in_category)) in enumerate(categories.items()):
            output.append(nodes.raw(text=self._category_title(category_id, category), format="html"))
            cards = list()
            for num in tutorials_in_category:
                data = tutorials[num]
                cases = data["cases"]
                if len(cases) == 1:
                    assert "-" in cases
                    links = {type_: local_pages.add(num, "-", type_, cases["-"][type_])
                             for type_ in self._types}
                    buttons = "".join([self._button(type_, links[type_]) for type_ in self._types])
                else:
                    links = {case: {type_: local_pages.add(num, case, type_, cases[case][type_])
                                    for type_ in self._types}
                             for case in cases}
                    buttons = "".join(
                        [self._dropdown(type_, {cases[case]["description"]: links[case][type_] for case in cases})
                         for type_ in self._types])
                card_num = self._card(
                    num=num,
                    title=data["title"],
                    description=data["description"],
                    buttons=buttons
                )
                cards.append(card_num)
            output.append(nodes.raw(text=self._card_container(category_id, cards), format="html"))
        return output

    @staticmethod
    def _category_title(category_id, category):
        return f"""
<input type="checkbox" name="category-toggle-{category_id}" id="category-toggle-{category_id}" class="tutorial-category-toggle">
<label for="category-toggle-{category_id}" class="tutorial-category-title">{category}</label>
"""

    @staticmethod
    def _card_container(category_id, cards):
        card_container = """
<div class="tutorial-container" id="tutorial-category-{category_id}">
  <div class="tutorial-row">
"""
        for card in cards:
            card_container += """
    <div class="tutorial-column">
""" + card + """
    </div>
"""
        card_container += """
  </div>
</div>
"""
        return card_container

    @staticmethod
    def _card(num, title, description, buttons):
        return f"""
<div class="tutorial-card">
  <div class="tutorial-number">
    {num}
  </div>
  <div class="tutorial-content">
    <h3 class="tutorial-title">
      {title}
    </h3>
    <div class="tutorial-description">
      <p>{description}</p>
    </div>
    <div class="tutorial-buttons">
      {buttons}
    </div>
  </div>
</div>
"""

    @classmethod
    def _dropdown(cls, type_, entries):
        all_links = "".join(entries.values())
        if all_links != "":
            dropdown = f"""
    <div id="tutorial-dropdown-{cls._dropdown_id}" class="jq-dropdown jq-dropdown-tip">
        <ul class="jq-dropdown-menu">
"""
            for (text, link) in entries.items():
                if link != "":
                    dropdown += f"""
            <li><a href="{link}">{text}</a></li>
"""
                else:
                    dropdown += f"""
            <li><span class="in-progress">{text} {cls._type_image(type_, "")}</span></li>
"""
            dropdown += f"""
        </ul>
    </div>
    <div class="tutorial-button" data-jq-dropdown="#tutorial-dropdown-{cls._dropdown_id}">{cls._type_text(type_, all_links)}</div>
"""
            cls._dropdown_id += 1
            return dropdown
        else:
            return cls._button(type_, all_links)

    _dropdown_id = 1

    @classmethod
    def _button(cls, type_, link):
        if link != "":
            return f"""
    <a href="{link}"><div class="tutorial-button">{cls._type_text(type_, link)}</div></a>
"""
        else:
            return f"""
    <div class="tutorial-button tutorial-button-in-progress">{cls._type_text(type_, link)}</div>
"""

    @classmethod
    def _type_text(cls, type_, link):
        if type_ == "file":
            text = "View on GitHub"
        elif type_ == "notebook":
            text = "Run on Google Colab"
        elif type_ == "app":
            text = "Run on ARGOS"
        else:
            raise RuntimeError("Invalid type")
        return f'{cls._type_image(type_, link)} {text}'

    @staticmethod
    def _type_image(type_, link):
        if link == "":
            logo = "_static/images/work-in-progress.png"
        else:
            if type_ == "file":
                logo = "_static/images/github-logo.png"
            elif type_ == "notebook":
                logo = "_static/images/colab-logo.png"
            elif type_ == "app":
                logo = "_static/images/argos-logo.png"
            else:
                raise RuntimeError("Invalid type")
        return f'<img src="{logo}" style="vertical-align: middle; width: 25px">'

    _types = ("file", "notebook", "app")

def on_build_finished(app, exc):
    if exc is None and app.builder.format == "html":
        # Unescape at symbol
        subprocess.run(
            "find " + app.outdir + " -type f -exec sed -i 's/%40/@/g' {} +",
            shell=True)
        # Mark current page as active
        subprocess.run(
            "find " + app.outdir + " -type f -exec sed -i 's/"
            + '<li class="md-tabs__item"><a href="#" class="md-tabs__link">'
            + "/"
            + '<li class="md-tabs__item md-tabs__item_current"><a href="#" class="md-tabs__link">'
            + "/g' {} +",
            shell=True)
        # Disable going to submenus on mobile
        subprocess.run(
            "find " + app.outdir + " -type f -exec sed -i 's/"
            + 'id="__toc"'
            + "/"
            + 'id="__toc_disabled"'
            + "/g' {} +",
            shell=True)
        # Write out local pages
        for (key, content, _) in local_pages.items():
            html_path = os.path.join(app.outdir, local_pages.url(*key), "index.html")
            os.makedirs(os.path.dirname(html_path), exist_ok=True)
            with open(html_path, "w") as html_file:
                html_file.write(content)


def setup(app):
    app.add_directive("tutorials", Tutorials)
    app.connect("build-finished", on_build_finished)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": False,
    }