from flask import Flask, render_template

app = Flask(__name__)

# General variables to be used across all pages
site_components = ['Home', 'Blog', 'About']

@app.route('/')
def home():
    text = 'The home page will contain initiatives, links to the blog, coding progress, etc.'
    return render_template('home.html', text = text, site_components = site_components)

@app.route('/blog/')
def blog():
    text = "The place where I will record my development progress and write down my thoughts"
    return render_template('blog.html', text = text, site_components = site_components)

@app.route('/about/')
def about():
    text = 'Content about me and what my goals are'
    return render_template('about.html', text = text, site_components = site_components)

if __name__ == '__main__':
    app.debug = True
    app.run()
