# Static Site Generator
A static site generator written in Python. This project converts Markdown files into HTML, handles templates and manages static assets.

The project is deployed on GitHub Pages. You can view the live version here:

https://przemekbukala.github.io/StaticSiteGenerator/

The site is served directly from the `docs/` directory.

##  How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/Przemekbukala/StaticSiteGenerator
cd StaticSiteGenerator
```
###  2. For Local Development
When running locally, the base path for links should be `/`.

Run the following command to generate the site and start the local server:
```bash
./main.sh "/"
```
Then open `http://localhost:8888` in your browser.

### Script Details
The `./main.sh` script executes `src/main.py`, which cleans the destination directory, copies static files, and generates HTML from Markdown files. It accepts an optional argument for the `basepath`.
### How to Run Tests
The project includes a suite of unit tests to verify the logic for parsing blocks, HTML nodes, and text nodes. To run them:
```bash
./test.sh
```
This command automatically discovers and runs all tests located in the `src/` directory.
### Project Structure
* `src/` - Source code for the generator and tests.
* `content/` - Source content files used to generate the site.
* `static/` - Images and CSS styles.
* `docs/` - Output folder, where the generated site resides, visible on GitHub Pages.
* `main.sh` - Script to run the generator.
* `test.sh` - Script to execute tests.
### Requirements
Python >=3.10
