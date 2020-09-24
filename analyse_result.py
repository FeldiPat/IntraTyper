import matplotlib.pyplot as plt
import numpy as np

common_types = ['$string$', '$boolean$', '$number$', '$any$', '$Array$', '$void$']


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
    rects1 = ax.bar(x - width / 2, top_1_acc, color='steelblue', width=width, label='Top-1')
    rects2 = ax.bar(x + width / 2, top_5_acc, color='orange', width=width, label='Top-5')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Accuracy')
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
        uncommon_top_1 = 0
        uncommon_top_5 = 0
        count = 0
        uncommon_count = 0
        for x in data:
            lx = x.split()
            if lx[0] != '$any$':
                if lx[0] == lx[1]:
                    top_1 += 1
                if int(lx[3]) != 0:
                    top_5 += 1
                count += 1
            if lx[0] not in common_types:
                if lx[0] == lx[1]:
                    uncommon_top_1 += 1
                if int(lx[3]) != 0:
                    uncommon_top_5 += 1
                uncommon_count += 1
        result = {'name': project, 'top_1': round(top_1 / count, 2), 'top_5': round(top_5 / count, 2), 'total': count,
                  'uc_1': round(uncommon_top_1 / uncommon_count, 2), 'uc_5': round(uncommon_top_5 / uncommon_count, 2),
                  'uc_total': uncommon_count}
        results.append(result)
        data.close()

        print("Model: " + project)
        print("Total Samples " + str(result.get('total')))
        print("Top 1 accuracy common: " + str(result.get('top_1')))
        print("Top 5 accuracy common: " + str(result.get('top_5')))
        print()
        print("Total Samples uncommon" + str(result.get('uc_total')))
        print("Top 1 accuracy uncommon: " + str(result.get('uc_1')))
        print("Top 5 accuracy uncommon: " + str(result.get('uc_5')))
        print()

    # plot the results
    labels = [results[0].get('name'), results[1].get('name')]
    top_1_acc = [results[0].get('top_1'), results[1].get('top_1')]
    top_5_acc = [results[0].get('top_5'), results[1].get('top_5')]
    uc_1_acc = [results[0].get('uc_1'), results[1].get('uc_1')]
    uc_5_acc = [results[0].get('uc_5'), results[1].get('uc_5')]

    # set width of bar
    barWidth = 0.2
    # Set position of bar on X axis
    r1 = np.arange(len(top_1_acc))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]

    # Make the plot
    fig, ax = plt.subplots()
    rects1 = ax.bar(r1, top_1_acc, color='steelblue', width=barWidth, edgecolor='white', label='Top-1 all')
    rects2 = ax.bar(r2, top_5_acc, color='deepskyblue', width=barWidth, edgecolor='white', label='Top-5 all')
    rects3 = ax.bar(r3, uc_1_acc, color='orange', width=barWidth, edgecolor='white', label='Top-1 uncommon')
    rects4 = ax.bar(r4, uc_5_acc, color='moccasin', width=barWidth, edgecolor='white', label='Top 5 uncommon')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Accuracy')
    ax.set_xlabel('Model')
    plt.xticks([r + 1.5 * barWidth for r in range(len(labels))], ['IntraTyper', 'DeepTyper'])
    ax.set_xticklabels(labels)
    ax.set_title("Intra-project comparison between IntraTyper and DeepTyper")
    ax.legend(loc='lower right')

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
    autolabel(rects3)
    autolabel(rects4)

    fig.tight_layout()

    plt.savefig("results/comparison")
    plt.figure(figsize=[10, 6])
    plt.show()


plotter_IT("results/intra-10000-200-300-google.txt",
           "results/intra-10000-200-300-tinymce.txt",
           "results/intra-10000-200-300-angular.txt")

plotter_comp("results/intra-10000-200-300-google.txt",
             "results/intra-DeepTyper.txt")
