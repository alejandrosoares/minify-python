# MINIFY-PYTHON
Minify html, css and java script files with services of <a href="https://www.toptal.com/">Toptal</a>,
through the use of their API and on the other hand optimize the images of your project to reduce your weight.
<br>
The script is written in python.

## Important
- The project has been perform in Linux platform and has not been probed in others platforms.
- The original project is <b>not</b> modified, a copy of project is created.

## Installation
Follow the next steps:
-  Download the folder and place it in the same parent folder as your project. For example: <br>
   ```
    parent_folder  
    │
    └───my_project
    │   
    └───minify
    ```
-  Create a virtualenvironment and install the packages described in <b>requirements.txt</b>.

## Usage
- Run command:
```bash
    minify.py source_path destination_path
```
For example, assuming I have a project named <b>example</b> and I want to put the folder with the minified files
in the parent folder of <b>example</b>, the command is: <br>
```bash
    minify.py  ./example  ./
```
- And the following folder will be created: <br>
```
parent_folder  
│
└───example
│   
└───minify
│   
└───prod
    │   
    └───example
```
- In <b>prod</b> folder there will be copy of <b>example</b> project with the minified files and compressed images.
- <b>source_path</b> and <b>destination_path</b> are taken from parent folder of minify folder. 
- By default the copy of project is created inside of a folder named <b>prod</b> and the optimization quality is of 65. These
and others parameters can be changed minify/settings.py.

## Project Files description
```
minify/
│  minify.py: main file that containing project logic.
│  settings.py: file that contain the configurations.
│  utils.py: file that contain helper functions for minify.py
```
## Contributing
Any pull request are welcome.

### Where could we continue?
- Perform unit tests.
- Join css files into a main css file.
- Use some API service to convert images to webp format.

## Resources

https://www.toptal.com/developers/cssminifier/python

https://www.toptal.com/developers/javascript-minifier/python

https://www.toptal.com/developers/html-minifier/python
