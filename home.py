from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    text = 'The home page will contain initiatives, links to the blog, coding progress, etc.'
    site_components = ['Home', 'Blog', 'About']
    return render_template('home.html', text = text, site_components = site_components)

@app.route('/blog/')
def blog():
    return 'Blog posts'

@app.route('/about/')
def about():
    return 'Content about me and what my goals are'

if __name__ == '__main__':
    app.debug = True
    app.run()
