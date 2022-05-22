import markdown, jinja2, toml, re

def load_config(config_string):
    return toml.loads(config_string)

def load_content_items(content_strings):
    items = []
    for item in content_strings:
        frontmatter, content = re.split("^\s*\+\+\+\+\+\s*$", item, 1, re.MULTILINE)
        item = toml.loads(frontmatter)
        item['content'] = markdown.markdown(content)

        items.append(item)

    # sort in reverse chronological order
    items.sort(key=lambda x: x["date"],reverse=True)

    return items

def load_templates(template_string):
    return jinja2.Template(template_string)

def render_site(config, content, template):
    print(template.render(config=config, content=content))

def main():
    config_string = """
    title = "My blog"
    """

    content_strings = ["""
title = "My first entry"
date = 2021-02-14T11:47:00+02:00
+++++

Hello, welcome to my **blog**
""",
"""
title = "My second entry"
date = 2021-02-15T17:47:00+02:00
+++++

This is my second post.
"""]

    template_string = """
<!DOCTYPE html>
<html>
    <body>
        <h1>{{ config.title }}</h1>
        {% for post in content %}
        <article>
            <h2>{{ post.title }}</h2>
            <p>Posted at {{ post.date }}</p>
            {{ post.content }}
        </article>
        {% endfor %}
    </body>
</html>
"""

    config = load_config(config_string)
    content = load_content_items(content_strings)
    templates = load_templates(template_string)
    render_site(config, content, templates)

main()