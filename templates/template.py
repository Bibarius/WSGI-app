from jinja2 import Environment, FileSystemLoader



env = Environment(loader=FileSystemLoader('templates/'))


template = env.get_template('register.html')
print(template.render())
