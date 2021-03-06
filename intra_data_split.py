import os
import random

random.seed(42)

data_dir = "data/"
in_dir = data_dir + "outputs-all/"
min_source_vocab = 3  # cut off source vocabulary at 10 token occurrences
min_target_vocab = 3  # cut off target vocabulary at 10 token occurrences
minibatchMaxSize = 10000  # cut off files with less than x characters
family = "angular"  # select project family for intra-setting
include_JS = False

file_count = 0
project_sizes = []
for project in os.listdir(in_dir):
    if "DefinitelyTyped" in project:
        continue
    if os.stat(in_dir + "/" + project).st_size == 0:
        continue
    file_count += 1

    source_tokens = []
    target_tokens = []

    # count source tokens of each project with same suffix
    with open(in_dir + "/" + project, "r", encoding="utf-8") as f:
        content = [line.strip() for line in f]
        for ix, line in enumerate(content):  # iterate over each line in the current sourcefile
            if len(line) == 0:
                continue
            parts = line.split("\t")  # split in source and target tokens
            if len(parts) < 2:
                continue
            source_tokens += parts[0].split(' ')
            target_tokens += parts[1].split(' ')

    if source_tokens[1] == "'js'" and not include_JS:
        continue
    if len(source_tokens) != len(target_tokens):
        continue

    suffix = project.split("__")[0].lower()
    proj_tuple = (suffix, len(source_tokens))
    for tuple in project_sizes:
        if tuple[0] == suffix:
            size = len(source_tokens) + tuple[1]
            proj_tuple = (suffix, size)
            project_sizes.pop()
    project_sizes.append(proj_tuple)

big10 = []
for tuple in project_sizes:
    if len(big10) < 10:
        big10.append(tuple)
    else:
        big10 = sorted(big10, key=lambda tuple: tuple[1])
        if big10[0][1] < tuple[1]:
            big10[0] = tuple

# Write biggest 10 files in data/biggest10.txt
with open(data_dir + "biggest10.txt", "w+") as f:
    for project in big10:
        f.write(project[0])
        f.write("\t")
        f.write(str(project[1]))
        f.write("\n")

tenth = file_count // 10
indices = list(range(file_count))
random.shuffle(indices)
train_indices = indices[:(8 * len(indices)) // 10]
valid_indices = indices[(8 * len(indices)) // 10:(9 * len(indices)) // 10]
test_indices = indices[(9 * len(indices)) // 10:]

train_sources = []
train_targets = []
valid_sources = []
valid_targets = []
test_sources = []
test_targets = []

# collect all source code lines of the selected project family
content = []
for project in os.listdir(in_dir):
    if "DefinitelyTyped" in project:
        continue
    if os.stat(in_dir + "/" + project).st_size == 0:
        continue
    if not project.lower().startswith(family):
        continue
    with open(in_dir + "/" + project, "r", encoding="utf-8") as f:
        content = content + [line.strip() for line in f]  # each line corresponds to one sourcefile

# split dataset into training, validation and test set
for ix, line in enumerate(content):  # iterate over each sourcode-line in the project
    if len(line) == 0:
        continue
    parts = line.split("\t")  # split in source and target tokens
    if len(parts) < 2:
        continue
    source_tokens = ["<s>"] + parts[0].split(' ') + ["</s>"]
    target_tokens = ["O"] + parts[1].split(' ') + ["O"]
    if source_tokens[1] == "'js'" and not include_JS:
        continue
    if len(source_tokens) != len(target_tokens):
        print("Different lengths at line %d!" % ix)
        print("%d, %d" % (len(source_tokens), len(target_tokens)))
        break
    if len(source_tokens) > minibatchMaxSize:
        continue
    # split source files into training/validation/test
    if ix in train_indices:
        train_sources.append(source_tokens)
        train_targets.append(target_tokens)
    elif ix in valid_indices:
        valid_sources.append(source_tokens)
        valid_targets.append(target_tokens)
    elif ix in test_indices:
        with open("data/intra_test_code-" + family + ".txt", 'a+') as t_code:
            t_code.write(" ".join(source_tokens))
            t_code.write("\n")
        test_sources.append(source_tokens)
        test_targets.append(target_tokens)

print("Statistics for project family: " + family)
print("Train files: %d" % len(train_sources))
print("Validation files: %d" % len(valid_sources))
print("Test files: %d" % len(test_sources))

# Vocabularies
# count the occurrence of each source and target token
source_counts = dict()
target_counts = dict()
for source in train_sources:
    for t in source:
        source_counts[t] = source_counts.get(t, 0) + 1
for target in train_targets:
    for t in target:
        target_counts[t] = target_counts.get(t, 0) + 1

# include source tokens until count < threshold
source_words = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)
source_cutoff = 0
for ix, (_, count) in enumerate(source_words):
    source_cutoff = ix
    if count < min_source_vocab:
        break
source_words = source_words[:source_cutoff]
source_word_vocab = set([word for word, _ in source_words])
if "<s>" not in source_word_vocab:
    source_words.append(("<s>", 0))
    source_word_vocab.add("<s>")
if "</s>" not in source_word_vocab:
    source_words.append(("</s>", 0))
    source_word_vocab.add("</s>")
source_words.append(("_UNKNOWN_", 0))
source_word_vocab.add("_UNKNOWN_")

# include target tokens until count < threshold
target_words = sorted(target_counts.items(), key=lambda x: x[1], reverse=True)
target_cutoff = 0
for ix, (_, count) in enumerate(target_words):
    target_cutoff = ix
    if count < min_target_vocab:
        break
target_words = target_words[:target_cutoff]
target_word_vocab = set([word for word, _ in target_words])

with open(data_dir + "intra_source_wl-" + family, "w", encoding="utf-8") as out:
    for name, count in source_words:
        out.write(name)
        out.write("\n")

with open(data_dir + "intra_target_wl-" + family, "w", encoding="utf-8") as out:
    for name, count in target_words:
        out.write(name)
        out.write("\n")

print("Size of source vocab: %d" % len(source_words))
print("Size of target vocab: %d" % len(target_words))

# Output files
print("Writing train/valid/test files")


def write(wfile, sources, targets):
    with open(wfile, "w", encoding="utf-8") as f:
        token_count = 0
        for i in range(len(sources)):
            source = sources[i]
            target = targets[i]
            source_tokens = [token if token in source_word_vocab else '_UNKNOWN_' for token in source]
            target_tokens = [token if token in target_word_vocab else '$any$' for token in target]
            if len(source_tokens) != len(target_tokens):
                print("Different lengths at line %d!" % ix)
                print("%d, %d" % (len(source_tokens), len(target_tokens)))
            token_count += len(source_tokens)
            f.write(" ".join(source_tokens))
            f.write("\t")
            f.write(" ".join(target_tokens))
            f.write("\n")
    return token_count


train_file = data_dir + "intra_train-" + family + ".txt"
valid_file = data_dir + "intra_valid-" + family + ".txt"
test_file = data_dir + "intra_test-" + family + ".txt"
train_tokens = write(train_file, train_sources, train_targets)
valid_tokens = write(valid_file, valid_sources, valid_targets)
test_tokens = write(test_file, test_sources, test_targets)

print("Overall tokens: %d train, %d valid and %d test" % (train_tokens, valid_tokens, test_tokens))
