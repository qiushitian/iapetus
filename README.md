# Can the Equatorial Ridge on Iapetus Form from a Debris Disk?

Authors: Ankita Dasgupta, Audrey Whitmer, Qiushi Chris Tian

Updated: 2026-11-12

## Notes on project approach:
- start with sun saturn iapetus, disk
- rain down on moon, record mass, energy, angular momentum...
- measure mass transfer rate, angular momentum transfer rate
- rotation rate is synched with saturn
- we dont have an angular momentum constraint
- when the ridge was formed, iapetus wasnt tidally locked yet. so even tho it wasnt tidally locked yet, saturn will take care of it
- concequence: integration of disk + iapetus is second order, and sun + saturn are forth order (bc n-body)
- bridge timestep is too long, it's longer than both n-body and hydro timesteps. so dont bridge them.
- monitor collisions between disk + moon surface: do this by removing anything that is colliding.
- when things collide, remove them from the system. then write mass, where on iapetus surface, with what velocity, so you can calculate momentum + mass transfer
- show pic: projection of iapetus surface that shows where the shit falls down / heat map of where mass is accreted
- alternate would be to use debris disk: cons: not naturally dissapative, they need some force/perturbation to get debris to fall. simon is not sure what the effect of saturn's influence on the disk would be. might work might not.
- we could try tilting the disk !! incline the disk with respect to saturn.
- bridge (i + disk) + (sun + saturn), incilne disk by 45, 90, 180...
- still need collision detection.
- Huyano is very stable for doing a disk. has many integrators. can do test particles w no mass.
- where is this ridge with respect to saturn??
- if we're not using hydro: use collision detection, not synch particle.
- collisions miiight help make ridge on iapetus...
- for all these, start with the same initial conditions. and just change the angle of the disk.
- n-body is more exciting, and  !! but hydro would definitely work ...
- take inclination of iapetus with respect to saturn's plane as a free parameter... make maps of the results, and show what % of the disk ends up accreting onto iapetus....
- do we need tidymess? try it only after we make the ridge!! it is a slow code, but it owuld be cool to see that after we build a ridge if tidymess will pull it to its 7* angle!!!
- do like 10 Lidov–Kozai cycles. one is too little, because it's too close to initial conditions. probably 100s of years??
- think of how many cores you can use depending on how many particles + how many years. final thing should be about 1 weekend.

## How to run our code?

The only script you need to run is `main.py`. It will do everything, including running the simulation and making plots and movies. The plots and movies are saved under `outputs/`. See the [Code Content](#code-content) section for more details.

The best way to run our code is to do it on a STRW computer system with the environment module `AMUSE/2026.6.0`. This makes sure you have the same versions of all the packages as we do. See below for instructions.

### Using the STRW Environment Module

You can load the AMUSE easybuild environment module on **vdesk** or any other STRW server node (e.g. maas, waal, ijssel, etc.) by running:
```bash
module load AMUSE/2026.6.0
```

Then, you can simply run our code by typing in
```bash
python main.py
```

You might want to make sure you are in a desirable working directory before you run `main.py`, because it will create an `output/` folder in your current working directory.

You can learn more about environment modules on [this page on the STRW Documentation Wiki](https://local.strw.leidenuniv.nl/docs/doku.php%3Fid=linux:environment_modules.html).

### Package Versions

If you run our code on other machines like your own computer, you might find this list of package versions useful:
```
python==3.14.10
amuse==2026.6.0
astropy==8.0.2
matplotlib==3.11.2
numpy==2.5.4
```

## Code Content
- `main.py`: The script that runs everything.
- `initialize.py`: Functions to make the simulated system and set initial conditions.
- `evolution.py`: Functions to evolve the system in the simulation.
- `plotting.py`: Functions to make plots and movies.
- `utils.py`: Helper functions.

## FAQ

### How do I get this code?

Hopefully you already know how to use Git and GitHub since you're on this page! You can clone our repository by running:
```bash
git clone https://github.com/qiushitian/iapetus.git
```

Alternatively, you can download all code by clicking on the green/blue "< > Code" button, and then select "Download ZIP".

### How do I know if I have loaded the environment module successfully?

The module is most likely successfully loaded if your shell prints nothing after you run `module load AMUSE/2026.6.0` (i.e. no error message). You can verify this by running `module list`, and you should see:
```
Currently Loaded Modules:
  1) Miniconda3/25.7.0-2   2) AMUSE/2026.6.0
```

Alternatively, you can run `which python`, and you should see:
```
/easybuild/easybuild/el9/software/AMUSE/2026.6.0/bin/python
```
