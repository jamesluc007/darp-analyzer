# darp-analyzer

This project was selected as [one of the best 5](https://medium.com/syntropynet/recap-of-the-deweb-virtual-hackathon-2021-3b8ae4d2c313) in a [Hackathon](https://www.syntropystack.com/hackathon) organized by Syntropy in June of 2021.

Here is the presentation video: https://youtu.be/M59Vnf72A8w

Here is the deployed web: https://share.streamlit.io/jamesluc007/darp-analyzer/deploy/darp_analyzer_webapp.py

Note: This repo is no longer maintained. If the web page goes down due to inactivity, you can ask me to get it up again by sending me a private message in case you need it. You can also run it locally as explained in the **How to Run It** section.

# Project Description

Darp Analyzer is a high-level, easy-to-use, easy-to-escalate data analysis tool for DARP data. It is presented as an easy-to-deploy web app programmed in python.

It uses **streamlit**, an open-source python library for web app designing. Everything is programmed in python so it is familiar to data scientists that might not have experience with HTML/web development.

# How to Run It

1. Install the necessary dependencies:
    * **streamlit 0.83 or higher**
    * **Pandas**
    * **PyDeck**
    * **numpy**
2. Run `python make.py`. This must be done only the very first time that you execute this web app.
3. Run `streamlit run darp_analyzer_webapp.py`

# How to Run It - option 2

- [x] Checkout to the branch called "deploy"

- [x] Run `pip install requirements.txt`

- [x] Run `streamlit run darp_analyzer_webapp.py`
