# Fake Images Please?

When designing websites, you may not have the images you need at first. But you already know the sizes and inserting some placeholders can help you better seeing the layout. Don’t waste your time making dummy images for your mockup or wireframe. Fakeimg.pl is a little tool that generates images with an URL. Choose the size, the colors, even the text. It’s free and [open-source](https://github.com/Rydgel/Fake-images-please).

## How to use

You just have to put your image size after our URL. Only the first parameter is mandatory. There are options too, you can pass a text, or change some colors. Colors must be hexadecimal, the first one is the background color. The text can be passed with the _text_ GET variable. Here are some examples you can look at:

    <img src="http://fakeimg.pl/300/">
    <img src="http://fakeimg.pl/250x100/">
    <img src="http://fakeimg.pl/250x100/ff0000/">
    <img src="http://fakeimg.pl/350x200/ff0000/000">
    <img src="http://fakeimg.pl/350x200/?text=Hello">

Use them directly in an image tag or a CSS background, or whatever you want to.

## Set up your own instance

Prerequisites:

* Python
* Python development headers
* Memcached
* Memcached development headers
* pip (`easy_install pip` if you don’t already have it.)
* A compilation chain (like gcc or else)

1. First you need to clone the project

       `git clone https://github.com/Rydgel/Fake-images-please.git`

2. Install all dependencies with `pip`

       `pip install -r requirements.txt`
       
	   You may need to have this command run by a privileged user.

3. Run the tests

       `python tests.py`

4. Run the server

       `python app.py`

5. Open the browser at `http://127.0.0.1:5000`

## About

Made by Jérôme Mahuet, with love in 2012. Follow [@phollow](http://twitter.com/phollow) to stay up-to-date with the project, or if you just want to ask something. Feel free to make pull requests.