# okcupidon
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/2aefdc3b25e24cbf902abaf1013f22ee)](https://www.codacy.com/manual/Maxence-L/okcupidon/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Maxence-L/okcupidon&amp;utm_campaign=Badge_Grade)

An python scraper for Okcupid.

Since the last big UI update (2018 I guess), no working open-source Okcupid scraper was available. Fear not ! Here it comes again !

While this scraper is still in development and may be finicky to use, it works. It tends to break sometimes, as Okcupid is javascript-heavy and uses anti-scraping patterns, but you can in this case just relaunch it.

## How can I participate ?

Open an issue to share feedback or propose features. Star the repo if you like it! 🌟

## Why ?

As humans more and more absorbed in their smartphones and computers, they tend to use them predominantly for all sorts of things :

- Grocery shopping
- Dentist appointment
- Watching tv
- Reading books
- Discussing about politics

And...

- Mating

Okcupid and similar apps/websites have indeed become the primary way of finding a mate in the US, as of 2017 :

![stanford](https://assets.weforum.org/editor/large_ydZUwVLPfB2_IAeib9WXWl-yXOjH8-061HmH-HRe4Ao.png)

[Source : Stanford University](https://web.stanford.edu/~mrosenfe/Rosenfeld_et_al_Disintermediating_Friends.pdf)

There is a lot to learn about how people present themselves in the online world, what they reflect on and so on. Hacking the process of finding a mate can be a part of it, as a [Chris McKinlay did few years ago](https://www.wired.com/2014/01/how-to-hack-okcupid/) (Using data science for finding a girlfriend ! Eternal respect !)

Besides, Okcupid has been a great trove of data for aspiring Data Scientists looking for "real-world" datasets to analyse. A research paper was even wrote about it : [*OkCupid Data for Introductory Statistics and Data Science Courses*, Kim, Albert Y.; Escobedo-Land, Adriana,Journal of Statistics Education, v23 n2 2015](https://eric.ed.gov/?id=EJ1070114)

### Why not just release a dataset ?

- The dataset will contain personnal information that have not been anonymised. As I used those sites before, I'm not sure I'd like to have my intros jokes recorded on the open web forever. **Please do not release the data you've gathered if you haven't aggregated the results before.**

- Scraping it yourself gives you more flexibility for the kind of data you're looking for. For instance, currently, all "old" OkC datasets are about 'murica' but with this you can scrape the Old World or even Asia !

## Installation

Ready to try ? 

For now, you'll have to build it yourself (everything is explained below), but I'll send it to Pypi once I feel it's good enough™️ for publication.

### 1. Create a fork of the package

Fork the scrapper by clicking on the "Fork" button, in the up-right corner.

Once the forking process is complete, you should have a fork (essentially a copy) of my template in your own GitHub account. On the GitHub page for your repository, click on the green “Clone or download” button, and copy the URL: we’ll need it for the next step.

### 2. Clone your repository locally

Next, we want to download the files from your GitHub repository onto your local machine. 

- Choose a directory on your local drive and in the command line, `cd` to it.

- Replace in the command below with the URL you copied in the previous step, then execute this command:

`git clone <YOUR_COPIED_URL_HERE> okcupidon-package`

### 3. Install package

For this to work, you should have Python 3 installed on your computer. I'd advise to use a virtual environment, as always.

- cd to the 'okcupidon-package' folder. if you use `ls`, you should see a `setup.py` file in the directory.

- Type `python setup.py sdist` - this command will tell python to look for the packages' files and build it nicely.

- Now you should have a new folder, called `dist`, with a `okcupidon-0.0.tar.gz` file inside - this is the package !

- You can now install the package using `pip install \path\to\okcupidon-0.0.tar.gz`

I should work. If it doesn't, please open a ticket and tell me !

