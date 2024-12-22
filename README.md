# Go-LLM Assignment

## Assignment Description

Create a simple WebApp with the following features:

1. **File Upload**  
   - I should be able to upload a file (only `.xlsx` and `.csv` files).
   
2. **Data Extraction**  
   - I should be able to extract only the numerical values, i.e., columns `C3` and `C4`.
   
3. **API Integration**  
   - I should be able to send the extracted values to the backend via an API.
   
4. **Backend Operations**  
   - In the backend, I should be able to perform mathematical operations (e.g., Average, Sum, etc.) on all the numbers for each of the columns received.
   
5. **Data Storage**  
   - I should be able to store the results of computations (e.g., Average) in a relational database with `session-id/user-id` as the primary key.
   
6. **Result Display**  
   - I should be able to receive and display the results of the computation on the frontend.

**Note:**  
It is essential that you leverage a Language Model (large/small) to generate the code for the mathematical operations that need to be performed on the numerical data in the backend.  
- Example 1: If the intended operation is `[column = “C3”, operation = “average”]`, then the LLM must generate the code to compute the Average.  
- Example 2: If the operation is `[column = “C4”, operation = “std. deviation”]`, then the LLM must generate the code to compute the Standard Deviation.

---

## Project Setup and Running the Code

1. **Clone and setup the repository**  
   ```bash
    git clone git@github.com:Anuj-S62/go-llm-assignment.git
    cd go-llm-assignment
    python3 -m venv .venv
    source .venv/bin/activate 
    cd app
    pip install -r requirements.txt
    ```

2. **Replace the API key**
   - Replace the GPT API key in the server.py file.

3. **Run the server**
   ```bash
   python3 backend/server.py
    ```

4. **Run the WebApp**
 - Open index.html in your browser and test the application.

## Assumption
- The LLM used is OpenAI GPT-4 or GPT-3.5.
- Operations will be performed on single columns only, one at a time.
- Perform any operation on single column at a time.

## Demo Video Drive Link
![Demo Video](https://drive.google.com/file/d/1-3PmmeF6Kz71qt8WqRwM_0bjETiBGJDS/view?usp=drive_link)
