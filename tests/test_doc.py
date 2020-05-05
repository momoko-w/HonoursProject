import timeit


def time_fetching_data():
        print("Time to fetch data for Green Belt - Moral Maze")

        setup = "from controllers import dataController as dataCtrl"
        code = """dataCtrl.fetchOrganisedData("Green Belt - Moral Maze")"""
        print(timeit.timeit(setup=setup, stmt=code, number=100)/100)


def time_calculating_tab_data():
    print("Time to calculate results for data in tab for Green Belt - Moral Maze")
    setup = "import mainController"
    code = """mainController.calculate_tab_data("Green Belt - Moral Maze")"""
    print(timeit.timeit(setup=setup, stmt=code, number=10)/10)


# get performance for fetching data
time_fetching_data()

# get performance for calculating data for the tab (includes fetching data)
time_calculating_tab_data()