# Raspberry Pi 3 Kaldi install guide
This is an instruction to compile the Kaldi ASR for this project. Credit to [saeidmokaram](https://github.com/saeidmokaram/Kaldi-on-RaspberryPi2) 

## System requirements:

1. Raspberry Pi 3
2. MicroSD card. 16GB is fine.
3. Raspberry Pi OS (previously called Raspbian).


## Preparing your Raspberry Pi 3
The first step is to install and run the [Raspberry Pi OS](https://www.raspberrypi.org/software/operating-systems/) on your Raspberry Pi 3.

The Kaldi installation requires a bit more memory than the 1GB of the Raspberry Pi 3. So an option for compiling Kaldi on the device is to allocate a swap space. Detail instruction on allocating swap space can be found [here](https://linuxize.com/post/create-a-linux-swap-file/). These are some basic steps that i followed:  
   1. Create a file that will be used for swap: 
   ```sh
   $ sudo fallocate -l 1G /swapfile
   ```
   2. Only the root user should be able to write and read the swap file. To set the correct permissions type:  
   ```sh
   $ sudo chmod 600 /swapfile
   ```
   3. Use the ```mkswap``` utility to set up the file as Linux swap area:
   ```sh
   $ sudo mkswap /swapfile
   ```
   4. Enable the swap with the following command:  
   ```sh
   $ sudo swapon /swapfile
   ```
   To make the change permanent open the `/etc/fstab` file and append the following line:
   ```sh
   /swapfile swap swap defaults 0 0
   ```
   5. To verify that the swap is active, use either the `swapon` or the `free` command as shown below:
   ```sh
   $ sudo swapon --show
   ```
   ```sh
   NAME         TYPE    SIZE    USED    PRIO
   /swapfile    file    1024M   507.4M   -1
   ```
   ```sh
   $ sudo free -h
   ```
   ```sh
                total       used        free      shared  buff/cache   available
    Mem:        488M        158M         83M        2.3M        246M        217M
    Swap:       1.0G        506M        517M
   ```


## Getting Kaldi

```sh
$ git clone https://github.com/kaldi-asr/kaldi.git kaldi --origin upstream
```

## Making required tools  

To check the prerequisites for Kaldi, first run  

```sh
$ extras/check_dependencies.sh
```  
and see if there are any system-level installations you need to do.  
  
Run your Pi in the "Shell Mode" and use just "one cpu" (-j 1) to compile because of memory limit on Pi.

```sh
$ cd kaldi/tools/
```

In Makefile, if required, uncomment the next line to build with OpenFst-1.6.5.

```sh
OPENFST_VERSION = 1.6.5
```

Add this befor "all: check_required_programs sph2pipe atlas sclite openfst"

```sh
CXXFLAGS = -mfpu=neon -march=native -mcpu=native -mtune=native -mfloat-abi=hard -funsafe-math-optimizations
```

Make the tools by:

```sh
$ make -j 1
```

## Making Kaldi:

```sh
$ cd ../src
```

In src do:

```sh
$ ./configure --shared
```



Making depend:

```sh
$ make depend -j 1
$ make -j 1
```

---
