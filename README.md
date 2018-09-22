
# ratCAVE Grass Scene

A 3D scene made as a demo for the Sirota Lab's ratCAVE virtual reality setup.

## Installation

```
git clone https://github.com/fabalinks/ratCAVE_grass
cd ratCAVE_grass
conda create --name grassVR python=2.7
pip install -r requirements.txt
```

## Build 3D Assets

Launch Blender and export all objects to an .obj file in the same folder.
Manually remove all Map_kd lines in the .mtl file that is generated.

## Run

Make sure you're runnign the Motive and streaming rigid bodies.  There should be an "Arena" and a "Rat" rigid body.

```
python run.py
```

