# viewsive
## Tool for creating responsive websites more easy
This tool is chrome specific fun. And is developed to show websites in different viewports.
To make developing responsive websites more easy. 

## Features 
* mobile viewport
* tablet viewport 
* desktop viewport

# Run 
Just see the requirements and the Pipfile. 

# Pyinstall 
The start.spec is my custom spec for creating aa windows executable.
I think, it will just work on my machine 
For me: 
* Just run the pyinstall with the pipenv and it should do the job


## Config File for different views
```yml

profiles:
  - profile: Desktop Views
    view_mode: tab
    tabs:
      - name: projects
        url: https://www.phipluspi.com/project/
        width: 1440
      - name: goove
        url: https://www.goove.at/
        width: 1440

  - profile: Mobile Views
    view_mode: tab
    tabs:
      - name: projects
        url: https://www.phipluspi.com/project/
        width: 768
      - name: goove
        url: https://www.goove.at/
        width: 768
 ```
        