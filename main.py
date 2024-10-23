"""
Stock market prediction using Markov chains.
"""

import comp140_module3 as stocks
import random 

### Model

def markov_chain(data, order):
    """
    Create a Markov chain with the given order from the given data.

    inputs:
        - data: a list of ints or floats representing previously collected data
        - order: an integer repesenting the desired order of the markov chain

    returns: a dictionary that represents the Markov chain
    """
    
    #helper function
    def dictionary_of_probabilities(list_of_values):
        """
        Create a dictionary that represents each value to its probability within the
        the given values
        input: a list of ints or floats representing its occurence in a data set
        """
        probabilities = {}
        for value in list_of_values:
            if(value in probabilities):
                probabilities[value] += 1
            else:
                probabilities[value] = 1
        for num, occurence in probabilities.items():
            probabilities[num] = occurence/len(list_of_values)
        return probabilities
    
    #create markov chain that will be returned
    chain = {}
    position = 0       
    
    #iterate through every value in data except for the last "order" values		
    while(position < len(data)-order) :
        #create the tuple containing all "order" values
        lists = []     
        for element in range(position,position + order):
            lists.append(data[element])
        tuple_element = tuple(lists)
          
          #add or update a key (the tuple) to have a value
          #containing a list of each number after it          
        if tuple_element in chain:       
            chain[tuple_element].append(data[position+order])
        else:
            chain[tuple_element] = [data[position+order]]            
        position += 1
        
    #find probabilities of each occurence in the values    
    for key,value in chain.items():
        chain[key] = dictionary_of_probabilities(value)
        
    return chain 
    

### Predict

def predict(model, last, num):
    """
    Predict the next num values given the model and the last values.
    inputs:
        - model: a dictionary representing a Markov chain
        - last: a list (with length of the order of the Markov chain)
                representing the previous states
        - num: an integer representing the number of desired future states

    returns: a list of integers that are the next num states
    """
    next_nums = []
    last_nums = list(last)
    while(len(next_nums) < num):
        if(tuple(last) in model):
            start = 0
            probability = random.random()
            for probabilities in model[tuple(last_nums)]:
                if probability > model[tuple(last_nums)][probabilities] + start:
                    start= start + model[tuple(last_nums)][probabilities]
                    continue
                last_num = probabilities
                break
        else:
            last_num = random.randint(0,3)
        next_nums.append(last_num)
        last_nums.pop(0)
        last_nums.append(last_num) 
                     
    return next_nums

### Error

def mse(result, expected):
    """
    Calculate the mean squared error between two data sets.

    The length of the inputs, result and expected, must be the same.

    inputs:
        - result: a list of integers or floats representing the actual output
        - expected: a list of integers or floats representing the predicted output

    returns: a float that is the mean squared error between the two data sets
    """
    difference_squared = 0 
    for num in range(0, len(result)):
        difference_squared += (expected[num] - result[num])**2

    return difference_squared/len(result)


### Experiment

def run_experiment(train, order, test, future, actual, trials):
    """
    Run an experiment to predict the future of the test
    data given the training data.

    inputs:
        - train: a list of integers representing past stock price data
        - order: an integer representing the order of the markov chain
                 that will be used
        - test: a list of integers of length "order" representing past
                stock price data (different time period than "train")
        - future: an integer representing the number of future days to
                  predict
        - actual: a list representing the actual results for the next
                  "future" days
        - trials: an integer representing the number of trials to run

    returns: a float that is the mean squared error over the number of trials
    """
    model = markov_chain(train,order)
    mse_value = 0
    trial = 0 
    while(trial < trials):
        predicted_future = predict(model, test, future)    
        mse_value += mse(actual, predicted_future)
        trial += 1
    return mse_value/trials


### Application

def run():
    """
    Run application.
    """
    # Get the supported stock symbols
    symbols = stocks.get_supported_symbols()

    # Get stock data and process it

    # Training data
    changes = {}
    bins = {}
    for symbol in symbols:
        prices = stocks.get_historical_prices(symbol)
        changes[symbol] = stocks.compute_daily_change(prices)
        bins[symbol] = stocks.bin_daily_changes(changes[symbol])

    # Test data
    testchanges = {}
    testbins = {}
    for symbol in symbols:
        testprices = stocks.get_test_prices(symbol)
        testchanges[symbol] = stocks.compute_daily_change(testprices)
        testbins[symbol] = stocks.bin_daily_changes(testchanges[symbol])

    # Display data
  
    stocks.plot_daily_change(changes)
    stocks.plot_bin_histogram(bins)

    # Run experiments
    orders = [1, 3, 5, 7, 9]
    ntrials = 500
    days = 5

    for symbol in symbols:
        print(symbol)
        print("====")
        print("Actual:", testbins[symbol][-days:])
        for order in orders:
            error = run_experiment(bins[symbol], order,
                                   testbins[symbol][-order-days:-days], days,
                                   testbins[symbol][-days:], ntrials)
            print("Order", order, ":", error)
        print()
#to test
run()
