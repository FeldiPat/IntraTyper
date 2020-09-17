import matplotlib.pyplot as plt
import numpy as np


def plotter_IT(f1, f2, f3):
    file_list = [f1, f2, f3]
    results = []
    for file in file_list:
        project = file.split('-')[4].rstrip('.txt')
        data = open(file)
        top_1 = 0
        top_5 = 0
        count = 0
        for x in data:
            lx = x.split()
            if lx[0] != '$any$':
                if lx[0] == lx[1]:
                    top_1 += 1
                if int(lx[3]) != 0:
                    top_5 += 1
                count += 1
        result = {'name': project, 'top_1': round(top_1 / count, 2), 'top_5': round(top_5 / count, 2), 'total': count}
        results.append(result)
        data.close()

        print("Project: " + project)
        print("Total Samples " + str(result.get('total')))
        print("Top 1 accuracy: " + str(result.get('top_1')))
        print("Top 5 accuracy: " + str(result.get('top_5')))
        print()

    # plot the results
    labels = [results[0].get('name'), results[1].get('name'), results[2].get('name')]
    top_1_acc = [results[0].get('top_1'), results[1].get('top_1'), results[2].get('top_1')]
    top_5_acc = [results[0].get('top_5'), results[1].get('top_5'), results[2].get('top_5')]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, top_1_acc, width, label='Top-1')
    rects2 = ax.bar(x + width / 2, top_5_acc, width, label='Top-5')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Accuracy in %')
    ax.set_xlabel('Project family')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Evaluation of IntraTyper")
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()
    plt.savefig("results/IntraTyper")
    plt.show()


def plotter_comp(f1, f2):
    file_list = [f1, f2]
    results = []
    for file in file_list:
        if file.startswith("results/inter") or file.startswith("results/intra-DeepTyper"):
            project = "DeepTyper"
        else:
            project = "IntraTyper"
        data = open(file)
        top_1 = 0
        top_5 = 0
        count = 0
        for x in data:
            lx = x.split()
            if lx[0] != '$any$':
                if lx[0] == lx[1]:
                    top_1 += 1
                if int(lx[3]) != 0:
                    top_5 += 1
                count += 1
        result = {'name': project, 'top_1': round(top_1 / count, 2), 'top_5': round(top_5 / count, 2), 'total': count}
        results.append(result)
        data.close()

        print("Project: " + project)
        print("Total Samples " + str(result.get('total')))
        print("Top 1 accuracy: " + str(result.get('top_1')))
        print("Top 5 accuracy: " + str(result.get('top_5')))
        print()

    # plot the results
    labels = [results[0].get('name'), results[1].get('name')]
    top_1_acc = [results[0].get('top_1'), results[1].get('top_1')]
    top_5_acc = [results[0].get('top_5'), results[1].get('top_5')]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, top_1_acc, width, label='Top-1')
    rects2 = ax.bar(x + width / 2, top_5_acc, width, label='Top-5')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Accuracy in %')
    ax.set_xlabel('Model')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Comparison between IntraTyper and DeepTyper on the google test set")
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()

    plt.savefig("results/comparison")
    plt.show()


plotter_IT("results/intra-10000-200-300-google.txt",
           "results/intra-10000-200-300-tinymce.txt",
           "results/intra-10000-200-300-angular.txt")

plotter_comp("results/intra-10000-200-300-google.txt",
             "results/intra-DeepTyper.txt")
