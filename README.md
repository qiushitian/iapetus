# Can the Equatorial Ridge on Iapetus Form from a Debris Disk?

Authors: Ankita Dasgupta, Audrey Whitmer, Qiushi Chris Tian

Updated: 2026-11-10

## How to run our code?

The only script you need to run is `main.py`. It will do everything, including setting up the initial conditions, evolving the system, and making plots and movies. The plots and movies are saved under `outputs/`.

### 

### Using Environment Module on vdesk and STRW Servers

If you are on vdesk or any other STRW server node (e.g. maas, waal, ijssel, etc.), you should load the AMUSE easybuild environment module: 
```bash
module load AMUSE/2026.6.0
```

This ensures that you are using the same version of AMUSE, Python, Matplotlib, NumPy, and other dependencies as when we were writing and testing our code.

You can check if the module is loaded by running `module list`, and you should see `AMUSE/2026.6.0`. Alternatively, you can run `which python`, and you should see `/easybuild/easybuild/el9/software/AMUSE/2026.6.0/bin/python`.

Then, you can simply run our code by typing in
```bash
python main.py
```

Violà!

## Code Content
- `plotting.py`: Functions to make plots and movies