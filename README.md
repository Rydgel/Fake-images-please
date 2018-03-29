# Fake Images Please?

[![Build Status](https://semaphoreci.com/api/v1/rydgel/fake-images-please/branches/master/badge.svg)](https://semaphoreci.com/rydgel/fake-images-please)

When designing websites, you may not have the images you need at first. But you already know the sizes and inserting some placeholders can help you better seeing the layout. Don’t waste your time making dummy images for your mockup or wireframe. Fakeimg.pl is a little tool that generates images with an URL. Choose the size, the colors, even the text. It’s free and [open-source](https://github.com/Rydgel/Fake-images-please).

## How to use

You just have to put your image size after our URL. Only the first parameter is mandatory. There are options too, you can pass a text, or change some colors. Colors must be hexadecimal, the first one is the background color. The text can be passed with the _text_ GET variable. Here are some examples you can look at:

```html
<img src="https://fakeimg.pl/300/">
<img src="https://fakeimg.pl/250x100/">
<img src="https://fakeimg.pl/250x100/ff0000/">
<img src="https://fakeimg.pl/350x200/ff0000/000">
<img src="https://fakeimg.pl/350x200/?text=Hello">
<img src="https://fakeimg.pl/350x200/?text=World&font=lobster">
```

Use them directly in an image tag or a CSS background, or whatever you want to.

## Change font

There are three *bonus* fonts you can choose by passing `font=lobster`, `font=bebas`, or `font=museo` in the URL.

## Change font size

You can manually change the font size by passing in the URL `font_size=12`.

## Retina mode

Just pass the `retina=1` in the URL. Your image will be 2 times bigger.

## Transparency

Colors support transparency (0 - 255) by putting the alpha value after the color
itself. Both colors are supported.

```html
<img src="https://fakeimg.pl/350x200/ff0000,128/000">
<img src="https://fakeimg.pl/350x200/ff0000,128/000,10">
```

## Set up your own instance

Prerequisites:

* Python 3.6
* Python development headers
* pip
* A compilation chain (like gcc or else)
* libfreetype-dev

```bash
# First you need to clone the project
$ git clone https://github.com/Rydgel/Fake-images-please.git
# Install all dependencies with pip
$ pip install Flask Pillow
# Run the tests
$ python tests.py
# Run the server
$ python app.py
# Open the browser at http://127.0.0.1:5000
```

## About

Made by Jérôme Mahuet in 2013.
Follow [@rydgel](http://twitter.com/rydgel) to stay up-to-date with the project, or if you just want to ask something.
Feel free to make pull requests.
