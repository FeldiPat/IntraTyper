import matplotlib.pyplot as plt
import numpy as np


def plotter(file):
    data = open(file)
    any_dt, all_dt = 0, 0
    any5_dt, all5_dt = 0, 0
    any_count, all_count = 0, 0
    for x in data:
        lx = x.split()
        if lx[0] != '$any$':
            if lx[0] == lx[1]:
                any_dt += 1
            if int(lx[3]) != 0:
                any5_dt += 1
            any_count += 1
        if lx[0] == lx[1]:
            all_dt += 1
        if int(lx[3]) != 0:
            all5_dt += 1
        all_count += 1
    data.close()

    dt1_acc = any_dt / any_count
    dt5_acc = any5_dt / any_count
    print("Total Samples without any: " + str(any_count))
    print("Top 1 accuracy of DeepTyper: " + str(dt1_acc))
    print("Top 5 accuracy of DeepTyper: " + str(dt5_acc))

    print()

    print("Total Samples with any: " + str(all_count))
    print("Top 1 accuracy of DeepTyper: " + str(all_dt / all_count))
    print("Top 5 accuracy of DeepTyper: " + str(all5_dt / all_count))

    # plot the results
    fig, ax = plt.subplots()
    labels = ['DeepTyper-Top1', 'DeepTyper-Top5']
    accuracies = [dt1_acc, dt5_acc]
    ax.bar(labels, accuracies, color=['c', 'g'])

    x = np.arange(len(labels))  # the label locations

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Accuracy')
    ax.set_title('Accuracies without any')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    plt.show()


plotter("results/evaluation-GRU-3500-300-650-google.txt")
