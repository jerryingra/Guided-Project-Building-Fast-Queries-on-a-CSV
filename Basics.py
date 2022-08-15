#!/usr/bin/env python
# coding: utf-8

# # Guided Project Solution: Building Fast Queries on a CSV
# 
# ## Reading the Inventory
# 
# Use the `csv` module to read the `laptops.csv` file and separate the header from the rows.

# In[7]:


import csv

with open('laptops.csv') as f:
    reader = csv.reader(f)
    rows = list(reader)
    header = rows[0]
    rows = rows[1:]
    
print(header)
print(rows[:5])


# ## Inventory Class
# 
# Start implementing a class to represent the inventory. It get the name of the CSV file as argument and reads it into `self.header` and `self.rows`.

# In[8]:


class Inventory():
    
    def __init__(self, csv_filename):
        with open(csv_filename) as f:
            reader = csv.reader(f)
            rows = list(reader)
        self.header = rows[0]
        self.rows = rows[1:]
        for row in self.rows:
            row[-1] = int(row[-1])
            
inventory = Inventory('laptops.csv')
print(inventory.header)
print(len(inventory.rows))
        


# ## Finding a Laptop From the Id
# 
# Implement a `get_laptop_from_id()` function that given a laptop identifier find the row corresponding to that laptop.

# In[9]:


class Inventory():
    
    def __init__(self, csv_filename):
        with open(csv_filename) as f:
            reader = csv.reader(f)
            rows = list(reader)
        self.header = rows[0]
        self.rows = rows[1:]
        for row in self.rows:
            row[-1] = int(row[-1])
            
    def get_laptop_from_id(self, laptop_id):
        for row in self.rows:
            if row[0] == laptop_id:
                return row
        return None


# In[10]:


inventory = Inventory('laptops.csv')
print(inventory.get_laptop_from_id('3362737'))
print(inventory.get_laptop_from_id('3362736'))


# ## Improving Id Lookups
# Improve the time complexity of finding a laptop with a given id by precomputing a dictionary that maps laptop ids to rows.

# In[23]:


class Inventory():
    
    def __init__(self, csv_filename):
        with open(csv_filename) as f:
            reader = csv.reader(f)
            rows = list(reader)
        self.header = rows[0]
        self.rows = rows[1:]
        for row in self.rows:
            row[-1] = int(row[-1])
            
        self.id_to_row = {}
        for row in self.rows:
            self.id_to_row[row[0]] = row
            
    def get_laptop_from_id_fast(self, laptop_id):
        if laptop_id in self.id_to_row:
            return self.id_to_row[laptop_id]
        return None
            
    def get_laptop_from_id(self, laptop_id):
        for row in self.rows:
            if row[0] == laptop_id:
                return row
        return None


# ## Test the code:

# In[24]:


inventory = Inventory('laptops.csv')

print(inventory.get_laptop_from_id_fast('3362737'))
print('\n')
print(inventory.get_laptop_from_id_fast('3362736'))


# ## Comparing the Performance

# In[28]:


import time
import random

ids = [str(random.randint(1000000, 9999999)) for _ in range(10000)]

inventory = Inventory('laptops.csv')

total_time_no_dict = 0
for identifier in ids:
    start = time.time()
    inventory.get_laptop_from_id(identifier)
    end = time.time()
    total_time_no_dict += end - start 
    
total_time_dict = 0
for identifier in ids:
    start = time.time()
    inventory.get_laptop_from_id_fast(identifier)
    end = time.time()
    total_time_dict += end - start
    
    
print('No Dictionary Total Time:' + str(total_time_no_dict))
print('Dictionary Time: ' + str(total_time_dict))


# ## Analysis
# 
# The `get_laptop_from_id()` method has time complexity *O(R)* where *R* is the number of rows. In contrast, `get_laptop_from_id_fast()` has time complexity *O(1)*.
# 
# We got:
# 
#     0.5884554386138916
#     0.0024595260620117188
# 
# We can see a significant improve in performance. If we divide *0.588* by *0.002* we see that the new method is about *294* times faster for this input size.

# ## Two Laptop Promotion
# 
# Write a method that finds whether we can spend a given amount of money by purchasing either one or two laptops.

# In[29]:


class Inventory():
    
    def __init__(self, csv_filename):
        with open(csv_filename) as f:
            reader = csv.reader(f)
            rows = list(reader)
        self.header = rows[0]
        self.rows = rows[1:]
        for row in self.rows:
            row[-1] = int(row[-1])
            
        self.id_to_row = {}
        for row in self.rows:
            self.id_to_row[row[0]] = row
            
    def get_laptop_from_id_fast(self, laptop_id):
        if laptop_id in self.id_to_row:
            return self.id_to_row[laptop_id]
        return None
            
    def get_laptop_from_id(self, laptop_id):
        for row in self.rows:
            if row[0] == laptop_id:
                return row
        return None
    
    def check_promotion_dollars(self, dollars):
        for row in self.rows:
            if row[-1] == dollars:
                return True
        
        for row1 in self.rows:                    
            for row2 in self.rows:
                if row1[-1] + row2[-1] == dollars:
                    return True
        return False                               


# In[30]:


inventory = Inventory('laptops.csv')

print(inventory.check_promotion_dollars(1000))
print('\n')
print(inventory.check_promotion_dollars(442))


# ## Optimizing Laptop Premium

# In[36]:


class Inventory():
    
    def __init__(self, csv_filename):
        with open(csv_filename) as f:
            reader = csv.reader(f)
            rows = list(reader)
        self.header = rows[0]
        self.rows = rows[1:]
        for row in self.rows:
            row[-1] = int(row[-1])
            
        self.id_to_row = {}
        for row in self.rows:
            self.id_to_row[row[0]] = row
            
        self.prices = set()
        for row in self.rows:
            self.prices.add(row[-1])
            
    def get_laptop_from_id_fast(self, laptop_id):
        if laptop_id in self.id_to_row:
            return self.id_to_row[laptop_id]
        return None
            
    def get_laptop_from_id(self, laptop_id):
        for row in self.rows:
            if row[0] == laptop_id:
                return row
        return None
    
    def check_promotion_dollars(self, dollars):
        for row in self.rows:
            if row[-1] == dollars:
                return True
        
        for row1 in self.rows:                    
            for row2 in self.rows:
                if row1[-1] + row2[-1] == dollars:
                    return True
        return False   
    
    def check_promotion_dollars_fast(self, dollars):
        if dollars in self.prices:
            return True
        for price in self.prices:
            if dollars - price in self.prices:
                return True
        return False


# ## Test the code

# In[33]:


inventory = Inventory('laptops.csv')

print(inventory.check_promotion_dollars_fast(1000))
print('\n')
print(inventory.check_promotion_dollars_fast(442))


# ## Compaing Promotion Functions
# Compare the performance of both methods for the promotion.

# In[38]:


prices = [random.randint(100, 5000) for _ in range(100)] 

inventory = Inventory('laptops.csv')

total_time_no_set = 0
for value in prices:
    start = time.time()
    inventory.check_promotion_dollars(value)
    end = time.time()
    total_time_no_set += end - start
    
total_time_set = 0
for value in prices:
    start = time.time()
    inventory.check_promotion_dollars_fast(value)
    end = time.time()
    total_time_set += end - start
    
print(total_time_no_set)
print('\n')
print(total_time_set)


# ## Analysis
# 
# We got:
# 
#  0.7781209945678711
#  
#  0.0003719329833984375
#  
# We can see a significant improve in performance. If we divide `0.7781` by `0.0002` we see that the new method is about `2593` times faster for this input size.

# ## Finding Laptops Within a Budget

# In[ ]:


def row_price(row):
    return row[-1]

class Inventory():
    
    def __init__(self, csv_filename):
        with open(csv_filename) as f:
            reader = csv.reader(f)
            rows = list(reader)
        self.header = rows[0]
        self.rows = rows[1:]
        for row in self.rows:
            row[-1] = int(row[-1])
            
        self.id_to_row = {}
        for row in self.rows:
            self.id_to_row[row[0]] = row
            
        self.prices = set()
        for row in self.rows:
            self.prices.add(row[-1])
            
        self.rows_by_price = sorted(self.rows, key=row_price)
            
    def get_laptop_from_id_fast(self, laptop_id):
        if laptop_id in self.id_to_row:
            return self.id_to_row[laptop_id]
        return None
            
    def get_laptop_from_id(self, laptop_id):
        for row in self.rows:
            if row[0] == laptop_id:
                return row
        return None
    
    def check_promotion_dollars(self, dollars):
        for row in self.rows:
            if row[-1] == dollars:
                return True
        
        for row1 in self.rows:                    
            for row2 in self.rows:
                if row1[-1] + row2[-1] == dollars:
                    return True
        return False   
    
    def check_promotion_dollars_fast(self, dollars):
        if dollars in self.prices:
            return True
        for price in self.prices:
            if dollars - price in self.prices:
                return True
        return False
    
    def find_laptop_with_price(self, target_price):
        range_start = 0                                   
        range_end = len(self.rows_by_price) - 1                       
        while range_start < range_end:
            range_middle = (range_end + range_start) // 2  
            value = self.rows_by_price[range_middle][-1]
            if value == target_price:                            
                return range_middle                        
            elif value < target_price:                           
                range_start = range_middle + 1             
            else:                                          
                range_end = range_middle - 1 
        if self.rows_by_price[range_start][-1] != target_price:                  
            return -1                                      
        return range_start

