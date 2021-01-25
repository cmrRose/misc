# Python 3.6.10
# Caroline Rose | cmr.rose@gmail.com | 01-24-2021


# NOTES:
# This script relies on certain assumptions; for instance, it relies on the product name including the exact text "Volume x" (e.g., "Volume 4") to count up the correct volume. If it can't find that text in the product name, it counts the product as "volume unspecified." 

# ++++++++++++ ~ SCRIPT OPTIONS ~  ++++++++++++
# Give it a file as downloaded from BigCartel. Place it in the same folder with the script. 
# File to manipulate:
orders_csv = "orders2020.csv"

# use "YES" to aggregate to just one column per volume.
# (NOT IMPLEMENTED; need to do this) use "NO" to add column for each unique product; 
byvolume = "YES" 

# ++++++++++++ ~ end script options ~  ++++++++++++ 


# Import a library to work with csv files.
import pandas as pd

# setup for pandas 
def front(self, n):
    return self.iloc[:, :n]

def back(self, n):
    return self.iloc[:, -n:]

pd.DataFrame.front = front
pd.DataFrame.back = back



# read the file into a pandas dataframe. 
df = pd.read_csv(orders_csv)

# create an empty list to hold the product names. 
productnames = []
newcolumnslist = []


# *************** DEFINE FUNCTIONS *****************
def evaluatecolumns(productname):
    #this function creates columns as needed and returns the proper column name for the quantity to be placed in.
    
    if byvolume == "YES":

        if "Volume 1" in productname:
            if 'Vol1' not in df:
                print('create Vol1 column.')
                df['Vol1']=''
            return "Vol1"
        
        elif "Volume 2" in productname:
            if 'Vol2' not in df:
                print('create Vol2 column.')
                df['Vol2']=''
            return "Vol2"
        
        elif "Volume 3" in productname:
            if 'Vol3' not in df:
                print('create Vol3 column.')
                df['Vol3']=''
            return "Vol3"
        
        elif "Volume 4" in productname:
            if 'Vol4' not in df:
                print('create Vol4 column.')
                df['Vol4']=''
            return "Vol4"
        
        elif "Volume 5" in productname:
            if 'Vol5' not in df:
                print('create Vol5 column.')
                df['Vol5']=''
            return "Vol5"
        else:
            if 'Volume unspecified' not in df:
                print('create Volume unspecified column.')
                df['Volume unspecified']=''
            return "Volume unspecified"


    elif byvolume == "NO":

        # this option is still in progress. 

         # push name to to the list of product names and identify/create a column for it. 
        if listingdict[productname] not in productnames:
                productnames.append(listingdict[productname])

        if productname not in df:
            print('create column ', productname) 
                
    
# **********************  end function defs  **********************  



#iterate through every row's items and isolate the product name. 
for ind in df.index:
    
    # just the items property from this individual csv row. 
    items = df['Items'][ind]
    
   # this will produce a list of the individual product listing strings, which each have one product name. 
    product_listings = items.split(";")

    # for this row, the new numbers to be assigned will be saved into the following dictionary of columnname-quantity pairs. 
    updatenumbers = {} 

    for listing in product_listings:
        #p is a pipe-delimited string with a product name.
        #turn the string into a dictionary.      
        listingdict = dict(item.split(":", 1) for item in listing.split("|"))


        #print("\r\nproduct name is: ", listingdict['product_name'])
        #print("quantity is: ", listingdict['quantity'])

        # create a column if necessary and return the proper column name for adding the quantity. 
        columnassign = evaluatecolumns(listingdict['product_name'])
        #quantity as an integer. 
        quantityassign = int(listingdict['quantity'])

        #print("add quantity ", quantityassign, "to column", columnassign)

        if columnassign in updatenumbers:
            updatenumbers[columnassign] += updatenumbers.get(updatenumbers[columnassign], quantityassign)
        else:
            updatenumbers[columnassign] = quantityassign

    # update the row in the data frame to the numbers determined above. 
    print("update", updatenumbers)

    for u in updatenumbers:
        # print("for this row, update column '", u, "' to the value", updatenumbers[u],".", "\r\n")
        
        df[u][ind] = updatenumbers[u]
        #df.loc[:, (u, ind)]
      


#print("List of ",len(productnames)," unique product names: ", productnames)

# print the end of the table. 
print(df.back(5))

# save back to the csv file. 
df.to_csv(orders_csv, index=False)
 
