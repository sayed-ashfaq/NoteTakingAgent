# load the data from the markdown file 
# segregate the data into Headings, subheadings and text
## we can do this by reading each line and based on prefix we can assign it to a category.

# for example:
## Heading 1
### Subheading 1
### Subheading 2
## Heading 2

# we can create a dictionary with key as heading and value as list of subheadings
# we can create another dictionary with key as subheading and value as list of text
