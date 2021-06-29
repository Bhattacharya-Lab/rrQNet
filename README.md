# rrQNet

<h2>Residue-residue quality estimation net</h2> 

## Installation

Installing rrQNet is very straightforward. The following instructions should work for 64-bit Linux system:

- Make sure you have Python with NumPy and TensorFlow installed. rrQNet has been tested on Python 3.8.5 (numpy version 1.18.4 and TensorFlow version 2.3.0), but it should run on higher versions as well.

That's it! rrQNet is ready to be used.

## Usage

To see the usage instructions, run `python rrQNet.py -h`

```

Usage: rrQNet.py [options]

Options:
  -h, --help  show this help message and exit
  -p PRE      precision matrix (npy format)
  -r RR       residue-residue contact map (rr format)
  -m MODEL    path to the model
  -L XL       top xL contacts in the contact matrix (default = 1)
  -t TGT      name of target

```

### File formats and parameters

- Precision matrix (-p): Precision matrix from a multiple sequence alignment can be obtained using [ResPRE](https://github.com/leeyang/ResPRE). For example, see `./example/input/T0869.npy`
- Contact map (-r): The first line contains the amino acid sequence followed by list of contact rows using a five-column format similar to CASP RR format. In each contact row, first two columns are the residue pairs in contact, third and fourth columns are lower and upper bounds of their distance (in Å) respectively, and fifth column is a real number indicating the probability of the two residues being in contact. For example, see `./examples/input/T0869.rr`   
- Model (-m): Path to the directory that contains trained model. For example, see `./model/rrQNet_55_40/`
- Contact cutoff (-L): To select top xL contacts, where L is the sequence length of protein. For example, use `-L 1` to select top L contacts. 
- Target (-t): Name of the target

### Test rrQNet

We give an example of running rrQNet on CASP12 FM target T0869.

Run `python rrQNet.py -p ./examples/input/T0869.out.npy -r ./examples/input/T0869.L.6.fl.respre.rr -m ./model/rrQNet_train_55_40/ -L 1 -t T0869.respre > out.txt`

The estimated quality score along with selected contacts is generated at `out.txt`. the output should look like [this](examples/output/T0869.txt)

rrQNet is very fast. On average it takes only a few seconds on a single core to run rrQNet. However, the running time depends on the sequence length of the target protein. For longer targets, it may take a few minutes to complete.

## Data

## Cite