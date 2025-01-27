# clirpiai
This simple script provides ability to interact with the OpenAI using API in various ways using command-line interface on Raspberry PI

1. **Install the Required Dependencies:**

   Ensure you have the necessary Python libraries installed. You can install them using pip:

   ```bash
   pip install openai python-dotenv colorama
   ```

2. **Set Up Your Environment Variables:**

   Create a `.env` file in the same directory as your script and add your OpenAI API key to it. The `.env` file should look like this:

   ```plaintext
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **How to Use the Script:**

   After setting up everything, run the script from the command line using the parameters described in the help section. Below are examples of how to run the script in different modes:

   - **Interactive Mode:**
     ```bash
     python clirpiai.py -i
     ```

   - **Text Mode:**
     ```bash
     python clirpiai.py -t "Your question or message here"
     ```

   - **Read from Standard Input Mode:**
     ```bash
     echo "Your question or message here" | python clirpiai.py -s
     ```

   - **Help:**
     ```bash
     python clirpiai.py -h
     ```
