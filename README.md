# 507-final
This is my final project for SI 507. In this project, I mainly achieved a web crawler.

The basic API is https://api.tvmaze.com. If we want to search for some items, we need to use this one, https://api.tvmaze.com/search?q= and add the search item at the end.

There are mainly six steps for users to interact with the program, including the search category, narrowing down the category(two different kinds of presentations), showing the result and statistics(two different kinds of presentations), going to the result webpages, etc.

For the data structure, I used a Binary Search Tree. The tree has been used to store the data. For every tree node in the tree, the key is “language” and the value is the index of the data.

