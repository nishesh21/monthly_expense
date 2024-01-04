
#file_path_dec = "dec_bank2.csv"
#result_dec = analyze_monthly_expenses(file_path_dec)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import warnings
st.set_option('deprecation.showPyplotGlobalUse', False)

warnings.filterwarnings("ignore")

def analyze_monthly_expenses(uploaded_file):
    # Load the CSV file from the uploaded file
    df = pd.read_csv(uploaded_file)

    # Additional preprocessing steps
    #df["Date2"] = pd.to_datetime(df['Date'], format='%d/%m/%y', dayfirst=True) #for december
    df["Date2"]=pd.to_datetime(df['Date'], format='%d/%m/%Y', dayfirst=True) #for other months

    # Function to extract name from narration
    def extract_name(narration):
        if "UPI" in narration:
            match = re.search(r'UPI-(.*?)-', narration)
            if match:
                return match.group(1).strip()
        elif "SEVEN MENTOR" in narration:
            return "Salary"
        elif "NWD" in narration:
            return "ATM Deduction"
        elif "BILLPAY" in narration:
            return "Credit Card Bill"
        elif "NPS" in narration:
            return "Nps Investment"
        else:
            return "Auto Deduction"

    # Apply extract_name to create a 'Name' column
    df["Name"] = df["Narration"].apply(extract_name)

    # Categorization rules and other analysis steps
    # ... (same as your original script)

    # Categorization rules
    categories = {

    'Groceries/Sweets': ['grocery',"fresh signature pune",'supermarket', "reliance", "zepto", "drogheria sellers pr", "star market", "kisankonnect", "fine foods aundh","trent hypermarket pv","chitale bandhu mitha","sai fruit","narendra ratnaram pa","groceries"],
    "Online Food": ["swiggy", "zomato", "razorpayzomato", "swiggygenie","dominos"],
    'Household and Rent/recharges': ['electricity', 'water', 'gas', "ashish kumar shrivas","euronetgpay","billdesktez","yagyaraj k joshi","salon"],
    'Entertainment': ['netflix', "prime", 'bookmyshow', "microsoft", "book my show", "isha foundation", "google india digital","disney hotstar"],
    'Dining': ['restaurant', 'coffee',"cafe","MH 14","naturals aundh","sandwich express","shree ashapuri dinin","kamal fast food","shakes n flakes","hotel","f c chat house","vasant s shetty"],
    "Gym related": ["the fitness temple", "muscle blaze", "healthkart", "protien", "muscle"],
    "Investment": ["indianclearingcorpor", "anjana gogia wo vija","indian clearing corp", "groww","zerodha","npstrust"],
    "Atm Deduction": ["nwd"],
    "Credit Card": ["billpay"],
    "Furniture rent": ["rentomojo"],
    "Shopping": ["myntra", "amazon", "crossword bookstores", "chidiya udd"],
    "Bike/Scooty": ["onepoint bike servic"],
    "Petrol": ["petrol", "famous auto centre","hp","pure fuel point","fuel","shri sai service"],
    "Ola/Uber": ["olamoney1","sanjay kumar"],
    "Tea/coffee/snacks":["shekhar nagnath sont","foods","swaraj tea and snack","sumit hospitality"],
    "Medical_expense":["naturopathy centre","plus medico","wellness forever","sunita shalin patil","sanjeev manohar dole"],
    "FastTAG":["fastag"],
    "Gifts/cakes":["sanket gogia","w s bakers","cake","ferocraft"],
    "Emergency Fund":["nishesh"],
    "Auto Deduction":["auto deduction","Auto Deduction"]
}


    # Function to categorize expenses
    def categorize_expense(description):
        for category, keywords in categories.items():
            if any(keyword in description.lower() for keyword in keywords):
                return category
        return 'Other'

    # Apply categorization to each transaction
    df['Category'] = df['Narration'].apply(categorize_expense)

    # Group by Category and sum the 'Withdrawal Amt.' for each category
    #category_wise_amount = df.groupby("Category")["Withdrawal Amt."].sum()
    #category_sort = category_wise_amount.sort_values(ascending=False)
    #print("Category-wise Withdrawal Amount Sum:\n", category_sort)


    return df  # Modify this line based on your analysis results

def main():
        st.title("Monthly Expense Analysis")

    # File upload
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

        if uploaded_file is not None:
            # Perform analysis
            result_df = analyze_monthly_expenses(uploaded_file)

            # Dropdown filter for Category
            selected_category = st.selectbox("Select Category", ['All'] + list(result_df['Category'].unique()))

            # Dropdown filter for Name
            selected_name = st.selectbox("Select Name", ['All'] + list(result_df['Name'].unique()))

            result=result_df[["Name","Category","Date2","Withdrawal Amt."]]

            # Apply filters to the DataFrame
            filtered_df = result[
                ((selected_category == 'All') | (result['Category'] == selected_category)) &
                ((selected_name == 'All') | (result['Name'] == selected_name))
            ]

            # Display filtered results
            st.write("Filtered Data:")
            st.write(filtered_df)
    
        category_wise_sum = result_df.groupby("Category")["Withdrawal Amt."].sum().sort_values(ascending=False)
        st.write("Category-wise Withdrawal Amount Sum:")
        st.title('Category-wise Withdrawal Amount Sum:')
        st.write(category_wise_sum)  

            # Create a DataFrame from the Series
        category_df = pd.DataFrame({'Category': category_wise_sum.index, 'Withdrawal Amount Sum': category_wise_sum.values})
        
        # Plot the bar chart
    

        st.bar_chart(category_df.set_index('Category'))

        online_foodf=result_df[result_df["Category"]=="Online Food"]
        daily_spending = online_foodf.groupby('Date2')['Withdrawal Amt.'].sum()

        st.write("online food expense:")
        st.title('Daily Spending on Online Food')
        st.write(daily_spending)

        daily_spending_df = pd.DataFrame({'Date': daily_spending.index, 'Total Amount Spent': daily_spending.values})

        # Plotting using Streamlit
        st.line_chart(daily_spending_df.set_index('Date'))

        # Convert to numeric type
        category_sort = pd.to_numeric(category_wise_sum)[:8]

        # Pie Chart
        plt.figure(figsize=(8, 8))
        plt.pie(category_sort, labels=category_sort.index, autopct='%1.1f%%', startangle=90)
        st.title('Category-wise Withdrawal Amount Distribution')

        # Display the pie chart using st.pyplot()
        st.pyplot()

        # Optionally, you can also display the data as a table
        st.write("Category-wise Withdrawal Amount Distribution:")
        st.write(category_sort)

        name_wise_amount = result_df.groupby("Name")["Withdrawal Amt."].sum()
        name_sort = name_wise_amount.sort_values(ascending=False)
        name_sort = name_sort[:15]

        st.title('Name wise Withdrawal Amount Distribution')

        st.write(name_sort)

        name_df = pd.DataFrame({'Name': name_sort.index, 'Withdrawal Amount Sum': name_sort.values})

        st.bar_chart(name_df.set_index('Name'))  # Use 'Name' as the index

        st.title("Percenatage distribution by Name")

        # Pie Chart
        name_sort=name_sort[:7]
        plt.figure(figsize=(8, 8))
        plt.pie(name_sort, labels=name_sort.index, autopct='%1.1f%%', startangle=90)
        st.pyplot()

      

        # Assuming you have a DataFrame 'result_df' with the necessary data

        # Streamlit app
        st.title("Daily Expense Overview")

        # Group by Date2 and sum the 'Withdrawal Amt.' for each date
        #daily_expenses = result_df.groupby(result_df['Date2'].dt.to_period("D"))['Withdrawal Amt.'].sum()
        daily_expenses = result_df.groupby('Date2')['Withdrawal Amt.'].sum()
        st.write(daily_expenses)

        daily_expenses_df = pd.DataFrame({'Date': daily_expenses.index, 'Total Amount Spent': daily_expenses.values})


        # Plotting using Streamlit
        st.line_chart(daily_expenses_df.set_index('Date'))


















        # Additional Streamlit options
       

        










        #st.header("Monthly Expense Overview")
        #st.line_chart(result_df.groupby(result_df['Date2'].dt.to_period("M"))['Withdrawal Amt.'].sum())

        # Add more Streamlit components as needed based on your analysis results

if __name__ == "__main__":
    main()
