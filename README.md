<h2>rrQNet</h2> 

rrQNet is a deep learning method for protein contact map quality estimation by evolutionary reconciliation.

## Installation

Installing rrQNet is very straightforward. The following instructions should work for 64-bit Linux system:

- Make sure you have Python with NumPy and TensorFlow installed. rrQNet has been tested on Python 3.8.5 (numpy version 1.18.4 and TensorFlow version 2.3.0), but it should run on higher versions as well.
- Download and unzip the model from [here](https://doi.org/10.5281/zenodo.6784573)

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
  -t TGT      name of target

```

### File formats and parameters

- Precision matrix (-p): Precision matrix is obtained from multiple sequence alignment. For example, see `./example/input/T0968s2.out.npy`
- Contact map (-r): The first line contains the amino acid sequence followed by list of contact rows using a five-column format similar to CASP RR format. In each contact row, first two columns are the residue pairs in contact, third and fourth columns are lower and upper bounds of their distance (in Å) respectively, and fifth column is a real number indicating the probability of the two residues being in contact. For example, see `./examples/input/T0968s2.L.6.fl.metapsicov.rr`   
- Model (-m): Path to the directory that contains trained model. For example, see `./model/rrQNet_train_55_40/`
- Target (-t): Name of the target

### Test rrQNet

We give an example of running rrQNet on CASP12 FM target T0869.

Run `python rrQNet.py -p ./examples/input/T0968s2.out.npy -r ./examples/input/T0968s2.L.6.fl.metapsicov.rr -m ./model/rrQNet_train_55_40/ -t T0968s2.metapsicov > out.txt`

The estimated quality score along with selected contacts is generated at `out.txt`. the output should look like [this](examples/output/T0968s2.metapsicov.txt)

rrQNet is very fast. On average it takes only a few seconds on a single core to run rrQNet. However, the running time depends on the sequence length of the target protein. For longer targets, it may take a few minutes to complete.

<!-- ## Data

1. Input files can be found [here](http://sanger.cse.eng.auburn.edu/rrQNet/downloads/inputs.tar.gz)
2. Output files can be found [here](http://sanger.cse.eng.auburn.edu/rrQNet/downloads/outputs.tar.gz) -->

## Cite

If you find rrQNet useful, please cite our [PROTEINS paper](https://onlinelibrary.wiley.com/doi/10.1002/prot.26394).
