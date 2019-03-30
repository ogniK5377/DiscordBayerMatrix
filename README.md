# DiscordBayerMatrix
Encode images using braille for discord or other applications

# Installation
`pip install pillow`
or for python 3
`pip3 install pillow`

# Usage
`python bayer.py <input> <output> <matrix size>`
`python3 bayer.py <input> <output> <matrix size>`

Example python2 usage `python bayer.py "C:\Path\Cat.png" bayer_output.txt 1`  
Example python3 usage `python3 bayer.py "C:\Path\Cat.png" bayer_output.txt 1`
![alt text][logo]

[logo]: https://i.imgur.com/Cu5LEDo.png "Imgage example"

# Notes
The matrix size determines how many levels of "gray" you will have. The amount of levels you will have can be calculated with `(2^s)*(2^s)` where `s` is the matrix size you specified. Example of this is with the matrix size of 1. `(2^1)*(2^1)` = `2*2` = `4` = 4 levels of gray.

Best results seem to be with images which are specifically made grayscale with lots of contrast between the different grays.
