# coloring_the_letters
Goal:
Given a text, I want to color each unique character as a "white" or "black" letter. I'm trying to minimize the number of consecutive white or black letters.
Ultimately, I'm using for a constructed writing system where I want each letter to be written "upwards" or "downwards", and I want to minimize the number of consecitive "upwards" or "downwards" letters.

Attempt 2:
- Choose a letter
- Go to a letter that is found next to that letter
- Find whether coloring it white or black minimizes the total penalty
- Repeat

Attempt 1:
Uses Kruskal's algorithm to create a maximum spanning trees for pairs of letters given a sample text.  
