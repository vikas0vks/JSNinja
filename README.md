# **JSNinja**  
"**Hunting Bugs in JavaScript!**"  

![JSNinja Banner](https://github.com/vikas0vks/JSNinja/blob/main/assets/jsninja_banner.jpg)

**JSNinja** is an advanced tool designed to extract URLs and sensitive secrets from JavaScript files. It’s a must-have tool for penetration testers and bug bounty hunters to analyze JS files efficiently and identify valuable data.  

---

## **Features**  
- **URL Extraction**: Automatically extracts URLs from JavaScript files.  
- **Secrets Detection**: Identifies sensitive data like AWS keys, Stripe keys, and more.  
- **Custom Cookie Support**: Option to provide cookies for analyzing authenticated JS files.  
- **Clean Error Handling**: Beautifully formatted error messages for non-200 responses.  
- **Organized Output**: Saves extracted data domain-wise or in a custom directory.  

---

## **How It Works**  
1. The tool accepts a single or multiple JS URLs (manually or via a file).  
2. Fetches the URLs and extracts links and sensitive information.  
3. Saves the extracted data in the output directory:  
   - **URLs**: `<domain>_urls.txt`  
   - **Secrets**: `<domain>_secrets.json`  

---

## **Inspiration**  
This tool is inspired by the amazing project [JSNinja](https://github.com/iamunixtz/JSNinja) by **@iamunixtz**. Their work on bug bounty automation provided a solid foundation and ideas for this project. Do check out their repository for additional insights and tools.  

---

## **Installation**  

### **Requirements**  
- Python 3.8+  
- Required Python libraries: `requests`, `beautifulsoup4`, `colorama` ,`urllib3` 

Install dependencies using:  
```bash
pip install -r requirements.txt
```

Clone this repository:  
```bash
git clone https://github.com/vikas0vks/JSNinja.git
cd JSNinja
```

---

## **Usage**  

### **Run the Tool**  
Run the tool using the following command:  
```bash
python jsninja.py
```

### **Options Available**  
1. **Single URL**: Process a single JS file.  
2. **File Input**: Provide a file containing multiple JS URLs.  
3. **Custom Cookies**: Provide cookies for analyzing authenticated JS files.  
4. **Custom Directory**: Specify a directory name to save extracted data.  

---

## **Output Structure**  
- **URLs**: Saved in `domain_urls.txt`  
- **Secrets**: Saved in `domain_secrets.json`  
- **Error Handling**: Clean and informative error messages for unreachable URLs.  

---

## **Screenshots**  
### Tool in Action:  
![Tool Running Screenshot](https://github.com/vikas0vks/JSNinja/blob/main/assets/running%20jsninja.jpg)

### Output Files:  
![Output Files Screenshot](https://github.com/vikas0vks/JSNinja/blob/main/assets/output_jsninja.jpg)

---

## **Contributing**  
If you find any issues or want to suggest new features, feel free to create a pull request or an issue. 😊  

---

## **License**  
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## **Disclaimer**  
This tool is intended for **educational** and **ethical testing** purposes only. The author is not responsible for any misuse of this tool for illegal activities. 🙏  

