I want to write a Python command line application that:

- expects some keywords as the user input
- searches recent (say past 2 weeks, could be user input) related papers at arxiv.org
- outputs a nicely formatted overview of the search results
- goes through the papers one by one, asking the user whether the paper should be downloaded
- if the user wants to download a paper, download its latex version, convert it to markdown, and save it to the `papers/` directory
