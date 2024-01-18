# Detection of shapes and colors with 1 camera

The code can detect colors and shapes from a camera that is located at a fixed distance perpendicular to the plane.

It uses the intrinsic matrix of the camera, specifically the focal length. Exactly the matrix K that we use is the newcameramtx variable in the calib.py code. 

Although the calibration data is stored in files by the pickle library, both codes have not yet been related, which would be very simple.

## Installation
If you use HTTPS run this command in your terminal:
```bash
git clone https://github.com/Nerofourm/triangulation_2_cams.git
```
If, on the other hand, you use SSH (recommended), run this command:
```bash
git clone git@github.com:Nerofourm/triangulation_2_cams.git
```

### Dependencies
Only need 2 libraries, you can install with pip. I recommend using a virtual environment, such as [venv](https://docs.python.org/3/library/venv.html)
```bash
pip install numpy
pip install opencv-python
```



## Usage

1.- Calibrate your camera and obtain the intrinsic matrix of the camera from the calib.py document

2.- Check the camera port in main.py and establish the appropriate one, likewise specify the distance from the camera to the plane (in mm)

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.


## License

[MIT](https://choosealicense.com/licenses/mit/)