# IntraTyper

This repository contains the code and replication scripts for IntraTyper, a modified version of the deep learning type inferring tool [DeepTyper by Hellendoorn et al. (2018)](https://github.com/DeepTyper/DeepTyper).
DeepTyper has been trained and evaluated on a set of different projects, a so-called inter-project environment.
In contrast to that, IntraTyper is trained and evaluated in an intra-project setting.
This means that IntraTyper is specifically tailored for one project.
As the results of the experiments show, due to this specific setting, the tool excels at predicting rather uncommon, project-specific types. 

# Experiment replication

IntraTyper uses the [CNTK library](https://docs.microsoft.com/en-us/cognitive-toolkit/).
Therefore, an environment which supports CNTK is necessary.
Unfortunately, CNTK runs natively only on Windows.

1. Execute the bash script `data/cloner.sh`. This will clone all the repositories mentioned in the `data/repo-SHAs.txt` file and reset them to the SHA commits as of February 28. 2018.
2. Copy the created `data/Repos` directory and name it `data/Repos-cleaned`.
3. Run `node CleanRepos.js`. This will create corresponding tokenized data and type (`*.ttokens`) files in Repos-cleaned and scrapes all user-added type annotations of the source code and stores these in `*.ttokens.pure` files.
4. Run `node GetTypes.js`. This will create three directories. In each directory, each line corresponds to a TypeScript file. Each line contains space-separated TypeScript tokens followed by the corresponding space-separated types. A tab separates the source-tokens and type-tokens.
   - `outputs-all` contains data in which every identifier is annotated with its inferred type. This will be used for training data.
   - `outputs-pure` contains only the real user-added type annotations for the TypeScript code (and `no-type` elsewhere); this is used for evaluation (GOLD data)
   - `outputs-checkjs` contains the TSc+CheckJS inferred types for every identifier. This can be used for comparing performance with TSc+CheckJS.
5. In the following, choose between the `intra-xyz.py` and `inter-xyz.py` scripts, depending on which setting you want to build. Hereafter, for simplicity, the `intra` scripts are used but can always be replaced with the `inter` scripts.
6. Run `intra_data_split.py` to create an 80% train, 10% valid and 10% test split, as well as source and target vocabularies. This will also create the file `test-projects.txt` which contains all the projects/source files chosen for the test split in the inter-project/intra-project setting respectively.
7. Convert the train/valid/test data to CNTK compatible `.ctf input files by using [CNTK's txt2ctf script](https://github.com/microsoft/CNTK/blob/master/Scripts/txt2ctf.py):
```
python txt2ctf.py --map data/source_wl data/target_wl --input data/train.txt --output data/train.ctf
python txt2ctf.py --map data/source_wl data/target_wl --input data/valid.txt --output data/valid.ctf
python txt2ctf.py --map data/source_wl data/target_wl --input data/test.txt --output data/test.ctf
```
9. Adjust the epoch size of `intra_infer.py` and `intra_evaluation.py` according to the output of `intra_data_split.py` in the line "Overall tokens: xyz train".
10. Run `intra_infer.py` to train the neural net over 10 epochs.
11. Choose the model with the best evaluation error and provide its path to the `model_file` variable in `intra_evaluation.py`.
12. Run `intra_evaluation.py` to let the model predict the corresponding types in the test data set. The results are written to the `results` directory in a txt file. The txt file contains four columns which are defined in the following way: true type | prediction | confidence of prediction | rank of prediction
13. To get a plot of the prediction-accuracies, run the script `analyze_result.py`.
