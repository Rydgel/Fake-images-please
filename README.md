# Fake Images Please?

[![Build Status](https://circleci.com/gh/Rydgel/Fake-images-please.svg?style=svg)](https://circleci.com/gh/Rydgel/Fake-images-please)

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=TSXSX65YY4RQL)

When designing websites, you may not have the images you need at first. But you already know the sizes and inserting some placeholders can help you better seeing the layout. Don’t waste your time making dummy images for your mockup or wireframe. Fakeimg.pl is a little tool that generates images with an URL. Choose the size, the colors, even the text. It’s free and [open-source](https://github.com/Rydgel/Fake-images-please).

## How to use

You just have to put your image size after our URL. Only the first parameter is mandatory. There are options too, you can pass a text, or change some colors. Colors must be hexadecimal, the first one is the background color. The text can be passed with the _text_ GET variable. Here are some examples you can look at:

```html
<img src="https://fakeimg.pl/300/">
<img src="https://fakeimg.pl/250x100/">
<img src="https://fakeimg.pl/250x100/ff0000/">
<img src="https://fakeimg.pl/350x200/ff0000/000">
<img src="https://fakeimg.pl/350x200/?text=Hello">
<img src="https://fakeimg.pl/350x200/?text=オラ&font=noto">
<img src="https://fakeimg.pl/350x200/?text=World&font=lobster">
```

Use them directly in an image tag or a CSS background, or whatever you want to.

## Change font

There are three *bonus* fonts you can choose by passing `font=lobster`, `font=bebas`, or `font=museo` in the URL.
Also please note that the `font=noto` is available for chinese/japanese/korean texts.

## Change font size

You can manually change the font size by passing in the URL `font_size=12`.

## Retina mode

Just pass the `retina=1` in the URL. Your image will be 2 times bigger.

## Asian text support

You can use the font `noto` for support of japanese, korean and chinese text.

## Transparency

Colors support transparency (0 - 255) by putting the alpha value after the color
itself. Both colors are supported.

## Emojis and Discord emotes support in text
The format for Discord emotes is like that: `<:rooThink:596576798351949847>`

```html
<img src="https://fakeimg.pl/350x200/ff0000,128/000">
<img src="https://fakeimg.pl/350x200/ff0000,128/000,10">
```

## Set up your own instance

Prerequisites:

* Docker

```bash
# Run the image (change the port if you need)
$ docker run -d -p 80:80 rydgel/fakeimg:latest
# Open the browser at http://127.0.0.1:80
```

## About

Made by Jérôme Mahuet.
Follow [@rydgel](http://twitter.com/rydgel) to stay up-to-date with the project, or if you just want to ask something.
Feel free to make pull requests.
