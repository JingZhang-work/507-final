import requests
import json
import os
import tree_class
import plotly
import plotly.graph_objs as go
import webbrowser

# Create the cahce file
def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2):
    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)

# Open the cache file
def open_cache():
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = requests.get("https://api.tvmaze.com/search/shows?q=dog").json()
        write_json("cache.json", cache_dict)
        abs_path_json = os.path.dirname(os.path.abspath(__file__))
        CACHE_FILENAME = os.path.join(abs_path_json, "cache.json")
    return cache_dict

# Initiate a tree, key is the language(str), value is the index(int)
def initiateTree(DOG_CACH):
    tree = tree_class.BinarySearchTree()
    # tree.put(DOG_CACHE[0]["score"], DOG_CACHE[0]["show"]["name"])
    for i in range(len(DOG_CACHE)):
        tree.put(DOG_CACHE[i]["show"]["language"], i)
    return tree

# 2.1. Prepare for the x,y of Pei chart
def getPieChart(tree):
    language_count = {}
    inorderLanguage(tree.root, language_count)
    x, y = [], []
    for k, v in language_count.items():
        x.append(k)
        y.append(len(v))
    return x, y, language_count

def inorderLanguage(node, count):
    if not node:
        return
    inorderLanguage(node.leftChild, count)
    if node.key not in count:
        count[node.key] = set()
    count[node.key].add(node.payload)
    inorderLanguage(node.rightChild, count)

# 2.2
def getShowsLanguage(language_input, language_dict, cache):
    language_input = language_input[0].upper() + language_input[1:]
    shows = language_dict[language_input]
    results = []
    for show in shows:
        results.append(cache[show])
    return results

# 3.1
def getBarChart(shows_ls):
    shows_status_dict = {}
    for show in shows_ls:
        sts = show["show"]["status"]
        if sts not in shows_status_dict:
            shows_status_dict[sts] = []
        shows_status_dict[sts].append(show)
    x, y = [], []
    for k, v in shows_status_dict.items():
        x.append(k)
        y.append(len(v))
    return x, y, shows_status_dict

# 3.2
def getShowsStatus(status_input, shows_dict):
    status_input = status_input.lower()
    if status_input == "running" or status_input == "Running":
        return shows_dict['Running']
    elif status_input == "ended" or status_input == "Ended":
        return shows_dict['Ended']
    else:
        return shows_dict['To Be Determined']

# 4.1
def getScatterChart(status_shows):
    x, y = [], []
    for i in range(len(status_shows)):
        show = status_shows[i]
        x_name = str(i + 1) + "." + show["show"]["name"]
        y_score = show["score"]
        x.append(x_name)
        y.append(y_score)
    return x, y

# 4.2
def getShow(show_input, status_shows):
    show_index = int(show_input) - 1
    return status_shows[show_index]

# 5.
def getThreeD(show_info):
    x, y, z = [0], [0], [0]
    x.append(show_info["score"])
    y.append(show_info["show"]["runtime"])
    z.append(show_info["show"]["weight"])
    return x, y, z







if __name__ == "__main__":

    ###########################################    Set Up     #############################################

    # Get the data and cache it
    # response = requests.get("https://api.tvmaze.com/search/shows?q=dog").json()
    # write_json("cache.json", response)

    # Get the cache file
    abs_path_json = os.path.dirname(os.path.abspath(__file__))
    CACHE_FILENAME = os.path.join(abs_path_json, "cache.json")
    DOG_CACHE = open_cache()

    # Initiate the tree. For every node, key is the score, val is the name
    tree = initiateTree(DOG_CACHE)

    ########################################### End of Setting #############################################


    # 1. Users search for "Dogs". It will show the number of shows realted to "dogs".
    search_input = input("Enter a search term, or 'exit' to quit: ")
    if search_input.lower() == 'exit':
        pass
    else:
        print(f"There are {tree.length()} shows realted to the {search_input}")



    # 2.1 Show different languages of these shows. -- Pie chart
    language_input = input("Do you want to see the layout of languages of these shows(y/n): ")
    language, l_count, language_count = getPieChart(tree)
    if language_input.lower() == 'n':
        pass
    else:
        pie_data = go.Pie(labels=language, values=l_count, hole=0.2, textfont=dict(size=12, color="white"))
        pie_layout = go.Layout(title="Languages of Shows")
        fig = go.Figure(data=pie_data, layout=pie_layout)
        fig.write_html("LanguagesOfShows.html", auto_open=True)

    # 2.2 Ask which language users want to choose: English/ Swedish/ Korean/ Polish
    language_input = input("Which language do you want to choose: ")
    language_shows = getShowsLanguage(language_input, language_count, DOG_CACHE)
    print(f"There are {len(language_shows)} shows of {language_input} language.")



    # 3.1 Show the status of these shows. -- Bar chart
    status_input = input("Do you want to see the layout of status of these shows(y/n): ")
    status, shows_num, shows_dict = getBarChart(language_shows)
    if status_input.lower() == 'n':
        pass
    else:
        bar_data = go.Bar(x=status, y=shows_num)
        basic_layout = go.Layout(title="Status of Shows")
        fig = go.Figure(data=bar_data, layout=basic_layout)
        fig.write_html("StatusOfShows.html", auto_open=True)

    # 3.2 Ask which status users want to choose: Running/ Ended/ To be Determined
    status_input = input("Which status do you want to choose: ")
    status_shows = getShowsStatus(status_input, shows_dict)
    print(f"There are {len(status_shows)} shows of this {status_input} status.")



    # 4.1 Show the scores of these shows. -- Scatter chart
    score_input = input("Do you want to see the layout of scores of these shows(y/n): ")
    shows_name, scores = getScatterChart(status_shows)
    if score_input.lower() == 'n':
        pass
    else:
        scatter_data = go.Scatter(x=shows_name, y=scores, mode="markers")
        basic_layout = go.Layout(
                        title="Shows and Scores",
                        xaxis_title = "Shows' Names",
                        yaxis_title = "Scores")
        fig = go.Figure(data=scatter_data, layout=basic_layout)
        fig.write_html("scatter.html", auto_open=True)

    # 4.2 Ask which show they want to watch
    print(f"There are {len(shows_name)} shows in your choosen category and the scores has been showed for each of them.")
    show_input = input("Which show do you want to know more? Please input the number of the show: ")
    choosen_show = getShow(show_input, status_shows)



    # 5. Show the statistics of this show
    statics_input = input("Do you want to see more information about this show(y/n): ")
    if statics_input.lower() == 'n':
        pass
    else:
        x, y, z = getThreeD(choosen_show)
        trace1 = go.Scatter3d(x=x, y=y, z=z, mode="markers")
        data = [trace1]
        fig = go.Figure(data=data)
        fig.write_html("3d.html", auto_open=True)



    # 6. Ask whether want to open it in browser
    browser_input = input("Do you want to go to the webpage for more details(y/n): ")
    if browser_input.lower() == 'n':
        pass
    else:
        webbrowser.open(choosen_show["show"]["url"])

    print("Bye!")


