# animated weather icons for the unicorn-hat-hd
handmade weather animations for unicorn-hat-hd made by pimoroni. each hd animation is made of 32 handmade mini pictures, combined to a sprite.


draw_animation(image) is same as in the 'show-png' example but put into a tiny little function.

put in your image object and you're done.

[pimoroni's show-png example](https://github.com/pimoroni/unicorn-hat-hd/blob/master/examples/show-png.py "pimoroni's show-png example")

the draw_animation() function will loop through all images in the sprite and it will look like a tiny animation. Awesome !!

you can change the 'fps' with changing the 'cycle_time' variable (0.25 is very smooth).

loop() finally loops through all png images in a folder (you might guessed it) so you can see all possibilities.

Usage:

```python weather-icons.py options```
    
options:
- loop
- image-file.png

example:

```weather-icons.py loop```

```weather-icons.py clear-day.png```


## new unicorn-hat-hd animations 16x16

|                             | unicornhat hd                           |                                             |
|:---------------------------:|:---------------------------------------:|:-------------------------------------------:|
| fog                         | partly-cloudy-day                       | partly-cloudy-night                         |
| ![fog][fog]                 | ![partly-cloudy-day][partly-cloudy-day] | ![partly-cloudy-night][partly-cloudy-night] |
| clear-night                 | clear-day                               | cloudy                                      |
| ![clear-night][clear-night] | ![clear-day][clear-day]                 | ![cloudy][cloudy]                           |
| rain                        | snow                                    | windy                                       |
| ![rain][rain]               | ![snow][snow]                           | ![windy][windy]                             |
| error                       | raspberry                               | pimoroni pirate                             |
| ![error][error]             | ![raspberry][raspberry]                 | ![pimoroni_pirate][pimoroni_pirate]         |


[clear-day]: https://github.com/LoveBootCaptain/unicornhat_weather_icons/blob/master/animation/HD/clear-day.gif "clear-day"
[clear-night]: https://github.com/LoveBootCaptain/unicornhat_weather_icons/blob/master/animation/HD/clear-night.gif "clear-night"
[cloudy]: https://github.com/LoveBootCaptain/unicornhat_weather_icons/blob/master/animation/HD/cloudy.gif "cloudy"

[fog]: https://github.com/LoveBootCaptain/unicornhat_weather_icons/blob/master/animation/HD/fog.gif "cloudy"
[partly-cloudy-day]: https://github.com/LoveBootCaptain/unicornhat_weather_icons/blob/master/animation/HD/partly-cloudy-day.gif "partly-cloudy-day"
[partly-cloudy-night]: https://github.com/LoveBootCaptain/unicornhat_weather_icons/blob/master/animation/HD/partly-cloudy-night.gif "partly-cloudy-night"

[rain]: https://github.com/LoveBootCaptain/unicornhat_weather_icons/blob/master/animation/HD/rain.gif "rain"
[snow]: https://github.com/LoveBootCaptain/unicornhat_weather_icons/blob/master/animation/HD/snow.gif "snow"
[windy]: https://github.com/LoveBootCaptain/unicornhat_weather_icons/blob/master/animation/HD/windy.gif "windy"

[error]: https://github.com/LoveBootCaptain/unicornhat_weather_icons/blob/master/animation/HD/error.gif "error"
[raspberry]: https://github.com/LoveBootCaptain/unicornhat_weather_icons/blob/master/animation/HD/raspberry.gif "raspberry"
[pimoroni_pirate]: https://github.com/LoveBootCaptain/unicornhat_weather_icons/blob/master/animation/HD/pimoroni.gif "pimoroni pirate"

[Buy the new Unicorn HAT HD on Pimoroni](https://shop.pimoroni.com/products/unicorn-hat-hd "Buy the new Unicorn HAT HD on Pimoroni")

For more animations and icons (also in 8x8 for good old unicorn-hat) please visit and support the original project by LoveBootCaptain:

[unicornhat_waether_icons by LoveBootCaptain](https://github.com/LoveBootCaptain/unicornhat_weather_icons "Contribute") 

